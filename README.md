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
--copy-to-clipboard: Copy the output to clipboard.
```

```bash
cdigest my_project -d 3 -o json --show-size --ignore-ext .pyc .log
```

# LLM Prompts for Enhanced Codebase Analysis 

We've prepared a set of prompts to help you analyze and improve your codebase using Large Language Models. These prompts are stored in the `prompt_library` directory for easy access and management.

You can use these prompts with various LLM interfaces:
- Directly in the [Cursor.sh IDE](https://cursor.sh/) for an integrated development experience.
- With [Gemini models](https://deepmind.google/technologies/gemini/) for larger codebases (up to 2,097,152 tokens).
- In any other LLM interface of your choice.

## Use Cases

1. **Codebase Mapping and Learning**: Quickly understand the structure and functionality of a new or complex codebase.
2. **Improving User Stories**: Analyze existing code to refine or generate user stories, ensuring better alignment between code and business requirements.
3. **Initial Security Analysis**: Perform a preliminary security assessment to identify potential vulnerabilities.
4. **Code Quality Enhancement**: Identify areas for improvement in code quality, readability, and maintainability.
5. **Documentation Generation**: Automatically generate or improve codebase documentation.
6. **Learning Tool**: Use as a teaching aid to explain complex coding concepts or architectures.
7. **Business Alignment**: Analyze how the codebase supports business objectives and identify potential improvements.
8. **Stakeholder Communication**: Generate insights to facilitate discussions with non-technical stakeholders.

## Prompt Categories

### I. Code Quality & Understanding:
- [Codebase Error and Inconsistency Analysis](prompt_library/quality_error_analysis.md): Identify and analyze errors and inconsistencies in the codebase.
- [Codebase Risk Assessment](prompt_library/quality_risk_assessment.md): Evaluate potential risks within the codebase.
- [Codebase Documentation Generation](prompt_library/quality_documentation_generation.md): Automatically generate or improve codebase documentation.

### II. Learning & Knowledge Extraction:
- [User Story Reconstruction from Code](prompt_library/learning_user_story_reconstruction.md): Reconstruct and structure user stories based on the codebase.
- [Code-Based Mini-Lesson Generation](prompt_library/learning_mini_lesson_generation.md): Create mini-lessons to explain complex coding concepts or architectures.

### III. Code Improvement & Transformation:
- [Codebase Best Practice Analysis](prompt_library/improvement_best_practice_analysis.md): Analyze the codebase for good and bad programming practices.
- [Codebase Translation to Another Programming Language](prompt_library/improvement_language_translation.md): Translate the codebase from one programming language to another.
- [Codebase Refactoring for Improved Readability and Performance](prompt_library/improvement_refactoring.md): Suggest refactoring improvements for better readability and performance.

### IV. Testing & Security:
- [Unit Test Generation for Codebase](prompt_library/testing_unit_test_generation.md): Generate unit tests for the provided codebase.
- [Security Vulnerability Analysis of Codebase](prompt_library/security_vulnerability_analysis.md): Identify potential security vulnerabilities in the codebase.

### V. Business & Stakeholder Analysis:
- [Business Impact Analysis](prompt_library/business_impact_analysis.md): Identify key features and their potential business impact.
- [Stakeholder Persona Generation](prompt_library/stakeholder_persona_generation.md): Infer potential stakeholder personas based on codebase functionalities.
- [Business Model Canvas Analysis](prompt_library/business_model_canvas_analysis.md): Analyze business implications using the Business Model Canvas framework.
- [Value Proposition Canvas Analysis](prompt_library/value_proposition_canvas_analysis.md): Align technical features with user needs and benefits.
- [SWOT Analysis](prompt_library/swot_analysis.md): Evaluate the codebase's current state and future potential.
- [Jobs to be Done (JTBD) Analysis](prompt_library/jobs_to_be_done_analysis.md): Understand core user needs and identify potential improvements.
- [Lean Canvas Analysis](prompt_library/lean_canvas_analysis.md): Evaluate business potential and identify areas for improvement or pivot.
- [OKR (Objectives and Key Results) Analysis](prompt_library/okr_analysis.md): Align codebase features with potential business objectives and key results.
- [Customer Journey Map Analysis](prompt_library/customer_journey_map_analysis.md): Map how different parts support various stages of the user's journey.
- [Value Chain Analysis](prompt_library/value_chain_analysis.md): Understand how the codebase supports the larger value creation process.

For detailed instructions on how to use these prompts, please refer to the individual files in the `prompt_library` directory.

## Conclusion

This collection of prompts covers a wide range of analysis techniques, from technical code quality assessments to business-oriented evaluations. By using these prompts with Large Language Models, developers and stakeholders can gain valuable insights into their codebase and its alignment with business objectives.

For detailed instructions on how to use each prompt, please refer to the individual files in the `prompt_library` directory.