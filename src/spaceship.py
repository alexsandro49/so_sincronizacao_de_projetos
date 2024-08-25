from dataclasses import dataclass, field
from typing import Optional
from queue import PriorityQueue
from enum import Enum
import threading
import time

class StatusEnum(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TaskType(Enum):
    COMMUNICATION = "Comunicação com a Terra"
    NAVIGATION = "Navegação"
    SAMPLE_COLLECTION = "Coleta de Amostras"
    SCIENTIFIC_ANALYSIS = "Análise Científica"
    LIFE_RESEARCH = "Pesquisa de Vida"

@dataclass(order=True)
class Task:
    sort_index: int = field(init=False, repr=False)
    id: str = field(hash=True)
    name: TaskType
    priority: int
    energy_required: int
    fuel_required: int
    oxygen_required: int
    duration: int
    status: StatusEnum = field(init=False, default=StatusEnum.PENDING)

    def __post_init__(self):
        status_order = {
            StatusEnum.PENDING: 0,
            StatusEnum.IN_PROGRESS: 1,
            StatusEnum.COMPLETED: 2,
            StatusEnum.FAILED: 3
        }
        self.sort_index = (status_order[self.status], -self.priority)

@dataclass
class Spaceship:
    energy: int
    fuel: int
    oxygen: int
    energy_capacity: Optional[int] = field(default=None)
    fuel_capacity: Optional[int] = field(default=None)
    oxygen_capacity: Optional[int] = field(default=None)
    task_list: PriorityQueue = field(default_factory=PriorityQueue, init=False)
    resource_lock: threading.Lock = field(default_factory=threading.Lock, init=False)
    task_event: threading.Event = field(default_factory=threading.Event, init=False)

    def __post_init__(self):
        if self.energy_capacity is None:
            self.energy_capacity = self.get_energy()
        if self.fuel_capacity is None:
            self.fuel_capacity = self.get_fuel()
        if self.oxygen_capacity is None:
            self.oxygen_capacity = self.get_oxygen()

    def get_energy(self):
        return self.energy

    def consume_energy(self, amount):
        if amount > self.energy_capacity:
            raise ValueError("Energia insuficiente para a operação")
        self.energy -= amount

    def get_fuel(self):
        return self.fuel

    def consume_fuel(self, amount):
        if amount > self.fuel_capacity:
            raise ValueError("Combustível insuficiente para a operação")
        self.fuel -= amount

    def get_oxygen(self):
        return self.oxygen

    def consume_oxygen(self, amount):
        if amount > self.oxygen_capacity:
            raise ValueError("Oxigênio insuficiente para a operação")
        self.oxygen -= amount

    def create_task(self, task: Task):
        self.task_list.put(task)
        self.task_event.set()  # Notifica que há uma nova tarefa

    def list_tasks(self):
        return list(self.task_list.queue)

    def verify_attend_requirements(self, task: Task):
        if task.energy_required > self.get_energy():
            raise ValueError("Energia insuficiente para a operação")
        if task.fuel_required > self.get_fuel():
            raise ValueError("Combustível insuficiente para a operação")
        if task.oxygen_required > self.get_oxygen():
            raise ValueError("Oxigênio insuficiente para a operação")

    def perform_task(self, task: Task):
        with self.resource_lock:
            try:
                if task.status == StatusEnum.PENDING:
                    self.verify_attend_requirements(task)
                    task.status = StatusEnum.IN_PROGRESS
                    print(f"Task {task.name} started.")
                    
                    energy_per_unit = task.energy_required / task.duration
                    fuel_per_unit = task.fuel_required / task.duration
                    oxygen_per_unit = task.oxygen_required / task.duration

                    for t in range(task.duration):
                        self.consume_energy(energy_per_unit)
                        self.consume_fuel(fuel_per_unit)
                        self.consume_oxygen(oxygen_per_unit)
                        
                        time.sleep(1)
                        print(f"[{task.name}] Progress: {t + 1}/{task.duration}")

                    task.status = StatusEnum.COMPLETED                    
                    print(f"Task {task.name} completed successfully!")
                    
            except ValueError as e:
                task.status = StatusEnum.FAILED
                print(f"Task {task.name} failed: {e}")

    def process_tasks(self):
        while True:
            self.task_event.wait()  # Espera até que haja uma tarefa para processar
            self.task_event.clear()  # Limpa o evento

            while not self.task_list.empty():
                task = self.task_list.get()
                if task.status == StatusEnum.PENDING:
                    print(f"Processing task: {task.name} (Priority: {task.priority}, Status: {task.status.value})")
                    self.perform_task(task)
                else:
                    # Se a tarefa não está no status PENDING, coloque-a de volta na fila
                    self.task_list.put(task)

# Exemplo de uso
spaceship = Spaceship(200, 100, 80)

tasks = [
    Task(id="1", name=TaskType.COMMUNICATION, priority=3, energy_required=10, fuel_required=20, oxygen_required=30, duration=6),
    Task(id="2", name=TaskType.LIFE_RESEARCH, priority=5, energy_required=15, fuel_required=10, oxygen_required=5, duration=3),
    Task(id="3", name=TaskType.SAMPLE_COLLECTION, priority=4, energy_required=20, fuel_required=30, oxygen_required=40, duration=9),
    Task(id="4", name=TaskType.COMMUNICATION, priority=2, energy_required=50, fuel_required=20, oxygen_required=40, duration=4),
    Task(id="5", name=TaskType.SAMPLE_COLLECTION, priority=4, energy_required=20, fuel_required=30, oxygen_required=40, duration=6),
    Task(id="6", name=TaskType.SAMPLE_COLLECTION, priority=4, energy_required=20, fuel_required=30, oxygen_required=5, duration=9),
    Task(id="7", name=TaskType.LIFE_RESEARCH, priority=5, energy_required=15, fuel_required=10, oxygen_required=5, duration=3),
]

for task in tasks:
    spaceship.create_task(task)

# Iniciar o processamento das tarefas em uma thread separada
task_processor_thread = threading.Thread(target=spaceship.process_tasks)
task_processor_thread.start()
