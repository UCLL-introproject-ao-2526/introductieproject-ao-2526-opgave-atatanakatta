# debugging walkthrough or debugging reasoning.
# black jack in python wth pygame!
#
import copy
import random
import pygame

pygame.init() # zorgt voor opstart van pygame
# game variables
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['♠', '♥', '♦', '♣'] #added
one_deck = [f"{rank}{suit}" for suit in suits for rank in cards] #added
decks = 4
WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Blackjack!')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 26)
smaller_font = pygame.font.Font('freesansbold.ttf', 26)
active = False
# win, loss, draw/push
records = [0, 0, 0]
player_name = "" # added naam opslag
name_input = True # added als true we zitten op name screen , false we zijn aant spelen.
cursor_visible = True     # added voor zichtbare cursor
cursor_timer = 0          # added telt de frames van de cursor
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
reveal_dealer = False
hand_active = False
outcome = 0
add_score = False
results = ['', 'PLAYER BUSTED', 'Player WINS!', 'DEALER WINS', 'TIE']

# MIJN TOEVOEGING
# kleuren
TABLE_GREEN = (30, 110, 60)
TABLE_DARK = (20, 80, 40)
CARD_WHITE = (250, 248, 245)
RED_CARD = (180, 30, 30)
BLACK_CARD = (30, 30, 30)
GOLD = (218, 165, 32)
BUTTON_BG = (240, 240, 240)
BUTTON_HOVER = (255, 255, 255)
BUTTON_BORDER = (180, 180, 180)
SHADOW = (0, 0, 0, 80)

# Add Helper Functie
def get_rank(card):
    return card[:-1] #added slice die alles teruggeeft behalve het laatste element.

def get_suit(card):
    return card[-1]

def get_suit_color(card):
    if '♥' in card or '♦' in card:
        return RED_CARD
    else:
        return BLACK_CARD

# deal cards by selecting randomly from deck, and make function for one card at a time
def deal_cards(current_hand, current_deck):
    if not current_deck:
        return current_hand, current_deck
    
    card = random.randint(0, len(current_deck) - 1)
    current_hand.append(current_deck[card - 1])
    current_deck.pop(card)
    return current_hand, current_deck


# draw scores for player and dealer on screen
def draw_scores(player, dealer):
    screen.blit(font.render(f'Score[{player}]', True, 'red'), (350, 400))
    if reveal_dealer:
        screen.blit(font.render(f'Score[{dealer}]', True, 'red'), (350, 100))


# draw cards visually onto screen
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
        screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 465 + 5 * i))
        screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 635 + 5 * i))
        pygame.draw.rect(screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)
    

    # if player hasn't finished turn, dealer will hide one card
    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 335 + 5 * i))
        else:
            screen.blit(font.render('?', True, 'black'), (75 + 70 * i, 165 + 5 * i))
            screen.blit(font.render('?', True, 'black'), (75 + 70 * i, 335 + 5 * i))
        pygame.draw.rect(screen, 'blue', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)


# pass in player or dealer hand and get best score possible
def calculate_score(hand): #added betere logica voor ace
    hand_score = 0
    aces_count = sum(1 for c in hand if c.startswith('A'))
    
    for card in hand:
        rank = get_rank(card)
        if rank in ['J', 'Q', 'K']:
            hand_score += 10
        elif rank == 'A':
            hand_score += 11
        else:
            hand_score += int(rank)
    
    # Reduce Aces from 11 to 1 as needed
    while hand_score > 21 and aces_count > 0:
        hand_score -= 10
        aces_count -= 1
    return hand_score


