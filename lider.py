import Pyro5.api

class Lider:
    def __init__(self, nome):
        self.nome = nome
    def getName(self):
        return self.nome
    @Pyro5.api.expose
    def teste (self):
        return 'hello world!'
    
ns = Pyro5.api.locate_ns()
daemon = Pyro5.api.Daemon()

lider_obj = Lider('Lider_Epoca1')
uri_objetoPyro = daemon.register(lider_obj)

ns.register(lider_obj.getName(), uri_objetoPyro)


print(f"Objeto {lider_obj.getName()} registrado com URI: {uri_objetoPyro}")
#while(True):
