from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
import hashlib
from pathlib import Path

from jsonschema import Draft202012Validator


SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"


class ResearchHarnessTests(unittest.TestCase):
    def run_script(self, name: str, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONIOENCODING"] = "utf-8"
        return subprocess.run(
            [sys.executable, str(SCRIPTS / name), *args], text=True, encoding="utf-8",
            capture_output=True, check=check, env=environment,
        )

    def init_run(self, project: Path, run_id: str = "harness-run") -> Path:
        result = self.run_script(
            "pipeline.py", "init", "--project", str(project), "--title", "受控科研任务",
            "--run-id", run_id,
        )
        return Path(json.loads(result.stdout)["run_dir"])

    def test_contract_models_emit_valid_machine_schemas(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            result = self.run_script("contracts.py", "emit-schemas", "--output-dir", str(output))
            payload = json.loads(result.stdout)
            self.assertEqual("complete", payload["status"])
            expected = {
                "task-envelope.schema.json", "role-result.schema.json",
                "tool-capability.schema.json", "loop-policy.schema.json",
                "evidence-ledger.schema.json",
            }
            self.assertEqual(expected, {path.name for path in output.glob("*.json")})
            for path in output.glob("*.json"):
                schema = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual("https://json-schema.org/draft/2020-12/schema", schema["$schema"])
                Draft202012Validator.check_schema(schema)

    def test_versioned_contract_schemas_match_typed_models(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            generated = Path(temp)
            self.run_script("contracts.py", "emit-schemas", "--output-dir", str(generated))
            for generated_path in generated.glob("*.json"):
                versioned_path = SKILL / "schemas" / generated_path.name
                self.assertTrue(versioned_path.is_file(), generated_path.name)
                self.assertEqual(
                    json.loads(generated_path.read_text(encoding="utf-8")),
                    json.loads(versioned_path.read_text(encoding="utf-8")),
                )

    def test_user_can_dispatch_a_hash_bound_controlled_role_task(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = self.init_run(project)
            source = project / "verified-source.txt"
            source.write_text("verified metadata", encoding="utf-8")
            task = project / "task.json"
            task.write_text(json.dumps({
                "schema_version": 1,
                "task_id": "TASK-EVIDENCE-001",
                "run_id": "harness-run",
                "stage": "02_search",
                "role": "evidence",
                "action": "verify metadata",
                "inputs": [{
                    "path": str(source.resolve()),
                    "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                    "role": "evidence",
                    "sensitive": False,
                }],
                "allowed_tools": ["crossref", "openalex"],
                "human_approval_required": False,
                "max_retries": 2,
                "reads_primary_results": False,
            }), encoding="utf-8")
            result = self.run_script(
                "pipeline.py", "dispatch-task", "--run-dir", str(run_dir), "--spec", str(task),
            )
            payload = json.loads(result.stdout)
            self.assertEqual("dispatched", payload["status"])
            task_state = Path(payload["task_state"])
            self.assertTrue(task_state.is_file())
            stored = json.loads(task_state.read_text(encoding="utf-8"))
            self.assertEqual("evidence", stored["envelope"]["role"])
            self.assertEqual(1, stored["next_attempt"])

    def test_transient_failures_retry_once_then_stop_with_auditable_reason(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = self.init_run(project, "bounded-loop")
            source = project / "source.txt"
            source.write_text("source", encoding="utf-8")
            task = project / "task.json"
            task.write_text(json.dumps({
                "schema_version": 1, "task_id": "TASK-LOOP-001", "run_id": "bounded-loop",
                "stage": "02_search", "role": "evidence", "action": "retrieve metadata",
                "inputs": [{"path": str(source.resolve()), "sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "role": "evidence", "sensitive": False}],
                "allowed_tools": ["crossref"], "human_approval_required": False,
                "max_retries": 1, "reads_primary_results": False,
            }), encoding="utf-8")
            self.run_script("pipeline.py", "dispatch-task", "--run-dir", str(run_dir), "--spec", str(task))
            result_path = project / "result.json"
            result_payload = {
                "schema_version": 1, "task_id": "TASK-LOOP-001", "status": "failed",
                "inputs": [], "outputs": [], "decisions": [], "unresolved_items": [],
                "human_approval_required": False, "stop_reason": "temporary API timeout",
                "error_class": "network-transient", "attempt": 1,
                "read_primary_results": False, "analysis_classification": "not-applicable",
            }
            result_path.write_text(json.dumps(result_payload), encoding="utf-8")
            first = json.loads(self.run_script(
                "pipeline.py", "resume-task", "--run-dir", str(run_dir),
                "--task-id", "TASK-LOOP-001", "--result", str(result_path),
            ).stdout)
            self.assertEqual("retrying", first["status"])
            result_payload["attempt"] = 2
            result_path.write_text(json.dumps(result_payload), encoding="utf-8")
            second = json.loads(self.run_script(
                "pipeline.py", "resume-task", "--run-dir", str(run_dir),
                "--task-id", "TASK-LOOP-001", "--result", str(result_path),
                check=False,
            ).stdout)
            self.assertEqual("blocked", second["status"])
            self.assertIn("retry limit", second["stop_reason"])

    def test_completed_task_verification_rejects_tampered_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = self.init_run(project, "verify-task")
            source = project / "source.txt"
            source.write_text("source", encoding="utf-8")
            task = project / "task.json"
            task.write_text(json.dumps({
                "schema_version": 1, "task_id": "TASK-VERIFY-001", "run_id": "verify-task",
                "stage": "02_search", "role": "evidence", "action": "verify one record",
                "inputs": [{"path": str(source.resolve()), "sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "role": "evidence", "sensitive": False}],
                "allowed_tools": ["crossref"], "human_approval_required": False,
                "max_retries": 0, "reads_primary_results": False,
            }), encoding="utf-8")
            self.run_script("pipeline.py", "dispatch-task", "--run-dir", str(run_dir), "--spec", str(task))
            output = project / "verified.json"
            output.write_text('{"status":"verified"}', encoding="utf-8")
            result = project / "result.json"
            result.write_text(json.dumps({
                "schema_version": 1, "task_id": "TASK-VERIFY-001", "status": "complete",
                "inputs": [], "outputs": [{"path": str(output.resolve()), "sha256": hashlib.sha256(output.read_bytes()).hexdigest(), "role": "output", "sensitive": False}],
                "decisions": [], "unresolved_items": [], "human_approval_required": False,
                "stop_reason": "", "error_class": "not-applicable", "attempt": 1,
                "read_primary_results": False, "analysis_classification": "not-applicable",
            }), encoding="utf-8")
            self.run_script(
                "pipeline.py", "resume-task", "--run-dir", str(run_dir),
                "--task-id", "TASK-VERIFY-001", "--result", str(result),
            )
            verified = json.loads(self.run_script(
                "pipeline.py", "verify-task", "--run-dir", str(run_dir), "--task-id", "TASK-VERIFY-001",
            ).stdout)
            self.assertEqual("verified", verified["status"])
            output.write_text('{"status":"changed"}', encoding="utf-8")
            tampered = self.run_script(
                "pipeline.py", "verify-task", "--run-dir", str(run_dir), "--task-id", "TASK-VERIFY-001",
                check=False,
            )
            self.assertEqual(3, tampered.returncode)
            self.assertIn("provenance mismatch", tampered.stdout)

    def test_retrieval_index_contains_only_fulltext_verified_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = self.init_run(project, "evidence-index")
            ledger = project / "ledger.jsonl"
            base = {
                "schema_version": 1, "candidate_id": "C-001", "title": "Verified paper",
                "doi": "10.1000/verified", "zotero_item_key": "ABCD1234",
                "study_design": "three-wave longitudinal", "sample": "adolescents",
                "measures": ["interparental conflict", "depressive symptoms"], "waves": "3",
                "effect_estimate": "standardized path", "uncertainty": "95% CI",
                "claim_ids": ["CL-001"], "evidence_location": "p. 8, Table 2",
                "correction_status": "none-found",
            }
            records = [
                {**base, "evidence_id": "EV-001", "verification_status": "fulltext-verified"},
                {**base, "evidence_id": "EV-002", "candidate_id": "C-002", "title": "Pending paper", "verification_status": "pending"},
            ]
            ledger.write_text("\n".join(json.dumps(item) for item in records) + "\n", encoding="utf-8")
            result = json.loads(self.run_script(
                "pipeline.py", "build-evidence-index", "--run-dir", str(run_dir), "--ledger", str(ledger),
            ).stdout)
            self.assertEqual("complete", result["status"])
            index = json.loads(Path(result["index"]).read_text(encoding="utf-8"))
            self.assertEqual(["EV-001"], [item["evidence_id"] for item in index["records"]])
            self.assertEqual(1, result["excluded_unverified"])
            self.assertIn(".cache", result["index"])

    def test_tool_registry_is_unique_and_contract_valid(self) -> None:
        result = json.loads(self.run_script(
            "tool_registry.py", "validate", "--registry",
            str(SKILL / "references" / "tool-capabilities.json"),
        ).stdout)
        self.assertEqual("valid", result["status"])
        self.assertEqual(7, result["count"])
        self.assertEqual(
            {"chrome", "zotero", "rscript", "quarto", "crossref", "openalex", "obsidian"},
            set(result["tool_ids"]),
        )

    def test_sensitive_input_and_significance_retry_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = self.init_run(project, "guardrails")
            source = project / "row-level-nssi.csv"
            source.write_text("participant,nssi\n001,1\n", encoding="utf-8")
            task = project / "task.json"
            task.write_text(json.dumps({
                "schema_version": 1, "task_id": "TASK-SENSITIVE-001", "run_id": "guardrails",
                "stage": "02_search", "role": "evidence", "action": "index raw data",
                "inputs": [{"path": str(source.resolve()), "sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "role": "input", "sensitive": True}],
                "allowed_tools": ["retrieval-index"], "human_approval_required": False,
                "max_retries": 1, "reads_primary_results": False,
            }), encoding="utf-8")
            blocked = self.run_script(
                "pipeline.py", "dispatch-task", "--run-dir", str(run_dir), "--spec", str(task), check=False,
            )
            self.assertEqual(3, blocked.returncode)
            self.assertIn("sensitive", blocked.stdout.lower())

    def test_dual_source_metadata_verification_flags_conflicts(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            candidate = root / "candidate.json"
            crossref = root / "crossref.json"
            openalex = root / "openalex.json"
            output = root / "verified.json"
            candidate.write_text(json.dumps({
                "doi": "10.1000/example", "title": "Dynamic relations in adolescence",
                "year": 2022, "authors": ["Li", "Wang"],
            }), encoding="utf-8")
            crossref.write_text(json.dumps({
                "doi": "10.1000/example", "title": "Dynamic relations in adolescence",
                "year": 2022, "authors": ["Li", "Wang"],
            }), encoding="utf-8")
            openalex.write_text(json.dumps({
                "doi": "10.1000/example", "title": "Dynamic relations in adolescence",
                "year": 2023, "authors": ["Li", "Wang"],
            }), encoding="utf-8")
            result = json.loads(self.run_script(
                "metadata_verify.py", "--candidate", str(candidate), "--crossref", str(crossref),
                "--openalex", str(openalex), "--output", str(output),
            ).stdout)
            self.assertEqual("conflict", result["status"])
            self.assertIn("year", result["conflict_fields"])
            self.assertFalse(result["eligible_for_verified_ledger"])

    def test_asreview_bridge_only_ranks_and_never_decides(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "records.jsonl"
            output = root / "ranking.json"
            source.write_text(
                json.dumps({"candidate_id": "C-2", "score": 0.2}) + "\n" +
                json.dumps({"candidate_id": "C-1", "score": 0.9}) + "\n",
                encoding="utf-8",
            )
            result = json.loads(self.run_script(
                "screening_rank_bridge.py", "--input", str(source), "--output", str(output),
            ).stdout)
            queue = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(["C-1", "C-2"], [item["candidate_id"] for item in queue["records"]])
            self.assertTrue(all(set(item) == {"candidate_id", "rank", "score", "decision"} for item in queue["records"]))
            self.assertTrue(all(item["decision"] == "human-review-required" for item in queue["records"]))
            self.assertEqual("ranking-only", result["authority"])

    def test_ro_crate_export_hashes_and_relates_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            run_dir = self.init_run(root, "ro-crate")
            artifact = run_dir / "09_论文正文" / "paper.md"
            artifact.write_text("# Paper\n", encoding="utf-8")
            result = json.loads(self.run_script(
                "export_ro_crate.py", "--run-dir", str(run_dir), "--artifact", str(artifact),
            ).stdout)
            crate = json.loads(Path(result["metadata"]).read_text(encoding="utf-8"))
            file_nodes = [item for item in crate["@graph"] if item.get("@type") == "File"]
            self.assertEqual(1, len(file_nodes))
            self.assertEqual(hashlib.sha256(artifact.read_bytes()).hexdigest(), file_nodes[0]["sha256"])

    def test_frozen_policy_evaluation_suite_passes(self) -> None:
        result = json.loads(self.run_script(
            "run_frozen_evals.py", "--cases", str(SKILL / "tests" / "frozen_cases" / "research_policy_cases.json"),
        ).stdout)
        self.assertEqual("passed", result["status"])
        self.assertEqual(result["total"], result["passed"])
        self.assertGreaterEqual(result["total"], 5)


if __name__ == "__main__":
    unittest.main()
