import os
import time

import psycopg2
import paho.mqtt.client as mqtt
from dotenv import load_dotenv


load_dotenv()


BROKER = "broker.hivemq.com"
PORTA = 1883

TOPICO_RUIDO = "senai510/biblioteca/ruido"
TOPICO_PRESENCA = "senai510/biblioteca/presenca"
TOPICO_STATUS = "senai510/biblioteca/status"


dados = {
    "ruido": 0,
    "presenca": "NAO_DETECTADA",
    "status": "SILENCIOSO"
}


ultima_leitura = 0
alerta_ativo = False


def salvar_no_banco():

    conexao = psycopg2.connect(
        os.getenv("DATABASE_URL")
    )

    cursor = conexao.cursor()

    presenca = True

    if dados["presenca"] == "NAO_DETECTADA":
        presenca = False

    cursor.execute("""
        INSERT INTO leituras (nivel_ruido, presenca, status)
        VALUES (%s, %s, %s)
    """, (
        dados["ruido"],
        presenca,
        dados["status"]
    ))

    conexao.commit()

    cursor.close()
    conexao.close()

    print("Leitura salva no Neon!")


def salvar_alerta():

    conexao = psycopg2.connect(
        os.getenv("DATABASE_URL")
    )

    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO alertas (nivel_ruido, mensagem)
        VALUES (%s, %s)
    """, (
        dados["ruido"],
        "Nível de ruído muito alto"
    ))

    conexao.commit()

    cursor.close()
    conexao.close()

    print("ALERTA salvo no Neon!")


def mensagem(client, userdata, msg):

    global ultima_leitura
    global alerta_ativo

    valor = msg.payload.decode()

    print("Mensagem recebida!")
    print("Topico:", msg.topic)
    print("Valor:", valor)
    print("------------------------")


    if msg.topic == TOPICO_RUIDO:

        dados["ruido"] = int(valor)


    elif msg.topic == TOPICO_PRESENCA:

        dados["presenca"] = valor


    elif msg.topic == TOPICO_STATUS:

        dados["status"] = valor

        if valor == "MUITO_ALTO":

            if alerta_ativo == False:

                salvar_alerta()

                alerta_ativo = True

        else:

            alerta_ativo = False


    tempo_atual = time.time()

    if tempo_atual - ultima_leitura >= 5:

        salvar_no_banco()

        ultima_leitura = tempo_atual


cliente = mqtt.Client()

cliente.on_message = mensagem

cliente.connect(BROKER, PORTA)

cliente.subscribe(TOPICO_RUIDO)
cliente.subscribe(TOPICO_PRESENCA)
cliente.subscribe(TOPICO_STATUS)


print("Conectado ao HiveMQ!")
print("Aguardando mensagens do ESP32...")
print("------------------------")


cliente.loop_start()