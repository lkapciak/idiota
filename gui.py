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
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
    
    return screen, players, images, back_img


def get_positions(player_index):
    y_offset = 200 if player_index == 0 else HEIGHT - 350
    x_start = 200
    gap = 100
    positions = {
        'hidden': [(x_start + i * gap, y_offset) for i in range(3)],
        'open': [(x_start + i * gap, y_offset - 30) for i in range(3)],
    }
    return positions

def get_hand_positions(cards_count, player_index):
    y = 50 if player_index == 0 else HEIGHT - CARD_HEIGHT - 50

    x_step = 25
    total_width = CARD_WIDTH + max(0, cards_count - 1) * x_step
    x_start = (WIDTH - total_width) // 2

    return [(x_start + i * x_step, y) for i in range(cards_count)]

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

def render_game_state(screen, game, images, back_img, selected_cards=None, active_player_idx=0):
    if selected_cards is None:
        selected_cards = []

    def draw_card(surface, card, images, back_img, x, y, hidden=False, selected=False):
        if hidden:
            surface.blit(back_img, (x, y))
        else:
            img = images.get((card.suit, card.rank))
            if img:
                surface.blit(img, (x, y))
            else:
                pygame.draw.rect(surface, (255, 255, 255), (x, y, CARD_WIDTH, CARD_HEIGHT))
                font = pygame.font.SysFont(None, 30)
                text = font.render(str(card), True, (0, 0, 0))
                surface.blit(text, (x + 10, y + 10))

        if selected:
            pygame.draw.rect(surface, (255, 255, 0), (x - 3, y - 3, CARD_WIDTH + 6, CARD_HEIGHT + 6), 4)

    screen.fill(GREEN)
    screen.blit(back_img, (WIDTH - 200, HEIGHT // 2 - 60))

    center_card = game.table[-1] if game.table else None
    if center_card:
        draw_card(screen, center_card, images, back_img, WIDTH // 2 - CARD_WIDTH // 2, HEIGHT // 2 - CARD_HEIGHT // 2)

    for idx, hand in enumerate(game.hands):
        pos = get_positions(idx)

        for card, (x, y) in zip(hand.hidden_cards, pos['hidden']):
            draw_card(screen, card, images, back_img, x, y, hidden=True)

        for card, (x, y) in zip(hand.open_cards, pos['open']):
            draw_card(screen, card, images, back_img, x, y)

        hand_positions = get_hand_positions(len(hand.cards), idx)

        for card, (x, y) in zip(hand.cards, hand_positions):
            is_selected = (idx == active_player_idx and card in selected_cards)
            draw_y = y - 20 if is_selected else y
            draw_card(screen, card, images, back_img, x, draw_y, selected=is_selected)


def get_clicked_hand_card(mouse_pos, hand, player_index):
    positions = get_hand_positions(len(hand.cards), player_index)

    for card, (x, y) in reversed(list(zip(hand.cards, positions))):
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        if rect.collidepoint(mouse_pos):
            return card

    return None



def choose_cards_via_gui(screen, game, images, back_img, current_hand, current_table, player_index, is_legal):

    selected_cards = []
    selected_rank = None
    font = pygame.font.SysFont(None, 28)

    while True:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked_card = get_clicked_hand_card(event.pos, current_hand, player_index)

                if clicked_card is None:
                    continue

                if selected_rank is None:
                    if is_legal(current_table, clicked_card):
                        selected_rank = clicked_card.rank
                        selected_cards = [clicked_card]

                else:
                    if clicked_card.rank == selected_rank:
                        if clicked_card in selected_cards:
                            if len(selected_cards) > 1:
                                selected_cards.remove(clicked_card)
                        else:
                            selected_cards.append(clicked_card)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and selected_cards:
                    return selected_cards

                elif event.key == pygame.K_ESCAPE:
                    selected_cards = []
                    selected_rank = None

        render_game_state(
            screen,
            game,
            images,
            back_img,
            selected_cards=selected_cards,
            active_player_idx=player_index
        )

        info_lines = [
            "Kliknij legalną kartę, aby wybrać rank.",
            "Klikaj karty tego samego ranku, aby dodać/usunąć.",
            "ENTER = zagraj, ESC = wyczyść wybór"
        ]

        y = 20
        for line in info_lines:
            txt = font.render(line, True, (255, 255, 255))
            screen.blit(txt, (20, y))
            y += 28

        pygame.display.flip()


def show_temporary_message(screen, game, images, back_img, message_lines, duration_ms=3000,
                           extra_card=None, active_player_idx=0):
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 28)

    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < duration_ms:
        CLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Render current game state
        render_game_state(
            screen,
            game,
            images,
            back_img,
            selected_cards=[],
            active_player_idx=active_player_idx
        )

        overlay = pygame.Surface((WIDTH, 140), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (20, 20))
        y = 35
        for i, line in enumerate(message_lines):
            current_font = font if i == 0 else small_font
            txt = current_font.render(line, True, (255, 255, 255))
            screen.blit(txt, (40, y))
            y += 38 if i == 0 else 30

        # display extra card (last resort)
        if extra_card is not None:
            img = images.get((extra_card.suit, extra_card.rank))
            x = WIDTH // 2 + 120
            y = HEIGHT // 2 - CARD_HEIGHT // 2

            label = small_font.render("Last resort:", True, (255, 255, 0))
            screen.blit(label, (x - 10, y - 35))

            if img:
                screen.blit(img, (x, y))
            else:
                pygame.draw.rect(screen, (255, 255, 255), (x, y, CARD_WIDTH, CARD_HEIGHT))
                txt = small_font.render(str(extra_card), True, (0, 0, 0))
                screen.blit(txt, (x + 8, y + 10))

        pygame.display.flip()