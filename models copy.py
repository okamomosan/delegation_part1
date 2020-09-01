from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


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


class Subsession(BaseSubsession):

    # 役割を固定して各ラウンドでランダムマッチング
    def creating_session(self):
        self.group_randomly(fixed_id_in_group=True)

    # コストシートの色の決定(そのラウンドのコストが青のシートならTrue, 黄色のシートならFalse)
    is_cost_blue = (False, False, False, False, False, True, True, True, True, True)

    def cost_blue(self):
        return self.is_cost_blue[self.round_number - 1]

    # 自分にとって望ましいプロジェクトが成功した時の、各ラウンドの報酬
    list_principal_when_success_a = (220, 280, 180, 220, 260, 440, 560, 360, 440, 520)
    list_agent_when_success_b = (220, 280, 180, 220, 260, 440, 560, 360, 440, 520)

    # 自分にとって望ましくないプロジェクトが成功した時の、各ラウンドの報酬
    list_agent_when_success_a = (190, 235, 140, 160, 260, 380, 470, 280, 320, 520)
    list_principal_when_success_b = (190, 235, 140, 160, 260, 380, 470, 280, 320, 520)

    # プロジェクトが失敗した時の、各ラウンドの報酬
    list_when_fail_a = (100, 100, 100, 100, 100, 200, 200, 200, 200, 200)
    list_when_fail_b = (100, 100, 100, 100, 100, 200, 200, 200, 200, 200)

    # 各プロジェクトの報酬
    def agent_when_success_a(self):
        return self.list_agent_when_success_a[self.round_number - 1]

    def principal_when_success_a(self):
        return self.list_principal_when_success_a[self.round_number - 1]

    def agent_when_success_b(self):
        return self.list_agent_when_success_b[self.round_number - 1]

    def principal_when_success_b(self):
        return self.list_principal_when_success_b[self.round_number - 1]

    def when_fail_a(self):
        return self.list_when_fail_a[self.round_number - 1]

    def when_fail_b(self):
        return self.list_when_fail_b[self.round_number - 1]


class Group(BaseGroup):
    # プロジェクト選択
    agent_project_choice = models.IntegerField(
        choices=[[A, 'プロジェクトA'], [B, 'プロジェクトB']],
        widget=widgets.RadioSelectHorizontal
    )

    principal_project_choice = models.IntegerField(
        choices=[[A, 'プロジェクトA'], [B, 'プロジェクトB']],
        widget=widgets.RadioSelectHorizontal
    )

    # 成功確率
    agent_effort_choice = models.IntegerField(min=0, max=100)
    principal_effort_choice = models.IntegerField(min=0, max=100)

    # 最小要件
    principal_minimum_requirement = models.IntegerField(min=0, max=100)

    def principal_minimum_requirement_minus1(self):
        return self.principal_minimum_requirement - 1


class Player(BasePlayer):
    pass
