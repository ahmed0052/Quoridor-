import pygame
from game import GameState, GameLogic, WallsPlacer
from ui import Game, DifficultyScreen, WinScreen, compute_layout
from AI import AI

pygame.init()

screen = pygame.display.set_mode((1200, 750), pygame.RESIZABLE)
pygame.display.set_caption("Quoridor")

# Displays the difficulty selection menu
def run_difficulty_screen():
    while True:
        layout = compute_layout(*screen.get_size())
        difficulty_screen = DifficultyScreen(screen, layout)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                difficulty_screen.handle_click(*pygame.mouse.get_pos())
                if difficulty_screen.selected is not None:
                    return difficulty_screen.selected
        difficulty_screen.draw()

# Creates and runs the main game loop
def run_game(selected):
    state = GameState()
    logic = GameLogic(state)
    wall_placer = WallsPlacer(state)

    if selected == 'human':
        ai = None
    else:
        ai = AI(state, AiPlayer=1, difficulty=selected)

    layout = compute_layout(*screen.get_size())
    game = Game(screen, state, logic, wall_placer, layout, ai=ai)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():

            # Exit game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Update layout when resizing the window
            elif event.type == pygame.VIDEORESIZE:
                layout = compute_layout(*screen.get_size())
                game.layout = layout
                game.board.layout = layout

            # Handle mouse input
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(*pygame.mouse.get_pos())

            # Handle keyboard input
            elif event.type == pygame.KEYDOWN:
                game.handle_key(event.key)

        game.update()
        game.draw()
        clock.tick(60) # Limit frame rate

        # Return winner after game ends
        if game.game_over and game.winner is not None:
            game.draw()
            pygame.time.wait(1000)
            return game.winner

        # Return to menu if game was reset
        if game.game_over and game.winner is None:
            return None

# Displays the winner screen after the game ends
def run_win_screen(winner):
    while True:
        layout = compute_layout(*screen.get_size())
        win_screen = WinScreen(screen, winner, layout)

        for event in pygame.event.get():

            # Exit game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                result = win_screen.handle_click(*pygame.mouse.get_pos())

                if result == 'again':
                    return 'again'

                elif result == 'quit':
                    pygame.quit()
                    exit()

        win_screen.draw()

# Main application loop
while True:
    selected = run_difficulty_screen()
    winner = run_game(selected)
    if winner is None:
        continue
    result = run_win_screen(winner)