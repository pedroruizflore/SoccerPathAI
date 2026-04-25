from abc import ABC, abstractmethod

class Athlete(ABC):
    def __init__(self, name: str, team: str):
        self.name = name
        self.team = team

    @abstractmethod
    def get_role_metrics(self):
        pass

class Winger(Athlete):
    def get_role_metrics(self):
        return ["assists", "successful_dribbles", "crosses"]

class Fullback(Athlete):
    def get_role_metrics(self):
        return ["interceptions", "tackles", "crosses"]
    