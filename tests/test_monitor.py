from funcoes.monitor import (
    classificar_status_ruido,
    precisa_disparar_alerta,
    formatar_dados_sensor
)

# TESTES DE CLASSIFICAÇÃO DE RUÍDO

def test_ambiente_silencioso():
    # FUNÇÃO DO TESTE:
    # Validar se ruídos abaixo de 50 dB são classificados como SILENCIOSO.
    # RESPOSTA ESPERADA:
    # O retorno da função deve ser a string "SILENCIOSO".

    assert classificar_status_ruido(30) == "SILENCIOSO"


def test_ambiente_atencao():
    # FUNÇÃO DO TESTE:
    # Validar se ruídos intermediários (entre 50 e 80 dB) mudam o status para ATENCAO.
    #
    # RESPOSTA ESPERADA:
    # O retorno da função deve ser a string "ATENCAO".

    assert classificar_status_ruido(70) == "ATENCAO"


def test_ambiente_muito_alto():
    # FUNÇÃO DO TESTE:
    # Validar se ruídos acima de 80 dB são classificados como MUITO_ALTO.
    #
    # RESPOSTA ESPERADA:
    # O retorno da função deve ser a string "MUITO_ALTO".

    assert classificar_status_ruido(95) == "MUITO_ALTO"

# TESTES DE DISPARO DE ALERTA

def test_alerta_muito_alto():
    # FUNÇÃO DO TESTE:
    # Checar se o alerta é ativado quando o status for MUITO_ALTO.
    #
    # RESPOSTA ESPERADA:
    # O retorno da função deve ser True.

    assert precisa_disparar_alerta("MUITO_ALTO") is True


def test_alerta_silencioso():
    # FUNÇÃO DO TESTE:
    # Checar se o alerta permanece desativado em status normais.
    #
    # RESPOSTA ESPERADA:
    # O retorno da função deve ser False.

    assert precisa_disparar_alerta("SILENCIOSO") is False

# TESTES DE FORMATAÇÃO DOS DADOS

def test_formatacao_dados_com_presenca():
    # FUNÇÃO DO TESTE:
    # Validar o dicionário retornado quando há presença detectada e ruído normal.
    #
    # RESPOSTA ESPERADA:
    # Um dicionário com ruido=65, presenca="DETECTADA" e status="ATENCAO".

    dados = formatar_dados_sensor(ruido=65, presenca_detectada=True)

    assert dados["ruido"] == 65
    assert dados["presenca"] == "DETECTADA"
    assert dados["status"] == "ATENCAO"


def test_formatacao_dados_sem_presenca():
    # FUNÇÃO DO TESTE:
    # Validar a formatação quando o sensor não detecta presença humana.
    #
    # RESPOSTA ESPERADA:
    # Um dicionário contendo presenca="NAO_DETECTADA" e status="SILENCIOSO".

    dados = formatar_dados_sensor(ruido=20, presenca_detectada=False)

    assert dados["ruido"] == 20
    assert dados["presenca"] == "NAO_DETECTADA"
    assert dados["status"] == "SILENCIOSO"