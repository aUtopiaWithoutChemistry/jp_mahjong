# import the pygame module, so you can use it
import pygame

WIDTH, HEIGHT = 1280, 960
 
# define a main function
def main():
     
    # initialize the pygame module
    pygame.init()
    
    # load and set the logo
    logo = pygame.image.load("../img/logo.jpeg")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Aho Mahjong")
    
    # create a surface on screen that has the size of 1280 x 960
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    # load the background image for start page, and convert it to a pygame image object.
    start_background_image = pygame.image.load("../img/start_page.jpeg").convert()
    
    # load the background image for game page, and convert it to a pygame image object.
    game_background_image = pygame.image.load("../img/mahjong_table.png").convert()
    game_background_image = pygame.transform.scale(game_background_image, (HEIGHT, HEIGHT)) 
    
    # center the background image
    image_x = (WIDTH - start_background_image.get_width()) // 2
    image_y = (HEIGHT - start_background_image.get_height()) // 2
    
    # create a font
    title_font = pygame.font.Font(None, 100)
    
    # control the frame rate
    clock = pygame.time.Clock()
     
    # define a variable to control the main loop
    running = True
    
    # define a variable to control game status
    game_state = "game"  # start, game, check_point, end
    
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():   
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        
        # keep the loop running 60 frame per second
        clock.tick(60)
        
        # start page
        if game_state == "start":
            ''' in the start page, user can see a big logo with Aho Mahjong and 
                a menu to select difficulty and game type, then there is a start 
                button. After user click the start button, the game_state will 
                change to game.
            '''
            # display the background image at the center of the screen
            screen.blit(start_background_image, (image_x, image_y))
            
            # display the title at the center of the screen, red color and bold font
            screen.blit(title_font.render("Aho Mahjong", True, 'red'), (WIDTH // 2 - 200, 100))
            pygame.display.update()
        
        # game page
        elif game_state == "game":
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
            # display the mahjong table at the left of screen
            screen.blit(game_background_image, (0, 0))
            pygame.display.update()
            
        # check point page
        elif game_state == "check_point":
            ''' in the check point page, user can see how much points each player 
                earns from winning the game, and also see the winner of the game.
                After checking the points, user can click the continue button to 
                go to next round, if this is the last round, user can click the
                end button to end the game.
            '''
            
            pass
        
        # end page
        elif game_state == "end":
            ''' in the end page, user can see the final score of each player, and 
                the winner of the game. After the game is over, user can click next
                button to start a new game or exit button to quit the game.
            '''
            
            pass
        
if __name__=="__main__":
    main()