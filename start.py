# Falta:
# - Separar uncomited de commited (tipo em duas filas)
# - Se o número de votantes for inferior ao mínimo do quórum promove um observador - aqui o líder conta e o cliente tem que solicitar a faixa de logs 'offset' desde o último commited (Novo votante tem que solicitar os dados do líder, não o líder enviar)
# - Votantes tem que saber quantos votantes tem


import subprocess

def startMultipleInstances(executable, instances):
    for brokerName, mode in instances:
        cmd = f'start cmd /k python {executable} {brokerName} {mode}'
        print(f"Iniciando: {cmd}")
        subprocess.Popen(cmd, shell=True)

instances_to_run = [
    ("Lider1", 1),
    ("Votante1", 2),
    ("Votante2", 2),
    ("Votante3", 2),
    ("Observador", 3)
]

startMultipleInstances("broker.py", instances_to_run)
