import pandas as pd 
import matplotlib.pyplot as plt 

def traduzir_mes(nome_mes_ingles):
    meses = {
        'January': 'janeiro', 'February': 'fevereiro', 'March': 'março',
        'April': 'abril', 'May': 'maio', 'June': 'junho',
        'July': 'julho', 'August': 'agosto', 'September': 'setembro',
        'October': 'outubro', 'November': 'novembro', 'December': 'dezembro'
    }
    return meses.get(nome_mes_ingles, nome_mes_ingles)

def criar_grafico_exportacao_carregamentos(
    df_consolidado, inicio_periodo, fim_periodo, total_periodo, tipo_exportacao='diario',caminho_exportacao=None
    ):
    '''
    
    Cria e salva um gráfico de barras com os carregamentos por cliente. 

    Parâmetros: 
    - df_consolidado (DataFrame): dados agregados por cliente.
    - inicio periodo  (datetime): data de início do período. 
    - fim periodo (datetime): data de fim do período.
    - total_periodo (float): soma total da quantidade no período. 
    - tipo_exportacao (str): "diario", "semanal" ou "mensal".
    
    '''

    if df_consolidado.empty:
        print('Nenhum dado disponível para gerar o gráfico!') 
        return 
    
    df_consolidado = df_consolidado.sort_values(by='Toneladas Carregadas', ascending=True)
    total_info = df_consolidado['Toneladas Carregadas'].sum()
    
    plt.figure(figsize=(12,5))

    cores = ['#e38736' if cliente in ['Subtotal Dia','Total Semana','Subtotal Semana','Total Mês','Subtotal Mês','Subtotal ano'] else '#34325f'
             for cliente in df_consolidado['Clientes']]
    
    barras = plt.bar(df_consolidado['Clientes'], df_consolidado['Toneladas Carregadas'], color=cores) 

    for barra in barras: 
        plt.text(barra.get_x() + barra.get_width() / 2, barra.get_height(), round(barra.get_height(), 2), 
                 ha='center', va='bottom', fontsize=7) 

    # Título com período
    titulo_mapa = {
        'diario': f'{inicio_periodo.strftime("%d/%m/%Y")}',
        'semanal': f'{inicio_periodo.strftime("%d/%m")} a {fim_periodo.strftime("%d/%m")}',
        'mensal': f'({traduzir_mes(inicio_periodo.strftime("%B")).capitalize()} de {inicio_periodo.year})'
    } 

    periodo_formatado = titulo_mapa.get(tipo_exportacao, "")
    # titulo = f'Quantidade de carregamentos por Cliente (Período {tipo_exportacao}: {periodo_formatado})'

    plt.xlabel('Clientes', fontsize=8)  
    plt.xticks(rotation=90, fontsize=7)
    
    plt.legend(['Toneladas Carregadas']) 
    
    df_consolidado =df_consolidado.apply(pd.to_numeric, errors='coerce')
    total_periodo = pd.to_numeric(total_periodo, errors='coerce')

    if df_consolidado is not None:
        colunas_monetarias = [
            'Valor da Viagem',
            'Custo com Transporte',
            'Receita Final',
            'Lucro Líquido Unitário (Média)'
        ]
        
        for coluna in colunas_monetarias:
            if coluna in df_consolidado.columns:
                df_consolidado[coluna] = df_consolidado[coluna].apply(
                    lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if pd.notnull(x) else x
                )
        
    # proporcao_total_por_periodo = (df_consolidado / total_periodo) * 100

    if tipo_exportacao == "diario":
        titulo = f"Quantidade de carregamentos por Cliente (Período {tipo_exportacao}: {periodo_formatado})"
        texto_rodape = (
            f'Total carregamentos {tipo_exportacao}: {df_consolidado["Toneladas Carregadas"].iloc[-2]:,.2f} toneladas.\n'
            f'Total carregamentos semanal: {df_consolidado["Toneladas Carregadas"].iloc[-1]:,.2f} toneladas.'
        )
    elif tipo_exportacao == "semanal":
        titulo = f'Quantidade de carregamentos por Cliente (Período {tipo_exportacao}: {inicio_periodo.strftime("%d/%m/%Y")} até {fim_periodo.strftime("%d/%m/%Y")})'
        texto_rodape = (
            f'Total carregamentos {tipo_exportacao}: {df_consolidado["Toneladas Carregadas"].iloc[-2]:,.2f} toneladas.\n'
            f'Total carregamentos semanal: {df_consolidado["Toneladas Carregadas"].iloc[-1]:,.2f} toneladas.'
        )
    else:  
        titulo = f'Quantidade de carregamentos por Cliente (Período {tipo_exportacao}: {inicio_periodo.strftime("%d/%m/%Y")} até {fim_periodo.strftime("%d/%m/%Y")})'
        texto_rodape = (
            f'Total carregamentos {tipo_exportacao}: {df_consolidado["Toneladas Carregadas"].iloc[-2]:,.2f} toneladas.\n'
            f'Total carregamentos semanal: {df_consolidado["Toneladas Carregadas"].iloc[-1]:,.2f} toneladas.'
        )
        
    texto_rodape = texto_rodape.replace(",", "X").replace(".", ",").replace("X", ".")
    
    plt.title(titulo, fontsize=10)
    
    plt.figtext(
        0.15, 0.02, 
        texto_rodape,
        ha='left', fontsize=8, bbox={'facecolor': 'orange', 'alpha': 0.5, 'pad': 5} 
    )
        
    plt.tight_layout()

    plt.savefig(caminho_exportacao) 
    print(f'\nGráfico salvo com sucesso em {caminho_exportacao}.') 
    

