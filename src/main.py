import sys
import pandas as pd 
from pathlib import Path
from datetime import datetime, timedelta

quant_dias_p_exportar = 3 # Número de dias a serem exportados, incluindo o dia atual
dia_escolhido = datetime.now() - timedelta(days=quant_dias_p_exportar)

tipos_exportacao = ['diario']
if dia_escolhido.weekday() == 4 or dia_escolhido.weekday() == 0: 
    tipos_exportacao.append('semanal')
if (dia_escolhido + timedelta(days=1)).month != dia_escolhido.month:
    tipos_exportacao.append('mensal')

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from utils.helpers_exportacao_relatorio.helper_extracao_p_relatorio import extrair_carregamentos_generico
from utils.helpers_exportacao_relatorio.helper_prazo_p_exportar import dia_p_exportar 
from utils.helpers_exportacao_relatorio.helper_gerador_de_graficos import criar_grafico_exportacao_carregamentos 

for tipo_exportacao in tipos_exportacao:
    if tipo_exportacao == 'diario':
        print("Exportando dados diario...\n") 
    elif tipo_exportacao == 'semanal':
        print("Exportando dados semanal...\n")
    elif tipo_exportacao == 'mensal':
        print("Exportando dados mensais...\n")
    else:
        print("Tipo de exportação desconhecido.\n==============================\n")
            
    def obter_titulos_por_tipo(tipo_exportacao):
        if tipo_exportacao == 'diario':
            return 'Subtotal Dia', 'Total Semana'
        elif tipo_exportacao == 'semanal':
            return 'Subtotal Semana', 'Total Mês'
        elif tipo_exportacao == 'mensal':
            return 'Subtotal Mês', 'Subtotal ano'
        else:
            return 'Subtotal', 'Total'
            
    for dias in range(quant_dias_p_exportar + 1):
        
        inicio_periodo, fim_periodo = dia_p_exportar(tipo_exportacao=tipo_exportacao,quant_dias_p_exportar=dias) 

        nome_arquivo_xlsx = f"carregamentos_{inicio_periodo.strftime('%Y-%m-%d')}_a_{fim_periodo.strftime('%Y-%m-%d')}.xlsx"
        nome_arquivo_pdf = f"carregamentos_{inicio_periodo.strftime('%Y-%m-%d')}_a_{fim_periodo.strftime('%Y-%m-%d')}.pdf"

        CAMINHO_SAIDA_XLSX = BASE_DIR / "data" / "output" / tipo_exportacao / "out_xlsx" / nome_arquivo_xlsx
        CAMINHO_SAIDA_pdf = BASE_DIR / "data" / "output" / tipo_exportacao / "out_pdf" / nome_arquivo_pdf 
        caminho_consolidado = BASE_DIR / "data" / "consolidado_viagens.xlsx"

        titulo_subtotal, titulo_total = obter_titulos_por_tipo(tipo_exportacao)

        df_consolidado, df_periodo, inicio_periodo, fim_periodo, total_periodo,arquivo_p_exportar = extrair_carregamentos_generico(
            inicio_periodo,
            fim_periodo,
            titulo_subtotal=titulo_subtotal,
            arquivo_p_exportar=caminho_consolidado,
            titulo_total=titulo_total,
        )

        #Criação de tabela de dados do excel;
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
            
            criar_grafico_exportacao_carregamentos(
                df_consolidado, inicio_periodo, fim_periodo, total_periodo, tipo_exportacao=tipo_exportacao,caminho_exportacao=CAMINHO_SAIDA_pdf
                ) 

            df_consolidado.to_excel(CAMINHO_SAIDA_XLSX, index=False)
            print(f"\nDados do dia anterior salvos em {CAMINHO_SAIDA_XLSX}!\n===============================\n")