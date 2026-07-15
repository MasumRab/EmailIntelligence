## 2026-07-15 - [Added React.memo to EmailList]
**Learning:** The EmailList component renders a large list of DOM nodes. When its parent dashboard component re-renders due to unrelated state changes, the entire list is unnecessarily re-rendered, potentially blocking the main thread. Implementing `React.memo` is a standard optimization in this codebase architecture for components rendering long lists.
**Action:** Use `React.memo` for list components to prevent expensive DOM updates when props haven't changed.
