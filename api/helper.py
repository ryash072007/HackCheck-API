def name_similarity(name1, name2, threshold=0.8):
    """
    Compare two names and determine if they are similar.
    
    Args:
        name1 (str): First name to compare
        name2 (str): Second name to compare
        threshold (float): Similarity threshold (default: 0.8 or 80%)
        
    Returns:
        bool: True if similarity is greater than the threshold, False otherwise

    Created by Yash Raj at 10:47PM on 11/03/2025
    """
    # Preprocess names - convert to lowercase and strip whitespace
    name1 = name1.lower().strip()
    name2 = name2.lower().strip()
    
    # If names are exactly the same, return True immediately
    if name1 == name2:
        return True
        
    # Calculate Levenshtein distance
    def levenshtein_distance(s1, s2):
        if len(s1) < len(s2):
            return levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    # Calculate similarity ratio
    distance = levenshtein_distance(name1, name2)
    max_len = max(len(name1), len(name2))
    
    if max_len == 0:  # Both strings are empty
        return True
        
    similarity = 1 - (distance / max_len)
    
    return similarity >= threshold