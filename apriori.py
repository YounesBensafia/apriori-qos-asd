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
                    
                    # Calculate lift
                    consequent_support = self.frequent_itemsets[frozenset(consequent)]
                    lift = confidence / consequent_support
                    
                    if confidence >= self.min_confidence:
                        self.rules.append((antecedent, consequent, confidence, lift))


# Example usage
if __name__ == "__main__":
    print("Running Apriori...")
    apriori = Apriori(min_support=0.2)
    print("Apriori running...")     
    apriori.fit(transactions)
    print("Apriori completed")
    
    import csv
    with open('apriori_rules.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Antecedent', 'Consequent', 'Confidence', 'Lift'])
        for antecedent, consequent, confidence, lift in apriori.rules:
            # Convert frozenset to string and remove frozenset formatting
            ant_str = ', '.join(str(x) for x in antecedent)
            cons_str = ', '.join(str(x) for x in consequent)
            writer.writerow([ant_str, cons_str, f"{confidence:.3f}", f"{lift:.3f}"])
    
    print("Rules saved to apriori_rules.csv")