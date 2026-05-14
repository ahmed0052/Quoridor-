from game import GameState, GameLogic

state = GameState()
logic = GameLogic(state)

state.print_board()
print("---")

# move player 1 down
logic.move_pawn( 1, 4)
state.print_board()
print("---")

# try an illegal move
logic.move_pawn(0, 0)
state.print_board()