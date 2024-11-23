import pygame
import time
from settings import HEIGHT, WIDTH, NAV_HEIGHT, CHAR_SIZE, MAP
from pacRL import PacRL
from cell import Cell
from berry import Berry
from ghost import Ghost
from display import Display

class WorldRL:
    def __init__(self, screen, action_space):
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
        self.action_space = action_space
        self._generate_world()

    def _generate_world(self):
        """Tạo thế giới ban đầu từ bản đồ."""
        for y_index, col in enumerate(MAP):
            for x_index, char in enumerate(col):
                if char == "1":  # Tường
                    self.walls.add(Cell(x_index, y_index, CHAR_SIZE, CHAR_SIZE))
                elif char == " ":  # Đường đi chứa berries
                    self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 4))
                elif char == "B":  # Berry lớn
                    self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 2, is_power_up=True))
                elif char in "spro":  # Ghosts
                    color_map = {"s": "skyblue", "p": "pink", "r": "red", "o": "orange"}
                    self.ghosts.add(Ghost(x_index, y_index, color_map[char]))
                elif char == "P":  # Pac-Man
                    self.player.add(PacRL(x_index, y_index, self.action_space))

        self.walls_collide_list = [wall.rect for wall in self.walls.sprites()]

    def generate_new_level(self):
        """Tạo cấp độ mới."""
        for y_index, col in enumerate(MAP):
            for x_index, char in enumerate(col):
                if char == " ":  # Đường đi chứa berries
                    self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 4))
                elif char == "B":  # Berry lớn
                    self.berries.add(Berry(x_index, y_index, CHAR_SIZE // 2, is_power_up=True))
        time.sleep(2)

    def restart_level(self):
        """Khởi động lại cấp độ hiện tại."""
        self.berries.empty()
        [ghost.move_to_start_pos() for ghost in self.ghosts.sprites()]
        self.game_level = 1
        self.player.sprite.pac_score = 0
        self.player.sprite.life = 10
        self.player.sprite.move_to_start_pos()
        self.generate_new_level()

    def _check_game_state(self):
        """Kiểm tra trạng thái trò chơi."""
        if self.player.sprite.life <= 0:
            self.game_over = True
        elif len(self.berries) == 0 and self.player.sprite.life > 0:
            self.game_level += 1
            for ghost in self.ghosts.sprites():
                ghost.move_speed += self.game_level
                ghost.move_to_start_pos()
            self.player.sprite.move_to_start_pos()
            self.generate_new_level()

    def update(self, action=None):
        """Cập nhật trạng thái trò chơi và trả về state, reward, done."""
        if not self.game_over:
            if action is not None:
                # Thực hiện hành động RL
                reward = self.player.sprite.take_action(
                    action, self.walls_collide_list, self.berries.sprites(), self.ghosts.sprites()
                )
            else:
                reward = 0  # Không thực hiện hành động nếu `action` là None

            # Pac-Man ăn berries
            for berry in self.berries.sprites():
                if self.player.sprite.rect.colliderect(berry.rect):
                    if berry.power_up:
                        self.player.sprite.immune_time = 150  # Thời gian Power-Up
                        self.player.sprite.pac_score += 50
                    else:
                        self.player.sprite.pac_score += 10
                    berry.kill()

            # Pac-Man chạm vào Ghosts
            for ghost in self.ghosts.sprites():
                if self.player.sprite.rect.colliderect(ghost.rect):
                    if not self.player.sprite.immune:
                        self.player.sprite.life -= 1
                        self.reset_pos = True
                        break
                    else:
                        ghost.move_to_start_pos()
                        self.player.sprite.pac_score += 100

        pac_position = self.player.sprite.get_position()

        for ghost in self.ghosts.sprites():
            ghost.update(self.walls_collide_list, pac_position)

        # Kiểm tra trạng thái trò chơi
        self._check_game_state()

        # Cập nhật các đối tượng
        [wall.update(self.screen) for wall in self.walls.sprites()]  # Cập nhật tường (nếu có)
        [berry.update(self.screen) for berry in self.berries.sprites()]  # Cập nhật berries (nếu có)
        self.ghosts.update(self.walls_collide_list, pac_position)  # Cập nhật ma quái
        self.player.update()  # Cập nhật Pac-Man

        # Hiển thị thông tin lên màn hình
        self.display.show_life(self.player.sprite.life)
        self.display.show_level(self.game_level)
        self.display.show_score(self.player.sprite.pac_score)

        # Vẽ Ghosts lên màn hình
        self.ghosts.draw(self.screen)

        # Đặt lại vị trí khi Pac-Man bị bắt
        if self.reset_pos and not self.game_over:
            [ghost.move_to_start_pos() for ghost in self.ghosts.sprites()]
            self.player.sprite.move_to_start_pos()
            self.reset_pos = False

        # Kiểm tra nếu người chơi nhấn phím 'r' để khởi động lại sau khi game over
        if self.game_over:
            pressed_key = pygame.key.get_pressed()
            if pressed_key[pygame.K_r]:
                self.game_over = False
                self.restart_level()

        # Trả về state, reward và done
        done = self.game_over  # Trả về True nếu trò chơi kết thúc
        state = self.player.sprite.get_position()  # Hoặc một state nào đó từ game, ví dụ vị trí Pac-Man
        return state, reward, done



