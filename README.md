# Codebase Digest

Codebase Digest is a command-line tool written in Python that helps you analyze and understand your codebase. It provides a structured overview of your project's directory structure, file sizes, token counts, and even consolidates the content of all text-based files into a single output for easy analysis with Large Language Models (LLMs).

## Features

* **Directory Tree Visualization:** Generates a hierarchical tree view of your project's directory structure, optionally including file sizes and ignoring specified files/directories.
* **Codebase Statistics:** Calculates total files, directories, code size, and token counts for your project.
* **File Content Consolidation:** Consolidates the content of all text-based files into a single output file (useful for LLM analysis).
* **.gitignore Support:** Respects your .gitignore file to exclude unwanted files and directories from the analysis.
* **Customizable Output:** Choose between text or JSON output formats and customize the level of detail included.
* **Colored Console Output:** Provides a visually appealing and informative summary in the console..

## Installation

### Option 1: Install via pip (Recommended)

```bash
pip install codebase-digest
```


### Option 2: Clone the repository

```bash
git clone https://github.com/kamilstanuch/codebase-digest.git
cd codebase-digest
pip install -r requirements.txt
```

## Usage

```bash
cdigest [path_to_directory] [options]
```

## Options

```bash
path_to_directory: Path to the directory you want to analyze.
-d, --max-depth: Maximum depth for directory traversal.
-o, --output: Output format (text or json). Default: text.
-f, --file: Output file name (default: codebase_analysis.txt or codebase_analysis.json).
--show-tree: Show directory tree in console output (always included in text file output).
--show-size: Show file sizes in directory tree.
--show-ignored: Show ignored files and directories in tree.
--ignore-ext: Additional file extensions to ignore (e.g., .pyc .log).
--no-content: Exclude file contents from the output.
--include-git: Include .git directory in the analysis.
--max-size: Maximum allowed text content size in KB (default: 10240 KB).
```

```bash
cdigest my_project -d 3 -o json --show-size --ignore-ext .pyc .log
```

# 10 LLM Prompts for Enhanced Codebase Analysis 

## I. Code Quality & Understanding:

### 1. Codebase Error and Inconsistency Analysis

```bash
**Objective:** Identify potential errors and inconsistencies within the provided codebase.

**Instructions:**

1. **Analyze the attached code** for the following:
    * Syntax errors and logical flaws.
    * Inconsistencies in variable and function naming conventions.
    * Code duplication.
    * Performance bottlenecks.
    * Violations of established coding best practices. 
2. **Structure your analysis clearly**, pinpointing specific code snippets and providing detailed descriptions of the identified issues.
3. **Prioritize clarity and conciseness** in your explanations.

**Expected Output:** A comprehensive report detailing errors and inconsistencies, organized by code section or error type, with actionable insights for improvement. 
```

### 2. Codebase Risk Assessment 

```bash
**Objective:** Identify code segments within the provided codebase that could potentially lead to future issues.

**Instructions:**

1. **Analyze the attached code** with a focus on:
    * Code that is difficult to understand and maintain (code smells).
    * Fragments that might cause errors under specific conditions (edge cases).
    * Code that deviates from established coding standards.
2. **Provide detailed justifications for your concerns**, explaining the potential risks associated with each identified segment.
3. **Suggest potential solutions or mitigation strategies** to address the identified risks.

**Expected Output:** A report highlighting potential risk areas within the codebase, with clear explanations of the risks and actionable recommendations for improvement.
```

### 3. Codebase Documentation Generation

```bash
**Objective:** Generate comprehensive and user-friendly documentation for the provided codebase.

**Instructions:**

1. **Analyze the attached code** and identify key components, functionalities, and APIs.
2. **Generate documentation that includes:**
    * API specifications with detailed descriptions of endpoints, parameters, and responses.
    * Function descriptions with clear explanations of their purpose, inputs, and outputs.
    * Usage examples demonstrating how to interact with the codebase effectively.
3. **Structure the documentation logically** and use a consistent format for clarity.
4. **Prioritize clarity, conciseness, and accuracy** in your documentation.

**Expected Output:**  Well-structured and informative documentation that facilitates understanding and utilization of the codebase by developers and other stakeholders.
```

## II. Learning & Knowledge Extraction:

### 4. User Story Reconstruction from Code

```bash
**Objective:** Reconstruct the user stories that likely served as the basis for the development of the provided codebase.

**Instructions:**

1. **Analyze the attached code** to identify the core functionalities of the application.
2. **Infer the user needs** that each functionality aims to address.
3. **Formulate user stories** using the following template: "As a [user role], I want [functionality], so that [benefit]."
4. **Identify potential missing user stories**. Suggest functionalities that could be added to the application to better meet user needs.

**Expected Output:** A list of reconstructed user stories based on the code's functionalities, along with insights into potential missing user stories and suggestions for application enhancements.
```

