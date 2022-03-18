import pygame
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pickle
import time
from random import seed
from random import randint
from PIL import Image
from matplotlib import style

style.use("ggplot")
HM_EPISODES = 500
COLLISION_PENALTY = 300
SCORE_REWARD = 25
epsilon = 0.43
EPS_DECAY = 0.999998
SHOW_EVERY = 10
start_q_table = None # for filename
LEARNING_RATE = 0.15
DISCOUNT = 0.93
episode_rewards = []
episode_reward = 0
run_reward = 0
# episode = 0
show = False
pass_obstacle = False
pass_obstacle_once = False
choice = 0
x_dist = 0
WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
HIGH_FPS = 600
LOW_FPS = 60
GRAVITY = 12
HITBOX_GROUND = (0, 350, 800, 650)
SC_MULTIPLIER = 1.1
OBSTACLES = [[800, 300, 50, 50], [800, 275, 50, 75], [800, 275, 50, 50], [800, 275, 50, 75], [800, 250, 50, 50]]
speed = 10
score = 0
jump = 0
target_fps = 60
duck = 0
show_obstacle = False
fps_mode = 0
seed(1)
grasses = []

for i in range(30):
    grass = [randint(0, 800), randint(350, 600)]
    grasses.append(grass)
    obstacle = OBSTACLES[0]
    run = True
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 20)
    SCREEN = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Dinosaur Knockoff by Hasif")

if start_q_table is None:
    q_table = {}
    for x in range(301):
        distance = x - 100
        for y in range(3):
            y_cor = (y * 25) + 250
            for height in range(2, 4):
                obs_height = height * 25
                q_table[(distance, y_cor, obs_height)] = [np.random.uniform(-5, -1) for act in range(0, 3)]
else:
    with open(start_q_table, "rb") as f:
        q_table = pickle.load(f)


def background():
    # Background
    bg_colour = (135, 206, 250)
    SCREEN.fill(bg_colour)
    ground_colour = (50, 205, 50)
    ground_shape = (0, 350, 800, 300)

    ground = pygame.draw.rect(SCREEN, color=ground_colour, rect=ground_shape)


def init_dino():
    # Dinosaur Block
    dino_colour = (218, 165, 32)
    dino_shape = (100, 300, 50, 50)
    dino = pygame.draw.rect(SCREEN, color=dino_colour, rect=dino_shape)
    return dino


def update_dino(dino):
    global run, jump, duck, obstacle, x_dist, run_reward, pass_obstacle, pass_obstacle_once
    duck_x = dino.size[0]
    duck_y = dino.size[1]
    x_dist = obstacle[0] - dino.x + duck_x
    if dino.x + duck_x > obstacle[0] and dino.x < obstacle[0] + obstacle[2]:
        if dino.y + duck_y > obstacle[1] and dino.y < obstacle[1] + obstacle[3]:
            run = False
            run_reward = -COLLISION_PENALTY
            obstacle[0] = 800
    elif obstacle[0] + obstacle[2] + 30 > dino.x > obstacle[0] + obstacle[2] + 40 and not pass_obstacle_once:
        pass_obstacle = True
        pass_obstacle_once = True

    if jump > 0:
        dino.move_ip(0, -1 * jump)
        jump -= 1

    if dino.y + 50 < HITBOX_GROUND[1] - 6:
        dino.move_ip(0, GRAVITY)
    elif dino.y + 50 < HITBOX_GROUND[1]:
        dino.move_ip(0, 2)

    if duck > 0:
        duck -= 5
        if dino.y == 300:
            dino.move_ip(-12, 25)

        duck_x = 75
        duck_y = 25
    elif dino.y > 300:
        dino.move_ip(6, -25)
        duck_x = 50
        duck_y = 50

    pygame.draw.rect(SCREEN, (218, 165, 32), (dino.x, dino.y, duck_x, duck_y))


def update_obstacle():
    global show_obstacle, obstacle, pass_obstacle_once
    if not show_obstacle:
        show_obstacle = True
        obstacle = OBSTACLES[randint(0, 4)]
    elif show_obstacle:
        if obstacle[0] > -50:
            obstacle[0] = round(obstacle[0] - speed)
            draw_grass = pygame.draw.rect(SCREEN, (220, 20, 60), (obstacle[0], obstacle[1], obstacle[2], obstacle[3]))
        elif obstacle[0] <= -50:
            obstacle[0] = 800
            show_obstacle = False
            pass_obstacle_once = False


