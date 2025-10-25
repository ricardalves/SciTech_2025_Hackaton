import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# ===============================
# 1️⃣ Ler ficheiros
# ===============================
ruas = pd.read_csv("ruas_teste9.csv")
pontos = pd.read_csv("pontos_teste9.csv")

# ===============================
# 2️⃣ Criar o grafo
# ===============================
G = nx.from_pandas_edgelist(
    ruas,
    source="ponto_origem",
    target="ponto_destino",
    edge_attr="tempo_transporte",
    create_using=nx.Graph()
)

# ===============================
# 3️⃣ Identificar tipos de nós
# ===============================
tipo_por_id = pontos.set_index("id")["tipo"].to_dict()
hospitais = [n for n, t in tipo_por_id.items() if t == "hospital" and n in G.nodes]
pacientes = [n for n, t in tipo_por_id.items() if t == "paciente" and n in G.nodes]

print(f"Hospitais ({len(hospitais)}): {hospitais}")
print(f"Pacientes ({len(pacientes)}): {pacientes}")

# ===============================
# 4️⃣ Desenhar grafo
# ===============================
pos = nx.spring_layout(G, seed=42)

# Nós
nx.draw_networkx_nodes(G, pos, nodelist=hospitais, node_color="red", node_size=900)
nx.draw_networkx_nodes(G, pos, nodelist=pacientes, node_color="green", node_size=700)

# Arestas
nx.draw_networkx_edges(G, pos, width=2, edge_color="lightgray")

# Etiquetas dos nós (usar IDs)
nx.draw_networkx_labels(G, pos, labels={n: str(n) for n in G.nodes()}, font_color="white", font_weight="bold", font_size=9)

# Etiquetas das arestas
edge_labels = nx.get_edge_attributes(G, "tempo_transporte")
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="black", font_size=7)

# ===============================
# 5️⃣ Legenda manual (lado direito)
# ===============================
legenda = [
    Line2D([0], [0], marker='o', color='w', label='Hospitais',
           markerfacecolor='red', markersize=12),
    Line2D([0], [0], marker='o', color='w', label='Pacientes',
           markerfacecolor='green', markersize=12)
]
plt.legend(handles=legenda, loc='upper left',
           bbox_to_anchor=(1.02, 1), frameon=False)

# ===============================
# 6️⃣ Mostrar com título a negrito
# ===============================
plt.title("Grafo de Transporte: Hospitais (vermelho) vs Pacientes (verde)",
          fontweight='bold', fontsize=12)
plt.axis("off")
plt.tight_layout()
plt.show()
