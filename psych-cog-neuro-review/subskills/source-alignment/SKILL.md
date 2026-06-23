---
name: psych-review-source-alignment
description: Use this subskill after a psychology or cognitive neuroscience review draft is written to create a paragraph-level matrix linking each review paragraph and claim to exact source passages, pages, tables, figures, or result sections. 用于综述原文与参考文献原文的逐段对应核查；不要用于没有文献原文或阅读矩阵支持的自由核查。
---

# Source Alignment / 综述原文—参考文献对应矩阵

## Purpose

After a review draft is complete, verify exactly which source passage supports each paragraph and claim. The goal is not only to check citation formatting, but to show “综述中的哪一段话，对应文献中的哪一段话或哪一个结果”。

## Inputs

- `05_write/review_draft.md` with stable paragraph IDs such as `P001`, `P002`
- full-text PDFs, extracted notes, or reading cards when available
- `03_extract/literature_matrix.csv`
- `03_extract/neural_mechanism_matrix.csv`
- `04_synthesis/claim_evidence_map.csv`
- BibTeX/RIS/Zotero export or reference list

## Required outputs

- `06_audit/paragraph_source_alignment_matrix.csv`
- `06_audit/paragraph_source_alignment_report.md`
- `06_audit/unsupported_or_overstated_claims.md`

## Workflow

1. Segment the review draft into numbered paragraphs. If paragraph IDs are absent, add IDs without changing the argument.
2. Split each paragraph into claim units. Label claims as definition, empirical finding, theory, method, mechanism, limitation, comparison, implication, or inference.
3. For each claim, locate supporting source passages from PDFs, notes, matrices, tables, figures, abstracts, or result sections.
4. Record the source passage precisely: source ID, citation key, author-year, page, section, paragraph/table/figure, short source excerpt, and the exact draft claim.
5. Classify support strength: direct, partial, indirect, review-only, contradictory, unsupported, or overextended.
6. Mark whether the draft citation is valid for that exact claim. A source can support one part of a sentence but not another; split claims when needed.
7. Create a revision note for every unsupported, contradictory, or overextended claim.
8. Revise the draft only when the user requested automatic revision; otherwise provide the matrix and issue list.

## Matrix fields

Use this header for `paragraph_source_alignment_matrix.csv`:

```csv
review_paragraph_id,review_sentence_or_claim_id,review_claim_text,claim_type,in_text_citation,source_id,citation_key,source_author_year,source_title,source_location,page_or_location,source_passage_excerpt,support_strength,evidence_role,does_source_support_exact_claim,problem_type,revision_suggestion,notes
```

## Support labels

- `direct`: the source passage directly states the draft claim.
- `partial`: the source supports part of the claim, but the claim needs narrowing.
- `indirect`: the source supports a premise, not the final conclusion.
- `review_only`: the source is a review or meta-analysis; acceptable for broad background but not as a primary empirical citation when primary studies are needed.
- `contradictory`: the source conflicts with the draft claim.
- `unsupported`: no source passage supports the claim.
- `overextended`: the source supports a weaker claim than the draft makes.

## Rules

- Do not treat a citation as valid merely because it appears near the sentence.
- Do not use titles or abstracts as full-text evidence when full text is available.
- Do not quote long passages. Keep source excerpts short and only as needed for verification.
- Do not convert review-level conclusions into primary empirical findings.
- Do not accept vague source locations such as “paper says this”; use page, section, table, figure, or paragraph-level notes when available.
- For neuroimaging claims, distinguish activation, connectivity, decoding, lesion evidence, and inferred psychological function.
- For REM/emotional memory claims, distinguish REM duration, REM density, REM physiology, sleep deprivation, nap/night sleep, encoding, consolidation, retrieval, and extinction.

## Completion gate

The draft passes only when every empirical, theoretical, definitional, and methodological claim is either directly supported, explicitly framed as inference, or revised. If any claim remains unsupported, list it in `unsupported_or_overstated_claims.md` with a concrete fix.
