from __future__ import annotations

import json
import os
import csv
import hashlib
from datetime import date
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
CLI = SKILL / "scripts" / "pipeline.py"


class PipelineCliTests(unittest.TestCase):
    def invoke(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONIOENCODING"] = "utf-8"
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, str(CLI), *args], text=True, encoding="utf-8",
            capture_output=True, check=check, env=environment,
        )

    def test_user_can_initialize_and_read_status_through_one_cli(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            created = self.invoke(
                "init", "--project", temp, "--title", "三波纵向研究",
                "--mode", "strict", "--run-id", "cli-run",
            )
            init_payload = json.loads(created.stdout)
            run_dir = Path(init_payload["run_dir"])
            self.assertEqual("active", init_payload["status"])
            self.assertEqual("00_scope", init_payload["current_stage"])
            self.assertTrue(run_dir.is_dir())

            status = self.invoke("status", "--run-dir", str(run_dir))
            status_payload = json.loads(status.stdout)
            self.assertEqual("cli-run", status_payload["run_id"])
            self.assertEqual("strict", status_payload["mode"])
            self.assertEqual(0, status_payload["completion_percent"])

            verification = self.invoke("verify-run", "--run-dir", str(run_dir), check=False)
            self.assertEqual(3, verification.returncode)
            verification_payload = json.loads(verification.stdout)
            self.assertEqual("blocked", verification_payload["status"])
            self.assertEqual("00_scope", verification_payload["stages"][0]["stage"])

            autopilot = self.invoke("autopilot", "--run-dir", str(run_dir), check=False)
            self.assertEqual(3, autopilot.returncode)
            self.assertEqual("00_scope", json.loads(autopilot.stdout)["blocked_stage"])

    def test_user_can_attach_a_versioned_project_pack_without_polluting_generic_references(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            pack = SKILL / "project-packs" / "interparental-conflict-depression-nssi"
            result = json.loads(self.invoke(
                "init", "--project", str(project), "--title", "project pack",
                "--run-id", "pack-run", "--project-pack", str(pack),
            ).stdout)
            run_dir = Path(result["run_dir"])
            self.assertEqual("interparental-conflict-depression-nssi", result["project_pack"]["id"])
            copied = run_dir / "00_项目定标" / "课题包_project_pack"
            self.assertTrue((copied / "pack.json").is_file())
            self.assertTrue((copied / "project-profile.md").is_file())
            self.assertTrue((copied / "presearch-protocol.json").is_file())
            self.assertTrue((copied / "zotero-target.json").is_file())
            self.assertTrue((copied / "data-audit-spec.json").is_file())
            self.assertTrue((copied / "search-plan.json").is_file())
            self.assertTrue((copied / "evidence-coverage.json").is_file())
            self.assertFalse((SKILL / "references" / "project-profile.md").exists())

    def test_source_inventory_hashes_files_without_reading_sensitive_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "inventory", "--run-id", "inventory-run",
            ).stdout)["run_dir"])
            sources = project / "资料"
            sources.mkdir()
            (sources / "data.csv").write_text("id,self_harm\np1,1\n", encoding="utf-8")
            (sources / "protocol.md").write_text("protocol", encoding="utf-8")
            result = json.loads(self.invoke(
                "inventory", "--run-dir", str(run_dir), "--source", str(sources),
            ).stdout)
            self.assertEqual("ready", result["status"])
            self.assertEqual(2, result["file_count"])
            inventory = json.loads(Path(result["inventory_json"]).read_text(encoding="utf-8"))
            data_item = next(item for item in inventory["files"] if item["name"] == "data.csv")
            self.assertEqual("participant-data", data_item["category"])
            self.assertNotIn("p1", json.dumps(inventory))

    def test_legacy_migration_only_copies_recognized_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            legacy = project / "legacy"
            (legacy / "01_scope").mkdir(parents=True)
            (legacy / "01_scope" / "project_brief.md").write_text("# Legacy\n\nverified content", encoding="utf-8")
            (legacy / "raw-data.sav").write_bytes(b"not-real-data")
            result = json.loads(self.invoke(
                "migrate", "--project", str(project), "--legacy-run", str(legacy),
                "--title", "migrated", "--run-id", "migrated-run",
            ).stdout)
            self.assertEqual("migrated-requires-gates", result["status"])
            run_dir = Path(result["run_dir"])
            migrated = run_dir / "00_项目定标" / "项目定标简报_project_brief.md"
            self.assertIn("verified content", migrated.read_text(encoding="utf-8"))
            self.assertFalse((run_dir / "raw-data.sav").exists())
            self.assertEqual("raw-data.sav", result["unmapped_metadata_only"][0]["path"])

    def test_user_can_audit_and_freeze_clean_panel_data(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            init_payload = json.loads(self.invoke(
                "init", "--project", str(project), "--title", "clean panel",
                "--mode", "strict", "--run-id", "data-run",
            ).stdout)
            run_dir = Path(init_payload["run_dir"])
            data = project / "panel.csv"
            with data.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=["id1", "id2", "sex1", "sex2", "y1", "y2"])
                writer.writeheader()
                writer.writerows([
                    {"id1": "p1", "id2": "p1", "sex1": 1, "sex2": 1, "y1": 2, "y2": 3},
                    {"id1": "p2", "id2": "p2", "sex1": 2, "sex2": 2, "y1": 4, "y2": 5},
                ])
            spec = project / "spec.json"
            spec.write_text(json.dumps({
                "profile": "clean-test",
                "id_by_wave": {"T1": "id1", "T2": "id2"},
                "sex_by_wave": {"T1": "sex1", "T2": "sex2"},
                "allowed_sex_values": [1, 2],
                "measures": [
                    {"construct": "outcome", "wave": "T1", "variable": "y1", "expected_min": 0, "expected_max": 10},
                    {"construct": "outcome", "wave": "T2", "variable": "y2", "expected_min": 0, "expected_max": 10},
                ],
                "score_relations": [],
            }, ensure_ascii=False), encoding="utf-8")

            audit = json.loads(self.invoke(
                "audit-data", "--run-dir", str(run_dir), "--data", str(data), "--spec", str(spec),
            ).stdout)
            self.assertEqual([], audit["flags"])
            self.assertEqual(2, audit["shape"]["rows"])

            frozen = json.loads(self.invoke(
                "freeze-data", "--run-dir", str(run_dir), "--data", str(data), "--spec", str(spec),
            ).stdout)
            self.assertEqual("frozen", frozen["status"])
            self.assertTrue(Path(frozen["frozen_data"]).is_file())
            self.assertEqual(2, frozen["rows"])

    def test_flagged_data_requires_exact_auditable_decisions_before_freeze(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "decision gate",
                "--run-id", "decision-run",
            ).stdout)["run_dir"])
            data = project / "panel.csv"
            data.write_text("id1,id2,y1\np1,p1,99\n", encoding="utf-8")
            spec = project / "spec.json"
            spec.write_text(json.dumps({
                "profile": "decision-test", "id_by_wave": {"T1": "id1", "T2": "id2"},
                "sex_by_wave": {}, "measures": [{
                    "construct": "outcome", "wave": "T1", "variable": "y1",
                    "expected_min": 0, "expected_max": 10,
                }], "score_relations": [],
            }), encoding="utf-8")

            blocked = self.invoke(
                "freeze-data", "--run-dir", str(run_dir), "--data", str(data),
                "--spec", str(spec), check=False,
            )
            self.assertEqual(3, blocked.returncode)
            blocked_payload = json.loads(blocked.stdout)
            self.assertEqual("blocked", blocked_payload["status"])
            flag = blocked_payload["flags"][0]
            issue = blocked_payload["issues"][0]
            audit = run_dir / "06_数据管理" / "数据质量审计_data_audit.json"
            import hashlib
            decisions = project / "decisions.json"
            decisions.write_text(json.dumps({
                "schema_version": 1,
                "audit_sha256": hashlib.sha256(audit.read_bytes()).hexdigest(),
                "decisions": [{
                    "issue_id": issue["issue_id"], "flag": flag, "status": "resolved", "resolution": "source-verified",
                    "rationale": "源问卷显示该值为经核验的特殊有效编码。",
                    "evidence": "source-form-page-1", "approved_by": "researcher",
                    "decided_at": date.today().isoformat(),
                }],
            }, ensure_ascii=False), encoding="utf-8")
            frozen = json.loads(self.invoke(
                "freeze-data", "--run-dir", str(run_dir), "--data", str(data),
                "--spec", str(spec), "--decisions", str(decisions),
            ).stdout)
            self.assertEqual("frozen", frozen["status"])
            self.assertEqual(1, len(frozen["resolved_flags"]))
            self.assertTrue(Path(frozen["decision_log"]).is_file())

    def test_linkage_issue_rejects_analysis_accommodation_and_private_register_hides_ids(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "private repair",
                "--run-id", "private-run",
            ).stdout)["run_dir"])
            data = project / "panel.csv"
            data.write_text("id1,id2,y1\nsecret-A,secret-B,2\n", encoding="utf-8")
            spec = project / "spec.json"
            spec.write_text(json.dumps({
                "profile": "private-test", "id_by_wave": {"T1": "id1", "T2": "id2"},
                "sex_by_wave": {}, "measures": [{
                    "construct": "outcome", "wave": "T1", "variable": "y1",
                    "expected_min": 0, "expected_max": 10,
                }], "score_relations": [],
            }), encoding="utf-8")
            private_register = run_dir / "06_数据管理" / ".private" / "issues.jsonl"
            audit = json.loads(self.invoke(
                "audit-data", "--run-dir", str(run_dir), "--data", str(data), "--spec", str(spec),
                "--private-register", str(private_register),
            ).stdout)
            self.assertEqual("linkage", audit["issues"][0]["category"])
            private_text = private_register.read_text(encoding="utf-8")
            self.assertIn("pseudonym", private_text)
            self.assertNotIn("secret-A", private_text)
            self.assertNotIn("secret-B", private_text)

            import hashlib
            decisions = project / "bad-decisions.json"
            audit_path = run_dir / "06_数据管理" / "数据质量审计_data_audit.json"
            decisions.write_text(json.dumps({
                "schema_version": 1, "audit_sha256": hashlib.sha256(audit_path.read_bytes()).hexdigest(),
                "decisions": [{
                    "issue_id": audit["issues"][0]["issue_id"], "flag": audit["flags"][0],
                    "status": "resolved", "resolution": "analysis-accommodation",
                    "rationale": "adjust model", "evidence": "plan", "approved_by": "researcher",
                    "decided_at": date.today().isoformat(),
                }],
            }), encoding="utf-8")
            blocked = self.invoke(
                "freeze-data", "--run-dir", str(run_dir), "--data", str(data), "--spec", str(spec),
                "--decisions", str(decisions), check=False,
            )
            self.assertEqual(3, blocked.returncode)
            self.assertIn("resolution is not allowed", blocked.stdout)

    def test_audit_distinguishes_id_format_candidates_and_item_range_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "item audit",
                "--run-id", "item-audit-run",
            ).stdout)["run_dir"])
            data = project / "panel.csv"
            data.write_text(
                "id1,id2,sex1,sex2,d1,d2,total\n"
                "a01,a1,1,1,1,4,5\n"
                "b02,b9,2,22,5,2,7\n",
                encoding="utf-8",
            )
            spec = project / "spec.json"
            spec.write_text(json.dumps({
                "profile": "item-audit-test",
                "id_by_wave": {"T1": "id1", "T2": "id2"},
                "id_normalization": {"mode": "alpha-prefix-integer-suffix"},
                "sex_by_wave": {"T1": "sex1", "T2": "sex2"},
                "allowed_sex_values": [1, 2],
                "measures": [],
                "item_sets": [{
                    "construct": "depression", "wave": "T1",
                    "variables": ["d1", "d2"], "expected_min": 1, "expected_max": 4,
                }],
                "score_relations": [{
                    "name": "sum", "target": "total", "coefficients": {"d1": 1, "d2": 1},
                }],
            }), encoding="utf-8")
            private_register = run_dir / "06_数据管理" / ".private" / "issues.jsonl"

            audit = json.loads(self.invoke(
                "audit-data", "--run-dir", str(run_dir), "--data", str(data),
                "--spec", str(spec), "--private-register", str(private_register),
            ).stdout)

            linkage = audit["ids"]["rowwise_mismatch"]["T1-T2"]
            self.assertEqual(2, linkage["raw_mismatch"])
            self.assertEqual(1, linkage["format_only_candidates"])
            self.assertEqual(1, linkage["normalized_mismatch"])
            self.assertEqual(1, audit["item_sets"][0]["invalid_cell_count"])
            categories = {item["category"] for item in audit["issues"]}
            self.assertIn("linkage-format", categories)
            self.assertIn("linkage", categories)
            self.assertIn("item-range", categories)
            self.assertIn("sex-code", categories)
            self.assertNotIn('"a01"', private_register.read_text(encoding="utf-8"))

    def test_project_pack_copies_measurement_map(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            pack = SKILL / "project-packs" / "interparental-conflict-depression-nssi"
            result = json.loads(self.invoke(
                "init", "--project", temp, "--title", "measurement map",
                "--run-id", "measurement-map-run", "--project-pack", str(pack),
            ).stdout)
            copied = Path(result["run_dir"]) / "00_项目定标" / "课题包_project_pack"
            self.assertTrue((copied / "measurement-map.json").is_file())

    def test_prepare_analysis_data_rescores_items_without_exporting_identifiers(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "prepare data",
                "--run-id", "prepare-run",
            ).stdout)["run_dir"])
            data = project / "raw.csv"
            data.write_text(
                "id1,sex1,d1,d2,f1,f2,s1,s2,c1,c2\n"
                "a01,1,1,4,0,2,,3,1,5\n"
                "b02,9,8,2,1,1,2,2,2,4\n",
                encoding="utf-8",
            )
            measurement_map = project / "measurement-map.json"
            measurement_map.write_text(json.dumps({
                "schema_version": 1,
                "constructs": {
                    "depressive_symptoms": {
                        "response_range": [1, 4], "reverse_items": [2],
                        "raw_selectors": {"T1": {"template": "d{item}", "start": 1, "end": 2}},
                        "analysis_scores": {"T1": "depression_score_t1"},
                    },
                    "nssi": {
                        "frequency_range": [0, 3], "severity_range": [0, 4],
                        "frequency_selectors": {"T1": {"template": "f{item}", "start": 1, "end": 2}},
                        "severity_selectors": {"T1": {"template": "s{item}", "start": 1, "end": 2}},
                        "analysis_scores": {"T1": "nssi_level_t1"},
                    },
                    "interparental_conflict": {
                        "response_range": [1, 5], "high_conflict_reverse_items": [1],
                        "raw_selectors": {"T1": {"template": "c{item}", "start": 1, "end": 2}},
                        "analysis_scores": {"T1": "conflict_score_t1"},
                    },
                },
                "identifiers_and_covariates": {
                    "id_by_wave": {"T1": "id1"}, "sex_by_wave": {"T1": "sex1"},
                },
            }), encoding="utf-8")

            result = json.loads(self.invoke(
                "prepare-analysis-data", "--run-dir", str(run_dir),
                "--data", str(data), "--measurement-map", str(measurement_map),
            ).stdout)
            self.assertEqual("prepared", result["status"])
            output = Path(result["analysis_data"])
            with output.open(encoding="utf-8-sig") as handle:
                prepared = list(csv.DictReader(handle))
            self.assertNotIn("id1", prepared[0])
            self.assertEqual("a", prepared[0]["school_code"])
            self.assertEqual("2.0", prepared[0]["depression_score_t1"])
            self.assertEqual("6.0", prepared[0]["nssi_level_t1"])
            self.assertEqual("10.0", prepared[0]["conflict_score_t1"])
            self.assertEqual("", prepared[1]["sex_analysis"])
            self.assertGreater(result["invalid_cells_set_missing"], 0)

    def test_zotero_sync_exports_imports_and_audits_pdf_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "zotero sync",
                "--run-id", "zotero-run",
            ).stdout)["run_dir"])
            helper = project / "fake_zotero.py"
            class ZoteroHandler(BaseHTTPRequestHandler):
                def do_GET(self) -> None:
                    body = b"@article{x, title={Test paper}, author={Li}, year={2024}, doi={10.1/test}}"
                    self.send_response(200)
                    self.send_header("Content-Type", "application/x-bibtex")
                    self.send_header("Total-Results", "1")
                    self.end_headers()
                    self.wfile.write(body)

                def log_message(self, *_args) -> None:
                    return

            server = ThreadingHTTPServer(("127.0.0.1", 0), ZoteroHandler)
            server_thread = threading.Thread(target=server.serve_forever, daemon=True)
            server_thread.start()
            helper.write_text(
                "import json, pathlib, sys\n"
                f"if sys.argv[1] == 'status': print(json.dumps({{'api_running': True, 'connector_running': True, 'base_url': 'http://127.0.0.1:{server.server_port}'}}))\n"
                "elif sys.argv[1] == 'collections': print(json.dumps([{'key': 'TESTKEY', 'name': 'Test Collection'}]))\n",
                encoding="utf-8",
            )
            pdf_dir = run_dir / "文献" / "02_全文PDF"
            (pdf_dir / "paper.pdf").write_bytes(b"%PDF-1.4\n%%EOF")

            try:
                result = json.loads(self.invoke(
                    "sync-zotero", "--run-dir", str(run_dir), "--helper", str(helper),
                    "--collection-name", "Test Collection", "--collection-key", "TESTKEY",
                ).stdout)
                self.assertEqual("complete", result["status"])
                self.assertEqual(1, result["imported_records"])
                self.assertEqual(1, result["pdf_count"])
                self.assertTrue(Path(result["zotero_manifest"]).is_file())
                self.assertTrue(Path(result["pdf_manifest"]).is_file())
            finally:
                server.shutdown()
                server.server_close()
                server_thread.join(timeout=5)

    def test_export_publication_files_builds_docx_pdf_and_submission_manifests(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "publication files",
                "--run-id", "publication-run",
            ).stdout)["run_dir"])
            manuscript = project / "manuscript.md"
            manuscript.write_text("# Test title\n\n## Abstract\n\nVerified text.\n", encoding="utf-8")
            result = json.loads(self.invoke(
                "export-publication-files", "--run-dir", str(run_dir),
                "--manuscript", str(manuscript), "--title", "Test title",
            ).stdout)
            self.assertEqual("complete", result["status"])
            self.assertTrue(Path(result["manuscript_docx"]).is_file())
            self.assertTrue(Path(result["manuscript_pdf"]).read_bytes().startswith(b"%PDF-"))
            self.assertTrue(Path(result["tables_figures_manifest"]).is_file())
            self.assertTrue(Path(result["submission_manifest"]).is_file())

    def test_user_can_generate_auditable_longitudinal_analysis_code(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "RI-CLPM",
                "--mode", "strict", "--run-id", "analysis-run",
            ).stdout)["run_dir"])
            frozen = project / "frozen.csv"
            columns = [
                "conflict_t1", "conflict_t2", "conflict_t3",
                "depression_t1", "depression_t2", "depression_t3",
                "nssi_t1", "nssi_t2", "nssi_t3", "sex", "school",
            ]
            with frozen.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=columns)
                writer.writeheader()
                writer.writerow({name: 1 for name in columns})
            spec = project / "analysis-spec.json"
            spec.write_text(json.dumps({
                "schema_version": 1,
                "status": "frozen",
                "blocking_items": [],
                "profile": "three-construct-panel",
                "waves": ["T1", "T2", "T3"],
                "constructs": {
                    "conflict": {"variables": {"T1": "conflict_t1", "T2": "conflict_t2", "T3": "conflict_t3"}, "distribution": "continuous"},
                    "depression": {"variables": {"T1": "depression_t1", "T2": "depression_t2", "T3": "depression_t3"}, "distribution": "continuous"},
                    "nssi": {"variables": {"T1": "nssi_t1", "T2": "nssi_t2", "T3": "nssi_t3"}, "distribution": "zero-heavy"}
                },
                "group_variable": "sex",
                "cluster_variable": "school",
                "estimator": "MLR",
                "missing": "FIML"
            }, ensure_ascii=False), encoding="utf-8")

            generated = json.loads(self.invoke(
                "generate-analysis", "--run-dir", str(run_dir),
                "--data", str(frozen), "--spec", str(spec),
            ).stdout)
            self.assertEqual("ready", generated["status"])
            self.assertGreaterEqual(len(generated["code_files"]), 6)
            model_text = Path(generated["code_files"][2]).read_text(encoding="utf-8")
            self.assertIn("RI_conflict", model_text)
            self.assertIn("RI_conflict ~~ 0*w_depression_T1", model_text)
            self.assertIn("RI_conflict ~~ 0*w_nssi_T3", model_text)
            self.assertIn("group.equal", Path(generated["code_files"][3]).read_text(encoding="utf-8"))
            self.assertIn("zero-heavy", Path(generated["code_files"][4]).read_text(encoding="utf-8"))

            if os.name == "nt":
                fake_rscript = project / "fake-rscript.cmd"
                fake_rscript.write_text(
                    "@echo off\n"
                    "if \"%1\"==\"--version\" (echo R version 4.5.0 & exit /b 0)\n"
                    "if \"%1\"==\"-e\" (\n"
                    "echo dplyr 1.0.0\n"
                    "echo jsonlite 1.0.0\n"
                    "echo lavaan 1.0.0\n"
                    "echo psych 1.0.0\n"
                    "echo readr 1.0.0\n"
                    "echo semTools 1.0.0\n"
                    "echo simsem 1.0.0\n"
                    "echo stats 1.0.0\n"
                    "exit /b 0\n"
                    ")\n"
                    "if \"%1\"==\"-e\" (echo dplyr 1.1.4& echo jsonlite 2.0.0& echo lavaan 0.6.20& echo psych 2.5.6& echo readr 2.1.5& echo semTools 0.5.7& echo simsem 0.5.17& echo stats 4.5.0& exit /b 0)\n"
                    "for %%F in (\"%1\") do set base=%%~nF\n"
                    "if \"%base%\"==\"01_measurement_gate\" (echo ok>..\\measurement_score_summary.csv & echo {}>..\\sex_measurement_gate.json)\n"
                    "if \"%base%\"==\"02_ri_clpm\" (echo ok>..\\ri_clpm_parameters.csv & echo ok>..\\ri_clpm_fit.csv & echo ok>..\\ri_clpm_fit.rds)\n"
                    "if \"%base%\"==\"03_sex_group_comparison\" (echo ok>..\\sex_group_constraint_test.txt & echo {}>..\\sex_group_comparison.json)\n"
                    "if \"%base%\"==\"04_distribution_sensitivity\" echo ok>..\\distribution_sensitivity_fits.rds\n"
                    "if \"%base%\"==\"05_power_simulation\" echo ok>..\\power_simulation_plan.rds\n"
                    "if \"%base%\"==\"06_descriptives_missingness\" (echo ok>..\\descriptives.csv & echo ok>..\\missingness.csv)\n"
                    "if \"%base%\"==\"07_export_machine_output\" echo {}>..\\model_output.json\n"
                    "exit /b 0\n",
                    encoding="utf-8",
                )
            else:
                fake_rscript = project / "fake-rscript"
                fake_rscript.write_text(
                    "#!/bin/sh\n"
                    "[ \"$1\" = \"--version\" ] && { echo 'R version 4.5.0'; exit 0; }\n"
                    "[ \"$1\" = \"-e\" ] && { for p in dplyr jsonlite lavaan psych readr semTools simsem stats; do echo \"$p 1.0.0\"; done; exit 0; }\n"
                    "[ \"$1\" = \"-e\" ] && { printf 'dplyr 1.1.4\\njsonlite 2.0.0\\nlavaan 0.6.20\\npsych 2.5.6\\nreadr 2.1.5\\nsemTools 0.5.7\\nsimsem 0.5.17\\nstats 4.5.0\\n'; exit 0; }\n"
                    "base=$(basename \"$1\" .R)\n"
                    "[ \"$base\" = \"01_measurement_gate\" ] && { echo ok > ../measurement_score_summary.csv; echo '{}' > ../sex_measurement_gate.json; }\n"
                    "[ \"$base\" = \"02_ri_clpm\" ] && { echo ok > ../ri_clpm_parameters.csv; echo ok > ../ri_clpm_fit.csv; echo ok > ../ri_clpm_fit.rds; }\n"
                    "[ \"$base\" = \"03_sex_group_comparison\" ] && { echo ok > ../sex_group_constraint_test.txt; echo '{}' > ../sex_group_comparison.json; }\n"
                    "[ \"$base\" = \"04_distribution_sensitivity\" ] && echo ok > ../distribution_sensitivity_fits.rds\n"
                    "[ \"$base\" = \"05_power_simulation\" ] && echo ok > ../power_simulation_plan.rds\n"
                    "[ \"$base\" = \"06_descriptives_missingness\" ] && { echo ok > ../descriptives.csv; echo ok > ../missingness.csv; }\n"
                    "[ \"$base\" = \"07_export_machine_output\" ] && echo '{}' > ../model_output.json\n"
                    "exit 0\n",
                    encoding="utf-8",
                )
                fake_rscript.chmod(0o755)
            execution = self.invoke(
                "run-analysis", "--run-dir", str(run_dir), "--manifest", generated["manifest"],
                "--rscript", str(fake_rscript), check=False,
            )
            self.assertEqual(0, execution.returncode, execution.stdout + execution.stderr)
            executed = json.loads(execution.stdout)
            self.assertEqual("executed", executed["status"])
            self.assertEqual("requires-result-validation", executed["validation_status"])
            self.assertTrue(Path(executed["execution_manifest"]).is_file())
            self.assertTrue(Path(executed["model_output"]).is_file())

    def test_generate_analysis_blocks_unfrozen_or_unresolved_spec(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "analysis readiness",
                "--run-id", "analysis-readiness-run",
            ).stdout)["run_dir"])
            data = project / "frozen.csv"
            data.write_text(
                "x_t1,x_t2,x_t3,y_t1,y_t2,y_t3\n1,1,1,1,1,1\n",
                encoding="utf-8",
            )
            base_spec = {
                "schema_version": 1,
                "waves": ["T1", "T2", "T3"],
                "measurement_mode": "score-comparability",
                "constructs": {
                    "x": {"variables": {"T1": "x_t1", "T2": "x_t2", "T3": "x_t3"}},
                    "y": {"variables": {"T1": "y_t1", "T2": "y_t2", "T3": "y_t3"}},
                },
            }
            cases = [
                ({**base_spec, "status": "draft", "blocking_items": []}, "not frozen"),
                ({**base_spec, "status": "frozen", "blocking_items": ["wave dates unresolved"]}, "blocking_items"),
            ]
            for index, (payload, expected_error) in enumerate(cases):
                spec = project / f"spec-{index}.json"
                spec.write_text(json.dumps(payload), encoding="utf-8")
                result = self.invoke(
                    "generate-analysis", "--run-dir", str(run_dir),
                    "--data", str(data), "--spec", str(spec), check=False,
                )
                self.assertEqual(3, result.returncode)
                blocked = json.loads(result.stdout)
                self.assertEqual("blocked", blocked["status"])
                self.assertTrue(any(expected_error in error for error in blocked["errors"]))
                self.assertEqual([], blocked["code_files"])

    def test_sex_group_free_model_has_group_specific_labels_and_real_equal_constraints(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "group constraints",
                "--run-id", "group-constraints-run",
            ).stdout)["run_dir"])
            data = project / "frozen.csv"
            data.write_text(
                "x_t1,x_t2,x_t3,y_t1,y_t2,y_t3,sex\n1,1,1,1,1,1,1\n",
                encoding="utf-8",
            )
            spec = project / "spec.json"
            spec.write_text(json.dumps({
                "schema_version": 1,
                "status": "frozen",
                "blocking_items": [],
                "waves": ["T1", "T2", "T3"],
                "measurement_mode": "score-comparability",
                "constructs": {
                    "x": {"variables": {"T1": "x_t1", "T2": "x_t2", "T3": "x_t3"}},
                    "y": {"variables": {"T1": "y_t1", "T2": "y_t2", "T3": "y_t3"}},
                },
                "group_variable": "sex",
                "group_labels": {"1": "male", "2": "female"},
            }), encoding="utf-8")
            generated = json.loads(self.invoke(
                "generate-analysis", "--run-dir", str(run_dir),
                "--data", str(data), "--spec", str(spec),
            ).stdout)
            comparison = Path(generated["code_files"][3]).read_text(encoding="utf-8")
            self.assertIn("riclpm_group_free_model", comparison)
            self.assertIn("c(ar_x_g1, ar_x_g2)*w_x_T1", comparison)
            self.assertIn("riclpm_group_equal_model", comparison)
            self.assertIn("ar_x*w_x_T1", comparison)
            self.assertIn('group.equal = c("regressions")', comparison)
            self.assertIn('fitMeasures(fit_group_free, "npar")', comparison)
            self.assertIn("free_npar <= equal_npar", comparison)
            self.assertIn("sex_group_comparison.json", comparison)

    def test_failed_measurement_invariance_blocks_structural_sex_comparison_with_json_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "measurement gate",
                "--run-id", "measurement-gate-run",
            ).stdout)["run_dir"])
            waves = ["T1", "T2", "T3"]
            columns = [f"{construct}_{wave.lower()}" for construct in ["x", "y"] for wave in waves]
            columns += [f"{construct}{item}_{wave.lower()}" for construct in ["x", "y"] for item in [1, 2] for wave in waves]
            columns.append("sex")
            data = project / "frozen.csv"
            data.write_text(",".join(columns) + "\n" + ",".join("1" for _ in columns) + "\n", encoding="utf-8")
            spec = project / "spec.json"
            spec.write_text(json.dumps({
                "schema_version": 1,
                "status": "frozen",
                "blocking_items": [],
                "waves": waves,
                "measurement_mode": "item-level",
                "constructs": {
                    construct: {
                        "variables": {wave: f"{construct}_{wave.lower()}" for wave in waves},
                        "indicators": {wave: [f"{construct}{item}_{wave.lower()}" for item in [1, 2]] for wave in waves},
                    } for construct in ["x", "y"]
                },
                "group_variable": "sex",
                "group_labels": {"1": "male", "2": "female"},
                "sex_measurement_invariance": {
                    "required_level": "metric",
                    "max_abs_delta_cfi": 0.01,
                    "max_increase_rmsea": 0.015,
                    "max_increase_srmr": 0.03,
                },
            }), encoding="utf-8")
            generated = json.loads(self.invoke(
                "generate-analysis", "--run-dir", str(run_dir),
                "--data", str(data), "--spec", str(spec),
            ).stdout)
            measurement = Path(generated["code_files"][1]).read_text(encoding="utf-8")
            comparison = Path(generated["code_files"][3]).read_text(encoding="utf-8")
            self.assertIn("sex_measurement_gate.json", measurement)
            self.assertIn('required_level <- "metric"', measurement)
            self.assertIn('status = if (sex_gate_passed) "passed" else "blocked"', measurement)
            self.assertIn('read_json("../sex_measurement_gate.json"', comparison)
            self.assertIn('!identical(sex_measurement_gate$status, "passed")', comparison)
            self.assertIn(
                str((run_dir / "07_统计分析" / "sex_measurement_gate.json").resolve()),
                generated["expected_outputs"],
            )

    def test_item_level_spec_generates_configural_metric_scalar_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "invariance",
                "--run-id", "invariance-run",
            ).stdout)["run_dir"])
            data = project / "frozen.csv"
            waves = ["T1", "T2", "T3"]
            columns = [f"x_{wave.lower()}" for wave in waves] + [f"y_{wave.lower()}" for wave in waves]
            columns += [f"{construct}{item}_{wave.lower()}" for construct in ["x", "y"] for item in [1, 2, 3] for wave in waves]
            with data.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=columns)
                writer.writeheader()
                writer.writerow({name: 1 for name in columns})
            spec = project / "spec.json"
            spec.write_text(json.dumps({
                "schema_version": 1, "status": "frozen", "blocking_items": [],
                "waves": waves, "measurement_mode": "item-level",
                "constructs": {
                    construct: {
                        "variables": {wave: f"{construct}_{wave.lower()}" for wave in waves},
                        "indicators": {wave: [f"{construct}{item}_{wave.lower()}" for item in [1, 2, 3]] for wave in waves},
                    } for construct in ["x", "y"]
                },
            }), encoding="utf-8")
            result = json.loads(self.invoke(
                "generate-analysis", "--run-dir", str(run_dir), "--data", str(data),
                "--spec", str(spec),
            ).stdout)
            measurement = Path(result["code_files"][1]).read_text(encoding="utf-8")
            self.assertIn("configural_model", measurement)
            self.assertIn("metric_model", measurement)
            self.assertIn("scalar_model", measurement)
            self.assertIn("delta_cfi", measurement)
            self.assertIn("x1_t1 ~~ x1_t2", measurement)

    def test_verified_model_output_becomes_machine_readable_results(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "results",
                "--run-id", "results-run",
            ).stdout)["run_dir"])
            model_payload = {
                "schema_version": 1, "analysis_id": "model-primary", "sample_n": 882,
                "primary_model": "RI-CLPM", "estimator": "MLR", "converged": True,
                "post_check": True, "fit": {"cfi": 0.96, "rmsea": 0.04, "srmr": 0.05},
                "parameters": [{
                    "result_id": "conflict_to_depression", "term": "T1 conflict -> T2 depression",
                    "role": "primary", "estimate": 0.12, "se": 0.04, "ci_low": 0.04,
                    "ci_high": 0.20, "p_value": 0.003, "standardized": 0.10,
                }], "deviations": [],
                "diagnostics": {"negative_variances": 0, "inadmissible_standardized": 0, "warnings": []},
                "robustness": [{"name": "free-lag", "conclusion": "direction consistent"}],
            }
            model_output = project / "handmade-model-output.json"
            model_output.write_text(json.dumps(model_payload), encoding="utf-8")
            handmade = self.invoke(
                "validate-results", "--run-dir", str(run_dir), "--input", str(model_output), check=False,
            )
            self.assertEqual(3, handmade.returncode)
            self.assertIn("execution manifest missing", " ".join(json.loads(handmade.stdout)["errors"]))

            data = project / "frozen.csv"
            data.write_text("x\n1\n", encoding="utf-8")
            spec = project / "analysis-spec.json"
            spec.write_text(json.dumps({"random_seed": 20260718}), encoding="utf-8")
            code = project / "analysis.R"
            code.write_text('required_packages <- c("jsonlite")\nset.seed(20260718)\n', encoding="utf-8")
            executed_output = run_dir / "07_统计分析" / "model_output.json"
            code_manifest = project / "analysis-code-manifest.json"
            code_manifest.write_text(json.dumps({
                "schema_version": 1, "status": "ready",
                "data": str(data.resolve()), "data_sha256": hashlib.sha256(data.read_bytes()).hexdigest(),
                "spec": str(spec.resolve()), "spec_sha256": hashlib.sha256(spec.read_bytes()).hexdigest(),
                "code_files": [str(code.resolve())],
                "code_hashes": {str(code.resolve()): hashlib.sha256(code.read_bytes()).hexdigest()},
                "expected_outputs": [str(executed_output.resolve())],
            }), encoding="utf-8")
            if os.name == "nt":
                fake_rscript = project / "fake-rscript.cmd"
                fake_rscript.write_text(
                    "@echo off\n"
                    "if \"%1\"==\"--version\" (echo R version 4.5.0 & exit /b 0)\n"
                    "if \"%1\"==\"-e\" (echo jsonlite 2.0.0 & exit /b 0)\n"
                    f'copy /Y "{model_output}" "{executed_output}" >nul\n'
                    "exit /b 0\n",
                    encoding="utf-8",
                )
            else:
                fake_rscript = project / "fake-rscript"
                fake_rscript.write_text(
                    "#!/bin/sh\n"
                    "[ \"$1\" = \"--version\" ] && { echo 'R version 4.5.0'; exit 0; }\n"
                    "[ \"$1\" = \"-e\" ] && { echo 'jsonlite 2.0.0'; exit 0; }\n"
                    f'cp "{model_output}" "{executed_output}"\n',
                    encoding="utf-8",
                )
                fake_rscript.chmod(0o755)
            executed = json.loads(self.invoke(
                "run-analysis", "--run-dir", str(run_dir), "--manifest", str(code_manifest),
                "--rscript", str(fake_rscript),
            ).stdout)
            self.assertEqual("executed", executed["status"])
            verified = json.loads(self.invoke(
                "validate-results", "--run-dir", str(run_dir), "--input", str(executed_output),
            ).stdout)
            self.assertEqual("verified", verified["status"])
            verified_results = json.loads(Path(verified["verified_results"]).read_text(encoding="utf-8"))
            self.assertEqual(882, verified_results["sample_n"])
            self.assertEqual(0.12, verified_results["conflict_to_depression.estimate"])
            self.assertTrue(Path(verified["analysis_manifest"]).is_file())
            gate = self.invoke("gate", "--run-dir", str(run_dir), "--stage", "07_analysis")
            self.assertIn("GATE PASSED", gate.stdout)

            invalid = project / "invalid-output.json"
            invalid.write_text(json.dumps({
                "schema_version": 1, "analysis_id": "bad", "sample_n": 10,
                "primary_model": "RI-CLPM", "estimator": "MLR", "converged": True,
                "post_check": True, "fit": {"cfi": 0.95, "rmsea": 0.05, "srmr": 0.05},
                "parameters": [{
                    "result_id": "bad-variance", "term": "x -> y", "role": "primary",
                    "estimate": 0.1, "se": 0.1, "ci_low": -0.1, "ci_high": 0.3,
                    "p_value": 0.2, "standardized": 0.1,
                }], "deviations": [],
                "diagnostics": {"negative_variances": 1, "inadmissible_standardized": 0, "warnings": ["Heywood case"]},
            }), encoding="utf-8")
            blocked = self.invoke(
                "validate-results", "--run-dir", str(run_dir), "--input", str(invalid), check=False,
            )
            self.assertEqual(3, blocked.returncode)
            blocked_payload = json.loads(blocked.stdout)
            self.assertEqual("blocked", blocked_payload["status"])
            self.assertIn("negative variances", " ".join(blocked_payload["errors"]))

            Path(executed["executions"][0]["log"]).write_text("tampered\n", encoding="utf-8")
            executed_output.write_text(json.dumps(model_payload | {"sample_n": 999}), encoding="utf-8")
            tampered_gate = self.invoke(
                "gate", "--run-dir", str(run_dir), "--stage", "07_analysis", check=False,
            )
            self.assertEqual(1, tampered_gate.returncode)
            self.assertIn("execution log hash mismatch", tampered_gate.stdout)
            self.assertIn("analysis output hash mismatch", tampered_gate.stdout)

    def test_user_can_deduplicate_evidence_with_stable_ids(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "evidence",
                "--run-id", "evidence-run",
            ).stdout)["run_dir"])
            candidates = project / "candidates.csv"
            fields = ["candidate_id", "title", "authors", "year", "doi", "database"]
            with candidates.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows([
                    {"candidate_id": "c1", "title": "A Longitudinal Study", "authors": "Li, A", "year": "2020", "doi": "https://doi.org/10.1000/ABC", "database": "PsycINFO"},
                    {"candidate_id": "c2", "title": "A longitudinal study", "authors": "Li, A", "year": "2020", "doi": "10.1000/abc", "database": "WoS"},
                    {"candidate_id": "c3", "title": "Another Study", "authors": "Wang, B", "year": "2021", "doi": "", "database": "CNKI"},
                ])
            result = json.loads(self.invoke(
                "dedupe-evidence", "--run-dir", str(run_dir), "--input", str(candidates),
            ).stdout)
            self.assertEqual(2, result["unique_records"])
            self.assertEqual(1, result["duplicate_records"])
            with Path(result["deduplicated_file"]).open(encoding="utf-8-sig") as handle:
                deduped = list(csv.DictReader(handle))
            self.assertEqual("10.1000/abc", deduped[0]["doi"])
            self.assertEqual({"study-0001", "study-0002"}, {row["study_id"] for row in deduped})

    def test_user_can_render_only_verified_results_and_claims(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "manuscript",
                "--run-id", "write-run",
            ).stdout)["run_dir"])
            template = project / "template.md"
            template.write_text(
                "# 论文\n\n## 结果\n\n最终样本量为 {{result.sample_n}}。\n\n"
                "## 讨论\n\n{{claim.claim-0001}}\n",
                encoding="utf-8",
            )
            results = project / "results.json"
            results.write_text(json.dumps({"sample_n": 100}), encoding="utf-8")
            claims = project / "claims.csv"
            claim_fields = ["claim_id", "claim_text", "source_type", "source_ids", "evidence_location", "verification_status"]
            with claims.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=claim_fields)
                writer.writeheader()
                writer.writerow({
                    "claim_id": "claim-0001", "claim_text": "该结果属于纵向预测关联，不构成因果证据。",
                    "source_type": "analysis", "source_ids": "model-primary", "evidence_location": "ri_clpm_parameters.csv",
                    "verification_status": "verified",
                })
            references = project / "references.bib"
            references.write_text("@article{seed2020, title={Seed}}\n", encoding="utf-8")

            rendered = json.loads(self.invoke(
                "render-manuscript", "--run-dir", str(run_dir), "--template", str(template),
                "--results", str(results), "--claims", str(claims), "--references", str(references),
            ).stdout)
            manuscript = Path(rendered["manuscript"]).read_text(encoding="utf-8")
            self.assertEqual("ready", rendered["status"])
            self.assertIn("最终样本量为 100", manuscript)
            self.assertIn("不构成因果证据", manuscript)
            self.assertNotIn("{{", manuscript)
            self.assertTrue(Path(rendered["numeric_audit"]).is_file())

            policy = project / "journal-policy.json"
            policy_snapshot = project / "journal-author-guide.html"
            policy_snapshot.write_text("<html><body>Original Article author requirements</body></html>", encoding="utf-8")
            import hashlib
            snapshot_hash = hashlib.sha256(policy_snapshot.read_bytes()).hexdigest()
            policy.write_text(json.dumps({
                "journal": "Test Journal of Psychology", "article_type": "Original Article",
                "checked_at": date.today().isoformat(), "scope_fit": "longitudinal developmental psychology",
                "word_limit": 8000, "ai_policy": "disclose language and coding assistance",
                "data_policy": "restricted adolescent data allowed with a justified statement",
                "official_domains": ["journal.example.edu"],
                "submission_url": "https://journal.example.edu/submit",
                "source_urls": ["https://journal.example.edu/authors"],
                "source_snapshots": [{
                    "url": "https://journal.example.edu/authors", "retrieved_at": date.today().isoformat(),
                    "file": str(policy_snapshot), "sha256": snapshot_hash,
                }]
            }), encoding="utf-8")
            package = json.loads(self.invoke(
                "build-submission", "--run-dir", str(run_dir), "--journal-policy", str(policy),
                "--manuscript", rendered["manuscript"], "--numeric-audit", rendered["numeric_audit"],
                "--claim-audit", rendered["claim_audit"],
            ).stdout)
            self.assertEqual("ready", package["status"])
            self.assertTrue(Path(package["package_dir"]).is_dir())
            self.assertNotIn(".sav", " ".join(package["files"]).lower())
            self.assertTrue(Path(package["simulated_reviews"]).is_file())

            tampered_policy = json.loads(policy.read_text(encoding="utf-8"))
            tampered_policy["source_snapshots"][0]["sha256"] = "0" * 64
            policy.write_text(json.dumps(tampered_policy), encoding="utf-8")
            blocked = self.invoke(
                "build-submission", "--run-dir", str(run_dir), "--journal-policy", str(policy),
                "--manuscript", rendered["manuscript"], "--numeric-audit", rendered["numeric_audit"],
                "--claim-audit", rendered["claim_audit"], check=False,
            )
            self.assertEqual(3, blocked.returncode)
            self.assertIn("snapshot hash mismatch", blocked.stdout)


if __name__ == "__main__":
    unittest.main()
