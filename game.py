import pygame
import time
from random import randint

class Game():
    def __init__(self, app):
        self._app = app
        self._app.gm_isRunning = False


    def timeDiff(self, time1, time2):
        return time1 - time2

    async def game(self, duration=0):
        if(self._app.gm_isRunning):
            return
        pygame.init()
        W_W = 400
        W_H = 600
        screen = pygame.display.set_mode((W_W, W_H))
        pygame.display.set_caption('Falling raspberry [In game]')
        clock = pygame.time.Clock()
        self._app.gm_isRunning = True
        side_size = W_W // 4
        blocks = []
        curr_time = time.time()
        colors = {
            0 : (212, 66, 19),
            1 : (145, 173, 84)
        }
        score = 0
        speed = 3
        last_time_block = curr_time
        last_time_speed = curr_time
        start_time = curr_time
        while self._app.gm_isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._app.gm_isRunning = False
                elif event.type == pygame.KEYDOWN and len(blocks) > 0:
                    if event.key == pygame.K_a:
                        if blocks.pop(0)["color"] == 0:
                            score += 1
                        elif duration == 0:
                            self._app.gm_isRunning = False
                    elif event.key == pygame.K_d:
                        if blocks.pop(0)["color"] == 1:
                            score += 1
                        elif duration == 0:
                            self._app.gm_isRunning = False
                    print(score)

            screen.fill((39, 39, 39))

            for block in blocks:
                if block["height"] + side_size > W_H:
                    blocks.remove(block)
                else:
                    pygame.draw.rect(screen, colors[block["color"]], 
                                    pygame.Rect(block["column"] * side_size, block["height"], side_size, side_size))
                    block["height"] += speed

            pygame.display.flip()
            curr_time = time.time()
            if self.timeDiff(curr_time, last_time_block) >= 1:
                last_time_block = curr_time
                blocks.append({
                    "column" : randint(0, 3),
                    "height" : 0,
                    "color"  : randint(0,1)
                })
            if self.timeDiff(curr_time, last_time_speed) > 10:
                speed = min(speed + 1, 10)
                last_time_speed = curr_time
            if duration != 0 and self.timeDiff(curr_time, start_time) > duration:
                self._app.gm_isRunning = False
            clock.tick(60)
        curr_time = time.time()
        self._app.gm_isRunning = False
        pygame.quit()
        self._app.gm_myScore = score
        self._app.gm_duration = self.timeDiff(curr_time, start_time)
        return (score, self._app.gm_duration)
