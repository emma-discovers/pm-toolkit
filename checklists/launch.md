# Launch Checklist

Not every item applies to every launch, but every item is worth a thought before you decide it doesn't.

## 1. Launch context

- [ ] **What is launching:** one line
- [ ] **Launch type:** new product / new feature / experiment
- [ ] **Launch tier:** major (full GTM) / moderate (announcement + enablement) / minor (release notes only)
- [ ] **Target date:** confirmed with engineering
- [ ] **Launch owner:** named person, not a team

## 2. Product readiness

- [ ] **Scope complete:** all P0 acceptance criteria pass in staging
- [ ] **P1 criteria:** pass in staging, or explicitly deferred with a reason
- [ ] **Edge cases and error states:** handled
- [ ] **Performance tested:** under expected load
- [ ] **Known bugs:** no P0 or P1 open
- [ ] **QA sign-off:** documented
- [ ] **Feature flag:** in place and tested (enable/disable works)
- [ ] **Rollout percentage:** configured if phased rollout is planned

## 3. User readiness

- [ ] **Onboarding or first-run experience:** exists and tested with real users
- [ ] **Help / FAQ:** updated for the new functionality
- [ ] **Support team:** briefed, with escalation path defined
- [ ] **Customer-facing documentation:** published or ready to publish
- [ ] **In-product announcements:** configured (banner, tooltip, modal — as appropriate)

## 4. Data & analytics

- [ ] **Success metric defined:** and measurable
- [ ] **Analytics events:** all events from the measurement plan are firing
- [ ] **Dashboard:** exists and is ready before launch day
- [ ] **Baseline captured:** before launch, so you can compare after
- [ ] **Error rate alerting:** configured for new code surface

## 5. Team & operations

- [ ] **Engineering sign-off:** received
- [ ] **Design sign-off:** received
- [ ] **Stakeholders informed:** launch date and expected impact communicated
- [ ] **Launch day coverage:** someone monitoring metrics and support channels, with a name
- [ ] **On-call engineering:** in place for launch day

## 6. Legal & compliance

- [ ] **Privacy review:** completed if new data is collected or processed
- [ ] **Disclosures / consent:** updated if the feature touches regulated data
- [ ] **Data residency:** confirmed if the feature crosses jurisdictions
- [ ] **Audit trail:** logging in place for any compliance-relevant action

## 7. Go / No-Go criteria

- [ ] **Go criteria:** what must be true to proceed
- [ ] **No-Go criteria:** what would force a delay, defined before launch day
- [ ] **Decision owner:** who makes the call if criteria are ambiguous

## 8. Rollback plan

- [ ] **Rollback trigger:** defined. (e.g., "If error rate exceeds X% for Y minutes, we roll back.")
- [ ] **Rollback owner:** named person who can make the call
- [ ] **Rollback procedure:** documented and tested
- [ ] **Time-to-rollback:** estimated and acceptable
- [ ] **Communication plan:** who gets notified if rollback happens

## 9. Post-launch monitoring

### First 24 hours
- [ ] Error logs reviewed
- [ ] Analytics events verified
- [ ] Support channels monitored
- [ ] Rollback criteria checked

### First 7 days
- [ ] Metrics reviewed against targets
- [ ] User feedback collected
- [ ] Bugs triaged and fixed
- [ ] No unexpected drop in guardrail metrics (NPS, retention, compliance)

### Day 30
- [ ] Retro completed: keep, iterate, or kill
- [ ] Success criteria evaluated
- [ ] Learnings documented
