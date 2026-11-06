# Gemini PR Review Authentication Setup

The `.github/workflows/gemini-review.yml` workflow requires authentication to communicate with the Gemini API.
If this is not configured, the `🔎 Gemini Review` check will fail for every pull request.

To fix this, an operator must configure **one of the following** in the GitHub repository settings.

## Where to configure

Go to your GitHub repository:
**Settings** > **Secrets and variables** > **Actions**

## What to configure

Add ONE of the following:

### Option A: Use a Gemini API Key (Secret)
* Name: `GEMINI_API_KEY`
* Value: Your Gemini API Key from Google AI Studio.
* Type: **Repository Secret**

### Option B: Use a Google API Key (Secret)
* Name: `GOOGLE_API_KEY`
* Value: Your Google Cloud API Key with Gemini API enabled.
* Type: **Repository Secret**

### Option C: Use GCP Workload Identity Federation (Variable)
* Name: `GCP_WIF_PROVIDER`
* Value: The full path to your Workload Identity Provider (e.g. `projects/123456789/locations/global/workloadIdentityPools/my-pool/providers/my-provider`).
* Type: **Repository Variable**

*Note: Once one of these is set, the Gemini Review action will automatically pick it up and run successfully on the next PR update.*
