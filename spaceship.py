import threading
import time
from dataclasses import dataclass, field

@dataclass
class Spaceship:
    _energy: float
    _fuel: float
    _oxygen: float
    _energy_capacity: float = field(init=False)
    _fuel_capacity: float = field(init=False)
    _oxygen_capacity: float = field(init=False)
    resource_lock: threading.Lock = field(default_factory=threading.Lock, init=False)

    def __post_init__(self):
        self._energy_capacity = self.getEnergy()
        self._fuel_capacity = self.getFuel()
        self._oxygen_capacity = self.getOxygen()

    def getEnergy(self) -> float:
        return self._energy

    def setEnergy(self, energy_consumed) -> None:
        if energy_consumed > self._energy:
            raise ValueError("Energia insuficiente para a operação")
        self._energy -= energy_consumed

    def getFuel(self) -> float:
        return self._fuel

    def setFuel(self, fuel_consumed) -> None:
        if fuel_consumed > self._fuel:
            raise ValueError("Combustível insuficiente para a operação")
        self._fuel -= fuel_consumed

    def getOxygen(self) -> float:
        return self._oxygen

    def setOxygen(self, oxygen_consumed) -> None:
        if oxygen_consumed > self._oxygen:
            raise ValueError("Oxigênio insuficiente para a operação")
        self._oxygen -= oxygen_consumed

    def _format_progress(self, current: float, total: float, length: int = 20) -> str:
        progress = int((current / total) * length)
        return f"[{'#' * progress}{'.' * (length - progress)}] {current:.1f}/{total:.1f}"

    def __str__(self) -> str:
        energy_percentage = self._energy / self._energy_capacity * 100
        fuel_percentage = self._fuel / self._fuel_capacity * 100
        oxygen_percentage = self._oxygen / self._oxygen_capacity * 100
        return (f"\n[STATUS DA NAVE]\n"
                f"  Energia: {self._format_progress(self._energy, self._energy_capacity)} ({energy_percentage:.1f}%)\n"
                f"  Combustível: {self._format_progress(self._fuel, self._fuel_capacity)} ({fuel_percentage:.1f}%)\n"
                f"  Oxigênio: {self._format_progress(self._oxygen, self._oxygen_capacity)} ({oxygen_percentage:.1f}%)\n")

    def perform_task(self, task_name, energy_needed, fuel_needed, oxygen_needed, duration):
        with self.resource_lock:
            try:
                # Verifica se há recursos suficientes
                self.setEnergy(energy_needed)
                self.setFuel(fuel_needed)
                self.setOxygen(oxygen_needed)
                
                print(f"\n➡️ [INÍCIO] {task_name}")
                print(f"  Consumindo recursos: Energia={energy_needed}, Combustível={fuel_needed}, Oxigênio={oxygen_needed}")
                print(f"  Tempo estimado: {duration} segundos")
                
                # Exibe o status atual dos recursos
                print(self)
                
                # Simula a execução da tarefa
                time.sleep(duration)
                
                print(f"✅ [CONCLUÍDO] {task_name}")
            except ValueError as e:
                print(f"❌ [FALHA] {task_name}: {e}")

# Exemplo de Tarefas a serem executadas
def task(spaceship, task_name, energy, fuel, oxygen, duration):
    spaceship.perform_task(task_name, energy, fuel, oxygen, duration)

# Inicialização da nave com recursos limitados
spaceship = Spaceship(100, 50, 75)

# Lista de tarefas que as threads irão executar
tasks = [
    ("Comunicação com a Terra", 20, 10, 5, 3),
    ("Navegação", 15, 12, 4, 2),
    ("Coleta de Amostras", 30, 20, 8, 5),
    ("Análise Científica", 25, 15, 6, 4),
]

# Criando threads para as tarefas
threads = []
for t in tasks:
    thread = threading.Thread(target=task, args=(spaceship, *t))
    threads.append(thread)
    thread.start()

# Espera todas as threads finalizarem
for thread in threads:
    thread.join()

print("\n🚀 Todas as tarefas foram concluídas.")
