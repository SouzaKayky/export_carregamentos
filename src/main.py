import matplotlib.pyplot as plt
import sys
from pathlib import Path
from datetime import datetime, timedelta

hoje = datetime.now()

tipos_exportacao = ['diario']
if hoje.weekday() == 4: 
    tipos_exportacao.append('semanal')
if (hoje + timedelta(days=1)).month != hoje.month:
    tipos_exportacao.append('mensal')

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from helpers.helpers_exportacao_relatorio.helper_extracao_p_relatorio import extrair_carregamentos_generico
from helpers.helpers_exportacao_relatorio.helper_prazo_p_exportar import dia_p_exportar 
from helpers.helpers_exportacao_relatorio.helper_gerador_de_graficos import criar_grafico_exportacao_carregamentos 

for tipo_exportacao in tipos_exportacao:
    if tipo_exportacao == 'diario':
        print("Exportando dados diario...")
    elif tipo_exportacao == 'semanal':
        print("Exportando dados semanal...")
    elif tipo_exportacao == 'mensal':
        print("Exportando dados mensais...")
    else:
        print("Tipo de exportação desconhecido.")
            
    def obter_titulos_por_tipo(tipo_exportacao):
        if tipo_exportacao == 'diario':
            return 'Subtotal Dia', 'Total Semana'
        elif tipo_exportacao == 'semanal':
            return 'Subtotal Semana', 'Total Mês'
        elif tipo_exportacao == 'mensal':
            return 'Subtotal Mês', 'Subtotal ano'
        else:
            return 'Subtotal', 'Total'
            
    inicio_periodo, fim_periodo = dia_p_exportar(tipo_exportacao=tipo_exportacao) 

    nome_arquivo_xlsx = f"carregamentos_{inicio_periodo.strftime('%Y-%m-%d')}_a_{fim_periodo.strftime('%Y-%m-%d')}.xlsx"
    nome_arquivo_pdf = f"carregamentos_{inicio_periodo.strftime('%Y-%m-%d')}_a_{fim_periodo.strftime('%Y-%m-%d')}.pdf"

    CAMINHO_SAIDA_XLSX = BASE_DIR / "output" / tipo_exportacao / nome_arquivo_xlsx
    CAMINHO_SAIDA_pdf = BASE_DIR / "output" / tipo_exportacao / nome_arquivo_pdf 
    caminho_consolidado = BASE_DIR / "data" / "consolidado_viagens.xlsx"

    titulo_subtotal, titulo_total = obter_titulos_por_tipo(tipo_exportacao)

    df_consolidado, df_periodo, inicio_periodo, fim_periodo, total_periodo,arquivo_p_exportar = extrair_carregamentos_generico(
        inicio_periodo,
        fim_periodo,
        titulo_subtotal=titulo_subtotal,
        titulo_total=titulo_total,
        arquivo_p_exportar=caminho_consolidado,
    )

    if df_consolidado is not None:
        df_consolidado.to_excel(CAMINHO_SAIDA_XLSX, index=False)
        print(f"Dados do dia anterior salvos em {CAMINHO_SAIDA_XLSX}!")
        
        criar_grafico_exportacao_carregamentos(
            df_consolidado, inicio_periodo, fim_periodo, total_periodo, tipo_exportacao=tipo_exportacao,caminho_exportacao=CAMINHO_SAIDA_pdf
            ) 
