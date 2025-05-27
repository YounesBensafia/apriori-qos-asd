import numpy as np
from itertools import combinations
from formule import qos_asd
from database import transactions

class Apriori:
    def __init__(self, min_support=0.1, min_confidence=0.5):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.transactions = []
        self.items = set()
        self.frequent_itemsets = {}
        self.rules = []

    def fit(self, transactions):
        self.transactions = transactions
        self.items = set(item for transaction in transactions for item in transaction)
        self._generate_frequent_itemsets()
        self._generate_rules()

    def _get_support(self, itemset):
        count = sum(1 for transaction in self.transactions 
                   if all(item in transaction for item in itemset))
        return count / len(self.transactions)

    def _generate_frequent_itemsets(self):
        k = 1
        current_candidates = [{item} for item in self.items]
        
        while current_candidates:
            # Calculate support for current candidates
            current_frequent = {}
            for itemset in current_candidates:
                support = self._get_support(itemset)
                if support >= self.min_support:
                    current_frequent[frozenset(itemset)] = support
            
            if not current_frequent:
                break
                
            self.frequent_itemsets.update(current_frequent)
            
            # Generate next level candidates
            k += 1
            current_candidates = self._generate_candidates(current_frequent.keys(), k)

    def _generate_candidates(self, prev_frequent, k):
        candidates = set()
        for item1 in prev_frequent:
            for item2 in prev_frequent:
                union = item1.union(item2)
                if len(union) == k:
                    candidates.add(union)
        return candidates

    def _generate_rules(self):
        for itemset in self.frequent_itemsets:
            if len(itemset) < 2:
                continue
                
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset - antecedent
                    
                    confidence = self.frequent_itemsets[itemset] / self.frequent_itemsets[antecedent]
                    
                    if confidence >= self.min_confidence:
                        self.rules.append((antecedent, consequent, confidence))

# def compare_rules(apriori_rules, transactions):
#     results = []
    
#     for antecedent, consequent, confidence in apriori_rules:
#         # Calculate P(A and B)
#         p_a_and_b = sum(1 for t in transactions 
#                        if all(x in t for x in antecedent) and all(x in t for x in consequent)) / len(transactions)
        
#         # Calculate P(A and not B)
#         p_a_and_not_b = sum(1 for t in transactions 
#                            if all(x in t for x in antecedent) and not all(x in t for x in consequent)) / len(transactions)
        
#         # Calculate P(not A and B)
#         p_not_a_and_b = sum(1 for t in transactions 
#                            if not all(x in t for x in antecedent) and all(x in t for x in consequent)) / len(transactions)
        
#         # Calculate QoS-ASD score
#         qos_score = qos_asd(p_a_and_b, p_a_and_not_b, p_not_a_and_b)
        
#         results.append({
#             'antecedent': antecedent,
#             'consequent': consequent,
#             'confidence': confidence,
#             'qos_score': qos_score
#         })
    
    # return results

def extract_best_rules(results, alpha=1.5, beta=1.0, top_n=10):
    """
    Extract the best rules based on QoS-ASD score
    
    Args:
        results: List of dictionaries containing rule information
        alpha: Alpha parameter for QoS-ASD formula (default 1.5)
        beta: Beta parameter for QoS-ASD formula (default 1.0) 
        top_n: Number of top rules to return (default 10)
        
    Returns:
        List of top N rules sorted by QoS-ASD score
    """
    # Sort rules by QoS score in descending order
    sorted_rules = sorted(results, key=lambda x: x['qos_score'], reverse=True)
    
    # Take top N rules
    top_rules = sorted_rules[:top_n]
    
    return top_rules

def print_best_rules(top_rules):
    """
    Print the best rules in a formatted way
    
    Args:
        top_rules: List of rules to print
    """
    print("\nTop Rules by QoS-ASD Score:")
    print("============================")
    for i, rule in enumerate(top_rules, 1):
        print(f"\nRule {i}:")
        print(f"Antecedent: {set(rule['antecedent'])}")
        print(f"Consequent: {set(rule['consequent'])}")
        print(f"Confidence: {rule['confidence']:.3f}")
        print(f"QoS-ASD Score: {rule['qos_score']:.3f}")

# Example usage
if __name__ == "__main__":
    # Initialize and run Apriori
    print("Running Apriori...")
    apriori = Apriori(min_support=0.2, min_confidence=0.5)
    apriori.fit(transactions)
    print("Apriori completed")
    
    # Compare rules
    print("\nApriori Rules:")
    print("==================")
    for antecedent, consequent, confidence in apriori.rules:
        print(f"\nRule: {set(antecedent)} -> {set(consequent)}")
        print(f"Confidence: {confidence:.3f}")