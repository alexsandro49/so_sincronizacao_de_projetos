from dataclasses import dataclass, field


@dataclass
class Spaceship:
    _energy: float
    _fuel: float
    _oxygen: float
    _energy_capacity: float = field(init=False)
    _fuel_capacity: float = field(init=False)
    _oxygen_capacity: float = field(init=False)

    def __post_init__(self):
        self._energy_capacity = self.getEnergy()
        self._fuel_capacity = self.getFuel()
        self._oxygen_capacity = self.getOxygen()

    def getEnergy(self) -> float:
        return self._energy

    def setEnergy(self, energy_consumed) -> None:
        if energy_consumed > self._energy:
            raise ValueError("Insufficient power for operation")

        self._energy -= energy_consumed

    def getFuel(self) -> float:
        return self._fuel

    def setFuel(self, fuel_consumed) -> None:
        if fuel_consumed > self._fuel:
            raise ValueError("Insufficient fuel for operation")

        self._fuel -= fuel_consumed

    def getOxygen(self) -> float:
        return self._oxygen

    def setOxygen(self, oxygen_consumed) -> None:
        if oxygen_consumed > self._oxygen:
            raise ValueError("Insufficient oxygen for operation")

        self._oxygen -= oxygen_consumed

    def __str__(self) -> str:
        energy_percentage = self._energy / self._energy_capacity * 100
        fuel_percentage = self._fuel / self._fuel_capacity * 100
        oxygen_percentage = self._oxygen / self._oxygen_capacity * 100

        return f"Spaceship status:\nEnergy: {energy_percentage:.1f}%\
            \nFuel: {fuel_percentage:.1f}%\nOxygen: {oxygen_percentage:.1f}%"
