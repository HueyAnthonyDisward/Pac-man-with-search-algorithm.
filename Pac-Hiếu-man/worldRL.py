import pygame
import time
import torch
import numpy as np
from settings import HEIGHT, WIDTH, NAV_HEIGHT, CHAR_SIZE, MAP
from pacRL import PacRL
from berry import Berry
from ghost import Ghost
from cell import Cell
from RlAgent import ReplayBuffer, DQN
from display import Display

class WorldRL:
    def __init__(self, screen):
        self.screen = screen
        self.player = pygame.sprite.GroupSingle()
        self.ghosts = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.berries = pygame.sprite.Group()
        self.display = Display(self.screen)
        self.game_over = False
        self.reset_pos = False
        self.player_score = 0
        self.game_level = 1

        # RL-specific components
        self.action_space = 4  # Số hành động: Trái, Phải, Lên, Xuống
        self.state_size = 10  # Kích thước của vector trạng thái
        self.q_network = DQN(self.state_size, self.action_space)
        self.target_network = DQN(self.state_size, self.action_space)
        self.replay_buffer = ReplayBuffer(10000)
        self.batch_size = 32
        self.gamma = 0.99
        self.optimizer = torch.optim.Adam(self.q_network.parameters(), lr=0.001)

        self._generate_world()


    def _generate_world(self):
        # Tạo các đối tượng trên bản đồ
        for y_index, col in enumerate(MAP):
            for x_index, char in enumerate(col):
                if char == "1":  # Tường
                    self.walls.add(Cell(x_index, y_index, CHAR_SIZE, CHAR_SIZE))
                elif char == " ":  # Berry nhỏ
                    self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 4))
                elif char == "B":  # Berry lớn (power-up)
                    self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 2, is_power_up=True))
                elif char == "s":
                    self.ghosts.add(Ghost(x_index, y_index, "skyblue"))
                elif char == "p":
                    self.ghosts.add(Ghost(x_index, y_index, "pink"))
                elif char == "o":
                    self.ghosts.add(Ghost(x_index, y_index, "orange"))
                elif char == "r":
                    self.ghosts.add(Ghost(x_index, y_index, "red"))
                elif char == "P":  # Pac-Man RL
                    self.player.add(PacRL(x_index, y_index, self.action_space))

        self.walls_collide_list = [wall.rect for wall in self.walls.sprites()]

    def step(self, action):
        """Thực hiện một hành động và trả về (trạng thái tiếp theo, phần thưởng, kết thúc)."""
        self.player.sprite.take_action(action, self.walls_collide_list)
        self.update()
        reward = self._calculate_reward()
        done = self.game_over
        next_state = self.player.sprite.get_state(self.walls, self.berries, self.ghosts)
        return next_state, reward, done

    def _calculate_reward(self):
        """Tính toán phần thưởng dựa trên trạng thái hiện tại."""
        reward = 0
        if len(self.berries) == 0:  # Ăn hết berries
            reward += 1000
        if self.reset_pos:  # Bị ma bắt
            reward -= 100
        if self.player.sprite.immune:  # Ăn được ma khi có power-up
            reward += 200
        return reward

    def train_step(self):
        """Thực hiện một bước huấn luyện trên replay buffer."""
        if len(self.replay_buffer) < self.batch_size:
            return

        # Lấy minibatch từ replay buffer
        batch = self.replay_buffer.sample(self.batch_size)
        states, actions, rewards, next_states, dones = map(np.array, zip(*batch))

        # Chuyển đổi dữ liệu sang tensor
        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.long)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        next_states = torch.tensor(next_states, dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.float32)

        # Dự đoán Q-values cho trạng thái hiện tại và tiếp theo
        q_values = self.q_network(states)
        next_q_values = self.target_network(next_states)

        # Chọn Q-value cho hành động đã thực hiện
        q_value = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)

        # Tính giá trị mục tiêu
        max_next_q_values = next_q_values.max(1)[0]
        target = rewards + self.gamma * max_next_q_values * (1 - dones)

        # Tính toán loss và cập nhật mạng nơ-ron
        loss = torch.nn.functional.mse_loss(q_value, target.detach())
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def update(self):
        if not self.game_over:
            self.player.sprite.update(self.walls_collide_list)  # Truyền walls_collide_list vào
            pac_position = self.player.sprite.get_position()

            # Cập nhật vị trí của Ghost
            for ghost in self.ghosts.sprites():
                ghost.update(self.walls_collide_list, pac_position)

        # Kiểm tra trạng thái trò chơi
        if len(self.berries) == 0:  # Chuyển sang level mới
            self.game_level += 1
            self.generate_new_level()

        if self.player.sprite.life <= 0:  # Kết thúc trò chơi
            self.game_over = True

        # Vẽ màn hình
        [wall.update(self.screen) for wall in self.walls.sprites()]
        [berry.update(self.screen) for berry in self.berries.sprites()]
        self.ghosts.draw(self.screen)
        self.player.draw(self.screen)
        self.display.game_over() if self.game_over else None

    def generate_new_level(self):
        """Tạo level mới với các berries được tái tạo."""
        self.berries.empty()
        for y_index, col in enumerate(MAP):
            for x_index, char in enumerate(col):
                if char == " ":
                    self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 4))
                elif char == "B":
                    self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 2, is_power_up=True))
        time.sleep(2)
