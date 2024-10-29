import plotly.graph_objects as go
import pandas as pd
import argparse

def plot_sankey(rules):
    antecedents = []
    consequents = []

    for index, row in rules.iterrows():
        antecedents.append(next(iter(row['antecedents'])))
        consequents.append(next(iter(row['consequents'])))

    labels = list(set(antecedents + consequents))
    print("Labels:", labels)

    source_indices = [labels.index(a) for a in antecedents]
    target_indices = [labels.index(c) for c in consequents]
    values = rules['confidence'].values 

    colors = '#dddddd'

    unique_consequents = list(set(consequents))
    consequent_colors = {c: f'rgba({i * 40 % 255}, {i * 80 % 255}, {i * 120 % 255}, 0.6)' for i, c in enumerate(unique_consequents)}

    link_colors = [consequent_colors[c] for c in consequents]

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=colors
        ),
        link=dict(
            source=source_indices, 
            target=target_indices,  
            value=values,          
            color=link_colors       
        )
    ))

    fig.update_layout(title_text="Diagrama de Sankey das 20 Regras de Associação com Maior Confiança", font_size=10)
    fig.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gerar gráfico')
    parser.add_argument('rules', type=str, help='Caminho para o arquivo CSV das regras')

    args = parser.parse_args()

    rules = pd.read_csv(args.rules)
    rules['antecedents'] = rules['antecedents'].apply(eval)  
    rules['consequents'] = rules['consequents'].apply(eval)  

    rules = rules.sort_values(by='confidence', ascending=False)

    rules = rules[
        (rules['antecedents'].apply(len) == 1) &
        (rules['consequents'].apply(len) == 1)
    ]

    top_rules = rules.head(20)

    print(top_rules)
    plot_sankey(top_rules)
