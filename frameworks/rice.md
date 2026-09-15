# RICE Prioritization

A simple framework for deciding what to build first.

## What it stands for

- **R**each — how many users will this affect in a given period?
- **I**mpact — how much will it move the metric?
- **C**onfidence — how sure are we about the estimates?
- **E**ffort — how much work will it take?

**Score = (Reach × Impact × Confidence) ÷ Effort**

## When to use it

- You have more ideas than capacity.
- You need to defend your prioritization to stakeholders.
- You want a fast, rough, comparable score.

## When NOT to use it

- Early discovery — you don't have data yet.
- Strategic bets where the metric isn't clear.
- When everything scores the same (means your inputs are wrong).

## Example

| Feature | Reach | Impact | Confidence | Effort | Score |
|---|---|---|---|---|---|
| Personalized learning paths | 10,000 | 3 | 0.8 | 5 | 4,800 |
| Chatbot for onboarding | 5,000 | 2 | 0.6 | 2 | 3,000 |

→ Personalized learning paths wins, despite higher effort.

## How I use it

I treat RICE as a conversation starter, not a verdict.  
If the score surprises me, I ask why: that's where the real insight is.
