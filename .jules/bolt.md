## 2024-05-14 - [Bolt: Debounce search input to reduce API calls]
**Learning:** In React Query setups tied directly to user input (like search bars), each keystroke can trigger an immediate API request and database query. This causes unnecessary load. Using a custom `useDebounce` hook resolves this nicely without any major architectural changes.
**Action:** Next time I see an un-debounced search input tied to data fetching, apply a debounce strategy to significantly improve performance.
