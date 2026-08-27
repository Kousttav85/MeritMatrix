
from src.algorithms import AutocompleteTrie

def test_trie_insertion_and_search():
    # 1. Arrange (Set up the data structure)
    trie = AutocompleteTrie()
    trie.insert("Engineering")
    trie.insert("Environmental")
    trie.insert("English")
    trie.insert("Data Science")
    
    # 2. Act (Run the algorithm)
    eng_results = trie.get_suggestions("Eng")
    env_results = trie.get_suggestions("Enviro")
    none_results = trie.get_suggestions("Agriculture")
    
    # 3. Assert (Verify the logic holds true)
    assert len(eng_results) == 2
    assert "engineering" in eng_results
    assert "english" in eng_results
    
    assert len(env_results) == 1
    assert env_results[0] == "environmental"
    
    assert len(none_results) == 0