from __future__ import annotations

import json
import csv
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
CLI = SKILL / "scripts" / "pipeline.py"


class LiteratureCliTests(unittest.TestCase):
    def invoke(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONIOENCODING"] = "utf-8"
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, str(CLI), *args], text=True, encoding="utf-8",
            capture_output=True, check=check, env=environment,
        )

    def init_run(self, project: Path, run_id: str) -> Path:
        payload = json.loads(self.invoke(
            "init", "--project", str(project), "--title", "literature automation", "--run-id", run_id,
        ).stdout)
        return Path(payload["run_dir"])

    def test_user_can_freeze_modular_search_families_with_query_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = self.init_run(project, "search-plan-run")
            spec = project / "search-plan.json"
            spec.write_text(json.dumps({
                "schema_version": 1,
                "review_id": "conflict-depression-self-harm",
                "concept_blocks": {
                    "population": ["adolescen*", "youth"],
                    "conflict": ["interparental conflict", "marital conflict"],
                    "depression": ["depress*", "depressive symptoms"],
                    "self_harm": ["nonsuicidal self-injury", "NSSI", "self-harm"],
                    "design": ["longitudinal", "prospective", "cross-lagged"],
                },
                "query_families": [{
                    "family_id": "conflict-depression-longitudinal",
                    "purpose": "direct empirical evidence",
                    "blocks": ["population", "conflict", "depression", "design"],
                    "queries": {
                        "PsycINFO": "(adolescen* OR youth) AND (interparental conflict OR marital conflict) AND depress* AND longitudinal",
                        "Web of Science": "TS=((adolescen* OR youth) AND (interparental conflict OR marital conflict) AND depress* AND longitudinal)",
                        "PubMed": "(adolescent[Title/Abstract]) AND (interparental conflict[Title/Abstract]) AND depression[Title/Abstract]"
                    }
                }],
                "languages": ["en", "zh"],
                "search_update_days": 30
            }), encoding="utf-8")
            result = json.loads(self.invoke(
                "plan-search", "--run-dir", str(run_dir), "--spec", str(spec),
            ).stdout)
            self.assertEqual("ready", result["status"])
            self.assertEqual(3, result["query_count"])
            plan = json.loads(Path(result["search_plan"]).read_text(encoding="utf-8"))
            self.assertEqual(64, len(plan["queries"][0]["query_sha256"]))
            self.assertIn("conflict-depression-longitudinal", Path(result["queries_markdown"]).read_text(encoding="utf-8"))

    def test_user_can_import_heterogeneous_exports_into_one_evidence_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = self.init_run(project, "evidence-import-run")
            exports = project / "exports"
            exports.mkdir()
            (exports / "records.csv").write_text(
                "title,authors,year,doi,abstract\nCSV study,Li Wei,2020,https://doi.org/10.1000/CSV.1,CSV abstract\n",
                encoding="utf-8",
            )
            (exports / "records.ris").write_text(
                "TY  - JOUR\nTI  - RIS study\nAU  - Smith, Jane\nPY  - 2021\nDO  - 10.1000/ris.1\nAB  - RIS abstract\nER  -\n",
                encoding="utf-8",
            )
            (exports / "records.bib").write_text(
                "@article{key, title={BibTeX study}, author={Wang, Ming and Zhao, Lin}, year={2022}, doi={10.1000/bib.1}, abstract={Bib abstract}}\n",
                encoding="utf-8",
            )
            (exports / "pubmed.xml").write_text(
                "<PubmedArticleSet><PubmedArticle><MedlineCitation><PMID>12345</PMID><Article><ArticleTitle>PubMed study</ArticleTitle><Abstract><AbstractText>PubMed abstract</AbstractText></Abstract><AuthorList><Author><LastName>Chen</LastName><ForeName>Yu</ForeName></Author></AuthorList><Journal><JournalIssue><PubDate><Year>2023</Year></PubDate></JournalIssue></Journal></Article></MedlineCitation><PubmedData><ArticleIdList><ArticleId IdType='doi'>10.1000/pubmed.1</ArticleId></ArticleIdList></PubmedData></PubmedArticle></PubmedArticleSet>",
                encoding="utf-8",
            )
            (exports / "crossref.json").write_text(json.dumps({"message": {"items": [{
                "title": ["Crossref study"], "author": [{"family": "Jones", "given": "Amy"}],
                "published": {"date-parts": [[2024]]}, "DOI": "10.1000/CROSSREF.1", "URL": "https://doi.org/10.1000/crossref.1",
            }]}}), encoding="utf-8")
            (exports / "openalex.json").write_text(json.dumps({"results": [{
                "id": "https://openalex.org/W123", "title": "OpenAlex study", "publication_year": 2025,
                "doi": "https://doi.org/10.1000/openalex.1", "authorships": [{"author": {"display_name": "Taylor Kim"}}],
                "primary_location": {"landing_page_url": "https://example.org/work"},
            }]}), encoding="utf-8")

            result = json.loads(self.invoke(
                "import-evidence", "--run-dir", str(run_dir), "--search-id", "search-0001",
                *sum((["--input", str(path)] for path in sorted(exports.iterdir())), []),
            ).stdout)
            self.assertEqual("complete", result["status"])
            self.assertEqual(6, result["imported_records"])
            with Path(result["candidate_records"]).open("r", encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(6, len(rows))
            self.assertIn("10.1000/csv.1", {row["doi"] for row in rows})
            self.assertTrue(all(row["candidate_id"].startswith("cand-") for row in rows))
            manifest = json.loads(Path(result["manifest"]).read_text(encoding="utf-8"))
            self.assertTrue(all(len(item["sha256"]) == 64 for item in manifest["source_exports"]))

    def test_deduplication_keeps_distinct_reports_and_flags_study_family_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = self.init_run(project, "study-linkage-run")
            source = project / "candidate_records.csv"
            fields = [
                "candidate_id", "title", "authors", "year", "doi", "pmid", "openalex_id",
                "cohort_name", "sample_country", "sample_size", "recruitment_years",
            ]
            rows = [
                ["cand-1", "Conflict and depression", "Li; Wang", "2020", "10.1/a", "", "", "Youth Growth Cohort", "China", "1200", "2016-2018"],
                ["cand-2", "Conflict and depression duplicate", "Li; Wang", "2020", "https://doi.org/10.1/A", "", "", "Youth Growth Cohort", "China", "1200", "2016-2018"],
                ["cand-3", "Depression and self-harm follow-up", "Li; Zhao", "2022", "10.1/b", "", "", "Youth Growth Cohort", "China", "1200", "2016-2018"],
                ["cand-4", "Independent cohort", "Smith", "2021", "", "9988", "W99", "Other Cohort", "USA", "600", "2017"],
            ]
            with source.open("w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(fields)
                writer.writerows(rows)
            dedupe = json.loads(self.invoke(
                "dedupe-evidence", "--run-dir", str(run_dir), "--input", str(source),
            ).stdout)
            self.assertEqual(3, dedupe["unique_records"])
            self.assertEqual(1, dedupe["duplicate_records"])
            with Path(dedupe["duplicate_file"]).open("r", encoding="utf-8-sig", newline="") as handle:
                duplicate = next(csv.DictReader(handle))
            self.assertEqual("doi", duplicate["duplicate_match_field"])

            linkage = json.loads(self.invoke(
                "cluster-studies", "--run-dir", str(run_dir), "--input", dedupe["deduplicated_file"],
            ).stdout)
            self.assertEqual("complete", linkage["status"])
            self.assertEqual(1, linkage["candidate_pairs"])
            with Path(linkage["study_family_candidates"]).open("r", encoding="utf-8-sig", newline="") as handle:
                pair = next(csv.DictReader(handle))
            self.assertEqual("pending", pair["review_status"])
            self.assertIn("cohort_name", pair["match_reasons"])

    def test_coverage_gate_retrieval_queue_and_refresh_are_auditable(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = self.init_run(project, "evidence-control-run")
            evidence = project / "evidence.csv"
            fields = [
                "candidate_id", "title", "authors", "year", "doi", "pmid", "openalex_id",
                "evidence_role", "constructs", "design", "fulltext_status", "retraction_status", "landing_url",
            ]
            rows = [
                ["cand-1", "Direct study", "Li", "2020", "10.1/a", "", "", "direct-empirical", "conflict;depression", "longitudinal", "metadata-only", "clear", "https://example.org/a"],
                ["cand-2", "Measure study", "Wang", "2021", "10.1/b", "", "", "measurement", "depression", "validation", "metadata-only", "clear", "https://example.org/b"],
                ["cand-3", "Retracted study", "Smith", "2019", "10.1/c", "", "", "direct-empirical", "conflict;self-harm", "longitudinal", "metadata-only", "retracted", "https://example.org/c"],
            ]
            with evidence.open("w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(fields)
                writer.writerows(rows)
            requirements = project / "coverage.json"
            requirements.write_text(json.dumps({
                "schema_version": 1,
                "requirements": [
                    {"slot_id": "conflict-depression", "core": True, "minimum": 1, "criteria": {"evidence_role": ["direct-empirical"], "constructs_all": ["conflict", "depression"], "design_any": ["longitudinal"]}},
                    {"slot_id": "conflict-self-harm", "core": True, "minimum": 1, "criteria": {"evidence_role": ["direct-empirical"], "constructs_all": ["conflict", "self-harm"], "design_any": ["longitudinal"]}},
                ],
            }), encoding="utf-8")
            coverage_process = self.invoke(
                "audit-evidence-coverage", "--run-dir", str(run_dir), "--input", str(evidence),
                "--requirements", str(requirements), check=False,
            )
            self.assertEqual(3, coverage_process.returncode)
            coverage = json.loads(coverage_process.stdout)
            self.assertEqual("blocked", coverage["status"])
            self.assertEqual(["conflict-self-harm"], coverage["missing_core_slots"])

            queue = json.loads(self.invoke(
                "build-retrieval-queue", "--run-dir", str(run_dir), "--input", str(evidence),
            ).stdout)
            self.assertEqual(2, queue["queued_records"])
            with Path(queue["retrieval_queue"]).open("r", encoding="utf-8-sig", newline="") as handle:
                queued = list(csv.DictReader(handle))
            self.assertEqual("cand-1", queued[0]["candidate_id"])
            self.assertNotIn("cand-3", {row["candidate_id"] for row in queued})

            refreshed = project / "refreshed.csv"
            with refreshed.open("w", encoding="utf-8-sig", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(fields)
                writer.writerows([rows[0], ["cand-4", "New study", "Zhao", "2026", "10.1/d", "", "", "direct-empirical", "conflict;depression", "longitudinal", "metadata-only", "clear", "https://example.org/d"]])
            refresh = json.loads(self.invoke(
                "refresh-search", "--run-dir", str(run_dir), "--baseline", str(evidence), "--current", str(refreshed),
            ).stdout)
            self.assertEqual(1, refresh["new_records"])
            self.assertEqual(2, refresh["missing_from_refresh"])
            self.assertTrue(Path(refresh["refresh_log"]).is_file())

    def test_strict_search_gate_detects_candidate_records_changed_after_import(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "strict search", "--mode", "strict", "--run-id", "strict-search",
            ).stdout)["run_dir"])
            spec = project / "search-plan.json"
            spec.write_text(json.dumps({
                "schema_version": 1, "review_id": "strict-search", "concept_blocks": {"population": ["adolescent"], "outcome": ["depression"]},
                "query_families": [{"family_id": "direct", "purpose": "direct evidence", "blocks": ["population", "outcome"], "queries": {"PubMed": "adolescent AND depression"}}],
                "languages": ["en"], "search_update_days": 30,
            }), encoding="utf-8")
            self.invoke("plan-search", "--run-dir", str(run_dir), "--spec", str(spec))
            export = project / "records.csv"
            export.write_text("title,authors,year,doi\nA longitudinal adolescent depression study,Li,2020,10.1/a\n", encoding="utf-8")
            imported = json.loads(self.invoke(
                "import-evidence", "--run-dir", str(run_dir), "--search-id", "search-0001", "--input", str(export),
            ).stdout)
            search_log = run_dir / "02_证据检索" / "检索记录_search_log.csv"
            search_log.write_text(
                "search_id,database,platform,query,filters,run_at,result_count,export_file,notes\n"
                f"search-0001,PubMed,PubMed,adolescent AND depression,none,2026-07-19T00:00:00+08:00,1,{export},exact export\n",
                encoding="utf-8",
            )
            passed = self.invoke("gate", "--run-dir", str(run_dir), "--stage", "02_search", check=False)
            self.assertEqual(0, passed.returncode)
            candidate_path = Path(imported["candidate_records"])
            candidate_path.write_text(candidate_path.read_text(encoding="utf-8-sig") + "\n", encoding="utf-8-sig")
            blocked = self.invoke("gate", "--run-dir", str(run_dir), "--stage", "02_search", check=False)
            self.assertEqual(1, blocked.returncode)
            self.assertIn("candidate records hash differs", blocked.stdout)

    def test_dual_reviewer_screening_produces_prisma_and_adjudication_audit(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = self.init_run(project, "screening-run")
            decisions = project / "decisions.csv"
            decisions.write_text(
                "candidate_id,stage,reviewer,decision,reason,decided_at\n"
                "c1,title-abstract,A,include,relevant,2026-07-21\n"
                "c1,title-abstract,B,include,relevant,2026-07-21\n"
                "c2,title-abstract,A,include,relevant,2026-07-21\n"
                "c2,title-abstract,B,exclude,wrong population,2026-07-21\n"
                "c2,title-abstract,ADJ,exclude,wrong population,2026-07-21\n",
                encoding="utf-8",
            )
            result = json.loads(self.invoke(
                "audit-screening", "--run-dir", str(run_dir), "--input", str(decisions),
                "--reviewers", "A", "B", "--adjudicator", "ADJ",
            ).stdout)
            self.assertEqual("complete", result["status"])
            self.assertEqual(1, result["conflicts"])
            self.assertEqual(0, result["unresolved_conflicts"])
            self.assertTrue(Path(result["prisma_counts"]).is_file())
            self.assertTrue(Path(result["risk_of_bias_template"]).is_file())


if __name__ == "__main__":
    unittest.main()
