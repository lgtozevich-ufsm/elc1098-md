import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

with open("data/padaria_trab.json", "r") as file:
    data = json.load(file)
    items = list(map(lambda x: x["produtos"], data))

    encoder = TransactionEncoder()
    transactions = encoder.fit(items).transform(items)

    df = pd.DataFrame(transactions, columns=encoder.columns_)
 
    frequent_itemsets = apriori(df, min_support=0.01, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric='confidence', min_threshold=0.0)
    rules = rules.sort_values(by='confidence', ascending=False)    

    candy_rules = rules[rules['consequents'].apply(lambda x: 'Doce' in str(x))]

    rules.to_csv("data/padaria_rules.csv")
    print(rules.head(5))
    print(rules.head(5))
    









    
