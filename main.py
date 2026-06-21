import mesa
from dataclasses import dataclass

# データクラス
@dataclass
class RationalParams:
    """
        理性的パラメータ
    """
    engineering_knowledge: float

    @classmethod
    def random_params(cls, rng):
        return cls(
            engineering_knowledge=rng.random()
        )

@dataclass
class IntuitiveParams:
    """
        直感的パラメータ
    """
    car_speed: float

    @classmethod
    def random_params(cls, rng):
        return cls(
            car_speed=rng.random()
        )

@dataclass
class ParamsWeights:
    """
        パラメータの重み
    """
    # 理性的パラメータ
    engineering_knowledge_weight: float
    # 直感的パラメータ
    car_speed_weight: float

    def __post_init__(self):
        """
            重みの合計が１になっているかをチェックする
        """
        rational_params_total = self.engineering_knowledge_weight
        intuitive_params_total = self.car_speed_weight

        if round(rational_params_total, 5) != 1.0:
            raise ValueError(f"理性的パラメータの重みの合計が 1.0 ではありません。現在: {rational_params_total})")
        if round(intuitive_params_total, 5) != 1.0:
            raise ValueError(f"直感的パラメータの重みの合計が 1.0 ではありません。現在: {intuitive_params_total})")



class MyAgent(mesa.Agent):
    """
        エージェントクラス
        Args:
            system_responsibility_ratio(float): 責任判断の割合。０～１で、０が自動運転システムには責任がなく、１が完全に自動運転システムの責任。
    """
    def __init__(self, model):
        super().__init__(model)
        self.system_responsibility_ratio: float = None

        self.rational_params = RationalParams.random_params(self.random)
        self.intuitive_params = IntuitiveParams.random_params(self.random)

    def deliberative_judge(self):
        """
            熟考的判断
            returns:
                deliberative_judgment(float): 熟考的な責任判断。０～１で、０が自動運転システムには責任がなく、１が完全に自動運転システムの責任。
        """
        deliberative_judgment = self.rational_params.engineering_knowledge * self.model.weights.engineering_knowledge_weight
        deliberative_judgment /= self.model.weights.engineering_knowledge_weight

        return deliberative_judgment

    def reflexive_judge(self):
        """
            反射的判断
            returns:
                reflexive_judgment(float): 反射的な責任判断。０～１で、０が自動運転システムには責任がなく、１が完全に自動運転システムの責任。
        """
        reflexive_judgment = self.intuitive_params.car_speed * self.model.weights.car_speed_weight
        reflexive_judgment /= self.model.weights.car_speed_weight
        
        return reflexive_judgment
        
    def emotional_control(self):
        pass
    def social_influence(self):
        pass
    def provisional_judgment(self):
        pass
    def finalize_judgment(self):
        pass

    def step(self):
        print(f"理性的判断：{self.deliberative_judge()}")
        print(f"反射的判断：{self.reflexive_judge()}")


class MyModel(mesa.Model):
    """
        モデルクラス
    """
    def __init__(self, n_agents: int, weights: ParamsWeights):
        super().__init__()
        self.weights = weights

        # エージェントの生成
        for i in range(n_agents):
            agent = MyAgent(self)

    def step(self):
        self.agents.shuffle_do("step")

def main():
    weights = ParamsWeights(
        engineering_knowledge_weight = 1.0,
        car_speed_weight = 1.0
    )
    model = MyModel(n_agents=5, weights = weights)
    model.step()


if __name__ == "__main__":
    main()
