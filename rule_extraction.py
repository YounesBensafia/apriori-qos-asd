from database import transactions
from formule import qos_asd
from itertools import combinations
import numpy as np
import csv
import os

def calculate_probabilities(antecedent, consequent, transactions):
    """
    Calcule les probabilités nécessaires pour la formule QoS-ASD
    """
    total = len(transactions)
    
    # P(A and B)
    p_a_and_b = sum(1 for t in transactions 
                   if all(x in t for x in antecedent) and all(x in t for x in consequent)) / total
    
    # P(A and not B)
    p_a_and_not_b = sum(1 for t in transactions 
                       if all(x in t for x in antecedent) and not all(x in t for x in consequent)) / total
    
    # P(not A and B)
    p_not_a_and_b = sum(1 for t in transactions 
                       if not all(x in t for x in antecedent) and all(x in t for x in consequent)) / total
    
    return p_a_and_b, p_a_and_not_b, p_not_a_and_b

def extract_rules(transactions, min_support=0.1, min_qos=0.0):
    """
    Extrait les règles en utilisant la formule QoS-ASD
    """
    print("Extraction des règles...")
    # Obtenir tous les items uniques
    items = set()
    for transaction in transactions:
        items.update(transaction)
    
    # Générer toutes les paires possibles d'itemsets
    rules = []
    for i in range(1, len(items)):
        for antecedent in combinations(items, i):
            for consequent in combinations(items - set(antecedent), 1):
                # Calculer les probabilités
                p_a_and_b, p_a_and_not_b, p_not_a_and_b = calculate_probabilities(antecedent, consequent, transactions)
                print(f"Antecedent: {antecedent}, Consequent: {consequent}")
                
                # Vérifier le support minimum
                if p_a_and_b >= min_support:
                    # Calculer le score QoS-ASD pour différentes valeurs de alpha et beta
                    for alpha in [0.5, 1.0, 1.5, 2.0]:
                        for beta in [0.5, 1.0, 1.5, 2.0]:
                            score = qos_asd(p_a_and_b, p_a_and_not_b, p_not_a_and_b, alpha, beta)
                            rules.append({
                                'antecedent': ', '.join(antecedent),
                                'consequent': ', '.join(consequent),
                                'support': p_a_and_b,
                                'alpha': alpha,
                                'beta': beta,
                                'qos_score': score
                            })
    
    return rules

def save_rules_to_csv(rules, filename='qos_rules.csv'):
    """
    Save rules to CSV file
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_dir, filename)
    
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['antecedent', 'consequent', 'support', 'alpha', 'beta', 'qos_score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for rule in rules:
            writer.writerow(rule)
    
    print(f"\nRules saved to: {filepath}")

if __name__ == "__main__":
    # Extract rules
    rules = extract_rules(transactions, min_support=0.2, min_qos=0.0)
    
    # Sort rules by QoS score
    rules.sort(key=lambda x: x['qos_score'], reverse=True)
    
    # Save rules to CSV
    save_rules_to_csv(rules)