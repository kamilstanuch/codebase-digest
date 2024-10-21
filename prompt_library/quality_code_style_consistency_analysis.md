# Code Style Consistency Analysis

**Objective:** Conduct a thorough analysis of the codebase to evaluate consistency in code style, naming conventions, and formatting, identifying deviations from the project's style guide or industry best practices, and providing actionable recommendations for improvement.

**Instructions:**

1. Review the entire codebase, focusing on:
   - Naming conventions (variables, functions, classes, modules)
   - Code formatting (indentation, line length, whitespace usage)
   - Comment style and frequency
   - File organization and structure
   - Language-specific idioms and best practices

2. For each identified inconsistency or style issue, analyze:

   a. Location:
      - File path
      - Line number(s) or range

   b. Issue Details:
      - Type of inconsistency (e.g., naming, formatting, structure)
      - Description of the deviation from expected style
      - Comparison with the correct style (if applicable)

   c. Impact Assessment:
      - Effect on code readability
      - Potential for introducing bugs or maintenance issues
      - Impact on team collaboration and onboarding of new developers

   d. Correction Suggestions:
      - Specific recommendations for addressing the issue
      - Code snippets demonstrating the correct style (if applicable)
      - Explanation of the rationale behind the suggested changes

3. Identify patterns and trends in style inconsistencies across the codebase:
   - Are certain types of issues more prevalent?
   - Do inconsistencies cluster in specific modules or areas of the codebase?
   - Are there differences in style between different team members or over time?

4. Assess the overall adherence to the project's style guide or industry standards:
   - Percentage of code adhering to expected style
   - Areas of high compliance and areas needing improvement
   - Comparison with similar projects or industry benchmarks (if available)

5. Analyze the effectiveness of current style enforcement mechanisms:
   - Evaluate the use of linters, formatters, or other automated tools
   - Assess the consistency of code review practices related to style

6. Provide strategic recommendations for improving code style consistency:
   - Suggest updates or clarifications to the project's style guide
   - Recommend tools or processes to automate style enforcement
   - Propose training or knowledge-sharing initiatives to improve team awareness
   - Suggest a phased approach for addressing identified issues, prioritizing based on impact and effort

**Expected Output:** A comprehensive analysis of the codebase's style consistency, including:

1. Executive summary of findings and key recommendations
2. Detailed analysis of style inconsistencies, grouped by category and severity
3. Statistical overview of style adherence across the codebase
4. In-depth discussion of patterns and trends in style issues
5. Evaluation of current style enforcement mechanisms
6. Strategic recommendations for improving overall code style consistency
7. Appendices with detailed examples and code snippets

For each identified issue, use the following format:

File: [file path]
Line(s): [line number(s) or range]
Issue Type: [naming/formatting/structure/etc.]
Description: [detailed description of the inconsistency]
Impact:
  - Readability: [low/medium/high] - [brief explanation]
  - Maintainability: [low/medium/high] - [brief explanation]
  - Collaboration: [low/medium/high] - [brief explanation]
Correct Style:
```[language]
[code snippet demonstrating correct style]
```
Suggestion:
  - [specific correction recommendation]
  - Rationale: [explanation of why this change improves consistency]

Conclude with an overall assessment of the code style consistency in the project, including a roadmap for addressing identified issues and implementing long-term improvements in coding practices and team collaboration.