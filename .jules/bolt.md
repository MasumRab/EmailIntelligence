## 2024-05-22 - SmartFilterManager Performance Regression
**Learning:** Pre-calculating derived data (like lowercasing the email body) for every item in a loop is an anti-pattern when that data is not used by all consumers. In `SmartFilterManager`, extracting patterns for every email caused a ~6x performance regression because most filters did not need the expensive body extraction.
**Action:** Only pay for what you use. Lazy evaluation or conditional extraction inside the loop is often better than eager pre-calculation unless the hit rate is very high.
