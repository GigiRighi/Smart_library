import os

import psycopg2

from dotenv import load_dotenv

from flask import Flask, render_template, jsonify

from mqtt import cliente, dados


load_dotenv()


app = Flask(__name__)


@app.route("/")
def inicio():

    return render_template(
        "index.html",
        dados=dados
    )


@app.route("/dados")
def obter_dados():

    return jsonify(dados)


@app.route("/historico")
def historico():

    conexao = psycopg2.connect(
        os.getenv("DATABASE_URL")
    )

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nivel_ruido, presenca, status, data_hora
        FROM leituras
        ORDER BY data_hora DESC
        LIMIT 50
    """)

    leituras = cursor.fetchall()

    cursor.close()
    conexao.close()

    resultado = []

    for leitura in leituras:

        resultado.append({
            "id": leitura[0],
            "nivel_ruido": leitura[1],
            "presenca": leitura[2],
            "status": leitura[3],
            "data_hora": str(leitura[4])
        })

    return jsonify(resultado)


@app.route("/alertas")
def alertas():

    conexao = psycopg2.connect(
        os.getenv("DATABASE_URL")
    )

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nivel_ruido, mensagem, data_hora
        FROM alertas
        ORDER BY data_hora DESC
        LIMIT 20
    """)

    alertas_banco = cursor.fetchall()

    cursor.close()
    conexao.close()

    resultado = []

    for alerta in alertas_banco:

        resultado.append({
            "id": alerta[0],
            "nivel_ruido": alerta[1],
            "mensagem": alerta[2],
            "data_hora": str(alerta[3])
        })

    return jsonify(resultado)


if __name__ == "__main__":

    app.run(debug=True)