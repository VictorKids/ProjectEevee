import pygame, random, os

#---------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                         CLASSES                                                                                         #
#---------------------------------------------------------------------------------------------------------------------------------------------------------#
class Tile(pygame.sprite.Sprite):
    def __init__(self, filename, x, y):
        super().__init__()
        self.name = filename.split(".")[0]
        self.original_img = pygame.image.load('img/poke_sprites/' + filename)
        self.back_img = pygame.image.load('img/poke_sprites/' + filename)
        pygame.draw.rect(self.back_img, BROWN, self.back_img.get_rect())
        self.image = self.back_img
        self.rect = self.image.get_rect(topleft = (x,y))
        self.face_up = False

    def update(self):
        if self.face_up:
            self.image = self.original_img
        else:
            self.image = self.back_img
    
    def show(self):
        self.face_up = True
    
    def hide(self):
        self.face_up = False

class Game():
    def __init__(self):
        self.level = 1
        self.level_complete = False

        # sprites infos
        self.all_pokemon = [f for f in os.listdir('img/poke_sprites') if os.path.join('img/poke_sprites', f)]
        self.img_width   = 128
        self.img_height  = 128
        self.padding     =  20
        self.marging_top = 160
        self.cols  = 4
        self.rows  = 4
        self.width = 1280

        self.tiles_group = pygame.sprite.Group()

        #tiles flip & timing
        self.flipped = []
        self.frame_count = 0
        self.block_game = False

        # generate level 1
        self.generate_level(self.level)

        # music initialization
        self.is_music_playing = True
        self.sound_on  = pygame.transform.scale(pygame.image.load("img/music_on.png").convert_alpha() , (40, 40))
        self.sound_off = pygame.transform.scale(pygame.image.load("img/music_off.png").convert_alpha(), (40, 40))
        self.music_toggle = self.sound_on
        self.music_toggle_rect = self.music_toggle.get_rect(topright = (WINDOW_WIDTH -20, 20))
        # load music
        pygame.mixer.music.load('music/evolution.mp3')
        pygame.mixer.music.set_volume(.3)
        pygame.mixer.music.play()

    def update(self, game_event_list):
        self.user_input(game_event_list)
        self.draw()
        self.check_level_complete(game_event_list)

    def check_level_complete(self, game_event_list):
        if not self.block_game:
            for event in game_event_list:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for tile in self.tiles_group:
                        if tile.rect.collidepoint(event.pos):
                            self.flipped.append(tile.name)
                            tile.show()
                            if len(self.flipped) == 2:
                                if self.flipped[0] != self.flipped[1]:
                                    self.block_game = True
                                else:
                                    self.flipped = []
                                    for tile in self.tiles_group:
                                        if tile.face_up:
                                            self.level_complete = True
                                        else:
                                            self.level_complete = False
                                            break
        else:
            self.frame_count += 1
            if self.frame_count == FPS:
                self.frame_count = 0
                self.block_game = False
                for tile in self.tiles_group:
                    if tile.name in self.flipped:
                        tile.hide()
                self.flipped = []

    def generate_level(self, level):
        self.pokemon = self.select_level_pokemon(self.level)
        self.level_complete = False
        self.rows = self.level + 1
        #self.cols = 4
        self.generate_tileset(self.pokemon)

    def generate_tileset(self, pokemon):
        # ELE REAJUSTA O NUMERO DE COLUNAS E LINHAS, TALVEZ VC TENHA Q VOLTAR AQ
        TILES_WIDTH  = (self.img_width  * self.cols + self.padding * 3)
        LEFT_MARGIN  = (self.width - TILES_WIDTH)//2
        RIGHT_MARGIN = (self.width - TILES_WIDTH)//2
        #tiles = []
        self.tiles_group.empty()
        for i in range(len(pokemon)):
            x = LEFT_MARGIN + ((self.img_width + self.padding) * (i % self.cols))
            y = self.marging_top + (i // self.cols * (self.img_height + self.padding))
            tile = Tile(pokemon[i], x, y)
            self.tiles_group.add(tile)

    def select_level_pokemon(self, level):
        if   level == 1:
            poke_list = self.all_pokemon[0:4]
        elif level == 2:
            poke_list = self.all_pokemon[0:6]
        elif level == 3:
            poke_list = self.all_pokemon[0:8]
        else:
            poke_list = self.all_pokemon
        poke_list_copy = poke_list.copy()
        poke_list.extend(poke_list_copy)
        random.shuffle(poke_list)
        return poke_list

    def user_input(self, game_event_list):
        for event in game_event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # == 1 means left mouse btn
                if self.music_toggle_rect.collidepoint(pygame.mouse.get_pos()): # clicking in the music toggler
                    if self.is_music_playing:
                        self.is_music_playing = False
                        self.music_toggle = self.sound_off
                        pygame.mixer.music.pause()
                    else:
                        self.is_music_playing = True
                        self.music_toggle = self.sound_on
                        pygame.mixer.music.unpause()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.level_complete:
                    self.level += 1
                    if self.level >= 5:
                        self.level = 1
                    self.generate_level(self.level)

    def draw(self):
        screen.fill(WHITE)
        # font
        title_font   = pygame.font.Font('fonts/Pokemon Solid.ttf', 44)
        content_font = pygame.font.Font(None, 24)

        # text
        title_text   = title_font.render('Project Eevee', True, BROWN)
        title_rect   = title_text.get_rect(midtop = (WINDOW_WIDTH/2, 10))

        level_text   = content_font.render('Level: ' + str(game.level), True, BROWN)
        level_rect   = level_text.get_rect(midtop = (WINDOW_WIDTH/8, 50))

        info_text    = content_font.render('Encontre os pares de imagens semelhantes', True, BLACK)
        info_rect    = info_text.get_rect(midtop = (WINDOW_WIDTH/2, 120))

        if self.level < 4:
            next_text = content_font.render('Pressione ESPAÇO para seguir para a próxima fase', True, BLACK)
        else:
            next_text = content_font.render('Parabéns! Você venceu! Pressione ESPAÇO para jogar novamente', True, BLACK)
        next_rect = next_text.get_rect(midtop = (WINDOW_WIDTH/2, WINDOW_HEIGHT - 40))

        # print texts
        screen.blit(title_text, title_rect)
        screen.blit(level_text, level_rect)
        screen.blit(info_text, info_rect)
        if self.level_complete == True:
            screen.blit(next_text, next_rect)
        
        # print images
        screen.blit(game.music_toggle, game.music_toggle_rect)

        # print tiles
        self.tiles_group.draw(screen)
        self.tiles_group.update()
    

#---------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                     INITIALIZATIONS                                                                                     #
#---------------------------------------------------------------------------------------------------------------------------------------------------------#
pygame.init()

WINDOW_WIDTH  = 1240
WINDOW_HEIGHT = 1000

screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )

pygame.display.set_caption("Project Eevee")
icon = pygame.image.load('favicon.ico')
pygame.display.set_icon(icon)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139,69,19)

FPS = 60
clock = pygame.time.Clock()

game = Game()

#---------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                        GAME LOOP                                                                                        #
#---------------------------------------------------------------------------------------------------------------------------------------------------------#

running = True
while running:
    game_event_list = pygame.event.get()
    for event in game_event_list:
        if event.type == pygame.QUIT:
            running = False

    game.update(game_event_list)


    pygame.display.update()
    clock.tick(FPS)

pygame.quit()