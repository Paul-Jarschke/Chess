import pygame
import chess
import chess.engine

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 512, 512
BOARD_SIZE = 8
SQ_SIZE = WIDTH // BOARD_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (238, 238, 210)
DARK_BROWN = (118, 150, 86)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Load chess pieces (you can download free chess piece sprites online)
piece_images = {}

def load_images():
    piece_file_map = {
        'r': 'black_rook.png', 'n': 'black_knight.png', 'b': 'black_bishop.png',
        'q': 'black_queen.png', 'k': 'black_king.png', 'p': 'black_pawn.png',
        'R': 'white_rook.png', 'N': 'white_knight.png', 'B': 'white_bishop.png',
        'Q': 'white_queen.png', 'K': 'white_king.png', 'P': 'white_pawn.png'
    }
    
    for piece, filename in piece_file_map.items():
        piece_images[piece] = pygame.transform.scale(pygame.image.load(f'images/{filename}'), (SQ_SIZE, SQ_SIZE))

# Draw the chess board
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Draw the pieces on the board
def draw_pieces(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            piece = board.piece_at(chess.square(col, 7 - row))
            if piece:
                screen.blit(piece_images[piece.symbol()], pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Handle dragging pieces
def drag_piece(start_square, board):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    row, col = 7 - (mouse_y // SQ_SIZE), mouse_x // SQ_SIZE
    piece = board.piece_at(chess.square(start_square[1], 7 - start_square[0]))
    
    if piece:
        screen.blit(piece_images[piece.symbol()], (mouse_x - SQ_SIZE // 2, mouse_y - SQ_SIZE // 2))
    return row, col

# Main game loop
def main():
    load_images()
    board = chess.Board()
    clock = pygame.time.Clock()

    dragging = False
    start_square = None
    end_square = None
    
    running = True
    while running:
        draw_board()
        draw_pieces(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Mouse click to select a piece
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not dragging:
                    x, y = pygame.mouse.get_pos()
                    start_square = (y // SQ_SIZE, x // SQ_SIZE)  # Get the starting square
                    dragging = True

            # Mouse button released to drop the piece
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    x, y = pygame.mouse.get_pos()  # Update mouse position when the button is released
                    end_square = (y // SQ_SIZE, x // SQ_SIZE)  # Get the ending square

                    # Check if the piece was dropped on the same square it started on
                    if start_square == end_square:
                        dragging = False  # Simply cancel the dragging, no move to make
                    else:
                        # Create the move based on the start and end squares
                        move = chess.Move.from_uci(
                            f"{chess.square_name(chess.square(start_square[1], 7 - start_square[0]))}"
                            f"{chess.square_name(chess.square(end_square[1], 7 - end_square[0]))}"
                        )

                        if move in board.legal_moves:
                            board.push(move)  # Legal move, push it to the board
                        else:
                            print(f"Illegal move: {move}")  # Debugging illegal move

                    dragging = False  # Stop dragging regardless of outcome

        # If dragging, show the piece moving with the mouse
        if dragging:
            drag_piece(start_square, board)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
