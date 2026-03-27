import random


class DummyPPOTrainer:
    def train(self, episodes: int = 100):
        reward = 0.0
        for _ in range(episodes):
            reward += random.uniform(0, 1)
        return {"episodes": episodes, "avg_reward": reward / episodes}


if __name__ == "__main__":
    print(DummyPPOTrainer().train())
