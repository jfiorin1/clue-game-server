from enum import Enum

def __init__(self, players):
    self.num_players = players

class PlayerTurnManager:
    def __init__(self):
        pass

    def next_turn(self):
        raise NotImplementedError()

class PlayerTurn:
    def __init__(self):
        self.phase = TurnPhase.ROLL

    def next_phase(self):
        raise NotImplementedError()

    def skip_to_accuse(self):
        self.phase = TurnPhase.ACCUSE
        raise NotImplementedError()

class TurnPhase(Enum):
    ROLL = 0
    MOVE = 1
    SUGGEST = 2
    REFUTE = 3
    ACCUSE = 4