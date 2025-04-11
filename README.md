# [Análise de Grafos - Trabalho Prático](https://github.com/seu-usuario/analise-grafos)

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.6%2B-blue" alt="Python 3.6+">
  <img src="https://img.shields.io/badge/Licença-Educacional-green" alt="Licença Educacional">
</div>

## 📑 Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Requisitos](#requisitos)
- [Instalação e Uso](#instalação-e-uso)
- [Formato do Arquivo de Entrada](#formato-do-arquivo-de-entrada)
- [Algoritmos Implementados](#algoritmos-implementados)
- [Exemplos de Saída](#exemplos-de-saída)
- [Contribuição](#contribuição)
- [Licença](#licença)

## 🔍 Sobre o Projeto

Este projeto implementa a Etapa 1 do Trabalho Prático Final da disciplina **GCC262 - Grafos** da Universidade Federal de Lavras (UFLA), conforme orientação do professor **Mayron César O. Moreira**.

A proposta é desenvolver uma ferramenta de análise de grafos capaz de:

- Ler e processar arquivos de entrada com dados específicos;
- Modelar o grafo como um **multigrafo orientado**;
- Calcular estatísticas estruturais e métricas avançadas;
- Gerar matrizes de caminhos mínimos;
- Utilizar apenas a biblioteca padrão do Python.

## ✨ Funcionalidades

### 🧱 Modelagem do Grafo

- ✅ Implementação de um multigrafo orientado usando dicionários e conjuntos.
- ✅ Suporte a vértices, arestas e arcos com atributos (demanda, custo, etc.).

### 📊 Estatísticas Calculadas

- **Informações básicas**:
  - Número de vértices, arestas e arcos.
  - Quantidade de elementos requeridos.
- **Propriedades estruturais**:
  - Densidade.
  - Número de componentes conectados.
  - Grau mínimo e máximo dos vértices.
- **Métricas avançadas**:
  - Intermediação (betweenness centrality).
  - Caminho médio.
  - Diâmetro do grafo.

### 📉 Caminhos Mínimos

- ✅ Algoritmo de **Floyd-Warshall**.
- ✅ Geração das matrizes de distâncias e predecessores.

### 📈 Visualização e Análise

- ✅ Exportação das estatísticas em JSON.
- ✅ Visualização interativa via Jupyter Notebook.
- ✅ Gráficos de distribuição das propriedades do grafo.

## 📁 Estrutura do Projeto

```
analise_grafos/
├── graph_analysis.py        # Script principal de análise
├── graph_analysis.ipynb     # Notebook Jupyter para visualização
├── graph_data.dat           # Arquivo de dados de exemplo
├── .gitignore               # Arquivos ignorados pelo Git
└── README.md                # Este arquivo
```

## 🧰 Requisitos

- Python 3.6 ou superior
- Jupyter Notebook (opcional, para visualização)
- Bibliotecas padrão:
  - `collections`
  - `json`
  - `math`
  - `os`
  - `sys`

> ⚠️ O projeto **não utiliza bibliotecas externas** como `networkx`, `igraph`, `numpy` ou `pandas`.

## 🚀 Instalação e Uso

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/analise-grafos.git
cd analise-grafos
```

### 2. Adicione o Arquivo `.dat`

Coloque o seu arquivo de entrada `.dat` no diretório do projeto ou utilize o exemplo fornecido.

### 3. Execute o Script

```bash
python graph_analysis.py [caminho_para_arquivo_dat]
```

Caso o caminho não seja especificado, o script procurará por `graph_data.dat` no diretório atual.

### 4. Visualização (Opcional)

```bash
jupyter notebook graph_analysis.ipynb
```

### 5. Arquivos de Saída

- `graph_statistics.json`: Estatísticas estruturais e métricas calculadas.
- `shortest_paths.json`: Matrizes de distâncias e predecessores.

## 🗂️ Formato do Arquivo de Entrada

O arquivo `.dat` deve seguir a estrutura:

1. **Cabeçalho**: Informações gerais.
2. **Vértices Requeridos**
3. **Arestas Requeridas e Não-Requeridas**
4. **Arcos Requeridos e Não-Requeridos**

#### Exemplo de Cabeçalho:

```
Name:		mgval_0.50_10D
Optimal value:	-1
#Vehicles:	10
Capacity:	75
Depot Node:	1
#Nodes:		50
#Edges:		42
#Arcs:		87
#Required N:	46
#Required E:	21
#Required A:	43

ReN.	DEMAND	S. COST
N2	20	20
N3	9	9
...
```

## 🧮 Algoritmos Implementados

### 📐 Modelagem e Estrutura

- Representação do grafo com dicionários e conjuntos.
- Operações básicas de inserção e consulta.

### 📊 Estatísticas

- Cálculo de densidade.
- Componentes conectados (DFS).
- Grau mínimo, máximo, de entrada e saída.

### 🔄 Caminhos Mínimos

- Algoritmo de **Floyd-Warshall**.
- Matrizes de distância e predecessores para reconstrução de caminhos.

### 🔁 Centralidade de Intermediação

- Baseada nos caminhos mínimos calculados.

## 📌 Exemplos de Saída

### Estatísticas Geradas

```
Número de vértices: 50
Número de arestas: 42
Número de arcos: 87
Vértices requeridos: 46
Arestas requeridas: 21
Arcos requeridos: 43
Densidade: 0.0526
Componentes conectados: 1
Grau mínimo: 1
Grau máximo: 12
Caminho médio: 3.2456
Diâmetro: 8
```

### Visualizações (via Notebook)

- Distribuição de graus dos vértices
- Centralidade de intermediação
- Heatmap da matriz de distâncias

## 🤝 Contribuição

Este projeto foi desenvolvido para fins educacionais como parte de um trabalho acadêmico. Contribuições são bem-vindas!

## 📝 Licença

Distribuído sob licença educacional, para uso não comercial e acadêmico.

---

Desenvolvido por [Ada Vitória](https://github.com/AdaVitoria) e [Kaique Salvador](https://github.com/kaique-salvador) — 2025
