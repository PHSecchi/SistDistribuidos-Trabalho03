import Pyro5.api

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
        self.lider = Pyro5.api.Proxy(ns.lookup("Lider_Epoca1"))

    def infoLider(self):
        info = {
            'cliente': self.name,
            'type': 1,
            'uri' : self.uri
        }
        self.lider.infoNewVot_Obs(info)
    
ns = Pyro5.api.locate_ns()
daemon = Pyro5.api.Daemon()

cliente1 = Cliente(f'Cliente_{ns.count()}',daemon, ns)

print(cliente1.lider.getLog())
