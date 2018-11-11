import numpy as np
#import loggers as lg

map_shape = [25,25]

class Game:
    
    def __init__(self, players):
        self.players = players
        
        self.reset()
        
    def reset(self):
        self.mapa = np.zeros(map_shape, dtype=int)
        
    def takeAction(self, action):
        self.c = 3
        
    
class GameState:
    
    def __init__(self):
        self.a = 1
        
    def _convertStateToId(self):
        self.b = 2
        
    def takeAction(self, action):
        self.c = 3
        
    def render(self, logger=None):
        self.d = 4
        
    