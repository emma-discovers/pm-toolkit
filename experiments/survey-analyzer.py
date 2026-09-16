"""
Survey Analyzer
===============

A lightweight script that reads post-training survey responses from a CSV file
and generates a Markdown report with NPS, CSAT, and open-feedback analysis.

Built for L&D teams who collect feedback but don't have a data team to analyze it.

Usage:
    python survey-analyzer.py --input survey.csv --output report.md

Input CSV format:
    user_id,department,nps_score,csat_score,open_feedback
    1,Engineering,9,5,"Great course, very practical"
    2,Marketing,7,4,"Could be shorter"

"""

import argparse
import csv
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "is", "are", "was", "were",
    "to", "of", "in", "on", "for", "with", "it", "this", "that", "very",
    "i", "we", "you", "they", "my", "our", "be", "been", "have", "has",
    "had", "do", "does", "did", "so", "not", "no", "yes", "as", "at",
    "by", "from", "would", "could", "should", "more", "less", "much",
}


def read_csv(filepath: str) -> list[dict]:
    """Read survey responses from a CSV file."""
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def to_int(value: str):
    """Safely convert a string to int, returning None if not possible."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def calculate_nps(scores: list[int]) -> float:
    """Calculate Net Promoter Score: %promoters (9-10) - %detractors (0-6)."""
    if not scores:
        return 0.0
    promoters = sum(1 for s in scores if s >= 9)
    detractors = sum(1 for s in scores if s <= 6)
    return round((promoters - detractors) / len(scores) * 100, 1)


def calculate_csat(scores: list[int]) -> float:
    """Calculate average CSAT score (typically 1-5)."""
    if not scores:
        return 0.0
    return round(sum(scores) / len(scores), 2)


def extract_top_words(feedback: list[str], top_n: int = 5) -> list[tuple[str, int]]:
    """Extract most common words from open-ended feedback, excluding stop words."""
    words = []
    for text in feedback:
        if not text:
            continue
        cleaned = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
        words.extend(w for w in cleaned if w not in STOP_WORDS)
    return Counter(words).most_common(top_n)


def group_by_department(rows: list[dict]) -> dict:
    """Group responses by department and calculate per-group metrics."""
    groups = defaultdict(list)
    for row in rows:
        groups[row["department"]].append(row)

    result = {}
    for dept, dept_rows in groups.items():
        nps_scores = [s for s in (to_int(r["nps_score"]) for r in dept_rows) if s is not None]
        csat_scores = [s for s in (to_int(r["csat_score"]) for r in dept_rows) if s is not None]
        result[dept] = {
            "responses": len(dept_rows),
            "nps": calculate_nps(nps_scores),
            "csat": calculate_csat(csat_scores),
        }
    return result


def generate_report(rows: list[dict], source: str) -> str:
    """Generate a Markdown report from survey responses."""
    nps_scores = [s for s in (to_int(r["nps_score"]) for r in rows) if s is not None]
    csat_scores = [s for s in (to_int(r["csat_score"]) for r in rows) if s is not None]
    feedback = [r.get("open_feedback", "") for r in rows]
    top_words = extract_top_words(feedback)
    by_dept = group_by_department(rows)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        "# Survey Report",
        "",
        f"**Source:** `{source}`  ",
        f"**Generated:** {now}",
        "",
        "## Overall metrics",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Responses | {len(rows)} |",
        f"| Average NPS | {calculate_nps(nps_scores)} |",
        f"| Average CSAT | {calculate_csat(csat_scores)} |",
        "",
        "## Top words in feedback",
        "",
    ]

    if top_words:
        for word, count in top_words:
            lines.append(f"- **{word}** — {count}")
    else:
        lines.append("*No open feedback provided.*")

    lines += [
        "",
        "## By department",
        "",
        "| Department | Responses | Avg NPS | Avg CSAT |",
        "|------------|-----------|---------|----------|",
    ]

    for dept, data in sorted(by_dept.items()):
        lines.append(
            f"| {dept} | {data['responses']} | {data['nps']} | {data['csat']} |"
        )

    lines += [
        "",
        "---",
        "",
        "*Generated automatically. Review before sharing.*",
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Analyze post-training survey responses.")
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--output", default="survey-report.md", help="Path to output Markdown file")
    args = parser.parse_args()

    rows = read_csv(args.input)
    if not rows:
        print("No data found in input file.")
        return

    report = generate_report(rows, args.input)
    Path(args.output).write_text(report, encoding="utf-8")
    print(f"Report generated: {args.output}")


if __name__ == "__main__":
    main()
