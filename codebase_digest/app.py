 # CodeConsolidator - Consolidates and analyzes codebases for insights.

import os
import argparse
import json
from collections import defaultdict
import fnmatch
import mimetypes
import tiktoken
from colorama import init, Fore, Back, Style
import sys
import pyperclip
import xml.etree.ElementTree as ET
import html

# Initialize colorama for colorful console output.
init()

# At the top of the file, after imports
DEFAULT_IGNORE_PATTERNS = [
    '*.pyc', '*.pyo', '*.pyd', '__pycache__',  # Python
    'node_modules', 'bower_components',        # JavaScript
    '.git', '.svn', '.hg', '.gitignore',                    # Version control
    'venv', '.venv', 'env',                    # Virtual environments
    '.idea', '.vscode',                        # IDEs
    '*.log', '*.bak', '*.swp', '*.tmp',        # Temporary and log files
    '.DS_Store',                               # macOS
    'Thumbs.db',                               # Windows
    'build', 'dist',                           # Build directories
    '*.egg-info',                              # Python egg info
    '*.so', '*.dylib', '*.dll'                 # Compiled libraries
]

def print_frame(text):
    """Prints a framed text box with colored borders."""
    width = max(len(line) for line in text.split('\n')) + 4
    print(Fore.CYAN + "+" + "-" * (width - 2) + "+")
    for line in text.split('\n'):
        print(Fore.CYAN + "| " + Fore.WHITE + line.ljust(width - 4) + Fore.CYAN + " |")
    print(Fore.CYAN + "+" + "-" * (width - 2) + "+" + Style.RESET_ALL)

