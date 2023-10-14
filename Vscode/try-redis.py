import csv
import pandas as pd
import redis

# Conecte-se ao Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Defina uma chave para os dados no Redis
REDIS_KEY = "meus_dados"

# Função para criar um registro
def criar_registro():
    registro = {}
    for chave in input("Informe os dados no formato 'chave:valor' (ou deixe em branco para sair): ").split():
        if ":" in chave:
            chave, valor = chave.split(":")
            registro[chave] = valor
    # Gere um ID único, você pode usar um contador ou outra estratégia
    registro_id = redis_client.incr("id_counter")
    registro["id"] = registro_id

    # Armazene o registro no Redis como um hash
    redis_client.hmset(f"{REDIS_KEY}:{registro_id}", registro)

# Função para ler todos os registros
def ler_registros():
    registros = []
    keys = redis_client.keys(f"{REDIS_KEY}:*")
    for key in keys:
        registro = redis_client.hgetall(key)
        registros.append(registro)
    return registros

# Função para atualizar um registro
def atualizar_registro():
    registro_id = input("Informe o ID do registro que deseja atualizar: ")
    novo_registro = {}
    for chave in input("Informe os novos dados no formato 'chave:valor' (ou deixe em branco para sair): ").split():
        if ":" in chave:
            chave, valor = chave.split(":")
            novo_registro[chave] = valor
    redis_client.hmset(f"{REDIS_KEY}:{registro_id}", novo_registro)

# Função para excluir um registro
def excluir_registro():
    registro_id = input("Informe o ID do registro que deseja excluir: ")
    redis_client.delete(f"{REDIS_KEY}:{registro_id}")

# Função principal
def main():
    while True:
        print("\nOpções:")
        print("1. Criar registro")
        print("2. Ler registros")
        print("3. Atualizar registro")
        print("4. Excluir registro")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            criar_registro()
            print("Registro criado.")

        elif opcao == "2":
            registros = ler_registros()
            for registro in registros:
                print(registro)

        elif opcao == "3":
            atualizar_registro()
            print("Registro atualizado.")

        elif opcao == "4":
            excluir_registro()
            print("Registro excluído.")

        elif opcao == "5":
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
