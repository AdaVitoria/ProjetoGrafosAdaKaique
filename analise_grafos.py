"""
Módulo de Análise de Grafos para Trabalho de Teoria dos Grafos
"""

import os
import sys
import math
from collections import defaultdict, deque
import json

class MultigrafoOrientado:
    """
    Implementação de um multigrafo orientado usando a biblioteca padrão do Python.
    """
    def __init__(self):
        # Estrutura principal do grafo
        self.nos = set()  # Conjunto de todos os nós
        self.arestas = {}  # Dicionário para armazenar arestas não direcionadas: {(u, v): [(custo, demanda, eh_requerido, custo_servico)]}
        self.arcos = {}   # Dicionário para armazenar arcos direcionados: {(u, v): [(custo, demanda, eh_requerido, custo_servico)]}
        
        # Atributos dos nós
        self.demandas_nos = {}  # Dicionário para armazenar demandas dos nós: {no: demanda}
        self.custos_servico_nos = {}  # Dicionário para armazenar custos de serviço dos nós: {no: custo_servico}
        self.nos_requeridos = set()  # Conjunto de nós requeridos
        
        # Informações adicionais
        self.deposito = None
        self.veiculos = 0
        self.capacidade = 0
        self.valor_otimo = 0
        self.nome = ""

    def adicionar_no(self, no, demanda=0, custo_servico=0, requerido=False):
        """Adiciona um nó ao grafo com atributos opcionais."""
        self.nos.add(no)
        if requerido:
            self.nos_requeridos.add(no)
            self.demandas_nos[no] = demanda
            self.custos_servico_nos[no] = custo_servico

    def adicionar_aresta(self, u, v, custo, demanda=0, custo_servico=0, requerido=False):
        """Adiciona uma aresta não direcionada entre os nós u e v."""
        self.nos.add(u)
        self.nos.add(v)
        
        # Armazena a aresta em ambas as direções para arestas não direcionadas
        chave_aresta = tuple(sorted([u, v]))
        if chave_aresta not in self.arestas:
            self.arestas[chave_aresta] = []
        
        self.arestas[chave_aresta].append((custo, demanda, requerido, custo_servico))

    def adicionar_arco(self, u, v, custo, demanda=0, custo_servico=0, requerido=False):
        """Adiciona um arco direcionado do nó u para o nó v."""
        self.nos.add(u)
        self.nos.add(v)
        
        chave_arco = (u, v)
        if chave_arco not in self.arcos:
            self.arcos[chave_arco] = []
        
        self.arcos[chave_arco].append((custo, demanda, requerido, custo_servico))

    def obter_vizinhos(self, no):
        """Obtém todos os vizinhos de um nó (tanto de arestas quanto de arcos)."""
        vizinhos = set()
        
        # Adiciona vizinhos de arestas não direcionadas
        for aresta in self.arestas:
            if no in aresta:
                u, v = aresta
                vizinhos.add(v if u == no else u)
        
        # Adiciona vizinhos de arcos de saída
        for arco in self.arcos:
            if arco[0] == no:
                vizinhos.add(arco[1])
        
        return vizinhos

    def obter_vizinhos_saida(self, no):
        """Obtém vizinhos conectados por arcos de saída."""
        vizinhos = set()
        for arco in self.arcos:
            if arco[0] == no:
                vizinhos.add(arco[1])
        return vizinhos

    def obter_vizinhos_entrada(self, no):
        """Obtém vizinhos conectados por arcos de entrada."""
        vizinhos = set()
        for arco in self.arcos:
            if arco[1] == no:
                vizinhos.add(arco[0])
        return vizinhos

    def obter_custo_aresta(self, u, v):
        """Obtém o custo mínimo de uma aresta entre u e v."""
        chave_aresta = tuple(sorted([u, v]))
        if chave_aresta in self.arestas:
            return min(custo for custo, _, _, _ in self.arestas[chave_aresta])
        return float('inf')

    def obter_custo_arco(self, u, v):
        """Obtém o custo mínimo de um arco de u para v."""
        if (u, v) in self.arcos:
            return min(custo for custo, _, _, _ in self.arcos[(u, v)])
        return float('inf')

    def obter_custo_minimo(self, u, v):
        """Obtém o custo mínimo para ir de u para v (considerando arestas e arcos)."""
        custo_aresta = self.obter_custo_aresta(u, v)
        custo_arco = self.obter_custo_arco(u, v)
        return min(custo_aresta, custo_arco)

    def obter_grau(self, no):
        """Obtém o grau de um nó (número de arestas e arcos conectados)."""
        grau = 0
        
        # Conta arestas não direcionadas
        for aresta in self.arestas:
            if no in aresta:
                grau += len(self.arestas[aresta])
        
        # Conta arcos de saída
        for arco in self.arcos:
            if arco[0] == no:
                grau += len(self.arcos[arco])
        
        # Conta arcos de entrada
        for arco in self.arcos:
            if arco[1] == no:
                grau += len(self.arcos[arco])
        
        return grau

    def obter_grau_saida(self, no):
        """Obtém o grau de saída de um nó (número de arcos de saída)."""
        grau = 0
        for arco in self.arcos:
            if arco[0] == no:
                grau += len(self.arcos[arco])
        return grau

    def obter_grau_entrada(self, no):
        """Obtém o grau de entrada de um nó (número de arcos de entrada)."""
        grau = 0
        for arco in self.arcos:
            if arco[1] == no:
                grau += len(self.arcos[arco])
        return grau

    def calcular_caminhos_minimos(self):
        """
        Calcula os caminhos mínimos entre todos os pares de nós usando o algoritmo de Floyd-Warshall.
        Retorna a matriz de distâncias e a matriz de predecessores.
        """
        lista_nos = sorted(list(self.nos))
        n = len(lista_nos)
        no_para_indice = {no: i for i, no in enumerate(lista_nos)}
        
        # Inicializa matrizes de distância e predecessores
        dist = [[float('inf') for _ in range(n)] for _ in range(n)]
        pred = [[-1 for _ in range(n)] for _ in range(n)]
        
        # Define a diagonal como 0
        for i in range(n):
            dist[i][i] = 0
        
        # Inicializa com conexões diretas
        for u in self.nos:
            for v in self.obter_vizinhos(u):
                i, j = no_para_indice[u], no_para_indice[v]
                custo = self.obter_custo_minimo(u, v)
                if custo < dist[i][j]:
                    dist[i][j] = custo
                    pred[i][j] = i
        
        # Algoritmo de Floyd-Warshall
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        pred[i][j] = pred[k][j]
        
        return dist, pred, lista_nos

    def calcular_componentes_conectados(self):
        """Calcula o número de componentes conectados no grafo."""
        visitados = set()
        componentes = 0
        
        def dfs(no):
            visitados.add(no)
            for vizinho in self.obter_vizinhos(no):
                if vizinho not in visitados:
                    dfs(vizinho)
        
        for no in self.nos:
            if no not in visitados:
                componentes += 1
                dfs(no)
        
        return componentes

    def calcular_centralidade_intermediacao(self):
        """
        Calcula a centralidade de intermediação para todos os nós com base nos caminhos mínimos.
        """
        dist, pred, lista_nos = self.calcular_caminhos_minimos()
        n = len(lista_nos)
        no_para_indice = {no: i for i, no in enumerate(lista_nos)}
        
        # Inicializa valores de intermediação
        intermediacao = {no: 0 for no in self.nos}
        
        # Para cada par de nós
        for s in self.nos:
            for t in self.nos:
                if s == t:
                    continue
                
                # Reconstrói o caminho mínimo de s para t
                caminho = []
                atual = t
                while atual != s and atual != -1:
                    caminho.append(atual)
                    i, j = no_para_indice[s], no_para_indice[atual]
                    if pred[i][j] == -1:
                        break
                    atual = lista_nos[pred[i][j]]
                
                # Se o caminho existe e tem nós intermediários
                if atual == s and len(caminho) > 1:
                    caminho.reverse()
                    # Incrementa a intermediação para nós intermediários
                    for no in caminho[:-1]:
                        intermediacao[no] += 1
        
        return intermediacao

    def calcular_comprimento_medio_caminho(self):
        """Calcula o comprimento médio do caminho no grafo."""
        dist, _, _ = self.calcular_caminhos_minimos()
        comprimento_total = 0
        contagem = 0
        
        for i in range(len(dist)):
            for j in range(len(dist)):
                if i != j and dist[i][j] != float('inf'):
                    comprimento_total += dist[i][j]
                    contagem += 1
        
        return comprimento_total / contagem if contagem > 0 else 0

    def calcular_diametro(self):
        """Calcula o diâmetro do grafo (caminho mínimo mais longo)."""
        dist, _, _ = self.calcular_caminhos_minimos()
        diametro = 0
        
        for i in range(len(dist)):
            for j in range(len(dist)):
                if i != j and dist[i][j] != float('inf'):
                    diametro = max(diametro, dist[i][j])
        
        return diametro

    def calcular_densidade(self):
        """Calcula a densidade do grafo."""
        n = len(self.nos)
        m = sum(len(arestas) for arestas in self.arestas.values())
        a = sum(len(arcos) for arcos in self.arcos.values())
        
        # Máximo possível de arestas em um multigrafo orientado é n(n-1)
        # Máximo possível de arestas em um grafo não direcionado é n(n-1)/2
        max_conexoes = n * (n - 1) + n * (n - 1) / 2
        
        return (m + a) / max_conexoes if max_conexoes > 0 else 0

    def calcular_estatisticas(self):
        """Calcula e retorna todas as estatísticas do grafo."""
        estatisticas = {}
        
        # Contagens básicas
        estatisticas["num_nos"] = len(self.nos)
        estatisticas["num_arestas"] = sum(len(arestas) for arestas in self.arestas.values())
        estatisticas["num_arcos"] = sum(len(arcos) for arcos in self.arcos.values())
        estatisticas["num_nos_requeridos"] = len(self.nos_requeridos)
        
        # Conta arestas e arcos requeridos
        arestas_requeridas = 0
        for lista_arestas in self.arestas.values():
            for _, _, requerido, _ in lista_arestas:
                if requerido:
                    arestas_requeridas += 1
        
        arcos_requeridos = 0
        for lista_arcos in self.arcos.values():
            for _, _, requerido, _ in lista_arcos:
                if requerido:
                    arcos_requeridos += 1
        
        estatisticas["num_arestas_requeridas"] = arestas_requeridas
        estatisticas["num_arcos_requeridos"] = arcos_requeridos
        
        # Calcula densidade
        estatisticas["densidade"] = self.calcular_densidade()
        
        # Calcula componentes conectados
        estatisticas["componentes_conectados"] = self.calcular_componentes_conectados()
        
        # Calcula graus mínimo e máximo
        graus = [self.obter_grau(no) for no in self.nos]
        estatisticas["grau_minimo"] = min(graus) if graus else 0
        estatisticas["grau_maximo"] = max(graus) if graus else 0
        
        # Calcula centralidade de intermediação
        intermediacao = self.calcular_centralidade_intermediacao()
        estatisticas["centralidade_intermediacao"] = intermediacao
        
        # Calcula comprimento médio do caminho
        estatisticas["comprimento_medio_caminho"] = self.calcular_comprimento_medio_caminho()
        
        # Calcula diâmetro
        estatisticas["diametro"] = self.calcular_diametro()
        
        # Informações adicionais
        estatisticas["nome"] = self.nome
        estatisticas["deposito"] = self.deposito
        estatisticas["veiculos"] = self.veiculos
        estatisticas["capacidade"] = self.capacidade
        estatisticas["valor_otimo"] = self.valor_otimo
        
        return estatisticas

