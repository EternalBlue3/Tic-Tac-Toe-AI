import pygame, sys, time

pygame.init()
red = pygame.Color(255,0,0)
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
pygame.display.set_caption('Tic Tac Toe AI')
width, height = 300,300
game_window = pygame.display.set_mode((width, height))

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

def make_move(move,posx,posy):
    global board
    global player
    
    if player == "X":
        game_window.blit(x_img, (posy,posx))
        board[move] = "X"
        if evaluate(board,"X"):
            print("Game Over, X wins.")
            game_over("X")
        player = "O"
    else:
        game_window.blit(o_img, (posy,posx))
        board[move] = "O"
        if evaluate(board,"O"):
            print("Game Over, O wins.")
            game_over("O")
        player = "X"
    if 0 not in board:
        game_over_draw()

while True:
    for event in pygame.event.get():
  
      # if user types QUIT then the screen will close
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            column, row = 0, 0
            
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
            
            make_move(move,posx,posy)
                
    pygame.display.update()
    fps_controller.tick(100)
