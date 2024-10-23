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
            table += f"\\caption{{{self.title}}}\n"

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
        joined_antecedents = ', '.join(row['antecedents'])
        joined_consequents = ', '.join(row['consequents'])

        table.add_row([
            f"{{{joined_antecedents}}} $\\rightarrow$ {{{joined_consequents}}}",
            f"{row['support']:.6f}",
            f"{row['confidence']:.6f}",
            f"{row['lift']:.6f}"
        ])
    
    return table

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Format association rules to LaTeX tables')
    parser.add_argument('rules', type=str, help='Path to the rules CSV file')

    args = parser.parse_args()

    rules = pd.read_csv(args.rules)
    rules['antecedents'] = rules['antecedents'].apply(eval)
    rules['consequents'] = rules['consequents'].apply(eval)

    rules = rules.sort_values(by='confidence', ascending=False)

    one_to_one_rules = rules[
        (rules['antecedents'].apply(len) == 1) &
        (rules['consequents'].apply(len) == 1)
    ]

    any_to_candy_rules = rules[
        rules['consequents'].apply(lambda x: len(x) == 1 and 'Doce' in str(x))
    ]

    print(format_rules(rules.head(5), 'Regras de Associação'))
    print(format_rules(one_to_one_rules.head(5), 'Regras de Associação de 1-1'))
    print(format_rules(any_to_candy_rules.head(5), 'Regras de Associação com Doce'))