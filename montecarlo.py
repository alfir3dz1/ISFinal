#Referenced from Winston Liu
import reversi
import random
from copy import deepcopy


all_nodes = {}


class Node(object):
    def __init__(self, board, player):

        self.board = board
        self.player = player
        self.score = float('-inf') if player == 'X' else float('inf')
        self.parents = set()
        self.children = {m: None for m in reversi.movablemoves(board, player)}

    def child(self):
        possible_moves = list(self.children.keys())
        if len(possible_moves) == 0:
            return None

        move = random.choice(possible_moves)

        if self.children[move] is not None:
            return self.children[move]

        new_board = deepcopy(self.board)
        other_player = reversi.computer(self.player)
        reversi.make_move(new_board, move, self.player)
        new_node = get_node(new_board, other_player)
        self.children[move] = new_node
        if new_node.score != float('-inf') and new_node.score != float('inf'):
            self.update_ancestors()
        new_node.parents.add(self)
        return new_node

    #datasets
    def suitablemove(self):
        assert self.player == 'X' or self.player == 'O'
        sorted_moves = sorted(((k, v.score) for k, v in self.children.items() if v is not None), key=lambda i: i[1],
                              reverse=self.player == 'X')
        print(sorted_moves)
        if len(sorted_moves) > 0:
            assert sorted_moves[0][1] != float('-inf') and sorted_moves[0][1] != float('inf')
            return sorted_moves[0]
        return random.choice(list(self.children.keys())), float('-inf') if self.player == 'X' else float('inf')

    def get_scores(self):
        return (v.score for k, v in self.children.items() if v is not None)

    def update_ancestors(self, score=None):

        score_before = self.score
        if score is not None:
            assert len(self.children.items()) == 0
            self.score = score
            assert self.score != float('-inf') and self.score != float('inf')
        else:
            if self.player == 'X':
                self.score = max(self.get_scores())
                if self.score == float('-inf'):
                    assert False
            else:
                self.score = min(self.get_scores())
                if self.score == float('inf'):
                    assert False

        # Propogate upwards
        if self.score != score_before:
            for p in self.parents:
                p.update_ancestors()

    def __repr__(self):
        return str(self.board) + str(self.player)

    def __hash__(self):
        return hash_board(self.board, self.player).__hash__()


def get_node(board, player):
    hash = hash_board(board, player)
    if hash in all_nodes:
        return all_nodes[hash]
    n = Node(board, player)
    all_nodes[hash] = n
    return n


def get_move(board, player, num_rollouts=100):
    node = get_node(board, player)

    for i in range(num_rollouts):
        do_rollout(node)

    return node.suitablemove()


def hash_board(board, player):
    return str(board) + player


def do_rollout(root):

    rollout = [root]
    while True:
        child = rollout[-1].child()
        if child is None:
            break
        rollout.append(child)
    rollout[-1].update_ancestors(reversi.scoreboard(rollout[-1].board))


if __name__ == '__main__':

    num_games = 20
    rollouts_selection = [0, 2, 5]
    for mc_player in ['X', 'O']:
        print("MCTS playing {} --".format(mc_player))
        for rollouts in rollouts_selection:
            scores = []
            for game_num in range(num_games):
                all_nodes = {}
                board = reversi.newboard(4)
                cur_move = 'X'
                passed = False
                while True:
                    reversi.drawmove(board, cur_move)
                    if len(reversi.movablemoves(board, cur_move)) == 0:
                        if passed:
                            break
                        passed = True
                        continue
                    passed = False

                    if cur_move == mc_player:
                        move, score = get_move(board, cur_move, num_rollouts=rollouts)
                    else:
                        move, score = get_move(board, cur_move)
                    reversi.make_move(board, move, cur_move)
                    cur_move = reversi.computer(cur_move)
                scores.append(reversi.scoreboard(board))

            print(str(rollouts) + " " + " ".join([str(r) for r in scores]))
