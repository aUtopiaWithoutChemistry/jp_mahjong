import pygame
from const import TILE_RATIO
from game import Game
from rules import Rule

WIDTH, HEIGHT = 1200, 900
EDGE = 20
INNER_WIDTH = WIDTH - 2 * EDGE
TILE_WIDTH = 0.7 * HEIGHT / TILE_RATIO
TILE_HEIGHT = HEIGHT // TILE_RATIO

def create_game():
    game = Game(WIDTH, HEIGHT, TILE_WIDTH, TILE_HEIGHT)
# define a main function
def main():
    """ in main game loop, the code take the rendering task, this will render players'
        tiles and all the movement player can take. All the date will be collect from
        game and player object, in this loop, we can only call their method rather
        than write the logic.
    """
    global game_obj, event
    # initialize the pygame module
    pygame.init()
    ruler = Rule()

    # load and set the logo
    logo = pygame.image.load('../img/logo.jpeg')
    pygame.display.set_icon(logo)
    pygame.display.set_caption('Aho Mahjong')

    # WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0]
    WIDTH, HEIGHT = 1200, 900
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    WIDTH, HEIGHT = screen.get_size()

    # create a surface on screen that has the size of 1280 x 960
    # screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen_rect = screen.get_rect()

    # load the background image for start page, and convert it to a pygame image object.
    start_background_image = pygame.image.load('../img/start_page.jpeg').convert_alpha()
    start_background_rect = start_background_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    # create a font
    title_font = pygame.font.Font(None, 100)
    normal_font = pygame.font.Font(None, 50)

    def draw_exit(screen):
        # draw exit button
        WIDTH, HEIGHT = screen.get_size()
        font = pygame.font.Font(None, 30)
        text_surf = font.render('Exit', True, 'black')
        button_width = text_surf.get_width() + 20
        button_height = text_surf.get_height() + 20
        exit_button_rect = pygame.Rect(WIDTH - button_width, 0, button_width, button_height)
        text_rect = text_surf.get_rect(center=exit_button_rect.center)
        pygame.draw.rect(screen, 'white', exit_button_rect, border_radius=10)
        screen.blit(text_surf, text_rect)
        running = True

        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and \
                exit_button_rect.collidepoint(mouse_pos):
            running = False
        elif exit_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, 'yellow', exit_button_rect, border_radius=10)

        screen.blit(text_surf, text_rect)
        return running

    def draw_button(word):
        """ Draw button on screen, player will trigger corresponding function by
            click the button
            :param word: str
            :param func: func
            :return: None
        """
        button_surf = normal_font.render(word, True, 'red')
        button_rect = button_surf.get_rect(topleft=(920, 820))
        pygame.draw.rect(screen, 'orange', button_rect, border_radius=10)
        screen.blit(button_surf, button_rect)
        if button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            game_obj.players[0].sort_tiles()
        pass

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
                # exit the main loop
                running = False

        # keep the loop running 60 frame per second
        clock.tick(30)

        running = draw_exit(screen)
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
            title_rect = title_surf.get_rect(center=(WIDTH // 2, 100))
            screen.blit(title_surf, title_rect)

            # display the start button
            start_button_surf = title_font.render('Start game!', True, 'black')
            start_button_rect = start_button_surf.get_rect(bottomright=(WIDTH, HEIGHT))
            pygame.draw.rect(screen, 'white', start_button_rect, border_radius=20)

            # check if there are mouseclick in this rectangle
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and \
                    start_button_rect.collidepoint(mouse_pos):
                # create a game object
                game_obj = Game(SCREEN_HEIGHT=HEIGHT, display=screen)
                ruler.set_game(game_obj)

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
                height to show it has been chosen. Every time that user could 
                have some movement chooses like chi, peng, there will be a small
                button to show the movement chooses. After user click the button,
                then this movement will be done and next player will play. After 
                at least one player finished hu, then game will change to check
                point page. 
            '''
            # game start
            if not init_state:
                game_obj.start_ju()
                init_state = True
            else:
                game_obj.gaming()
            # clear the screen, black color
            pygame.draw.rect(screen, 'black', screen_rect)
            running = draw_exit(screen)

            # draw the mahjong table
            table_rect = pygame.Rect(0, 0, HEIGHT, HEIGHT)
            inner_rect = pygame.Rect(EDGE, EDGE, HEIGHT - EDGE * 2, HEIGHT - EDGE * 2)
            inner_color = pygame.Color(79, 164, 133)
            pygame.draw.rect(screen, inner_color, inner_rect)
            pygame.draw.rect(screen, 'brown', table_rect, width=EDGE, border_radius=EDGE)
            pygame.draw.line(screen, 'black', (EDGE, EDGE), (HEIGHT - EDGE, HEIGHT - EDGE))
            pygame.draw.line(screen, 'black', (EDGE, HEIGHT - EDGE), (HEIGHT - EDGE, EDGE))

            # draw the region to store waste tiles
            waste_tiles_rect = pygame.Rect(0, 0, TILE_WIDTH * 6, TILE_WIDTH * 6)
            waste_tiles_rect.center = (HEIGHT // 2, HEIGHT // 2)
            pygame.draw.rect(screen, 'black', waste_tiles_rect, width=1)

            # show current player's tile
            for i in range(4):
                game_obj.players[0].display_my_tiles(screen, HEIGHT, direction=i)

            # show sort button
            draw_button('sort')

            # show discard button
            button_surf = normal_font.render('Sort', True, 'red')
            button_rect = button_surf.get_rect(topleft=(920, 720))
            pygame.draw.rect(screen, 'orange', button_rect, border_radius=10)
            screen.blit(button_surf, button_rect)
            if button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                game_obj.players[0].discard()

            # update the display
            pygame.display.update()

        # check point page
        elif game_state == 'check_point':
            """ in the check point page, user can see how much points each player 
                earns from winning the game, and also see the winner of the game.
                After checking the points, user can click the continue button to 
                go to next round, if this is the last round, user can click the
                end button to end the game.
            """

            pass

        # end page
        elif game_state == 'end':
            ''' in the end page, user can see the final score of each player, and 
                the winner of the game. After the game is over, user can click next
                button to start a new game or exit button to quit the game.
            '''

            pass


if __name__ == '__main__':
    main()
