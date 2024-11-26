import Pyro4
import time

def connectToLeader():

    try:
        print("Conectando-se ao líder...")
        return Pyro4.Proxy("PYRONAME:Líder-Epoca1")
    except Exception as e:
        print(f"Erro ao conectar-se com o lider: {e}")
        return None

def main():
    brokerLeader = connectToLeader()

    print("Consumidor conectado ao líder. Aguardando dados confirmados...")

    while True:
        committedLogs = brokerLeader.getCommittedLogs()
        print("Dados confirmados consumidos:")
        for entry in committedLogs:
            print(f" - {entry['msg']} (epoca: {entry['epoca']}, offset: {entry['offset']})")
        time.sleep(10)


if __name__ == "__main__":
    main()
