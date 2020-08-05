import pygame as pg
from constants import *
from dir import *

vec = pg.math.Vector2

class SpriteSheet(object):

    def __init__(self, file):
        self.sprite_sheet = pg.image.load(path.join(img_dir, file)).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface([width, height], ).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(GREEN)
        return image


class Player(pg.sprite.Sprite):
    def __init__(self, game, line_1, line_2, right_key, left_key):
        pg.sprite.Sprite.__init__(self)
        super().__init__()
        sprite_sheet = SpriteSheet("player_list.png")
        self.sprite = [
            sprite_sheet.get_image(0, line_1, 32, 32),
            sprite_sheet.get_image(32, line_1, 32, 32),
            sprite_sheet.get_image(64, line_1, 32, 32),
            sprite_sheet.get_image(96, line_1, 32, 32),
            sprite_sheet.get_image(128, line_1, 32, 32),
            sprite_sheet.get_image(160, line_1, 32, 32),
            sprite_sheet.get_image(192, line_1, 32, 32),
            sprite_sheet.get_image(224, line_1, 32, 32),
            sprite_sheet.get_image(0, line_2, 32, 32),
            sprite_sheet.get_image(32, line_2, 32, 32),
            sprite_sheet.get_image(64, line_2, 32, 32),
            sprite_sheet.get_image(96, line_2, 32, 32),
            sprite_sheet.get_image(128, line_2, 32, 32),
            sprite_sheet.get_image(160, line_2, 32, 32),
            sprite_sheet.get_image(192, line_2, 32, 32),
            sprite_sheet.get_image(224, line_2, 32, 32)
        ]
        self.current_sprite_1 = 0
        self.current_sprite_2 = 8
        self.game = game
        self.image = self.sprite[self.current_sprite_1]
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH / 2, HEIGHT - 62)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.last_time = pg.time.get_ticks()
        self.frame_rate_1 = 83
        self.frame_rate_2 = 50
        self.last_button_hit = "right"
        self.jumping = False
        self.right_key = right_key
        self.left_key = left_key

    def update(self):
        now = pg.time.get_ticks()
        self.acc = vec(0, PLAYER_GRAV)
        keystate = pg.key.get_pressed()
        if not keystate[pg.K_RIGHT] or not keystate[pg.K_LEFT] or not keystate[pg.K_SPACE]:
            if self.last_button_hit == "right":
                if now - self.last_time > self.frame_rate_1:
                    self.last_time = pg.time.get_ticks()
                    self.current_sprite_1 += 1
                    if self.current_sprite_1 > 7:
                        self.current_sprite_1 = 0
                    self.image = self.sprite[self.current_sprite_1]
            if self.last_button_hit == "left":
                if now - self.last_time > self.frame_rate_1:
                    self.last_time = pg.time.get_ticks()
                    self.current_sprite_1 += 1
                    if self.current_sprite_1 > 7:
                        self.current_sprite_1 = 0
                    to_flip = self.sprite[self.current_sprite_1]
                    self.image = pg.transform.flip(to_flip, True, False)
        if keystate[self.right_key]:
            self.acc.x = PLAYER_ACC
            self.last_button_hit = "right"
            if now - self.last_time > self.frame_rate_2:
                self.last_time = pg.time.get_ticks()
                self.current_sprite_2 += 1
                if self.current_sprite_2 > 15:
                    self.current_sprite_2 = 8
                self.image = self.sprite[self.current_sprite_2]
        elif keystate[self.left_key]:
            self.acc.x = -PLAYER_ACC
            self.last_button_hit = "left"
            if now - self.last_time > self.frame_rate_2:
                self.last_time = pg.time.get_ticks()
                self.current_sprite_2 += 1
                if self.current_sprite_2 > 15:
                    self.current_sprite_2 = 8
                to_flip = self.sprite[self.current_sprite_2]
                self.image = pg.transform.flip(to_flip, True, False)
        self.acc.x += self.vel.x * PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

        if self.pos.x > WIDTH + 13:
            self.pos.x = -13
        if self.pos.x < -13:
            self.pos.x = WIDTH + 13

    def jump(self):
        self.rect.y += 2
        self.rect.y -= 2
        self.jumping = True
        if self.jumping:
            self.vel.y = PLAYER_JUMP
        self.game.soundChannel_in_game.play(random.choice(jump_snds))
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

