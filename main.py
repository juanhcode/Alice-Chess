import pygame
from constantes import *

pygame.init()


# draw main game board
def draw_board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [column * 160, row * 80, 80, 80])
        else:
            pygame.draw.rect(screen, 'light gray', [80 + (column * 160), row * 80, 80, 80])
        pygame.draw.rect(screen, 'gray', [0, 642, WIDTH, 200])
        pygame.draw.rect(screen, 'gold', [0, 642, WIDTH, 200], 5)
        pygame.draw.rect(screen, 'gold', [650, 0, 200, HEIGHT], 5)
        status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                    'Black: Select a Piece to Move!', 'Black: Select a Destination!']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (10, 660))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 80 * i), (640, 80 * i), 2)
            pygame.draw.line(screen, 'black', (80 * i, 0), (80 * i, 640), 2)
        screen.blit(medium_font.render('SURRENDER', True, 'black'), (660, 710))
        if white_promote or black_promote:
            pygame.draw.rect(screen, 'gray', [0, 642, WIDTH, 200])
            pygame.draw.rect(screen, 'gold', [0, 642, WIDTH, 200], 5)
            screen.blit(big_font.render('Select Piece to Promote Pawn', True, 'black'), (20, 670))

# draw secondary board
def draw_board2():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [1420 - (column * 160), row * 80, 80, 80])
        else:
            pygame.draw.rect(screen, 'light gray', [1340 - (column * 160), row * 80, 80, 80])

        for i in range(9):
            pygame.draw.line(screen, 'black', (860, 80 * i), (1500, 80 * i), 2)
            pygame.draw.line(screen, 'black', (80 * i + 860, 0), (80 * i + 860, 640), 2)

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
                
# function to check all pieces valid options on board
def check_options(pieces, locations, turn):
    global castling_moves
    moves_list = []
    all_moves_list = []
    castling_moves = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list

# check king valid moves
def check_king(position, color):
    moves_list = []
    if color == 'white':
        friends_list = white_locations
    else:
        friends_list = black_locations
    # 8 squares to check for kings, they can go one square any direction
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list

# check valid knight moves
def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list

# check queen valid moves
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list

# check bishop moves
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

# check rook moves
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

# check valid pawn moves
def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in white_locations and \
            (position[0], position[1] + 1) not in black_locations and  position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
            # indent the check for two spaces ahead, so it is only checked if one space ahead is also open
            if (position[0], position[1] + 2) not in white_locations and \
                    (position[0], position[1] + 2) not in black_locations and position[1] == 1:
                moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
        # add en passant move checker
        if (position[0] + 1, position[1] + 1) == black_ep:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) == black_ep:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
            # indent the check for two spaces ahead, so it is only checked if one space ahead is also open
            if (position[0], position[1] - 2) not in white_locations and \
                    (position[0], position[1] - 2) not in black_locations and position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
        # add en passant move checker
        if (position[0] + 1, position[1] - 1) == white_ep:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) == white_ep:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list

# check en passant
def check_ep(old_coords, new_coords):
    if turn_step <= 1:
        index = white_locations.index(old_coords)
        ep_coords = (new_coords[0], new_coords[1] - 1)
        piece = white_pieces[index]
    else:
        index = black_locations.index(old_coords)
        ep_coords = (new_coords[0], new_coords[1] + 1)
        piece = black_pieces[index]
    if piece == 'pawn' and abs(old_coords[1] - new_coords[1]) > 1:
        # if piece was pawn and moved two spaces, return EP coords as defined above
        pass
    else:
        ep_coords = (80, 80)
    return ep_coords

# check for valid moves for just selected piece
def check_valid_moves():
    global valid_moves
    capture_moves = []
    if turn_step < 2:  # Turno de las blancas
        capture_moves = get_capture_moves(white_pieces, white_locations, black_locations, 'white')
        options_list = white_options
    else:  # Turno de las negras
        capture_moves = get_capture_moves(black_pieces, black_locations, white_locations, 'black')
        options_list = black_options

    # Si hay capturas disponibles, restringe los movimientos válidos
    if capture_moves:
        # Filtrar solo las capturas posibles
        valid_moves = []
        for move in capture_moves:
            if move[0] == selection:  # Si la pieza seleccionada tiene capturas
                valid_moves.extend(move[1])  # Agrega las posiciones de captura
    else:
        # Si no hay capturas, permite todos los movimientos normales
        valid_moves = options_list[selection]

    return valid_moves

