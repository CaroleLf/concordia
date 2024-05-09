class God:
    god_name: str
    god_example: str
    god_significance: str
    god_reward: str
    god_victory_points: int

    def __init__(self,
                 p_god_name: str,
                 p_god_example: str,
                 p_god_significance: str,
                 p_god_reward: str,
                 p_god_victory_points: int):
        self.god_name = p_god_name
        self.god_example = p_god_example
        self.god_significance = p_god_significance
        self.god_reward = p_god_reward
        self.god_victory_points = p_god_victory_points
