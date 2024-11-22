import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
button_margin = 20
button_y_start = 400

# Danh sách nút
buttons = [
    ("Player", "Player"),
    ("Reinforcement Learning", "Reinforcement")
]

# Hàm vẽ nút
def draw_button(text, x, y):
    pygame.draw.rect(screen, BLUE, (x, y, button_width, button_height))
    pygame.draw.rect(screen, BLACK, (x, y, button_width, button_height), 5)  # Viền nút
    text_surface = font_button.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + button_width // 2, y + button_height // 2))
    screen.blit(text_surface, text_rect)

# Hàm bắt đầu trò chơi với chế độ được chọn
def start_game(mode):
    print(f"Bắt đầu trò chơi với chế độ: {mode}")

# Hàm xử lý sự kiện khi nhấn nút
def handle_click(mouse_pos):
    x, y = mouse_pos
    for i, (text, mode) in enumerate(buttons):
        button_y = button_y_start + i * (button_height + button_margin)
        if SCREEN_WIDTH // 2 - button_width // 2 < x < SCREEN_WIDTH // 2 + button_width // 2 and \
                button_y < y < button_y + button_height:
            start_game(mode)

# Hàm vẽ màn hình chính
def main_menu():
    screen.fill(BLACK)

    # Tiêu đề
    title_surface = font_title.render("Pacman Game", True, YELLOW)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_surface, title_rect)

    # Vẽ các nút
    for i, (text, mode) in enumerate(buttons):
        button_y = button_y_start + i * (button_height + button_margin)
        draw_button(text, SCREEN_WIDTH // 2 - button_width // 2, button_y)

    # Hiển thị tên người thực hiện
    names_surface = font_names.render("Nguyễn Trung Hiếu, Lê Hoàng Bảo Phúc, Lý Quang Vinh", True, WHITE)
    names_rect = names_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
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
                    handle_click(pygame.mouse.get_pos())

        main_menu()

    pygame.quit()
    sys.exit()

# Chạy vòng lặp chính
game_loop()
