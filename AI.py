from game import PawnMovement, WallsPlacer, BFS
import copy
import sys
sys.setrecursionlimit(1000000)

# AI player using Minimax with Alpha-Beta pruning
class AI:
    # Difficulty affects search depth and wall search range
    def __init__(self,state,AiPlayer=1, difficulty='medium'):
        self.state = state
        self.AiPlayer = AiPlayer
        if difficulty == 'easy':
            self.depth = 1
            self.wall_range = 0

        #fixed play time for both medium and hard
        elif difficulty == 'medium':
            self.depth = 2
            self.wall_range = 1

        elif difficulty == 'hard':
            self.depth = 3
            self.wall_range = 1

    # Try all possible actions and choose the highest scoring one
    def get_best_move(self):
        best_move = None
        best_score = float ('-inf')

        for action in self.get_all_action(self.AiPlayer, self.state):
            newState = copy.deepcopy(self.state)
            self.apply_Action(newState,self.AiPlayer,action)
            score = self.minimax(newState,self.depth-1, False, float('-inf'),float('inf'))

            if score > best_score:
                best_score = score
                best_move = action

        return best_move

    def check_winner(self,state):
        if state.pawns[0][0] == 8:
            return 0

        if state.pawns[1][0] == 0:
            return 1

        return None

    # Recursive Minimax algorithm with Alpha-Beta pruning
    def minimax(self,state,depth,isMax,alpha,beta):
        winner = self.check_winner(state)
        if winner == self.AiPlayer:
            return 1000
        if winner is not None:
            return -1000
        if depth == 0:
            return self.evaluate(state)

        player = self.AiPlayer if isMax else 1 - self.AiPlayer

        # AI tries to maximize score
        if isMax:
            max_score = float('-inf')
            for action in self.get_all_action(player, state):
                newState = copy.deepcopy(state)
                self.apply_Action(newState,player,action)
                score = self.minimax(newState,depth-1,False,alpha,beta)
                max_score = max(max_score,score)
                alpha = max(alpha,score)

                if beta <= alpha:
                    break

            return max_score

        # Opponent tries to minimize score
        else:
            min_score = float('inf')
            for action in self.get_all_action(player, state):
                newState = copy.deepcopy(state)
                self.apply_Action(newState,player,action)
                score = self.minimax(newState,depth-1,True,alpha,beta)
                min_score = min(min_score,score)
                beta = min(beta,score)
                if beta <= alpha:
                    break
            return min_score

    # Heuristic based on shortest distance to goal
    def evaluate(self,state):
        Ai_distance = self.BFS_distance(state,self.AiPlayer)
        oppo_distance = self.BFS_distance(state,1 - self.AiPlayer)

        return oppo_distance - Ai_distance

    # Finds shortest path length using BFS
    def BFS_distance(self,state,player):
        start = state.pawns[player]
        goalRow = 8 if player == 0 else 0
        visited = []
        queue = [[start, 0]]
        while queue:
            current,distance = queue.pop(0)
            x,y = current
            if x == goalRow:
                return distance
            if current in visited:
                continue

            visited.append(current)
            bfs = BFS(state)
            for neighbor in bfs.get_neighbors(x,y):
                if neighbor not in visited:
                    queue.append([neighbor,distance+1])

        return float('inf')

    def get_all_action(self,player,state):
        actions = []
        movement = PawnMovement(state)

        # Generate possible pawn moves
        for move in movement.get_valid_moves(player):
            actions.append(('move', move))


        if state.walls_available[player] > 0:

            p0 = state.pawns[0]
            p1 = state.pawns[1]

            for x in range(9):
                for y in range(9):
                    near_p0 = abs(x - p0[0]) <= self.wall_range and abs(y - p0[1]) <= self.wall_range
                    near_p1 = abs(x - p1[0]) <= self.wall_range and abs(y - p1[1]) <= self.wall_range

                    # Generate possible wall placements near players
                    if near_p0 or near_p1:
                        if y < 8:
                            actions.append(('wall', x, y, 'h'))
                        if x < 8:
                            actions.append(('wall', x, y, 'v'))

        return actions

    # Applies a simulated move/wall during Minimax search
    def apply_Action(self,state,player,action):
        state.current_player = player

        if action[0] == 'move':
            move = action[1]
            state.pawns[player] = move
            state.current_player = 1 - player

        elif action[0] == 'wall':
            _, x, y, direction = action
            wall_placer = WallsPlacer(state)
            wall_placer.place_wall(x, y, direction)




