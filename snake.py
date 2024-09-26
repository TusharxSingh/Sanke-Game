import pygame
import sys
import random

pygame.init()
pygame.display.set_caption("Snake Game")
pygame.font.init()


eat_sound = pygame.mixer.Sound('EAT1.wav')  
collision_sound = pygame.mixer.Sound('COLLISION.wav') 

SPEED = 0.1
SNAKE_SIZE = 20
APPLE_SIZE = SNAKE_SIZE
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
FPS = 15
KEY = {"UP": pygame.K_w, "DOWN": pygame.K_s, "LEFT": pygame.K_a, "RIGHT": pygame.K_d}
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

score_font = pygame.font.Font(None, 38)
game_over_font = pygame.font.Font(None, 48)
background_color = pygame.Color(0, 0, 0)

class Apple:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = pygame.Color("orange")

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, APPLE_SIZE, APPLE_SIZE))

class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self, x, y):
        self.direction = KEY["UP"]
        self.body = [Segment(x, y), Segment(x, y + SNAKE_SIZE), Segment(x, y + 2 * SNAKE_SIZE)]

    def move(self):
        head = self.body[0]
        new_head = Segment(head.x, head.y)
        if self.direction == KEY["UP"]:
            new_head.y -= SNAKE_SIZE
        elif self.direction == KEY["DOWN"]:
            new_head.y += SNAKE_SIZE
        elif self.direction == KEY["LEFT"]:
            new_head.x -= SNAKE_SIZE
        elif self.direction == KEY["RIGHT"]:
            new_head.x += SNAKE_SIZE

        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        tail = self.body[-1]
        new_segment = Segment(tail.x, tail.y)
        self.body.append(new_segment)

    def setDirection(self, direction):
        if (self.direction == KEY["RIGHT"] and direction == KEY["LEFT"]) or \
           (self.direction == KEY["LEFT"] and direction == KEY["RIGHT"]) or \
           (self.direction == KEY["UP"] and direction == KEY["DOWN"]) or \
           (self.direction == KEY["DOWN"] and direction == KEY["UP"]):
            return
        self.direction = direction

    def checkCollision(self):
        head = self.body[0]
        if head.x < 0 or head.x >= SCREEN_WIDTH or head.y < 0 or head.y >= SCREEN_HEIGHT:
            return True
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, pygame.Color("green"), (segment.x, segment.y, SNAKE_SIZE, SNAKE_SIZE))

def getKey():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key in KEY.values():
                return event.key
            if event.key == pygame.K_ESCAPE:
                sys.exit(0)
        if event.type == pygame.QUIT:
            sys.exit(0)

def endGame(score):
    message = game_over_font.render("Game Over", 1, pygame.Color("white"))
    restart_message = score_font.render("Press Y to Restart or N to Quit", 1, pygame.Color("white"))
    screen.fill(background_color)
    screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
    screen.blit(restart_message, (SCREEN_WIDTH // 2 - restart_message.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    main()
                elif event.key == pygame.K_n:
                    sys.exit(0)
            if event.type == pygame.QUIT:
                sys.exit(0)

def main():
    score = 0
    mySnake = Snake(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    apples = [Apple(random.randint(0, (SCREEN_WIDTH - APPLE_SIZE) // APPLE_SIZE) * APPLE_SIZE,
                    random.randint(0, (SCREEN_HEIGHT - APPLE_SIZE) // APPLE_SIZE) * APPLE_SIZE)]

    gameClock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    while True:
        gameClock.tick(FPS)
        keyPress = getKey()
        if keyPress:
            mySnake.setDirection(keyPress)

        mySnake.move()

        if mySnake.checkCollision():
            collision_sound.play()  
            endGame(score)

        head = mySnake.body[0]
        for myApple in apples:
            if head.x == myApple.x and head.y == myApple.y:
                mySnake.grow()  
                eat_sound.play() 
                score += 10
                apples[0] = Apple(random.randint(0, (SCREEN_WIDTH - APPLE_SIZE) // APPLE_SIZE) * APPLE_SIZE,
                                  random.randint(0, (SCREEN_HEIGHT - APPLE_SIZE) // APPLE_SIZE) * APPLE_SIZE)

        screen.fill(background_color)
        for myApple in apples:
            myApple.draw()

        mySnake.draw()
        score_display = score_font.render(f"Score: {score}", 1, pygame.Color("red"))
        timer_display = score_font.render(f"Time: {pygame.time.get_ticks() // 1000}", 1, pygame.Color("white"))
        screen.blit(score_display, (10, 10))
        screen.blit(timer_display, (SCREEN_WIDTH - timer_display.get_width() - 10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    main()
