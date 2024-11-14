import Pyro5.api

class observador:
    teste = 1

daemon = Pyro5.api.Daemon()
uri_objetoPyro = daemon.register(observador)
ns = Pyro5.core.locate_ns()

print(ns.count())

ns.register(f'Observador_{ns.count}', uri_objetoPyro)