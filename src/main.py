import threading
from time import sleep
from spaceship import Spaceship, TaskType, Task
oxygen, fuel, energy = 100, 100, 100

def main():
    spaceship = Spaceship(oxygen, fuel, energy)

    tasks = [
        Task(id="1", name=TaskType.COMMUNICATION, priority=3, energy_required=10, fuel_required=20, oxygen_required=30, duration=6),
        Task(id="2", name=TaskType.LIFE_RESEARCH, priority=5, energy_required=15, fuel_required=10, oxygen_required=5, duration=3),
        Task(id="3", name=TaskType.SAMPLE_COLLECTION, priority=4, energy_required=20, fuel_required=30, oxygen_required=40, duration=9),
        Task(id="4", name=TaskType.COMMUNICATION, priority=2, energy_required=50, fuel_required=20, oxygen_required=40, duration=4),
        Task(id="5", name=TaskType.SAMPLE_COLLECTION, priority=4, energy_required=20, fuel_required=30, oxygen_required=40, duration=6)
    ]

    for task in tasks:
        spaceship.create_task(task)

    task_processor_thread = threading.Thread(target=spaceship.process_tasks)
    task_processor_thread.start()

    task_adder_thread = threading.Thread(target=spaceship.add_random_tasks)
    task_adder_thread.start()



if __name__ == "__main__":
    main()