def load_gitignore(path):
    """Loads .gitignore patterns from a given path."""
    gitignore_patterns = []
    gitignore_path = os.path.join(path, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            gitignore_patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return gitignore_patterns

def should_ignore(path, base_path, ignore_patterns):
    """Checks if a file or directory should be ignored based on patterns."""
    name = os.path.basename(path)
    rel_path = os.path.relpath(path, base_path)
    abs_path = os.path.abspath(path)
    
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(name, pattern) or \
           fnmatch.fnmatch(rel_path, pattern) or \
           fnmatch.fnmatch(abs_path, pattern) or \
           (pattern.startswith('/') and fnmatch.fnmatch(abs_path, os.path.join(base_path, pattern[1:]))) or \
           any(fnmatch.fnmatch(part, pattern) for part in rel_path.split(os.sep)):
            print(f"Debug: Ignoring {path} due to pattern {pattern}")
            return True
    return False

def is_text_file(file_path):
    """Determines if a file is likely a text file based on its content."""
    try:
        with open(file_path, 'rb') as file:
            chunk = file.read(1024)
        return not bool(chunk.translate(None, bytes([7, 8, 9, 10, 12, 13, 27] + list(range(0x20, 0x100)))))
    except IOError:
        return False

def count_tokens(text):
    """Counts the number of tokens in a text string using tiktoken."""
    enc = tiktoken.get_encoding("cl100k_base")
    try:
        return len(enc.encode(text, disallowed_special=()))
    except Exception as e:
        print(f"Warning: Error counting tokens: {str(e)}")
        return 0

def read_file_content(file_path):
    """Reads the content of a file, handling potential encoding errors."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def analyze_directory(path, ignore_patterns, base_path, include_git=False, max_depth=None, current_depth=0):
    """Recursively analyzes a directory and its contents."""
    if max_depth is not None and current_depth > max_depth:
        return None

    result = {
        "name": os.path.basename(path),
        "type": "directory",
        "size": 0,
        "children": [],
        "total_tokens": 0,
        "file_count": 0,
        "dir_count": 0,
        "text_content_size": 0,
        "total_text_size": 0  # New field for total size of all text files
    }

    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            
            # Skip .git directory unless explicitly included
            if item == '.git' and not include_git:
                continue

            is_ignored = should_ignore(item_path, base_path, ignore_patterns)
            print(f"Debug: Checking {item_path}, ignored: {is_ignored}")  # Debug line

            if os.path.isfile(item_path) and is_text_file(item_path):
                file_size = os.path.getsize(item_path)
                result["total_text_size"] += file_size

            if is_ignored:
                continue  # Skip ignored items for further analysis

            # Log progress
            print(Fore.YELLOW + f"Analyzing: {item_path}" + Style.RESET_ALL)

            if os.path.isfile(item_path):
                file_size = os.path.getsize(item_path)
                is_text = is_text_file(item_path)
                if is_text:
                    content = read_file_content(item_path)
                    tokens = count_tokens(content)
                    print(f"Debug: Text file {item_path}, size: {file_size}, content size: {len(content)}")
                else:
                    content = "[Non-text file]"
                    tokens = 0
                    print(f"Debug: Non-text file {item_path}, size: {file_size}")
                child = {
                    "name": item,
                    "type": "file",
                    "size": file_size,
                    "tokens": tokens,
                    "content": content,
                    "is_ignored": is_ignored
                }
                result["children"].append(child)
                if not is_ignored:
                    result["size"] += file_size
                    result["total_tokens"] += tokens
                    result["file_count"] += 1
                    if is_text:
                        result["text_content_size"] += len(content)
            elif os.path.isdir(item_path):
                subdir = analyze_directory(item_path, ignore_patterns, base_path, include_git, max_depth, current_depth + 1)
                if subdir:
                    subdir["is_ignored"] = is_ignored
                    result["children"].append(subdir)
                    if not is_ignored:
                        result["size"] += subdir["size"]
                        result["total_tokens"] += subdir["total_tokens"]
                        result["file_count"] += subdir["file_count"]
                        result["dir_count"] += 1 + subdir["dir_count"]
                        result["text_content_size"] += subdir["text_content_size"]
    except PermissionError:
        print(Fore.RED + f"Permission denied: {path}" + Style.RESET_ALL)

    return result

def generate_tree_string(node, prefix="", is_last=True, show_size=False, show_ignored=False, use_color=False):
    """Generates a string representation of the directory tree."""
    if node.get("is_ignored", False) and not show_ignored:
        return ""

    if use_color:
        result = prefix + (Fore.GREEN + "└── " if is_last else "├── ")
        result += Fore.BLUE + node["name"] + Style.RESET_ALL
    else:
        result = prefix + ("└── " if is_last else "├── ") + node["name"]

    if show_size and node["type"] == "file":
        size_str = f" ({node['size']} bytes)"
        result += Fore.YELLOW + size_str + Style.RESET_ALL if use_color else size_str

    if node.get("is_ignored", False):
        ignored_str = " [IGNORED]"
        result += Fore.RED + ignored_str + Style.RESET_ALL if use_color else ignored_str

    result += "\n"

    if node["type"] == "directory":
        prefix += "    " if is_last else "│   "
        children = node["children"]
        if not show_ignored:
            children = [child for child in children if not child.get("is_ignored", False)]
        for i, child in enumerate(children):
            result += generate_tree_string(child, prefix, i == len(children) - 1, show_size, show_ignored, use_color)
    return result

def generate_summary_string(data, estimated_size, use_color=True):
    summary = "\nSummary:\n"
    summary += f"Total files analyzed: {data['file_count']}\n"
    summary += f"Total directories analyzed: {data['dir_count']}\n"
    summary += f"Estimated output size: {estimated_size / 1024:.2f} KB\n"
    summary += f"Actual analyzed size: {data['size'] / 1024:.2f} KB\n"
    summary += f"Total tokens: {data['total_tokens']}\n"
    summary += f"Actual text content size: {data['text_content_size'] / 1024:.2f} KB\n"
    
    if use_color:
        return Fore.CYAN + summary + Style.RESET_ALL
    return summary

def generate_content_string(data):
    """Generates a structured representation of file contents."""
    content = []

    def add_file_content(node, path=""):
        if node["type"] == "file" and not node.get("is_ignored", False) and node["content"] != "[Non-text file]":
            content.append({
                "path": os.path.join(path, node["name"]),
                "content": node["content"]
            })
        elif node["type"] == "directory":
            for child in node["children"]:
                add_file_content(child, os.path.join(path, node["name"]))

    add_file_content(data)
    return content

def generate_markdown_output(data):
    output = f"# Codebase Analysis for: {data['name']}\n\n"
    output += "## Directory Structure\n\n"
    output += "```\n"
    output += generate_tree_string(data, show_size=True, show_ignored=True)
    output += "```\n\n"
    output += "## Summary\n\n"
    output += f"- Total files: {data['file_count']}\n"
    output += f"- Total directories: {data['dir_count']}\n"
    output += f"- Analyzed size: {data['size'] / 1024:.2f} KB\n"
    output += f"- Total text file size (including ignored): {data['total_text_size'] / 1024:.2f} KB\n"
    output += f"- Total tokens: {data['total_tokens']}\n"
    output += f"- Analyzed text content size: {data['text_content_size'] / 1024:.2f} KB\n\n"
    output += "## File Contents\n\n"
    for file in generate_content_string(data):
        output += f"### {file['path']}\n\n```\n{file['content']}\n```\n\n"
    return output

def generate_xml_output(data):
    root = ET.Element("codebase-analysis")
    ET.SubElement(root, "name").text = data['name']
    structure = ET.SubElement(root, "directory-structure")
    structure.text = generate_tree_string(data, show_size=True, show_ignored=True)
    summary = ET.SubElement(root, "summary")
    ET.SubElement(summary, "total-files").text = str(data['file_count'])
    ET.SubElement(summary, "total-directories").text = str(data['dir_count'])
    ET.SubElement(summary, "analyzed-size-kb").text = f"{data['size'] / 1024:.2f}"
    ET.SubElement(summary, "total-text-file-size-kb").text = f"{data['total_text_size'] / 1024:.2f}"
    ET.SubElement(summary, "total-tokens").text = str(data['total_tokens'])
    ET.SubElement(summary, "analyzed-text-content-size-kb").text = f"{data['text_content_size'] / 1024:.2f}"
    contents = ET.SubElement(root, "file-contents")
    for file in generate_content_string(data):
        file_elem = ET.SubElement(contents, "file")
        ET.SubElement(file_elem, "path").text = file['path']
        ET.SubElement(file_elem, "content").text = file['content']
    return ET.tostring(root, encoding="unicode")

def generate_html_output(data):
    output = f"""
    <html>
    <head>
        <title>Codebase Analysis for: {html.escape(data['name'])}</title>
        <style>
            pre {{ white-space: pre-wrap; word-wrap: break-word; }}
        </style>
    </head>
    <body>
    <h1>Codebase Analysis for: {html.escape(data['name'])}</h1>
    <h2>Directory Structure</h2>
    <pre>{html.escape(generate_tree_string(data, show_size=True, show_ignored=True))}</pre>
    <h2>Summary</h2>
    <ul>
    <li>Total files: {data['file_count']}</li>
    <li>Total directories: {data['dir_count']}</li>
    <li>Analyzed size: {data['size'] / 1024:.2f} KB</li>
    <li>Total text file size (including ignored): {data['total_text_size'] / 1024:.2f} KB</li>
    <li>Total tokens: {data['total_tokens']}</li>
    <li>Analyzed text content size: {data['text_content_size'] / 1024:.2f} KB</li>
    </ul>
    <h2>File Contents</h2>
    """
    for file in generate_content_string(data):
        output += f"<h3>{html.escape(file['path'])}</h3><pre>{html.escape(file['content'])}</pre>"
    output += "</body></html>"
    return output

def load_ignore_patterns(args, base_path):
    patterns = set()
    if not args.no_default_ignores:
        patterns.update(DEFAULT_IGNORE_PATTERNS)
    
    if args.ignore:
        patterns.update(args.ignore)
    
    # Load patterns from .cdigestignore file if it exists
    cdigestignore_path = os.path.join(base_path, '.cdigestignore')
    if os.path.exists(cdigestignore_path):
        with open(cdigestignore_path, 'r') as f:
            file_patterns = {line.strip() for line in f if line.strip() and not line.startswith('#')}
        patterns.update(file_patterns)
    
    print(f"Debug: Final ignore patterns: {patterns}")
    return patterns

def estimate_output_size(path, ignore_patterns, base_path):
    estimated_size = 0
    file_count = 0
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), base_path, ignore_patterns)]
        for file in files:
            file_path = os.path.join(root, file)
            if not should_ignore(file_path, base_path, ignore_patterns) and is_text_file(file_path):
                file_size = os.path.getsize(file_path)
                estimated_size += file_size
                file_count += 1
    
    # Add some overhead for the directory structure and summary
    estimated_size += file_count * 100  # Assume 100 bytes per file for structure
    estimated_size += 1000  # Add 1KB for summary

    return estimated_size

def main():
    parser = argparse.ArgumentParser(
        description="Analyze and visualize codebase structure.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("path", nargs="?", 
                        help="Path to the directory to analyze")
    parser.add_argument("-d", "--max-depth", type=int, 
                        help="Maximum depth for directory traversal")
    parser.add_argument("-o", "--output-format", 
                        choices=["text", "json", "markdown", "xml", "html"],
                        default="text", 
                        help="Output format (default: text)")
    parser.add_argument("-f", "--file", 
                        help="Output file name (default: <directory_name>_codebase_digest.<format_extension>)")
    parser.add_argument("--show-size", action="store_true", 
                        help="Show file sizes in directory tree")
    parser.add_argument("--show-ignored", action="store_true", 
                        help="Show ignored files and directories in tree")
    parser.add_argument("--ignore", nargs="+", default=None,
                        help="Additional patterns to ignore. These will be added to the default ignore patterns.\n"
                             "Examples:\n"
                             "  --ignore '*.txt' 'temp_*' '/path/to/specific/file.py'\n"
                             "Patterns can use wildcards (* and ?) and can be:\n"
                             "  - Filenames (e.g., 'file.txt')\n"
                             "  - Directory names (e.g., 'node_modules')\n"
                             "  - File extensions (e.g., '*.pyc')\n"
                             "  - Paths (e.g., '/path/to/ignore')\n"
                             f"Default ignore patterns: {', '.join(DEFAULT_IGNORE_PATTERNS)}")
    parser.add_argument("--no-default-ignores", action="store_true",
                        help="Do not use default ignore patterns. Only use patterns specified by --ignore.")
    parser.add_argument("--no-content", action="store_true", 
                        help="Exclude file contents from the output")
    parser.add_argument("--include-git", action="store_true", 
                        help="Include .git directory in the analysis (ignored by default)")
    parser.add_argument("--max-size", type=int, default=10240, 
                        help="Maximum allowed text content size in KB (default: 10240 KB)")
    parser.add_argument("--copy-to-clipboard", action="store_true", 
                        help="Copy the output to clipboard after analysis")
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if not args.path:
        print(Fore.RED + "Error: Path argument is required." + Style.RESET_ALL)
        parser.print_help(sys.stderr)
        sys.exit(1)

    ignore_patterns = load_ignore_patterns(args, args.path)
    print(f"Debug: Ignore patterns after load_ignore_patterns: {ignore_patterns}")

    print_frame("Codebase Digest")
    print(Fore.CYAN + "Analyzing directory: " + Fore.WHITE + args.path + Style.RESET_ALL)

    # Estimate the output size
    estimated_size = estimate_output_size(args.path, ignore_patterns, args.path)
    print(f"Estimated output size: {estimated_size / 1024:.2f} KB")

    # Perform a quick size check of all text files
    total_size = sum(os.path.getsize(os.path.join(dirpath, f)) 
                     for dirpath, _, filenames in os.walk(args.path) 
                     for f in filenames if is_text_file(os.path.join(dirpath, f)))

    if estimated_size / 1024 > args.max_size:
        print(Fore.YELLOW + f"\nWarning: The estimated output size ({estimated_size / 1024:.2f} KB) exceeds the maximum allowed size ({args.max_size} KB)." + Style.RESET_ALL)
        proceed = input("Do you want to proceed? (y/n): ").lower().strip()
        if proceed != 'y':
            print(Fore.YELLOW + "Analysis aborted." + Style.RESET_ALL)
            sys.exit(0)
    elif total_size / 1024 > args.max_size * 2:  # Only show this if total size is significantly larger
        print(Fore.YELLOW + f"\nNote: The total size of all text files in the directory ({total_size / 1024:.2f} KB) is significantly larger than the estimated output size." + Style.RESET_ALL)
        print(Fore.YELLOW + "This is likely due to large files or directories that will be ignored in the analysis." + Style.RESET_ALL)

    try:
        data = analyze_directory(args.path, ignore_patterns, args.path, include_git=args.include_git, max_depth=args.max_depth)
        
        # Generate output based on the chosen format
        if args.output_format == "json":
            output = json.dumps(data, indent=2)
            file_extension = "json"
        elif args.output_format == "markdown":
            output = generate_markdown_output(data)
            file_extension = "md"
        elif args.output_format == "xml":
            output = generate_xml_output(data)
            file_extension = "xml"
        elif args.output_format == "html":
            output = generate_html_output(data)
            file_extension = "html"
        else:  # text
            output = f"Codebase Analysis for: {args.path}\n"
            output += "\nDirectory Structure:\n"
            output += generate_tree_string(data, show_size=args.show_size, show_ignored=args.show_ignored, use_color=False)
            output += generate_summary_string(data, estimated_size, use_color=False)
            if not args.no_content:
                output += "\nFile Contents:\n"
                for file in generate_content_string(data):
                    output += f"\n{'=' * 50}\n"
                    output += f"File: {file['path']}\n"
                    output += f"{'=' * 50}\n"
                    output += file['content']
                    output += "\n"
            file_extension = "txt"

        # Save the output to a file
        file_name = args.file or f"{os.path.basename(args.path)}_codebase_digest.{file_extension}"
        full_path = os.path.abspath(file_name)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(output)
        print(Fore.GREEN + f"\nAnalysis saved to: {full_path}" + Style.RESET_ALL)

        # Print colored summary to console immediately
        print_frame("Analysis Summary")
        print(generate_tree_string(data, show_size=args.show_size, show_ignored=args.show_ignored, use_color=True))
        print(generate_summary_string(data, estimated_size, use_color=True))

        # Handle clipboard functionality for all formats
        if args.copy_to_clipboard:
            try:
                pyperclip.copy(output)
                print(Fore.GREEN + "Output copied to clipboard!" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Failed to copy to clipboard: {str(e)}" + Style.RESET_ALL)
        else:
            copy_to_clipboard = input("Do you want to copy the output to clipboard? (y/n): ").lower().strip()
            if copy_to_clipboard == 'y':
                try:
                    pyperclip.copy(output)
                    print(Fore.GREEN + "Output copied to clipboard!" + Style.RESET_ALL)
                except Exception as e:
                    print(Fore.RED + f"Failed to copy to clipboard: {str(e)}" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"An error occurred: {str(e)}" + Style.RESET_ALL)
        sys.exit(1)

    if data['text_content_size'] / 1024 > args.max_size:
        print(Fore.RED + f"\nWarning: The text content size ({data['text_content_size'] / 1024:.2f} KB) exceeds the maximum allowed size ({args.max_size} KB)." + Style.RESET_ALL)
        proceed = input("Do you want to proceed? (y/n): ").lower().strip()
        if proceed != 'y':
            print(Fore.YELLOW + "Analysis aborted." + Style.RESET_ALL)
            sys.exit(0)

if __name__ == "__main__":
    main()