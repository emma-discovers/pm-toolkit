"""
Assessment Report Generator
============================

A lightweight script that reads assessment results from a CSV file
and generates a Markdown report with completion rates, score distribution,
and group-level breakdowns.

Built for L&D teams who need to automate reporting without a data engineering team.

Usage:
    python assessment-report.py --input results.csv --output report.md

Input CSV format:
    user_id,user_name,department,assessment_id,assessment_name,status,score,max_score,completed_at
    1,Anna,Engineering,101,Security Basics,completed,85,100,2026-09-01
    2,Ivan,Marketing,101,Security Basics,completed,72,100,2026-09-02
    3,Olga,Sales,101,Security Basics,failed,45,100,2026-09-02

Author: Emma Mesropian
"""

import argparse
import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def read_csv(filepath: str) -> list[dict]:
    """Read assessment results from a CSV file."""
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def calculate_metrics(rows: list[dict]) -> dict:
    """Calculate completion rates and score statistics."""
    total = len(rows)
    completed = [r for r in rows if r["status"] == "completed"]
    failed = [r for r in rows if r["status"] == "failed"]
    in_progress = [r for r in rows if r["status"] == "in_progress"]

    scores = [int(r["score"]) for r in completed if r["score"].isdigit()]
    avg_score = sum(scores) / len(scores) if scores else 0

    return {
        "total": total,
        "completed": len(completed),
        "failed": len(failed),
        "in_progress": len(in_progress),
        "completion_rate": round(len(completed) / total * 100, 1) if total else 0,
        "avg_score": round(avg_score, 1),
        "pass_rate": round(len(completed) / (len(completed) + len(failed)) * 100, 1)
        if (len(completed) + len(failed)) else 0,
    }


def group_by_department(rows: list[dict]) -> dict:
    """Group results by department and calculate per-group metrics."""
    groups = defaultdict(list)
    for row in rows:
        groups[row["department"]].append(row)

    result = {}
    for dept, dept_rows in groups.items():
        completed = [r for r in dept_rows if r["status"] == "completed"]
        scores = [int(r["score"]) for r in completed if r["score"].isdigit()]
        avg = sum(scores) / len(scores) if scores else 0

        result[dept] = {
            "total": len(dept_rows),
            "completed": len(completed),
            "completion_rate": round(len(completed) / len(dept_rows) * 100, 1)
            if dept_rows else 0,
            "avg_score": round(avg, 1),
        }
    return result


def generate_report(metrics: dict, by_dept: dict, source: str) -> str:
    """Generate a Markdown report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        "# Assessment Report",
        "",
        f"**Source:** `{source}`  ",
        f"**Generated:** {now}",
        "",
        "## Overall metrics",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total attempts | {metrics['total']} |",
        f"| Completed | {metrics['completed']} |",
        f"| Failed | {metrics['failed']} |",
        f"| In progress | {metrics['in_progress']} |",
        f"| Completion rate | {metrics['completion_rate']}% |",
        f"| Average score | {metrics['avg_score']} |",
        f"| Pass rate | {metrics['pass_rate']}% |",
        "",
        "## By department",
        "",
        "| Department | Attempts | Completed | Completion rate | Avg score |",
        "|------------|----------|-----------|-----------------|-----------|",
    ]

    for dept, data in sorted(by_dept.items()):
        lines.append(
            f"| {dept} | {data['total']} | {data['completed']} | "
            f"{data['completion_rate']}% | {data['avg_score']} |"
        )

    lines += [
        "",
        "---",
        "",
        "*Generated automatically. Review before sharing.*",
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate assessment report from CSV.")
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--output", default="report.md", help="Path to output Markdown file")
    args = parser.parse_args()

    rows = read_csv(args.input)
    if not rows:
        print("No data found in input file.")
        return

    metrics = calculate_metrics(rows)
    by_dept = group_by_department(rows)
    report = generate_report(metrics, by_dept, args.input)

    Path(args.output).write_text(report, encoding="utf-8")
    print(f"Report generated: {args.output}")


if __name__ == "__main__":
    main()
