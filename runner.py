import pygame
import sys
import sudoku

pygame.init()

running = True
clock = pygame.time.Clock()

# Screen size
width, height = size = 600, 400

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Font
fontLarge = pygame.font.SysFont("Arial Black", 30)
fontSmall = pygame.font.SysFont("Times New Roman", 25)

ROWS, COLS = sudoku.ROWS, sudoku.COLS
GRID_SIZE = sudoku.GRID_SIZE
SUBGRID_SIZE = sudoku.SUBGRID_SIZE
TILE_SIZE = 40
TILE_ORIGIN = (width / 4 - (1.5 * TILE_SIZE), height / 5 - (1.5 * TILE_SIZE))

VARIABLES = sudoku.VARIABLES

game_start = False
is_custom_value = False
cell_selected = None
cell_value = None
selected_var = None
board = sudoku.generate_sudoku()
EMPTY = sudoku.EMPTY

screen = pygame.display.set_mode(size)


def handle_click_on_empty_tile(board):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == EMPTY:
                return row, col
    return None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

    screen.fill(BLACK)

    # Game interface
    tiles = []
    if game_start:
        for i in range(ROWS):
            row = []
            for j in range(COLS):
                tile = board[i][j]
                rect = pygame.Rect(TILE_ORIGIN[0] + j * TILE_SIZE,
                                   TILE_ORIGIN[1] + i * TILE_SIZE,
                                   TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, WHITE, rect, 3)

                if tile != EMPTY:
                    tile_val = fontSmall.render(str(tile), True, WHITE)
                    tile_val_rect = tile_val.get_rect(center=rect.center)
                    screen.blit(tile_val, tile_val_rect)
                row.append(rect)
            tiles.append(row)
        
        # solution = sudoku.backtrack(board)
        # if solution:
        #     print("Solution found:", solution)
        #     # game_start = False
        #     board = solution
        # else:
        #     print("No solution found")
        
        click, _, _ = pygame.mouse.get_pressed()
        if click:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(len(tiles)):
                for j in range(len(tiles[0])):
                    if tiles[i][j].collidepoint(mouse_pos):
                        if board[i][j] == EMPTY:
                            cell_selected = (i, j)
                            print(f"Cell selected: {cell_selected}")
                        elif is_custom_value:
                            board[i][j] = EMPTY
                            is_custom_value = False
                            print(f"Cell cleared: {cell_selected}")
                        else:
                            cell_selected = None

        # Improvement 3: Displaying numbers from 1-9 as selectable options
        available_numbers = []
        for i in range(len(VARIABLES)):
            rect2 = pygame.Rect(width - (TILE_SIZE + 20), TILE_ORIGIN[1] + i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            varText = fontSmall.render(str(VARIABLES[i]), True, WHITE)
            varTextRect = varText.get_rect(center=rect2.center)
            pygame.draw.rect(screen, WHITE, rect2, 3)
            screen.blit(varText, varTextRect)
            available_numbers.append((rect2, VARIABLES[i]))
        
        click, _, _ = pygame.mouse.get_pressed()
        if click:
            mouse_pos = pygame.mouse.get_pos()
            for rect, value in available_numbers:
                if rect.collidepoint(mouse_pos):
                    selected_var = value
                    if cell_selected is not None:
                        board[cell_selected[0]][cell_selected[1]] = selected_var
                        is_custom_value = True
                        print(f"Cell {cell_selected} set to {selected_var}")
                    else:
                        print("Select a cell first")

    else:
        # Welcome Screen
        welcomeText = fontLarge.render("Welcome to Sudoku Solver", True, WHITE)
        welcomeTextRect = welcomeText.get_rect(center=(width // 2, height // 5))
        screen.blit(welcomeText, welcomeTextRect)

        # Start Button
        btnStartRect = pygame.Rect((width // 3), (height // 2), 200, 50)
        btnText = fontSmall.render("Start Playing", True, WHITE)
        btnTextRect = btnText.get_rect(center=btnStartRect.center)
        pygame.draw.rect(screen, GREEN, btnStartRect)
        screen.blit(btnText, btnTextRect)

        # Exit Button
        btnExitRect = pygame.Rect((width // 3), (height // 2 + btnStartRect.height + 20), 200, 50)
        btnExitText = fontSmall.render("Exit Game", True, WHITE)
        btnExitTextRect = btnExitText.get_rect(center=btnExitRect.center)
        pygame.draw.rect(screen, RED, btnExitRect)
        screen.blit(btnExitText, btnExitTextRect)

        click, _, _ = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if click and btnStartRect.collidepoint(mouse_pos):
            game_start = True
        elif click and btnExitRect.collidepoint(mouse_pos):
            sys.exit(0)
            pygame.quit()

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
