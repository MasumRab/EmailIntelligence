## 2026-11-06 - [Bolt: Debounce search input to reduce API calls]
**Learning:** The dashboard search input was tied directly to the React Query key for fetching emails, causing unnecessary API requests per keystroke.
**Action:** Implemented a `useDebounce` hook to wrap the search input state before passing it to `useQuery`, significantly reducing backend load and UI sluggishness. This change was ultimately integrated by another PR and the PR attempting to resolve this task was closed as obsolete.
