# Jules Session Nudge Queue

**Daily Limit: 15 sessions**
**Created: 2026-04-13**
**Strategy: Nudge EXISTING sessions with existing PRs - don't create new sessions**

---

## Priority 1: FAILED Sessions (4) - Nudge When Limit Resets

These produced zero changes. Need nudge to existing PRs.

| # | Session ID | PR | Nudge Message |
|---|---------|-----|-------------|
| 1.1 | 1718535776004701779 | Resume this session. Make one small change to your PR and push. |
| 1.2 | 18083307284626523730 | Resume this session. Make one small change to your PR and push. |
| 1.3 | 9416853960953674263 | Resume this session. Make one small change to your PR and push. |
| 1.4 | 2019152598300629437 | Resume this session. Make one small change to your PR and push. |

---

## Priority 2: NO-STATUS Sessions (6) - Nudge After Priority 1

Sessions with PRs but no status shown.

| # | Session ID | PR |
|---|-----------|-----|
| 2.1 | 1674154434053758629 | - |
| 2.2 | 6776898346429646182 | - |
| 2.3 | 10925145603004142302 | - |
| 2.4 | 5561916866105318571 | - |
| 2.5 | 9258939324841518557 | - |
| 2.6 | 5158047970794815827 | - |

**Nudge Message:**
> "Please continue working on your PR. Make one small change and push."

---

## Priority 3: COMPLETED Sessions - Follow-up (5)

Completed sessions that may have open PRs needing review.

| # | Session ID | Status |
|---|-----------|--------|
| 3.1 | 14323196579621021860 (Sentinel) |
| 3.2 | 5656601079512900964 (Bolt) |
| 3.3 | 12020355510843090616 (Sentinel) |
| 3.4 | 6825852734872785736 (Bolt) |
| 3.5 | 314162335015195357 (Sentinel) |

---

## Already Active - Don't Nudge

These are actively working - no action needed:

- 17230506058855569154 (In Progress)
- 14526103937317527694 (In Progress)
- 14540362026225469649 (In Progress)
- 10052513681880916076 (In Progress)
- 7692854003959057341 (In Progress)
- 8919410920181695339 (In Progress)
- 5814112027244730925 (In Progress)
- 2308156640503755864 (Planning)
- 7831562456284511166 (Planning)
- 381423427753404511 (Planning)
- 14220203592363167967 (Planning)
- 11315881698264364189 (Planning)
- 8098457377596089277 (Planning)
- 2140584468424237267 (Planning)
- 10020942061822270894 (Planning)
- 12706650364775836825 (Planning)
- 12772292616880399643 (Planning)
- 13249318558277900638 (In Progress)
- 5013138083547654050 (Planning)

---

## How to Nudge Existing Sessions

When limit resets, use Jules API to send message to EXISTING session:

```bash
# Via Jules API (requires authentication)
curl -X POST "https://jules.googleapis.com/v1alpha/sessions/{session_id}:sendMessage" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Resume working on your PR. Make one small change and push."}'
```

OR create new sessions targeting the same repo (will link to existing PR):

```bash
jules new --repo MasumRab/EmailIntelligenceGem "Resume session {session_id}: Make one small change and push."
```