### 5. Code-Based Mini-Lesson Generation

```bash
**Objective:** Create a series of mini-lessons that explain the key concepts implemented within the provided codebase.

**Instructions:**

1. **Divide the code into logical sections** and create a separate lesson for each.
2. **Start with the simplest concepts** and gradually progress to more complex ones.
3. **Use code examples from the application** to illustrate the discussed concepts.
4. **Include exercises and quizzes** to help learners test their understanding.
5. **Focus on clarity and pedagogical effectiveness** in your lesson design.

**Expected Output:** A set of well-structured mini-lessons covering the key concepts of the application, with code examples, exercises, and quizzes to facilitate learning.
```

## III. Code Improvement & Transformation:

### 6. Codebase Best Practice Analysis

```bash
**Objective:** Analyze the provided codebase and identify examples of both good and bad programming practices.

**Instructions:**

1. **Carefully review the attached code** and pinpoint instances of exemplary and problematic coding practices.
2. **For each example, provide a detailed analysis** that includes:
    * **What is good/bad about the specific solution?**
    * **What concepts or principles underpin the solution?**
    * **What are the potential positive/negative consequences of using this solution?**

**Expected Output:** A comprehensive report highlighting both positive and negative coding practices within the codebase, with in-depth explanations and analysis of their impact.
```

### 7. Codebase Translation to Another Programming Language

```bash
**Objective:**  Translate the provided codebase from [Source Language] to [Target Language] while preserving its functionality and structure.

**Instructions:**

1. **Analyze the attached code** written in [Source Language] and understand its logic and functionalities.
2. **Translate the code** into [Target Language], ensuring that the translated code performs the same tasks as the original code.
3. **Maintain the original code's structure and organization** as much as possible in the translated version. 
4. **Adhere to the coding conventions and best practices** of the target language.
5. **Comment the translated code** to explain any significant changes or adaptations made during the translation process.

**Expected Output:** A functional codebase in [Target Language] that accurately reflects the functionality and structure of the original [Source Language] codebase.
```

### 8. Codebase Refactoring for Improved Readability and Performance

```bash
**Objective:** Refactor the provided codebase to enhance its readability, maintainability, and performance.

**Instructions:**

1. **Analyze the attached code** and identify areas that can be improved in terms of code clarity, structure, and efficiency.
2. **Suggest specific code transformations and optimizations** to address the identified areas for improvement.
3. **Prioritize refactoring techniques** that improve code readability without introducing unnecessary complexity.
4. **Consider performance implications** of your suggested refactoring and aim for solutions that enhance efficiency without sacrificing clarity. 
5. **Provide clear explanations** for each refactoring suggestion, justifying its benefits and potential impact.

**Expected Output:**  A set of actionable refactoring suggestions with detailed explanations of their benefits and potential impact on code quality and performance.
```

## IV. Testing & Security:

### 9. Unit Test Generation for Codebase

```bash
**Objective:** Generate unit tests for the provided codebase to ensure code correctness and prevent regressions.

**Instructions:**

1. **Analyze the attached code** and identify its core functions and methods.
2. **Generate unit tests** that cover a wide range of input values and expected outputs for each function/method.
3. **Follow best practices for unit testing**, including:
    * **Test one function/method per test case.**
    * **Use descriptive test names.**
    * **Assert expected outcomes clearly.**
    * **Keep tests independent and isolated.**
4. **Prioritize test coverage for critical functionalities** and edge cases.

**Expected Output:** A comprehensive suite of unit tests that can be used to verify the correctness of the codebase and prevent regressions during future development.
```

### 10. Security Vulnerability Analysis of Codebase

```bash
**Objective:** Identify potential security vulnerabilities within the provided codebase.

**Instructions:**

1. **Analyze the attached code** with a focus on identifying common security weaknesses such as:
    * SQL injection.
    * Cross-site scripting (XSS).
    * Cross-site request forgery (CSRF).
    * Authentication and authorization bypasses.
    * Data exposure.
2. **For each identified vulnerability, provide a detailed explanation** of:
    * The nature of the vulnerability.
    * The potential impact of exploitation.
    * Recommendations for mitigation using secure coding practices.
3. **Prioritize vulnerabilities based on their severity and potential impact.**

**Expected Output:** A comprehensive security report highlighting potential vulnerabilities within the codebase, along with clear explanations of their risks and actionable recommendations for remediation.
```