import pygame
from game import Game

class App:
    
    step = 10

    def __init__(self, n_players=1, n_human_players=1):
        self._dispaly_surf = None
        self._head_surf = None
        self._body_surf = None
        self._apple_surf = None
        self.game = Game(n_players, n_human_players)
        self.windowWidth = self.windowHeight = self.game.map_size * self.step
        
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        
        pygame.display.set_caption('Snakes')
        self._running = True
        self._head_surf = pygame.image.load("head.png").convert()
        self._body_surf = pygame.image.load("body.png").convert()
        self._apple_surf = pygame.image.load("apple.png").convert()
        
        
    def on_render(self):
        self._display_surf.fill((0,0,0))
        for p in self.game.players:
            self.draw_snake(self._display_surf, p)
        for a in self.game.apples:
            self.draw_apple(self._display_surf, a)
        pygame.display.flip()
        
    def draw_snake(self, surface, player):
        surface.blit(self._head_surf,(player.pos[0][0] * self.step, player.pos[0][1] * self.step))
        for i in range (1,player.length):
            surface.blit(self._body_surf,(player.pos[i][0] * self.step, player.pos[i][1] * self.step))
            
    def draw_apple(self, surface, apple):
        surface.blit(self._apple_surf,(apple.pos[0][0] * self.step, apple.pos[0][1] * self.step))
        
    def on_cleanup(self):
        pygame.quit()
        
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
            
        self.game.reset()
        
        while(self._running and not self.game.hasEnded):
            pygame.event.pump()
            pygame.time.delay(100)
            
            keys = pygame.key.get_pressed()
            
            if (keys[pygame.K_RIGHT]):
                humanActions = [1]
            elif (keys[pygame.K_LEFT]):
                humanActions = [-1]
            else:
                humanActions = [0]
                
            #ToDo: If multiple human players append here
               
            self.game.play(humanActions)
            self.on_render()
                
        self.on_cleanup()
        print('Game Over')
            
if __name__ == "__main__":
    theApp = App(10,0)
    theApp.on_execute()