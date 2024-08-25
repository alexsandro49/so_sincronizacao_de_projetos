from enum import Enum


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
