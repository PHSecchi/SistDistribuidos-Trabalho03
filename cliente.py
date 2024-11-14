import Pyro5.api

class Cliente:
    def __init__(self, nome):
        self.nome = nome
    def getName(self):
        return self.nome
    
ns = Pyro5.api.locate_ns()
daemon = Pyro5.api.Daemon()

cliente_obj = Cliente(f'Cliente_{ns.count()}')
uri_objetoPyro = daemon.register(cliente_obj)


ns.register(cliente_obj.getName(), uri_objetoPyro)
print(f"Objeto {cliente_obj.getName()} registrado com URI: {uri_objetoPyro}")


lider = Pyro5.api.Proxy(ns.lookup("Lider_Epoca1"))
print(lider.teste())