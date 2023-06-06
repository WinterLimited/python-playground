# snake game을 만든다.
# 1. 뱀이 화면에 나타난다.
# 2. 뱀이 움직인다.
# 3. 뱀이 벽에 부딪히면 게임이 종료된다.
# 4. 뱀이 자기 자신의 몸에 부딪히면 게임이 종료된다.
# 5. 뱀이 먹이를 먹으면 뱀의 몸이 길어진다.
# 6. 뱀이 먹이를 먹으면 먹이가 다른 곳으로 이동한다.
# 7. 뱀이 먹이를 먹으면 점수가 1점 증가한다.
# 8. 뱀이 먹이를 먹으면 먹이가 다른 곳으로 이동한다.
# 8-1. 뱀이 다음 먹이를 일정 시간 내에 먹지 못하면 게임이 종료된다.
# 8-2. 일정시간은 새로 생성된 먹이와 뱀의 현재 위치에 비례한다.
# 8-3. 일정시간은 뱀의 현재 길이에 반비례한다.
# 8-4. 일정시간의 공식은 일정시간 = (새로 생성된 먹이와 뱀의 현재 위치 사이의 거리) - (뱀의 현재 길이) 로 한다
# 8-4. 일정시간은 1초마다 1씩 감소한다.
# 8-5. 일정시간이 0이 되면 게임이 종료된다.
# 9. 게임 종료 후 점수를 알려준다.
# 10. 게임 종료 후 다시 시작할 수 있다. (y/n)
# 11. 게임 종료 후 다시 시작할 때 뱀의 길이가 초기화된다.
# 12. 게임 종료 후 다시 시작할 때 뱀의 위치가 초기화된다.
# 13. 게임 종료 후 다시 시작할 때 먹이의 위치가 초기화된다.
# 14. 게임 종료 후 다시 시작할 때 점수가 초기화된다.
# 15. 게임 종료 후 다시 시작할 때 뱀의 방향이 초기화된다.
# github에 올린다.

import pygame
import random
import sys
import os

# 전역변수로 사용할 상수를 정의한다.
# 화면의 크기를 정의한다.
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# 뱀의 크기를 정의한다.
SNAKE_SIZE = 10

# 뱀의 초기 위치를 정의한다.
snake = [[100, 100], [110, 100], [120, 100]]

# 뱀의 초기 방향을 정의한다.
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
direction = DOWN

# 뱀의 색상을 정의한다.
snake_skin = pygame.Surface((SNAKE_SIZE, SNAKE_SIZE))
snake_skin.fill((255, 255, 255))

# 먹이의 색상을 정의한다.
apple_skin = pygame.Surface((SNAKE_SIZE, SNAKE_SIZE))
apple_skin.fill((255, 0, 0))

# 먹이의 초기 위치를 정의한다.
apple_pos = [random.randint(0, 59) * 10, random.randint(0, 59) * 10]

# pygame을 초기화한다.
pygame.init()

# 화면을 설정한다.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 화면의 타이틀을 설정한다.
pygame.display.set_caption('Snake')

# 게임의 FPS를 설정한다.
fps = pygame.time.Clock()

# 게임의 점수를 설정한다.
score = 0

# 남은 시간을 설정한다.
time = 60

TIME_TICK = pygame.USEREVENT + 1
pygame.time.set_timer(TIME_TICK, 1000)

# 필요 함수들을 정의한다.
# 뱀이 화면에 나타나는 것을 구현한다.
def draw_snake():
    for pos in snake:
        screen.blit(snake_skin, pos)

# 뱀이 움직이는 것을 구현한다.
def move_snake():
    global snake
    # 뱀의 머리 위치를 복사합니다.
    head_pos = list(snake[0])

    # 뱀의 머리가 움직이는 방향에 따라 뱀의 머리 위치를 변경합니다.
    if direction == UP:
        head_pos[1] -= 10
    elif direction == DOWN:
        head_pos[1] += 10
    elif direction == LEFT:
        head_pos[0] -= 10
    elif direction == RIGHT:
        head_pos[0] += 10

    # 뱀의 머리 위치를 뱀의 몸통 부분의 앞에 추가합니다.
    snake.insert(0, head_pos)

    # 뱀의 꼬리 부분을 제거합니다.
    if not check_eat():
        snake.pop()


# 뱀이 벽에 부딪히면 게임이 종료되는 것을 구현한다.
# 게임이 종료되면 종료 함수를 호출한다.
def check_game_over():
    if snake[0][0] < 0 or snake[0][0] > SCREEN_WIDTH - 10:
        return True
    elif snake[0][1] < 0 or snake[0][1] > SCREEN_HEIGHT - 10:
        return True

    for i in range(1, len(snake) - 1):
        if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
            return True
        
    if time <= 0:
        return True

    return False