class Crawler_mob(pg.sprite.Sprite):
    def __init__(self, game, plat):
        pg.sprite.Sprite.__init__(self)
        super().__init__()
        sprite_sheet = SpriteSheet("Crawler.png")
        self.game = game
        self.plat = plat
        self.sprite = [
            sprite_sheet.get_image(0, 0, 32, 32),
            sprite_sheet.get_image(32, 0, 32, 32),
            sprite_sheet.get_image(64, 0, 32, 32),
            sprite_sheet.get_image(96, 0, 32, 32),
            sprite_sheet.get_image(128, 0, 32, 32),
            sprite_sheet.get_image(160, 0, 32, 32),
            sprite_sheet.get_image(192, 0, 32, 32)
        ]
        self.walk_sprite_index = 0
        self.image = self.sprite[self.walk_sprite_index]
        self.change_x = 1
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx - random.randrange(0,45,1)
        self.rect.bottom = self.plat.rect.top
        self.last_time = pg.time.get_ticks()
        self.frame_rate_1 = 130
        self.frame_rate_2 = 50
        self.phase = "right"

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_time >= self.frame_rate_1:
            self.last_time = now
            self.walk_sprite_index += 1
            if self.walk_sprite_index >= 3:
                self.walk_sprite_index = 0

        if self.rect.centerx >= self.plat.rect.right - 13:
            self.change_x = -1
            self.phase = "left"
        if self.rect.centerx <= self.plat.rect.left + 13:
            self.change_x = 1
            self.phase = "right"
        self.rect.x += self.change_x
        if self.phase == "right":
            self.image = self.sprite[self.walk_sprite_index]
        if self.phase == "left":
            to_flip = self.sprite[self.walk_sprite_index]
            self.image = pg.transform.flip(to_flip, True, False)



        self.rect.bottom = self.plat.rect.top

        if not self.game.platform_sprites.has(self.plat):
            self.kill()


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        super().__init__()
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        if random.randrange(0,100) < POW_SPAWN_CHANCE:
            p = Pow(self.game, self)
            self.game.powerups.add(p)
            self.game.game_sprites.add(p)

        if random.randrange(0,100) < MOB_SPAWN_CHANCE:
            cm = Crawler_mob(self.game, self)
            self.game.mob_sprites.add(cm)
            self.game.game_sprites.add(cm)

class Pow(pg.sprite.Sprite):
    def __init__(self, game, plat):
        pg.sprite.Sprite.__init__(self)
        super().__init__()
        self.game = game
        self.plat = plat
        self.type = random.choice(['boost'])
        sprite_sheet = SpriteSheet("poweruptest.png")
        self.image = sprite_sheet.get_image(0,0,32,32)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platform_sprites.has(self.plat):
            self.kill()

class Box(pg.sprite.Sprite):
    def __init__(self, game, main_img_index, is_hovered_index, pos):
        pg.sprite.Sprite.__init__(self)
        super().__init__()
        sprite_sheet = SpriteSheet("hover_but_0.png")
        self.game = game
        self.sprite = [
            sprite_sheet.get_image(0, 0, 242, 50),
            sprite_sheet.get_image(0, 50, 242, 50),
            sprite_sheet.get_image(0, 100, 242, 50),
            sprite_sheet.get_image(0, 150, 242, 50),
            sprite_sheet.get_image(0, 200, 242, 50),
            sprite_sheet.get_image(0, 250, 242, 50),
            sprite_sheet.get_image(0,300, 242, 50),
            sprite_sheet.get_image(0, 350, 242, 50),
            sprite_sheet.get_image(0, 400, 242, 50),
            sprite_sheet.get_image(0, 450, 242, 50),
            sprite_sheet.get_image(0, 500, 121, 50),
            sprite_sheet.get_image(0, 550, 121, 50),
            sprite_sheet.get_image(121, 500, 121, 50),
            sprite_sheet.get_image(121, 550, 121, 50)
        ]
        self.image_1 = self.sprite[main_img_index]
        self.image_2 = self.sprite[is_hovered_index]
        self.rect = self.image_2.get_rect()
        self.rect.center = pos

        self.hoverd = False
        self.sfx_play = True
    def draw(self, screen):
        if self.hoverd:
            screen.blit(self.image_1, self.rect)
            if self.sfx_play:
                self.game.soundChannel_menu.play(random.choice(hover_snds))
            self.sfx_play = False
        else:
            self.sfx_play = True
            screen.blit(self.image_2, self.rect)
