import itertools
import logging

import ggsolver.models as models


logging.basicConfig(level=logging.INFO)


class DTPCGame(models.Game):
    """
    delta(s, a) -> s
    """
    def __init__(self, actions, trans_dict, start_state, y, **kwargs):
        self.actions = actions
        self.trans_dict = trans_dict
        self.start_state = start_state
        self.states = trans_dict.keys()
        self.y = y

    def asw_reach(self, player, final, verbose=False):
        """

        :param player: passed in as {1, 2} for readability but converted to {0, 1} for indexing -
        the player to calculate reachability for
        :param final: final states to reach
        :param verbose: dispaly intermediate computations for containment and safety regions
        :return: almost-sure-reachability states and policy -> displays message if final cannot be reached from start
        """
        # Let U0 = S, y0 = y[player]
        u = [set(self.states)]
        c = []
        y_list = []
        player -= 1 # use player = {0, 1}
        opponent = not player

        while True:
            # calculate confinement states for opponent
            c.append(self.safe(player=opponent, u=u[-1] - final, y=self.y[opponent]))

            # calculate safe states for player to avoid confinement
            u.append(self.safe(player=player, u=u[-1] - c[-1], y=self.y[player]))

            # calculate policy to stay in safe states
            y_list.append(self.stay(player=player, u=u[-1], y=self.y[player]))

            # until Uk+1 = Uk
            if u[-1] == u[-2]:
                # return Uk and y
                return u[-2], y_list[-2]

            if verbose:
                print(f'*** Iteration {len(u)-1} ***')
                print(f'Player {int(opponent+1)} Confinement Set: {c[-1]}')
                print(f'Player {int(player+1)} Safe Set: {u[-1]} \nPolicy: {y_list[-1]}\n')

    def stay(self, player, u, y):
        """
        Stay1(U)(s) = {a1 ∈ A1(s) |∀a2 ∈A2(s),T(s,a1,a2) ∈ U }.
        Stay2(U)(s) = {a2 ∈ A2(s) |∀a1 ∈A1(s),T(s,a1,a2) ∈ U }.

        :param player: {0, 1} - the player to calculate the stay actions for
        :param u: set of goal states player that can be reached by player regardless of opponent's actions
        :param y: allowed actions at each given state
        :return: largest move sub-assignment for player that guarantees game is in U after one round, regardless of
        the move chosen by opponent
        """
        pre = u.copy()
        stay_acts = {}
        # check each state to see if it should be removed
        for state in u:
            # get y - available actions for current state
            temp_y = y[state].copy()
            for act in self.trans_dict[state].keys():
                if act[player] in temp_y:
                    # if there's an action that can't ensure reaching U, remove it
                    if self.trans_dict[state][act] not in u:
                        temp_y.remove(act[player])
                        # remove state if no more actions in y remain to reach U
                        if not temp_y:
                            pre.remove(state)
                            break
            stay_acts[state] = temp_y

        return stay_acts


    def safe(self, player, u, y):
        """
        Given a set U ⊆S and a P1’s move subassignement γ, the safe confinement of player i
        is a set: Safe_i : 2S ×Γ →2S which is a set that player i can ensure the game to stay in, no matter which
        actions are taken by the other player, as long as Player 1 selects actions in the move sub-assignment.

        :param player: {0, 1} - the player to calculate the safe region for
        :param u: set of goal states player that can be reached by player regardless of opponent's actions
        :param y: allowed actions at each given state
        :return: States from which player can confine their opponent
        """

        # X_0 = U, k = 0
        x = [set(u)]
        while True:
            # Xk+1 = Xk ∩ Pre(Xk ,γ), k ← k + 1.
            x.append(x[-1].intersection(self.pre(player, x[-1], y)))

            # Until k = n and Xn = Xn + 1. Let Safe(U, γ) = Xn
            if x[-1] == x[-2]:
                return x[-2]



    def pre(self, player, u, y):
        """
        Pre1(U ,γ) = {s ∈ S |∃a1 ∈ γ(s),∀a2 ∈ A2(s).T(s,a1,a2) ∈ U }
        Pre2(U ,γ) = {s ∈ S |∃a2 ∈A2(s),∀a1 ∈γ(s).T (s,a1,a2) ∈ U }

        :param player: {0, 1} - the player to calculate the Pre for
        :param u: set of goal states player that can be reached by player regardless of opponent's actions
        :param y: allowed actions at each given state
        :return: The Pre for provided player - set of states from which player can select some allowed actions from
        y to ensure reaching U no matter the opponent's action.
        """

        pre = u.copy()
        # check each state to see if it should be removed
        for state in u:
            # get y - available actions for current state
            temp_y = y[state].copy()
            for act in self.trans_dict[state].keys():
                if act[player] in temp_y:
                    # if there's an action that can't ensure remaining in U, remove it
                    if self.trans_dict[state][act] not in u:
                        # - denotes all actions so we know no action can remain in U
                        if act[player] == '-':
                            pre.remove(state)
                            break

                        temp_y.remove(act[player])
                        # remove state if no more actions in y remain to reach U
                        if not temp_y:
                            pre.remove(state)
                            break
        # return
        return pre