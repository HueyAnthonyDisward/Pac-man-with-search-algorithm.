import pygame
import random
from settings import WIDTH, CHAR_SIZE, GHOST_SPEED, MAP
from bfs import bfs_search

COLOR_NAMES = {
    (255, 0, 0, 255): "Red",
    (135, 206, 235, 255): "Sky Blue",
    (255, 192, 203, 255): "Pink",
    (255, 165, 0, 255): "Orange"
}


class Ghost(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        super().__init__()
        self.grid_row = row
        self.grid_col = col
        self.abs_x = row * CHAR_SIZE
        self.abs_y = col * CHAR_SIZE
        self.move_speed = GHOST_SPEED
        self.color = pygame.Color(color)
        self.color_name = COLOR_NAMES.get(self.color.normalize(), "Unknown Color")

        # Load và lưu các hình ảnh theo hướng
        self.img_path = f'assets/ghosts/{color}/'
        self.images = {
            'up': pygame.transform.scale(pygame.image.load(self.img_path + 'up.png'), (CHAR_SIZE, CHAR_SIZE)),
            'down': pygame.transform.scale(pygame.image.load(self.img_path + 'down.png'), (CHAR_SIZE, CHAR_SIZE)),
            'left': pygame.transform.scale(pygame.image.load(self.img_path + 'left.png'), (CHAR_SIZE, CHAR_SIZE)),
            'right': pygame.transform.scale(pygame.image.load(self.img_path + 'right.png'), (CHAR_SIZE, CHAR_SIZE)),
        }

        self.image = self.images['up']
        self.rect = self.image.get_rect(topleft=(self.abs_x, self.abs_y))
        self.mask = pygame.mask.from_surface(self.image)

        # Lưu vị trí trước và sau của ghost theo dạng hàng, cột
        self.previous_position = (self.grid_row, self.grid_col)
        self.current_position = (self.grid_row, self.grid_col)
        self.moving_dir = 'up'



    def _animate(self):
        self.image = self.images[self.moving_dir]
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

    def update(self, walls_collide_list, pacman_position, ghost_speed=GHOST_SPEED):
        start = (self.rect.y // CHAR_SIZE, self.rect.x // CHAR_SIZE)
        destination = (pacman_position[1] // CHAR_SIZE, pacman_position[0] // CHAR_SIZE)

        # Sử dụng BFS để tìm đường đến Pac-Man
        path = bfs_search(MAP, start, destination)

        if not path:  # Nếu không tìm thấy đường đi
            print(f"Ghost {self.color_name} could not find a path to Pac-Man.")
        else:
            if len(path) > 1:
                next_position = path[1]  # Lấy vị trí tiếp theo trong đường đi từ BFS
                dx, dy = (next_position[1] * CHAR_SIZE - self.rect.x), (next_position[0] * CHAR_SIZE - self.rect.y)

                # Cập nhật tốc độ di chuyển theo chiều ngang và dọc
                dx = ghost_speed if dx > 0 else -ghost_speed if dx < 0 else 0
                dy = ghost_speed if dy > 0 else -ghost_speed if dy < 0 else 0

                # Nếu không va chạm, di chuyển con ma
                if not self.is_collide(dx, dy, walls_collide_list):
                    self.rect.move_ip(dx, dy)  # Di chuyển con ma theo dx, dy đã tính toán
                    self.update_direction(dx, dy)
                else:
                    # Nếu có va chạm, thử di chuyển ít hơn hoặc thay đổi hướng
                    print(f"Ghost {self.color_name} is stuck at ({self.rect.x}, {self.rect.y})")
                    # Có thể thay đổi hướng hoặc di chuyển một đoạn ngắn hơn
                    if dx != 0:
                        dx = ghost_speed if dx > 0 else -ghost_speed
                    if dy != 0:
                        dy = ghost_speed if dy > 0 else -ghost_speed
                    self.rect.move_ip(dx, dy)  # Di chuyển con ma một bước nhỏ

            self._animate()

            # Cập nhật vị trí theo dạng hàng, cột
            self.current_position = (self.rect.y // CHAR_SIZE, self.rect.x // CHAR_SIZE)
            if self.current_position != self.previous_position:
                self.previous_position = self.current_position

    def is_collide(self, dx, dy, walls_collide_list):
        tmp_rect = self.rect.move(dx, dy)
        # Kiểm tra va chạm với tường
        return tmp_rect.collidelist(walls_collide_list) != -1

    def update_direction(self, dx, dy):
        if dx < 0:
            self.moving_dir = 'left'
        elif dx > 0:
            self.moving_dir = 'right'
        elif dy < 0:
            self.moving_dir = 'up'
        elif dy > 0:
            self.moving_dir = 'down'

    def move_to_start_pos(self):
        # Đặt ghost về vị trí ban đầu
        self.rect.x = self.abs_x
        self.rect.y = self.abs_y
        self.previous_position = (self.grid_row, self.grid_col)
        self.current_position = (self.grid_row, self.grid_col)

    def get_position(self):
        return self.current_position
