import random as rnd

# Actions
# 0: No change
# 1: Turn right
#-1: Turn left

# Directions
# 0: Up
# 1: Right
# 2: Down
# 3: Left

class Player:
    
    def __init__(self, length, pos, direction, isHuman = False, name=None):
        self.name = name
        self.length = length
        self.pos = pos
        self.direction = direction
        self.isHuman = isHuman
        self.isDead = False
        
    def move(self):
        
        # move previous positions
        for i in range(self.length-1,0,-1):
            self.pos[i][0] = self.pos[i-1][0]
            self.pos[i][1] = self.pos[i-1][1]
            
        # move position of head of snake
        if self.direction == 0:
            self.pos[0][1] += -1
        if self.direction == 1:
            self.pos[0][0] += 1
        if self.direction == 2:
            self.pos[0][1] += 1
        if self.direction == 3:
            self.pos[0][0] += -1
            
                    
    def takeAction(self, gameState, humanAction=None):
        
        if self.isHuman:
            action = humanAction
        else:
            ### AI HERE
            action = rnd.randint(-1,1)
            
        print(self.name, action)
        
        # change direction of the head
        if self.direction == 3 and action == 1:
            self.direction = 0
        elif self.direction == 0 and action == -1:
            self.direction = 3
        else:
            self.direction = self.direction + action
            
        return action