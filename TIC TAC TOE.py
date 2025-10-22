import pygame
import math
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH, CIRCLE_RADIUS, CIRCLE_WIDTH, CROSS_WIDTH, SPACE = 15, 60, 15, 25, 55

# Colors (fixed CROSS_COLOR and BG_COLOR to make X visible)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (242, 85, 96)
CROSS_COLOR = (84, 84, 84)  # Dark grey for X
BG_COLOR = (28, 170, 156)   # Teal background

PLAYER_X, PLAYER_O = 'X', 'O'

font = pygame.font.SysFont('Arial', 40)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

board = [[None] * 3 for _ in range(3)]


def draw_lines():  # Draw the grid lines
    screen.fill(BG_COLOR)
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, i * 200), (WIDTH, i * 200), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * 200, 0), (i * 200, HEIGHT), LINE_WIDTH)


def draw_figures():  # Draw X and O
    for row in range(3):
        for col in range(3):
            if board[row][col] == PLAYER_X:
                pygame.draw.line(screen, CROSS_COLOR, (col * 200 + 50, row * 200 + 50),
                                 (col * 200 + 150, row * 200 + 150), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * 200 + 150, row * 200 + 50),
                                 (col * 200 + 50, row * 200 + 150), CROSS_WIDTH)
            elif board[row][col] == PLAYER_O:
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * 200 + 100, row * 200 + 100),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)


def check_winner(player):
    for i in range(3):
        if all([board[i][j] == player for j in range(3)]) or all([board[j][i] == player for j in range(3)]):
            return True
    if board[0][0] == board[1][1] == board[2][2] == player or board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False


def check_draw():  # Check for draw
    return all(board[row][col] is not None for row in range(3) for col in range(3))


def minimax(board, depth, is_maximizing):
    if check_winner(PLAYER_X):
        return -1
    if check_winner(PLAYER_O):
        return 1
    if check_draw():
        return 0

    best_move = None

    if is_maximizing:
        max_eval = -math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = PLAYER_O
                    eval = minimax(board, depth + 1, False)
                    board[row][col] = None
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (row, col)
        return best_move if depth == 0 else max_eval

    else:
        min_eval = math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = PLAYER_X
                    eval = minimax(board, depth + 1, True)
                    board[row][col] = None
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (row, col)
        return best_move if depth == 0 else min_eval


def display_result(text):  # Show the result
    result_text = font.render(text, True, (255, 255, 255))
    screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2,
                              HEIGHT // 2 - result_text.get_height() // 2))


def main():
    running, turn, game_over, result = True, PLAYER_X, False, None
    draw_lines()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = pygame.mouse.get_pos()
                row, col = y // 200, x // 200

                if board[row][col] is None and turn == PLAYER_X:
                    board[row][col] = PLAYER_X

                    if check_winner(PLAYER_X):
                        result = "You won!"
                    elif check_draw():
                        result = "It's a draw!"
                    else:
                        turn = PLAYER_O

            # AI Turn
            if turn == PLAYER_O and not game_over and not result:
                row, col = minimax(board, 0, True)
                board[row][col] = PLAYER_O

                if check_winner(PLAYER_O):
                    result = "AI won!"
                elif check_draw():
                    result = "It's a draw!"
                else:
                    turn = PLAYER_X

        draw_lines()
        draw_figures()

        if result:
            game_over = True
            display_result(result)
            pygame.display.update()
            pygame.time.wait(2000)
            # Reset the game
            for r in range(3):
                for c in range(3):
                    board[r][c] = None
            game_over, result, turn = False, None, PLAYER_X
            draw_lines()

        pygame.display.update()


if __name__ == "__main__":
    main()
