from datetime import datetime, timedelta
    
def dia_p_exportar(tipo_exportacao, quant_dias_p_exportar):
    hoje = datetime.today().date()
                    
    if tipo_exportacao == 'diario':
        inicio_periodo = hoje - timedelta(days=quant_dias_p_exportar)
        return inicio_periodo, inicio_periodo

    elif tipo_exportacao == 'semanal':
        inicio_periodo = hoje - timedelta(days=hoje.weekday()) 
        fim_periodo = inicio_periodo + timedelta(days=4)
        return inicio_periodo, fim_periodo

    elif tipo_exportacao == 'mensal': 
        primeiro_dia_mes_atual = hoje.replace(day=1)
        fim_periodo = primeiro_dia_mes_atual - timedelta(days=1)
        inicio_periodo = fim_periodo.replace(day=1)
        return inicio_periodo, fim_periodo

    else:
        raise ValueError("Tipo de extração inválido. Use: diario, semanal ou mensal.")
