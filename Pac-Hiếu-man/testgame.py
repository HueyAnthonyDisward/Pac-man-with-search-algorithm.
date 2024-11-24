import torch
import pygame
import numpy as np
import random
import os


MODEL_PATH = "q_table.pth"
# Kích thước của mỗi ô trong bản đồ
CELL_SIZE = 21
# Kích thước màn hình
WIDTH, HEIGHT = 600, 600

# Map mà bạn đã cung cấp
MAP = [
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
    ['1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1'],
    ['1', 'B', '1', '1', ' ', '1', '1', '1', ' ', '1', ' ', '1', '1', '1', ' ', '1', '1', 'B', '1'],
    ['1', ' ', ' ', ' ', ' ', '1', ' ', ' ', ' ', '1', ' ', ' ', ' ', '1', ' ', ' ', ' ', ' ', '1'],
    ['1', '1', ' ', '1', ' ', '1', ' ', '1', ' ', '1', ' ', '1', ' ', '1', ' ', '1', ' ', '1', '1'],
    ['1', ' ', ' ', '1', ' ', ' ', ' ', '1', ' ', ' ', ' ', '1', ' ', ' ', ' ', '1', ' ', ' ', '1'],
    ['1', ' ', '1', '1', '1', '1', ' ', '1', '1', '1', '1', '1', ' ', '1', '1', '1', '1', ' ', '1'],
    ['1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'r', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1'],
    ['1', '1', ' ', '1', '1', '1', ' ', '1', '1', '-', '1', '1', ' ', '1', '1', '1', ' ', '1', '1'],
    [' ', ' ', ' ', ' ', ' ', '1', ' ', '1', 's', 'p', 'o', '1', ' ', '1', ' ', ' ', ' ', ' ', ' '],
    ['1', '1', ' ', '1', ' ', '1', ' ', '1', '1', '1', '1', '1', ' ', '1', ' ', '1', ' ', '1', '1'],
    ['1', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1', ' ', ' ', '1'],
    ['1', ' ', '1', '1', '1', '1', ' ', '1', '1', '1', '1', '1', ' ', '1', '1', '1', '1', ' ', '1'],
    ['1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1'],
    ['1', '1', '1', ' ', '1', '1', '1', ' ', '1', '1', '1', ' ', '1', '1', '1', ' ', '1', '1', '1'],
    ['1', ' ', ' ', ' ', '1', ' ', ' ', ' ', ' ', 'P', ' ', ' ', ' ', ' ', '1', ' ', ' ', ' ', '1'],
    ['1', 'B', '1', ' ', '1', ' ', '1', ' ', '1', '1', '1', ' ', '1', ' ', '1', ' ', '1', 'B', '1'],
    ['1', ' ', '1', ' ', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', '1', ' ', ' ', ' ', '1', ' ', '1'],
    ['1', ' ', '1', '1', '1', ' ', '1', '1', '1', ' ', '1', '1', '1', ' ', '1', '1', '1', ' ', '1'],
    ['1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '1'],
    ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']
]

# Các ký tự đại diện cho các vật thể trong game
WALL = '1'
BERRY = 'B'
PACMAN = 'P'
ENEMY = ['r', 'P', 's', 'O']

# Khởi tạo pygame
pygame.init()

# Kích thước cửa sổ
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman Q-Learning")

# Tải hình ảnh cho Pacman, các con ma và quả berry
pacman_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
pacman_img.fill((255, 255, 0))  # Màu vàng cho Pacman

enemy_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
enemy_img.fill((255, 0, 0))  # Màu đỏ cho các con ma

berry_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
berry_img.fill((0, 255, 0))  # Màu xanh cho quả berry


# Lớp môi trường (Environment)
class PacmanEnv:
    def __init__(self, map_data):
        self.map = map_data
        self.state = self.reset()
        self.visited = set()  # Set lưu trữ các ô đã được đi qua
        self.ghost_positions = self.find_ghost_positions()

    def reset(self):
        # Tìm vị trí Pacman và ghost trên bản đồ
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == PACMAN:
                    self.pacman_pos = (x, y)
                    return (x, y)
        return None

    def find_ghost_positions(self):
        positions = []
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell in ENEMY:
                    positions.append((x, y))
        return positions

    def move_ghosts(self):
        new_positions = []
        for ghost_pos in self.ghost_positions:
            x, y = ghost_pos
            action = random.choice([0, 1, 2, 3])  # Chọn hành động ngẫu nhiên
            if action == 0:  # lên
                new_pos = (x, y - 1)
            elif action == 1:  # xuống
                new_pos = (x, y + 1)
            elif action == 2:  # trái
                new_pos = (x - 1, y)
            elif action == 3:  # phải
                new_pos = (x + 1, y)

            # Chỉ di chuyển ghost nếu vị trí hợp lệ
            if (
                0 <= new_pos[1] < len(self.map)
                and 0 <= new_pos[0] < len(self.map[0])
                and self.map[new_pos[1]][new_pos[0]] not in [WALL, BERRY, PACMAN]
            ):
                new_positions.append(new_pos)
                self.map[y][x] = ' '  # Xóa vị trí cũ
                self.map[new_pos[1]][new_pos[0]] = 'r'  # Cập nhật vị trí mới
            else:
                new_positions.append(ghost_pos)  # Nếu không di chuyển được, giữ nguyên vị trí
        self.ghost_positions = new_positions

    def step(self, action):
        x, y = self.pacman_pos
        if action == 0:  # lên
            new_pos = (x, y - 1)
        elif action == 1:  # xuống
            new_pos = (x, y + 1)
        elif action == 2:  # trái
            new_pos = (x - 1, y)
        elif action == 3:  # phải
            new_pos = (x + 1, y)

        # Kiểm tra di chuyển hợp lệ
        if (
                new_pos[1] < 0 or new_pos[1] >= len(self.map) or
                new_pos[0] < 0 or new_pos[0] >= len(self.map[0]) or
                self.map[new_pos[1]][new_pos[0]] == WALL
        ):
            return self.state, -1, False


        self.pacman_pos = new_pos
        self.state = new_pos
        reward = 0

        # Ăn quả berry
        if self.map[new_pos[1]][new_pos[0]] == BERRY:
            reward += 100
            print(f"Pacman ate a berry! Reward: {reward}")
            self.map[new_pos[1]][new_pos[0]] = ' '

        # Thưởng/Phạt khi đi qua ô đã ghé thăm
        if new_pos in self.visited:
            reward -= 1
        else:
            self.visited.add(new_pos)

        # Cập nhật vị trí Pacman trên bản đồ
        self.map[y][x] = ' '  # Xóa vị trí cũ
        self.map[new_pos[1]][new_pos[0]] = PACMAN

        # Di chuyển ghost
        self.move_ghosts()

        # Kiểm tra va chạm giữa Pacman và ghost
        if new_pos in self.ghost_positions:
            reward += -100
            return self.state, reward, False

        return self.state, reward, True

    def render(self):
        screen.fill((0, 0, 0))

        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == WALL:
                    pygame.draw.rect(screen, (0, 0, 255), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                elif cell == BERRY:
                    screen.blit(berry_img, (x * CELL_SIZE, y * CELL_SIZE))
                elif cell == PACMAN:
                    screen.blit(pacman_img, (x * CELL_SIZE, y * CELL_SIZE))
                elif cell in ENEMY:
                    screen.blit(enemy_img, (x * CELL_SIZE, y * CELL_SIZE))

        pygame.display.flip()



# Q-Learning Agent
class QLearningAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}

    def get_state_key(self, state):
        return f"{state[0]}_{state[1]}"

    def choose_action(self, state):
        state_key = self.get_state_key(state)
        if random.uniform(0, 1) < self.epsilon or state_key not in self.q_table:
            return random.choice(self.actions)
        return max(self.actions, key=lambda action: self.q_table[state_key][action])

    def update_q_table(self, state, action, reward, next_state):
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = {a: 0 for a in self.actions}
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {a: 0 for a in self.actions}

        old_value = self.q_table[state_key][action]
        next_max = max(self.q_table[next_state_key].values())
        self.q_table[state_key][action] = old_value + self.alpha * (reward + self.gamma * next_max - old_value)

    def save_model(self, path):
        torch.save(self.q_table, path)

    def load_model(self, path):
        self.q_table = torch.load(path)


# Training Loop
actions = [0, 1, 2, 3]  # Các hành động: lên, xuống, trái, phải
agent = QLearningAgent(actions)
env = PacmanEnv(MAP)
total_reward_all_episodes = 0
# Training 500 episodes
for episode in range(500):
    state = env.reset()
    done = False
    total_reward = 0

    while not done:
        action = agent.choose_action(state)
        next_state, reward, done = env.step(action)
        agent.update_q_table(state, action, reward, next_state)
        state = next_state
        total_reward += reward

        # Render game environment every 10 episodes
        if episode % 10 == 0:
            pygame.time.wait(300)
            env.render()
    total_reward_all_episodes += total_reward
    print(f"Episode {episode + 1}: Total Reward = {total_reward}, Total all: {total_reward_all_episodes}")

# Save the trained Q-Table
agent.save_model("q_table.pth")

print("Training completed and model saved!")

# Quit pygame after rendering
pygame.quit()
