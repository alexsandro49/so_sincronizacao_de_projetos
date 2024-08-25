from enum import Enum


class TaskType(Enum):
    COMMUNICATION = "Comunicação com a Terra"
    NAVIGATION = "Navegação"
    SAMPLE_COLLECTION = "Coleta de Amostras"
    SCIENTIFIC_ANALYSIS = "Análise Científica"
    LIFE_RESEARCH = "Pesquisa de Vida"
    TRAJECTORY_ADJUSTMENTS = "Ajustes de Trajetória"
