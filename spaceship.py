import threading
import time
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from queue import PriorityQueue
import random

from rich.live import Live
from rich.table import Table
from rich import print
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn

# Configurações iniciais de layout e console
layout = Layout()
console = Console()

# Tabela para exibir o status das tarefas
panel_table = Table.grid(expand=True)
panel_table.add_column("Tempo")
panel_table.add_column("Descrição")
panel_table.add_column("Status")

# Progresso das tarefas
tasks_progress = Progress()

# Tabela para exibir os logs
logs_table = Table(show_header=False, box=None, expand=True)

# Progresso dos recursos da nave
resources_progress = Progress(
    TextColumn("[bold]{task.fields[resource_name]}:"),
    BarColumn(),
    "[progress.percentage]{task.percentage:>3.0f}%",
)

class TaskType(Enum):
    COMUNICACAO = "Comunicação com a Terra"
    NAVEGACAO = "Navegação"
    COLETA_AMOSTRAS = "Coleta de Amostras"
    ANALISE_CIENTIFICA = "Análise Científica"
    PESQUISA_VIDA = "Pesquisa de Vida"
    AJUSTES_TRAJETORIA = "Ajustes de Trajetória"

class TaskPriority(Enum):
    ALTA = 1
    MEDIA = 2
    BAIXA = 3

def get_timestamp():
    return f"[{datetime.now().strftime('%H:%M:%S')}]"

def print_task_panel(time, description, status):
    panel_table.add_row(time, description, status)

def print_log(message):
    logs_table.add_row(get_timestamp(), message)

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
        self._energy_capacity = self.get_energy()
        self._fuel_capacity = self.get_fuel()
        self._oxygen_capacity = self.get_oxygen()

    def get_energy(self) -> float:
        return self._energy

    def consume_energy(self, amount) -> None:
        if amount > self._energy:
            raise ValueError("Energia insuficiente para a operação")
        self._energy -= amount

    def get_fuel(self) -> float:
        return self._fuel

    def consume_fuel(self, amount) -> None:
        if amount > self._fuel:
            raise ValueError("Combustível insuficiente para a operação")
        self._fuel -= amount

    def get_oxygen(self) -> float:
        return self._oxygen

    def consume_oxygen(self, amount) -> None:
        if amount > self._oxygen:
            raise ValueError("Oxigênio insuficiente para a operação")
        self._oxygen -= amount

    def perform_task(self, task_id, task_name, energy_needed, fuel_needed, oxygen_needed, duration):
        with self.resource_lock:
            try:
                # Consumo dos recursos
                self.consume_energy(energy_needed)
                self.consume_fuel(fuel_needed)
                self.consume_oxygen(oxygen_needed)

                # Atualiza o progresso dos recursos
                resources_progress.update(energy_task_id, completed=self._energy)
                resources_progress.update(fuel_task_id, completed=self._fuel)
                resources_progress.update(oxygen_task_id, completed=self._oxygen)

                start_time = get_timestamp()
                print_log(f"[green]Tarefa iniciada: {task_name}")
                print_task_panel(start_time, task_name, "[blue]INICIADO")
                tasks_progress.start_task(task_id)
                tasks_progress.update(task_id, description=f"[blue][INICIADO] {task_name}")
                for _ in range(duration):
                    time.sleep(1)
                    tasks_progress.update(task_id, advance=1)

                end_time = get_timestamp()
                tasks_progress.update(task_id, description=f"[green][CONCLUÍDO] {task_name}")
                print_task_panel(end_time, task_name, "[green]CONCLUÍDO")
                print_log(f"[green]Tarefa concluída: {task_name}")

            except ValueError as e:
                error_time = get_timestamp()
                print_task_panel(error_time, task_name, "[red]ERRO")
                tasks_progress.update(task_id, description=f"[red][FALHOU] {task_name}")
                print_log(f"[red]Tarefa falhou: {task_name}")
                print_log(f"[red]Erro: {str(e)}")

# Função que representa uma tarefa
def task(spaceship, task_id, task_name, energy, fuel, oxygen, duration):
    spaceship.perform_task(task_id, task_name, energy, fuel, oxygen, duration)

# Simulação de nave espacial
spaceship = Spaceship(200, 100, 80)

# Fila de tarefas com prioridade
task_queue = PriorityQueue()

# Função para adicionar tarefas à fila
def add_task_to_queue(task_name, priority, energy, fuel, oxygen, duration):
    priority_level = TaskPriority[priority].value
    task_queue.put((priority_level, task_name, energy, fuel, oxygen, duration))

