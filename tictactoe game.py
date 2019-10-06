import pygame
import sys
import os
import time

def map_mouse_to_board(x, y):
    if x < gameSize / 3 + margin: column = 0
    elif gameSize / 3+margin <= x < (gameSize / 3) * 2+margin: column = 1
    else: column = 2
    if y < gameSize / 3 + margin: row = 0
    elif gameSize / 3 + margin <= y < (gameSize / 3) * 2 + margin:row = 1
    else:row = 2
    return row, column
try:
	o_img, x_img = pygame.image.load('o.png'),pygame.image.load('x.png')
except:
	from time import sleep
	print("there is missing files related to the game (o.png, x.png) please replace them at same directory as the game is.")
	sleep(10)
	sys.exit()

def draw_board(board):
    for y in range(3):
        for x in range(3):
            picker = lambda xx,oo: xx if board[y][x] == -1 else oo if board[y][x] == +1 else pygame.Surface((0, 0))
            screen.blit(picker(x_img, o_img), (x * (gameSize // 3) + margin + 17,15+ y * (gameSize // 3) + margin) )
def is_full(board):
    return not any(None in sublist for sublist in board)
def get_winner(board):
    # Diagonals
    if ((board[0][0] == board[1][1] and board[1][1] == board[2][2]) \
            or (board[0][2] == board[1][1] and board[1][1] == board[2][0])) and board[1][1] is not None:
        return board[1][1]
    for i in range(3):
        if board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] is not None:  # Rows
            return board[i][0]
        if board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] is not None:  # Columns
            return board[0][i]
    return None
def draw_lines():
    # Vertical lines
    pygame.draw.line(screen, lineColor, (margin + gameSize // 3, margin),
                     (margin + gameSize // 3, screenSize - margin), lineSize)
    pygame.draw.line(screen, lineColor, (margin + (gameSize // 3) * 2, margin),
                     (margin + (gameSize // 3) * 2, screenSize - margin), lineSize)
    # Horizontal lines
    pygame.draw.line(screen, lineColor, (margin, margin + gameSize // 3), (screenSize - margin, margin + gameSize // 3),
                     lineSize)
    pygame.draw.line(screen, lineColor, (margin, margin + (gameSize // 3) * 2),
                     (screenSize - margin, margin + (gameSize // 3) * 2), lineSize)

def minimax(state, depth, alpha=-float('inf'), beta=float('inf'), player=+1):#ِplayers:(Ai: +1 & human: -1) #best move selector function.
    best = [-1,-1, -float("inf")] if player== +1 else [-1,-1, +float("inf")] #<<human
    wins  =(((0,0),(0,1),(0,2)),((1,0),(1,1),(1,2)),((2,0),(2,1),(2,2)),((0,0),(1,0),(2,0)),((0,1),(1,1),(2,1)),((0,2),(1,2),(2,2)),((0,0),(1,1),(2,2)),((0,2),(1,1),(2,0))) #wining combinations
    empties = [(i,j) for i in range(3) for j in range(3) if state[i][j]==None] #empty cells 
    win =lambda player: any(map(lambda w: state[w[0][0]][w[0][1]]==state[w[1][0]][w[1][1]]==state[w[2][0]][w[2][1]]==player, wins))
    minimax.check = win #end slot.
    if depth == 0 or win(+1) or win(-1):
        evaluate = 1 if win(+1) else -1 if win(-1) else 0
        return [-1,-1, evaluate]
    for row,col in empties: 
        state[row][col] = player
        score = minimax(state, depth-1, alpha, beta, -player) #recursion core
        state[row][col] = None
        score[0],score[1] = row, col 
        if player == +1:
            best = score if score[2] > best[2] else best  #maximizing
            alpha = max(alpha, best[2]) 
            if alpha >= beta:break 
        else:
            best = score if score[2] < best[2] else best  #minimizing

            beta = min(beta, best[2]) 
            if alpha >= beta:break  
    return best
screenSize = 400
margin = 35
gameSize = screenSize - (2 * margin)
lineSize = 5
lineColor = (255, 255, 255)
backgroundColor = (0, 0, 0)
xColor = (200, 0, 0)
oColor = (0, 0, 200)
xMark = 'X'
oMark = 'O'
board = [[None, None, None], [None, None, None], [None, None, None]]
currentMove = 'X'
pygame.init()
clock = pygame.time.Clock()
icon = pygame.image.load('x.png')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((screenSize, screenSize))
pygame.display.set_caption("Tic Tac Toe")
pygame.font.init()
myFont = pygame.font.SysFont('Tahoma', gameSize // 3)
screen.fill(backgroundColor)
canPlay = True
draw_lines()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                board = [[None, None, None], [None, None, None], [None, None, None]]
                screen.fill(backgroundColor)
                draw_lines()
                canPlay = True
                currentMove = xMark
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type is pygame.MOUSEBUTTONDOWN and canPlay and currentMove == xMark:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            (column, row) = map_mouse_to_board(mouseX, mouseY)
            if board[column][row] is None:
                board[column][row] = -1
                
                if currentMove == xMark:
                    currentMove = oMark
                else:
                    currentMove = xMark
                draw_board(board)
                winner = get_winner(board)
                if winner is not None:
                    s = pygame.Surface((400,400))  
                    s.set_alpha(230)           
                    s.fill((0,0,0))       
                    screen.blit(s, (0,0))
                    myFont = pygame.font.SysFont('Verdana', 50)
                    myFont2 = pygame.font.SysFont('Verdana', 20)
                    text_surface = myFont.render("You won!", False, lineColor)
                    text_surface2 = myFont2.render("press (F) to play again!", False, lineColor)
                    size, size2 = myFont.size("You won!"), myFont2.size("press (F) to play again!")
                    screen.blit(text_surface, (0.5*screenSize-0.5*size[0], screenSize // 2 - screenSize // 10))
                    screen.blit(text_surface2, (0.5*screenSize-0.5*size2[0], screenSize // 2 - screenSize // 10+100))
                    canPlay = False
                else:
                    if is_full(board):
                        currentMove = 0
                        s = pygame.Surface((400,400))  
                        s.set_alpha(230)           
                        s.fill((0,0,0))       
                        screen.blit(s, (0,0))
                        myFont = pygame.font.SysFont('Verdana', 50)
                        myFont2 = pygame.font.SysFont('Verdana', 20)
                        text_surface = myFont.render("Draw!", False, lineColor)
                        text_surface2 = myFont2.render("press (F) to play again!", False, lineColor)
                        size, size2 = myFont.size("Draw!"), myFont2.size("press (F) to play again!")
                        screen.blit(text_surface, (0.5*screenSize-0.5*size[0], screenSize // 2 - screenSize // 10))
                        screen.blit(text_surface2, (0.5*screenSize-0.5*size2[0], screenSize // 2 - screenSize // 10+100))

        elif currentMove == oMark:
            raw = minimax(board, len([(i,j) for i in range(3) for j in range(3) if board[i][j]==None]))
            (row, column) = raw[:2]
            if board[row][column] is None:
                board[row][column] = +1
                if currentMove == xMark:
                    currentMove = oMark
                else:
                    currentMove = xMark
                draw_board(board)
                winner = get_winner(board)
                if winner is not None:
                    s = pygame.Surface((400,400))  
                    s.set_alpha(230)           
                    s.fill((0,0,0))       
                    screen.blit(s, (0,0))
                    myFont = pygame.font.SysFont('Verdana', 50)
                    myFont2 = pygame.font.SysFont('Verdana', 20)
                    text_surface = myFont.render("Computer won!", False, lineColor)
                    text_surface2 = myFont2.render("press (F) to play again!", False, lineColor)
                    size, size2 = myFont.size("Computer won!"), myFont2.size("press (F) to play again!")
                    screen.blit(text_surface, (0.5*screenSize-0.5*size[0], screenSize // 2 - screenSize // 10))
                    screen.blit(text_surface2, (0.5*screenSize-0.5*size2[0], screenSize // 2 - screenSize // 10+100))
                    canPlay = False
                else:
                    if is_full(board):
                        currentMove = 0
                        s = pygame.Surface((400,400))  
                        s.set_alpha(230)           
                        s.fill((0,0,0))       
                        screen.blit(s, (0,0))
                        myFont = pygame.font.SysFont('Verdana', 50)
                        myFont2 = pygame.font.SysFont('Verdana', 20)
                        text_surface = myFont.render("Draw!", False, lineColor)
                        text_surface2 = myFont2.render("press (F) to play again!", False, lineColor)
                        size, size2 = myFont.size("Draw!"), myFont2.size("press (F) to play again!")
                        screen.blit(text_surface, (0.5*screenSize-0.5*size[0], screenSize // 2 - screenSize // 10))
                        screen.blit(text_surface2, (0.5*screenSize-0.5*size2[0], screenSize // 2 - screenSize // 10+100))


    pygame.display.update()
    clock.tick(60)