# 뱀이 먹이를 먹으면 뱀의 몸이 길어지는 것을 구현한다.
def check_eat():
    global apple_pos
    global score
    global time

    if snake[0][0] == apple_pos[0] and snake[0][1] == apple_pos[1]:
        snake.append([0, 0])
        apple_pos = [random.randint(0, 59) * 10, random.randint(0, 59) * 10]
        score += 1
        
        # 뱀과 먹이 사이의 거리를 구하는 것을 구현한다.
        distance = abs(snake[0][0] - apple_pos[0]) + abs(snake[0][1] - apple_pos[1])

        # 남은 시간을 구하는 것을 구현한다.
        # TODO: score가 높아짐에 따라 남은 시간 내에 다음 먹이를 먹을 수 없는 경우에 대한 예외처리 필요.
        time = distance / 15 - score

# 남은 시간을 1초마다 갱신하는 것을 구현한다.
def update_time():
    global time
    time -= 1

# 뱀이 먹이를 먹으면 먹이가 다른 곳으로 이동하는 것을 구현한다.
def draw_food():
    screen.blit(apple_skin, apple_pos)

# 뱀이 다음 먹이를 먹을 때까지 남은 시간을 출력하는 것을 구현한다.
# 남은 시간을 갱신하는 것을 어떻게 구현할 수 있을까? -> 점수를 이용한다. 구체적인 방법은 아래에 정의한다.
def show_time(pos, color, font, size):
    time_font = pygame.font.SysFont(font, size)
    # time의 출력은 정수로 한다.
    time_surface = time_font.render('Time : ' + str(int(time)), True, color)
    time_rect = time_surface.get_rect()
    time_rect.midtop = pos
    screen.blit(time_surface, time_rect)

# 뱀이 먹이를 먹으면 점수가 1점 증가하는 것을 구현한다.
def show_score(pos, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    score_rect.midtop = pos
    screen.blit(score_surface, score_rect)

# 게임 종료 시에 점수를 출력하는 것을 구현한다.
def game_over():
    global score

    score_font = pygame.font.SysFont('malgungothic', 72)
    score_surface = score_font.render('Score : ' + str(score), True, (255, 255, 255))
    score_rect = score_surface.get_rect()
    score_rect.midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    screen.blit(score_surface, score_rect)
    
    pygame.display.update()

    restart_or_end()

# 게임을 다시 시작하거나 종료하는 것을 구현한다.
# 아무 키를 누르면 게임을 다시 시작하고, ESC 키를 누르면 게임을 종료한다.
# 아무 키를 누르면 게임을 다시 시작하고, ESC 키를 누르면 게임을 종료하는 설명을 Score 위에 출력한다.
def restart_or_end():
    global score

    # 재시작 설명을 출력한다.
    restart_font = pygame.font.SysFont('malgungothic', 24)
    # 영어로 출력
    restart_surface = restart_font.render('Press any key to restart the game.', True, (255, 255, 255))
    restart_rect = restart_surface.get_rect()
    restart_rect.midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.5)
    screen.blit(restart_surface, restart_rect)

    # 종료 설명을 출력한다.
    end_font = pygame.font.SysFont('malgungothic', 24)
    # 영어로 출력
    end_surface = end_font.render('Press ESC key to end the game.', True, (255, 255, 255))
    end_rect = end_surface.get_rect()
    end_rect.midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.3)
    screen.blit(end_surface, end_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # 이 부분을 추가해주세요.

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()  # 이 부분을 추가해주세요.
                else:
                    score = 0
                    main()

# 게임의 메인 루프로 이동하는 것을 구현한다.
def main():
    global direction
    global snake
    global apple_pos
    global score
    global time

    direction = RIGHT
    snake = [[200, 200], [210, 200], [220, 200]]
    apple_pos = [random.randint(0, 59) * 10, random.randint(0, 59) * 10]
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # 이 부분을 추가해주세요.

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = UP
                elif event.key == pygame.K_DOWN:
                    direction = DOWN
                elif event.key == pygame.K_LEFT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    direction = RIGHT

            if event.type == TIME_TICK:
                time -= 1

        # 뱀이 움직이는 것을 구현한다.
        move_snake()

        # 뱀이 벽에 부딪히면 게임이 종료되는 것을 구현한다.
        if check_game_over():
            game_over()

        # 뱀이 먹이를 먹으면 뱀의 몸이 길어지는 것을 구현한다.
        screen.fill((0, 0, 0))

        # 뱀이 먹이를 먹으면 먹이가 다른 곳으로 이동하는 것을 구현한다.
        draw_snake()

        # 뱀이 먹이를 먹으면 점수가 1점 증가하는 것을 구현한다.
        draw_food()

        # 뱀이 다음 먹이를 먹을 때까지 남은 시간을 출력하는 것을 구현한다.
        show_time((SCREEN_WIDTH / 2, 10), (255, 255, 255), 'malgungothic', 20)

        # 게임 종료 시에 점수를 출력하는 것을 구현한다.
        show_score((50, 10), (255, 255, 255), 'malgungothic', 20)

        # 화면을 업데이트한다.
        pygame.display.update()

        # 게임의 FPS를 설정한다.
        fps.tick(10)

main()