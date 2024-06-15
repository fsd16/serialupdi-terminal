from dataclasses import dataclass
from json import dumps
from pathlib import Path
import re
import sys

@dataclass
class Section:
    name: str
    address: int
    size: int

class LinkerMapParser:
    def __init__(self, content: str):
        self.content = content
        self.parse()

    @classmethod
    def from_file(cls, map_file_path):
        with open(map_file_path, 'r') as file:
            content = file.read()
        return cls(content)
                    
    def parse(self):
        linker_blocks = self._pre_parse(self.content)
        
        self.archive_members = self._parse_archive_members(linker_blocks["Archive member included to satisfy reference by file (symbol)"])
        self.discarded_sections = self._parse_sections(linker_blocks["Discarded input sections"])
        self.memory_config = self._parse_memory_config(linker_blocks["Memory Configuration"])
        self.memory_sections = self._parse_sections(linker_blocks["Linker script and memory map"])
    
    @staticmethod
    def _pre_parse(content):
        headers = ["Archive member included to satisfy reference by file (symbol)",
                    "Discarded input sections",
                    "Memory Configuration",
                    "Linker script and memory map"]
        
        # Create a regex pattern to match the headers
        pattern = re.compile("|".join([f"({re.escape(header)})" for header in headers]))

        # Split the content based on the headers
        sections = pattern.split(content)

        # Initialize a dictionary to hold the sections
        sections_dict = {}

        # Iterate through the split content to fill the dictionary
        current_header = None
        for section in sections:
            if section is None:
                continue
            if section.strip() in headers:
                current_header = section.strip()
                sections_dict[current_header] = ""
            elif current_header:
                sections_dict[current_header] += section.strip()
        
        return sections_dict
    
    @staticmethod
    def _parse_archive_members(content):
        archive_members = []

        lines = content.strip().splitlines()

        for line in lines:
            if line.strip():  # Skip empty lines
                # Split by the first occurrence of '(' to separate the archive member path and the symbol
                split_index = line.find('(')
                if split_index != -1:
                    archive_member = line[:split_index].strip()
                    symbol = line[split_index+1:].strip(' )')
                    archive_members.append({
                        'Archive Member': archive_member,
                        'Symbol': symbol
                    })

        return archive_members
        
    @staticmethod
    def _parse_memory_config(content):
        memory_config = []
        pattern = re.compile(r'(\S+)\s+([0-9a-fx]+)\s+([0-9a-fx]+)\s+(\S+)')

        # Split the input into lines and skip the first two lines (header and separator)
        lines = content.strip().splitlines()[2:]

        for line in lines:
            match = pattern.match(line)
            if match:
                name = match.group(1)
                origin = int(match.group(2), 16)  # Convert hex string to integer
                length = int(match.group(3), 16)  # Convert hex string to integer
                attributes = match.group(4)
                memory_config.append({
                    'Name': name,
                    'Origin': origin,
                    'Length': length,
                    'Attributes': attributes
                })

        return memory_config

    @staticmethod
    def _parse_sections(content):
        sections: dict[str, Section] = {}
        section_pattern = re.compile(r'(\.\w+)\s+0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)')
        for match in section_pattern.finditer(content):
            section_name = match.group(1).lstrip('.')
            section_address = int(match.group(2), 16)
            section_size = int(match.group(3), 16)
            sections[section_name] = Section(section_name, section_address, section_size)
        return sections

if __name__ == "__main__":
    project_path = Path(r"C:\Users\Finn\OneDrive\Shared Documents\Projects\CupWarmer\CupWarmer\firmware\CupWarmer.X")
    
    memory_maps = project_path.glob("*.map")
    
    for memory_map in memory_maps:
        parser = LinkerMapParser.from_file(memory_map)
        parser.parse()
        
        # for k, v in parser.memory_sections.items():
        v = parser.memory_sections['pb_pressed_state']
        print(f"Address={hex(v.address):<15} Size={v.size}")
