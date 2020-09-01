from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


author = 'Tomo OKADA'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'delegation_part1'
    players_per_group = 2
    num_rounds = 10  # ラウンド数
    endowment = c(100)
    timeout = models.IntegerField()
    instructions_template = 'delegation_part1/Instructions.html'
    cost_k = (0.01, 0.02)

    # ラウンドナンバー管理用（あとでデータを見てどのラウンドと紐づいているかわかるように...）
    #! 実験中に何らかの弾みでサーバがリロードされると再度ラウンドがランダマイズされるので、本番ではnumには何らかの定数を入れておく方が良い。
    num = random.random()
    round_index = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    random.seed(num)
    random.shuffle(round_index)

    # コストシートの色の決定(そのラウンドのコストが青のシートならTrue, 黄色のシートならFalse)
    is_cost_blue = [False, False, False, False, False, True, True, True, True, True]
    random.seed(num)
    random.shuffle(is_cost_blue)

    # 自分にとって望ましいプロジェクトが成功した時の、各ラウンドの報酬
    list_principal_when_success_a = [220.1, 280.2, 180.3, 220.4, 260.5, 440.6, 560.7, 360.8, 440.9, 520.0]
    list_agent_when_success_b = [220.1, 280.2, 180.3, 220.4, 260.5, 440.6, 560.7, 360.8, 440.9, 520.0]
    random.seed(num)
    random.shuffle(list_principal_when_success_a)
    random.seed(num)
    random.shuffle(list_agent_when_success_b)

    # 自分にとって望ましくないプロジェクトが成功した時の、各ラウンドの報酬
    list_agent_when_success_a = [190.1, 235.2, 140.3, 160.4, 260.5, 380.6, 470.7, 280.8, 320.9, 520.0]
    list_principal_when_success_b = [190.1, 235.2, 140.3, 160.4, 260.5, 380.6, 470.7, 280.8, 320.9, 520.0]
    random.seed(num)
    random.shuffle(list_agent_when_success_a)
    random.seed(num)
    random.shuffle(list_principal_when_success_b)

    # プロジェクトが失敗した時の、各ラウンドの報酬
    list_when_fail_a = [100.1, 100.2, 100.3, 100.4, 100.5, 200.6, 200.7, 200.8, 200.9, 200.0]
    list_when_fail_b = [100.1, 100.2, 100.3, 100.4, 100.5, 200.6, 200.7, 200.8, 200.9, 200.0]
    random.seed(num)
    random.shuffle(list_when_fail_a)
    random.seed(num)
    random.shuffle(list_when_fail_b)


class Subsession(BaseSubsession):

    # 役割を固定して各ラウンドでランダムマッチング
    # todo これでラウンドごとにマッチングし直すせるかは要検証。ダメならShuffling during the sessionを試す。
    def creating_session(self):
        self.group_randomly(fixed_id_in_group=True)

    is_cost_blue = Constants.is_cost_blue

    def cost_blue(self):
        return Constants.is_cost_blue[self.round_number - 1]

    # 各プロジェクトの報酬（ラウンド番号の管理）
    def round_index(self):
        return Constants.round_index[self.round_number - 1]

    # 各プロジェクトの報酬

    def agent_when_success_a(self):
        return Constants.list_agent_when_success_a[self.round_number - 1]

    def principal_when_success_a(self):
        return Constants.list_principal_when_success_a[self.round_number - 1]

    def agent_when_success_b(self):
        return Constants.list_agent_when_success_b[self.round_number - 1]

    def principal_when_success_b(self):
        return Constants.list_principal_when_success_b[self.round_number - 1]

    def when_fail_a(self):
        return Constants.list_when_fail_a[self.round_number - 1]

    def when_fail_b(self):
        return Constants.list_when_fail_b[self.round_number - 1]


class Group(BaseGroup):
    # プロジェクト選択
    agent_project_choice = models.IntegerField()

    principal_project_choice = models.IntegerField(
        choices=[[1, 'プロジェクトA'], [2, 'プロジェクトB']],
        widget=widgets.RadioSelectHorizontal
    )

    round_index = models.IntegerField()

    # 成功確率
    agent_effort_choice = models.IntegerField()
    principal_effort_choice = models.IntegerField(min=0, max=100)

    # 最小要件
    principal_minimum_requirement = models.IntegerField(min=0, max=100)

    def principal_minimum_requirement_minus1(self):
        return self.principal_minimum_requirement - 1


class Player(BasePlayer):
    pass
