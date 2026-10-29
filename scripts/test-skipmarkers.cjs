#!/usr/bin/env node
/**
 * Smoke test for skipMarkers filtering logic.
 *
 * Fetches real PR comments via GitHub API, runs the same skipMarkers
 * filtering used by the review/force-review/walkthrough/auto-fix/resolve-conflicts
 * workflows, and shows what would be included vs excluded as priorFeedback.
 *
 * Does NOT create Jules sessions or consume GitHub Actions minutes.
 * Only uses GitHub REST API (authenticated via gh CLI token).
 *
 * Usage:
 *   node scripts/test-skipmarkers.cjs <repo> <pr-number>
 *   node scripts/test-skipmarkers.cjs MasumRab/EmailIntelligence 571
 */

const { execFileSync } = require('child_process');

// --- Configuration ---

// The exact skipMarkers arrays from the deployed workflows
const SKIP_MARKERS_FULL = [
  '<!-- jules-pr-reviewer -->',
  '<!-- jules-auto-fix -->',
  '<!-- jules-resolve -->',
  '<!-- jules-walkthrough -->',
  '<!-- jules-rebuild -->',
  '<!-- jules-quota-exhausted -->',
  '<!-- jules-address-comments -->',
];

const SKIP_MARKERS_SHORT = [
  '<!-- jules-pr-reviewer -->',
  '<!-- jules-auto-fix -->',
  '<!-- jules-resolve -->',
  '<!-- jules-rebuild -->',
  '<!-- jules-quota-exhausted -->',
  '<!-- jules-address-comments -->',
];

// --- GitHub API helper ---

function ghApi(endpoint) {
  try {
    const result = execFileSync(
      'gh',
      ['api', '--paginate', endpoint],
      { encoding: 'utf8', timeout: 30000, maxBuffer: 50 * 1024 * 1024 }
    );
    const parsed = JSON.parse(result);
    if (!Array.isArray(parsed)) {
      console.error(`API error: ${endpoint} returned non-array response`);
      process.exit(1);
    }
    return parsed;
  } catch (e) {
    console.error(`API error fetching ${endpoint}: ${e.message}`);
    process.exit(1);
  }
}

// --- Main ---

const repoArg = process.argv[2] || 'MasumRab/EmailIntelligence';
const prArg = process.argv[3];

if (!prArg) {
  console.error('Usage: node test-skipmarkers.cjs <owner/repo> <pr-number>');
  process.exit(1);
}

console.log(`\n=== SkipMarkers Smoke Test ===`);
console.log(`Repo: ${repoArg}`);
console.log(`PR:   #${prArg}\n`);

// Fetch issue comments
console.log('Fetching issue comments...');
const allComments = ghApi(`repos/${repoArg}/issues/${prArg}/comments`);
console.log(`  Found ${allComments.length} issue comments`);

// Fetch review comments (line-level)
console.log('Fetching review comments...');
const reviewComments = ghApi(`repos/${repoArg}/pulls/${prArg}/comments`);
console.log(`  Found ${reviewComments.length} review comments\n`);

// Sort by created_at desc (same as workflow)
const sortedComments = allComments.sort(
  (a, b) => new Date(b.created_at) - new Date(a.created_at)
);

// --- Run both skipMarkers variants ---

for (const [name, markers] of [
  ['review/force-review/walkthrough', SKIP_MARKERS_FULL],
  ['auto-fix/resolve-conflicts', SKIP_MARKERS_SHORT],
]) {
  console.log(`\n--- Using ${name} skipMarkers (${markers.length} markers) ---`);

  const filtered = sortedComments.filter(
    (c) => !markers.some((m) => c.body?.includes(m))
  );
  const included = filtered.slice(0, 10);
  const excluded = sortedComments.filter((c) =>
    markers.some((m) => c.body?.includes(m))
  );

  console.log(`\n  INCLUDED as priorFeedback (${included.length} comments):`);
  for (const c of included) {
    const who = c.user?.login || 'unknown';
    const preview = (c.body || '').slice(0, 120).replace(/\n/g, ' ');
    console.log(`    [${c.created_at}] ${who}: ${preview}...`);
  }

  console.log(`\n  EXCLUDED by skipMarkers (${excluded.length} comments):`);
  for (const c of excluded) {
    const who = c.user?.login || 'unknown';
    const matched = markers.find((m) => c.body?.includes(m));
    const preview = (c.body || '').slice(0, 80).replace(/\n/g, ' ');
    console.log(`    [${c.created_at}] ${who}: ${preview}...`);
    console.log(`      ↳ matched: ${matched}`);
  }
}

// --- Show what the prompt's "Existing PR comments" section would look like ---

console.log('\n\n=== Simulated prompt section: "Existing PR comments" ===');
console.log('(Using review/force-review/walkthrough skipMarkers)\n');

const priorFeedback = sortedComments
  .filter((c) => !SKIP_MARKERS_FULL.some((m) => c.body?.includes(m)))
  .slice(0, 10)
  .map((c) => {
    const who = c.user?.type === 'User' ? c.user.login : `[${c.user?.login}]`;
    return `${who}: ${c.body?.slice(0, 300)}`;
  })
  .join('\n\n');

console.log(priorFeedback || '(empty — all comments filtered by skipMarkers)');

// --- Show what the prompt's "Existing review comments" section would look like ---

console.log('\n\n=== Simulated prompt section: "Existing review comments" ===\n');

const priorReviews = reviewComments
  .slice(0, 10)
  .map((c) => `- ${c.path}:${c.line} — ${c.body?.slice(0, 300)}`)
  .join('\n');

console.log(priorReviews || '(empty — no review comments)');

console.log('\n\n=== Smoke test complete ===');
