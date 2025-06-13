import pandas as pd
from datetime import timedelta, datetime

def extrair_carregamentos_generico(
    inicio_periodo=None,
    fim_periodo=None,
    titulo_subtotal='titulo_subtotal',
    titulo_total='titulo_total',
    arquivo_p_exportar=None,
    formato_exportacao='clientes'  
): 
    if not arquivo_p_exportar.exists():
        print(f"Erro: O arquivo {arquivo_p_exportar} não foi encontrado!")
        return None, None, None, None, None, None

    try:
        df = pd.read_excel(arquivo_p_exportar, header=0)
    except Exception as e:
        print(f"Erro ao ler o arquivo Excel: {e}")  
        return None, None, None, None, None, None
    
    df.columns = df.columns.str.strip()
    colunas_necessarias = [
        'Data', 'Clientes', 'Quant. - Cliente', 'R$ da viagem - Cliente', 'R$ pago a Transportadora','Imposto - Nf-e', 'Receita Final', 'Média R$ uni'
        ]
    
    if not all(col in df.columns for col in colunas_necessarias):
        print("Algumas colunas obrigatórias estão faltando no DataFrame.")
        return None, None, None, None, None, None
    
    df = df.rename(columns={
        'Quant. - Cliente': 'Toneladas Carregadas',
        'R$ da viagem - Cliente': 'Valor da Viagem',
        'R$ pago a Transportadora': 'Custo com Transporte',
        'Média R$ uni': 'Lucro Líquido Unitário (Média)'
    })

    df['Data'] = pd.to_datetime(df['Data'], errors='coerce', format='%Y-%m-%d').dt.date

    # Ajustar inicio_periodo e fim_periodo com base nas datas disponíveis
    if df['Data'].notna().any():
        inicio_periodo = df['Data'].min() if inicio_periodo is None else inicio_periodo
        fim_periodo = df['Data'].max() if fim_periodo is None else fim_periodo
    else:
        print("Nenhuma data válida encontrada no DataFrame.")
        return None, None, None, None, None, None

    df_periodo = df[(df['Data'] >= inicio_periodo) & (df['Data'] <= fim_periodo)].copy()
    
    if df_periodo.empty:
        print(f"Nenhum dado encontrado em {inicio_periodo}!\n ++++++++++++++++++++++++++++++++")
        return None, None, None, None, None, None

    colunas_numericas = [
        'Toneladas Carregadas', 'Valor da Viagem', 'Custo com Transporte', 'Receita Final', 'Lucro Líquido Unitário (Média)', 'Imposto - Nf-e'
        ]
    df_periodo[colunas_numericas] = df_periodo[colunas_numericas].apply(pd.to_numeric, errors='coerce')
    
    df_consolidado = df_periodo.groupby('Clientes', as_index=False).agg({
        'Toneladas Carregadas': 'sum',
        'Data': 'count',  
        'Valor da Viagem': 'sum',
        'Custo com Transporte': 'sum',
        # 'Imposto - Nf-e': 'sum',
        'Receita Final': 'sum',
        'Lucro Líquido Unitário (Média)': 'mean'
    }).fillna(0).round(2)
    
    df_consolidado.rename(columns={'Data': 'Números de viagens'}, inplace=True)

    subtotal_periodo = df_consolidado[colunas_numericas[:-1]].sum()
    subtotal_periodo['Lucro Líquido Unitário (Média)'] = df_consolidado['Lucro Líquido Unitário (Média)'].mean()
    subtotal_periodo['Clientes'] = titulo_subtotal
    subtotal_periodo['Números de viagens'] = df_consolidado['Números de viagens'].sum()
    
    df_consolidado = pd.concat([df_consolidado, pd.DataFrame([subtotal_periodo])], ignore_index=True)

    inicio_total = inicio_periodo - timedelta(days=inicio_periodo.weekday())
    inicio_periodo = inicio_periodo.date() if isinstance(inicio_periodo, datetime) else inicio_periodo
    fim_periodo = fim_periodo.date() if isinstance(fim_periodo, datetime) else fim_periodo
    df_total = df[(df['Data'] >= inicio_total) & (df['Data'] <= fim_periodo)].copy()
    df_total[colunas_numericas] = df_total[colunas_numericas].apply(pd.to_numeric, errors='coerce')

    Soma_totais_periodo = df_total[colunas_numericas[:-1]].sum()
    medias_diarias = df_total.groupby('Data').agg({'Lucro Líquido Unitário (Média)': 'mean', 'Toneladas Carregadas': 'sum'})
    Soma_totais_periodo ['Lucro Líquido Unitário (Média)'] = (medias_diarias['Lucro Líquido Unitário (Média)'] * medias_diarias['Toneladas Carregadas']).sum() / medias_diarias['Toneladas Carregadas'].sum()
    Soma_totais_periodo ['Clientes'] = titulo_total
   
    df_consolidado = pd.concat([df_consolidado, pd.DataFrame([Soma_totais_periodo ])], ignore_index=True)
    
    total_periodo = f"{Soma_totais_periodo ['Toneladas Carregadas']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    print(f"Prévia:\n", df_consolidado)
    return df_consolidado, df_periodo, inicio_periodo, fim_periodo, total_periodo, arquivo_p_exportar
