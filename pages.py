from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import time


class Start(Page):

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        # user has 3 minutes to complete as many pages as possible
        self.participant.vars['expiry'] = time.time() + 3*60


class AgentProjectChoice(Page):

    form_model = "group"
    form_fields = ["agent_project_choice"]
    timer_text = ''

    def get_timeout_seconds(self):
        return self.participant.vars['expiry'] - time.time()

    def is_displayed(self):
        return self.player.id_in_group == 2


class AgentEffortChoice(Page):
    form_model = "group"
    form_fields = ["agent_effort_choice"]
    timer_text = ''

    def get_timeout_seconds(self):
        return self.participant.vars['expiry'] - time.time()

    def is_displayed(self):
        return self.player.id_in_group == 2


class AgentConfirm(Page):
    timer_text = ''

    def get_timeout_seconds(self):
        return self.participant.vars['expiry'] - time.time()

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        if self.group.agent_effort_choice >= 10:
            return {
                'agent_cost_blue': Constants.cost_k[1] * self.group.agent_effort_choice ** 2,
                'agent_cost_yellow': Constants.cost_k[0] * self.group.agent_effort_choice ** 2
            }
        else:
            return {
                'agent_cost_blue': Constants.cost_k[1] * 10 * self.group.agent_effort_choice,
                'agent_cost_yellow': Constants.cost_k[0] * 10 * self.group.agent_effort_choice
            }

    def before_next_page(self):
        if self.request.POST.get('back1'):
            if self.request.POST.get('back1')[0] == '1':
                self._is_frozen = False
                self._index_in_pages -= 2
                self.participant._index_in_pages -= 2
        elif self.request.POST.get('back2'):
            if self.request.POST.get('back2')[0] == '2':
                self._is_frozen = False
                self._index_in_pages -= 3
                self.participant._index_in_pages -= 3


class WaitForAgent(WaitPage):
    pass


class PrincipalProjectChoice(Page):

    form_model = "group"
    form_fields = ["principal_project_choice"]
    timer_text = ''

    def get_timeout_seconds(self):
        return self.participant.vars['expiry'] - time.time()

    def is_displayed(self):
        return self.player.id_in_group == 1


class PrincipalEffortChoice(Page):
    form_model = "group"
    form_fields = ["principal_effort_choice"]
    timer_text = ''

    def get_timeout_seconds(self):
        return self.participant.vars['expiry'] - time.time()

    def is_displayed(self):
        return self.player.id_in_group == 1


class PrincipalMiniReq(Page):
    form_model = "group"
    form_fields = ["principal_minimum_requirement"]
    timer_text = ''

    def get_timeout_seconds(self):
        return self.participant.vars['expiry'] - time.time()

    def is_displayed(self):
        return self.player.id_in_group == 1


class PrincipalConfirm(Page):
    timer_text = ''

    def get_timeout_seconds(self):
        return self.participant.vars['expiry'] - time.time()

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        if self.group.principal_effort_choice >= 10:
            if self.group.principal_minimum_requirement >= 10:
                return {
                    'principal_cost_blue': Constants.cost_k[1] * self.group.principal_effort_choice ** 2,
                    'principal_cost_yellow': Constants.cost_k[0]*self.group.principal_effort_choice ** 2,
                    'minimum_cost_blue': Constants.cost_k[1] * self.group.principal_minimum_requirement ** 2,
                    'minimum_cost_yellow': Constants.cost_k[0]*self.group.principal_minimum_requirement ** 2,
                }
            else:
                return {
                    'principal_cost_blue': Constants.cost_k[1] * self.group.principal_effort_choice ** 2,
                    'principal_cost_yellow': Constants.cost_k[0]*self.group.principal_effort_choice ** 2,
                    'minimum_cost_blue': Constants.cost_k[1] * 10 * self.group.principal_minimum_requirement,
                    'minimum_cost_yellow': Constants.cost_k[0] * 10 * self.group.principal_minimum_requirement,
                }
        else:
            if self.group.principal_minimum_requirement >= 10:
                return {
                    'principal_cost_blue': Constants.cost_k[1] * 10 * self.group.principal_effort_choice,
                    'principal_cost_yellow': Constants.cost_k[0] * 10 * self.group.principal_effort_choice,
                    'minimum_cost_blue': Constants.cost_k[1] * self.group.principal_minimum_requirement ** 2,
                    'minimum_cost_yellow': Constants.cost_k[0]*self.group.principal_minimum_requirement ** 2,
                }
            else:
                return {
                    'principal_cost_blue': Constants.cost_k[1] * 10 * self.group.principal_effort_choice,
                    'principal_cost_yellow': Constants.cost_k[0] * 10 * self.group.principal_effort_choice,
                    'minimum_cost_blue': Constants.cost_k[1] * 10 * self.group.principal_minimum_requirement,
                    'minimum_cost_yellow': Constants.cost_k[0] * 10 * self.group.principal_minimum_requirement,
                }

    def before_next_page(self):
        if self.request.POST.get('back1'):
            if self.request.POST.get('back1')[0] == '1':
                self._is_frozen = False
                self._index_in_pages -= 2
                self.participant._index_in_pages -= 2
        elif self.request.POST.get('back2'):
            if self.request.POST.get('back2')[0] == '2':
                self._is_frozen = False
                self._index_in_pages -= 3
                self.participant._index_in_pages -= 3
        elif self.request.POST.get('back3'):
            if self.request.POST.get('back3')[0] == '3':
                self._is_frozen = False
                self._index_in_pages -= 4
                self.participant._index_in_pages -= 4


class ResultsWaitPage(WaitPage):
    template_name = 'delegation_part1/ResultsWaitPage.html'
    body_text = ''
    title_text = ''


class GoNext(Page):
    form_model = "group"
    form_fields = ["round_index"]

    def before_next_page(self):
        # user has 3 minutes to complete as many pages as possible
        self.participant.vars['expiry'] = time.time() + 3*60


page_sequence = [
    Start,
    AgentProjectChoice,
    AgentEffortChoice,
    AgentConfirm,
    # WaitForAgent,
    # 別にエージェントを待つ必要はないからいらないと思う。よって除外。
    PrincipalProjectChoice,
    PrincipalEffortChoice,
    PrincipalMiniReq,
    PrincipalConfirm,
    ResultsWaitPage,
    GoNext,


]
