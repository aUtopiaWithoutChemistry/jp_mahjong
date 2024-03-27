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
    
    zero_man = pygame.image.load("../img/0m.png")
     
    # create a surface on screen that has the size of 1280 x 960
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    background_image = pygame.image.load("../img/start_page.jpeg").convert()
    
    # center the background image
    image_x = (WIDTH - background_image.get_width()) // 2
    image_y = (HEIGHT - background_image.get_height()) // 2
     
    # define color
    color = (0, 204, 204)
    
    # Create a Rect object (x, y, width, height)
    rect_obj = pygame.Rect(100, 100, 200, 150)
    
    # draw the start button
    button_rect = pygame.draw.rect(screen, color, rect_obj, width=0, border_radius=3)
     
    # define a variable to control the main loop
    running = True
    
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():   
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                # Button clicked! Transition to the game screen.
                # Change the background image here.
                    screen.blit()
                    background_image = pygame.image.load("../img/logo.jpeg")  # Load the new image
                # Other game setup logic goes here
                # Set a flag to indicate that the game has started
                game_started = True
            
            # Draw the background image
            # background_image_resized = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
            screen.blit(background_image, (image_x, image_y))
            
            # Update the display
            pygame.display.flip()

   
if __name__=="__main__":
    main()