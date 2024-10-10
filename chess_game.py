import pygame
import chess
import chess.engine

# Initialize Pygame
pygame.init()

# Constants for board and colors
WIDTH, HEIGHT = 512, 512  # Screen width and height
BOARD_SIZE = 8  # Chess board is 8x8
SQ_SIZE = WIDTH // BOARD_SIZE  # Size of each square on the board
WHITE = (255, 255, 255)  # RGB color for white
BLACK = (0, 0, 0)  # RGB color for black
LIGHT_BROWN = (227,193,111)  # RGB color for light squares
DARK_BROWN = (184,139,74)  # RGB color for dark squares

# Set up the display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")  # Title for the window

# Dictionary to store chess piece images
piece_images = {}

# Function to load images for each chess piece
def load_images():
    piece_file_map = {
        'r': 'black_rook.png', 'n': 'black_knight.png', 'b': 'black_bishop.png',
        'q': 'black_queen.png', 'k': 'black_king.png', 'p': 'black_pawn.png',
        'R': 'white_rook.png', 'N': 'white_knight.png', 'B': 'white_bishop.png',
        'Q': 'white_queen.png', 'K': 'white_king.png', 'P': 'white_pawn.png'
    }
    
    # Load each piece image and scale it to fit on the board
    for piece, filename in piece_file_map.items():
        piece_images[piece] = pygame.transform.scale(
            pygame.image.load(f'images/{filename}'), (SQ_SIZE, SQ_SIZE))

# Function to draw the chess board
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # Alternate between light and dark squares
            color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Function to draw chess pieces on the board based on the current state
def draw_pieces(board, dragging, start_square):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # Get the piece on the current square
            piece = board.piece_at(chess.square(col, 7 - row))
            
            # Skip drawing the piece that is being dragged
            if dragging and (row, col) == start_square:
                continue  # Don't draw the dragged piece on the board
            
            if piece:
                # Draw the corresponding image for the piece on the square
                screen.blit(piece_images[piece.symbol()], pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


# Function to handle piece dragging
def drag_piece(start_square, board):
    mouse_x, mouse_y = pygame.mouse.get_pos()  # Get current mouse position
    row, col = 7 - (mouse_y // SQ_SIZE), mouse_x // SQ_SIZE  # Convert mouse position to board square
    piece = board.piece_at(chess.square(start_square[1], 7 - start_square[0]))  # Get the dragged piece
    
    if piece:
        # Display the piece being dragged along with the mouse
        screen.blit(piece_images[piece.symbol()], (mouse_x - SQ_SIZE // 2, mouse_y - SQ_SIZE // 2))
    return row, col  # Return the row and column where the piece is dragged

# Main game loop
def main():
    load_images()  # Load chess piece images
    board = chess.Board()  # Initialize the chess board (from python-chess library)
    clock = pygame.time.Clock()  # Set up a clock to control frame rate

    dragging = False  # Flag to track if a piece is being dragged
    start_square = None  # The square where the piece was picked up from
    end_square = None  # The square where the piece will be dropped
    
    running = True
    while running:
        draw_board()  # Draw the board

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If user closes the window, stop the game
                running = False

            # Mouse button pressed: start dragging the piece
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not dragging:
                    x, y = pygame.mouse.get_pos()  # Get mouse position
                    start_square = (y // SQ_SIZE, x // SQ_SIZE)  # Convert mouse position to board square
                    dragging = True  # Set the flag to indicate dragging

            # Mouse button released: drop the piece
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    x, y = pygame.mouse.get_pos()  # Get mouse position at the time of release
                    end_square = (y // SQ_SIZE, x // SQ_SIZE)  # Get the square where the piece is dropped

                    # Check if the piece was dropped on the same square it was picked up from
                    if start_square == end_square:
                        dragging = False  # Cancel dragging, no move is made
                    else:
                        # Create a move using UCI notation (start and end squares)
                        move = chess.Move.from_uci(
                            f"{chess.square_name(chess.square(start_square[1], 7 - start_square[0]))}"
                            f"{chess.square_name(chess.square(end_square[1], 7 - end_square[0]))}"
                        )

                        # If the move is legal, make the move
                        if move in board.legal_moves:
                            board.push(move)  # Push the legal move to the board
                        else:
                            print(f"Illegal move: {move}")  # Debugging: print illegal move

                    dragging = False  # Stop dragging after the move

        # If a piece is being dragged, update its position with the mouse
        if dragging:
            # Draw the board and pieces excluding the one being dragged
            draw_pieces(board, dragging, start_square)
            # Then draw the dragged piece at the current mouse position
            drag_piece(start_square, board)
        else:
            # Draw the board and all the pieces normally when not dragging
            draw_pieces(board, dragging, start_square)

        pygame.display.flip()  # Update the display
        clock.tick(120)  # Set the frame rate to 60 FPS

    pygame.quit()  # Quit the game when the loop ends

# Run the game if this script is executed directly
if __name__ == "__main__":
    main()
