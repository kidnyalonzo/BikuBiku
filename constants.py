import random

WIDTH = 450
HEIGHT = 600
ICON = "bikubikuicon.png"
TITLE = "Biku-Biku"
FPS = 60
font_1 = "BowlbyOneSC-Regular.ttf"

LIGHT_MASK = "light2.png"
LIGHT_MASK_2 = "light2.png"
LIGHT_RADIUS = (700,700)
LIGHT_RADIUS_2 = (1000,1000)

PLAYER_ACC = 0.7
PLAYER_FRIC = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = -20

plat_width = [
    312,
    224,
    136,
    64
]
plat_2nd = plat_width[random.randrange(0,3,1)]
plat_3rd = plat_width[random.randrange(0,3,1)]

PLATFORM_LIST = [
    (0, 570, 514, 30), #Initial Platform
    (random.randrange(0, WIDTH - plat_2nd), HEIGHT * 5 / 8, plat_2nd, 30), #2nd platform
    (random.randrange(0, WIDTH - plat_3rd), HEIGHT * 3 / 9, plat_3rd, 30), #3rd platform
]


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
NIGHT_COLOR = (5, 5, 5)

'''Power ups properties'''
BOOST_POWER = -60
POW_SPAWN_CHANCE = 40
MOB_SPAWN_CHANCE = 80

#sounds
jump_snds = []
jump_list = [
    'jmp0.wav',
    'jmp1.wav',
    'jmp2.wav',
]
hover_snds = []
hover_list = [
    'hover0.wav',
    'hover1.wav',
    'hover2.wav',
]
