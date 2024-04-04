import pygame
from game import game
from element import generate_tiles
from const import TILE_RATIO

WIDTH, HEIGHT = 1200, 900
EDGE = 20
INNER_WIDTH = WIDTH - 2 * EDGE 
 
# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()
    
    # load and set the logo
    logo = pygame.image.load('../img/logo.jpeg')
    pygame.display.set_icon(logo)
    pygame.display.set_caption('Aho Mahjong')
    
    # WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0]
    WIDTH, HEIGHT = 1200, 900
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    WIDTH, HEIGHT = screen.get_size()
    
    # create a surface on screen that has the size of 1280 x 960
    #screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen_rect = screen.get_rect()
    
    # load the background image for start page, and convert it to a pygame image object.
    start_background_image = pygame.image.load('../img/start_page.jpeg').convert_alpha()
    start_background_rect = start_background_image.get_rect(center = (WIDTH // 2, HEIGHT // 2))
    
    # create a font
    title_font = pygame.font.Font(None, 100)
    normal_font = pygame.font.Font(None, 50)
    
    # control the frame rate
    clock = pygame.time.Clock()
     
    # define a variable to control the main loop
    running = True
    
    # define a variable to control game status
    game_state = 'start_page'  # start, game, check_point, end
    
    # define a variable to control the initialization 
    init_state = False
    
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():   
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        
        # keep the loop running 60 frame per second
        clock.tick(30)
        
        # start page
        if game_state == 'start_page':
            ''' in the start page, user can see a big logo with Aho Mahjong and 
                a menu to select difficulty and game type, then there is a start 
                button. After user click the start button, the game_state will 
                change to game.
            '''
            # display the background image at the center of the screen
            screen.blit(start_background_image, start_background_rect)
            
            # display the title at the center of the screen, red color and bold font
            title_surf = title_font.render('Aho Mahjong', True, 'white')
            title_rect = title_surf.get_rect(center = (WIDTH // 2, 100))
            screen.blit(title_surf, title_rect)
            
            # display the start button
            start_button_surf = title_font.render('Start game!', True, 'black')
            start_button_rect = start_button_surf.get_rect(center = (WIDTH // 2 + 300, HEIGHT // 2))
            pygame.draw.rect(screen, 'white', start_button_rect, border_radius=20)
            
            # check if there are mouseclick in this rectangle
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and \
                start_button_rect.collidepoint(mouse_pos):
                # create a game object
                game_obj = game(SCREEN_HEIGHT=HEIGHT)
                
                # change the game_state to game
                game_state = 'game'
            elif event.type == pygame.MOUSEMOTION and start_button_rect.collidepoint(mouse_pos):
                # change the color of start button to yellow
                pygame.draw.rect(screen, 'yellow', start_button_rect, border_radius=20)
        
            # update the display
            screen.blit(start_button_surf, start_button_rect)
            pygame.display.update()
            
        # game page
        elif game_state == 'game':
            ''' in the game page, user can see a mahjong table, user's mahjong 
                tile will display one by one at the bottom of the screen, when 
                user click one of its tile, the tile will be move up half its 
                height to show it has been choosen. Every time that user could 
                have some movement choises like chi, peng, there will be a small
                button to show the movement choises. After user click the button,
                then this movement will be done and next player will play. After 
                at least one player finished hu, then game will change to check
                point page. 
            '''
            # game start
            if init_state == False:
                game_obj.start_ju()
                init_state = True
            
            # clear the screen, black color
            pygame.draw.rect(screen, 'black', screen_rect)
            
            # draw the mahjong table
            table_rect = pygame.Rect(0, 0, HEIGHT, HEIGHT)
            inner_rect = pygame.Rect(EDGE, EDGE, HEIGHT - EDGE * 2, HEIGHT - EDGE * 2)
            inner_color = pygame.Color(79, 164, 133)
            pygame.draw.rect(screen, inner_color, inner_rect)
            pygame.draw.rect(screen, 'brown', table_rect, width=EDGE, border_radius=EDGE)
            pygame.draw.line(screen, 'black', (EDGE, EDGE), (HEIGHT - EDGE, HEIGHT - EDGE))
            pygame.draw.line(screen, 'black', (EDGE, HEIGHT - EDGE), (HEIGHT - EDGE, EDGE))
            
            # draw the region contains all hidden tiles
            hidden_tiles_rect = pygame.Rect(EDGE + HEIGHT // TILE_RATIO, EDGE + HEIGHT // TILE_RATIO,\
                                            HEIGHT // TILE_RATIO * 0.7 * 17, HEIGHT // TILE_RATIO)
            hidden_tiles_rect2 = hidden_tiles_rect.copy()
            pygame.draw.rect(screen, 'black', hidden_tiles_rect, width=1)

            
            # show current player's tile
            game_obj.players[0].display_my_tiles(screen)
            
            # show sort button
            button_surf = normal_font.render('Sort', True, 'red')
            button_rect = button_surf.get_rect(topleft=(920, 820))
            pygame.draw.rect(screen, 'orange', button_rect, border_radius=10)
            # screen.blit(button_surf, button_rect)
            if button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                game_obj.players[0].sort_tiles()
            
            # update the display
            pygame.display.update()
            
        # check point page
        elif game_state == 'check_point':
            ''' in the check point page, user can see how much points each player 
                earns from winning the game, and also see the winner of the game.
                After checking the points, user can click the continue button to 
                go to next round, if this is the last round, user can click the
                end button to end the game.
            '''
            
            pass
        
        # end page
        elif game_state == 'end':
            ''' in the end page, user can see the final score of each player, and 
                the winner of the game. After the game is over, user can click next
                button to start a new game or exit button to quit the game.
            '''
            
            pass
        
if __name__=='__main__':
    main()