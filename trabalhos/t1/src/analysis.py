import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

def format_df(data):
    items = list(map(lambda x: x['produtos'], data))

    encoder = TransactionEncoder()
    transactions = encoder.fit(items).transform(items)

    return pd.DataFrame(transactions, columns=encoder.columns_)

def create_grouped_df(df, prefixes):
    grouped_df = df.copy()

    for prefix in prefixes:
        matches = df.filter(regex=rf'^{prefix}', axis=1)
        grouped_df[prefix] = matches.any(axis=1)

        for column in matches.columns:
            del grouped_df[column]
    

    return grouped_df

def create_rules(df, min_support=0.2, metric='confidence', min_threshold=0.0):
    frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_threshold)

    return rules.sort_values(by=metric, ascending=False)

with open('data/padaria_trab.json', 'r') as file:
    raw_data = json.load(file)

    df = format_df(raw_data)

    variations = set(column.split()[0] for column in df.columns)

    ungrouped_rules = create_rules(df, min_support=5 / len(df.index))
    grouped_variation_rules = create_rules(create_grouped_df(df, variations), min_support=5 / len(df.index))
    grouped_only_candy_rules = create_rules(create_grouped_df(df, ['Doce']), min_support=5 / len(df.index))

    
    df.to_csv('results/df.csv')
    ungrouped_rules.to_csv('results/ungrouped_rules.csv')
    grouped_variation_rules.to_csv('results/grouped_variation_rules.csv')
    grouped_only_candy_rules.to_csv('results/grouped_only_candy_rules.csv')
