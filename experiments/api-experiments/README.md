# API Experiments

Testing how APIs can support L&D tasks. These are small scripts I built to see what's possible without paid subscriptions.

## quiz-generator.py

Generates quiz questions from a topic using Google Gemini's free API.

- **Why:** Creating quiz content manually is slow. This tests whether AI can speed it up.
- **Input:** a topic (e.g., "Python loops")
- **Output:** [sample-output.md](sample-output.md)
- **Run:** `python quiz-generator.py --topic "Python loops" --num 3`

## Note on the free tier

Gemini's free tier gives 50 requests per day. Enough for experiments and learning[reference:1].

More experiments will be added over time.
