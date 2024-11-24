import random
import numpy as np
import pygame
from settings import CHAR_SIZE, PLAYER_SPEED, MAP, WIDTH, HEIGHT
from ghost import Ghost
from berry import Berry
from cell import Cell

class PacmanAgent:
    def __init__(self, map):
        self.map = map
        self.actions = ['up', 'down', 'left', 'right']
        self.q_table = np.zeros((len(map), len(map[0]), len(self.actions)))
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1
        self.position = (1, 1)

    def get_state(self):
        return self.position

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)
        else:
            state_x, state_y = state
            q_values = self.q_table[state_x][state_y]
            max_q_value = np.max(q_values)
            best_actions = [self.actions[i] for i in range(len(self.actions)) if q_values[i] == max_q_value]
            return random.choice(best_actions)

    def update_q_value(self, state, action, reward, next_state):
        state_x, state_y = state
        next_state_x, next_state_y = next_state
        action_index = self.actions.index(action)
        max_future_q = np.max(self.q_table[next_state_x][next_state_y])
        current_q = self.q_table[state_x][state_y][action_index]
        new_q = current_q + self.alpha * (reward + self.gamma * max_future_q - current_q)
        self.q_table[state_x][state_y][action_index] = new_q

    def move(self, action):
        x, y = self.position
        if action == 'up':
            self.position = (x - 1, y)
        elif action == 'down':
            self.position = (x + 1, y)
        elif action == 'left':
            self.position = (x, y - 1)
        elif action == 'right':
            self.position = (x, y + 1)

    def reset(self):
        self.position = (1, 1)

class PacmanEnvironment:
    def __init__(self):
        self.agent = PacmanAgent(MAP)
        self.ghosts = [Ghost(5, 5, 'red')]
        self.berries = [Berry(3, 3, 4)]
        self.map = MAP
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

    def get_reward(self, state):
        x, y = state
        for berry in self.berries:
            if (berry.abs_x == x * CHAR_SIZE) and (berry.abs_y == y * CHAR_SIZE):
                self.berries.remove(berry)
                return 10
        for ghost in self.ghosts:
            if ghost.get_position() == state:
                return -10
        return -1

    def step(self, action):
        state = self.agent.get_state()
        self.agent.move(action)
        new_state = self.agent.get_state()
        reward = self.get_reward(new_state)
        self.agent.update_q_value(state, action, reward, new_state)
        return new_state, reward

    def reset(self):
        self.agent.reset()
        return self.agent.get_state()

    def draw(self):
        self.screen.fill((0, 0, 0))  # Lấp đầy màn hình bằng màu đen

        # Vẽ Pacman
        pacman_x, pacman_y = self.agent.get_state()
        pygame.draw.rect(self.screen, (255, 255, 0), pygame.Rect(pacman_x * CHAR_SIZE, pacman_y * CHAR_SIZE, CHAR_SIZE, CHAR_SIZE))

        # Vẽ các ma
        for ghost in self.ghosts:
            ghost_x, ghost_y = ghost.get_position()
            pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(ghost_x * CHAR_SIZE, ghost_y * CHAR_SIZE, CHAR_SIZE, CHAR_SIZE))

        # Vẽ các quả Berry
        for berry in self.berries:
            berry_x, berry_y = berry.get_position()
            pygame.draw.circle(self.screen, (0, 255, 0), (berry_x * CHAR_SIZE + CHAR_SIZE // 2, berry_y * CHAR_SIZE + CHAR_SIZE // 2), CHAR_SIZE // 4)

        pygame.display.flip()  # Cập nhật màn hình

def train_agent():
    environment = PacmanEnvironment()
    for episode in range(1000):
        state = environment.reset()
        done = False
        while not done:
            action = environment.agent.choose_action(state)
            next_state, reward = environment.step(action)
            state = next_state
            environment.draw()  # Vẽ lại tất cả các thực thể sau mỗi bước
            if reward == 10 or reward == -10:  # Nếu ăn berry hoặc bị ma bắt
                done = True
            environment.clock.tick(10)  # Điều chỉnh tốc độ khung hình

if __name__ == "__main__":
    train_agent()
