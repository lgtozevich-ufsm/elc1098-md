import argparse
import pandas as pd

class Table:
    def __init__(self, title = None):
        self.title = title
        self.columns = []
        self.rows = []
    
    def add_column(self, column):
        self.columns.append(column)
    
    def add_row(self, row):
        self.rows.append(row)

    def __str__(self):
        table = "\\begin{table}[htpb]\n"
        table += "\\centering\n"
        
        if self.title:
            table += f"\\caption*{{{self.title}}}\n"

        table += f"\\begin{{tabular}}{{{' '.join('c' * len(self.columns))}}}\n"

        table += "\\toprule\n"
        table += f"{' & '.join(self.columns)} \\\\\n"
        table += "\\midrule\n"

        for row in self.rows:
            table += f"{' & '.join(row)} \\\\\n"

        table += "\\bottomrule\n"

        table += "\\end{tabular}\n"
        table += "\\end{table} \\\\\n"

        return table

def format_rules(df, title):
    table = Table(title)

    table.add_column('Regra')
    table.add_column('Suporte')
    table.add_column('Confiança')
    table.add_column('Lift')

    for index, row in df.iterrows():
        table.add_row([
            f"{row['antecedents']} $\\rightarrow$ {row['consequents']}",
            f"{row['support']:.2f}",
            f"{row['confidence']:.2f}",
            f"{row['lift']:.2f}"
        ])
    
    return table

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Format association rules to LaTeX tables')
    parser.add_argument('rules', type=str, help='Path to the rules CSV file')

    args = parser.parse_args()

    rules = pd.read_csv(args.rules)
    rules = rules.sort_values(by='confidence', ascending=False)

    print(format_rules(rules, 'Regras de Associação'))