def analisar_arquivo_dat(caminho_arquivo):
    """
    Analisa um arquivo .dat e retorna um objeto MultigrafoOrientado.
    """
    grafo = MultigrafoOrientado()
    
    with open(caminho_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    
    # Analisa informações do cabeçalho
    for linha in linhas:
        linha = linha.strip()
        
        if linha.startswith("Name:"):
            grafo.nome = linha.split("\t")[1]
        elif linha.startswith("Optimal value:"):
            grafo.valor_otimo = float(linha.split("\t")[1])
        elif linha.startswith("#Vehicles:"):
            grafo.veiculos = int(linha.split("\t")[1])
        elif linha.startswith("Capacity:"):
            grafo.capacidade = int(linha.split("\t")[1])
        elif linha.startswith("Depot Node:"):
            grafo.deposito = int(linha.split("\t")[1])
        
        # Para após a seção do cabeçalho
        if linha.startswith("ReN."):
            break
    
    # Encontra seções no arquivo
    indices_secao = {}
    for i, linha in enumerate(linhas):
        if linha.startswith("ReN."):
            indices_secao["nos_requeridos"] = i
        elif linha.startswith("ReE."):
            indices_secao["arestas_requeridas"] = i
        elif linha.startswith("EDGE"):
            indices_secao["arestas_nao_requeridas"] = i
        elif linha.startswith("ReA."):
            indices_secao["arcos_requeridos"] = i
        elif linha.startswith("ARC"):
            indices_secao["arcos_nao_requeridos"] = i
    
    # Analisa nós requeridos
    i = indices_secao["nos_requeridos"] + 1
    while i < indices_secao["arestas_requeridas"]:
        linha = linhas[i].strip()
        if not linha or linha.startswith("#"):
            i += 1
            continue
        
        partes = linha.split("\t")
        if len(partes) >= 3:
            id_no = int(partes[0][1:])  # Remove o prefixo 'N' e converte para int
            demanda = int(partes[1])
            custo_servico = int(partes[2])
            grafo.adicionar_no(id_no, demanda, custo_servico, requerido=True)
        i += 1
    
    # Analisa arestas requeridas
    i = indices_secao["arestas_requeridas"] + 1
    while i < indices_secao["arestas_nao_requeridas"]:
        linha = linhas[i].strip()
        if not linha or linha.startswith("#"):
            i += 1
            continue
        
        partes = linha.split("\t")
        if len(partes) >= 6:
            id_aresta = partes[0]
            no_origem = int(partes[1])
            no_destino = int(partes[2])
            custo = int(partes[3])
            demanda = int(partes[4])
            custo_servico = int(partes[5])
            grafo.adicionar_aresta(no_origem, no_destino, custo, demanda, custo_servico, requerido=True)
        i += 1
    
    # Analisa arestas não requeridas
    i = indices_secao["arestas_nao_requeridas"] + 1
    while i < indices_secao["arcos_requeridos"]:
        linha = linhas[i].strip()
        if not linha or linha.startswith("#"):
            i += 1
            continue
        
        partes = linha.split("\t")
        if len(partes) >= 4:
            id_aresta = partes[0]
            no_origem = int(partes[1])
            no_destino = int(partes[2])
            custo = int(partes[3])
            grafo.adicionar_aresta(no_origem, no_destino, custo, requerido=False)
        i += 1
    
    # Analisa arcos requeridos
    i = indices_secao["arcos_requeridos"] + 1
    while i < indices_secao["arcos_nao_requeridos"]:
        linha = linhas[i].strip()
        if not linha or linha.startswith("#"):
            i += 1
            continue
        
        partes = linha.split("\t")
        if len(partes) >= 6:
            id_arco = partes[0]
            no_origem = int(partes[1])
            no_destino = int(partes[2])
            custo = int(partes[3])
            demanda = int(partes[4])
            custo_servico = int(partes[5])
            grafo.adicionar_arco(no_origem, no_destino, custo, demanda, custo_servico, requerido=True)
        i += 1
    
    # Analisa arcos não requeridos
    i = indices_secao["arcos_nao_requeridos"] + 1
    while i < len(linhas):
        linha = linhas[i].strip()
        if not linha or linha.startswith("#"):
            i += 1
            continue
        
        partes = linha.split("\t")
        if len(partes) >= 4:
            id_arco = partes[0]
            no_origem = int(partes[1])
            no_destino = int(partes[2])
            custo = int(partes[3])
            grafo.adicionar_arco(no_origem, no_destino, custo, requerido=False)
        i += 1
    
    # Adiciona o nó depósito se ainda não estiver no grafo
    if grafo.deposito and grafo.deposito not in grafo.nos:
        grafo.adicionar_no(grafo.deposito)
    
    return grafo

def exportar_estatisticas(grafo, arquivo_saida):
    """
    Exporta as estatísticas do grafo para um arquivo JSON.
    """
    estatisticas = grafo.calcular_estatisticas()
    
    # Converte conjuntos para listas para serialização JSON
    for chave, valor in estatisticas.items():
        if isinstance(valor, set):
            estatisticas[chave] = list(valor)
    
    with open(arquivo_saida, 'w') as arquivo:
        json.dump(estatisticas, arquivo, indent=4)
    
    return estatisticas

def exportar_caminhos_minimos(grafo, arquivo_saida):
    """
    Exporta a matriz de caminhos mínimos e a matriz de predecessores para um arquivo JSON.
    """
    dist, pred, lista_nos = grafo.calcular_caminhos_minimos()
    
    # Converte matrizes para dicionários para melhor legibilidade
    dict_dist = {}
    dict_pred = {}
    
    for i, u in enumerate(lista_nos):
        dict_dist[u] = {}
        dict_pred[u] = {}
        for j, v in enumerate(lista_nos):
            dict_dist[u][v] = dist[i][j] if dist[i][j] != float('inf') else "inf"
            dict_pred[u][v] = lista_nos[pred[i][j]] if pred[i][j] != -1 else None
    
    resultado = {
        "distancias": dict_dist,
        "predecessores": dict_pred
    }
    
    with open(arquivo_saida, 'w') as arquivo:
        json.dump(resultado, arquivo, indent=4)
    
    return resultado

def main():
    """
    Função principal para analisar um arquivo .dat, calcular estatísticas e exportar resultados.
    """
    # Verifica se o caminho do arquivo foi fornecido como argumento de linha de comando
    if len(sys.argv) > 1:
        caminho_arquivo = sys.argv[1]
    else:
        # Caminho padrão do arquivo - SUBSTITUA PELO CAMINHO DO SEU ARQUIVO .dat
        caminho_arquivo = "dados_grafo.dat"
    
    # Verifica se o arquivo existe
    if not os.path.isfile(caminho_arquivo):
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        return
    
    # Analisa o arquivo .dat
    print(f"Analisando arquivo: {caminho_arquivo}")
    grafo = analisar_arquivo_dat(caminho_arquivo)
    
    # Exporta estatísticas
    arquivo_estatisticas = "estatisticas_grafo.json"
    estatisticas = exportar_estatisticas(grafo, arquivo_estatisticas)
    print(f"Estatísticas exportadas para: {arquivo_estatisticas}")
    
    # Exporta caminhos mínimos
    arquivo_caminhos = "caminhos_minimos.json"
    caminhos = exportar_caminhos_minimos(grafo, arquivo_caminhos)
    print(f"Caminhos mínimos exportados para: {arquivo_caminhos}")
    
    # Imprime estatísticas básicas
    print("\nEstatísticas Básicas do Grafo:")
    print(f"Número de nós: {estatisticas['num_nos']}")
    print(f"Número de arestas: {estatisticas['num_arestas']}")
    print(f"Número de arcos: {estatisticas['num_arcos']}")
    print(f"Número de nós requeridos: {estatisticas['num_nos_requeridos']}")
    print(f"Número de arestas requeridas: {estatisticas['num_arestas_requeridas']}")
    print(f"Número de arcos requeridos: {estatisticas['num_arcos_requeridos']}")
    print(f"Densidade do grafo: {estatisticas['densidade']:.4f}")
    print(f"Número de componentes conectados: {estatisticas['componentes_conectados']}")
    print(f"Grau mínimo: {estatisticas['grau_minimo']}")
    print(f"Grau máximo: {estatisticas['grau_maximo']}")
    print(f"Comprimento médio do caminho: {estatisticas['comprimento_medio_caminho']:.4f}")
    print(f"Diâmetro do grafo: {estatisticas['diametro']}")

if __name__ == "__main__":
    main()