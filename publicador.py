import Pyro5.api

class Publisher:
    
    def __init__(self, name, daemon, ns):
        self.name = name
        self.register(daemon, ns)
        self.getLider(ns)

    def register(self,daemon, ns):
        self.uri = daemon.register(self)
        print(f"Objeto {self.name} registrado com URI: {self.uri}")
    
    def getLider(self,ns):
        self.lider = Pyro5.api.Proxy(ns.lookup("Lider_Epoca1"))
        self.lider._pyroBind()
        print(f'Lider {self.lider} encontrado')
        print("Métodos expostos:", self.lider._pyroMethods)
    
    def publish(self, msg):
        self.lider.recivePublication(msg)
        print(f'A mensagem publicada: {msg}')

ns = Pyro5.api.locate_ns()
daemon = Pyro5.api.Daemon()

publi = Publisher('Publicador',daemon, ns)

while True:
    message = input("Digite uma mensagem para ser publicada (ou 'exit' para sair): ")
    if message.lower() == 'exit': 
            break
    elif message.lower() == 'lider':
         publi.getLider(ns)
    else: publi.publish(message)