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
    
    def registerLog(self,msg):
        newLog = {
            'epoca' : self.name,
            'offset' : self.count,
            'msg' : msg
        }
        self.logs.append(newLog)

    def sendNotification(cod):
        cod=0

    @Pyro5.api.expose
    def getLog (self):
        return self.logs
    
    def newPubli(self,msg):
        self.registerLog(msg)

    def infoNewVot_Obs(self,info):
        self.listClient.append(info)
    

ns = Pyro5.api.locate_ns()
daemon = Pyro5.api.Daemon()

lider= Lider('Lider_Epoca1',daemon, ns)

lider.registerLog()

daemon.requestLoop()