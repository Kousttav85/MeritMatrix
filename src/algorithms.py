class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class AutocompleteTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def _dfs(self, node: TrieNode, prefix: str, results: list):
        if node.is_end:
            results.append(prefix)
        for char, next_node in node.children.items():
            self._dfs(next_node, prefix + char, results)

    def get_suggestions(self, prefix: str) -> list[str]:
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]
        
        results = []
        self._dfs(node, prefix.lower(), results)
        return results

def calculate_edit_distance(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    # Initializing a 2D DP array
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j  # Min operations is inserting all characters of s2
            elif j == 0:
                dp[i][j] = i  # Min operations is deleting all characters of s1
            elif s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i][j-1],    # Insert
                    dp[i-1][j],    # Remove
                    dp[i-1][j-1]   # Replace
                )
    return dp[m][n]

def fuzzy_match(query: str, target: str, threshold: int = 2) -> bool:
    """Returns True if any word in the target is within the edit distance threshold of the query."""
    if not query:
        return True
    
    query = query.lower()
    target_words = target.lower().split()
    
    for word in target_words:
        # Optimization: Only run DP if length difference is within threshold
        if abs(len(query) - len(word)) <= threshold:
            if calculate_edit_distance(query, word) <= threshold:
                return True
    return False

class FieldGraph:
    def __init__(self):
        # Adjacency list mapping fields to related fields
        self.adj_list = {
            "Agricultural Engineering": ["Agricultural Sciences", "Environmental Engineering", "Engineering"],
            "Agricultural Sciences": ["Agricultural Engineering", "Environmental Science & Geospatial", "Ecology & Economics"],
            "Machine Learning & AI": ["Computer Science", "Data Science", "Engineering"],
            "Computer Science": ["Machine Learning & AI", "Data Science", "Engineering"],
            "Data Science": ["Machine Learning & AI", "Computer Science", "Basic Sciences"],
            "Environmental Science & Geospatial": ["Environmental Engineering", "Agricultural Sciences", "Ecology & Economics"],
            "Environmental Engineering": ["Environmental Science & Geospatial", "Engineering", "Agricultural Engineering"],
            "Ecology & Economics": ["Environmental Science & Geospatial", "Agricultural Sciences", "Business & Management"],
            "Engineering": ["Computer Science", "Agricultural Engineering", "Environmental Engineering"],
            "Basic Sciences": ["Data Science", "Medicine", "Environmental Science & Geospatial"],
            "Medicine": ["Basic Sciences"],
            "Arts & Humanities": ["Business & Management"],
            "Business & Management": ["Arts & Humanities", "Ecology & Economics"]
        }

    def get_adjacent_fields(self, field: str) -> list[str]:
        """Returns direct neighbors of the given academic field."""
        return self.adj_list.get(field, [])