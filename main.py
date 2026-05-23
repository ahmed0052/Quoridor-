from game import GameState, GameLogic, WallsPlacer
from AI import AI

state = GameState()
logic = GameLogic(state)
AI = AI(state, AiPlayer=1, difficulty='hard')

state.print_board()
print("---")

# player 0 moves down
logic.move_pawn(1, 4)
state.print_board()
print("---")

# AI makes its move
best = AI.get_best_move()
print("AI chose:", best)

# apply the AI's move
if best[0] == 'move':
    logic.move_pawn(best[1][0], best[1][1])
elif best[0] == 'wall':
    wall_placer = WallsPlacer(state)
    wall_placer.place_wall(best[1], best[2], best[3])

state.print_board()