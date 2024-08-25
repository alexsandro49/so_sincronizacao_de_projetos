import threading
import time
from datetime import datetime
from dataclasses import dataclass, field

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
panel_table.add_column()
panel_table.add_column()
panel_table.add_column()

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
                print_log(f"[magenta]Tarefa liberada para execução: {task_name}")
                print_log(f"Recursos necessários: Energia: {energy_needed}, Combustível: {fuel_needed}, Oxigênio: {oxygen_needed}")
                print_log(f"[magenta]Analisando viabilidade")

                # Consumo dos recursos
                self.consume_energy(energy_needed)
                self.consume_fuel(fuel_needed)
                self.consume_oxygen(oxygen_needed)

                print_log(f"[yellow]Execução autorizada")
                print_log(f"[blue]Executando tarefa: {task_name}")

                # Atualiza o progresso dos recursos
                resources_progress.update(energy_task_id, completed=self._energy)
                resources_progress.update(fuel_task_id, completed=self._fuel)
                resources_progress.update(oxygen_task_id, completed=self._oxygen)

                start_time = get_timestamp()
                print_task_panel(start_time, task_name, "[blue]INICIADO")
                current_task = tasks_progress.add_task(task_name, total=duration, completed=0)

                for _ in range(duration):
                    time.sleep(1)
                    tasks_progress.update(task_id, advance=1)
                    print_log(tasks_progress.get_renderable())

                end_time = get_timestamp()
                print_task_panel(end_time, task_name, "[green]CONCLUÍDO")
                tasks_progress.remove_task(task_id)
                print_log(f"[green]Tarefa concluída: {task_name}")

            except ValueError as e:
                error_time = get_timestamp()
                print_task_panel(error_time, task_name, "[red]ERRO")
                print_log(f"[red]Tarefa falhou: {task_name}")
                print_log(f"[red]Erro: {str(e)}")

# Função que representa uma tarefa
def task(spaceship, task_id, task_name, energy, fuel, oxygen, duration):
    spaceship.perform_task(task_id, task_name, energy, fuel, oxygen, duration)

# Simulação de nave espacial
spaceship = Spaceship(100, 50, 75)

# Lista de tarefas
tasks = [
    ("Comunicação com a Terra", 20, 10, 5, 3),
    ("Navegação", 15, 12, 4, 2),
    ("Coleta de Amostras", 30, 20, 8, 5),
    ("Análise Científica", 25, 15, 6, 4),
]

# Execução das tarefas em threads
threads = []

with Live(layout, refresh_per_second=4, vertical_overflow="ellipsis", console=console) as live:
    # Adicionar os recursos ao progresso
    energy_task_id = resources_progress.add_task("Energia", resource_name="Energia", total=spaceship._energy_capacity, completed=spaceship.get_energy())
    fuel_task_id = resources_progress.add_task("Combustível", resource_name="Combustível", total=spaceship._fuel_capacity, completed=spaceship.get_fuel())
    oxygen_task_id = resources_progress.add_task("Oxigênio", resource_name="Oxigênio", total=spaceship._oxygen_capacity, completed=spaceship.get_oxygen())

    layout.split_row(
        Panel(panel_table, title="🚀 Missão Marte - Tarefas", border_style="cyan", title_align="left"),
        Panel(resources_progress, title="📦 Recursos - Painel", border_style="green", title_align="left"),
        Panel(logs_table, title="📦 Logs - Painel", border_style="green", title_align="left"),
    )

    print_log("Missão iniciada")

    for task_id, (task_name, energy, fuel, oxygen, duration) in enumerate(tasks):
        time.sleep(0.5)
        create_time = get_timestamp()
        thread = threading.Thread(target=task, args=(spaceship, task_id, task_name, energy, fuel, oxygen, duration))
        print_task_panel(create_time, task_name, "[yellow]PENDENTE")
        print_log(f"[green]Tarefa criada: {task_name}")
        threads.append(thread)
        thread.start()

    # Espera todas as threads finalizarem
    for thread in threads:
        thread.join()
