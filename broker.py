#python -m Pyro4.naming
#pip install Pyro4

import Pyro4
import time
import threading

@Pyro4.expose
class Broker:
    
    def __init__(self, name, mode): 
        self.name = name
        self.mode = mode  # 1:líder, 2:votante e 3:observador
        self.epoca = 1
        self.logs = []  
        self.leader = None 
        self.voters = {}  
        self.observers = []  
        self.confirmations = {}  
        self.heartbeatTime = 5

        if self.mode == 1:
            self.heartbeats = {}  
        print(f"Broker {name} inicializado como {self.getMode(mode)}.")

    def getMode(self,mode):
        match mode:
            case 1:
                return "Líder"
            case 2:
                return "Votante"
            case 3: 
                return "Observador"

    #Registra o broker no NS do Pyro
    def register(self,daemon, ns):
        self.uri = daemon.register(self)
        if self.mode == 1:
            ns.register("Lider-Epoca1", self.uri)
            print(f"Líder registrado como 'Lider-Epoca1' com a URI: {self.uri}.")
        else:
            ns.register(self.name, self.uri)
            print(f"Broker {self.name} registrado com a URI: {self.uri}")

    def getLeader(self):
        try:
            self.leader = Pyro4.Proxy("PYRONAME:Lider-Epoca1")
            print(f"Líder encontrado!")
        except Exception as e:
            print(f"Erro ao conectar ao líder: {e}")
            return

    #Registra novos brokers no lider
    def infoLeader(self,brokerName, mode, uri):
        proxy = Pyro4.Proxy(uri)
        
        if mode == 2:
            self.voters[brokerName] = proxy
            self.heartbeats[brokerName] = time.time() 
            print(f"Votante {brokerName} registrado.")
        else:
            self.observers.append(proxy)
            print(f"Observador {brokerName} registrado.")

    #Recebe publicação do publicador
    def newPublication(self,msg):

        newLog = {"epoca": self.epoca, "offset": len(self.logs), "msg": msg, "committed": False}
        self.logs.append(newLog)
        print(f"Nova mensagem adicionada ao log: {newLog}")

        # Notifica votantes
        voters = list(self.voters.values())
        confirmations = [] 

        for proxy in voters:
            def notifyVoter(voter):
                try:
                    voter.replicateLog(len(self.logs)- 1)
                    confirmations.append(True)
                except Exception as e:
                    print(f"Erro ao notificar votante: {e}")
                    confirmations.append(False)
            
            threading.Thread(target=notifyVoter, args=(proxy,)).start()

        # Aguarda as confirmações
        while len(confirmations) < len(voters):
            time.sleep(0.1)

        # Verifica se a quantidade mínima confirmou o recebimento 
        if confirmations.count(True) >= (len(self.voters) // 2) + 1:
            self.logs[-1]['committed'] = True
            print(f"Mensagem commitada pelo quórum!")
            return True
        else:
            print(f"Falha ao atingir o número minimo de confirmação.")
            return False

    # Busca o log e envia confirmação para o lider
    def replicateLog(self, offset):
        try:
            infoToReplicate = self.leader.getLogs(offset)
            if infoToReplicate:
                self.logs.append(infoToReplicate)
                print(f"Dados replicados do líder: {infoToReplicate}")
                
        except Exception as e:
            print(f"Erro ao replicar log: {e}")

    def getLogs(self,offset):
        return self.logs[offset]

    #Gera logs commitados para envio para o consumidor
    def getCommittedLogs(self):
        committedLogs = [log for log in self.logs if log["committed"]]
        print(f"Enviando logs para consumidor: {committedLogs}")
        return committedLogs

    #metodo para envio do heartbeat pelo votante
    def heartbeat(self):
        while True:
            try:
                self.leader.receiveHeartbeat(self.name)
                print(f"Heartbeat enviado para o líder.")
            except Exception as e:
                print(f"Erro ao enviar heartbeat: {e}")
            time.sleep(self.heartbeatTime)

    #Verifica se votante se desconectou
    def checkHeartbeat(self):
        while True:  
            for voterName in list(self.heartbeats):
                if time.time() - self.heartbeats[voterName] > self.heartbeatTime * 2:
                    self.heartbeats.pop(voterName, None)
                    self.voters.pop(voterName, None)
                    print(f"{voterName}: Não está respondendo.")
                    self.promoteObserver()
            time.sleep(self.heartbeatTime)

    #recebe a mensagem de heartbeat dos votantes
    def receiveHeartbeat(self, voterName):
        self.heartbeats[voterName] = time.time()
        print(f"{voterName}: heartbeat recebido.")

    def synchronizelogs(self,logs):
        self.logs = logs

    def promoteObserver(self):
        if self.observers:
            newVoter = self.observers.pop(0)
            newVoterName = f"Votante{len(self.voters) + 1}"
            self.voters[newVoterName] = newVoter
            self.heartbeats[newVoterName] = time.time()

            print(f"Observador promovido a votante: {newVoterName}")
            newVoter.observerToVoter(newVoterName,self.logs)
    

    def observerToVoter(self, newVoterName, logs):
        self.mode = 2
        self.logs = logs
        threading.Thread(target=self.heartbeat, daemon=True).start()
        print(f"Observador promovido a {newVoterName}")


#Inicialização do broker
def startBroker(brokerName, mode): 
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS() 

    broker = Broker(brokerName, mode)
    broker.register(daemon,ns)

    if mode == 1:
        threading.Thread(target=broker.checkHeartbeat, daemon=True).start()
    else:
        broker.getLeader()
        try:
            broker.leader.infoLeader(brokerName, mode, broker.uri)
            print(f"{brokerName} registrado como '{broker.getMode(mode)}'e conectado.")
            
            if mode == 2:
                threading.Thread(target=broker.heartbeat, daemon=True).start()
        except Exception as e:
            print(f"Erro ao conectar ao líder: {e}")
            return

    daemon.requestLoop()

if __name__ == "__main__":
    import sys
    brokerName = sys.argv[1]
    mode = int(sys.argv[2])
    startBroker(brokerName, mode)