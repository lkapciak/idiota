import pygame, os, sys
from core import *

WIDTH, HEIGHT = 1200, 800
CARD_WIDTH = 80
CARD_HEIGHT = 120
BACK_IMG = 'BACK.svg'
CLOCK = pygame.time.Clock()
FPS = 40

# colors 
GREEN = (34, 139, 34)

def gui_init():
    def load_card_images():
        back_img = pygame.image.load(f'images/{BACK_IMG}')
        back_img = pygame.transform.scale(back_img, (CARD_WIDTH, CARD_HEIGHT))
        rank_to_number = {
        'J': '11',
        'Q': '12',
        'K': '13',
        'A': '14'
        }
        images = {}
        for suit in Suit:
            for rank in Rank:
                rank_str = rank.value if rank.value.isdigit() else rank_to_number[rank.value]
                filename = f"{suit.name[:-1]}-{rank_str}.svg"
                path = os.path.join('images', filename)
                
                if os.path.exists(path):
                    img = pygame.image.load(path)
                    img = pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))
                    images[(suit, rank)] = img
        return images, back_img

    def screen_init():
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Idiota")
        font = pygame.font.SysFont(None, 36)
        return screen, font

    def get_players_via_gui(screen, font):
        players = []
        current_text = ""
        asking_players = True

        info_text = "Enter player name, ENTER to confirm, ESC to start game"

        while asking_players:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    print(event.key)
                    if event.key == pygame.K_ESCAPE:
                        if len(players) >= 2:
                            asking_players = False

                    elif event.key == pygame.K_RETURN:
                        if current_text and current_text not in players:
                            players.append(current_text)
                            current_text = ""

                    elif event.key == pygame.K_BACKSPACE:
                        current_text = current_text[:-1]

                    else:
                        current_text += event.unicode

            screen.fill((30, 120, 30))

            info_surface = font.render(info_text, True, (255, 255, 255))
            screen.blit(info_surface, (40, 40))

            input_surface = font.render("Name: " + current_text, True, (255, 255, 0))
            screen.blit(input_surface, (40, 100))

            y = 160
            for p in players:
                player_surface = font.render(p, True, (255, 255, 255))
                screen.blit(player_surface, (60, y))
                y += 30

            pygame.display.flip()

        return players
    
    images, back_img = load_card_images()
    screen, font = screen_init()
    players = get_players_via_gui(screen, font)
    
    return players, images, back_img


def serve_gui(screen, game, images, back_img):
    
    def draw_card(surface, card, images, back_img, x, y, hidden=False):
        if hidden:
            surface.blit(back_img, (x, y))
        else:
            img = images.get((card.suit, card.rank))
            if img:
                surface.blit(img, (x, y))
            else:
                pygame.draw.rect(surface, (255,255,255), (x, y, CARD_WIDTH, CARD_HEIGHT))
                font = pygame.font.SysFont(None, 30)
                text = font.render(str(card), True, (0,0,0))
                surface.blit(text, (x+10, y+10))

    def get_positions(player_index):
        y_offset = 200 if player_index == 0 else HEIGHT-350
        x_start = 200
        gap = 100
        positions = {
            'hidden': [(x_start + i*gap, y_offset) for i in range(3)],
            'open': [(x_start + i*gap, y_offset - 30) for i in range(3)],
            'hand': [(x_start + i*gap, y_offset - 150 if player_index==0 else y_offset+150) for i in range(3)]
        }
        return positions
    
    running = True
    while running:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(GREEN)
        screen.blit(back_img, (WIDTH-200, HEIGHT//2-60))

        if game.table:
            center_card = game.table[-1]
        else:
            center_card = None
        
        if center_card:
            draw_card(screen, center_card, WIDTH//2-CARD_WIDTH//2, HEIGHT//2-CARD_HEIGHT//2)

        for idx, hand in enumerate(game.hands):
            pos = get_positions(idx)
            for card, (x, y) in zip(hand.hidden_cards, pos['hidden']):
                draw_card(screen, card, images, back_img, x, y, hidden=True)
            for card, (x, y) in zip(hand.open_cards, pos['open']):
                draw_card(screen, card, images, back_img, x, y)
            for card, (x, y) in zip(hand.cards, pos['hand']):
                draw_card(screen, card, images, back_img, x, y)

        pygame.display.flip()

def update_game_screen():
    pass