
# Projeto: Análise e Exportação de Carregamentos

Este projeto contém funções para **extrair**, **consolidar**, **analisar** e **exportar** dados de carregamentos a partir de arquivos Excel, gerando relatórios e gráficos customizados por períodos (diário, semanal ou mensal).

---

## Sumário

- [Função: extrair_carregamentos_generico](#função-extrair_carregamentos_generico)  
- [Função: criar_grafico_exportacao_carregamentos](#função-criar_grafico_exportacao_carregamentos)  
- [Função: dia_p_exportar](#função-dia_p_exportar)  
- [Requisitos](#requisitos)  
- [Exemplo de uso](#exemplo-de-uso)  

---

## Função: `extrair_carregamentos_generico`

### Descrição

Extrai dados consolidados de carregamentos de um arquivo Excel, filtrando por um período definido, renomeando colunas, calculando subtotais e totais com títulos customizados.  
Retorna DataFrames consolidados, dados do período, período utilizado, total em formato string formatada, e o caminho do arquivo lido.

### Assinatura

```python
def extrair_carregamentos_generico(
    inicio_periodo=None,
    fim_periodo=None,
    titulo_subtotal='titulo_subtotal',
    titulo_total='titulo_total',
    arquivo_p_exportar=None,
    formato_exportacao='clientes'  
)
```

### Parâmetros

| Parâmetro            | Tipo           | Descrição                                                                                         | Padrão               |
|----------------------|----------------|-------------------------------------------------------------------------------------------------|----------------------|
| `inicio_periodo`     | `datetime.date` ou `None` | Data inicial para filtro dos dados. Se `None`, usa a menor data do arquivo.                     | `None`               |
| `fim_periodo`        | `datetime.date` ou `None` | Data final para filtro dos dados. Se `None`, usa a maior data do arquivo.                       | `None`               |
| `titulo_subtotal`    | `str`          | Texto para título do subtotal no DataFrame consolidado.                                         | `'titulo_subtotal'`   |
| `titulo_total`       | `str`          | Texto para título do total no DataFrame consolidado.                                            | `'titulo_total'`      |
| `arquivo_p_exportar` | `pathlib.Path` | Caminho do arquivo Excel contendo os dados originais para análise.                              | `None`               |
| `formato_exportacao` | `str`          | Formato desejado para exportação, atualmente não utilizado dentro da função.                    | `'clientes'`          |

### Retorno

Tuple com:

- DataFrame consolidado por cliente (incluindo subtotal e total)  
- DataFrame com dados filtrados pelo período  
- Data de início do período usado  
- Data de fim do período usado  
- String com total formatado (Toneladas Carregadas)  
- Caminho do arquivo Excel lido

---

## Função: `criar_grafico_exportacao_carregamentos`

### Descrição

Gera um gráfico de barras da quantidade de toneladas carregadas por cliente em um período definido. O gráfico destaca subtotais e totais com cores específicas e exibe o valor numérico em cada barra.

### Assinatura

```python
def criar_grafico_exportacao_carregamentos(
    df_consolidado, inicio_periodo, fim_periodo, total_periodo, tipo_exportacao='diario', caminho_exportacao=None
)
```

### Parâmetros

| Parâmetro          | Tipo             | Descrição                                                                                      | Padrão        |
|--------------------|------------------|-----------------------------------------------------------------------------------------------|---------------|
| `df_consolidado`  | `pandas.DataFrame` | DataFrame com dados consolidados por cliente, contendo coluna `'Toneladas Carregadas'`.       | Obrigatório   |
| `inicio_periodo`  | `datetime.date`   | Data inicial do período para título e legenda do gráfico.                                     | Obrigatório   |
| `fim_periodo`     | `datetime.date`   | Data final do período para título e legenda do gráfico.                                       | Obrigatório   |
| `total_periodo`   | `str`             | Texto formatado com o total de toneladas carregadas no período.                               | Obrigatório   |
| `tipo_exportacao` | `str`             | Tipo de período (`'diario'`, `'semanal'` ou `'mensal'`) para ajustar título e legenda.       | `'diario'`    |
| `caminho_exportacao`| `pathlib.Path`   | Caminho para salvar o gráfico gerado em formato PNG. Se `None`, não salva.                    | `None`        |

---

## Função: `dia_p_exportar`

### Descrição

Calcula o intervalo de datas a partir do tipo de exportação (`diario`, `semanal` ou `mensal`) e da quantidade de dias a exportar. Retorna as datas inicial e final para uso em filtros e relatórios.

### Assinatura

```python
def dia_p_exportar(tipo_exportacao, quant_dias_p_exportar):
```

### Parâmetros

| Parâmetro             | Tipo     | Descrição                                      | Exemplos               |
|-----------------------|----------|------------------------------------------------|------------------------|
| `tipo_exportacao`     | `str`    | Tipo de período: `'diario'`, `'semanal'`, `'mensal'`. | `'diario'`             |
| `quant_dias_p_exportar`| `int`    | Número de dias para o intervalo.               | `7`, `30`, `1`         |

### Retorno

Tupla (`data_inicio`, `data_fim`) com as datas calculadas para exportação.

---

## Requisitos

- Python 3.7+  
- Bibliotecas:  
  - pandas  
  - matplotlib  
  - pathlib  
  - datetime  

---

## Exemplo de Uso

```python
from pathlib import Path
from datetime import date
from seu_modulo import extrair_carregamentos_generico, criar_grafico_exportacao_carregamentos, dia_p_exportar

# Define caminho do arquivo
arquivo = Path('dados/carregamentos.xlsx')

# Define período
inicio, fim = dia_p_exportar('diario', 1)

# Extrai dados consolidados
df_consolidado, df_periodo, inicio_periodo, fim_periodo, total_periodo, arquivo_usado = extrair_carregamentos_generico(
    inicio_periodo=inicio,
    fim_periodo=fim,
    titulo_subtotal='Subtotal',
    titulo_total='Total Geral',
    arquivo_p_exportar=arquivo
)

# Cria gráfico e salva (opcional)
caminho_grafico = Path('output/grafico_carregamentos.png')
criar_grafico_exportacao_carregamentos(
    df_consolidado, inicio_periodo, fim_periodo, total_periodo, tipo_exportacao='diario', caminho_exportacao=caminho_grafico
)
```

---


