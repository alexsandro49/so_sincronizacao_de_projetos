from dataclasses import dataclass


@dataclass(frozen=True)
class TaskRequirements:
    _energy: float
    _fuel: float
    _oxygen: float

    def get_energy(self) -> float:
        return self._energy

    def get_fuel(self) -> float:
        return self._fuel

    def get_oxygen(self) -> float:
        return self._oxygen