def check_promo_select():
    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    x_pos = mouse_pos[0] // 80
    y_pos = mouse_pos[1] // 80
    # print(f"Mouse position: {mouse_pos}, Grid position: ({x_pos}, {y_pos})")
    # print(f"White promote: {white_promote}, Black promote: {black_promote}")
    # print(f"Promo index: {promo_index}")
    # print(f"White pieces: {white_pieces}")
    # print(f"White promotions: {white_promotions}")
    if white_promote and left_click and x_pos > 8 and y_pos < 5:
        white_pieces[promo_index] = white_promotions[y_pos]
        print(f"White pieces: {white_pieces}")
    elif black_promote and left_click and x_pos > 8 and y_pos < 5:
        black_pieces[promo_index] = black_promotions[y_pos]

# draw valid moves on screen
def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 80 + 40, moves[i][1] * 80 + 40), 5)

# draw captured pieces on side of screen
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        if i < 8:
            screen.blit(small_black_images[index], (670, 5 + 50 * i))
        else:
            screen.blit(small_black_images[index], (690, 5 + 50 * (i - 8)))
        # If there are more than 8 captured pieces, start a new row
            
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        if i < 8:
            screen.blit(small_white_images[index], (770, 5 + 50 * i))
        else:
            screen.blit(small_white_images[index], (790, 5 + 50 * (i - 8)))

# Determinar si hay movimientos de captura disponibles
def get_capture_moves(pieces, locations, opponent_locations, turn):
    capture_moves = []
    for i in range(len(pieces)):
        piece = pieces[i]
        location = locations[i]
        if piece == 'pawn':
            moves = check_pawn(location, turn)
            capture = []
            for move in moves:
                if move in opponent_locations:
                    capture.append(move)
                if turn == 'white' and move == black_ep:
                    capture.append(move)
                if turn == 'black' and move == white_ep:
                    capture.append(move)
            if capture:
                capture_moves.append((i, capture))
        
        if piece == 'rook':
            moves = check_rook(location, turn)
            capture = []
            for move in moves:
                if move in opponent_locations:
                    capture.append(move)
            if capture:
                capture_moves.append((i, capture))
        
        if piece == 'knight':
            moves = check_knight(location, turn)
            capture = []
            for move in moves:
                if move in opponent_locations:
                    capture.append(move)
            if capture:
                capture_moves.append((i, capture))

        if piece == 'bishop':
            moves = check_bishop(location, turn)
            capture = []
            for move in moves:
                if move in opponent_locations:
                    capture.append(move)
            if capture:
                capture_moves.append((i, capture))
        
        if piece == 'queen':
            moves = check_queen(location, turn)
            capture = []
            for move in moves:
                if move in opponent_locations:
                    capture.append(move)
            if capture:
                capture_moves.append((i, capture))

        if piece == 'king':
            moves = check_king(location, turn)
            capture = []
            for move in moves:
                if move in opponent_locations:
                    capture.append(move)
            if capture:
                capture_moves.append((i, capture))

    return capture_moves

# add pawn promotion
def check_promotion():
    pawn_indexes = []
    white_promotion = False
    black_promotion = False
    promote_index = 80
    for i in range(len(white_pieces)):
        if white_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if white_locations[pawn_indexes[i]][1] == 7:
            white_promotion = True
            promote_index = pawn_indexes[i]
    pawn_indexes = []
    for i in range(len(black_pieces)):
        if black_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if black_locations[pawn_indexes[i]][1] == 0:
            black_promotion = True
            promote_index = pawn_indexes[i]
    return white_promotion, black_promotion, promote_index

