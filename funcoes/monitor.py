def classificar_status_ruido(nivel_ruido):
    """Retorna a categoria do ambiente com base no nível em decibéis."""
    if nivel_ruido < 50:
        return "SILENCIOSO"
    elif nivel_ruido <= 80:
        return "ATENCAO"
    else:
        return "MUITO_ALTO"


def precisa_disparar_alerta(status):
    """Verifica se o status exige a gravação de um alerta de emergência."""
    return status == "MUITO_ALTO"


def formatar_dados_sensor(ruido, presenca_detectada):
    """Recebe as leituras do sensor e gera o dicionário formatado."""
    status = classificar_status_ruido(ruido)
    texto_presenca = "DETECTADA" if presenca_detectada else "NAO_DETECTADA"

    return {
        "ruido": ruido,
        "presenca": texto_presenca,
        "status": status
    }