# draw game conditions and buttons
def draw_game(act, record, result):
    button_list = []
    # initially on startup (not active) only option is to deal new hand
    if not act:                                 # [x, y, button_width, button_height]
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 0, 5) # button
        pygame.draw.rect(screen, 'green',        [150, 20, 300, 100], 3, 5) # rand
        deal_text = font.render('DEAL', True, 'black')
        text_rect = deal_text.get_rect(center = deal.center)
        screen.blit(deal_text, text_rect)
        button_list.append(deal)

    # once game started, shot hit and stand buttons and win/loss records
    else:
        # HIT knop #[x, y, breedte, hoogte]
        hit = pygame.draw.rect(screen, 'white', [390, 750, 200, 70], 0, 5) # button
        pygame.draw.rect(screen, 'green', [390, 750, 200, 70], 3, 5) # rand
        hit_text = font.render('HIT ME', True, 'black')
        text_rect = hit_text.get_rect(center = hit.center) ### tekst automatisch centreren
        screen.blit(hit_text, text_rect)  # dynamisch gecentreerd in knop
        button_list.append(hit)
        # STAND knop #[x, y, breedte, hoogte]
        stand = pygame.draw.rect(screen, 'white', [10, 750, 200, 70], 0, 5) 
        pygame.draw.rect(screen, 'green', [10, 750, 200, 70], 3, 5)
        stand_text = font.render('STAND', True, 'black')
        text_rect = stand_text.get_rect(center = stand.center) ### tekst automatisch centreren
        screen.blit(stand_text, text_rect)  # gecentreerd in knop
        button_list.append(stand)
        
        score_text = smaller_font.render(f'Win: {record[0]}   Loss: {record[1]}   Draw: {record[2]}', True, 'white')
        screen.blit(score_text, (100, 50,)) # "Wins: 0 Losses: 0 Draws: 0" 
    # if there is an outcome for the hand that was played, display a restart button and tell user what happened
    if result != 0:
        screen.blit(font.render(results[result], True, 'white'), (15, 25))
        deal = pygame.draw.rect(screen, 'white', [150, 220, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 220, 300, 100], 3, 5)
        pygame.draw.rect(screen, 'black', [153, 223, 294, 94], 3, 5)
        deal_text = font.render('NEW HAND', True, 'black')
        screen.blit(deal_text, (165, 250))
        button_list.append(deal)
    return button_list


# check endgame conditions function
def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    # check end game scenarios is player has stood, busted or blackjacked
    # result 1- player bust, 2-win, 3-loss, 4-push
    if not hand_act and deal_score >= 17: # check als dealer klaar is met uithalen
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
    return result, totals, add


### MAIN GAME LOOP ###
run = True
while run:
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)

    # event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # NAME INPUT EVENT
        if name_input:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1] # bevestigd de naam alleen als er iets getypts is.
                elif event.key == pygame.K_RETURN and player_name.strip():
                    name_input = False
                else:
                    player_name += event.unicode
            continue

        # Keyboard inputs
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(one_deck * decks)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    outcome = 0
                    add_score = True
            else:
                # if player can hit, allow them to draw a card
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                # allow player to end turn (stand)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(one_deck * decks)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0

    # GAME LOGICA
    # if player busts, automatically end turn - treat like a stand
    if not name_input:
        if hand_active and player_score >= 21:
            hand_active = False
            reveal_dealer = True

        outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)
    
    # DRAW NAME INPUT SCREEN
    if name_input:
        # --- NAAM INVOER SCHERM ---
        screen.fill(TABLE_GREEN)
        prompt = font.render("Player", True, 'white')
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 - 100))
        input_box = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 25, 400, 60)
        pygame.draw.rect(screen, (250, 250, 250), input_box, border_radius=10)
        pygame.draw.rect(screen, GOLD, input_box, 1, border_radius=2)
        
        # Blinkende cursor
        cursor_timer += 1
        if cursor_timer > 60:
            cursor_visible = not cursor_visible
            cursor_timer = 0
        display_text = player_name + ("|" if cursor_visible else "")
        name_surface = font.render(display_text, True, 'black')
        screen.blit(name_surface, (input_box.x + 15, input_box.centery - name_surface.get_height() // 2))
        hint = smaller_font.render("Press ENTER to start", True, (200, 200, 200))
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 60))
    
    else:
        # BLACKJACK TAFEL
        screen.fill(TABLE_GREEN)
        pygame.draw.ellipse(screen, TABLE_DARK, [50, 80, WIDTH - 100, HEIGHT - 160])
        pygame.draw.ellipse(screen, GOLD, [50, 80, WIDTH - 100, HEIGHT - 160], 2)
        
        # Labels
        if player_name:
            p_label = smaller_font.render(f"{player_name.upper()}", True, 'white')
        else:
            p_label = smaller_font.render('YOUR HAND', True, 'white')
        
        d_label = smaller_font.render('DEALER', True, 'white')
        screen.blit(d_label, (WIDTH // 2 - d_label.get_width() // 2, 90))
        screen.blit(p_label, (WIDTH // 2 - p_label.get_width() // 2, 390))
        
        # Initial deal
        if initial_deal:
            for i in range(2):
                my_hand, game_deck = deal_cards(my_hand, game_deck)
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            initial_deal = False
        
        # Game actief
        if active:
            player_score = calculate_score(my_hand)
            draw_cards(my_hand, dealer_hand, reveal_dealer)
            if reveal_dealer:
                dealer_score = calculate_score(dealer_hand)
                if dealer_score < 17:
                    dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            draw_scores(player_score, dealer_score)
        buttons = draw_game(active, records, outcome)
    pygame.display.flip()
pygame.quit()