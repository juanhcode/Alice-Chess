import pygame

pygame.init()
#Ancho para una pantalla de 14 pulgadas
WIDTH = 1500
#Alto para una pantalla de 14 pulgadas
HEIGHT = 800

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two-Player Pygame Chess!')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 35)
big_font = pygame.font.Font('freesansbold.ttf', 45)
timer = pygame.time.Clock()
fps = 60
# game variables and images
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
captured_pieces_white = []
captured_pieces_black = []
# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = 100
valid_moves = []
# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
black_queen = pygame.image.load('assets/images/black queen.png')
black_queen = pygame.transform.scale(black_queen, (60, 60))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))
black_king = pygame.image.load('assets/images/black king.png')
black_king = pygame.transform.scale(black_king, (60, 60))
black_king_small = pygame.transform.scale(black_king, (45, 45))
black_rook = pygame.image.load('assets/images/black rook.png')
black_rook = pygame.transform.scale(black_rook, (60, 60))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))
black_bishop = pygame.image.load('assets/images/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (60, 60))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_knight = pygame.image.load('assets/images/black knight.png')
black_knight = pygame.transform.scale(black_knight, (60, 60))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_pawn = pygame.image.load('assets/images/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (50, 50))
black_pawn_small = pygame.transform.scale(black_pawn, (40, 40))
white_queen = pygame.image.load('assets/images/white queen.png')
white_queen = pygame.transform.scale(white_queen, (60, 60))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))
white_king = pygame.image.load('assets/images/white king.png')
white_king = pygame.transform.scale(white_king, (60, 60))
white_king_small = pygame.transform.scale(white_king, (45, 45))
white_rook = pygame.image.load('assets/images/white rook.png')
white_rook = pygame.transform.scale(white_rook, (60, 60))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))
white_bishop = pygame.image.load('assets/images/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (60, 60))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_knight = pygame.image.load('assets/images/white knight.png')
white_knight = pygame.transform.scale(white_knight, (60, 60))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_pawn = pygame.image.load('assets/images/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (50, 50))
white_pawn_small = pygame.transform.scale(white_pawn, (40, 40))
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
# check variables/ flashing counter
counter = 0
winner = ''
game_over = False

# draw main game board
def draw_board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [column * 160, row * 80, 80, 80])
        else:
            pygame.draw.rect(screen, 'light gray', [80 + (column * 160), row * 80, 80, 80])
        pygame.draw.rect(screen, 'gray', [0, 700, WIDTH, 100])
        pygame.draw.rect(screen, 'gold', [0, 700, WIDTH, 100], 5)
        pygame.draw.rect(screen, 'gold', [700, 0, 200, HEIGHT], 5)
        status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                    'Black: Select a Piece to Move!', 'Black: Select a Destination!']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (10, 710))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 80 * i), (640, 80 * i), 2)
            pygame.draw.line(screen, 'black', (80 * i, 0), (80 * i, 640), 2)
        # screen.blit(medium_font.render('FORFEIT', True, 'black'), (610, 630))

# draw secondary board
def draw_board2():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [1500 - (column * 160), row * 80, 80, 80])
        else:
            pygame.draw.rect(screen, 'light gray', [1420 - (column * 160), row * 80, 80, 80])

        for i in range(9):
            pygame.draw.line(screen, 'black', (940, 80 * i), (1500, 80 * i), 2)
            pygame.draw.line(screen, 'black', (80 * i + 940, 0), (80 * i + 940, 640), 2)

# draw pieces onto board
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 80 + 15, white_locations[i][1] * 80 + 20))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 80 + 10, white_locations[i][1] * 80 + 10))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 80 + 1, white_locations[i][1] * 80 + 1,
                                                 80, 80], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 80 + 15, black_locations[i][1] * 80 + 20))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 80 + 10, black_locations[i][1] * 80 + 10))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 80 + 1, black_locations[i][1] * 80 + 1,
                                                  80, 80], 2)


# main game loop
# black_options = check_options(black_pieces, black_locations, 'black')
# white_options = check_options(white_pieces, white_locations, 'white')
run = True
while run:
    timer.tick(fps)
    # if counter < 30:
    #     counter += 1
    # else:
    #     counter = 0
    screen.fill('dark gray')
    draw_board()
    draw_board2()
    draw_pieces()
    # draw_captured()
    # draw_check()
    # if selection != 100:
    #     valid_moves = check_valid_moves()
    #     draw_valid(valid_moves)
    # # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #     if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
    #         x_coord = event.pos[0] // 100
    #         y_coord = event.pos[1] // 100
    #         click_coords = (x_coord, y_coord)
    #         if turn_step <= 1:
    #             if click_coords == (8, 8) or click_coords == (9, 8):
    #                 winner = 'black'
    #             if click_coords in white_locations:
    #                 selection = white_locations.index(click_coords)
    #                 if turn_step == 0:
    #                     turn_step = 1
    #             if click_coords in valid_moves and selection != 100:
    #                 white_locations[selection] = click_coords
    #                 if click_coords in black_locations:
    #                     black_piece = black_locations.index(click_coords)
    #                     captured_pieces_white.append(black_pieces[black_piece])
    #                     if black_pieces[black_piece] == 'king':
    #                         winner = 'white'
    #                     black_pieces.pop(black_piece)
    #                     black_locations.pop(black_piece)
    #                 black_options = check_options(black_pieces, black_locations, 'black')
    #                 white_options = check_options(white_pieces, white_locations, 'white')
    #                 turn_step = 2
    #                 selection = 100
    #                 valid_moves = []
    #         if turn_step > 1:
    #             if click_coords == (8, 8) or click_coords == (9, 8):
    #                 winner = 'white'
    #             if click_coords in black_locations:
    #                 selection = black_locations.index(click_coords)
    #                 if turn_step == 2:
    #                     turn_step = 3
    #             if click_coords in valid_moves and selection != 100:
    #                 black_locations[selection] = click_coords
    #                 if click_coords in white_locations:
    #                     white_piece = white_locations.index(click_coords)
    #                     captured_pieces_black.append(white_pieces[white_piece])
    #                     if white_pieces[white_piece] == 'king':
    #                         winner = 'black'
    #                     white_pieces.pop(white_piece)
    #                     white_locations.pop(white_piece)
    #                 black_options = check_options(black_pieces, black_locations, 'black')
    #                 white_options = check_options(white_pieces, white_locations, 'white')
    #                 turn_step = 0
    #                 selection = 100
    #                 valid_moves = []
    #     if event.type == pygame.KEYDOWN and game_over:
    #         if event.key == pygame.K_RETURN:
    #             game_over = False
    #             winner = ''
    #             white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
    #                             'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
    #             white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
    #                                (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
    #             black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
    #                             'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
    #             black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
    #                                (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
    #             captured_pieces_white = []
    #             captured_pieces_black = []
    #             turn_step = 0
    #             selection = 100
    #             valid_moves = []
    #             black_options = check_options(black_pieces, black_locations, 'black')
    #             white_options = check_options(white_pieces, white_locations, 'white')

    # if winner != '':
    #     game_over = True
    #     draw_game_over()

    pygame.display.flip()
pygame.quit()