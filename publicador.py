import Pyro4

def connectToLeader():

    try:
        print("Conectando-se ao líder...")
        return Pyro4.Proxy("PYRONAME:Lider-Epoca1")
    except Exception as e:
        print(f"Erro ao conectar-se com o lider: {e}")
        return None

def main():
    brokerLeader = connectToLeader()

    while True:
        msg = input("Insira a mensagem (ou 'sair' para sair): ")
        if msg.lower() == "sair":
            break
        print("Publicando...")
        success = brokerLeader.newPublication(msg)
        if success:
            print(f"Mensagem '{msg}' publicada com sucesso!")
        else:
            print(f"Erro ao publicar mensagem.")


if __name__ == "__main__":
    main()

