#!/usr/bin/env python3
"""Generate the paper v1 tables from frozen evaluation artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_METRICS = ROOT / "results/public-paper-metrics-v1.json"


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    lines.extend("| " + " | ".join(str(value) for value in row) + " |" for row in rows)
    return "\n".join(lines)


def source_note(label: str, path: Path) -> str:
    try:
        relative = path.relative_to(ROOT)
    except ValueError:
        relative = Path(*path.parts[-2:])
    return f"Source: `{relative.as_posix()}`; SHA-256 `{sha256(path)}`."

def mechanical_table() -> str:
    path = PUBLIC_METRICS
    data = load_json(path)
    methods = data["mechanical_holdout_v2"]
    names = {
        "b1-ordinary-rag-deterministic": "ordinary RAG deterministic",
        "b2-hybrid-rag-deterministic": "hybrid RAG deterministic",
        "b3-self-rag-style-deterministic": "Self-RAG-style deterministic",
        "b4-rule-only": "rule-only",
        "v10-full": "v10-full",
        "concept-closure-v1": "concept-closure-v1",
    }
    rows = []
    for method_id, display_name in names.items():
        item = methods[method_id]
        metrics = item["primary_metrics"]
        rows.append(
            [
                display_name,
                item["sample_count"],
                f"{metrics['behavior_accuracy']:.3f}",
                f"{metrics['false_answer_rate']:.3f}",
                f"{metrics['false_refusal_rate']:.3f}",
                f"{metrics['citation_precision']:.3f}",
                f"{metrics['citation_recall']:.3f}",
                f"{metrics['evidence_closure_rate']:.3f}",
                f"{metrics['certificate_completeness']:.3f}",
            ]
        )
    return (
        "## Table 1: Mechanical held-out v2\n\n"
        + markdown_table(
            [
                "Method",
                "N",
                "Behavior",
                "False answer",
                "False refusal",
                "Citation P",
                "Citation R",
                "Closure",
                "Certificate",
            ],
            rows,
        )
        + "\n\nClaim: mechanism-level support only; labels and baselines are deterministic/mechanical.\n\n"
        + source_note("mechanical held-out", path)
    )


def privacyqa_v7_table() -> str:
    path = PUBLIC_METRICS
    data = load_json(path)["privacyqa_v1_4_v7_gate"]
    reference_behavior = 91
    candidate_behavior = 72
    citation = data["citation_precision_micro"]
    false_answer = data["false_answer"]
    false_refusal = data["false_refusal"]
    rows = [
        [
            "v4 reference",
            f"{reference_behavior}/147",
            f"{false_answer['reference_count']}/{false_answer['reference_denominator']}",
            f"{false_refusal['reference_count']}/{false_refusal['reference_denominator']}",
            f"{citation['method_b_mean']:.4f}",
        ],
        [
            "v7 candidate",
            f"{candidate_behavior}/147",
            f"{false_answer['candidate_count']}/{false_answer['candidate_denominator']}",
            f"{false_refusal['candidate_count']}/{false_refusal['candidate_denominator']}",
            f"{citation['method_a_mean']:.4f}",
        ],
    ]
    return (
        "## Table 2: PrivacyQA v1.4 v7 one-pass gate\n\n"
        + markdown_table(
            ["Method", "Behavior", "False answer", "False refusal", "Citation micro-P"],
            rows,
        )
        + "\n\nDecision: `"
        + data["decision"]
        + "`; the false-answer gain is offset by a false-refusal collapse.\n\n"
        + source_note("PrivacyQA gate audit", path)
    )


def p5_table() -> str:
    path = PUBLIC_METRICS
    data = load_json(path)["privacyqa_relation_p5"]
    citations = data["citation_metrics"]
    closure = data["closure_metrics"]
    safety = data["provenance_safety"]
    strict = data["strict_public_label_metrics"]
    rows = [
        ["Items", data["item_count"]],
        ["Grounded answers", strict["grounded_answer_count"]],
        ["Answerable grounded", f"3/{data['public_label_counts']['answerable']}"],
        ["False grounded on no-relevant", strict["false_grounded_on_no_relevant"]],
        ["No-relevant empty selected evidence", safety["no_relevant_items_with_empty_selected_evidence"]],
        ["Selected citation precision", f"{citations['selected_citation_precision']:.3f}"],
        ["Grounded citations in gold", f"{citations['selected_citations_in_gold']}/{citations['selected_citation_record_count']}"],
        ["Gap certificates valid", f"{closure['nonanswer_gap_certificate_count']}/{closure['nonanswer_count']}"],
        ["Runtime LLM calls", safety["runtime_llm_calls"]],
        ["Runtime human confirmations", safety["runtime_human_confirmations"]],
    ]
    return (
        "## Table 3: PrivacyQA relation closure P5 held-out 20\n\n"
        + markdown_table(["Metric", "Value"], rows)
        + "\n\nClaim: safety and certificate transfer only; coverage is a weak signal.\n\n"
        + source_note("P5 evaluation", path)
    )


def real_standard_extraction_table() -> str:
    path = PUBLIC_METRICS
    data = load_json(path)["real_standard_extraction_heldout"]
    v1 = data["structured_relation_v1"]
    v6 = data["scope_extraction_v6"]
    rows = [
        [
            "structured relation v1",
            v1["item_count"],
            f"{v1['exact_match_count']}/{v1['item_count']}",
            f"{v1['precision']:.6f}",
            f"{v1['recall']:.6f}",
            "n/a",
        ],
        [
            "scope extraction v6",
            v6["clause_count"],
            f"{v6['matched_action_count']} action match",
            f"{v6['semantic_precision']:.6f}",
            f"{v6['semantic_recall']:.6f}",
            f"{v6['semantic_f1']:.6f}",
        ],
    ]
    return (
        "## Table 4: Real standard extraction held-out negative results\n\n"
        + markdown_table(
            ["Method", "Items", "Exact/action match", "Precision", "Recall", "F1"],
            rows,
        )
        + "\n\nClaim: these failures justify Closure-Ready gating; they do not prove all extraction is impossible.\n\n"
        + source_note("public metric subset", path)
    )


def closure_ready_table() -> str:
    path = PUBLIC_METRICS
    data = load_json(path)["closure_ready_routing_dev_smoke_v0"]
    rows = []
    for layer in ("structured_frames", "passage_only", "out_of_domain"):
        item = data["layers"][layer]
        rows.append(
            [
                layer,
                item["sample_count"],
                f"{item['behavior_accuracy'] * item['sample_count']:.0f}",
                f"{item['false_answer_rate'] * item['sample_count']:.0f}",
                f"{item['false_refusal_rate'] * item['sample_count']:.0f}",
                f"{item['citation_precision']:.3f}",
                f"{item['unauthorized_judgment_rate'] * item['sample_count']:.0f}",
            ]
        )
    overall = data["overall"]
    rows.append(
        [
            "overall",
            data["sample_count"],
            f"{overall['behavior_accuracy'] * data['sample_count']:.0f}",
            f"{overall['false_answer_rate'] * data['sample_count']:.0f}",
            f"{overall['false_refusal_rate'] * data['sample_count']:.0f}",
            f"{overall['citation_precision']:.4f}",
            f"{overall['unauthorized_judgment_rate'] * data['sample_count']:.0f}",
        ]
    )
    return (
        "## Table 5: Closure-Ready routing dev smoke v0\n\n"
        + markdown_table(
            ["Layer", "N", "Behavior correct", "False answer", "False refusal", "Citation P", "Unauthorized frame"],
            rows,
        )
        + "\n\nClaim: 13-item development smoke; mechanism viability only, not held-out or product effectiveness.\n\n"
        + source_note("Closure-Ready summary", path)
    )


def render() -> str:
    parts = [
        "# Paper v1 frozen-result tables",
        "",
        "Generated from committed evaluation artifacts; no evaluation is rerun by this script.",
        "",
        mechanical_table(),
        "",
        privacyqa_v7_table(),
        "",
        p5_table(),
        "",
        real_standard_extraction_table(),
        "",
        closure_ready_table(),
        "",
        "## Claim boundary",
        "",
        "These tables are evidence layers, not one composite leaderboard. Mechanical, public-gold, real-standard, and development-smoke results must not be mixed into a single SOTA claim.",
        "",
    ]
    return "\n".join(parts)


def main() -> None:
    global PUBLIC_METRICS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=PUBLIC_METRICS,
        help="Public metrics JSON path",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "docs/paper_v1_tables.md",
        help="Output Markdown path",
    )
    args = parser.parse_args()
    PUBLIC_METRICS = args.input.resolve()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(), encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
