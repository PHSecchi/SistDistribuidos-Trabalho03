#python -m Pyro5.nameserver
import threading
import Pyro5.api

class Lider:
    
    def __init__(self, name, daemon, ns):
        self.name = name
        self.logs = []
        self.count = 0
        self.listClient = []
        self.register(daemon, ns)

    def getName(self):
        return self.name
    
    def register(self,daemon, ns):
        self.uri = daemon.register(self)
        ns.register(self.name, self.uri)
        print(f"Objeto {self.name} registrado com URI: {self.uri}")
        print(type(self.uri))
    
    def registerLog(self,msg):
        newLog = {
            'epoca' : self.name,
            'offset' : self.count,
            'msg' : msg
        }
        print(f'Novo Log gerado: {newLog}')
        self.logs.append(newLog)
        #print(self.logs)
        self.sendNotification("1")

    def sendNotification(self,cod):
        # if self.listClient:
        print(f'Log enviado para {self.listClient[-1]["obj"]}')
            # print(self.listClient[-1]["obj"]._pyroMethods)
            # self.listClient[-1]["obj"].reciveNotification("teste")
        for client in self.listClient:
            print(f'Log enviado para {client["obj"]}')
            print(type(client["obj"]))
            client["obj"]._pyroMethods()
            try:
                client["obj"]._pyroBind()  # Garante conexão
                client["obj"].reciveNotification(cod)
                print(f"Notificação enviada para {client['cliente']}")
            except Pyro5.errors.CommunicationError as e:
                print(f"Erro ao notificar {client['cliente']}: {e}")           

    @Pyro5.api.expose
    def getLog (self):
        return self.logs
    
    def newPubli(self,msg):
        self.registerLog(msg)

    @Pyro5.api.expose
    @Pyro5.api.oneway
    def infoNewVot_Obs(self,info):
        print(f"Objeto {info['cliente']} querendo registar")
        print(type(info['uri']))
        try:
            obj = Pyro5.api.Proxy(info['uri'])
            obj._pyroTimeout = 5
            obj._pyroBind()  # Testa a conexão
            print(f"Conectado ao cliente: {info['cliente']} com URI: {info['uri']}")
            print("Métodos expostos:", obj._pyroMethods)
        except Pyro5.errors.CommunicationError as e:
            print(f"Erro ao conectar ao cliente: {e}")
        info['obj'] = obj
        obj.reciveNotification("teste") 
        self.listClient.append(info)
            
    def conecta(obj):
        print(obj)
        obj._pyroBind()
        print(obj)
    
    @Pyro5.api.expose
    @Pyro5.api.oneway
    def reciveNotification(self,notification):
        print(notification)
    
    @Pyro5.api.expose
    @Pyro5.api.oneway
    def recivePublication(self,publication):
        print(f"Publicação recebida: {publication}")
        self.registerLog(publication)


def main():
    ns = Pyro5.api.locate_ns()
    daemon = Pyro5.api.Daemon()

    lider= Lider('Lider_Epoca1',daemon, ns)
    threading.Thread(target=daemon.requestLoop, daemon=True).start()
    print("Daemon rodando em segundo plano...")

    # Mantendo o programa ativo para interações
    while True:
        cmd = input("Digite 'sair' para encerrar: ").strip().lower()
        if cmd == "sair":
            daemon.shutdown()
            print("Encerrando o programa.")
            break
    
if __name__ == "__main__":
    main()