import pandas as pd
import networkx as nx

# === 1. Ler ficheiros ===
param = pd.read_csv("dados_iniciais_teste9.csv")
pontos = pd.read_csv("pontos_teste9.csv")
ruas = pd.read_csv("ruas_teste9.csv")

# === 2. Criar o grafo ===
G = nx.Graph()
for _, r in ruas.iterrows():
    G.add_edge(int(r['ponto_origem']), int(r['ponto_destino']), weight=float(r['tempo_transporte']))

# === 3. Dados iniciais ===
hospital_inicial = int(param.loc[0, 'ponto_inicial'])
tempo_total_disp = float(param.loc[0, 'tempo_total'])

# === 4. Listas úteis ===
hospitais = pontos[pontos['tipo'] == 'hospital']['id'].tolist()
pacientes = pontos[pontos['tipo'] == 'paciente'].copy()

# === 5. Pré-calcular distâncias (Dijkstra) ===
distancias = dict(nx.all_pairs_dijkstra_path_length(G, weight='weight'))

# === 6. Ordenar pacientes por prioridade decrescente ===
pacientes = pacientes.sort_values(by='prioridade', ascending=False)

# === 7. Variáveis de controlo ===
tempo_restante = tempo_total_disp
hospital_atual = hospital_inicial
pacientes_atendidos = []

# === 8. Ciclo principal ===
for _, p in pacientes.iterrows():
    pid = int(p['id'])
    prioridade = float(p['prioridade'])
    cuidados = float(p['tempo_cuidados_minimos'])

    # Verifica caminho até paciente
    if pid not in distancias.get(hospital_atual, {}):
        continue

    tempo_ida = distancias[hospital_atual][pid]

    # Encontrar hospital mais próximo para entrega
    tempo_regresso = float('inf')
    hospital_destino = None
    for h in hospitais:
        if h in distancias.get(pid, {}):
            if distancias[pid][h] < tempo_regresso:
                tempo_regresso = distancias[pid][h]
                hospital_destino = h

    if hospital_destino is None:
        continue  # não há hospital acessível

    tempo_total = tempo_ida + cuidados + tempo_regresso

    # Se couber no tempo restante, socorre o paciente
    if tempo_total <= tempo_restante:
        # Caminhos completos (usando Dijkstra)
        caminho_ida = nx.dijkstra_path(G, hospital_atual, pid, weight='weight')
        caminho_volta = nx.dijkstra_path(G, pid, hospital_destino, weight='weight')[1:]  # remove duplicação do paciente
        caminho_completo = caminho_ida + caminho_volta

        pacientes_atendidos.append({
            "nome": p['nome'],
            "prioridade": prioridade,
            "tempo_usado": tempo_total,
            "hospital_chegada": hospital_destino,
            "caminho": caminho_completo
        })

        tempo_restante -= tempo_total
        hospital_atual = hospital_destino  # próxima viagem começa neste hospital

# === 9. Resultados ===
if pacientes_atendidos:
    print("✅ Pacientes atendidos dentro do tempo total:\n")
    for i, p in enumerate(pacientes_atendidos, 1):
        print(f"{i}. {p['nome']} | Prioridade {p['prioridade']} | Tempo usado: {p['tempo_usado']:.1f} min")
        print(f"   ➜ Hospital de chegada: {p['hospital_chegada']}")
        print(f"   ➜ Caminho percorrido: {p['caminho']}\n")
    print(f"Tempo total gasto: {tempo_total_disp - tempo_restante:.1f} min")
    print(f"Tempo restante: {tempo_restante:.1f} min")
    print(f"Total de pacientes socorridos: {len(pacientes_atendidos)}")
    sum=0
    for paciente in pacientes_atendidos:
        sum+=paciente["prioridade"]
    
    
    print(f"Soma das prioridades: {sum}")
else:
    print("❌ Nenhum paciente pôde ser socorrido dentro do tempo total disponível.")
