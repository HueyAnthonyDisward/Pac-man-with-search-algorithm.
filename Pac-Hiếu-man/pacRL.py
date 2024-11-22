from pac import Pac
import numpy as np

class PacRL(Pac):
    def __init__(self, row, col, action_space):
        super().__init__(row, col)
        self.action_space = action_space
        self.q_network = None
        self.current_state = None

    def update(self, walls_collide_list=None):
        """Cập nhật vị trí Pac-Man. Nếu walls_collide_list không được truyền, bỏ qua va chạm."""
        super().update()
        if walls_collide_list is not None:
            self.check_collision(walls_collide_list)

    def check_collision(self, walls_collide_list):
        """Kiểm tra và xử lý va chạm với tường."""
        for wall in walls_collide_list:
            if self.rect.colliderect(wall):
                self.handle_collision()

    def handle_collision(self):
        print("Pac-Man has collided with a wall!")

    def set_q_network(self, q_network):
        self.q_network = q_network

    def get_state(self, walls, berries, ghosts):
        """Tính toán trạng thái hiện tại của Pac-Man."""
        state = []
        state.extend(self.get_position())  # Vị trí Pac-Man
        state.extend([ghost.get_position() for ghost in ghosts])  # Vị trí ma
        state.extend([berry.rect.topleft for berry in berries])  # Vị trí Berry
        state.append(self.immune)  # Trạng thái Power-Up
        return np.array(state, dtype=np.float32)

    def take_action(self, action):
        """Thực hiện hành động dựa trên chỉ số hành động."""
        if action == 0:  # Trái
            self.direction = self.directions['left']
        elif action == 1:  # Phải
            self.direction = self.directions['right']
        elif action == 2:  # Lên
            self.direction = self.directions['up']
        elif action == 3:  # Xuống
            self.direction = self.directions['down']
