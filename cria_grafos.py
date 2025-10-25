import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Example DataFrame (replace with your real data)
df = pd.read_csv("ruas_teste9.csv")
# It should have at least two columns: 'source' and 'target'
# Optionally it may have 'weight'

# Check columns
print("Columns in df:", df.columns)

# If 'weight' column does not exist, create it with default value 1
if 'weight' not in df.columns:
    df['weight'] = 1

#É PRECISO MUDAR O NOME DAS VARIÁVEIS!!!!!!!!!! ATENÇÃO
# Now safely create the graph
G = nx.from_pandas_edgelist(df, source='ponto_origem', target='ponto_destino', edge_attr='tempo_transporte')

# Optional: show info
print("Graph created successfully!")
print(nx.info(G))

pos = nx.spring_layout(G, seed=42)  # force-directed layout

# draw nodes
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')

# draw edges
nx.draw_networkx_edges(G, pos, width=2, edge_color='gray')

# draw labels (node names)
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

# draw edge labels (tempo_transporte values)
edge_labels = nx.get_edge_attributes(G, 'tempo_transporte')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

# display the graph
plt.title("Grafo de Transporte (NetworkX)")
plt.axis('off')
plt.show()

