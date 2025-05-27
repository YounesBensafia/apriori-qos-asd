import arff
import numpy as np

def load_arff_data(file_path='Autism_Data.arff'):
    """
    Charge les données depuis un fichier ARFF et les convertit en format de transactions
    """
    attributes = []
    transactions = []
    data_section = False
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            
            # Ignorer les lignes vides et les commentaires
            if not line or line.startswith('%'):
                continue
                
            # Détecter le début de la section @DATA
            if line.upper() == '@DATA':
                data_section = True
                continue
                
            # Lire les attributs
            if not data_section and line.startswith('@ATTRIBUTE'):
                parts = line.split()
                if len(parts) >= 3:
                    attr_name = parts[1]
                    attr_type = parts[2].upper()
                    attributes.append((attr_name, attr_type))
                continue
                
            # Lire les données
            if data_section:
                values = line.split(',')
                if len(values) == len(attributes):
                    transaction = []
                    for i, (attr_name, attr_type) in enumerate(attributes):
                        value = values[i].strip()
                        if attr_type == 'NUMERIC':
                            try:
                                if float(value) == 1:
                                    transaction.append(attr_name)
                            except ValueError:
                                continue
                        else:
                            if value != '?':  # Ignorer les valeurs manquantes
                                transaction.append(f"{attr_name}_{value}")
                    
                    if transaction:  # Ne garder que les transactions non vides
                        transactions.append(transaction)
    
    return transactions

# Charger les transactions depuis le fichier ARFF
transactions = load_arff_data() 