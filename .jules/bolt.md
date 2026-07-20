
## 2024-05-16 - Add Debouncing to Search Query in Dashboard
**Learning:** The `Dashboard` component was firing a React Query API request on every keystroke in the search bar because the `searchQuery` state was directly linked to the `queryKey`. This is a classic frontend performance bottleneck that causes unnecessary network traffic and backend load.
**Action:** When implementing search-as-you-type inputs, always introduce a debounced state variable using `setTimeout` within a `useEffect` (or a dedicated hook) to delay the API call until the user pauses typing. This significantly reduces the number of requests and improves responsiveness.
