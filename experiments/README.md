# Experiments

A place for things I'm testing, learning, and figuring out. I'm not a developer! These are my attempts at self-learning, working prototypes, and small scripts I use to automate routine L&D tasks. 

## What's here
### assessment-report.py

Reads assessment results from a CSV file and generates a Markdown report with completion rates, score distribution, and per-department breakdowns.

- **Why:** L&D teams often spend hours manually compiling reports from LMS exports. This is my attempt to cut that time down.
- **Input:** [sample-results.csv](sample-results.csv)
- **Output:** [sample-report.md](sample-report.md)
- **Run:** `python assessment-report.py --input sample-results.csv --output report.md`

## Limitations

- **Pass rate is calculated as `completed / (completed + failed)`:** This treats every completed attempt as passed. In reality, a learner can complete an attempt and still score below the passing threshold. A production version would compare `score` against `max_score` and a defined pass mark.
- **Only integer scores are counted:** The script uses `int()` and `.isdigit()`, so decimal scores (e.g., `85.5`) are silently skipped. The sample data uses integers, so this does not affect the output. But it would matter with real LMS exports.

### survey-analyzer.py

Reads post-training survey responses from a CSV file and generates a Markdown report with NPS, CSAT, top words in open feedback, and a per-department breakdown.

- **Why:** feedback is collected but rarely analyzed. This script turns raw responses into a summary in seconds.
- **Input:** [sample-survey.csv](sample-survey.csv)
- **Output:** [sample-survey-report.md](sample-survey-report.md)
- **Run:** `python survey-analyzer.py --input sample-survey.csv --output report.md`

## Limitations

- **NPS is calculated on a 0–10 scale:** (promoters 9–10, detractors 0–6). CSAT is treated as a 1–5 scale. If your survey uses different scales, the formula needs to be adjusted.
- **Open feedback analysis is keyword-based:** not semantic. It counts frequent words after removing stop words. A production version could use sentiment analysis or topic modeling, but for a quick read, keyword frequency is often enough.

*(More experiments will be added here as I go.)*
