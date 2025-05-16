import re
from abc import ABC, abstractmethod


class Database(ABC):
    """Abstract base class for all database types."""
    
    def __init__(self, database_path=None):
        self.database_path = database_path
        self.is_loaded = False
    
    @abstractmethod
    def load(self):
        """Load data from the database source."""
        pass
    
    @abstractmethod
    def save(self):
        """Save data to the database source."""
        pass
    
    @abstractmethod
    def get(self, key):
        """Get a value by key."""
        pass
    
    @abstractmethod
    def search(self, query):
        """Search for entries in the database."""
        pass


class FileDatabase(Database):
    """Base class for file-based databases."""
    
    def __init__(self, file_path):
        super().__init__(file_path)
        self.data = {}
    
    def load(self):
        """Load data from file."""
        try:
            with open(self.database_path, 'r', encoding='utf-8') as f:
                self._parse_file_content(f.readlines())
            self.is_loaded = True
            return True
        except Exception as e:
            print(f"Error loading database: {e}")
            self.is_loaded = False
            return False
    
    def save(self):
        """Save data to file."""
        try:
            with open(self.database_path, 'w', encoding='utf-8') as f:
                f.write(self._format_data_for_save())
            return True
        except Exception as e:
            print(f"Error saving database: {e}")
            return False
    
    def get(self, key):
        """Get a value by key."""
        return self.data.get(str(key))
    
    def search(self, query):
        """Search for entries in the database."""
        query = query.lower()
        return {k: v for k, v in self.data.items() if query in str(v).lower()}
    
    @abstractmethod
    def _parse_file_content(self, lines):
        """Parse the content of the file."""
        pass
    
    @abstractmethod
    def _format_data_for_save(self):
        """Format the data for saving to file."""
        pass


class RuleDatabase(FileDatabase):
    """Database for internet rules."""
    
    def __init__(self, file_path='txt_files/100_rules_of_internet.txt'):
        super().__init__(file_path)
        self.load()  # Automatically load rules when initialized
    
    def _parse_file_content(self, lines):
        """Parse the rules file content."""
        self.data = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            rule_num = self._parse_rule_number(line)
            if rule_num:
                content = self._get_rule_content(line)
                if content:
                    self.data[rule_num] = content
    
    def _format_data_for_save(self):
        """Format the rules data for saving to file."""
        lines = []
        for rule_num, content in sorted(self.data.items(), key=lambda x: self._rule_sorter(x[0])):
            lines.append(f"{rule_num}. {content}")
        return "\n".join(lines)
    
    def _rule_sorter(self, rule_key):
        """Sort rules numerically, handling complex rule numbers."""
        parts = rule_key.split('.')
        return [int(p) if p.isdigit() else p for p in parts]
    
    def _parse_rule_number(self, line):
        """Parse rule numbers including special formats."""
        # Match patterns like: "1.", "2.1.", "3.14159...", etc.
        pattern = r'^(\d+(?:\.\d+)?(?:\.\d+)*)'
        match = re.match(pattern, line)
        if match:
            return match.group(1).rstrip('.')
        return None

    def _get_rule_content(self, line):
        """Extract rule content after rule number."""
        # Find first occurrence of dot and space after numbers
        pattern = r'^[\d.]+\.\s*(.+)$'
        match = re.match(pattern, line)
        if match:
            return match.group(1).strip()
        return None
    
    def get_rule(self, rule_number):
        """Get rule by number, supports special rule numbers."""
        return self.get(str(rule_number))
    
    def search_rules(self, query):
        """Search rules by content."""
        return self.search(query)
