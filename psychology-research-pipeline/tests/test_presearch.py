from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"
PACK = SKILL / "project-packs" / "interparental-conflict-depression-nssi"
sys.path.insert(0, str(SCRIPTS))

from analysis_runner import resolve_rscript  # noqa: E402
from environment_preflight import R_PACKAGES, r_audit, zotero_audit  # noqa: E402
from zotero_bridge import sync  # noqa: E402


class PresearchTests(unittest.TestCase):
    def invoke(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONIOENCODING"] = "utf-8"
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "pipeline.py"), *args], text=True,
            encoding="utf-8", capture_output=True, check=check, env=environment,
        )

    def init_run(self, project: Path, run_id: str, mode: str = "top-journal-prep") -> Path:
        payload = json.loads(self.invoke(
            "init", "--project", str(project), "--title", "presearch",
            "--mode", mode, "--run-id", run_id, "--project-pack", str(PACK),
        ).stdout)
        return Path(payload["run_dir"])

    def test_presearch_draft_renders_artifacts_but_cannot_advance(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = self.init_run(project, "draft-run")
            result = self.invoke(
                "prepare-presearch", "--run-dir", str(run_dir),
                "--spec", str(PACK / "presearch-protocol.json"), check=False,
            )
            self.assertEqual(3, result.returncode)
            payload = json.loads(result.stdout)
            self.assertEqual("prepared-blocked", payload["status"])
            self.assertFalse(payload["ready_for_search"])
            self.assertTrue((run_dir / "00_项目定标" / "项目定标简报_project_brief.md").is_file())
            self.assertTrue((run_dir / "01_标准与协议" / "检索前准备审计_presearch_readiness.json").is_file())
            self.assertTrue((run_dir / "02_证据检索" / "检索前方案_presearch_protocol.md").is_file())
            gate = self.invoke("gate", "--run-dir", str(run_dir), "--stage", "00_scope", check=False)
            self.assertEqual(1, gate.returncode)
            self.assertIn("pre-search readiness is blocked", gate.stdout)

    def test_presearch_ready_requires_explicit_approval_ethics_and_resolutions(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = self.init_run(project, "ready-run")
            spec = json.loads((PACK / "presearch-protocol.json").read_text(encoding="utf-8"))
            for item in spec["unresolved_items"]:
                if set(item["blocking_stages"]).intersection({"00_scope", "01_protocol", "02_search"}):
                    item["status"] = "resolved"
            spec["approval"] = {
                "scope_status": "approved", "protocol_status": "frozen",
                "approved_by": "research-team", "approved_at": "2026-07-22T00:00:00+08:00",
            }
            spec["ethics"].update({
                "approval_status": "verified", "approval_id": "verified-in-source",
                "consent_status": "verified", "assent_status": "verified",
                "risk_protocol_status": "verified",
            })
            spec_path = project / "approved-presearch.json"
            spec_path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
            result = self.invoke(
                "prepare-presearch", "--run-dir", str(run_dir), "--spec", str(spec_path),
            )
            payload = json.loads(result.stdout)
            self.assertTrue(payload["ready_for_search"])
            gate = self.invoke("gate", "--run-dir", str(run_dir), "--stage", "00_scope", check=False)
            self.assertEqual(0, gate.returncode, gate.stdout)

    def fake_helper(self, root: Path) -> Path:
        helper = root / "fake_zotero.py"
        helper.write_text(
            "import json, sys\n"
            "if sys.argv[1] == 'status': print(json.dumps({'api_running': True, 'connector_running': True, 'base_url': 'http://unused'}))\n"
            "elif sys.argv[1] == 'collections': print(json.dumps([{'key': 'S2I8LT6I', 'name': '\\u65e9\\u671f', 'parentCollection': 'ROOT'}]))\n",
            encoding="utf-8",
        )
        return helper

    def test_zotero_bridge_requires_exact_collection_and_accepts_verified_empty_preflight(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "文献").mkdir()
            helper = self.fake_helper(root)
            with patch("zotero_bridge.fetch_collection_bibtex", return_value=("", 0)):
                missing, missing_code = sync(root, helper)
                self.assertEqual(3, missing_code)
                self.assertEqual("zotero-collection-required", missing["gate"])
                ready, ready_code = sync(
                    root, helper, collection_name="早期", collection_key="S2I8LT6I", allow_empty=True,
                )
            self.assertEqual(0, ready_code)
            self.assertEqual("ready-empty", ready["status"])
            self.assertIsNone(ready["candidate_records"])
            self.assertIn("S2I8LT6I", Path(ready["bibtex"]).name)

    def test_rscript_resolution_uses_r_home_when_path_is_not_configured(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            executable = root / "bin" / "Rscript.exe"
            executable.parent.mkdir()
            executable.write_bytes(b"")
            with patch.dict(os.environ, {"R_HOME": str(root)}, clear=False), patch(
                "analysis_runner.shutil.which", return_value=None,
            ):
                self.assertEqual(executable.resolve(), resolve_rscript("Rscript"))

    def test_environment_preflight_records_r_versions_and_exact_zotero_target(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            executable = root / "Rscript.exe"
            executable.write_bytes(b"test executable")
            package_output = "\n".join(f"{name}\t1.0" for name in R_PACKAGES)
            completed = [
                subprocess.CompletedProcess([], 0, stdout="", stderr="Rscript (R) version 4.6.1"),
                subprocess.CompletedProcess([], 0, stdout=package_output, stderr=""),
            ]
            with patch("environment_preflight.resolve_rscript", return_value=executable), patch(
                "environment_preflight.subprocess.run", side_effect=completed,
            ):
                r_result = r_audit("Rscript")
            self.assertTrue(r_result["ready"])
            self.assertEqual(len(R_PACKAGES), len(r_result["packages"]))

            helper = self.fake_helper(root)
            zotero_result = zotero_audit(root, helper, "早期", "S2I8LT6I")
            self.assertTrue(zotero_result["ready"])
            self.assertEqual("S2I8LT6I", zotero_result["matched_collection"]["key"])


if __name__ == "__main__":
    unittest.main()
