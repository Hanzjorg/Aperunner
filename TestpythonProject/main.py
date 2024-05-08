import pygame
from sys import exit
from random import randint
def animation():
    global Player_Surface, Player_index
    if Player_Rect.bottom < 650:
        Player_Surface = Player_jump
    else:
        Player_index += 0.1
        if Player_index >= len(Player_walk): Player_index = 0
        Player_Surface = Player_walk[int(Player_index)]
def display_score():
    current_time = int(pygame.time.get_ticks() / 100) - start_time
    score_Surface = text_font.render(f'{current_time}', False, (64, 64, 64))
    score_Rect = score_Surface.get_rect(center=(520, 50))
    screen.blit(score_Surface, score_Rect)
    return current_time

def obsticale_movement(ostacale_list):
    if ostacale_list:
        for ostacale_rect in ostacale_list:
            ostacale_rect.x -= 7

            if ostacale_rect.bottom == 640:
                screen.blit(Snail_Surface, ostacale_rect)
            else:
                screen.blit(fly_Surface, ostacale_rect)

        ostacale_list = [ostacale for ostacale in ostacale_list if ostacale.x > -100]
        return ostacale_list
    else:
        return []

def collisions(Player,ostacale):
    if ostacale:
        for ostacale_rect in ostacale:
            if Player_Rect.colliderect(ostacale_rect): return False
    return True

pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Ape Runner")
clock = pygame.time.Clock()
text_font = pygame.font.Font("grafics/Pixeltype.ttf", 75)
game_active = False
start_time = 0
score = 0

Sky_Surface = pygame.image.load("grafics/Sky.png").convert_alpha()

Graund_Surface = pygame.image.load("grafics/graund.png").convert_alpha()
Graund_Surface_Rect = Graund_Surface.get_rect(topleft=(0, 640))

Snail_walk1 = pygame.image.load("grafics/snail1.png").convert_alpha()
Snail_walk2 = pygame.image.load("grafics/snail2.png").convert_alpha()
Snail_walk = [Snail_walk1, Snail_walk2]
Snail_walk_index = 0
Snail_Surface = Snail_walk[Snail_walk_index]

fly_walk1 = pygame.image.load("grafics/Fly1.png").convert_alpha()
fly_walk2 = pygame.image.load("grafics/Fly2.png").convert_alpha()
fly_walk = [fly_walk1, fly_walk2]
fly_walk_index = 0
fly_Surface = fly_walk[fly_walk_index]

ostacale_rect_list = []

Player_walk1 = pygame.image.load("grafics/Player1.png").convert_alpha()
Player_walk2 = pygame.image.load("grafics/Player2.png").convert_alpha()
Player_jump = pygame.image.load("grafics/Player.png").convert_alpha()
Player_walk = [Player_walk1, Player_walk2]
Player_index = 0
Player_Surface = Player_walk[Player_index]
Player_Rect = Player_Surface.get_rect(midbottom=(150, 650))
Player_gravity = 0
Player_left = False
Player_right = False

jump_audio = pygame.mixer.Sound("audio/jump.mp3")
jump_audio.set_volume(0.2)
background_audio = pygame.mixer.Sound("audio/background_music.mp3")
background_audio.set_volume(0.1)
if game_active == False:
    background_audio.play(loops=-1)

Rock_Surface = pygame.image.load("grafics/Rock1.png").convert_alpha()
Rock_Rect = Rock_Surface.get_rect(center=(500, 250))

Player_Scaled = pygame.transform.scale2x(Player_jump).convert_alpha()
Player_Scaled_Rect = Player_Scaled.get_rect(center=(500, 400))

Ape_Runner = text_font.render("Ape Runner", False, "Black")
Game_Over_Surf = text_font.render("Game Over", False, "Black")
Game_Over_Surf2 = text_font.render("Leertaste zum Spielen", False, "Black")

ostacale_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ostacale_timer, 1500)

Snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(Snail_timer, 500)

fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer, 200)

while True:
    key = pygame.key.get_pressed()

    if key[pygame.K_a] == True:
        Player_Rect.x -= 5

    if key[pygame.K_d] == True:
        Player_Rect.x += 6

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if Player_Rect.bottom == 650:
                        Player_gravity = -20
                        jump_audio.play()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if Player_Rect.bottom == 650:
                    Player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 100)

        if game_active:
            if event.type == ostacale_timer:
                if randint(0, 1):
                    ostacale_rect_list.append(Snail_Surface.get_rect(midbottom=(randint(1050, 1500), 640)))
                else:
                    ostacale_rect_list.append(fly_Surface.get_rect(midbottom=(randint(1050, 1500), 500)))

            if event.type == Snail_timer:
                if Snail_walk_index == 0: Snail_walk_index = 1
                else: Snail_walk_index = 0
                Snail_Surface = Snail_walk[Snail_walk_index]

            if event.type == fly_timer:
                if fly_walk_index == 0: fly_walk_index = 1
                else: fly_walk_index = 0
                fly_Surface = fly_walk[fly_walk_index]

    if Player_left == True:
        Player_Rect.x -= 5

    if Player_right == True:
        Player_Rect.x += 5

    if game_active:
        background_audio.set_volume(0)
        screen.blit(Sky_Surface, (0, 0))
        screen.blit(Graund_Surface, Graund_Surface_Rect)
        screen.blit(Rock_Surface, Rock_Rect)

        score = display_score()

        Player_gravity += 0.8
        Player_Rect.y += Player_gravity
        if Player_Rect.bottom >= 650:
            Player_Rect.bottom = 650
        screen.blit(Player_Surface, Player_Rect)

        if Player_Rect.left <= 0:
            Player_Rect.left = 5

        if Player_Rect.x >= 800:
            Player_Rect.x = 800

        Rock_Rect.y += 9
        if Rock_Rect.y >= 850:
            Rock_Rect.midbottom = (randint(0, 800), 0)

        ostacale_rect_list = obsticale_movement(ostacale_rect_list)

        animation()

        game_active = collisions(Player_Rect, ostacale_rect_list)


        if Player_Rect.colliderect(Rock_Rect):
            game_active = False

    else:
        background_audio.set_volume(0.1)
        Rock_Rect.midbottom = (randint(0, 800), 0)
        screen.fill("Green")
        ostacale_rect_list.clear()
        Player_Rect.midbottom=(150, 650)

        if score == 0:
            screen.blit(Game_Over_Surf2, (250, 600))
            screen.blit(Ape_Runner, (350, 100))
        else:
            Game_Over_Score = text_font.render(f"Dein Score: {score}", False, "Black")
            screen.blit(Game_Over_Score, (350, 600))
            screen.blit(Game_Over_Surf, (400, 200))

        screen.blit(Player_Scaled, Player_Scaled_Rect)

    pygame.display.update()
    clock.tick(60)
