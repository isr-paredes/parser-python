import os
import pandas as pd
from parser import Parser, lex
from runner import is_oop_code
def analyze_file(filepath):
    with open(filepath, 'r') as f:
        code = f.read()
    try:
        tokens = lex(code)
        parser = Parser(tokens) 
        parse_result = parser.parse()
        oop = is_oop_code(parse_result)

    except Exception as e:
        # If parsing fails, treat as not OOP
        oop = False
    return oop

def main():
    tester_dir = 'tests'
    results = []

    # Iterate over all .txt files in tester_dir
    for filename in os.listdir(tester_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(tester_dir, filename)
            oop_found = analyze_file(filepath)
            results.append({'filename': filename[:-4], 'is_oop': oop_found})

    # Create dataframe
    df = pd.DataFrame(results)

    # Save to CSV
    df.to_csv('parser_results.csv', index=False)
    print(df) 

if __name__ == '__main__':
    main()

    

