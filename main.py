import mesa
from dataclasses import dataclass
import pandas as pd

# データクラス
@dataclass
class RationalParams:
    """
        理性的パラメータ
    """
    # エージェントの能力・知識
    philosophical_ability: float            # 哲学的能力
    metacognitive_ability: float            # メタ認知能力
    engineering_knowledge: float            # 工学知識
    ethical_knowledge: float                # 経済学知識
    legal_knowledge: float                  # 法学知識
    insurance_knowledge: float              # 保険知識

    # エージェントの倫理的価値観
    normative_ethical_orientation: float    # 規範倫理志向性
    moral_orientation: float                # 道徳的志向性

    # 事故状況に対する評価
    accident_foreseeability: float          # 事故の想定可能性
    accident_avoidability: float            # 事故の回避可能性
    duty_deviation: float                   # 義務の逸脱性

    # ドライバーとシステムの状態・認知限界
    driver_perception_scope: float          # ドライバーの認識範囲
    system_perception_scope: float          # システムの認識範囲
    driver_health_condition: float          # ドライバーの健康状態
    driver_health_condition: float          # 車の操作性

    # 外部環境
    road_conditions: float                  # 道路状況
    weather: float                          # 天候
    road_accident_frequency: float          # 道路の事故頻度



    @classmethod
    def random_params(cls, rng):
        return cls(
            philosophical_ability=rng.random(),
            metacognitive_ability=rng.random(),
            engineering_knowledge=rng.random(),
            ethical_knowledge=rng.random(),
            legal_knowledge=rng.random(),
            insurance_knowledge=rng.random(),
            normative_ethical_orientation=rng.random(),
            moral_orientation=rng.random(),
            accident_foreseeability=rng.random(),
            accident_avoidability=rng.random(),
            duty_deviation=rng.random(),
            driver_perception_scope=rng.random(),
            system_perception_scope=rng.random(),
            driver_health_condition=rng.random(),
            road_conditions=rng.random(),
            weather=rng.random(),
            road_accident_frequency=rng.random()
        )

@dataclass
class IntuitiveParams:
    """
        直感的パラメータ
    """
    # 状況コンテキスト
    car_speed: float                    # 車の速度
    # 個人の背景・属性
    car_affinity: float                 # 自動車愛好度
    tech_affinity: float                # 技術親和性
    driving_exp: float                  # 運転経験
    av_driving_exp: float               # 自動運転車の運転経験
    self_age: float                     # 自分の年齢
    # 過去の経験
    accident_exp_perpetrator: bool      # 事故経験（加害）
    accident_exp_victim: bool           # 事故経験（被害）
    violation_exp: bool                 # 違法行為の経験
    # 共感・価値観バイアス
    driver_age: float                   # ドライバーの年齢
    driver_similarity: float            # ドライバーとの類似性
    victim_similarity: float            # 被害者との類似性
    social_value_orientation: float     # 社会的価値観志向性



    @classmethod
    def random_params(cls, rng):
        return cls(
            car_speed=rng.random(),
            car_affinity=rng.random(),
            tech_affinity=rng.random(),
            driving_exp=rng.random(),
            av_driving_exp=rng.random(),
            self_age=rng.random(),
            accident_exp_perpetrator=rng.choice([True, False]),
            accident_exp_victim=rng.choice([True, False]),
            violation_exp=rng.choice([True, False]),
            driver_age=rng.random(),
            driver_similarity=rng.random(),
            victim_similarity=rng.random(),
            social_value_orientation=rng.random()
        )

