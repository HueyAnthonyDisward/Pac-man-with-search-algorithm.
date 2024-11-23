import pygame
from settings import CHAR_SIZE, PLAYER_SPEED
from animation import import_sprite
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim


STATE_DIM = 2 + (2 * 4) + 3
class PacRL(pygame.sprite.Sprite):
    def __init__(self, row, col, action_space):
        super().__init__()

        # Vị trí ban đầu
        self.initial_x = (row * CHAR_SIZE)
        self.initial_y = (col * CHAR_SIZE)
        self.abs_x = self.initial_x
        self.abs_y = self.initial_y
        self.rect = pygame.Rect(self.initial_x, self.initial_y, CHAR_SIZE, CHAR_SIZE)
        self.image = pygame.Surface((CHAR_SIZE, CHAR_SIZE))
        self.image.fill((255, 255, 0))  # Màu vàng tượng trưng cho Pac-Man
        self.visited_positions = set()  # Tập hợp để lưu các vị trí đã đi qua
        self.total_score = 0

        # Hoạt ảnh
        self._import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.5
        self.current_animation = self.animations["idle"]



        # Di chuyển và trạng thái
        self.speed = PLAYER_SPEED
        self.directions = {
            0: (-PLAYER_SPEED, 0),  # Trái
            1: (PLAYER_SPEED, 0),   # Phải
            2: (0, -PLAYER_SPEED),  # Lên
            3: (0, PLAYER_SPEED)    # Xuống
        }
        self.direction = (0, 0)
        self.status = "idle"

        # RL liên quan
        self.action_space = action_space
        self.q_network = None  # Placeholder cho mạng Q nếu sử dụng DQN hoặc tương tự

        # Thuộc tính Pac-Man
        self.immune_time = 0
        self.immune = False
        self.life = 3
        self.pac_score = 0
        self.previous_position = (self.rect.x, self.rect.y)

        self.q_network = nn.Sequential(
            nn.Linear(STATE_DIM, 128),
            nn.ReLU(),
            nn.Linear(128, action_space)
        )
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.q_network.to(self.device)

    def save_model(self, file_path="pac_rl_model.pth"):
        """Lưu mô hình RL vào tệp .pth."""
        torch.save(self.q_network.state_dict(), file_path)
        print(f"Model saved to {file_path}")

    def _import_character_assets(self):
        character_path = "assets/pac/"
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "idle": [],
            "power_up": []
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_sprite(full_path)

    def animate(self, pressed_key, walls_collide_list):
        """Xử lý chuyển động và hoạt ảnh của Pac-Man"""
        animation = self.animations[self.status]
        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale(image, (CHAR_SIZE, CHAR_SIZE))
        self.walls_collide_list = walls_collide_list

        for key, key_value in self.keys.items():
            if pressed_key[key_value] and not self._is_collide(*self.directions[key]):
                self.direction = self.directions[key]
                self.status = key if not self.immune else "power_up"
                break

        if not self._is_collide(*self.direction):
            self.rect.move_ip(self.direction)
            self.status = self.status if not self.immune else "power_up"
            if (self.rect.x, self.rect.y) != self.previous_position:
                self.previous_position = (self.rect.x, self.rect.y)
                self.position = (self.rect.x, self.rect.y)  # Cập nhật lại tọa độ thực tế
                self.log_position()

        if self._is_collide(*self.direction):
            self.status = "idle" if not self.immune else "power_up"

    def load_model(self, file_path="pac_rl_model.pth"):
        """Tải mô hình RL từ tệp .pth."""
        try:
            self.q_network.load_state_dict(torch.load(file_path, map_location=self.device))
            print(f"Model loaded from {file_path}")
        except FileNotFoundError:
            print(f"No saved model found at {file_path}. Starting fresh.")

    def _import_character_assets(self):
        """Nhập tài sản hình ảnh Pac-Man."""
        character_path = "assets/pac/"
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "idle": [],
            "power_up": []
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_sprite(full_path)

    def reset_position(self):
        """Đặt lại Pac-Man về vị trí ban đầu."""
        self.rect.x = self.initial_x
        self.rect.y = self.initial_y
        self.previous_position = (self.rect.x, self.rect.y)

    def get_position(self):
        """Trả về vị trí hiện tại của Pac-Man."""
        return self.rect.x, self.rect.y

    def update_immune_status(self):
        """Cập nhật trạng thái miễn dịch."""
        self.immune = True if self.immune_time > 0 else False
        self.immune_time -= 1 if self.immune_time > 0 else 0

    def animate(self):
        """Cập nhật hình ảnh Pac-Man dựa trên trạng thái."""
        animation = self.current_animation
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = pygame.transform.scale(animation[int(self.frame_index)], (CHAR_SIZE, CHAR_SIZE))

    def get_state(self, walls, berries, ghosts):
        """Tính toán trạng thái hiện tại của Pac-Man."""
        state = []
        state.extend(self.get_position())  # Vị trí Pac-Man
        state.extend([ghost.get_position() for ghost in ghosts])  # Vị trí ma
        state.extend([berry.rect.topleft for berry in berries])  # Vị trí Berry
        state.append(self.immune)  # Trạng thái Power-Up
        return np.array(state, dtype=np.float32)

    def calculate_reward(self, berries, ghosts):
        """
        Tính toán phần thưởng dựa trên trạng thái hiện tại.
        :param berries: Danh sách các berry (quả ăn được).
        :param ghosts: Danh sách các ma (ghosts).
        :return: reward (phần thưởng tại trạng thái hiện tại).
        """
        reward = 0
        current_position = (self.rect.x, self.rect.y)

        # Kiểm tra nếu đi đến ô mới
        if current_position not in self.visited_positions:
            reward += 10
            self.visited_positions.add(current_position)
        else:
            reward -= 10  # Đi lại ô cũ

        # Kiểm tra nếu ăn berry lớn
        for berry in berries:
            if self.rect.colliderect(berry.rect):  # Pac-Man ăn được berry
                reward += 100
                berries.remove(berry)  # Loại berry ra khỏi danh sách

        # Kiểm tra nếu bị ma bắt
        for ghost in ghosts:
            if self.rect.colliderect(ghost.rect):  # Pac-Man chạm phải ghost
                reward -= 100
                self.reset_position()  # Đưa Pac-Man về vị trí ban đầu

        self.total_score += reward  # Cộng dồn điểm vào tổng điểm của mạng
        return reward

    def end_game(self):
        """Hàm được gọi khi kết thúc một mạng."""
        print(f"Game Over! Total Score: {self.total_score}")
        # Reset tổng điểm sau khi kết thúc mạng
        self.total_score = 0

    def take_action(self, action, walls_collide_list, berries, ghosts):
        """
        Thực hiện hành động dựa trên RL agent và tính toán phần thưởng.
        :param action: Chỉ số hành động (0, 1, 2, 3 tương ứng với Trái, Phải, Lên, Xuống).
        :param walls_collide_list: Danh sách các vật thể tường để kiểm tra va chạm.
        :param berries: Danh sách các berry (quả ăn được).
        :param ghosts: Danh sách các ma (ghosts).
        :return: reward (phần thưởng cho hành động).
        """
        self.direction = self.directions[action]
        future_position = self.rect.move(self.direction[0], self.direction[1])

        # Kiểm tra va chạm với tường
        if any(future_position.colliderect(wall) for wall in walls_collide_list):
            self.direction = (0, 0)  # Không di chuyển nếu va chạm
        else:
            self.rect = future_position  # Di chuyển nếu không va chạm

        # Tính toán phần thưởng
        reward = self.calculate_reward(berries, ghosts)

        if self.life <= 0:
            self.end_game()
            # Cập nhật trạng thái
        self.previous_position = (self.rect.x, self.rect.y)
        return reward

    def log_position(self):
        """Ghi lại vị trí hiện tại của Pac-Man."""
        print(f"Pac-Man's current position: ({self.rect.x}, {self.rect.y})")

    def update_state(self, action, walls_collide_list):
        """
        Cập nhật Pac-Man theo hành động RL và trạng thái miễn dịch.
        :param action: Hành động RL (0, 1, 2, 3).
        :param walls_collide_list: Danh sách tường để kiểm tra va chạm.
        """
        self.update_immune_status()
        self.take_action(action, walls_collide_list)
        self.animate()

    def move_to_start_pos(self):
        """Di chuyển Pac-Man về vị trí ban đầu"""
        self.rect.x = self.abs_x
        self.rect.y = self.abs_y
        self.previous_position = (self.rect.x, self.rect.y)
        self.position = (self.rect.x, self.rect.y)  # Cập nhật lại tọa độ thực tế
        self.log_position()