def update_grass():
    global speed, grasses
    for i in range(len(grasses)):
        grasses[i][0] = round(grasses[i][0]-speed)
        draw_grass = pygame.draw.rect(SCREEN, (34, 139, 34), (grasses[i][0], grasses[i][1], 7, 15))
        if grasses[i][0] <= -7:
            grasses[i][0] = 800


def trigger(key_press, dino):
    global jump, duck, fps_mode, target_fps
    if key_press[pygame.K_UP] and dino.y+50 >= HITBOX_GROUND[1]:
        pass
    # jump = 27
    if key_press[pygame.K_DOWN] and (dino.y+50 == HITBOX_GROUND[1] or dino.y+25 == HITBOX_GROUND[1]):
        pass
    # duck = True

    if duck > 0 and dino.y+25 > HITBOX_GROUND[1]:
        dino.move_ip(0, -1)
    elif duck == 0 and dino.y+50 > HITBOX_GROUND[1]:
        dino.move_ip(0, -1)

    if key_press[pygame.K_SPACE]:
        if fps_mode == 0:
            fps_mode = 1
            target_fps = HIGH_FPS
        elif fps_mode == 1:
            fps_mode = 0
            target_fps = LOW_FPS


def action(choice, dino):
    global jump, duck
    if choice == 0:
        pass
    elif choice == 1 and dino.y+50 >= HITBOX_GROUND[1] and duck == 0:
        jump = 27
    elif choice == 2 and (dino.y+50 == HITBOX_GROUND[1] or dino.y+25 == HITBOX_GROUND[1]) and duck == 0:
        duck = 100


def main():
    global run, jump, duck, score, speed, show_obstacle, grasses, episode_rewards, show, episode_reward
    global run_reward, epsilon, choice, pass_obstacle, target_fps, fps_mode
    for episode in range(HM_EPISODES):
        if episode % 1 == 0:
            print(f"on # {episode}, epsilon: {epsilon}")
            print(f"{SHOW_EVERY} ep mean {np.mean(episode_rewards[-SHOW_EVERY:])}")
            show = True
        else:
            show = False

        episode_reward = 0
        score = 0
        speed = 10
        background()
        dino = init_dino()
        clock = pygame.time.Clock()
        timeout = 0
        run = True

        while run:
            clock.tick(target_fps)
            score += 1 * SC_MULTIPLIER
            score = round(score)
            if score % 200 == 0:
                speed += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if x_dist in range(-100, 201):
                if np.random.random() > epsilon:
                    choice = np.argmax(q_table[x_dist, obstacle[1], obstacle[3]])
                else:
                    choice = np.random.randint(0, 2)
            else:
                choice = 0

            action(choice, dino)
            key_press = pygame.key.get_pressed()
            trigger(key_press, dino)
            # print(speed)
            background()
            update_grass()
            update_dino(dino)
            update_obstacle()
            text_score = font.render('Score: ' + str(score), False, (0, 0, 0))
            SCREEN.blit(text_score, (10, 5))
            text_gen = font.render('Gen: ' + str(episode), False, (0, 0, 0))
            SCREEN.blit(text_gen, (11, 25))
            pygame.display.update()

            if score % 100 == 0:
                run_reward = round(score/100) * 10
            if pass_obstacle:
                run_reward = 100
            if x_dist in range(-100, 201):
                max_future_q = np.max(q_table[x_dist, obstacle[1], obstacle[3]])
                current_q = q_table[x_dist, obstacle[1], obstacle[3]][choice]
                if pass_obstacle:
                    new_q = run_reward
                    pass_obstacle = False
                if run_reward == round(score/100) * 10:
                    new_q = round(score/100) * 10
                elif run_reward == COLLISION_PENALTY:
                    new_q = SCORE_REWARD
                else:
                    new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (run_reward + DISCOUNT * max_future_q)
                    q_table[x_dist, obstacle[1], obstacle[3]][choice] = new_q

            if not show_obstacle:
                timeout += 1
            else:
                timeout = 0

        # episode_reward += run_reward

        if show:
            pygame.display.set_mode((800, 600))
        else:
            pygame.display.set_mode((1, 1))
            episode_rewards.append(score)
            epsilon *= EPS_DECAY
            print(f"Score: {score}")

    pygame.quit()
    plot_table()


def plot_table():
    score_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,)) / SHOW_EVERY, mode="valid")
    plt.plot([i for i in range(len(score_avg))], score_avg)
    plt.ylabel(f"rewards {SHOW_EVERY}")
    plt.xlabel(f"episode #")
    plt.show()
    with open(f"qtable-{int(time.time())}.pickle", "wb") as f:
        pickle.dump(q_table, f)


if __name__ == "__main__":
    main()