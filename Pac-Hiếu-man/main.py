import pygame
import sys
from settings import WIDTH, HEIGHT, NAV_HEIGHT
from world import World
from worldRL import WorldRL

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
screen = pygame.display.set_mode((WIDTH, HEIGHT + NAV_HEIGHT))
pygame.display.set_caption("Pacman Game")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Phông chữ
font_title = pygame.font.SysFont("Times New Roman", 50, bold=True)
font_button = pygame.font.SysFont("Times New Roman", 30)
font_names = pygame.font.SysFont("Times New Roman", 20)

# Vị trí nút
button_width = 400
button_height = 50
button_margin = 30  # Tăng khoảng cách giữa các nút
button_y_start = 200  # Chuyển vị trí khởi đầu xuống dưới màn hình

# Danh sách nút
buttons = [
    ("Player", "Player"),
    ("Reinforcement Learning", "Reinforcement")
]

# Lớp Main cho chế độ Player
# Lớp Main cho chế độ Player
class Main:
    def __init__(self, screen):
        self.screen = screen
        self.FPS = pygame.time.Clock()

    def main(self):
        world = World(self.screen)  # Sử dụng World cho chế độ Player
        while True:
            self.screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            world.update()  # Gọi hàm update của lớp World
            pygame.display.update()
            self.FPS.tick(30)

# Lớp Main cho chế độ Reinforcement Learning
class ReinforcementMain:
    def __init__(self, screen):
        self.screen = screen
        self.FPS = pygame.time.Clock()

    def main(self):
        world_rl = WorldRL(self.screen)  # Sử dụng WorldRL cho chế độ Reinforcement Learning
        while True:
            self.screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            world_rl.update()  # Gọi hàm update của lớp WorldRL
            pygame.display.update()
            self.FPS.tick(30)


# Hàm vẽ nút
def draw_button(text, x, y):
    pygame.draw.rect(screen, BLUE, (x, y, button_width, button_height))
    pygame.draw.rect(screen, BLACK, (x, y, button_width, button_height), 5)  # Viền nút
    text_surface = font_button.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + button_width // 2, y + button_height // 2))
    screen.blit(text_surface, text_rect)

# Hàm bắt đầu chế độ Player
def start_player_mode():
    play = Main(screen)  # Khởi tạo Main cho chế độ Player
    play.main()

# Hàm bắt đầu chế độ Reinforcement Learning
def start_reinforcement_mode():
    reinforcement = ReinforcementMain(screen)  # Khởi tạo ReinforcementMain
    reinforcement.main()


# Hàm xử lý sự kiện khi nhấn nút
def handle_click(mouse_pos):
    x, y = mouse_pos
    for i, (text, mode) in enumerate(buttons):
        button_y = button_y_start + i * (button_height + button_margin)
        if WIDTH // 2 - button_width // 2 < x < WIDTH // 2 + button_width // 2 and \
                button_y < y < button_y + button_height:
            if mode == "Player":
                start_player_mode()  # Chạy chế độ Player
            elif mode == "Reinforcement":
                start_reinforcement_mode()  # Chạy chế độ Reinforcement Learning


# Hàm vẽ màn hình chính
def main_menu():
    screen.fill(BLACK)

    # Tiêu đề
    title_surface = font_title.render("Pacman Game", True, YELLOW)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title_surface, title_rect)

    # Vẽ các nút
    for i, (text, mode) in enumerate(buttons):
        button_y = button_y_start + i * (button_height + button_margin)
        draw_button(text, WIDTH // 2 - button_width // 2, button_y)

    # Hiển thị tên người thực hiện
    names_surface = font_names.render("Nguyễn Trung Hiếu, Lê Hoàng Bảo Phúc, Lý Quang Vinh", True, WHITE)
    names_rect = names_surface.get_rect(center=(WIDTH // 2, HEIGHT + NAV_HEIGHT - 50))
    screen.blit(names_surface, names_rect)

    pygame.display.flip()

# Vòng lặp chính
def game_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Kiểm tra nếu là click chuột trái
                    handle_click(pygame.mouse.get_pos())  # Xử lý sự kiện click

        main_menu()  # Hiển thị màn hình chính

    pygame.quit()
    sys.exit()

# Chạy vòng lặp chính
game_loop()
