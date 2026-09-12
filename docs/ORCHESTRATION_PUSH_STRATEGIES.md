# Orchestration Push Strategies for Agent Incremental Pushes

**Problem:** Agent tools make multiple incremental pushes in single session. Current post-push hook fires on each push, creating duplicate/conflicting PRs.

**Solution:** Aggregate changes in orchestration-tools-changes branch before promotion.

---

## Strategy 5: Orchestration-Tools-Changes Branch Pattern (RECOMMENDED)

**Concept:** Agent pushes accumulate in `orchestration-tools-changes` branch. When settled, single PR merges to orchestration-tools.

### Implementation

1. **Agent pushes to orchestration-tools-changes** (instead of orchestration-tools)
   - `git push origin orchestration-tools-changes`
   - Changes accumulate without creating PRs yet

2. **Post-push hook debounces** (5-10 second wait)
   - Waits for push burst to settle
   - Prevents duplicate PR creation

3. **Single PR created** after debounce
   - Merges all accumulated changes from orchestration-tools-changes → orchestration-tools
   - Clean, single PR per session

4. **Developer reviews/merges**
   - PR shows all aggregated changes
   - One decision point, not multiple

### Pros
- No duplicate PRs
- Simple state tracking (branch exists or doesn't)
- Natural aggregation (changes accumulate on branch)
- Easy to understand

### Cons
- Requires branch name convention
- Debounce timing needs tuning (5-10 seconds)
- Developers must push to correct branch

### Testing Steps
1. Switch to feature/test branch
2. Make simulated agent pushes to orchestration-tools-changes
3. Verify single PR created (not multiple)
4. Monitor: conflicts, merge behavior
5. Document results

---

## Strategy 7: Hybrid (Combine Best Parts)

**Concept:** Combine Strategy 5 (changes branch) with Strategy 3 (git notes) for resilience.

- **Primary:** orchestration-tools-changes branch aggregation (Strategy 5)
- **Backup:** git notes for metadata tracking (Strategy 3)
- **Extra:** Pre-push warnings to user

### Pros
- Fallback if changes branch breaks
- Metadata survives force-push
- Extra safety for critical changes

### Cons
- More complex implementation
- Requires git notes understanding

### When to Use
- If Strategy 5 fails (race conditions, branch conflicts)
- For critical/sensitive changes
- Production orchestration

---

## Decision Matrix

| Scenario | Strategy |
|----------|----------|
| Multiple agent pushes → duplicate PRs | Strategy 5 |
| Need metadata persistence | Strategy 3 (git notes) |
| Race conditions appear | Strategy 7 |
| Simple, fast aggregation | Strategy 5 ✓ |

---

## Switchability

**From Strategy 5 to Strategy 7:**
- Add git notes tracking without removing changes branch
- Add pre-push hook warnings
- Keep same branch flow

**Quick switch:**
- Update post-push hook logic
- No branch restructuring needed

