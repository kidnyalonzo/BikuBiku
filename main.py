import pygame as pg
from sprites import *
from constants import *
from dir import *

class Game:

    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.light_mask = pg.image.load(path.join(img_dir, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()
        self.light_mask_2 = pg.image.load(path.join(img_dir, LIGHT_MASK_2)).convert_alpha()
        self.light_mask_2 = pg.transform.scale(self.light_mask_2, LIGHT_RADIUS_2)
        self.light_rect_2 = self.light_mask_2.get_rect()
        self.fog = pg.Surface((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.icon_tempo = pg.image.load(path.join(img_dir, ICON))
        pg.display.set_icon(self.icon_tempo)
        self.font = font_1

        '''sounds'''
        for snd in jump_list:
            jump_snds.append(pg.mixer.Sound(path.join(snd_dir, snd)))
        for snd in hover_list:
            hover_snds.append(pg.mixer.Sound(path.join(snd_dir, snd)))
        self.soundChannel_menu = pg.mixer.Channel(0)
        self.soundChannel_in_game = pg.mixer.Channel(1)
        self.double_jump = 0
        self.double_jump_p1 = 0
        self.double_jump_p2 = 0

    def onep_game(self):
        self.score = 0
        self.game_sprites = pg.sprite.Group()
        self.platform_sprites = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mob_sprites = pg.sprite.Group()
        self.player = Player(self, 192, 224, pg.K_RIGHT, pg.K_LEFT)
        self.game_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(self, *plat)
            self.game_sprites.add(p)
            self.platform_sprites.add(p)
        playing = True
        while playing:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    if playing:
                        self.pause_screen()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        if playing:
                            self.pause_screen()
                    if self.double_jump <= 1:
                        if event.key == pg.K_UP:
                            self.double_jump += 1
                            self.player.jump()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_UP:
                        self.player.jump_cut()

            '''Update Section'''
            self.game_sprites.update()
            if self.player.vel.y > 0:
                hit = pg.sprite.spritecollide(self.player, self.platform_sprites, False)
                if hit:
                    lowest = hit[0]
                    for h in hit:
                        if h.rect.bottom > lowest.rect.bottom:
                            lowest = h
                    if self.player.rect.centerx < lowest.rect.right + 5 and self.player.rect.centerx >  lowest.rect.left -5:
                        if self.player.pos.y <= lowest.rect.bottom:
                            self.player.pos.y = lowest.rect.top
                            self.double_jump = 0
                            self.player.jumping = False
                            self.player.vel.y = 0

            if self.player.rect.top <= HEIGHT / 2:
                self.player.pos.y += abs(self.player.vel.y)
                for plat in self.platform_sprites:
                    plat.rect.y += abs(self.player.vel.y)
                    if plat.rect.top >= HEIGHT:
                        self.score += 5
                        plat.kill()
            pow_hit = pg.sprite.spritecollide(self.player,self.powerups,True, pg.sprite.collide_mask)
            for pow in pow_hit:
                if pow.type == 'boost':
                    self.double_jump = 2
                    self.juming = False
                    self.player.vel.y = BOOST_POWER

            while len(self.platform_sprites) < 3:
                self.random_length = plat_width[random.randrange(0,3,1)]
                p = Platform(self, random.randrange(0, WIDTH - self.random_length), random.randrange(-30, -20),
                             self.random_length, 30 )

                self.platform_sprites.add(p)
                self.game_sprites.add(p)
            if self.player.rect.top > HEIGHT:
                playing = False

            '''Draw'''
            self.screen.fill(WHITE)
            self.game_sprites.draw(self.screen)
            self.platform_sprites.draw(self.screen)
            self.render_fog((self.player.pos.x, self.player.pos.y - 16),self.light_mask,self.light_rect)
            self.draw_text(self.screen, str(self.score), 20, 10, 2, font_1, RED, True, 0)
            pg.display.flip()

    def twop_game(self):
        self.p1_score = 0
        self.p2_score = 0
        self.game_sprites = pg.sprite.Group()
        self.platform_sprites = pg.sprite.Group()
        self.player_p1 = Player(self, 192, 224, pg.K_RIGHT, pg.K_LEFT)
        self.player_p2 = Player(self, 0, 32, pg.K_d, pg.K_a)
        self.double_jump_p1 = 0
        self.double_jump_p2 = 0
        for plat in PLATFORM_LIST:
            p = Platform(self, *plat)
            self.game_sprites.add(p)
            self.platform_sprites.add(p)
        playing = True
        self.game_sprites.add(self.player_p1)
        self.game_sprites.add(self.player_p2)
        while playing:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    if playing:
                        self.pause_screen()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        if playing:
                            self.pause_screen()
                    if self.double_jump_p1 <= 1:
                        if event.key == pg.K_UP:
                            self.double_jump_p1 += 1
                            self.player_p1.jump()
                    if self.double_jump_p2 <= 1:
                        if event.key == pg.K_w:
                            self.double_jump_p2 += 1
                            self.player_p2.jump()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_UP:
                        self.player_p1.jump_cut()
                    if event.key == pg.K_w:
                        self.player_p2.jump_cut()

            '''Update Section'''
            self.game_sprites.update()
            if self.player_p1.vel.y > 0:
                hit = pg.sprite.spritecollide(self.player_p1, self.platform_sprites, False)
                if hit:
                    lowest = hit[0]
                    for h in hit:
                        if h.rect.bottom > lowest.rect.bottom:
                            lowest = h
                    if self.player_p1.rect.centerx < lowest.rect.right + 5 and self.player_p1.rect.centerx > lowest.rect.left - 5:
                        if self.player_p1.pos.y <= lowest.rect.bottom:
                            self.player_p1.pos.y = lowest.rect.top
                            self.double_jump_p1 = 0
                            self.player_p1.jumping = False
                            self.player_p1.vel.y = 0
            if self.player_p1.rect.top <= HEIGHT / 2:
                self.player_p1.pos.y += abs(self.player_p1.vel.y)
                for plat in self.platform_sprites:
                    plat.rect.y += abs(self.player_p1.vel.y)
                    if plat.rect.top >= HEIGHT:
                        self.p1_score += 5
                        plat.kill()

            while len(self.platform_sprites) < 3:
                self.random_length = plat_width[random.randrange(0, 3, 1)]
                p = Platform(self, random.randrange(0, WIDTH - self.random_length), random.randrange(-30, -20),
                             self.random_length, 30)
                self.platform_sprites.add(p)
                self.game_sprites.add(p)
            if self.player_p1.rect.top > HEIGHT:
                playing = False

            if self.player_p2.vel.y > 0:
                hit = pg.sprite.spritecollide(self.player_p2, self.platform_sprites, False)
                if hit:
                    lowest = hit[0]
                    for h in hit:
                        if h.rect.bottom > lowest.rect.bottom:
                            lowest = h
                    if self.player_p2.rect.centerx < lowest.rect.right + 5 and self.player_p2.rect.centerx > lowest.rect.left - 5:
                        if self.player_p2.pos.y <= lowest.rect.bottom:
                            self.player_p2.pos.y = lowest.rect.top
                            self.double_jump_p2 = 0
                            self.player_p2.jumping = False
                            self.player_p2.vel.y = 0
            if self.player_p2.rect.top <= HEIGHT / 2:
                self.player_p2.pos.y += abs(self.player_p2.vel.y)
                for plat in self.platform_sprites:
                    plat.rect.y += abs(self.player_p2.vel.y)
                    if plat.rect.top >= HEIGHT:
                        self.p2_score += 5
                        plat.kill()

            if self.player_p2.rect.top > HEIGHT:
                playing = False

            '''Draw'''
            self.screen.fill(WHITE)
            self.game_sprites.draw(self.screen)
            self.platform_sprites.draw(self.screen)
            self.render_fog((self.player_p1.pos.x, self.player_p1.pos.y - 16), self.light_mask_2, self.light_rect_2)
            self.render_fog((self.player_p2.pos.x, self.player_p2.pos.y - 16), self.light_mask_2, self.light_rect_2)
            self.draw_text(self.screen, str(self.p1_score), 20, 10, 2, font_1, RED, True, 0)
            self.draw_text(self.screen, str(self.p2_score), 20, 10, 25, font_1, GREEN, True, 0)
            pg.display.flip()

    def draw_text(self, surf, text, size, x, y, font_type, color, antialias, alignment0123):
        font = pg.font.Font(path.join(user_dir,font_type), size)
        text_surface = font.render(text, antialias, color)
        text_rect = text_surface.get_rect()
        text_align = alignment0123
        if text_align == 0:
            text_rect.topleft = (x, y)
        if text_align == 1:
            text_rect.midtop = (x, y)
        if text_align == 2:
            text_rect.topright = (x, y)
        if text_align == 3:
            text_rect.center = (x, y)
        surf.blit(text_surface, text_rect)

    def show_start_screen(self):
        board_boxes = []
        one_mode = Box(self,0,1,(WIDTH/ 2, 260))
        two_mode = Box(self, 2, 3, (WIDTH / 2, 310))
        sett = Box(self, 4, 5, (WIDTH / 2, 360))
        stor = Box(self, 6, 7, (WIDTH / 2, 410))
        creds = Box(self, 8, 9, (WIDTH / 2, 460))
        board_boxes.append(one_mode)
        board_boxes.append(two_mode)
        board_boxes.append(sett)
        board_boxes.append(stor)
        board_boxes.append(creds)
        waiting = True
        # running bool
        self.one_mode_running = False
        self.two_mode_running = False
        self.settings_running = False
        self.store_running = False
        self.credits_running = False
        self.help_running = False
        while waiting:
            self.screen.fill(WHITE)
            self.draw_text(self.screen, "BIKU BIKU", 60, WIDTH /2, 104, font_1, BLACK, True, 3)
            title2_fill = pg.Rect(39, 133, 372, 63)
            pg.draw.rect(self.screen, BLACK, title2_fill)
            self.draw_text(self.screen, "BIKU BIKU", 60, WIDTH / 2, 165, font_1, WHITE, True, 3)
            self.draw_text(self.screen, "DEMO", 40, WIDTH / 2, 510, font_1, RED, True, 3)

            self.draw_text(self.screen, "arrow keys for movement, press up arrow", 12, WIDTH / 2, 535, font_1, BLACK, True, 3)
            self.draw_text(self.screen, "twice to double jump", 12, WIDTH / 2, 549, font_1, BLACK,
                           True, 3)

            self.clock.tick(FPS)
            pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if one_mode.rect.collidepoint(pos):
                            waiting = False
                            self.one_mode_running = True
                        if two_mode.rect.collidepoint(pos):
                            waiting = False
                            self.two_mode_running = True
                        if creds.rect.collidepoint(pos):
                            pass
                            #waiting = False
                            #self.credits_running = True

            for box in board_boxes:
                box.hoverd = box.rect.collidepoint(pos)

            for box in board_boxes:
                box.draw(self.screen)

            pg.display.flip()
            pg.display.update()

    def pause_screen(self):
        pass

    def show_go_screen(self):
        board_boxes = []
        back = Box(self, 12, 13, (WIDTH / 2, 260))
        retry = Box(self, 10, 11, (WIDTH / 2, 310))
        board_boxes.append(back)
        board_boxes.append(retry)
        waiting = True
        while waiting:
            self.screen.fill(WHITE)
            self.draw_text(self.screen, "GAME", 60, WIDTH / 2, 104, font_1, BLACK, True, 3)
            title2_fill = pg.Rect(WIDTH/2 - 100, 133, 200, 63)
            pg.draw.rect(self.screen, BLACK, title2_fill)
            self.draw_text(self.screen, "OVER", 60, WIDTH / 2, 165, font_1, WHITE, True, 3)
            self.clock.tick(FPS)
            pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pass
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        waiting = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if back.rect.collidepoint(pos):
                            waiting = False
                        if retry.rect.collidepoint(pos):
                            self.onep_game()

            for box in board_boxes:
                box.hoverd = box.rect.collidepoint(pos)

            for box in board_boxes:
                box.draw(self.screen)

            pg.display.flip()
            pg.display.update()

    def render_fog(self, center_pos, light_mask_type, light_rect):
        self.fog.fill(NIGHT_COLOR)
        light_rect.center = center_pos
        self.fog.blit(light_mask_type, light_rect)
        self.screen.blit(self.fog, (0,0), special_flags=pg.BLEND_MULT)

    def settings(self):
        pass
    def store(self):
        pass

    def credits(self):
        running = True
        while running:
            self.screen.fill(BLACK)
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False


            pg.display.flip()
            pg.display.update()

g = Game()

g.show_start_screen()
while g.one_mode_running:
    g.onep_game()
    g.show_go_screen()
    g.show_start_screen()
while g.two_mode_running:
    g.twop_game()
    g.show_start_screen()


pg.quit()