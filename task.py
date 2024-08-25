from dataclasses import dataclass, field
from Enums.task_priority import TaskPriority
from task_requirements import TaskRequirements


@dataclass(frozen=True, order=True)
class Task:
    _id: field(init=False)
    _name: str
    _priority: TaskPriority
    _requirements: TaskRequirements
    _duration: float

    def __post_init__(self):
        object.__setattr__(self, '_id', id(self))

    def get_id(self) -> id:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_priority(self) -> TaskPriority:
        return self._priority

    def get_requirements(self) -> TaskRequirements:
        return self._requirements

    def get_duration(self) -> float:
        return self._duration
