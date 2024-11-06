from ghost import Ghost
from Astar import a_star_search  # Import các class và hàm từ file ghost.py

def main():
    # Định nghĩa lưới (1 là không bị chặn, 0 là bị chặn)
    grid = [
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
        [1, 0, 1, 1, 1, 1, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 0, 0, 1]
    ]

    # Tọa độ Pacman
    pacman_position = [0, 0]

    # Khởi tạo ma
    ghost = Ghost(5, 0, 'red')

    # Di chuyển ma đến Pacman
    ghost.move_to_pacman(grid, pacman_position)

# Chạy hàm main khi file này được chạy trực tiếp
if __name__ == "__main__":
    main()
