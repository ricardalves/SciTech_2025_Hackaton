import pandas as pd
import networkx as nx

# Ler ficheiros
param = pd.read_csv("dados_iniciais_teste8.csv")
pontos = pd.read_csv("pontos_teste8.csv")
ruas = pd.read_csv("ruas_teste8.csv")

# Criar o grafo
G = nx.Graph()
for _, r in ruas.iterrows():
    G.add_edge(int(r['ponto_origem']), int(r['ponto_destino']), weight=float(r['tempo_transporte']))

hospital_inicial = int(param.loc[0, 'ponto_inicial'])
tempo_total_disp = float(param.loc[0, 'tempo_total'])

hospitais = pontos[pontos['tipo'] == 'hospital']['id'].tolist()
pacientes = pontos[pontos['tipo'] == 'paciente']

distancias = {}
caminhos = {}
for origem in hospitais + pacientes['id'].tolist():
    distancias[origem], caminhos[origem] = nx.single_source_dijkstra(G, origem, weight='weight')

# Ordenar pacientes por prioridade decrescente
pacientes = pacientes.sort_values(by='prioridade', ascending=False)

tempo_restante = tempo_total_disp
hospital_atual = hospital_inicial
pacientes_atendidos = []

for _, p in pacientes.iterrows():
    pid = int(p['id'])
    prioridade = float(p['prioridade'])
    cuidados = float(p['tempo_cuidados_minimos'])

    tempo_ida = distancias.get(hospital_atual, {}).get(pid)
    if tempo_ida is None:
        continue

    # Encontrar hospital de regresso
    melhor = min(
        ((h, distancias[pid][h]) for h in hospitais if h in distancias[pid]),
        default=(None, float('inf')),
        key=lambda x: x[1]
    )
    hospital_destino, tempo_regresso = melhor
    if hospital_destino is None:
        continue

    tempo_total = tempo_ida + cuidados + tempo_regresso
    if tempo_total <= tempo_restante:
        caminho_ida = caminhos[hospital_atual][pid]
        caminho_volta = caminhos[pid][hospital_destino][1:]
        caminho_completo = caminho_ida + caminho_volta

        pacientes_atendidos.append({
            "nome": p['nome'],
            "prioridade": prioridade,
            "tempo_usado": tempo_total,
            "hospital_chegada": hospital_destino,
            "caminho": caminho_completo
        })

        tempo_restante -= tempo_total
        hospital_atual = hospital_destino



if pacientes_atendidos:
    print("Pacientes atendidos dentro do tempo total:\n")
    for i, p in enumerate(pacientes_atendidos, 1):
        print(f"{i}. {p['nome']} | Prioridade {p['prioridade']} | Tempo usado: {p['tempo_usado']:.1f} min")
        print(f"   ➜ Hospital de chegada: {p['hospital_chegada']}")
        print(f"   ➜ Caminho percorrido: {p['caminho']}\n")
    print(f"Tempo total gasto: {tempo_total_disp - tempo_restante:.1f} min")
    print(f"Tempo restante: {tempo_restante:.1f} min")
    print(f"Total de pacientes socorridos: {len(pacientes_atendidos)}")
else:
    print("Nenhum paciente pôde ser socorrido dentro do tempo total disponível.")