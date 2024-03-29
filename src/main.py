# import the pygame module, so you can use it
import pygame

WIDTH, HEIGHT = 840, 840
 
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
    background_image = pygame.image.load("../img/start_page.jpeg").convert()
    
    # center the background image
    image_x = (WIDTH - background_image.get_width()) // 2
    image_y = (HEIGHT - background_image.get_height()) // 2
    
    # control the frame rate
    clock = pygame.time.Clock()
     
    # define a variable to control the main loop
    running = True
    
    # define a variable to control game status
    game_state = "start"  # start, game, end
    
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():   
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        
        # display the background image at the center of the screen
        screen.blit(background_image, (image_x, image_y))
        pygame.display.update()
        
        # keep the loop running 60 frame per second
        clock.tick(60)
        
        # start page
        if game_state == "start":
            ''' in the start page, user can see a big logo with Aho Mahjong and 
                a menu to select difficulty and game type, then there is a start 
                button. After user click the start button, the game_state will 
                change to game.
            '''
            
            pass
        
        # game page
        elif game_state == "game":
            ''' in the game page, user can see a mahjong table, user's mahjong 
                tile will display one by one at the bottom of the screen, when 
                user click one of its tile, the tile will be move up half its 
                height to show it has been choosen. Every time that user could 
                have some movement choises like chi, peng, their w
            '''
            pass
            
        # check point page
        elif game_state == "check_point":
            pass
        
        # end page
        elif game_state == "end":
            pass
        
if __name__=="__main__":
    main()