@dataclass
class ParamsWeights:
    """
        パラメータの重み
    """
    # 理性的パラメータ
    philosophical_ability_weight: float
    metacognitive_ability_weight: float
    engineering_knowledge_weight: float
    ethical_knowledge_weight: float
    legal_knowledge_weight: float
    insurance_knowledge_weight: float
    normative_ethical_orientation_weight: float
    moral_orientation_weight: float
    accident_foreseeability_weight: float
    accident_avoidability_weight: float
    duty_deviation_weight: float
    driver_perception_scope_weight: float
    system_perception_scope_weight: float
    driver_health_condition_weight: float
    road_conditions_weight: float
    weather_weight: float
    road_accident_frequency_weight: float

    # 直感的パラメータ
    car_speed_weight: float
    car_affinity_weight: float
    tech_affinity_weight: float
    driving_exp_weight: float
    av_driving_exp_weight: float
    self_age_weight: float
    accident_exp_perpetrator_weight: float
    accident_exp_victim_weight: float
    violation_exp_weight: float
    driver_age_weight: float
    driver_similarity_weight: float
    victim_similarity_weight: float
    social_value_orientation_weight: float

    def __post_init__(self):
        """
            重みの合計が１になっているかをチェックする
        """
        rational_fields = [
            "philosophical_ability_weight", "metacognitive_ability_weight",
            "engineering_knowledge_weight", "ethical_knowledge_weight",
            "legal_knowledge_weight", "insurance_knowledge_weight",
            "normative_ethical_orientation_weight", "moral_orientation_weight",
            "accident_foreseeability_weight", "accident_avoidability_weight",
            "duty_deviation_weight", "driver_perception_scope_weight",
            "system_perception_scope_weight", "driver_health_condition_weight",
            "road_conditions_weight", "weather_weight", "road_accident_frequency_weight"
        ]

        intuitive_fields = [
            "car_speed_weight", "car_affinity_weight", "tech_affinity_weight",
            "driving_exp_weight", "av_driving_exp_weight", "self_age_weight",
            "accident_exp_perpetrator_weight", "accident_exp_victim_weight",
            "violation_exp_weight", "driver_age_weight", "driver_similarity_weight",
            "victim_similarity_weight", "social_value_orientation_weight"
        ]

        rational_params_total = sum(getattr(self, f) for f in rational_fields)
        intuitive_params_total = sum(getattr(self, f) for f in intuitive_fields)

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
        self.emotion_level = self.random.gauss(0.5, 0.15)
        self.emotion_level = max(0.0, min(1.0, self.emotion_level))

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
        """
            感情制御
            returns:
                emotional_level(float): 感情レベル。０～１で、０が感情が全くない状態、１が感情が非常に高い状態。
        """
        return self.emotion_level

    def social_influence(self):
        pass
    def provisional_judge(self):
        """
            暫定判断
            returns:
                provisional_judgment(float): 暫定的な責任判断。０～１で、０が自動運転システムには責任がなく、１が完全に自動運転システムの責任。
        """
        provisional_judgment = (self.deliberative_judge() * (1 - self.emotional_control())) + (self.reflexive_judge() * self.emotional_control())

        return provisional_judgment
    def finalize_judge(self):
        """
            最終判断
            returns:
                finalaize_judgment(float): 最終的な責任判断。０～１で、０が自動運転システムには責任がなく、１が完全に自動運転システムの責任。
        """
        finalize_judgment = self.provisional_judge()
        return finalize_judgment

    def step(self):
        self.deliberative_judgment = self.deliberative_judge()
        self.reflexive_judgment = self.reflexive_judge()
        self.provisional_judgment = self.provisional_judge()
        self.finalize_judgment = self.finalize_judge()



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

        # データコレクターの設定
        self.datacollector = mesa.DataCollector(
            agent_reporters={
                "理性的判断": "deliberative_judgment",
                "反射的判断": "reflexive_judgment",
                "暫定判断": "provisional_judgment",
                "最終判断": "finalize_judgment"
            }
        )

    def step(self):
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)

def main():
    weights = ParamsWeights(
        # 理性的パラメータの重み
        philosophical_ability_weight = 1.0/17,
        metacognitive_ability_weight = 1.0/17,
        engineering_knowledge_weight = 1.0/17,
        ethical_knowledge_weight = 1.0/17,
        legal_knowledge_weight = 1.0/17,
        insurance_knowledge_weight = 1.0/17,
        normative_ethical_orientation_weight = 1.0/17,
        moral_orientation_weight = 1.0/17,
        accident_foreseeability_weight = 1.0/17,
        accident_avoidability_weight = 1.0/17,
        duty_deviation_weight = 1.0/17,
        driver_perception_scope_weight = 1.0/17,
        system_perception_scope_weight = 1.0/17,
        driver_health_condition_weight = 1.0/17,
        road_conditions_weight = 1.0/17,
        weather_weight = 1.0/17,
        road_accident_frequency_weight = 1.0/17,
        # 反射的パラメータの重み
        car_speed_weight = 1.0/13,
        car_affinity_weight = 1.0/13,
        tech_affinity_weight = 1.0/13,
        driving_exp_weight = 1.0/13,
        av_driving_exp_weight = 1.0/13,
        self_age_weight = 1.0/13,
        accident_exp_perpetrator_weight = 1.0/13,
        accident_exp_victim_weight = 1.0/13,
        violation_exp_weight = 1.0/13,
        driver_age_weight = 1.0/13,
        driver_similarity_weight = 1.0/13,
        victim_similarity_weight = 1.0/13,
        social_value_orientation_weight = 1.0/13
    )
    model = MyModel(n_agents=5, weights = weights)
    for i in range(3):
        model.step()

    agent_data = model.datacollector.get_agent_vars_dataframe()
    print("\n=== 収集された全エージェントのデータ ===")
    print(agent_data)


if __name__ == "__main__":
    main()
