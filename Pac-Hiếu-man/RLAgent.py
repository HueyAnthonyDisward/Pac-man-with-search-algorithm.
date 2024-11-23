import numpy as np
import random

class RLAgent:
    def __init__(self, action_space, learning_rate=0.01, gamma=0.99, epsilon=1.0, epsilon_decay=0.995):
        self.action_space = action_space
        self.q_table = {}
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay

    def select_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(range(self.action_space))  # Hành động ngẫu nhiên
        state_key = tuple(state)
        return np.argmax(self.q_table.get(state_key, np.zeros(self.action_space)))  # Hành động tối ưu

    def store_transition(self, state, action, reward, next_state, done):
        state_key = tuple(state)
        next_state_key = tuple(next_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_space)

        # Tính giá trị cập nhật Q
        target = reward + self.gamma * np.max(self.q_table.get(next_state_key, np.zeros(self.action_space))) * (not done)
        self.q_table[state_key][action] += self.learning_rate * (target - self.q_table[state_key][action])

    def learn(self):
        self.epsilon *= self.epsilon_decay  # Giảm epsilon theo thời gian
