from flask import Flask, request, render_template, redirect, url_for
import redis
import csv
import random
from locust import HttpUser, task, between

app = Flask(__name__)

# Inicialize a conexão com o Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# ... Defina as funções do Flask (create_registro, read_registro, etc.) como antes

class MyUser(HttpUser):
    wait_time = between(1, 5)  # Define uma pausa aleatória entre as solicitações

    @task(1)
    def create_registro(self):
        # Simule uma operação de criação (escrita)
        data = {
            "nome": "NovoNome",
            "matricula": f"MAT{random.randint(10000, 99999)}",
            "curso": "NovoCurso"
        }
        self.client.post("/create", data=data)

    @task(1)
    def read_registro(self):
        # Simule uma operação de leitura
        matricula = f"MAT{random.randint(1000, 9999)}"  # Substitua pelo ID de um registro existente
        self.client.get(f"/read/{matricula}")

# Resto do código Flask ...

if __name__ == "__main__":
    app.run(debug=True)