# Lista de tarefas inicial
tasks_data = [
    (TaskType.COMUNICACAO.value, TaskPriority.MEDIA.name, 20, 10, 5, 5),
    (TaskType.NAVEGACAO.value, TaskPriority.BAIXA.name, 15, 12, 4, 3),
    (TaskType.COLETA_AMOSTRAS.value, TaskPriority.ALTA.name, 30, 20, 8, 4),
    (TaskType.ANALISE_CIENTIFICA.value, TaskPriority.MEDIA.name, 25, 15, 6, 9),
    (TaskType.PESQUISA_VIDA.value, TaskPriority.MEDIA.name, 35, 30, 12, 10),
    (TaskType.AJUSTES_TRAJETORIA.value, TaskPriority.BAIXA.name, 20, 15, 7, 2),
    (TaskType.COLETA_AMOSTRAS.value, TaskPriority.ALTA.name, 30, 20, 8, 4),
    (TaskType.PESQUISA_VIDA.value, TaskPriority.MEDIA.name, 35, 30, 12, 8)
]

# Adiciona as tarefas iniciais à fila
for task_name, priority, energy, fuel, oxygen, duration in tasks_data:
    add_task_to_queue(task_name, priority, energy, fuel, oxygen, duration)

# Delay inicial para "Sistema inicializando"
def initial_delay():
    print_log("[yellow]Sistema inicializando...")
    time.sleep(1)
    print_log("[green]Sistema iniciado.")

# Adiciona novas tarefas periodicamente
def add_new_tasks_periodically():
    task_types = list(TaskType)
    priorities = list(TaskPriority)
    
    while True:
        time.sleep(random.randint(5, 10))  # Adiciona uma nova tarefa a cada 5 a 10 segundos
        task_name = random.choice([task_type.value for task_type in task_types])
        priority = random.choice([priority.name for priority in priorities])
        energy = random.randint(10, 40)
        fuel = random.randint(5, 25)
        oxygen = random.randint(3, 15)
        duration = random.randint(3, 10)
        add_task_to_queue(task_name, priority, energy, fuel, oxygen, duration)
        tasks_progress.add_task(f"[yellow][PENDENTE] {task_name}", total=duration, completed=0, start=False)
        print_log(f"[yellow]Nova tarefa adicionada: {task_name}")

# Execução das tarefas em threads
threads = []
task_creator_thread = threading.Thread(target=add_new_tasks_periodically)
task_creator_thread.daemon = True
task_creator_thread.start()

def worker():
    initial_delay()  # Adiciona o delay inicial

    while not task_queue.empty() or any(thread.is_alive() for thread in threads):
        if not task_queue.empty():
            _, task_name, energy, fuel, oxygen, duration = task_queue.get()
            task_id = len(threads)
            create_time = get_timestamp()
            thread = threading.Thread(target=task, args=(spaceship, task_id, task_name, energy, fuel, oxygen, duration))
            print_task_panel(create_time, task_name, "[yellow]PENDENTE")
            print_log(f"[yellow]Tarefa criada: {task_name}")
            tasks_progress.add_task(f"[yellow][PENDENTE] {task_name}", total=duration, completed=0, start=False)
            threads.append(thread)
            thread.start()
            task_queue.task_done()

with Live(layout, refresh_per_second=4, vertical_overflow="ellipsis", console=console) as live:
    # Adicionar os recursos ao progresso
    energy_task_id = resources_progress.add_task("Energia", resource_name="Energia", total=spaceship._energy_capacity, completed=spaceship.get_energy())
    fuel_task_id = resources_progress.add_task("Combustível", resource_name="Combustível", total=spaceship._fuel_capacity, completed=spaceship.get_fuel())
    oxygen_task_id = resources_progress.add_task("Oxigênio", resource_name="Oxigênio", total=spaceship._oxygen_capacity, completed=spaceship.get_oxygen())

    layout.split_row(
        Panel(tasks_progress, title="🚀 Missão Marte - Tarefas", border_style="cyan", title_align="left"),
        Panel(resources_progress, title="📦 Recursos - Painel", border_style="green", title_align="left"),
        Panel(logs_table, title="📦 Logs - Painel", border_style="green", title_align="left"),
    )

    print_log("Missão iniciada")

    # Executar tarefas na fila com prioridade
    worker_thread = threading.Thread(target=worker)
    worker_thread.start()

    # Espera todas as threads finalizarem
    worker_thread.join()
    for thread in threads:
        thread.join()
