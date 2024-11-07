from dataclasses import dataclass, field
from typing import List, Union
import tiktoken

@dataclass
class NodeAnalysis:
    name: str = ""
    is_ignored: bool = False

    @property
    def type(self) -> str:
        return NotImplemented
    
    @property
    def size(self) -> int:
        return NotImplemented

@dataclass
class TextFileAnalysis(NodeAnalysis):
    file_content: str = ""

    @property
    def type(self) -> str:
        return "text_file"
    
    @property
    def size(self) -> int:
        return len(self.file_content)
    
    def count_tokens(self):
        """Counts the number of tokens in a text string."""
        enc = tiktoken.get_encoding("cl100k_base")
        try:
            return len(enc.encode(self.file_content, disallowed_special=()))
        except Exception as e:
            print(f"Warning: Error counting tokens: {str(e)}")
            return 0

@dataclass
class DirectoryAnalysis(NodeAnalysis):
    children: List[Union["DirectoryAnalysis", TextFileAnalysis]] = field(default_factory=list)

    @property
    def type(self) -> str:
        return "directory"

    def get_file_count(self) -> int:
        count = 0
        for child in self.children:
            if child.is_ignored:
                continue

            if isinstance(child, TextFileAnalysis):
                count += 1
            if isinstance(child, DirectoryAnalysis):
                count += child.get_file_count()
        return count
    
    def get_dir_count(self) -> int:
       count = 0
       for child in self.children:
           if child.is_ignored:
               continue 
           
           if isinstance(child, DirectoryAnalysis):
               count += 1 + child.get_dir_count()
       return count


    def get_total_tokens(self) -> int:
        tokens = 0
        for child in self.children:
            if child.is_ignored:
                continue

            if isinstance(child, TextFileAnalysis):
                tokens += child.count_tokens()
            elif isinstance(child, DirectoryAnalysis):
                tokens += child.get_total_tokens()
        return tokens

    @property
    def size(self) -> int:
        size = 0
        for child in self.children:
            if isinstance(child, TextFileAnalysis):
                 size += child.size
            elif isinstance(child, DirectoryAnalysis):
                 size += child.size

        return size

    def get_non_ignored_text_content_size(self) -> int:
        size = 0
        for child in self.children:
            if child.is_ignored:
                continue    

            if isinstance(child, TextFileAnalysis) and child.file_content:
                size += len(child.file_content)
            elif isinstance(child, DirectoryAnalysis):
               size += child.size
        return size