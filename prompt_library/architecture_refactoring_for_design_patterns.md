## Suggest Refactoring for Design Patterns 

**Objective:** Analyze the codebase and identify opportunities to refactor code by implementing suitable design patterns to improve code maintainability, extensibility, or reusability.

**Instructions:**

1. **Analyze the codebase:**  Examine the existing code structure, identify areas that are complex, difficult to maintain, or lack flexibility.
2. **Identify potential design pattern applications:** Determine if any of the following situations exist:
    * **Code Smells:** Look for common code smells like "Large Class", "Long Method", "Shotgun Surgery" (many small changes across multiple classes), or "Divergent Change" (one class changing for multiple reasons) as indicators for refactoring. 
    * **Repetitive Code:** Identify duplicated code or logic that could be extracted and made reusable.
    * **Tight Coupling:** Look for areas where components are too tightly dependent on each other, making it difficult to change one without affecting others.
    * **Lack of Flexibility:** Identify code that is difficult to extend or modify to accommodate new requirements. 
3. **Suggest specific design patterns:**  Based on your analysis, recommend suitable design patterns to address the identified issues. For each suggestion:
    * **Name the pattern.** 
    * **Explain why the pattern is a good fit for the specific situation.**
    * **Describe how the pattern should be implemented:** Include specific details about which classes or modules should be created or modified.
    * **Illustrate with code examples (if possible):** Show how the code could be refactored using the suggested pattern. 

**Expected Output:** A report (or a series of suggestions) that:

1. Clearly identifies specific areas in the codebase that would benefit from refactoring.
2. Recommends appropriate design patterns to address each identified issue.
3. Provides detailed explanations and (ideally) code examples to guide the refactoring process. 