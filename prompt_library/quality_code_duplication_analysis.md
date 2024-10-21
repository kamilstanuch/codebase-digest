# Code Duplication Analysis

**Objective:** Analyze the codebase to identify duplicated code fragments, providing insights into potential maintainability issues and suggesting refactoring opportunities.

**Instructions:**

1. Review the codebase and identify instances of duplicated code.

2. For each identified duplication, analyze:

   a. Location:
      - File paths of affected files
      - Line numbers in each file

   b. Duplication Details:
      - Length of the duplicated code fragment (in lines of code)
      - Content or purpose of the duplicated code

   c. Impact Assessment:
      - Potential impact on code maintainability
      - Risks associated with the duplication (e.g., inconsistent updates)

   d. Refactoring Opportunities:
      - Suggestions for extracting duplicated code into reusable functions or classes
      - Potential design patterns or architectural changes to eliminate duplication

3. Identify patterns or trends in code duplication across the codebase.

4. Assess the overall impact of code duplication on the project's maintainability and scalability.

5. Suggest improvements to reduce code duplication, considering:
   - Priority areas based on the extent and impact of duplication
   - Refactoring strategies that align with the project's architecture
   - Tools or processes to prevent future code duplication

**Expected Output:** A comprehensive analysis of the codebase's code duplication, including:

1. An overview of the duplication analysis findings
2. Detailed breakdowns for each identified duplication
3. General recommendations for reducing and preventing code duplication
4. If applicable, a summary of duplication trends or patterns observed in the codebase

For each identified duplication, use the following format:

Files:
- [file path 1]
- [file path 2]
Line(s): 
- [file 1 line numbers]
- [file 2 line numbers]
Length: [number of duplicated lines]
Impact: [potential impact on maintainability]
Suggestions:
- [refactoring suggestion 1]
- [refactoring suggestion 2]
- ...

If no significant duplications are found, provide a summary stating that the codebase has minimal code duplication.

Conclude with an overall assessment of the code duplication in the project, including recommendations for addressing the most critical instances and strategies for maintaining a DRY (Don't Repeat Yourself) codebase.