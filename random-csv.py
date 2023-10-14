import csv
import redis
import random

# Inicialize a conexão com o Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)  # Atualize as informações de conexão conforme necessário

# Leia o conteúdo do arquivo CSV
with open("dados.csv", mode='r', newline='') as file:
    reader = csv.reader(file)
    next(reader)  # Pule o cabeçalho
    for row in reader:
        nome, matricula, curso = row
        # Use uma chave única (por exemplo, matrícula) para armazenar os dados no Redis
        redis_key = f"matricula:{matricula}"
        # Armazene os dados no Redis como um dicionário
        r.hset(redis_key, "nome", nome)
        r.hset(redis_key, "matricula", matricula)
        r.hset(redis_key, "curso", curso)

print("Dados CSV salvos no Redis.")

# Função para criar um novo registro
def create_registro(input_string):
    nome, matricula, curso = input_string.split(",")
    redis_key = f"matricula:{matricula}"
    if r.hget(redis_key, "nome"):
        return "Registro com essa matrícula já existe."
    r.hset(redis_key, "nome", nome)
    r.hset(redis_key, "matricula", matricula)
    r.hset(redis_key, "curso", curso)
    return "Registro criado com sucesso."

# Função para ler um registro por matrícula
def read_registro(matricula):
    redis_key = f"matricula:{matricula}"
    registro = r.hgetall(redis_key)
    return registro if registro else "Registro não encontrado."

# Função para atualizar um registro por matrícula
def update_registro(matricula, input_string):
    nome, matricula_nova, curso = input_string.split(",")
    redis_key = f"matrícula:{matricula}"
    if not r.hget(redis_key, "nome"):
        return "Registro não encontrado."
    r.hset(redis_key, "nome", nome)
    r.hset(redis_key, "matricula", matricula_nova)
    r.hset(redis_key, "curso", curso)
    return "Registro atualizado com sucesso."

# Função para excluir um registro por matrícula
def delete_registro(matricula):
    redis_key = f"matricula:{matricula}"
    if not r.hget(redis_key, "nome"):
        return "Registro não encontrado."
    r.delete(redis_key)
    return "Registro excluído com sucesso."

# Função para gerar uma operação (leitura ou escrita) com base na probabilidade
def operacao_aleatoria():
    probabilidade = random.random()
    if probabilidade < 0.5:
        return "leitura"
    else:
        return "escrita"

# Função principal para executar as operações CRUD
def main():
    while True:
        operacao = operacao_aleatoria()

        if operacao == "leitura":
            matricula = input("Digite a matrícula do registro a ser lido: ")
            result = read_registro(matricula)
            if result == "Registro não encontrado.":
                print(result)
            else:
                print("Registro encontrado:")
                for key, value in result.items():
                    print(f"{key.decode('utf-8')}: {value.decode('utf-8')}")
        else:
            input_string = input("Digite os dados do novo registro (nome, matrícula, curso): ")
            result = create_registro(input_string)
            print(result)

        continuar = input("Deseja realizar outra operação? (S/N): ")
        if continuar.lower() != "s":
            print("Saindo.")
            break

if __name__ == "__main__":
    main()
