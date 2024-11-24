import Pyro5.api
import threading

class Cliente:
    def __init__(self, name, daemon, ns):
        self.name = name
        self.logs = []
        self.count = 0
        self.listClient = []
        self.register(daemon, ns)
        self.getLider(ns)
        self.infoLider()
    
    def getName(self):
        return self.name
    
    def register(self,daemon, ns):
        self.uri = daemon.register(self)
        ns.register(self.name, self.uri)
        print(f"Objeto {self.name} registrado com URI: {self.uri}")
    
    def getLider(self,ns):
        print(type(ns.lookup("Lider_Epoca1")))
        self.lider = Pyro5.api.Proxy(ns.lookup("Lider_Epoca1"))
        self.lider._pyroBind()
        print(f'Lider encontrado')
       #print("Métodos expostos:", self.lider._pyroMethods)

    def infoLider(self):
        info = {
            'cliente': self.name,
            'type': 1,
            'uri' : self.uri
        }
        self.lider.infoNewVot_Obs(info)
        print("deposi")
    
    @Pyro5.api.expose
    @Pyro5.api.oneway
    def reciveNotification(self, notification):
       print(f"Notificação recebida: {notification}")
    
def main():
    ns = Pyro5.api.locate_ns()
    daemon = Pyro5.api.Daemon()
    
    cliente1 = Cliente(f'Cliente_{ns.count()}',daemon, ns)
    # Rodar o daemon em uma thread separada
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