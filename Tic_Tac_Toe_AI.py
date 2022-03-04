# importing the required libraries
import pygame, sys, time

pygame.init()
red = pygame.Color(255,0,0)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
pygame.display.set_caption('Tic Tac Toe AI')
width, height = 300,300
game_window = pygame.display.set_mode((width, height))

# 1 = X
# -1 = O
player = "X"
board = [0]*9

x_img = pygame.image.load("X_img.png")
y_img = pygame.image.load("O_img.png")
x_img = pygame.transform.scale(x_img, (86, 86))
o_img = pygame.transform.scale(y_img, (86, 86))

fps_controller = pygame.time.Clock()

game_window.fill(white)

pygame.draw.line(game_window, black, (width/3, 0), (width/3, height), 7)
pygame.draw.line(game_window, black, (width/3 * 2, 0), (width/3 * 2, height), 7)
   
pygame.draw.line(game_window, black, (0, height/3), (width, height/3), 7)
pygame.draw.line(game_window, black, (0, height/3 * 2), (width, height/3 * 2), 7)
pygame.display.update()

def evaluate(board, turn):
    for pos in ([0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]):  # Go through all possible winning lines
        if board[pos[0]] == board[pos[1]] == board[pos[2]] == turn: 
            return 1  # Return 1 if player turn has 3 in a row

def possible_moves(board):
    returns = []
    for x in range(len(board)):
        if board[x] == 0:
            returns.append(x)
    return returns
        
# AI
def negamax(board, depth, turn):
    if evaluate(board, turn): return 0, (9+depth)  # Return positive score if maximizing player
    
    if evaluate(board, -turn): return 0, -(9 + depth)  # Return negative score if minimizing player wins
    
    if 0 not in board: return 0, 0  # Drawn game, return 0
    
    if depth == 0:
        return possible_moves(board)[0], (4+depth)
    
    best_score = -20  # Initiate with less than smallest possible score
    
    for move in [i for i in range(9) if not board[i]]:  # Go through all empty squares on board
        
        board[move] = turn  # Make move
        
        score = -negamax(board, depth - 1, -turn)[1]  # Recursive call to go through all child nodes
        
        board[move] = 0  # Unmake the move
        
        if score > best_score: 
            best_score, best_move = score, move  # If score is larger than previous best, update score
    return best_move, best_score  # Return the best move and its corresponding score
        
def game_over(player):
    game_window.fill(black)
    my_font = pygame.font.SysFont('times new roman', 40)
    game_over_surface = my_font.render(f'{player} WINS', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (width/2, height/4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()
    
def game_over_draw():
    game_window.fill(black)
    my_font = pygame.font.SysFont('times new roman', 40)
    game_over_surface = my_font.render(f'Draw', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (width/2, height/4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

def make_move(player,move,posx,posy):
    global board
    
    if player == "X":
        game_window.blit(x_img, (posy,posx))
        pygame.display.update()
        board[move] = 1
        if evaluate(board,1):
            time.sleep(0.1)
            print("Game Over, X wins.")
            game_over("X")
    else:
        game_window.blit(o_img, (posy,posx))
        pygame.display.update()
        board[move] = -1
        if evaluate(board,-1):
            time.sleep(0.1)
            print("Game Over, O wins.")
            game_over("O")
    
    if 0 not in board:
        game_over_draw()

while True:
    for event in pygame.event.get():
  
      # if user types QUIT then the screen will close
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            run_ai_move = True
            
            mouseX, mouseY = pygame.mouse.get_pos()
            column, row = 0, 0
            
            # Human Move
            if mouseY > 100:
                column = 1
                if mouseY > 200:
                    column = 2
                    
            if mouseX > 100:
                row = 1
                if mouseX > 200:
                    row = 2
                    
            posy = row*100 + 7
            posx = column*100 + 7
            
            move = row + column*3
            
            if board[move] ==  0:
                make_move("X",move,posx,posy)
            else:
                run_ai_move = False
                            
            # AI Move
            if run_ai_move:
                ai_move = negamax(board, 9, -1)[0]

                # Translate move into rows and columns
                if ai_move == 0:
                    ai_row, ai_column = 0, 0
                if ai_move == 1:
                    ai_row, ai_column = 1, 0
                if ai_move == 2:
                    ai_row, ai_column = 2, 0
                if ai_move == 3:
                    ai_row, ai_column = 0, 1
                if ai_move == 4:
                    ai_row, ai_column = 1, 1
                if ai_move == 5:
                    ai_row, ai_column = 2, 1
                if ai_move == 6:
                    ai_row, ai_column = 0, 2
                if ai_move == 7:
                    ai_row, ai_column = 1, 2
                if ai_move == 8:
                    ai_row, ai_column = 2, 2

                ai_posy = ai_row*100 + 7
                ai_posx = ai_column*100 + 7

                make_move("O",ai_move,ai_posx,ai_posy)
                
    pygame.display.update()
    fps_controller.tick(100)
