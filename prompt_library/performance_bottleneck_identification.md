#### Identify Performance Bottlenecks

**Objective:** Analyze the codebase to pinpoint specific areas that negatively impact performance, such as inefficient algorithms, excessive database queries, or slow network requests.

**Instructions:**

1. **Profile the codebase:** Use profiling tools to identify functions or code blocks with high execution time, excessive function calls, or significant resource consumption.
2. **Analyze algorithms:** Review algorithms for complexity and efficiency. Look for opportunities to use more optimal algorithms or data structures.
3. **Inspect database interactions:**
   -  Identify queries that are executed frequently or take a long time to complete.
   - Analyze query plans to identify inefficient joins, missing indexes, or other database-related bottlenecks.
4. **Examine network communication:**
    -  Analyze network requests to identify slow responses, excessive data transfer, or unnecessary round trips.
    -  Look for opportunities to implement caching or optimize network communication patterns.
5. **Prioritize based on impact:** Categorize identified bottlenecks based on their potential impact on overall system performance.

**Expected Output:** A prioritized list of performance bottlenecks with clear explanations of:

- The specific code, query, or network operation causing the bottleneck.
- The estimated impact on performance.
-  Potential solutions or optimization strategies.