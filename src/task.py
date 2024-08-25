from dataclasses import dataclass, field
from enums import TaskType, StatusEnum

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
