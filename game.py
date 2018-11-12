import random as rnd
import numpy as np
from player import Player


class Game:
    
    map_size = 100
    initial_length = 3
    n_apples = 10
    
    def __init__(self, n_players, n_human_players):
        self.n_players = n_players
        self.n_human_players = n_human_players
        self.players = []
        self.apples = []
        self.gameState = None
        
    def play(self, humanActions=[]):
        
        actions = []
        for p in self.players:
            ## <Ugly POG>
            if p.isHuman:
                this_humanAction = humanActions[int(p.name[-1])-1]
                actions.append(p.takeAction(self.gameState, this_humanAction))
            else:
            ## </Ugly POG>
                actions.append(p.takeAction(self.gameState))
        
        self.gameState = self.step(actions)
        return self.hasEnded
            
    def step(self, actions):
        
        for p in self.players:
            p.move()
            
        for p in self.players:
            
            # Does it hit the wall?
            if p.pos[0][0] < 0 or p.pos[0][1] < 0 or p.pos[0][0] >= self.map_size or p.pos[0][1] >= self.map_size:
                # Die
                p.isDead = True
                
            for p2 in self.players:
                # Does it hit a snake's body?
                for i in range(1,p2.length):
                    if (p.pos[0][0] == p2.pos[i][0]) and (p.pos[0][1] == p2.pos[i][1]):
                        # Die
                        p.isDead = True
                # Does it hit another snake's head?
                ## ToDo
                        
            # Does it get an apple?
            for a in self.apples:
                if (p.pos[0][0] == a.pos[0][0]) and (p.pos[0][1] == a.pos[0][1]):
                    # Eat the apple
                    a.isEaten = True
                    p.length += 1
                    p.pos.append([p.pos[-1][0],p.pos[-1][1]])
            
            
        for p in self.players:
            if p.isDead:
                self.players.remove(p)
                
        for a in self.apples:
            if a.isEaten:
                self.apples.remove(a)
                self.spawnApple()
                
        if len(self.players) == 0:
            # End of game
            self.hasEnded = True
        
        gameState = GameState(self.map_size, self.players, self.apples)
        return gameState
        
    def reset(self):
        
        self.hasEnded = False
        
        for i in range(self.n_players):
            initial_pos = [
                    [rnd.randint(self.initial_length,self.map_size-self.initial_length), 
                    rnd.randint(self.initial_length,self.map_size-self.initial_length)]
                    ]
            initial_direction = rnd.randint(0,3)
            for j in range (1,self.initial_length):
                
                if initial_direction == 0: #Head looking up, body goes down
                    initial_pos.append([
                            initial_pos[j-1][0],
                            initial_pos[j-1][1] + 1
                            ])
                if initial_direction == 3: #Head looking down, body goes up
                    initial_pos.append([
                            initial_pos[j-1][0],
                            initial_pos[j-1][1] - 1
                            ])
                if initial_direction == 1: #Head looking right, body goes left
                    initial_pos.append([
                            initial_pos[j-1][0] - 1,
                            initial_pos[j-1][1]
                            ])
                if initial_direction == 2: #Head looking left, body goes right
                    initial_pos.append([
                            initial_pos[j-1][0] + 1,
                            initial_pos[j-1][1]
                            ])

                
            if i < self.n_human_players:
                isHuman = True
            else:
                isHuman = False
            
            name = 'Player_' + str(i)
            self.players.append(Player(self.initial_length, initial_pos, initial_direction, isHuman, name))
            
        for i in range(self.n_apples):
            self.spawnApple()
        
        self.gameState = GameState(self.map_size, self.players, self.apples)
        
    def spawnApple(self):
        
        aux_gameState = GameState(self.map_size, self.players, self.apples)
        
        if 0 not in aux_gameState.gameMap:
            return 1

        appleIn = False
        while not appleIn:
            pos = [[rnd.randint(0,self.map_size-1),rnd.randint(0,self.map_size-1)]]
            if aux_gameState.gameMap[pos[0][0], pos[0][1]] == 0:
                self.apples.append(Apple(pos))
                appleIn = True
                
        return 0
    
    
class GameState:
    
    # Legend
    # 0: Empty space
    # 1: Body
    # 2: Head
    # 3: Apple
    
    def __init__(self, map_size, players, apples):
        self.gameMap = np.zeros([map_size,map_size], dtype=int)
        
        for a in apples:
            self.gameMap[a.pos[0][0],a.pos[0][1]] = 3
            
        for p in players:
            self.gameMap[p.pos[0][0]][p.pos[0][1]] = 2
            for i in range(1,p.length):
                self.gameMap[p.pos[i][0]][p.pos[i][1]] = 1
                
    def getLayers(self):
        
        layers = None
        layers[0] = self.gameMap == 1
        layers[1] = self.gameMap == 2
        layers[2] = self.gameMap == 3
        
        return layers

class Apple:
    
    def __init__(self, pos):
        self.pos = pos
        self.isEaten = False