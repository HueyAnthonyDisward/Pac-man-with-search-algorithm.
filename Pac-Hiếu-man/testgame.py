import pygame
import numpy as np
import random

# Kích thước của mỗi ô trong bản đồ
CELL_SIZE = 30
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
ENEMY = ['r', 'P', 'S', 'O']

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

    def reset(self):
        # Tìm vị trí Pacman trên bản đồ
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell == PACMAN:
                    self.pacman_pos = (x, y)
                    return (x, y)
        return None

    def step(self, action):
        # Di chuyển Pacman theo hành động và trả về trạng thái mới
        x, y = self.pacman_pos
        if action == 0:  # lên
            new_pos = (x, y - 1)
        elif action == 1:  # xuống
            new_pos = (x, y + 1)
        elif action == 2:  # trái
            new_pos = (x - 1, y)
        elif action == 3:  # phải
            new_pos = (x + 1, y)

        # Kiểm tra nếu new_pos ra ngoài bản đồ hoặc là tường
        if new_pos[1] < 0 or new_pos[1] >= len(self.map) or new_pos[0] < 0 or new_pos[0] >= len(self.map[0]) or self.map[new_pos[1]][new_pos[0]] == WALL:
            return self.state, 0, False  # Nếu không di chuyển được, không thay đổi trạng thái

        self.pacman_pos = new_pos
        self.state = new_pos
        reward = 0

        # Kiểm tra nếu Pacman ăn berry
        if self.map[new_pos[1]][new_pos[0]] == BERRY:
            reward = 1
            self.map[new_pos[1]][new_pos[0]] = ' '  # Xóa quả berry

        return self.state, reward, False  # Trả lại trạng thái mới và phần thưởng

    def move_ghosts(self):
        # Di chuyển ngẫu nhiên các con ma
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if cell in ENEMY:
                    new_pos = self.random_move(x, y)
                    if self.map[new_pos[1]][new_pos[0]] != WALL and self.map[new_pos[1]][new_pos[0]] != PACMAN:
                        self.map[y][x] = ' '  # Xóa con ma cũ
                        self.map[new_pos[1]][new_pos[0]] = cell  # Cập nhật vị trí con ma

    def random_move(self, x, y):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Di chuyển lên, xuống, trái, phải
        random_direction = random.choice(directions)
        return (x + random_direction[0], y + random_direction[1])


# Hàm hiển thị game
def draw_game(env):
    screen.fill((0, 0, 0))  # Màu nền đen

    # Vẽ map
    for y, row in enumerate(env.map):
        for x, cell in enumerate(row):
            if cell == WALL:
                pygame.draw.rect(screen, (0, 0, 255),
                                 pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Màu xanh cho tường
            elif cell == BERRY:
                screen.blit(berry_img, (x * CELL_SIZE, y * CELL_SIZE))  # Vẽ berry
            elif cell == PACMAN:
                screen.blit(pacman_img, (x * CELL_SIZE, y * CELL_SIZE))  # Vẽ Pacman
            elif cell in ENEMY:
                screen.blit(enemy_img, (x * CELL_SIZE, y * CELL_SIZE))  # Vẽ con ma

    pygame.display.flip()


# Q-learning setup
class QLearningAgent:
    def __init__(self, env, actions):
        self.env = env
        self.actions = actions
        self.q_table = np.zeros(
            (len(env.map), len(env.map[0]), len(actions)))  # Q-table với các trạng thái và hành động
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 1.0
        self.exploration_decay = 0.995

    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.choice(self.actions)  # Khám phá (exploration)
        else:
            return np.argmax(self.q_table[state[1], state[0], :])  # Tận dụng (exploitation)

    def learn(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state[1], next_state[0], :])
        td_target = reward + self.discount_factor * self.q_table[next_state[1], next_state[0], best_next_action]
        td_error = td_target - self.q_table[state[1], state[0], action]
        self.q_table[state[1], state[0], action] += self.learning_rate * td_error


# Khởi tạo môi trường và agent
env = PacmanEnv(MAP)
agent = QLearningAgent(env, actions=[0, 1, 2, 3])

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    action = agent.choose_action(env.state)
    next_state, reward, done = env.step(action)
    agent.learn(env.state, action, reward, next_state)
    env.state = next_state

    # Di chuyển ma
    env.move_ghosts()

    draw_game(env)

    # Đợi một chút để game không quá nhanh
    pygame.time.delay(100)

    # Kiểm tra các sự kiện (ví dụ như nhấn nút thoát)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    agent.exploration_rate *= agent.exploration_decay  # Giảm tỷ lệ khám phá theo thời gian

pygame.quit()