def draw_promotion():
    pygame.draw.rect(screen, 'dark gray', [650, 0, 200, 400])
    if white_promote:
        color = 'white'
        for i in range(len(white_promotions)):
            piece = white_promotions[i]
            index = piece_list.index(piece)
            screen.blit(white_images[index], (720, 5 + 80 * i))
    elif black_promote:
        color = 'black'
        for i in range(len(black_promotions)):
            piece = black_promotions[i]
            index = piece_list.index(piece)
            screen.blit(black_images[index], (720, 5 + 80 * i))
    pygame.draw.rect(screen, color, [650, 0, 200, 400], 8)


def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))

def has_legal_moves(options):
    for moves in options:
        if moves:
            return True
    return False

# main game loop
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
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
    draw_captured()
    if not game_over:
        white_promote, black_promote, promo_index = check_promotion()
        if white_promote or black_promote:
            draw_promotion()
            check_promo_select()
    if selection != 80:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
    # # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if not (white_promote or black_promote):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
                x_coord = event.pos[0] // 80
                y_coord = event.pos[1] // 80
                click_coords = (x_coord, y_coord)
                if turn_step <= 1:
                    if click_coords == (8, 8) or click_coords == (9, 8) or click_coords == (8, 9) or click_coords == (9, 9) \
                        or click_coords == (8, 10) or click_coords == (9, 10) or click_coords == (10, 9) or click_coords == (10, 8):
                        winner = 'black'
                    if click_coords in white_locations:
                        selection = white_locations.index(click_coords)
                        if turn_step == 0:
                            turn_step = 1
                    if click_coords in valid_moves and selection != 80:
                        white_ep = check_ep(white_locations[selection], click_coords)
                        white_locations[selection] = click_coords
                        if click_coords in black_locations:
                            black_piece = black_locations.index(click_coords)
                            captured_pieces_white.append(black_pieces[black_piece])
                            if len(captured_pieces_white) == 16:
                                winner = 'white'
                            black_pieces.pop(black_piece)
                            black_locations.pop(black_piece)
                        if click_coords == black_ep:
                            black_piece = black_locations.index((black_ep[0], black_ep[1] - 1))
                            captured_pieces_white.append(black_pieces[black_piece])
                            black_pieces.pop(black_piece)
                            black_locations.pop(black_piece)
                        black_options = check_options(black_pieces, black_locations, 'black')
                        white_options = check_options(white_pieces, white_locations, 'white')
                        if not has_legal_moves(black_options):
                            winner = 'black'
                        turn_step = (turn_step + 1) % 4  # Alternar entre turnos
                        selection = 80
                        valid_moves = []
                if turn_step > 1:
                    if click_coords == (8, 8) or click_coords == (9, 8) or click_coords == (8, 9) or click_coords == (9, 9) \
                        or click_coords == (8, 10) or click_coords == (9, 10) or click_coords == (10, 9) or click_coords == (10, 8):
                        winner = 'white'
                    if click_coords in black_locations:
                        selection = black_locations.index(click_coords)
                        if turn_step == 2:
                            turn_step = 3
                    if click_coords in valid_moves and selection != 80:
                        black_ep = check_ep(black_locations[selection], click_coords)
                        black_locations[selection] = click_coords
                        if click_coords in white_locations:
                            white_piece = white_locations.index(click_coords)
                            captured_pieces_black.append(white_pieces[white_piece])
                            if len(captured_pieces_black) == 16:
                                winner = 'black'
                            white_pieces.pop(white_piece)
                            white_locations.pop(white_piece)
                        if click_coords == white_ep:
                            white_piece = white_locations.index((white_ep[0], white_ep[1] + 1))
                            captured_pieces_black.append(white_pieces[white_piece])
                            white_pieces.pop(white_piece)
                            white_locations.pop(white_piece)
                        black_options = check_options(black_pieces, black_locations, 'black')
                        white_options = check_options(white_pieces, white_locations, 'white')
                        if not has_legal_moves(white_options):
                            winner = 'white' 
                        turn_step = 0
                        selection = 80
                        valid_moves = []
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 80
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')

    if winner != '':
        game_over = True
        draw_game_over()

    pygame.display.flip()
pygame.quit()