import re

class RuleDatabase:
    def __init__(self):
        self.rules = {}
        self.load_rules()

    def parse_rule_number(self, line):
        """Parse rule numbers including special formats."""
        # Match patterns like: "1.", "2.1.", "3.14159...", etc.
        pattern = r'^(\d+(?:\.\d+)?(?:\.\d+)*)'
        match = re.match(pattern, line)
        if match:
            return match.group(1).rstrip('.')
        return None

    def get_rule_content(self, line):
        """Extract rule content after rule number."""
        # Find first occurrence of dot and space after numbers
        pattern = r'^[\d.]+\.\s*(.+)$'
        match = re.match(pattern, line)
        if match:
            return match.group(1).strip()
        return None

    def load_rules(self):
        try:
            with open('txt_files/100_rules_of_internet.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    rule_num = self.parse_rule_number(line)
                    if rule_num:
                        content = self.get_rule_content(line)
                        if content:
                            self.rules[rule_num] = content
        except Exception as e:
            print(f"Error loading rules: {e}")
            self.rules = {}

    def get_rule(self, rule_number):
        """Get rule by number, supports special rule numbers."""
        return self.rules.get(str(rule_number))

    def search_rules(self, query):
        """Search rules by content."""
        query = query.lower()
        return {num: rule for num, rule in self.rules.items() 
                if query in rule.lower()}
