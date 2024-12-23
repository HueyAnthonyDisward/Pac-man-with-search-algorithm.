import pygame
import random
from settings import WIDTH, CHAR_SIZE, GHOST_SPEED, MAP
from bfs import bfs_search
from bestfs import best_first_search
from Astar import a_star_search
from ids import ids_search
from Local import simulated_annealing
from dfs import dfs_search
from AC3 import backtrack_with_ac3
COLOR_NAMES = {
    (255, 0, 0): "Red",
    (135, 206, 235): "Sky Blue",
    (255, 192, 203): "Pink",
    (255, 165, 0): "Orange"
}


class Ghost(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        super().__init__()
        self.grid_row = row
        self.grid_col = col
        self.abs_x = row * CHAR_SIZE
        self.abs_y = col * CHAR_SIZE
        self.move_speed = GHOST_SPEED

        # Chuyển đổi màu thành tuple RGB
        self.color = pygame.Color(color)[:3]
        self.color_name = COLOR_NAMES.get(self.color, "Unknown Color")


        if self.color_name == "Unknown Color":
            print(f"Unknown color for Ghost: {self.color}")

        # Đường dẫn hình ảnh dựa trên tên màu
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

        self.previous_position = (self.grid_row, self.grid_col)
        self.current_position = (self.grid_row, self.grid_col)
        self.moving_dir = 'up'


    def _animate(self):
        self.image = self.images[self.moving_dir]
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

    def update(self, walls_collide_list, pacman_position, ghost_speed=GHOST_SPEED):
        # Xác định vị trí bắt đầu (con ma) và đích (Pacman)
        start = (self.rect.y // CHAR_SIZE, self.rect.x // CHAR_SIZE)
        destination = (pacman_position[1] // CHAR_SIZE, pacman_position[0] // CHAR_SIZE)


        if self.color_name == "Red":
            path = best_first_search(MAP, start, destination)
            ghost_speed *= 1
        elif self.color_name == "Sky Blue":
            path = ids_search(MAP, start, destination)
            ghost_speed *= 1
        elif self.color_name == "Orange":
            path = simulated_annealing(MAP, start, destination)
            ghost_speed *= 1
        elif self.color_name == "Pink":
            path = backtrack_with_ac3(MAP, start, destination)
            ghost_speed *= 1
            #if path:
                #print(f"Pink Ghost Path: {path}")  # In đường đi của ma màu Pink

        # Kiểm tra nếu không tìm thấy đường đi
        if not path:
            print(f"Ghost {self.color_name} could not find a path to Pac-Man.")
        else:
            if len(path) > 1:
                # Lấy vị trí tiếp theo trên đường đi và tính toán khoảng cách
                next_position = path[1] #path[1] là đường tiếp theo
                target_x, target_y = next_position[1] * CHAR_SIZE, next_position[0] * CHAR_SIZE
                dx = target_x - self.rect.x # xy của ô tiếp theo trừ đi hiện tại
                dy = target_y - self.rect.y

                # dx dy > 0 thì ma đi theo hướng mục tiêu, nếu âm thì đi ngược lại
                move_x = ghost_speed if dx > 0 else -ghost_speed if dx < 0 else 0
                move_y = ghost_speed if dy > 0 else -ghost_speed if dy < 0 else 0


                # Kiểm tra di chuyển trục x trước xem co va vào tường không, nếu không thì di chuyển và cập nhật hướng
                if move_x != 0 and not self.is_collide(move_x, 0, walls_collide_list):
                    self.rect.move_ip(move_x, 0)
                    self.update_direction(move_x, 0)
                elif move_y != 0 and not self.is_collide(0, move_y, walls_collide_list): # không được x thì đi theo trục y
                    self.rect.move_ip(0, move_y)
                    self.update_direction(0, move_y)
                else:
                    # Nếu không thể di chuyển theo cả hai trục, thử bước di chuyển nhỏ hơn
                    if dx != 0 and not self.is_collide(dx // 2, 0, walls_collide_list):
                        self.rect.move_ip(dx // 2, 0)
                    elif dy != 0 and not self.is_collide(0, dy // 2, walls_collide_list):
                        self.rect.move_ip(0, dy // 2)
                    else:
                        print(f"Ghost {self.color_name} is stuck at ({self.rect.x}, {self.rect.y})")

                # Cập nhật hình ảnh và vị trí
                self._animate()
                self.current_position = (self.rect.y // CHAR_SIZE, self.rect.x // CHAR_SIZE)
                if self.current_position != self.previous_position:
                    self.previous_position = self.current_position

    #Kiểm tra va chạm(-1)
    def is_collide(self, dx, dy, walls_collide_list):
        tmp_rect = self.rect.move(dx, dy)
        return tmp_rect.collidelist(walls_collide_list) != -1


    #dựa vào dấu của dx và dy để quyết định hướng
    def update_direction(self, dx, dy):
        if dx < 0:
            self.moving_dir = 'left'
        elif dx > 0:
            self.moving_dir = 'right'
        elif dy < 0:
            self.moving_dir = 'up'
        elif dy > 0:
            self.moving_dir = 'down'

    #Đi về vị trí đầu khi bị solokill
    def move_to_start_pos(self):

        self.rect.x = self.abs_x
        self.rect.y = self.abs_y
        self.previous_position = (self.grid_row, self.grid_col)
        self.current_position = (self.grid_row, self.grid_col)

    #Lấy vị trí hiện tại
    def get_position(self):
        return self.current_position