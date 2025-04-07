"""
Script para visualizar os resultados da análise de grafos sem precisar do Jupyter Notebook.
"""

import json
import os

def imprimir_cabecalho(texto):
    """Imprime um cabeçalho formatado."""
    print("\n" + "=" * 50)
    print(texto)
    print("=" * 50 + "\n")

def main():
    # Verificar se os arquivos de resultados existem
    arquivo_estatisticas = "estatisticas_grafo.json"
    arquivo_caminhos = "caminhos_minimos.json"
    
    if not os.path.exists(arquivo_estatisticas):
        print(f"Erro: Arquivo '{arquivo_estatisticas}' não encontrado.")
        print("Execute primeiro o script analise_grafos.py para gerar os resultados.")
        return
    
    # Carregar estatísticas
    with open(arquivo_estatisticas, 'r') as f:
        estatisticas = json.load(f)
    
    # Exibir informações básicas
    imprimir_cabecalho("INFORMAÇÕES BÁSICAS DO GRAFO")
    print(f"Nome do grafo: {estatisticas.get('nome', 'N/A')}")
    print(f"Valor ótimo: {estatisticas.get('valor_otimo', 'N/A')}")
    print(f"Número de veículos: {estatisticas.get('veiculos', 'N/A')}")
    print(f"Capacidade: {estatisticas.get('capacidade', 'N/A')}")
    print(f"Nó depósito: {estatisticas.get('deposito', 'N/A')}")
    
    # Exibir estatísticas principais
    imprimir_cabecalho("ESTATÍSTICAS DO GRAFO")
    print(f"Número de nós: {estatisticas.get('num_nos', 'N/A')}")
    print(f"Número de arestas: {estatisticas.get('num_arestas', 'N/A')}")
    print(f"Número de arcos: {estatisticas.get('num_arcos', 'N/A')}")
    print(f"Número de nós requeridos: {estatisticas.get('num_nos_requeridos', 'N/A')}")
    print(f"Número de arestas requeridas: {estatisticas.get('num_arestas_requeridas', 'N/A')}")
    print(f"Número de arcos requeridos: {estatisticas.get('num_arcos_requeridos', 'N/A')}")
    print(f"Densidade do grafo: {estatisticas.get('densidade', 'N/A'):.4f}")
    print(f"Número de componentes conectados: {estatisticas.get('componentes_conectados', 'N/A')}")
    print(f"Grau mínimo: {estatisticas.get('grau_minimo', 'N/A')}")
    print(f"Grau máximo: {estatisticas.get('grau_maximo', 'N/A')}")
    print(f"Comprimento médio do caminho: {estatisticas.get('comprimento_medio_caminho', 'N/A'):.4f}")
    print(f"Diâmetro do grafo: {estatisticas.get('diametro', 'N/A')}")
    
    # Exibir informações sobre centralidade de intermediação
    imprimir_cabecalho("CENTRALIDADE DE INTERMEDIAÇÃO (TOP 10)")
    intermediacao = estatisticas.get('centralidade_intermediacao', {})
    if isinstance(intermediacao, dict):
        # Converter para lista de tuplas e ordenar
        lista_intermediacao = [(no, valor) for no, valor in intermediacao.items()]
        lista_intermediacao.sort(key=lambda x: x[1], reverse=True)
        
        # Exibir top 10
        for i, (no, valor) in enumerate(lista_intermediacao[:10], 1):
            print(f"{i}. Nó {no}: {valor}")
    
    # Verificar se o arquivo de caminhos mínimos existe
    if os.path.exists(arquivo_caminhos):
        with open(arquivo_caminhos, 'r') as f:
            caminhos = json.load(f)
        
        # Exibir amostra da matriz de distâncias
        imprimir_cabecalho("AMOSTRA DA MATRIZ DE DISTÂNCIAS")
        distancias = caminhos.get('distancias', {})
        nos = list(distancias.keys())[:5]  # Primeiros 5 nós
        
        # Imprimir cabeçalho
        print(f"{'De/Para':<8}", end="")
        for no in nos:
            print(f"{no:<8}", end="")
        print()
        
        # Imprimir linhas
        for origem in nos:
            print(f"{origem:<8}", end="")
            for destino in nos:
                valor = distancias.get(origem, {}).get(destino, "inf")
                print(f"{valor:<8}", end="")
            print()

if __name__ == "__main__":
    main()