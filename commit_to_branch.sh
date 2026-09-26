#!/bin/bash
BRANCH="sentinel-fix-security-headers-18398192057925240698"

# 1. Get the repository ID
REPO_INFO=$(gh api graphql -f query='
  query {
    repository(owner: "MasumRab", name: "EmailIntelligence") {
      nameWithOwner
    }
  }
')
REPO_NAME_WITH_OWNER=$(echo "$REPO_INFO" | jq -r '.data.repository.nameWithOwner')

# 2. Get the latest commit OID for the branch
BRANCH_INFO=$(gh api graphql -f query='
  query($repo: String!, $branch: String!) {
    repository(owner: "MasumRab", name: $repo) {
      ref(qualifiedName: $branch) {
        target {
          ... on Commit {
            oid
          }
        }
      }
    }
  }
' -F repo="EmailIntelligence" -F branch="refs/heads/$BRANCH")
EXPECTED_HEAD_OID=$(echo "$BRANCH_INFO" | jq -r '.data.repository.ref.target.oid')

# 3. Prepare the file changes payload
# Read file contents and base64 encode them
FILE1_CONTENT=$(base64 -w 0 .github/workflows/gemini-invoke.yml)
FILE2_CONTENT=$(base64 -w 0 .github/workflows/gemini-review.yml)
FILE3_CONTENT=$(base64 -w 0 .github/workflows/gemini-triage.yml)

# 4. Construct and execute the mutation
gh api graphql -f query='
  mutation($repoNameWithOwner: String!, $branchName: String!, $expectedHeadOid: GitObjectID!, $file1: Base64String!, $file2: Base64String!, $file3: Base64String!) {
    createCommitOnBranch(input: {
      branch: {
        repositoryNameWithOwner: $repoNameWithOwner,
        branchName: $branchName
      },
      message: {
        headline: "fix(ci): Handle missing Gemini API key gracefully in workflows"
      },
      fileChanges: {
        additions: [
          { path: ".github/workflows/gemini-invoke.yml", contents: $file1 },
          { path: ".github/workflows/gemini-review.yml", contents: $file2 },
          { path: ".github/workflows/gemini-triage.yml", contents: $file3 }
        ]
      },
      expectedHeadOid: $expectedHeadOid
    }) {
      commit {
        oid
        url
      }
    }
  }
' -F repoNameWithOwner="$REPO_NAME_WITH_OWNER" \
  -F branchName="$BRANCH" \
  -F expectedHeadOid="$EXPECTED_HEAD_OID" \
  -F file1="$FILE1_CONTENT" \
  -F file2="$FILE2_CONTENT" \
  -F file3="$FILE3_CONTENT"
