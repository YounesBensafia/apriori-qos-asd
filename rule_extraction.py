from database import transactions
from formule import qos_asd
from itertools import combinations
import numpy as np

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
                    qos_scores = {}
                    for alpha in [0.5, 1.0, 1.5, 2.0]:
                        for beta in [0.5, 1.0, 1.5, 2.0]:
                            score = qos_asd(p_a_and_b, p_a_and_not_b, p_not_a_and_b, alpha, beta)
                            qos_scores[f"alpha={alpha},beta={beta}"] = score
                    print(f"qos_scores: {qos_scores}")
                    
                    # Ne garder que les règles avec un score QoS minimum
                    if any(score >= min_qos for score in qos_scores.values()):
                        rules.append({
                            'antecedent': antecedent,
                            'consequent': consequent,
                            'support': p_a_and_b,
                            'qos_scores': qos_scores
                        })
    
    return rules

def print_rules(rules):
    """
    Affiche les règles extraites de manière formatée
    """
    print("\nRègles extraites :")
    print("=================")
    for i, rule in enumerate(rules, 1):
        print(f"\nRègle {i}:")
        print(f"Si {set(rule['antecedent'])} alors {set(rule['consequent'])}")
        print(f"Support: {rule['support']:.3f}")
        print("Scores QoS-ASD:")
        for params, score in rule['qos_scores'].items():
            print(f"  {params}: {score:.3f}")

if __name__ == "__main__":
    # Extraire les règles
    rules = extract_rules(transactions, min_support=0.2, min_qos=0.0)
    
    # Trier les règles par score QoS moyen
    rules.sort(key=lambda x: np.mean(list(x['qos_scores'].values())), reverse=True)
    
    # Afficher les règles
    print_rules(rules) 