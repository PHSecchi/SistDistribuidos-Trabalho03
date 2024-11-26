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
    ("Observador", 3),
]

startMultipleInstances("broker.py", instances_to_run)
