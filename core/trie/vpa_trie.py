class TrieNode:
    def __init__(self):
        # Dictionary to hold children nodes. Space-efficient for characters.
        self.children = {}
        # Boolean to mark the end of a valid bank suffix
        self.is_end_of_valid_suffix = False

class VPATrie:
    def __init__(self):
        self.root = TrieNode()

    def insert_valid_suffix(self, suffix: str):
        """Adds a valid bank suffix (e.g., '@okicici', '@sbi') to the Trie."""
        node = self.root
        for char in suffix:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_valid_suffix = True

    def validate_vpa(self, vpa: str) -> bool:
        """
        Validates if a UPI ID ends with a registered suffix.
        Time Complexity: O(m) where m is the length of the VPA.
        """
        # A valid VPA must have an '@'
        if "@" not in vpa:
            return False
        
        # We only care about the routing suffix for validation
        _, suffix = vpa.split("@", 1)
        suffixWithAt = "@" + suffix

        node = self.root
        for char in suffixWithAt:
            if char not in node.children:
                return False # Path broken, invalid suffix
            node = node.children[char]
        
        return node.is_end_of_valid_suffix

# --- Quick Local Test ---
if __name__ == "__main__":
    trie = VPATrie()
    
    # 1. Load the Trie with valid banking suffixes
    valid_suffixes = ["@okicici", "@sbi", "@hdfcbank", "@ybl"]
    for suffix in valid_suffixes:
        trie.insert_valid_suffix(suffix)
        
    print("Trie initialized with valid banking routes.\n")

    # 2. Simulate incoming transactions
    test_vpas = [
        "jayanth@okicici",    # Should be True
        "merchant@sbi",       # Should be True
        "scammer@fakebank",   # Should be False
        "invalid_vpa_format"  # Should be False
    ]

    for vpa in test_vpas:
        is_valid = trie.validate_vpa(vpa)
        status = "✅ ACCEPTED" if is_valid else "❌ REJECTED"
        print(f"Validating {vpa.ljust(20)} -> {status}")