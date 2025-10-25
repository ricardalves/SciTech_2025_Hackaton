import pandas as pd
import networkx as nx

# === 1. Ler ficheiros ===
param = pd.read_csv("dados_iniciais_teste9.csv")
pontos = pd.read_csv("pontos_teste9.csv")
ruas = pd.read_csv("ruas_teste9.csv")

# === 2. Criar o grafo com networkx ===
G = nx.Graph()
for _, r in ruas.iterrows():
    G.add_edge(int(r['ponto_origem']), int(r['ponto_destino']), weight=float(r['tempo_transporte']))

# === 3. Dados iniciais ===
hospital_inicial = int(param.loc[0, 'ponto_inicial'])
tempo_total_disp = float(param.loc[0, 'tempo_total'])

# === 4. Separar tipos de pontos ===
hospitais = pontos[pontos['tipo'] == 'hospital']['id'].tolist()
pacientes = pontos[pontos['tipo'] == 'paciente']

# === 5. Pré-calcular distâncias mínimas entre todos os pontos (Dijkstra) ===
# Usa Dijkstra de cada nó hospital e paciente relevante
distancias = dict(nx.all_pairs_dijkstra_path_length(G, weight='weight'))

# === 6. Procurar melhor paciente ===
melhor_paciente = None
melhor_prioridade = -1
melhor_caminho = None
melhor_tempo = None

for _, p in pacientes.iterrows():
    pid = int(p['id'])
    prioridade = float(p['prioridade'])
    cuidados = float(p['tempo_cuidados_minimos'])

    # 6.1 Ida: hospital_inicial → paciente
    if pid not in distancias.get(hospital_inicial, {}):
        continue  # sem caminho possível

    tempo_ida = distancias[hospital_inicial][pid]

    # 6.2 Regresso: paciente → hospital mais próximo
    tempo_regresso = float('inf')
    hospital_destino = None
    for h in hospitais:
        if h in distancias.get(pid, {}):
            if distancias[pid][h] < tempo_regresso:
                tempo_regresso = distancias[pid][h]
                hospital_destino = h

    if hospital_destino is None:
        continue  # paciente inacessível a qualquer hospital

    # 6.3 Tempo total
    tempo_total = tempo_ida + cuidados + tempo_regresso

    if tempo_total <= tempo_total_disp and prioridade > melhor_prioridade:
        melhor_prioridade = prioridade
        melhor_paciente = p['nome']
        melhor_tempo = tempo_total
        # reconstruir caminho completo
        caminho_ida = nx.dijkstra_path(G, hospital_inicial, pid, weight='weight')
        caminho_volta = nx.dijkstra_path(G, pid, hospital_destino, weight='weight')[1:]
        melhor_caminho = caminho_ida + caminho_volta

# === 7. Resultado final ===
if melhor_paciente:
    print(f"✅ Melhor paciente para socorrer: {melhor_paciente}")
    print(f"Prioridade: {melhor_prioridade}")
    print(f"Tempo total estimado: {melhor_tempo:.1f} minutos")
    print(f"Caminho sugerido: {melhor_caminho}")
else:
    print("❌ Nenhum paciente pode ser socorrido dentro do tempo disponível.")

