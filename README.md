# Pathfinder RPG

## Alunos
|Matrícula    | Aluno                                 |
| ----------- | ------------------------------------- |
| 23/1027121  |  José Victor Gabriel Menezes da Costa |
| 23/1011284  |  Eduardo Silva Waski                  |

## Sobre
O Pathfinder RPG é uma ferramenta de simulação de busca de caminhos em ambientes de jogos de mesa. O projeto utiliza uma <b>matriz MxN</b>  para representar um mapa com diferentes biomas (Grama, Floresta, Pântano, etc.), onde cada terreno possui um <b>custo de movimentação</b> específico.
<br><br>
O objetivo principal é demonstrar a aplicação do <b>Algoritmo de Dijkstra</b> e da <b>BFS (Busca em Largura)</b> para encontrar o menor caminho de um nó origem até um nó destino, e verificar se para ambos os casos a resposta é a mesma.

### Legenda de Terrenos (Pesos)

O projeto utiliza um sistema de pesos para representar o custo de movimento em diferentes biomas. Enquanto a **BFS** ignora pesos, o **Algoritmo de Dijkstra** utiliza os valores abaixo:

<table>
  <thead>
    <tr>
      <th>Célula</th>
      <th>Peso</th>
      <th>Observação</th>
      <th align="center">Cor</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>Asfalto</b></td>
      <td>1</td>
      <td>-</td>
      <td align="center">
        <img src="https://dummyimage.com/25x25/cccccc/000000.png" />
      </td>
    </tr>
    <tr>
      <td><b>Grama</b></td>
      <td>2</td>
      <td>-</td>
      <td align="center">
        <img src="https://dummyimage.com/25x25/93c47d/000000.png" />
      </td>
    </tr>
    <tr>
      <td><b>Floresta</b></td>
      <td>5</td>
      <td>-</td>
      <td align="center">
        <img src="https://dummyimage.com/25x25/274e13/ffffff.png" />
      </td>
    </tr>
    <tr>
      <td><b>Deserto</b></td>
      <td>8</td>
      <td>-</td>
      <td align="center">
        <img src="https://dummyimage.com/25x25/f1c232/000000.png" />
      </td>
    </tr>
    <tr>
      <td><b>Lama</b></td>
      <td>12</td>
      <td>-</td>
      <td align="center">
        <img src="https://dummyimage.com/25x25/783f04/ffffff.png" />
      </td>
    </tr>
    <tr>
      <td><b>Pântano</b></td>
      <td>20</td>
      <td>-</td>
      <td align="center">
        <img src="https://dummyimage.com/25x25/741b47/ffffff.png" />
      </td>
    </tr>
    <tr>
      <td><b>Água</b></td>
      <td>22</td>
      <td>-</td>
      <td align="center">
        <img src="https://dummyimage.com/25x25/1c4587/ffffff.png" />
      </td>
    </tr>
    <tr>
      <td><b>Montanha</b></td>
      <td>60</td>
      <td>-</td>
      <td align="center">
        <img src="https://dummyimage.com/25x25/434343/ffffff.png" />
      </td>
    </tr>
    <tr>
      <td><b>Falha na Matrix</b></td>
      <td>∞</td>
      <td><b>Intransponível.</b> Corta a conexão entre as células.</td>
      <td align="center">
        <img src="https://dummyimage.com/25x25/000000/ffffff.png" />
      </td>
    </tr>
  </tbody>
</table>
## Screenshots

### Geração de Mapa
O usuário pode gerar um mapa quadrado com o tamanho **mínimo de 10x10**, e tamanho **máximo de 200x200**. Para mapas grandes, o usuário pode usar o **Scroll** do mouse para utilizar o **Zoom** e se movimentar pelo mapa **segurando e arrastando o Botão Direito do mouse**.

![Interface da Grid 10x10](assets/map_size_10.png)
  *Grid: 10x10*


![Interface da Grid 200x200](assets/map_size_10.png)
  *Grid: 200x200*

### Dijkstra em Ação

Selecionando um ponto de **Start** e um ponto de **Final**, e clicando no botão **"Rodar Dijkstra"**, o Algoritmo de Dijkstra será executado para as posições selecionadas, e as informações referentes a **número de passos**, **custo** e **tempo de execução do algoritmo** serão exibidas no painel lateral.

![Algoritmo de Dijkstra](assets/dijkstra.png)
*Exemplo de menor caminho calculado pelo Dijkstra, desviando de terrenos custosos.*

### BFS em Ação

Selecionando um ponto de **Start** e um ponto de **Final**, e clicando no botão **"Rodar BFS"**, uma BFS será executada para as posições selecionadas, e as informações referentes a **número de passos**, **custo** e **tempo de execução do algoritmo** também serão exibidas no painel lateral.

![BFS](assets/bfs.png)
*Exemplo do caminho com menor nº de passos encontrados pelo algoritmo de BFS.*


## Instalação e Execução

### Pré-requisitos
Certifique-se de ter o [Python 3](https://www.python.org/) instalado em sua máquina.

### Instalação
1. **Clonar o repositório**:

```bash
git clone https://github.com/projeto-de-algoritmos-2026/G26_Grafos_PA-26.1.git
cd "G26_Grafos_PA-26.1"
```

2. **Criar e ativar o ambiente virtual**:

```bash
python3 -m venv .venv
source .venv/bin/activate  # No Linux/macOS
# ou
source .\.venv\Scripts\activate  # No Windows
```

3. **Instalar as dependências**:
```bash
pip install -r requirements.txt
```

### Execução

Com o ambiente virtual ativado, e dentro da pasta `/G26_Grafos_PA-26.1/` execute:
```bash
python3 -m app
```