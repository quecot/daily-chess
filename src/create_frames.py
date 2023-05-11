import pygame as p
from numpy import flip
import os
import glob
from PIL import Image, ImageFont, ImageDraw

WIDTH = HEIGHT = 1080
BOARD_DIMENSION = 8
SQUARE_SIZE = WIDTH // BOARD_DIMENSION

IMAGES = {}
NAG_IMAGES = {}

def get_frames(game):
    screen = p.display.set_mode((WIDTH, HEIGHT))
    board = game.board()
    board_array = make_matrix(board)
    result = game.headers['Result'] == '1-0'
    c = 1
    b_nag = False
    nag_type = 0

    loadImages()
    load_nags()
    remove_previous_frames()
    make_frame(screen, board_array, result, c, b_nag, nag_type, board)
    main_line = game.mainline_moves()
    nags = get_nags(main_line)
    for move in main_line:
        board.push(move)
        board_array = make_matrix(board)
        c+=1
        b_nag = False
        for nag in nags:
            if c == nag[1]:
                b_nag = True
                nag_type = nag[0]
        make_frame(screen, board_array, result, c, b_nag, nag_type, board)

    make_frame(screen, board_array, result, c+1, b_nag, nag_type, board)
    make_frame(screen, board_array, result, c+2, b_nag, nag_type, board)

    add_result(game, c+1)
    add_result(game, c+2)

        
def make_frame(screen, board_array, result, c, b_nag, nag_type, board):
    if result:
        drawBoard(screen, board_array, b_nag, nag_type, board, result)
    else:
        drawBoard(screen, flip(board_array), b_nag, nag_type, board, result)
    p.image.save(screen, f'data/frames/{c}frame.jpg')

def drawBoard(screen, board_array, b_nag, nag_type, board, result):
    drawBoardBG(screen)
    if b_nag:
        draw_nag(screen, board, nag_type, result)
    else:
        draw_highlights(screen, board, result) 
    drawPieces(screen, board_array)
    if b_nag:
        draw_nag(screen, board, nag_type, result, first=False)
def drawBoardBG(screen):
    colors = [p.Color('white'), p.Color('gray')]
    for row in range(BOARD_DIMENSION):
        for column in range(BOARD_DIMENSION):
            color = colors[((row+column)%2)]
            p.draw.rect(screen, color, p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def drawPieces(screen, board):
    for row in range(BOARD_DIMENSION):
        for column in range(BOARD_DIMENSION):
            piece = board[row][column]
            if piece != '.':
                screen.blit(IMAGES[piece], p.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def loadImages():
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'wP']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('data/pieceImages/' + piece + '.svg'), (SQUARE_SIZE, SQUARE_SIZE))

def load_nags():
    for i in range(1,7):
        NAG_IMAGES[i-1] = p.transform.scale(p.image.load('data/nag_images/' + str(i) + '.png'), (SQUARE_SIZE//2.5, SQUARE_SIZE//2.5))
def make_matrix(board): #type(board) == chess.Board()
    '''
    Adepted from https://stackoverflow.com/questions/55876336/is-there-a-way-to-convert-a-python-chess-board-into-a-list-of-integers
    '''
    pgn = board.epd()
    foo = []  #Final board
    pieces = pgn.split(' ', 1)[0]
    rows = pieces.split('/')
    for row in rows:
        foo2 = []  #This is the row I make
        for thing in row:
            if thing.isdigit():
                for i in range(0, int(thing)):
                    foo2.append('.')
            else:
                if thing.isupper():
                    foo2.append('w'+thing)
                else:
                    foo2.append('b'+thing.upper())
        foo.append(foo2)
    return foo

def remove_previous_frames():
    files = glob.glob('data/frames/*')
    for f in files:
        os.remove(f)

def add_result(game, c):
    my_image = Image.open(f'data/frames/{c}frame.jpg')
    title_font = ImageFont.truetype('data/arial.TTF', 200)
    image_editable = ImageDraw.Draw(my_image)
    
    image_editable.rectangle([(0, HEIGHT/2-150),(WIDTH, HEIGHT/2+135)], fill ="#7AC5CD00",)
    
    
    image_editable.text((WIDTH/2-130, HEIGHT/2-130), game.headers['Result'], (0, 0, 0), font=title_font)
    my_image.save(f'data/frames/{c}frame.jpg')

def get_nags(main_line):
    nags = []
    s = str(main_line)
    for nag in find(s, '$'):
        frame_def = ""
        nag_type = s[nag+1]
        frame = s[s.rfind('.', 0, nag)-7:s.rfind('.', 0, nag)]
        move = 1 if frame.count('.') > 1 else 0
        for i in range(len(frame)):
            if frame[i].isdigit():
                frame_def = frame_def + frame[i]
        nags.append([int(nag_type), int(frame_def)*2+move])
    return nags

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def draw_nag(screen, board, nag_type, result, first=True):
    dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    col_dict = {'1': [p.Color("lightsteelblue2"), p.Color("lightsteelblue1")], '2': [p.Color("orange2"), p.Color("orange1")], '3': [p.Color("lightskyblue2"), p.Color("lightskyblue1")], '4': [p.Color("red2"), p.Color("red1")], '5': [p.Color("rosybrown2"), p.Color("rosybrown1")], '6': [p.Color("lightgoldenrod1"), p.Color("lightgoldenrodyellow")]}
    start_row = 8 - int(str(board.peek())[1])
    start_col = dict[str(board.peek())[0]]
    end_row = 8 - int(str(board.peek())[3])
    end_col = dict[str(board.peek())[2]]

    if not result:
        start_row = 7 - start_row
        end_row   = 7 - end_row
        start_col = 7 - start_col
        end_col   = 7 - end_col
    if first:
        p.draw.rect(screen, col_dict[str(nag_type)][1], p.Rect(start_col * SQUARE_SIZE, start_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        p.draw.rect(screen, col_dict[str(nag_type)][0], p.Rect(end_col    * SQUARE_SIZE, end_row   * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    screen.blit(NAG_IMAGES[nag_type-1], p.Rect(end_col * SQUARE_SIZE, end_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_highlights(screen, board, result):
    dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    try:
        board.peek()
    except:
        return

    start_row = 8 - int(str(board.peek())[1])
    start_col = dict[str(board.peek())[0]]
    end_row   = 8 - int(str(board.peek())[3])
    end_col   = dict[str(board.peek())[2]]

    if not result:
        start_row = 7 - start_row
        end_row   = 7 - end_row
        start_col = 7 - start_col
        end_col   = 7 - end_col

    p.draw.rect(screen, p.Color("palegreen1"), p.Rect(start_col * SQUARE_SIZE, start_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    p.draw.rect(screen, p.Color("palegreen"), p.Rect(end_col    * SQUARE_SIZE, end_row   * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))