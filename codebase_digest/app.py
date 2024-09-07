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

# Initialize colorama for colorful console output.
init()

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

def should_ignore(path, ignore_patterns, ignore_extensions):
    """Checks if a file or directory should be ignored based on patterns and extensions."""
    return any(fnmatch.fnmatch(path, pattern) for pattern in ignore_patterns) or \
           os.path.splitext(path)[1].lower() in ignore_extensions

def is_text_file(file_path):
    """Determines if a file is a text file based on its MIME type."""
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith('text')

def count_tokens(text):
    """Counts the number of tokens in a text string using tiktoken."""
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def read_file_content(file_path):
    """Reads the content of a file, handling potential encoding errors."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def analyze_directory(path, ignore_patterns, ignore_extensions, include_git=False, max_depth=None, current_depth=0):
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
        "text_content_size": 0
    }

    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            
            # Skip .git directory unless explicitly included
            if item == '.git' and not include_git:
                continue

            is_ignored = should_ignore(item_path, ignore_patterns, ignore_extensions)

            # Log progress
            print(Fore.YELLOW + f"Analyzing: {item_path}" + Style.RESET_ALL)

            if os.path.isfile(item_path):
                file_size = os.path.getsize(item_path)
                is_text = is_text_file(item_path)
                content = read_file_content(item_path) if is_text else "[Non-text file]"
                tokens = count_tokens(content) if is_text else 0
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
                subdir = analyze_directory(item_path, ignore_patterns, ignore_extensions, include_git, max_depth, current_depth + 1)
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

def generate_summary_string(data, use_color=False):
    """Generates a summary string of the codebase analysis."""
    if use_color:
        summary = f"\n{Fore.CYAN}Summary:{Style.RESET_ALL}\n"
        summary += f"{Fore.GREEN}Total files:{Style.RESET_ALL} {data['file_count']}\n"
        summary += f"{Fore.GREEN}Total directories:{Style.RESET_ALL} {data['dir_count']}\n"
        summary += f"{Fore.GREEN}Total size:{Style.RESET_ALL} {data['size'] / 1024:.2f} KB\n"
        summary += f"{Fore.GREEN}Total tokens:{Style.RESET_ALL} {data['total_tokens']}\n"
        summary += f"{Fore.GREEN}Text content size:{Style.RESET_ALL} {data['text_content_size'] / 1024:.2f} KB\n"
    else:
        summary = "\nSummary:\n"
        summary += f"Total files: {data['file_count']}\n"
        summary += f"Total directories: {data['dir_count']}\n"
        summary += f"Total size: {data['size'] / 1024:.2f} KB\n"
        summary += f"Total tokens: {data['total_tokens']}\n"
        summary += f"Text content size: {data['text_content_size'] / 1024:.2f} KB\n"
    return summary

def generate_content_string(data):
    """Generates a string containing the content of all text files."""
    content = "\nFile Contents:\n"

    def add_file_content(node, path=""):
        nonlocal content
        if node["type"] == "file" and not node.get("is_ignored", False) and node["content"] != "[Non-text file]":
            content += f"\n{'=' * 50}\n"
            content += f"File: {os.path.join(path, node['name'])}\n"
            content += f"{'=' * 50}\n"
            content += node["content"]
            content += "\n"
        elif node["type"] == "directory":
            for child in node["children"]:
                add_file_content(child, os.path.join(path, node["name"]))

    add_file_content(data)
    return content

def main():
    parser = argparse.ArgumentParser(description="Analyze and visualize codebase structure.")
    parser.add_argument("path", nargs="?", help="Path to the directory to analyze")
    parser.add_argument("-d", "--max-depth", type=int, help="Maximum depth for directory traversal")
    parser.add_argument("-o", "--output", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("-f", "--file", help="Output file name (default: codebase_analysis.txt or codebase_analysis.json)")
    parser.add_argument("--show-tree", action="store_true", help="Show directory tree in console output (always included in text file output)")
    parser.add_argument("--show-size", action="store_true", help="Show file sizes in directory tree")
    parser.add_argument("--show-ignored", action="store_true", help="Show ignored files and directories in tree")
    parser.add_argument("--ignore-ext", nargs="+", default=[], help="Additional file extensions to ignore")
    parser.add_argument("--no-content", action="store_true", help="Exclude file contents from the output")
    parser.add_argument("--include-git", action="store_true", help="Include .git directory in the analysis")
    parser.add_argument("--max-size", type=int, default=10240, help="Maximum allowed text content size in KB (default: 10240 KB)")
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if not args.path:
        print(Fore.RED + "Error: Path argument is required." + Style.RESET_ALL)
        parser.print_help(sys.stderr)
        sys.exit(1)

    ignore_patterns = load_gitignore(args.path)
    ignore_extensions = set(ext.lower() if ext.startswith('.') else f'.{ext.lower()}' for ext in args.ignore_ext)

    print_frame("Codebase Analyzer")
    print(Fore.CYAN + "Analyzing directory: " + Fore.WHITE + args.path + Style.RESET_ALL)

    data = analyze_directory(args.path, ignore_patterns, ignore_extensions, include_git=args.include_git, max_depth=args.max_depth)

    if data['text_content_size'] / 1024 > args.max_size:
        print(Fore.RED + f"\nWarning: The text content size ({data['text_content_size'] / 1024:.2f} KB) exceeds the maximum allowed size ({args.max_size} KB)." + Style.RESET_ALL)
        proceed = input("Do you want to proceed? (y/n): ").lower().strip()
        if proceed != 'y':
            print(Fore.YELLOW + "Analysis aborted." + Style.RESET_ALL)
            sys.exit(0)

    if args.output == "json":
        output = json.dumps(data, indent=2)
        file_name = args.file or "codebase_analysis.json"
    else:
        output = f"Codebase Analysis for: {args.path}\n"
        # Always include the tree in the .txt output
        output += "\nDirectory Structure:\n"
        output += generate_tree_string(data, show_size=args.show_size, show_ignored=args.show_ignored, use_color=False)
        output += generate_summary_string(data, use_color=False)
        if not args.no_content:
            output += generate_content_string(data)
        file_name = args.file or "codebase_analysis.txt"

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(output)
    print(Fore.GREEN + f"\nAnalysis saved to {file_name}" + Style.RESET_ALL)

    # Print colored summary to console
    print_frame("Analysis Summary")
    if args.show_tree:
        print(generate_tree_string(data, show_size=args.show_size, show_ignored=args.show_ignored, use_color=True))
    print(generate_summary_string(data, use_color=True))

if __name__ == "__main__":
    main()