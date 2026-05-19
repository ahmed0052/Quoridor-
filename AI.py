from game import PawnMovement, WallsPlacer, BFS
import copy

class AI:
    def __init__(self,state,AiPlayer=1, depth =2):
        self.state = state
        self.AiPlayer = AiPlayer
        self.depth = depth

    def get_best_move(self):
        best_move = None
        best_score = float ('-inf')
        for action in self.get_all_actions(self.AiPlayer, self.state):
            newState = copy.deepcopy(self.state)
            self.apply_Action(newState,self.AiPlayer,action)
            score = self.minimax(newState,self.depth-1, False, float('-inf'),float('inf'))
            if score > best_score:
                best_score = score
                best_move = action

        return best_move

    def check_winner(self,state):
        if self.state.pawns[0][0] == 8:
            return 0

        if self.state.pawns[1][0] == 0:
            return 1

        return None

    def minimax(self,state,depth,isMax,alpha,beta):
        winner = self.check_winner(state)
        if winner == self.AiPlayer:
            return 1000
        if winner is not None:
            return -1000
        if depth == 0:
            return self.evaluate(state)

        player = self.AiPlayer if isMax else 1 - self.AiPlayer
        if isMax:
            max_score = float('-inf')
            for action in self.get_all_action(player, state):
                newState = copy.deepcopy(self.state)
                self.apply_Action(newState,player,action)
                score = self.minimax(newState,self.depth-1,False,alpha,beta)
                max_score = max(max_score,score)
                alpha = max(alpha,score)
                if beta <= alpha:
                    break

            return max_score
        else:
            min_score = float('inf')
            for action in self.get_all_action(player, state):
                newState = copy.deepcopy(self.state)
                self.apply_Action(newState,player,action)
                score = self.minimax(newState,self.depth-1,True,alpha,beta)
                min_score = min(min_score,score)
                beta = min(beta,score)
                if beta <= alpha:
                    break
            return min_score

    def evaluate(self,state):
        Ai_distance = self.BFS_distance(state,self.AiPlayer)
        oppo_distance = self.BFS_distance(state,1 - self.AiPlayer)

        return oppo_distance - Ai_distance

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






