import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

def plot_association_rules(rules):
    # Criar um gráfico direcionado
    G = nx.DiGraph()

    # Adicionar arestas ao gráfico com pesos baseados no lift
    for _, rule in rules.iterrows():
        antecedent = list(rule['antecedents'])[0]  # Assumindo que há apenas um antecedente
        consequent = list(rule['consequents'])[0]  # Assumindo que há apenas um consequente
        lift = rule['lift']
        G.add_edge(antecedent, consequent, weight=lift)

    # Definir a posição dos nós usando o layout da força
    pos = nx.spring_layout(G)

    # Definir o tamanho dos nós de acordo com o suporte
    node_sizes = [50000 * rules[rules['antecedents'].apply(lambda x: list(x)[0]) == node]['support'].values[0] for node in G.nodes()]

    # Mapear cores dos nós de acordo com o suporte
    node_colors = [rules[rules['antecedents'].apply(lambda x: list(x)[0]) == node]['support'].values[0] for node in G.nodes()]
    
    # Normalizar os valores de suporte para o intervalo de cores
    norm = plt.Normalize(vmin=min(node_colors), vmax=max(node_colors))
    colormap = plt.cm.Blues
    node_colors = [colormap(norm(value)) for value in node_colors]

    # Criar uma nova figura
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color=node_colors, font_size=12, font_color='black', font_weight='bold', arrows=True)

    # Adicionar rótulos de peso
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{w:.2f}" for (u, v), w in edge_labels.items()})

    # Adicionar uma legenda para o suporte
    sm = plt.cm.ScalarMappable(cmap="Blues", norm=plt.Normalize(vmin=min(rules['support']), vmax=max(rules['support'])))
    sm.set_array([])

    # Definindo os eixos da figura
    ax = plt.gca()  # Obtém o eixo atual
    cbar = plt.colorbar(sm, ax=ax)  # Adiciona a barra de cores ao eixo
    cbar.set_label('Suporte')
    
    plt.title('Regras de Associação')
    plt.axis('off')  # Desligar o eixo
    plt.show()

with open("data/padaria_trab.json", "r") as file:
    data = json.load(file)
    items = list(map(lambda x: x["produtos"], data))

    encoder = TransactionEncoder()
    transactions = encoder.fit(items).transform(items)

    original_df = pd.DataFrame(transactions, columns=encoder.columns_)
    grouped_df = pd.DataFrame()

    variations = set(column.split()[0] for column in original_df.columns)

    for variation in variations:
        grouped_df[variation] = original_df.filter(regex=rf"^{variation}", axis=1).any(axis=1)

    original_df.to_csv("data/padaria_original.csv")
    grouped_df.to_csv("data/padaria_joined.csv")

    frequent_itemsets = apriori(grouped_df, min_support=0.1, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric='confidence', min_threshold=0.0)

    rules = rules.sort_values(by='conviction', ascending=False)

    one_to_one_rules = rules[
        rules["consequents"].apply(lambda x: len(x) == 1) &
        rules["antecedents"].apply(lambda x: len(x) == 1)
    ]
    candy_rules = rules[rules['consequents'].apply(lambda x: 'Doce' in str(x))]

    rules.to_csv("data/padaria_rules.csv")

    print(rules)
    print(one_to_one_rules)
    print(candy_rules)

    plot_association_rules(rules)   
