import os

def convert_arff_to_csv(content):
    data_section = False
    header = []
    csv_content = []
    
    for line in content:
        line = line.strip()
        if not line or line.startswith('%'):  # Skip empty lines and comments
            continue
            
        if not data_section:
            if "@attribute" in line.lower():
                # Extract attribute name, handling quoted names
                parts = line.split(None, 2)
                attr_name = parts[1].strip("'\"")
                header.append(attr_name)
            elif "@data" in line.lower():
                data_section = True
                csv_content.append(','.join(header) + '\n')
        else:
            # Only append non-empty data lines
            if line:
                csv_content.append(line + '\n')
                
    return csv_content

def main():
    path_to_directory = "./database"
    if not os.path.exists(path_to_directory):
        print(f"Directory {path_to_directory} does not exist")
        return
        
    arff_files = [f for f in os.listdir(path_to_directory) if f.endswith('.arff')]
    
    for arff_file in arff_files:
        arff_path = os.path.join(path_to_directory, arff_file)
        csv_path = os.path.splitext(arff_path)[0] + '.csv'
        
        try:
            with open(arff_path, 'r', encoding='utf-8') as infile:
                content = infile.readlines()
            
            csv_content = convert_arff_to_csv(content)
            
            with open(csv_path, 'w', encoding='utf-8') as outfile:
                outfile.writelines(csv_content)
                
            print(f"Successfully converted {arff_file} to CSV")
                
        except Exception as e:
            print(f"Error processing {arff_file}: {str(e)}")

if __name__ == "__main__":
    main()