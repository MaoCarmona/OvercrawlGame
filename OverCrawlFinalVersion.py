import pygame
from pygame import *
import funciones
import random

"""
Archivo: dungeon.py
Programa: Overcrawl
version: 2.0.0
Autor: Kevin Carmona, Jose Barco, Daniel Lopez
Fecha Inicio: 16/Nov/2019
"""
"""Por hacer
-cambio de nivel
-nivel 2 [listo]
-nivel boss[listo]
-nivel tutorial[listo]
-mejorar efectos de sonido[listo]
-chat de npc [ listo]
-agregar efectos visuales (barco)[listo]
-mas enemies xq si y el boss (barco)[listo]
-iconos para corazoncitos de vida, el antidoto, espada, arco[listo]
-icono cuando un enemigo lleve la llave(barco)[listo]
-menu de inicio con seleccion de dificultad
-menu de pausa
-historia[listo]
-nivel 0 tutorial [listo]
-Normalizar animaciones en multiples pc's[listo]
-Normalizar movimiento en multiples pc's


Enemigos
Cobra[listo]
Imp[listo]
Slime[listo]
Undead[listo]
Scorpion[listo]
Gran imp[listo]
HellHound[listo]
Skeleton Archer base[listo]
Skeleton Warrior base[listo]
Skeleton Archer variantes[listo]
Skeleton Warrior variantes[listo]
Minotaur[listo]
Knight [listo]
Necromancer[listo]
Berserker
Santa[Aliado]
"""
#Player puede conseguir arco,flechas y espada, con golpe pesado pierde la espada

WIN_WIDTH = 514
WIN_HEIGHT = 414
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 1.4)
DIFFICULTY = 2
BLANCO = [255,255,255]
ROJO = [255,0,0]
negro=[0,0,0]
plomo=[230,230,250]
grey=[128,128,128]
SCREEN_SIZE = pygame.Rect((0, 0, WIN_WIDTH, WIN_HEIGHT))
TILE_SIZE = 16
GRAVITY = pygame.Vector2((0, 0.3))
FPS = 60
#Initialize
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(SCREEN_SIZE.size)
#Fonts
pequenafuente = pygame.font.SysFont("comicsansms",15)
medianafuente = pygame.font.SysFont("comicsansms",30)
grandefuente = pygame.font.SysFont("italic",80)

bgBoss = pygame.image.load('Dg/Background.png')
#Pos Botones
boton1=[350,195]
tamboton=[100,32]
#----------------
boton2=[350,235]
#----------------
boton3=[350,275]
colorboton=[plomo,grey]
#----------------
#mapas
STAGES = {}
#Sprites
SS_ALLIES = {}
SS_ENEMIES = {}
SS_ITEM = {}
SS_STRUCTURES = {}
SS_TILES = {}
SS_PROJECTILES = {}
SS_FX = {}
#todos los grupos estan en el world
world = {}


def main():
    """Programa principal"""
    #Carga de sprites y mapas
    loadWord()
    loadSprites()
    loadMaps()#inicio del mundo
    #Sound
    #pygame.mixer.music.load('SFX/TEMA.mp3')
    pygame.mixer.music.load('SFX/8bitDungeon.ogg')
    pygame.mixer.music.play(-1)
    GO = pygame.image.load('Dg/gameover.png')
    #Sprites de mapa
    tileset=SS_TILES["dungeon"]
    tileset2=SS_TILES
    #Setup
    pygame.display.flip()
    pygame.display.set_caption("__DUNGEON__")
    timer = pygame.time.Clock()
    fuente = pygame.font.Font(None, 16)
    con=0
    seg=0
    min=0
    limM=6
    limS=59
    pHealth = Status(0,screen,4)
    bossHealth = Status(0,screen,4)
    bossName = Display("",screen, 20)
    pSword = Status(1,screen,0)
    pBow = Status(2,screen,0)
    pArrow = Status(3,screen,0)
    pPoiton = Status(4,screen,0)
    pAntidote = Status(5,screen,0)
    PauseScreen=Display("",screen,50)
    PauseScreen=Display("",screen,50)
    # Creacion del jugador
    player = Player(world["platforms"], world["hitItems"], (100, 100), world["passLevel"])
    if player.stage == 3:
        pygame.mixer.music.load('SFX/BossTheme.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
    #Construir nivel
    loadLevel(player)
    camera = setCamera(player.stage)  # camara complex

    #Main loop
    state=1
    nextStage=False
    while 1:
        dt = timer.tick(FPS)/1000
        seg=con/FPS
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                if state == 0 and not player.dead and not nextStage:
                    state=1
                    pygame.mixer.music.play(-1)
                else:
                    if not player.dead:
                        state = 0
                        pygame.mixer.music.stop()
            if e.type == KEYDOWN and (e.key == K_RETURN or e.key == K_d):
                if state == 0 and nextStage:
                    state = 1
                    nextStage = False
                    pygame.mixer.music.play(-1)

                    print("ir a new stage")

        if not player.levelC and not player.game:
            if state == 1:
                if player.stage == 1 or player.stage == 0:
                    #DRAW BACKGGROUND LEVEL 1
                    for y in range(32):
                        for x in range(34):
                            if x == random.randrange(34):
                                bg = tileset[7][1]
                                screen.blit(bg, (x * TILE_SIZE, y * TILE_SIZE))
                            else:
                                bg = tileset[7][0]
                                screen.blit(bg, (x * TILE_SIZE, y * TILE_SIZE))
                elif player.stage == 2:
                    #DRAW BACKGROUNG LEVEL 2
                    for y in range(32):
                        for x in range(34):
                                bg = tileset[3][11]
                                screen.blit(bg, (x * TILE_SIZE, y * TILE_SIZE))
                elif player.stage == 3:
                    screen.blit(bgBoss,(0,0))

                #Updates
                camera.update(player)
                player.update(world["enemies"], world["spawners"],world["projectiles"],world["items"],world["effects"],dt)
                #pygame.draw.rect(screen,(0,0,255),player.rect,1)
                #pygame.draw.rect(screen,(255,0,0),player.hitbox,1)
                for e in world["entities"]:
                    #e.update()
                    #IF ON CAMERA-DRAW IT
                    distx=abs(abs(camera.state[0])-e.rect[0])
                    disty=abs(abs(camera.state[1])-e.rect[1])
                    if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
                        screen.blit(e.image, camera.apply(e))
                for e in world["structures"] :
                    e.update(player)
                    if e.onCamera:
                        screen.blit(e.image, camera.apply(e))
                for e in world["enemies"]:
                    #pygame.draw.rect(screen,(0,0,255),e.rect,1)
                    #pygame.draw.rect(screen,(255,0,0),e.hitbox,1)
                    e.update(player,dt,world["items"],world["projectiles"],world["effects"],world["enemies"],screen)
                    if e.hasKey and e.onCamera:
                        bossName.update(e.__class__.__name__, screen)
                        #cargar nuevo nivel
                        screen.blit(bossName.image, (300, 20))
                        bossHealth.update(int((e.hp+1)/2),screen)
                        for c in range(bossHealth.images):
                            screen.blit(bossHealth.image,(320+(16*(c+1)),36))
                    if e.onCamera:
                        screen.blit(e.image, camera.apply(e))
                for e in world["spawners"]:
                    e.update(player,world["enemies"],world["items"],world["projectiles"])
                    if e.onCamera:
                        screen.blit(e.image, camera.apply(e))
                for e in world["items"]:
                    e.update(player)
                    if e.onCamera:
                        screen.blit(e.image, camera.apply(e))
                for e in world["projectiles"]:
                    e.update(player,dt,world["enemies"],world["spawners"],world["effects"],world["projectiles"])
                    if e.onCamera:
                        screen.blit(e.image, camera.apply(e))
                for e in world["effects"]:
                    e.update(player,dt,world["projectiles"],world["effects"])
                    #pygame.draw.rect(screen,(0,0,255),e.rect,1)
                    #pygame.draw.rect(screen,(255,0,0),e.hitbox,1)
                    screen.blit(e.image, camera.apply(e))
                #se dibuja al jugador por encima de todo lo demas
                screen.blit(player.image, camera.apply(player))
                pHealth.update(int((player.hp+1)/2),screen)
                pArrow.update(player.arrows,screen)
                pPoiton.update(player.potion,screen)
                pAntidote.update(player.antidote,screen)
                for c in range(pHealth.images):
                    screen.blit(pHealth.image,(16*(c+1),16))
                if player.sword:screen.blit(pSword.image,(16,32))
                if player.bow:screen.blit(pBow.image,(32,32))
                if player.arrows > 0:
                    screen.blit(pArrow.image,(48,32))
                    screen.blit(pArrow.cant,(64,32))
                screen.blit(pPoiton.image,(32,48))
                screen.blit(pPoiton.cant,(48,48))
                screen.blit(pAntidote.image,(64,48))
                screen.blit(pAntidote.cant,(80,48))
                if player.stage == 3:
                    val=int(limM -min)
                    val1 = int(limS - seg)
                    txt = "Tiempo : " + str(val) +" : "+ str(val1)
                    if val1==0:
                        con=0
                        min+=1
                        seg=0
                    if val < 1:
                        texto = fuente.render(txt, True, ROJO)
                    else:
                        texto = fuente.render(txt, True, plomo)
                    if val == 0 and val1 == 0:
                        player.dead=True
                    screen.blit(texto, [20, 80])
                pygame.display.update()

                if player.dead:
                    state = 2
                    pygame.mixer.music.stop()
                    screen.blit(GO, [50, 80])
                    pygame.display.update()
            elif state == 0 and not nextStage:
                player.pause=True
                PauseScreen.update("Game Paused", screen)
                screen.blit(PauseScreen.image, (160,175))
                pygame.display.update()
        elif player.levelC and not player.game:
            nextStage = True
            state=0
            PauseScreen.update("LEVEL COMPLETE", screen)
            #cargar nuevo nivel
            screen.blit(PauseScreen.image, (160, 175))
            newLevel(player)
            if player.stage == 3:
                pygame.mixer.music.load('SFX/BossTheme.ogg')
                pygame.mixer.music.set_volume(0.3)
            else:
                pygame.mixer.music.set_volume(1)
                #pygame.mixer.music.load('SFX/TEMA.mp3')
                pygame.mixer.music.load('SFX/8bitDungeon.ogg')
            camera = setCamera(player.stage)  # camara complex
            pygame.display.update()
        if player.game:
            PauseScreen.update("GAME COMPLETE", screen)
            screen.blit(PauseScreen.image, (100, 175))
            pygame.display.update()
        if player.stage == 3:
            con+=1
def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)
def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)
def setCamera(stage):
    if stage == 0:
        level=STAGES["Tuto"]
        WIN_HEIGHT=210
    elif stage == 1:
        level = STAGES["nivel1"]
    elif stage == 2:
        level = STAGES["nivel2"]
    elif stage == 3:
        level=STAGES["Boss"]
    level_width  = len(level[0])*TILE_SIZE
    level_height = len(level)*TILE_SIZE
    cam=Camera(complex_camera,level_width,level_height)
    return cam
"""Stages"""
def newLevel(player):
    loadWord()
    player.nextStage()
    loadLevel(player)
def loadLevel(player):

    global world
    if player.stage == 0:
        loadTuto(world)
        player.newStage(world["platforms"], world["hitItems"],[1300,144])
    if player.stage == 1:
        mes1 = pygame.image.load('Dg/textmss1-1.png')
        fin_mesS1 = False
        cont_mesS1 = 0
        while not fin_mesS1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    fin_mesS1 = True
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        cont_mesS1 += 1
                    if event.key == pygame.K_a:
                        fin_mesS1 = True
            if cont_mesS1 == 0:
                screen.fill(negro)
                screen.blit(mes1, [30, 100])
                pygame.display.update()

            elif cont_mesS1 == 1:
                fin_mesS1 = True
        loadStage1(world)
        player.newStage(world["platforms"], world["hitItems"])
    elif player.stage == 2:
        mes2 = pygame.image.load('Dg/textmss2-1.png')
        fin_mesS2 = False
        cont_mesS2 = 0
        while not fin_mesS2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    fin_mesS2 = True
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        cont_mesS2 += 1
                    if event.key == pygame.K_a:
                        fin_mesS2 = True
            if cont_mesS2 == 0:
                screen.fill(negro)
                screen.blit(mes2, [30, 100])
                pygame.display.update()

            elif cont_mesS2 == 1:
                fin_mesS2 = True
        loadStage2(world)
        player.newStage(world["platforms"],world["hitItems"],(352,715))

    elif player.stage == 3:
        mes31 = pygame.image.load('Dg/textmss3-1.png')
        mes32 = pygame.image.load('Dg/textmss3-2.png')
        fin_mesS3 = False
        cont_mesS3 = 0
        while not fin_mesS3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    fin_mesS3 = True
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        cont_mesS3 += 1
                    if event.key == pygame.K_a:
                        fin_mesS3 = True
            if cont_mesS3 == 0:
                screen.fill(negro)
                screen.blit(mes31, [30, 100])
                pygame.display.update()

            if cont_mesS3 == 1:
                screen.fill(negro)
                screen.blit(mes32, [30, 100])
                pygame.display.update()

            elif cont_mesS3 == 2:
                fin_mesS3 = True

        loadBossStage(world)
        player.newStage(world["platforms"],world["hitItems"],(100,700))
def loadTuto(world):
    level = STAGES["Tuto"]  # Se carga el primer nivel
    tileset = SS_TILES["dungeon"]
    x = y = 0
    for row in level:
        for col in row:
            if col == "T":
                Platform(6,(x, y),tileset, world["platforms"], world["entities"])
            if col == "I":
                r = random.randint(0, 4)
                item = Item((x, y), r)
                world["items"].add(item)
            if col == "o":
                item = BowItem((x, y))
                world["items"].add(item)
            if col == "*":
                item=SwordItem((x,y))
                world["items"].add(item)
            if col == "+":
                item=BowItem((x,y))
                world["items"].add(item)
            if col == "/":
                item=ArrowItem((x,y))
                world["items"].add(item)
            if col == "1":
                d = Door((x,y),3)
                world["structures"].add(d)
            if col == "K":
                item = Key((x, y))
                world["items"].add(item)
            if col == "k":
                item = Key((x, y), 2)
                world["items"].add(item)
            if col == "0":
                trap = BearTrap((x, y))
                world["structures"].add(trap)
            if col == "X":
                Platform2(0, (x, y), tileset, world["platforms"], world["entities"])
            if col == "L":#UP
                HitItems(1,(x, y),tileset, world["hitItems"], world["entities"])
            if col == "C":
                Platform(1,(x, y),tileset, world["platforms"], world["entities"])
            x += TILE_SIZE
        y += TILE_SIZE
        x = 0
    enemiesStage0(world)
def loadStage1(world):
    level = STAGES["nivel1"] #Se carga el primer nivel
    tileset=SS_TILES["dungeon"]
    x = y = 0
    for row in level:
        for col in row:
            if col == "S":
                spawn=Spawner(world["platforms"],(x,y),0)
                world["spawners"].add(spawn)
            if col == "U":
                spawn=Spawner(world["platforms"],(x,y),1)
                world["spawners"].add(spawn)
            if col == "I":
                r=random.randint(0,4)
                item=Potion((x,y),r)
                world["items"].add(item)
            if col == "*":
                item=SwordItem((x,y))
                world["items"].add(item)
            if col == "+":
                item=BowItem((x,y))
                world["items"].add(item)
            if col == "/":
                item=ArrowItem((x,y))
                world["items"].add(item)
            if col == "1":
                d = Door((x,y),4)
                world["structures"].add(d)
            if col == "K":
                item=Key((x,y))
                world["items"].add(item)
            if col == "k":
                item=Key((x,y),2)
                world["items"].add(item)
            if col == "0":
                trap=BearTrap((x,y))
                world["structures"].add(trap)
            if col == "P":
                Platform(0,(x, y),tileset, world["platforms"], world["entities"])
            if col == "C":
                Platform(1,(x, y),tileset, world["platforms"], world["entities"])
            if col == "p":#B-R
                Platform(2,(x, y),tileset, world["platforms"], world["entities"])
            if col == "c":#B-L
                Platform(3,(x, y),tileset, world["platforms"], world["entities"])
            if col == "M":#M-L
                Platform(4,(x, y),tileset, world["platforms"], world["entities"])
            if col == "X":#M-L
                Platform(5,(x, y),tileset, world["platforms"], world["entities"])
            if col == "#":#M-L
                MovilPlatform((x, y),tileset, world["passLevel"] , world["entities"])
            if col == "B":#COL-DOWN
                CreateMap(0,(x, y),tileset, world["justMap"], world["entities"])
            if col == "G":#COL-MIDDLE
                CreateMap(1,(x, y),tileset, world["justMap"], world["entities"])
            if col == "A":#COL-UP
                CreateMap(2,(x, y),tileset, world["justMap"], world["entities"])
            if col == "b":
                CreateMap(3,(x, y),tileset, world["justMap"], world["entities"])
            if col == "a":
                CreateMap(4,(x, y),tileset, world["justMap"], world["entities"])
            if col == "s":
                CreateMap(5,(x, y),tileset, world["justMap"], world["entities"])
            if col == "V":#LAVA
                HitItems(0,(x, y),tileset, world["hitItems"], world["entities"])
            if col == "L":#UP
                HitItems(1,(x, y),tileset, world["hitItems"], world["entities"])
            if col == "D":#DOWN
                HitItems(2,(x, y),tileset, world["hitItems"], world["entities"])
            if col == "J":#LEFT
                HitItems(3,(x, y),tileset, world["hitItems"], world["entities"])
            if col == "R":#RIGHT
                HitItems(4,(x, y),tileset, world["hitItems"], world["entities"])
            if col == "E":
                ExitBlock((x, y), world["platforms"], world["entities"])
            x += TILE_SIZE
        y += TILE_SIZE
        x = 0

    enemiesStage1(world)  # carga enemigos del nivel 1
def loadStage2(world):
    level2=STAGES["nivel2"]#Se carga nivel 2
    tileset=SS_TILES["dungeon"]
    x=y=0
    for f in level2:
        for col in f:
            if col == "I":
                r = random.randint(0, 4)
                item = Item((x, y), r)
                world["items"].add(item)
            if col == "o":
                item = BowItem((x, y))
                world["items"].add(item)
            if col == "*":
                item=SwordItem((x,y))
                world["items"].add(item)
            if col == "+":
                item=BowItem((x,y))
                world["items"].add(item)
            if col == "/":
                item=ArrowItem((x,y))
                world["items"].add(item)
            if col == "S":
                spawn=Spawner(world["platforms"],(x,y),0)
                world["spawners"].add(spawn)
            if col == "U":
                spawn=Spawner(world["platforms"],(x,y),1)
                world["spawners"].add(spawn)
            if col == "I":
                r=random.randint(0,4)
                item=Item((x,y),r)
                world["items"].add(item)
            if col == "o":
                item=BowItem((x,y))
                world["items"].add(item)
            if col == "1":
                d = Door((x,y),5)
                world["structures"].add(d)
            if col == "K":
                item=Key((x,y))
                world["items"].add(item)
            if col == "k":
                item=Key((x,y),2)
                world["items"].add(item)
            if col == "0":
                trap=BearTrap((x,y))
                world["structures"].add(trap)
            if col == "L":#UP
                HitItems(1,(x, y),tileset, world["hitItems"], world["entities"])
            if col == "D":#DOWN
                HitItems(2,(x, y),tileset, world["hitItems"], world["entities"])
            if col == "C":
                Platform2(1,(x, y),tileset, world["platforms"], world["entities"])
            if col == "X":
                Platform2(0,(x, y),tileset, world["platforms"], world["entities"])
            if col == "x":
                Platform2(2,(x, y),tileset, world["platforms"], world["entities"])
            if col == "q":
                Platform2(3,(x, y),tileset, world["platforms"], world["entities"])
            if col == "w":
                Platform2(4,(x, y),tileset, world["platforms"], world["entities"])
            if col == "r":
                Platform2(5,(x, y),tileset, world["platforms"], world["entities"])
            if col == "a":#COL-DOWN
                CreateMap1(3,(x, y),tileset, world["justMap"], world["entities"])
            if col == "b":#COL-MIDDLE
                CreateMap1(4,(x, y),tileset, world["justMap"], world["entities"])
            if col == "c":#COL-UP
                CreateMap1(5,(x, y),tileset, world["justMap"], world["entities"])
            if col == "d":
                CreateMap1(6,(x, y),tileset, world["justMap"], world["entities"])
            if col == "e":
                CreateMap1(7,(x, y),tileset, world["justMap"], world["entities"])
            if col == "f":
                CreateMap1(8,(x, y),tileset, world["justMap"], world["entities"])
            x+=TILE_SIZE
        y+=TILE_SIZE
        x=0
    enemiesStage2(world)
def loadBossStage(world):
    level = STAGES["Boss"]  # Se carga el nivel del boss
    tileset = SS_TILES["dungeon"]
    x = y = 0
    for f in level:
        for col in f:
            if col == "T":
                Platform(6,(x, y),tileset, world["platforms"], world["entities"])
            if col == "I":
                r=random.randint(0,4)
                item=Potion((x,y),r)
                world["items"].add(item)
            if col == "*":
                item=SwordItem((x,y))
                world["items"].add(item)
            if col == "+":
                item=BowItem((x,y))
                world["items"].add(item)
            if col == "/":
                item=ArrowItem((x,y))
                world["items"].add(item)
            if col == "1":
                d = Door((x,y),4)
                world["structures"].add(d)
            if col == "K":
                item=Key((x,y))
                world["items"].add(item)
            if col == "k":
                item=Key((x,y),2)
                world["items"].add(item)
            if col == "0":
                trap=BearTrap((x,y))
                world["structures"].add(trap)
            if col == "#":#COL-DOWN
                CreateMap(6,(x, y),tileset, world["justMap"], world["entities"])
            if col == "%":#COL-DOWN
                CreateMap(7,(x, y),tileset, world["justMap"], world["entities"])
            if col == "-":
                CreateMap(8,(x, y),tileset, world["justMap"], world["entities"])
            if col == ".":
                CreateMap(9,(x, y),tileset, world["justMap"], world["entities"])
            if col == ",":
                CreateMap(10,(x, y),tileset, world["justMap"], world["entities"])
            if col == "C":
                Platform(1,(x, y),tileset, world["platforms"], world["entities"])
            if col == "X":
                BossPlatform(0, (x, y), tileset, world["platforms"], world["entities"])
            if col == "a":
                BossPlatform(2, (x, y), tileset, world["platforms"], world["entities"])
            if col == "b":
                BossPlatform(3, (x, y), tileset, world["platforms"], world["entities"])
            if col == "c":
                BossPlatform(4, (x, y), tileset, world["platforms"], world["entities"])
            if col == "d":
                BossPlatform(5, (x, y), tileset, world["platforms"], world["entities"])
            if col == "e":
                BossPlatform(6, (x, y), tileset, world["platforms"], world["entities"])
            if col == "f":
                BossPlatform(7, (x, y), tileset, world["platforms"], world["entities"])
            if col == "g":
                BossPlatform(8, (x, y), tileset, world["platforms"], world["entities"])
            if col == "h":
                BossPlatform(9, (x, y), tileset, world["platforms"], world["entities"])
            if col == "i":
                BossPlatform(10, (x, y), tileset, world["platforms"], world["entities"])
            if col == "U":#UP
                HitItems(5,(x, y),tileset, world["hitItems"], world["entities"])
            if col == "D":#UP
                HitItems(6,(x, y),tileset, world["hitItems"], world["entities"])
            if col == "R":#UP
                HitItems(7,(x, y),tileset, world["hitItems"], world["entities"])
            if col == "L":#UP
                HitItems(8,(x, y),tileset, world["hitItems"], world["entities"])


            if col == "E":
                ExitBlock((x, y), world["platforms"], world["entities"])
            x += TILE_SIZE
        y += TILE_SIZE
        x = 0
    enemiesStage3(world)
def enemiesStage0(world):
    """
    [Tutorial]
    mobs = puede ser la cobra
    poner como subjefecito sencillo al skeleton warrior base q suelte la espada tal vez
    """
    #Cargar algunos enemies en el
    enemy = Cobra(world["platforms"], (1126, 264))
    world["enemies"].add(enemy)
    enemy = Santa(world["platforms"], (336, 70))
    world["enemies"].add(enemy)
    enemy = SkeletonWarriorBase(world["platforms"], (736, 300),True,world["items"])
    world["enemies"].add(enemy)
def enemiesStage1(world):
    """
    mobs=imp,slime,cobra
    subjefe:
    0=hellHound[llave]
    1=Skeleton Archer(basico)[llave]
    2=Skeleton Archer(basico)[llave]
    """
    #Cargar algunos enemies en el
    enemy = Cobra(world["platforms"], (1610, 50))
    world["enemies"].add(enemy)
    enemy = Imp(world["platforms"], (686, 144))
    world["enemies"].add(enemy)
    enemy = Slime(world["platforms"], (500, 144))
    world["enemies"].add(enemy)
    enemy = Cobra(world["platforms"], (416, 144))
    world["enemies"].add(enemy)
    enemy = Imp(world["platforms"], (2405, 144))
    world["enemies"].add(enemy)
    enemy = Cobra(world["platforms"], (2539, 257))
    world["enemies"].add(enemy)
    #enemy = Undead(world["platforms"], (2450, 144))
    #world["enemies"].add(enemy)
    #enemy = Undead(world["platforms"], (1650, 352))
    #world["enemies"].add(enemy)
    #enemy = Undead(world["platforms"], (2500, 272))
    #world["enemies"].add(enemy)
    #enemy = Undead(world["platforms"], (2600, 144))
    #world["enemies"].add(enemy)
    if DIFFICULTY == 0:
        enemy = HellHound(world["platforms"], (300, 50),True,world["items"])
        enemy.dir = 1
        world["enemies"].add(enemy)
    elif DIFFICULTY > 0:
        enemy = Cobra(world["platforms"], (2227, 257))
        world["enemies"].add(enemy)
        enemy = Imp(world["platforms"], (1595, 465))
        world["enemies"].add(enemy)
        enemy = HellHound(world["platforms"], (300, 50))
        world["enemies"].add(enemy)
        enemy = SkeletonArcherBase(world["platforms"], (850,670),True,world["items"])
        world["enemies"].add(enemy)
def enemiesStage2(world):
    """
    mobs=undead,scorpion,slime,gran imp,hellHound
    [subjefe]:
    0=Minotaur[llave]
    0=Skeleton Archer(tipo 1 o 2)[llave]
    1=Skeleton Warrior(tipo 1 o 2)[llave]
    """
    #Cargar algunos enemies en el
    enemy = Scorpion(world["platforms"], (923, 381))
    world["enemies"].add(enemy)
    enemy = Scorpion(world["platforms"], (1165, 271))
    world["enemies"].add(enemy)
    enemy = Undead(world["platforms"], (328, 157))
    world["enemies"].add(enemy)
    enemy = Undead(world["platforms"], (706, 133))
    world["enemies"].add(enemy)
    enemy = Undead(world["platforms"], (1940, 381))
    world["enemies"].add(enemy)
    enemy = Scorpion(world["platforms"], (2116, 536))
    world["enemies"].add(enemy)
    enemy = Scorpion(world["platforms"], (1230, 462))
    world["enemies"].add(enemy)
    enemy = Scorpion(world["platforms"], (1008, 544))
    world["enemies"].add(enemy)
    enemy = Undead(world["platforms"], (2326, 607))
    world["enemies"].add(enemy)
    enemy = Scorpion(world["platforms"], (2092, 701))
    world["enemies"].add(enemy)
    enemy = GranImp(world["platforms"], (1196, 698))
    world["enemies"].add(enemy)

    enemy = Slime(world["platforms"], (680, 288))
    world["enemies"].add(enemy)
    enemy = Slime(world["platforms"], (48, 256))
    world["enemies"].add(enemy)
    enemy = Slime(world["platforms"], (528, 144))
    world["enemies"].add(enemy)
    if DIFFICULTY == 0:
        enemy = Minotaur(world["platforms"], (850, 720),True,world["items"])
        world["enemies"].add(enemy)
    if DIFFICULTY == 1:
        r = random.randint(1,2)
        enemy = SkeletonArcher(world["platforms"], (850, 720),r,True,world["items"])
        world["enemies"].add(enemy)
    if DIFFICULTY == 2:
        r = random.randint(1,2)
        enemy = SkeletonWarrior(world["platforms"], (850, 720),r,True,world["items"])
        world["enemies"].add(enemy)
    if DIFFICULTY > 0:
        enemy = Scorpion(world["platforms"], (1375, 381))
        world["enemies"].add(enemy)
        enemy = Scorpion(world["platforms"], (701, 271))
        world["enemies"].add(enemy)
        enemy = Undead(world["platforms"], (1260, 152))
        world["enemies"].add(enemy)
        enemy = Undead(world["platforms"], (2402, 55))
        world["enemies"].add(enemy)
        enemy = Scorpion(world["platforms"], (2326, 607))
        world["enemies"].add(enemy)
        enemy = Scorpion(world["platforms"],(1196, 698))
        world["enemies"].add(enemy)

def enemiesStage3(world):
    """
    [Boss]
    0,1=Knight
    2=Necromancer
    """
    #Cargar algunos enemies en el
    enemy = Imp(world["platforms"], (964, 65))
    world["enemies"].add(enemy)
    enemy = Imp(world["platforms"], (964, 75))
    world["enemies"].add(enemy)
    enemy = Scorpion(world["platforms"], (3572, 182))
    world["enemies"].add(enemy)
    enemy = Scorpion(world["platforms"], (3798, 274))
    world["enemies"].add(enemy)
    enemy = Imp(world["platforms"], (4656, 719))
    world["enemies"].add(enemy)
    enemy = Imp(world["platforms"], (4972, 719))
    world["enemies"].add(enemy)
    enemy = Imp(world["platforms"], (6556, 719))
    world["enemies"].add(enemy)
    enemy = Imp(world["platforms"], (6536, 719))
    world["enemies"].add(enemy)
    enemy = Scorpion(world["platforms"], (6556, 719))
    world["enemies"].add(enemy)
    enemy = Scorpion(world["platforms"], (7574, 459))
    world["enemies"].add(enemy)
    if DIFFICULTY == 0:
        enemy = Knight(world["platforms"], (3572, 182))
        world["enemies"].add(enemy)
    if DIFFICULTY == 1:
        enemy = Knight(world["platforms"], (3572, 182))
        world["enemies"].add(enemy)
    if DIFFICULTY == 2:
        enemy = Necromancer(world["platforms"], (480,600))
        world["enemies"].add(enemy)
"""Fin"""
def loadWord():
    global world
    world = {
    "platforms": pygame.sprite.Group(),
    "enemies": pygame.sprite.Group(),
    "entities": pygame.sprite.Group(),
    "passLevel": pygame.sprite.Group(),
    "justMap": pygame.sprite.Group(),
    "hitItems": pygame.sprite.Group(),
    "structures": pygame.sprite.Group(),
    "items": pygame.sprite.Group(),
    "projectiles": pygame.sprite.Group(),
    "spawners": pygame.sprite.Group(),
    "effects": pygame.sprite.Group()
    }
def loadMaps():
    global STAGES
    STAGES["Tuto"] = [
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "X                                                                                     X",
        "X                                                                                     X",
        "X                                                                                     X",
        "X                                                                                     X",
        "X                                                               X                 1   X",
        "X                                                               XXXXXXXXXXXXXXXXXXXXXXX",
        "X                                                           X                         X",
        "X                                                      X    X                         X",
        "X           T            T             T               X    X                         X",
        "X        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "X        X                                                                            X",
        "X       XX                                                                            X",
        "X                                                                                     X",
        "X                                                                                     X",
        "X                                                                                     X",
        "X                LLL                         C                         + /            X",
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    ]
    STAGES["nivel1"] = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP     A         A       s  s             A         A    s    A                  s                 A                                      A     s          s    A                              s         PPPP",
        "PP     G         G       s  s             G         G    s    G                  s                 G                                      G     s          s    G                              s         PPPP",
        "PP     G         G       sLLs             G         G    s    G                  s      C          B          C                           G     s          s    G                              s         PPPP",
        "PP     G         G       JPPR             G         G    s    G               C    C     PPPPPPPPPPPPPPPPPPPPP                            G     s          s    G                              s         PPPP",
        "PP     G         G       JPPR             G         a    s    G               JPPPP      DDDDDDDDDDDDDDDDDDDDD      C      C              G                s    G                                        PPPP",
        "PP     G   PPP   G       sDDs             G         b         G        C   C                                        JPPPPPPR              G                s    G                                     MMcPPPP",
        "PP+    G   PPP   G       s  s             GPP   I   G         G        JPPP                                                               G                     G                                        PPPP",
        "PP     G   DDD   G      C    C            G         G         G  C   C                                                             C     CG                     G JPPR       C CC C                      JPPP",
        "PP     B   ///// B      JPPPPR            B     0   B         B  JPPPLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLPPPPPRB           I        CBJPPPPRC      PLLP        C              JPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPR              JPPP",
        "PP    s   s                               A                   A                                                                           A                     A                       PR               JPPP",
        "PP    s   s                               B                   B                                                                           B                     B                      PR                JPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPR                 JPPP",
        "PP    s   s        A                                  s         s  s                     A                 A               s                                  A                                          JPPP",
        "PP    s   s        G                                  s         sLLs                     G                 G               s               b                  a                                          JPPP",
        "PP    s   s        G                                  s         JPPR                     G                 G               s        C   0  B   C  C  C  C            C                                  JPPPP",
        "PP    s   s        G                                  s         JPPR                     G                 G                         PPPPPPPPPPPLLLPPLLLPPPPPPPPPPPPP                                  JPPPPP",
        "PP    s   s        G                      I                     sDDs                     G                 G               0                  JPPPPPPPPPR       s s s                         C       JPPPPPP",
        "PP    s   s        G                  cPPPPPPp                  s  s                     G                 G            JPPPPPR                                 s s      JPPPPPR              JPPPPPPPPPPPPPP",
        "PP  I  0  s        G         0                       L                PPPPPPR            G                 G             DDDDD                                  s                             JPDDDDDDDDDPPPP",
        "PPpMMMMMMMs        G       cPPPp                  cPPPPPp                       C   0 LLCB       I  0      BCLL      C                                                             JPPPPPR                PPP",
        "PP s      s        G                                           cPPPp            JPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPR                                                                                    PPP",
        "PP s      s       0B C                                                                   s                 s                                                                                    JPPPPPPLPPPPPPP",
        "PP               PPPPVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVPVVVPPPP",
        "PP               PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP               PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP   PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PPPPPPR          PP      s         s                                    PP                 A           s           A                                      A   A  PP",
        "PPDDD            PP      s         s         S                          PP                 G           S           G                                      B1  B  PP",
        "PP s             PP      s         s                                    PP   C             B           s           B               C                PPPPPPPPPPPPPPP",
        "PP s          0  PP     S          s                              S     PP    PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP       XX         PP",
        "PP s       MMcPPPPPMMMMMMMp        s                            cMMMMMMcPP              s              s             s          PPP                  PP",
        "PP s           s PP                s  C     II0II   C                   PP              s              s             s          PPPX                 PP",
        "PP             s PP                s   cMMMMMMMMMMMMp                   PPPpMMMM        s              s      0     XXX         PPP    X             PP",
        "PP             s PP                                                     PP             XXX        cXXXXp     XXX     s          PPP               X PP",
        "PP      C      s PP         cXXXXp                        cXXXXp        PP              s          s                 s   PP  MMcPPPVVVVVVVVVVVVVVVVVVPP",
        "PPPPPPPp         PP                                                     PP    I         s          s                 I          PPPVVVVVVVVVVVVVVVVVVPP",
        "PP               PP    0                            C         0         PP                         s            0               PPPVVVVVVVVVVVVVVVVVVPP",
        "PP               PPPPPPPPPPPPPPPPPPPPp        C      cPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPp                cPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP               AA                          cPp                                                                     JPP",
        "PP               GG                     C                                  C                       XXXX              JPP",
        "PP               GG                    cPp                                  P    0   0    0     LLLLLLLLLL           JPP",
        "PP               GG             C   C                                      cPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "PP   0      0    BB             JPPPR             0             0        C JPPPPP",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP"
    ]
    STAGES["nivel2"]=[
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "XX                         X   XXX   X                   XDDXXXDDDXXXDDDXXXDDDXXX                  XX                                        XX             XX                    X                         XX",
        "XX                +        X   DDD   X                                                C    C       XX     CI  IC               C             DD      I      DD            C       X                         XX",
        "XX/////                    X    I    X                                                 XXXX        XX      qwwr                 XX      C                         C     XX        Xqwr                   qwrXX",
        "XXqwwwr                    X    I    X                  C   C C   C C   C C   C C     XXXXX        XX                   C   C   XXXXXXXX            LLL            XXXXXXX        X            X            XX",
        "XX               qwr       X         X                   XXXLLLXXXLLLXXXLLLXXXLLLXXXXXXXXX         XX                    qwr    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX       X         qwrXqwr         XX",
        "XX                          X       X                   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX          XXX     C    C                XX                  DDD                DDD        X            X            XX",
        "XX       qwr                                           XXX                                       XXDD      qwwr                 XX *                         C I C            C   X            X            XX",
        "XX                             C C                    XXXX////                                                          C   C   XXqwr                         qwr              qwrXqwr         X         qwrXX",
        "XXqwr                          XXX                   XXXXXqwwr                                                           qwr    XX                                                X            X            XX",
        "XX          qwr               XXXXX                 XXXXXX                                                                      XX        C                  C   C                X            X            XX",
        "XX           X               XXXXXXX               XXXXXXX  C   0   C    C    0    C C XX C   C    CC   C    C / C   C / C  C   XX         XXXXLLLLXXXXXXXXXXLLLLLXXXXXXXXXXLLXXXXX         qwrXqwr         XX",
        "XX   X       X              XXXXXXXXX             XXXXXXXXLLLXXXXXXXLLLLLLXXXXXXXXXLLLXXXXLLLLLXXXXLLXXXLLLLLLXXXLLLLLXXXLLLLXXXXX         XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX            X            XX",
        "XX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXqwr      XX                                                  X            XX",
        "XX                                                                                                 X                                       XX                                  C        0      X            XX",
        "XX                                                                                                 X/I I/ C               C   C            XX                  XX               XXXXXXXXXXXXXXXX          qrXX",
        "XX  C                          XX                                                                  XXXXXXX                 XXX             XX             qwr   XXX           XX                            XX",
        "XXwr                           XX                                                                        X   C             XXX             XXqwr                  XXXXXXXXXXXXX                             XX",
        "XX            qwwr          qwwXX           0           C   C              0          C                  X    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                               XX                       qr     XX",
        "XX                             XXXXXXXXXXXXXXXXXXXXXXXXXXLLLXXXXXXXXXXXXXXXXXXXXXXXXXXXL            0  * X    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX      qwwwr                    XX qr                           XX",
        "XX                             XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX          XXXXXXX                               XXXX              qwwwr            XX           qwwwwr             XX",
        "XX                             XX                                                                  XXXXXXX                                XXX                      qwwwr    XX                              XX",
        "XX                             XX                                                                  XXXXXXX                                 XX                              XXX                             XXX",
        "XX                             XX                                                              XXXXXXXXXXX                                 DD                             XXXXqr                          XXXX",
        "XX                                   X                                                             XXXXXXX                                                               XXXXX                           XXXXX",
        "XX                                  LXL    0     LL       0       LL       0       LL          LLLLXXXXXXXLLLL             000                                          XXXXXX                          XXXXXX",
        "XX                        qwrXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                         XXXXXXX",
        "XX                           XXXXX                                                                                                                                                      XXXXXXXXXXXXXXXXXXXXX",
        "XX           qwwwr           XXXXX                                                                                                                                                      XX                  XX",
        "XX                           XXXXX                                                                  XX                              L              L                                   XXX                  XX",
        "XX qwr                       XXXXX    C            0       L        0        L       0             XXXX          XXXX            qwwwwwr       qwwwwwwwr                              XXXX     ///II///     XX",
        "XX                           XXXXX     XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX             D              D            qwwwwr               XXXXX      qwwwwwwr    XX",
        "XX                           XXXXX                                                                               XXXX                                                               XXXXXX x                XX",
        "XX        qwwwwwwwwwr        XXXXX                                                                               XXXX                             ///                    x         XXXXXXXqwwr             *XX",
        "XX                           XXXXX                         0                 0                         C         XXXXLLL                          XXX                    x     LL0XXXXXXXX                 xXX",
        "XX                           XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX           XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                xxXX",
        "XX                         qrXXXXX                                                                  XXXX                                                                                                 qwrXX",
        "XX                           XXXXX                                                                     XXX                                                                                       qwr        XX",
        "XX               qwr         XXXXX                              ///     II*II     ///                    XXXXX                                                                                   XXX        XX",
        "XX                           XXXXX                     qwwwr   qwwwr   qwwwwwr   qwwwr                       XXXXXX         L            0           L          0                               xXXX        XX",
        "XX qwwr                      XXXXXII                                                     qwwwr                    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX        XX",
        "XX  abf                      XXXXXqwwwwwwwwwr                                                    qwwwr                      D                        D                     XXXXX                            XX",
        "XX  def                      XXXXX                                                                         XX                                                               XXX                           qrXX",
        "XX  abf   qwwr               XXXXX                                                                       qrXXX                                                    X          X          X                   XX",
        "XX  def                      XXXXX                                                                         XXXX                                                  XXX                   XXX                  XX",
        "XX  abf          x           XXXXX1                                                                        XXXXX                        0                       XXXXX        I        XXXXX         xx    IIXX",
        "XX  def          XXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",

    ]
    STAGES["Boss"] = [
        "                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            ",
        "                                                                                                                                                                                                                                                                     ",
        "                                                                                                                                                                                                                                                                     ",
        "                                                                                                                                                                                                                                                                     ",
        "                                                                                                                                                                                                                                                                     ",
        "                                                                                                                                                                                                                                                                     ",
        "                            C    0           0           0            0           0     C                                           U               U                                                                                                                ",
        "                             abbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbc           abbbc          abbbc           abbbc           abbbc           abbbc          abbbc        LXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX           XXX  ",
        "                              dXXXXXXXX #    XX     # XXXXXXXXXX #    XX    # XXXXXXXXf             ghi            ghi             ghi             ghi             ghi            ghi        LXRDDDDDDDDDDDDDDDDDDDDXXXXXDDDDDDDDDDDDDDDDXXXXXDDDDDDD           XXX  ",
        "                               dXXXXXX  %   XXXX    %  XXXXXXXX  %   XXXX   %  XXXXXXf                                                                                                   UUUUXR                     DXXXD                DXXXD                  XXX  ",
        "             abbbbc             dXXXX   %  XXXXXX   %   XXXXXX   %  XXXXXX  %   XXXXf                                                                                                   XXXXXR                       DDD                  DDD                   XXX  ",
        "             deeeef              dXX      XXXXXXXX       XXXX      XXXXXXXX      XXf                                            UUUUUUUUUUUUUUUUUUUUUUUUU                               XXXXR                                                                   XXX  ",
        "             ghhhhi               d      XXXXXXXXXX       XX      XXXXXXXXXX      f                                            LXXXXXXXXXXXXXXXXXXXXXXXXXR                              XXXR                                                                    XXX  ",
        " XX                                ghhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhi                                             LXXX                   XXXR                              XX     XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  ",
        "                                                                                                                               LXX                     XXR                              XX                                                                      XXX  ",
        "                                                                                                                               LX                       XRUUUUUUUUUUUUUUUUR             XX                                                                      XXX  ",
        "                                                                                                                               LX/          I          /XXXXXXXXXXXXXXXXXXR             XXXX                                                                    XXX  ",
        "X                                                                                                                              LXX         /+/         XXXXXXXXXXXXXXXXXXXR             XXR                     XX                                              XXX  ",
        "                                                                                          XXXX                                 LX          XXX          XXXXXXXXXXXXXXXXXXR             XXUUUUUU              UXXXXU        0                           C       XXX  ",
        "                                                                                          XXXX                                 LX                       XR       #     XXXR             XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX        XXX  ",
        "                                                                                          XXXX                                 LXXI                   IXXR       %     XXXR             XX                        #   XXXXXXXXXX                                XXX  ",
        "XXX                                                                                       #  #                                 LXXX                   XXXR       %     XXXR             XX                        %XXXXXXXXXX                                   XXX   ",
        "                                                                                          %  %                                 LXXXXXXXXXXX   XXXXXXXXXXXR       %     XXXR             XX/I/                     %                          XXXXXXXXXXXXXXXXXXXXXX  ",
        "     /*/                                                                                  %  %                                   #     #         #     #         %     XXXR             XXXXX                     %                       XXXXDD                XXX                                                                                                                                                                           XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "    abbbcU                    X                                                           %  %                                   %     %         %     %         %     XXX              XX                        %                    XXXXDD                   XXX                                                                                                                                                                           XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "    deeeeeef                 LXR                                                                                                 %     %         %     %         %     XXX              XX       *          UUXXXXX                 XXXXDD                      XXX                                                                                                                                                                           XX       #                    #                       XXXXXX",
        "    ghhhhhhi               abbbbbc          XX           abbbc                                                                   %     %   XXX   %     %         %     XXX              XX               UXXXXXX                 XXXXDD                         XXX                                                                                                                                                                           XX       %                    %                       XXXXXX",
        "     #  #                  ghhhhhi          DD           ghhhi                                                                         %  X   X  %               %     XXX              XX//            UXXXX                 XXXXDD                            XXX                                                                                                                                                                           XX       %                    %               I I I       XX",
        "     %  %                                  UUUU                                                                                        % X     X %               %     XXX              XXXXXXXXXXXXXXXXXX                 XXXXD  I        I                    XXX                                                                                                                                                                           XX       %                    %                           XX",
        "     %  %                                 LXXXXXR                      abbbc                                                           UX   X   XU               %     XXX              XX                              XXXXD        //                         XXX                                                                                                                                                                           XX                                 C      T            1  XX",
        "     %  %                                 LXXXXXR                      ghhhi                                                  abbbbbbbbbbbb # bbbbbbbbbbc        %     XXX              XX                           XXXXD    I          I                      XXX                                                                                                                                                                           XX              abbbbbbbbf         LXXXXXXXXXXXXXXXXXXXXXXXX",
        "     %  %                                 LXXXXXR                                                                             ghhhhhhhhhhhh % hhhhhhhhhhg        %     XXX              XX                        XXXXU                              C          XXX                                                                                                                                                                           XX              dhhhhhhhhi          DDDDDDDDDDDDDDDDD XXXXXX",
        "     %  %                                  #DDD#                                     abbbc                                                  %                    %     XXX              XX /// C               XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX           XXX                                                                                                                                                                           XX    T                                               XX",
        "     %                                     %   %                                     ghhhi                      abbbc                       %                    %     XXX              XXXXXXX             XXXX       XXXXXXXXXX                             XXXXX                                                                                                                                                                           XX   XX                                               XX",
        "                                           % + %                                                                ghhhi                       %                    %     XXX              XXR              XXX           #DDDDDDDD#                            X  XXX                                                                                                                                                                           XX   X                                                XX",
        "                                                                                                                             X                                   %     XXX              XXR           XXXX             %        %                           X   XXX                                                                                                                                                                           XX                                         CT     */  XX",
        "                                                                                                 abbbc                       XXX    C       C                    %     XXX              XXR        XXXX                %        %                          X    XXX                                                                                                                                                                           XXXX                                       LXXXXXXXXXXXX",
        "                                          /     /                                                deeef                      abbbbbbUUbbbbbbc          X          %     XXX              XXR        XXX                          %                         X     XXX                                                                                                                                                                           XXXX                                        DDDDDDDDDDXX",
        "                                         LX     XR                                                ghi                        ghhhhhhhhhhhhi           XX         %     XXX              XXR        XXX                                         C         XXXXXXXXXX                                                                                                                                                                           XXXXXX          C  T 0    C                           XX",
        "                                         LX     XR                                 abbbc                                                              XXX        %     XXX              XXR        XXX                                          XXXXXXXXXXXXXXXXXXX                                                                                                                                                                           XX              abbbbbbbbbc                           XX",
        "                                      X  LX     XR  X                              deeef                                                             abbbbbc           XXX              XXR        XXX           UXXXXR        LXXXXU                           XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX              dhhhhhhhhhi                           XX",
        "                 C                    UUUUX     XUUUU                    C         ghhhi                                                             deeeeef           XXX              XXR        XXX          XXXXXR          LXXXXX                          XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                                                    XX",
        "                  abbbbbbbbbbbbbbbbbbbbbbbb     bbbbbbbbbbbbbbbbbbbbbbbbc                                                                            ghhhhhi           XXX              XXR        XXX         XXXXXR            LXXXXX                         XXX                                     # DDXDD                    #DDD                                                                             -    -    -    -          XX                                abbbbbc             XX",
        "                  Ldeeeeeeeeeeeeeeeeeeeeeee     eeeeeeeeeeeeeeeeeeeeeeefR                                                                                            XXXXX              XXR        XXX        XXXXXR              LXXXXX                                                                %   D                      %                                                                                .    .    .    .          -                                 dhhhhhi             XX",
        "                   Ldeeeeeeeeeeeeeeeeeeeeee     eeeeeeeeeeeeeeeeeeeeeefR                                                                                            XXXXXX              XXR                  XXXXXR                LXXXXX                                                               %                          %                                                                                .    .    .    .          .                    abbbc          DD                XX",
        "    abbc            Ldeeeeeeeeeeeeeeeeeeeee     eeeeeeeeeeeeeeeeeeeeefR                                                                                            XXXXXXX              XXR                 XXXXXR                  LXXXXX                                                                                         %                U           U                                                   ,    ,    ,    ,          ,                    deeef                            XX",
        "    deef             Lqhhhhhhhhhhhhhhhhhhhh     hhhhhhhhhhhhhhhhhhhhiR                                                                                            XXXXXXXX              XXR                XXXXXR                    LXXXXX                                                C              C   C                  C %     C         UXU         UXU                C      C        UUU  UUU  UUU  UUU  UUU  UUU  UUU    T       C         T         ghhhi                            XX",
        "    ghhi                                                                            ///            ///            ///                   C                        XXXXXXXXX              XXUU              XXXXXR                      LXXXXX                    XXXXXXXXXXXXXXXXXXX         XXXXXXXXXXXXXXUUUUUXXXXXXXXXXXXXXXXXX  %      XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX         XX                                         XX",
        "                                                                                   XXXXX          XXXXX          XXXXX                UUUXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX              XXXXXXXXXXXXXXXXXXXXXXR                        LXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX         XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  %      XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX         XX                                         XX",
        "                                                                                   XXXXX          XXXXX          XXXXX           XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX                                                                                          ",
    ]
def loadSprites():
    global SS_ALLIES, SS_ENEMIES, SS_ITEM, SS_STRUCTURES, SS_TILES, SS_PROJECTILES,SS_FX
    SS_ALLIES = loadAllies()
    SS_ENEMIES = loadEnemies()
    SS_ITEM = loadItems()
    SS_STRUCTURES = loadStructures()
    SS_TILES = loadTiles()
    SS_PROJECTILES = loadProjectiles()
    SS_FX = loadEffects()
def loadEffects():
    sprites = {}
    #Sprites de items
    fx = pygame.image.load("FX/IceCast.png").convert_alpha()
    icecast=funciones.recortar(fx,96,96)
    fx = pygame.image.load("FX/FireCast.png").convert_alpha()
    firecast=funciones.recortar(fx,96,96)
    fx = pygame.image.load("FX/IceShatter.png").convert_alpha()
    IceShatter=funciones.recortar(fx,96,96)
    fx = pygame.image.load("FX/xplosion.png").convert_alpha()
    xplotion=funciones.recortar(fx,100,100)
    fx = pygame.image.load("FX/status1.png").convert_alpha()
    status1=funciones.recortar(fx,64,64)
    fx = pygame.image.load("FX/status2.png").convert_alpha()
    status2=funciones.recortar(fx,64,64)
    fx = pygame.image.load("FX/dust.png").convert_alpha()
    dust=funciones.recortar(fx,64,64)
    fx = pygame.image.load("FX/earth1.png").convert_alpha()
    earth1=funciones.recortar(fx,64,64)
    fx = pygame.image.load("FX/explosion.png").convert_alpha()
    explosion=funciones.recortar(fx,64,64)
    fx = pygame.image.load("FX/fire.png").convert_alpha()
    fire=funciones.recortar(fx,64,64)
    fx = pygame.image.load("FX/heal.png").convert_alpha()
    heal=funciones.recortar(fx,64,64)
    fx = pygame.image.load("FX/ice.png").convert_alpha()
    ice=funciones.recortar(fx,64,64)
    fx = pygame.image.load("FX/impact1.png").convert_alpha()
    impact1=funciones.recortar(fx,64,64)
    fx = pygame.image.load("FX/lightning.png").convert_alpha()
    lightning=funciones.recortar(fx,64,64)
    fx = pygame.image.load("FX/electro-shock.png").convert_alpha()
    shock=funciones.recortar(fx,128,96)
    fx = pygame.image.load("FX/slash-upward.png").convert_alpha()
    sUp=funciones.recortar(fx,52,56)
    fx = pygame.image.load("FX/slash-horizontal.png").convert_alpha()
    sHor=funciones.recortar(fx,65,40)


    sprites["dust"] = funciones.flatten(dust)
    sprites["earth1"] = funciones.flatten(earth1)
    sprites["explosion"] = funciones.flatten(explosion)
    sprites["fire"] = funciones.flatten(fire)
    sprites["heal"] = funciones.flatten(heal)
    sprites["ice"] = funciones.flatten(ice)
    sprites["impact1"] = funciones.flatten(impact1)
    sprites["lightning"] = funciones.flatten(lightning)
    sprites["shock"] = funciones.flatten(shock)
    sprites["slashUp"] = funciones.flatten(sUp)
    sprites["slashSide"] = funciones.flatten(sHor)
    sprites["iceshatter"] = funciones.flatten(IceShatter)
    sprites["icecast"] = funciones.flatten(icecast)
    sprites["firecast"] = funciones.flatten(firecast)
    sprites["status1"] = funciones.flatten(status1)
    sprites["status2"] = funciones.flatten(status2)
    sprites["xplosion"] = funciones.flatten(xplotion)
    return sprites
def loadEnemies():
    sprites = {}
    #Sprites de los enemigos
    uIdle = pygame.image.load("Sprites/Mobs/Undead/undeadIdle.png").convert_alpha()
    uWalk = pygame.image.load("Sprites/Mobs/Undead/undeadWalk.png").convert_alpha()
    uHit = pygame.image.load("Sprites/Mobs/Undead/undeadHurt.png").convert_alpha()
    uDead = pygame.image.load("Sprites/Mobs/Undead/undeadDeath.png").convert_alpha()
    uAttack = pygame.image.load("Sprites/Mobs/Undead/undeadAttack.png").convert_alpha()
    undeadSprite=funciones.recortarLista([uIdle,uWalk,uHit,uDead,uAttack],[18,20,16,13,20])
    cobra = pygame.image.load("Sprites/Mobs/cobra.png").convert_alpha()
    cobraSprite=funciones.recortar(cobra,32,32)
    hellHound = pygame.image.load("Sprites/Mobs/HellHound.png").convert_alpha()
    hellHoundSprite=funciones.recortar(hellHound,64,38)
    imp = pygame.image.load("Sprites/Mobs/imp.png").convert_alpha()
    impSprite=funciones.recortar(imp,32,32)
    scorpion = pygame.image.load("Sprites/Mobs/scorpion.png").convert_alpha()
    scorpionSprite=funciones.recortar(scorpion,32,32)
    slime = pygame.image.load("Sprites/Mobs/slime.png").convert_alpha()
    slimeSprite=funciones.recortar(slime,32,24)
    mino = pygame.image.load("Sprites/Mobs/minotaur.png").convert_alpha()
    minoSprite = funciones.recortar(mino,126,107)
    gimp = pygame.image.load("Sprites/Mobs/granimp.png").convert_alpha()
    gimpSprite = funciones.recortar(gimp,50,50)
    necro = pygame.image.load("Sprites/Mobs/necromancer.png").convert_alpha()
    necroSprite = funciones.recortar(necro,60,61)
    SAIdle = pygame.image.load("Sprites/Mobs/sArcher/A/idle.png").convert_alpha()
    SARun = pygame.image.load("Sprites/Mobs/sArcher/A/run.png").convert_alpha()
    SAHurt = pygame.image.load("Sprites/Mobs/sArcher/A/hurt.png").convert_alpha()
    SADie = pygame.image.load("Sprites/Mobs/sArcher/A/die.png").convert_alpha()
    SAAttack = pygame.image.load("Sprites/Mobs/sArcher/A/attack.png").convert_alpha()
    sArcherA=funciones.recortarLista([SAIdle,SARun,SAHurt,SADie,SAAttack],[8,8,11,21,20])
    SAIdle = pygame.image.load("Sprites/Mobs/sArcher/B/idle.png").convert_alpha()
    SARun = pygame.image.load("Sprites/Mobs/sArcher/B/run.png").convert_alpha()
    SAHurt = pygame.image.load("Sprites/Mobs/sArcher/B/hurt.png").convert_alpha()
    SADie = pygame.image.load("Sprites/Mobs/sArcher/B/die.png").convert_alpha()
    SAAttack = pygame.image.load("Sprites/Mobs/sArcher/B/attack.png").convert_alpha()
    sArcherB=funciones.recortarLista([SAIdle,SARun,SAHurt,SADie,SAAttack],[8,8,11,21,20])
    SAIdle = pygame.image.load("Sprites/Mobs/sArcher/C/idle.png").convert_alpha()
    SARun = pygame.image.load("Sprites/Mobs/sArcher/C/run.png").convert_alpha()
    SAHurt = pygame.image.load("Sprites/Mobs/sArcher/C/hurt.png").convert_alpha()
    SADie = pygame.image.load("Sprites/Mobs/sArcher/C/die.png").convert_alpha()
    SAAttack = pygame.image.load("Sprites/Mobs/sArcher/C/attack.png").convert_alpha()
    sArcherC=funciones.recortarLista([SAIdle,SARun,SAHurt,SADie,SAAttack],[8,8,11,21,20])
    sWIdle = pygame.image.load("Sprites/Mobs/sWarrior/A/idle.png").convert_alpha()
    SWRun = pygame.image.load("Sprites/Mobs/sWarrior/A/run.png").convert_alpha()
    SWHurt = pygame.image.load("Sprites/Mobs/sWarrior/A/hurt.png").convert_alpha()
    SWDie = pygame.image.load("Sprites/Mobs/sWarrior/A/die.png").convert_alpha()
    SWAttack = pygame.image.load("Sprites/Mobs/sWarrior/A/attack.png").convert_alpha()
    SWBlock = pygame.image.load("Sprites/Mobs/sWarrior/A/block.png").convert_alpha()
    sWarriorA=funciones.recortarLista([sWIdle,SWRun,SWHurt,SWDie,SWAttack,SWBlock],[8,8,13,21,19,12])
    sWIdle = pygame.image.load("Sprites/Mobs/sWarrior/B/idle.png").convert_alpha()
    SWRun = pygame.image.load("Sprites/Mobs/sWarrior/B/run.png").convert_alpha()
    SWHurt = pygame.image.load("Sprites/Mobs/sWarrior/B/hurt.png").convert_alpha()
    SWDie = pygame.image.load("Sprites/Mobs/sWarrior/B/die.png").convert_alpha()
    SWAttack = pygame.image.load("Sprites/Mobs/sWarrior/B/attack.png").convert_alpha()
    SWBlock = pygame.image.load("Sprites/Mobs/sWarrior/B/block.png").convert_alpha()
    sWarriorB=funciones.recortarLista([sWIdle,SWRun,SWHurt,SWDie,SWAttack,SWBlock],[8,8,13,21,19,12])
    sWIdle = pygame.image.load("Sprites/Mobs/sWarrior/C/idle.png").convert_alpha()
    SWRun = pygame.image.load("Sprites/Mobs/sWarrior/C/run.png").convert_alpha()
    SWHurt = pygame.image.load("Sprites/Mobs/sWarrior/C/hurt.png").convert_alpha()
    SWDie = pygame.image.load("Sprites/Mobs/sWarrior/C/die.png").convert_alpha()
    SWAttack = pygame.image.load("Sprites/Mobs/sWarrior/C/attack.png").convert_alpha()
    SWBlock = pygame.image.load("Sprites/Mobs/sWarrior/C/block.png").convert_alpha()
    sWarriorC=funciones.recortarLista([sWIdle,SWRun,SWHurt,SWDie,SWAttack,SWBlock],[8,8,13,21,19,12])

    kIdle = pygame.image.load("Sprites/Mobs/knight/idle.png").convert_alpha()
    kRun = pygame.image.load("Sprites/Mobs/knight/run.png").convert_alpha()
    kRoll = pygame.image.load("Sprites/Mobs/knight/roll.png").convert_alpha()
    kJump = pygame.image.load("Sprites/Mobs/knight/jump.png").convert_alpha()
    kAttack = pygame.image.load("Sprites/Mobs/knight/attack.png").convert_alpha()
    kShield = pygame.image.load("Sprites/Mobs/knight/shield.png").convert_alpha()
    kDeath = pygame.image.load("Sprites/Mobs/knight/death.png").convert_alpha()
    knight=funciones.recortarLista([kIdle,kRun,kRoll,kJump,kAttack,kShield,kDeath],[15,8,10,14,22,7,15])


    bIdle = pygame.image.load("Sprites/Mobs/berserker/idle.png").convert_alpha()
    bWalk = pygame.image.load("Sprites/Mobs/berserker/walk.png").convert_alpha()
    bDash = pygame.image.load("Sprites/Mobs/berserker/dash.png").convert_alpha()
    bTaunt = pygame.image.load("Sprites/Mobs/berserker/taunt.png").convert_alpha()
    bAttack = pygame.image.load("Sprites/Mobs/berserker/attack.png").convert_alpha()
    bSpin = pygame.image.load("Sprites/Mobs/berserker/spinAttack.png").convert_alpha()
    bJump = pygame.image.load("Sprites/Mobs/berserker/jump.png").convert_alpha()
    bLeap = pygame.image.load("Sprites/Mobs/berserker/leap.png").convert_alpha()
    bDeath = pygame.image.load("Sprites/Mobs/berserker/death.png").convert_alpha()
    berserker=funciones.recortarLista([bIdle,bWalk,bDash,bTaunt,bAttack,bSpin,bJump,bLeap,bDeath],[16,8,8,18,30,30,25,40,40])

    sprites["undead"]=undeadSprite
    sprites["cobra"]=cobraSprite
    sprites["hellhound"]=hellHoundSprite
    sprites["imp"]=impSprite
    sprites["scorpion"] = scorpionSprite
    sprites["slime"] = slimeSprite
    sprites["minotaur"] = funciones.flatten(minoSprite)
    sprites["granimp"] = funciones.flatten(gimpSprite)
    sprites["necromancer"] = funciones.flatten(necroSprite)
    sprites["sArcherA"]=sArcherA
    sprites["sArcherB"]=sArcherB
    sprites["sArcherC"]=sArcherC
    sprites["sWarriorA"] = sWarriorA
    sprites["sWarriorB"] = sWarriorB
    sprites["sWarriorC"] = sWarriorC
    sprites["knight"] = knight
    sprites["berserker"] = berserker
    return sprites
def loadAllies():
    sprites = {}
    #Player Sprites
    pUnarmed = pygame.image.load("Sprites/player/playerUnarmed.png").convert_alpha()
    pSpriteUnarmed = funciones.recortar(pUnarmed,50,37)
    pSpriteUnarmed = funciones.flatten(pSpriteUnarmed)
    pSword = pygame.image.load("Sprites/player/playerSword.png").convert_alpha()
    pSpriteSword = funciones.recortar(pSword,50,37)
    pSpriteSword = funciones.flatten(pSpriteSword)
    pBow = pygame.image.load("Sprites/player/playerBow.png").convert_alpha()
    pSpriteBow = funciones.recortar(pBow,50,37)
    pSpriteBow = funciones.flatten(pSpriteBow)
    gladiator = pygame.image.load("Sprites/Mobs/gladiator.png").convert_alpha()
    gladiatorS = funciones.recortar(gladiator,32,32)
    santa = pygame.image.load("Sprites/Mobs/santa.png").convert_alpha()
    santaSprite = funciones.recortar(santa,40,40)
    sprites["pUnarmed"]=pSpriteUnarmed
    sprites["pSword"]=pSpriteSword
    sprites["pBow"]=pSpriteBow
    sprites["santa"] = santaSprite
    sprites["gladiator"]=gladiatorS
    return sprites
def loadItems():
    sprites = {}
    #Sprites de items
    items = pygame.image.load("Sprites/items/items.png").convert_alpha()
    itemsSprite=funciones.recortar(items,16,16)
    potions = pygame.image.load("Sprites/potions.png").convert_alpha()
    potionsSprite=funciones.recortar(potions,16,16)
    keys = pygame.image.load("Sprites/items/keys.png").convert_alpha()
    keysSprite=funciones.recortar(keys,16,16)
    sprites["potions"]=potionsSprite
    sprites["keys"]=keysSprite
    sprites["items"]=itemsSprite
    return sprites
def loadProjectiles():
    sprites = {}
    #Sprites de proyectiles
    arrow = pygame.image.load("Sprites/Projectiles/pArrow.png").convert_alpha()
    pArrow=funciones.recortar(arrow,16,3)
    arrow = pygame.image.load("Sprites/Projectiles/arrowA.png").convert_alpha()
    arrowA=funciones.recortar(arrow,28,5)
    arrow = pygame.image.load("Sprites/Projectiles/arrowB.png").convert_alpha()
    arrowB=funciones.recortar(arrow,28,5)
    arrow = pygame.image.load("Sprites/Projectiles/arrowC.png").convert_alpha()
    arrowC=funciones.recortar(arrow,28,5)
    gift = pygame.image.load("Sprites/Projectiles/gift.png").convert_alpha()
    giftSprite=funciones.recortar(gift,16,16)
    imp = pygame.image.load("Sprites/Mobs/imp.png").convert_alpha()
    impSprite=funciones.recortar(imp,32,32)
    impShot = impSprite[-1]
    gimp = pygame.image.load("Sprites/Projectiles/gimpShot.png").convert_alpha()
    gimpshot=funciones.recortar(gimp,34,9)
    ice = pygame.image.load("Sprites/Projectiles/IcePick.png").convert_alpha()
    IcePick=funciones.recortar(ice,64,64)

    sprites["arrowA"]=arrowA
    sprites["arrowB"]=arrowB
    sprites["arrowC"]=arrowC
    sprites["pArrow"]=pArrow
    sprites["icepick"]=IcePick
    sprites["impShot"]=impShot
    sprites["GImpShot"]=gimpshot
    sprites["gift"] = giftSprite
    return sprites
def loadTiles():
    tiles = {}
    #Sprites de items
    tileSource=pygame.image.load("Dg/tileset.png").convert_alpha()
    tileset=funciones.recortar(tileSource,TILE_SIZE,TILE_SIZE)
    tiles["dungeon"]=tileset
    return tiles
def loadStructures():
    sprites = {}
    #Sprites de Estructuras
    campfire = pygame.image.load("Sprites/campfire.png").convert_alpha()
    campfireSprite=funciones.recortar(campfire,16,16)
    doors = pygame.image.load("Sprites/doors.png").convert_alpha()
    doorsSprite=funciones.recortar2(doors,50,50)
    bearTrap = pygame.image.load("Sprites/BearTrap.png").convert_alpha()
    bearTrapSprite=funciones.recortar(bearTrap,32,32)
    sprites["campfire"]=campfireSprite
    sprites["doors"]=doorsSprite
    sprites["bearTrap"]=bearTrapSprite
    return sprites

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
class Entity(pygame.sprite.Sprite):
    """"Clase abstracta Entity"""
    def __init__(self, color=BLANCO, pos=(0,0), *groups):
        super().__init__(*groups)
        self.image = Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)
class Sprite(Entity):
    """"Clase abstracta Sprite"""
    def __init__(self,platforms,pos=(0,0),*groups):
        super().__init__()
        self.vel = pygame.Vector2((0, 0))
        self.onGround = False
        self.platforms = platforms
        self.nearbyTiles = self.platforms
        self.obstacles = []
        self.nearbyObst=self.obstacles
        self.startPos=(0,0)
        self.chunkSize=(WIN_WIDTH,HALF_HEIGHT)
        self.speed = 1#mod
        self.hp = 3
        self.fx = None
        self.immunity = 50
        self.animationTime = 0.1
        self.currentTime = 0
        self.animationFrames = 6
        self.currentFrame = 0
        self.dead=3
        self.dir= random.randint(0,1)
        self.action=0
        self.act=self.action
        self.con=0
        self.lim=[0]#mod
        self.rect=Rect(pos[0],pos[1],TILE_SIZE*2,TILE_SIZE*2)
        self.hitbox = self.rect
        self.onCamera = False
        self.lifespan = 0

    def newLevel(self,platforms):
        self.platforms = platforms

    def checkNearby(self):
        movedx=abs(self.rect[0]-self.startPos[0])
        movedy=abs(self.rect[1]-self.startPos[1])
        if(movedx >= (self.chunkSize[0] - 100) or movedy >= (self.chunkSize[1] - 100)):
            self.refreshNearby()
            if self.obstacles!=[]:
                self.refreshHitItems()
    def refreshNearby(self):
        nearby = pygame.sprite.Group()
        for p in self.platforms:
            distx = abs(self.rect[0] - p.rect[0])
            disty = abs(self.rect[1] - p.rect[1])
            if distx <= self.chunkSize[0] and disty <= self.chunkSize[1]:
                nearby.add(p)
        self.nearbyTiles = nearby
        self.startPos = self.rect.center

    def refreshHitItems(self):
        nearby = pygame.sprite.Group()
        for p in self.obstacles:
            distx = abs(self.rect[0] - p.rect[0])
            disty = abs(self.rect[1] - p.rect[1])
            if distx <= self.chunkSize[0] and disty <= self.chunkSize[1]:
                nearby.add(p)
        self.nearbyObst = nearby

    def collideVertical(self,blocks,dif=0):
        for p in self.nearbyTiles:
            if (p.type in blocks) and self.hitbox.colliderect(p.rect):
                if self.vel.y < 0:
                    self.vel.y=0
                    self.hitbox.top = p.rect.bottom
                if self.vel.y > 0:
                    self.hitbox.bottom = p.rect.top
                    self.onGround = True
                self.rect.bottom = self.hitbox.bottom+dif

    def spawnItem(self,items,t=0):
        self.items=items
        if DIFFICULTY == 0:
            if t==1:t=0
        i = Potion((self.hitbox.left,self.hitbox.bottom-16),t)
        self.items.add(i)
        items = self.items
class Enemy(Sprite):
    """"Clase abstracta Enemy"""
    def __init__(self,platforms,pos=(0,0),*args):
        super().__init__(platforms,pos)
        self.move = 1
        self.idle = 0
        self.damage = 1
        self.key = None
        self.hasKey = False
        self.itemDroped=False
        self.pain = pygame.mixer.Sound("SFX/undeadPain.ogg")
        self.timeAttack = 0

    def die(self):
        print("dead")
        self.action=self.dead
        self.vel.x=0
    def move(self,sx=0):
        if sx==0:
            sx = self.speed
        if self.dir==1:
            self.vel.x = sx
        else:
            self.vel.x = -sx
    def checkLifespan(self):
        if self.lifespan > 1:
            self.lifespan -=1
            if self.lifespan == 1:
                self.die()

    def createKey(self,items):
        self.key = Key((self.rect.center[0],self.rect.top-16),1,False)
        items.add(self.key)
        self.hasKey = True
    def updateKey(self):
        if self.hasKey:
            self.key.hitbox.center = self.hitbox.center
            self.key.hitbox.top = self.hitbox.top-16
    def dropKey(self,items):
        k = Key(self.hitbox.midtop)
        items.add(k)

    def dropWeapon(self,items,t=2):
        if t == 0:
            w = SwordItem((self.hitbox.center[0],self.hitbox.bottom-16))
        elif t == 1:
            w = BowItem((self.hitbox.center[0],self.hitbox.bottom-16))
        else:
            w = ArrowItem((self.hitbox.center[0],self.hitbox.bottom-16))
        items.add(w)

    def gotHit(self,hit,maxImmunity=100,hurt=2):
        if self.immunity <= 50:
            self.pain.play()
            self.hp -= hit
            self.immunity = maxImmunity
            self.action = hurt
            self.vel.x = 0
            if self.hp<=0:
                self.die()
    def animation_mat(self,dt,priority=[3,4],usual=[0,1]):
        #Time dependant
        #Prioridad de animaciones
        if (self.action in priority) and self.act != self.action:
            self.act = self.action
            self.con = 0
            self.vel.x = 0.1
        #Cambiar en cualquier momento de animacion
        if (self.act in usual) and self.act != self.action:
            self.act = self.action
            self.con = 0
        #Direccion
        if self.dir == 1: #derecha
            sprite = self.mR
        else:#izquierda
            sprite = self.mL
        #Cantidad de imagenes de la accion
        images = self.lim[self.act]
        self.currentTime += dt
        if self.currentTime >= self.animationTime:
            self.currentTime = 0
            self.con = (self.con % images)
            index = self.con
            self.image = sprite[self.act][index]
            self.con += 1
            #reset de animacion
            if index == self.lim[self.act]-1:
                if self.act == self.dead: self.kill()
                if self.vel.x != 0: self.action = self.move
                else: self.action=self.idle
                self.act = self.action
                self.con = 0
    def animation_list(self,dt,priority=[3,4],usual=[0,1]):
        #Time dependant
        if self.dir == 1: #derecha
            sprite = self.mR
        else:#izquierda
            sprite = self.mL
        #Prioridad de animaciones
        if (self.action in priority) and self.act != self.action:
            self.act = self.action
            self.con = 0
        #Cambiar en cualquier momento de animacion
        if (self.act in usual) and self.act != self.action:
            self.act = self.action
            self.con = 0
        #Cantidad de imagenes de la accion
        images =self.lim[self.act+1] - self.lim[self.act]
        self.currentTime += dt
        if self.currentTime >= self.animationTime:
            self.currentTime = 0
            self.con = ((self.con) % images)
            index = self.con + self.lim[self.act]
            self.image = sprite[index]
            self.con += 1
            #reset de animacion
            if index == self.lim[self.act+1]-1:
                if self.act == self.dead: self.kill()
                if self.vel.x != 0: self.action = self.move
                else: self.action=self.idle
                self.act = self.action
                self.con = 0
    def animation(self,fSpeed=0.3,idle=0):
        if self.dir == 1:
            self.image=self.mR[self.act][int(self.con)]
        else:
            self.image=self.mL[self.act][int(self.con)]
        if self.con < self.lim[self.act]-fSpeed:
            self.con+=fSpeed
        else:
            if(self.act==self.dead):self.kill()
            self.con=0
            if self.vel.x != 0: self.action = self.move
            else: self.action=idle
            self.act = self.action
    def collideHorizontal(self,blocks,changeDir = True):
        for p in self.nearbyTiles:
            if (p.type in blocks) and self.hitbox.colliderect(p.rect):
                if self.vel.x > 0:
                    self.hitbox.right = p.rect.left
                    if changeDir:self.dir = 0
                    self.vel.x = self.speed
                if self.vel.x < 0:
                    self.hitbox.left = p.rect.right
                    if changeDir:self.dir = 1
                    self.vel.x = -self.speed
                self.rect.center = self.hitbox.center
"""Enemies"""
class Undead(Enemy):
    def __init__(self,platforms, pos,speed=1, *groups):
        super().__init__(platforms,pos)
        asset = SS_ENEMIES["undead"]
        self.chasing = False
        self.speed = speed
        self.hp = 5
        self.damage = 3
        #0=Idle,1=Walk,2=Hurt,3=Dead,4=Attack
        self.lim=[18,20,16,13,20]
        self.mR=asset
        self.mL=funciones.spriteFlip(asset)
        self.image=self.mL[self.action][self.con]
        self.rect=Rect(pos[0],pos[1],TILE_SIZE*3,TILE_SIZE*2+4)
        self.hitbox = self.rect.inflate(-16,-4)
        self.hitbox.midbottom = self.rect.midbottom
        self.chunkSize=(HALF_WIDTH/2,HALF_HEIGHT/2)
        self.pain = pygame.mixer.Sound("SFX/undeadPain.ogg")
        self.pain.set_volume(0.5)
        self.refreshNearby()

    def update(self,player,dt,items,*args):
        #0=idle
        self.checkNearby()
        if self.action==self.dead and not self.itemDroped:
            self.spawnItem(items,random.randint(0,4))
            self.itemDroped = True
        self.checkLifespan()
        if not self.onGround:
            #only accelerate with gravity if in the air
            self.vel += GRAVITY
            #max falling speed
            if self.vel.y > 50: self.vel.y=50
        elif self.chasing and self.act == 1:
            if self.dir==1:
                self.vel.x = self.speed
            else:
                self.vel.x = -self.speed
        # increment in x direction
        self.rect.left += self.vel.x
        self.hitbox.left += self.vel.x
        self.collidePlayer(player)
        # do x-axis collisions
        self.collideHorizontal()
        # increment in y direction
        self.rect.top += self.vel.y
        self.hitbox.top += self.vel.y
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collideVertical()
        self.animation_mat(dt,[2,3])
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
            self.action=1
            if not self.chasing:
                self.chasing = True
                if self.hitbox.x < player.hitbox.x:
                    self.dir = 1
                else:
                    self.dir = 0
            if self.immunity == 0 and distx<=150 and player.vel.x != 0:
                self.action=4
                self.vel.x=0
        elif self.action!=3:
            self.onCamera = False
            self.chasing = False
            self.action = 0
            self.vel.x = 0
        if self.immunity > 0:
            self.immunity -=1

    def collidePlayer(self,p):
        if self.rect.colliderect(p.hitbox):
            if self.rect.x < p.rect.x:
                self.dir = 1
            else:
                self.dir = 0
            if self.immunity == 0:
                self.action=4
                self.vel.x=0
            dist = abs(self.hitbox.x - p.hitbox.x)
            if self.act==4 and self.con >= 7 and self.con <= 11 and dist < 40 and self.immunity == 0:
                p.gotHit(self.damage)
    def collideHorizontal(self):
        super().collideHorizontal([0])
    def collideVertical(self):
        super().collideVertical([0])
class Cobra(Enemy):
    def __init__(self,platforms, pos,speed=2, *groups):
        super().__init__(platforms,pos)
        asset = SS_ENEMIES["cobra"]
        self.speed = speed
        #0=Idle,1=Walk,2=Attack,3=Hurt,4=Dead,5=spawn
        self.lim=[8,8,6,4,6,6]
        self.dead=4
        self.venomous = DIFFICULTY
        self.action=5
        self.mR=asset
        self.mL=funciones.spriteFlip(asset)
        self.image=self.mR[self.action][self.con]
        self.rect.bottom = pos[1]
        self.hitbox = self.rect.inflate(-8,-16)
        self.hitbox.midbottom = self.rect.midbottom
        self.pain = pygame.mixer.Sound("SFX/snakePain.ogg")
        self.refreshNearby()

    def gotHit(self,hit):
        super().gotHit(hit,180,3)

    def update(self,player,dt,items,*args):
        #0=idle
        self.checkNearby()
        if self.action==self.dead and not self.itemDroped:
            r = random.randint(0,5)
            if r == 1:self.spawnItem(items,random.randint(0,4))
            self.itemDroped = True
        self.checkLifespan()
        if not self.onGround:
            self.vel.x = 0
            #only accelerate with gravity if in the air
            self.vel += GRAVITY
            #max falling speed
            if self.vel.y > 50: self.vel.y=50
        elif self.act <= 1:
            if self.dir==1:
                self.vel.x = self.speed
            else:
                self.vel.x = -self.speed
            if self.immunity > 0:
                self.vel.x *= 2
        # increment in x direction
        self.rect.left += self.vel.x
        self.hitbox.left += self.vel.x
        self.collidePlayer(player)
        # do x-axis collisions
        self.collideHorizontal()
        # increment in y direction
        self.rect.top += self.vel.y
        self.hitbox.top += self.vel.y
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collideVertical()
        self.animation_mat(dt)
        if self.immunity > 0:
            self.immunity -=1
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False

    def collidePlayer(self,p):
        if self.rect.colliderect(p.hitbox) and self.immunity == 0:
            if self.hitbox.x < p.hitbox.x:
                self.dir = 1
            else:
                self.dir = 0
            if abs(self.hitbox.x - p.hitbox.x) < 20:
                self.action = 2
                self.vel.x = 0
                if self.act == 2 and int(self.con) == 4:
                    if self.venomous > 0:p.setPoison(self.venomous)
                    p.gotHit(self.damage)
    def collideHorizontal(self):
        super().collideHorizontal([0,1])
    def collideVertical(self):
        super().collideVertical([0])
class Spawner(Sprite):
    def __init__(self,platforms, pos,mob, *args):
        super().__init__(platforms)
        asset = SS_STRUCTURES["campfire"]
        self.destroyed=False
        self.hp = 4
        self.spawnCD = 0
        self.mob = mob
        self.action = mob
        self.spawnTime = 200
        self.pain = pygame.mixer.Sound("SFX/spawnPain.ogg")
        #0=idle,1=hit,2=destroyed
        self.enemies = []
        self.mR=asset
        self.image=self.mR[self.action][self.con]
        self.rect= self.image.get_rect(topleft=pos)
        self.hitbox = self.rect
        self.lim=[4,4,4,4,4,4]

    def destroy(self):
        self.destroyed = True

    def gotHit(self,hit):
        if self.immunity == 0:
            self.pain.play()
            self.hp -= hit
            self.immunity = 30
            #self.action = 1
            self.spawnTime = 5
            if self.hp<=0:
                self.destroy()
    def staticAnimation(self):
        self.image=self.mR[self.action][int(self.con)]
        if self.con < self.lim[self.action]-0.1:
            self.con+=0.1
        else:
            self.con=0

    def update(self,player,enemies,items,*args):
        self.staticAnimation()
        if self.immunity > 0:
            self.immunity -=1
        if self.spawnTime > 0:
            self.spawnTime -= 1
        else:
            self.enemies = enemies
            self.spawnEnemy()
            enemies = self.enemies
        if self.destroyed:
            self.spawnItem(items)
            self.enemies = enemies
            self.spawnEnemy(1)
            enemies = self.enemies
            self.kill()
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False

    def spawnEnemy(self,speed=round(random.uniform(1,3), 2)):
        if self.mob == 0:
            mob = Cobra(self.platforms, (self.rect.center),speed)
        elif self.mob == 1:
            mob = Undead(self.platforms, (self.rect.center),speed)
        mob.lifespan = 1000
        self.enemies.add(mob)
        self.spawnTime = 1200
class HellHound(Spawner,Enemy):
    '''Clase HellHound'''
    def __init__(self,platforms, pos,key_=False,items = None,speed=3, *groups):
        '''Constructor'''
        super().__init__(platforms, pos, 0)
        asset = SS_ENEMIES["hellhound"]
        self.hp = 7
        self.speed = speed
        self.originalSpeed=speed
        #0=Idle,1=Walk,2=Hurt,3=Dead,4=run,5=jump,6=spawnEgg
        self.lim=[7,6,5,4,5,6,6]
        self.mR=funciones.spriteFlip(asset)
        self.mL=asset
        self.rect=Rect(pos[0],pos[1],TILE_SIZE*4,TILE_SIZE*2+4)
        self.hitbox = self.rect.inflate(-32,-12)
        self.enemies = []
        self.running = 0
        self.dead = -1
        self.idle = self.move
        self.spawn = False
        self.jumping=False
        self.blocks = [0,1]
        self.jump_strength = 4
        self.colliding=0
        self.pain = pygame.mixer.Sound("SFX/dogPain.ogg")
        self.chunkSize=(WIN_WIDTH*3,WIN_HEIGHT)
        self.refreshNearby()
        if key_:
            self.createKey(items)

    def die(self):
        print("dead")
        self.vel.x=0
        self.kill()
    def gotHit(self,hit):
        if self.immunity == 0:
            self.pain.play()
            self.hp -= hit
            self.immunity = 90
            self.running = 180
            if self.act==0:self.running = 10
            self.action = 2
            self.spawnTime = 90
            self.vel.x=0

    def update(self,player,dt,items,p,e,enemies,*args):
        #0=idle
        if self.hp<=0:
            self.vel.x=0
            self.action=3
        self.checkNearby()
        if self.act==3 and self.con > 2:
            if self.hasKey:
                self.key.kill()
                self.dropKey(items)
                self.hasKey = False
        if(self.act==3) and self.con == self.lim[self.act]-1:
            if self.currentTime+dt >=self.animationTime:
                self.destroyed = True
        if self.destroyed:
            self.spawnItem(items)
            self.spawnEnemy(enemies,2)
            self.die()
        if self.spawn:
            self.spawnEnemy(enemies)
            self.spawn=False
            self.spawnCD = 60

        if not self.onGround:
            #only accelerate with gravity if in the air
            self.vel += GRAVITY
            #max falling speed
            if self.vel.y > 50: self.vel.y=50

        elif self.action == self.move:
            if self.dir==1:
                self.vel.x = self.speed
            else:
                self.vel.x = -self.speed
            if self.action == 0:
                self.vel.x = 0
        # increment in x direction
        self.rect.left += self.vel.x
        self.collidePlayer(player)
        self.hitbox.center = self.rect.center
        # do x-axis collisions
        self.collideHorizontal()
        # increment in y direction
        #Modificado
        self.rect.bottom += self.vel.y
        self.hitbox.bottom = self.rect.bottom
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collideVertical()
        self.updateKey()
        if self.spawnTime > 0:
            self.spawnTime -= 1
        elif self.onGround:
            self.action=6
            self.vel.x = 0
        if self.running > 0:
            self.running -=1
            self.speed=self.originalSpeed*2
            if self.running == 0:
                self.speed = self.originalSpeed
                self.move=1
        if self.jumping and not self.act in [2,3]:
            self.action=5
            if self.vel.y < 0 and self.con >= 2:
                self.con = 2
            if self.vel.y > 0 and self.con >= 4:
                self.con = 4
            if self.dir==1:
                self.vel.x = self.speed
            else:
                self.vel.x = -self.speed
        if self.colliding >=30:
            if self.dir==1:self.dir = 0
            else: self.dir = 1
        if self.act == 3:
            self.animationTime = 0.2
        self.animation_mat(dt,[2,3],[0,1,4])

        if(self.act==6) and self.con == self.lim[self.act]-1 and self.spawnCD == 0:
            self.spawn=True
        if self.immunity > 0:
            self.immunity -=1
        if self.spawnCD > 0:
            self.spawnCD -=1

        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False
    def collidePlayer(self,p):
        if self.hitbox.colliderect(p.hitbox) and self.immunity == 0 and self.act!=6:
            if self.hitbox.x < p.hitbox.x:
                self.dir = 0
            else:
                self.dir = 1
            self.action=4
            self.move=4
            self.spawnTime = 90
            self.running = 90
    def spawnEnemy(self,enemies,speed=2):
        self.enemies = enemies
        mob = Cobra(self.platforms, (self.rect.center[0]-16,self.rect.bottom),speed)
        mob.rect.bottom
        mob.lifespan = 600
        self.enemies.add(mob)
        enemies = self.enemies
        self.spawnTime = 600
    def collideHorizontal(self):
        collided=False
        for p in self.platforms:
            if (p.type in self.blocks) and self.hitbox.colliderect(p.hitbox):
                if p.type==0 :
                    if self.vel.x > 0:
                        self.hitbox.right = p.rect.left
                        self.rect.center = self.hitbox.center
                        self.vel.x = 0
                        self.colliding+=1
                    if self.vel.x < 0:
                        self.hitbox.left = p.rect.right
                        self.rect.center = self.hitbox.center
                        self.vel.x = 0
                        self.colliding+=1
                    collided=True
                elif p.type==1:
                    if not self.jumping:self.jump()
        if not collided: self.colliding=0
    def jump(self):
        self.jumping = True
        self.action = 5
        self.vel.y = -self.jump_strength
    def collideVertical(self):
        super().collideVertical([0])
        if self.onGround:
            self.jumping = False
class Imp(Enemy):
    def __init__(self,platforms, pos,speed=2, *groups):
        super().__init__(platforms,pos)
        asset = SS_ENEMIES["imp"]
        self.speed = speed
        self.r=random.randint(0,1)
        #0=Idle,1=Walk,2=Attack,3=Hurt,4=Dead
        self.lim=[7,8,6,4,6]
        self.dead=4
        self.action=0
        self.evolved = False
        self.mR=asset
        self.mL=funciones.spriteFlip(asset)
        self.image=self.mR[self.action][self.con]
        self.hitbox = self.rect.inflate(-8,-16)
        self.hitbox.midbottom = self.rect.midbottom
        self.pain = pygame.mixer.Sound("SFX/impPain.ogg")
        self.refreshNearby()

    def gotHit(self,hit):
        super().gotHit(hit,180,3)
    def attack(self,pX,projectiles):
        if pX < self.rect[0]:
            self.dir = 0
        else:
            self.dir = 1
        self.action = 2
        p = projectiles
        shot=ImpShot(self.platforms,self.rect.center,self.dir)
        p.add(shot)
        projectiles = p
    def update(self,player,dt,items,projectiles,e,mobs,*args):
        #0=idle
        self.checkNearby()
        if self.action==self.dead and int(self.con)==5:
            if not self.itemDroped:
                r = random.randint(0,5)
                if r == 1:self.spawnItem(items,random.randint(0,4))
                self.itemDroped = True
            if not self.evolved:
                if self.r == 1:
                    evo = GranImp(self.platforms, self.rect.center,5)
                    evo.rect.bottom = self.rect.bottom
                    mobs.add(evo)
                self.evolved = True
        self.checkLifespan()
        if not self.onGround:
            #only accelerate with gravity if in the air
            self.vel += GRAVITY
            #max falling speed
            if self.vel.y > 50: self.vel.y=50
        elif self.act == 1:
            if self.dir==1:
                self.vel.x = self.speed
            else:
                self.vel.x = -self.speed
            if self.immunity > 0 or self.timeAttack > 0:
                self.vel.x *= 2
        if self.act == 2:
            self.vel.x = 0
        # increment in x direction
        self.rect.left += self.vel.x
        self.hitbox.left += self.vel.x
        self.collidePlayer(player)
        # do x-axis collisions
        self.collideHorizontal()
        # increment in y direction
        self.rect.top += self.vel.y
        self.hitbox.top += self.vel.y
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collideVertical()
        self.animation_mat(dt)
        if self.immunity > 0:
            self.immunity -=1
        if self.timeAttack > 0:
            self.timeAttack -= 1
            if self.timeAttack == 0:
                self.attack(player.rect[0],projectiles)
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False

    def collidePlayer(self,p):
        if self.rect.colliderect(p.hitbox) and self.immunity == 0:
            if self.hitbox.x < p.hitbox.x:
                self.dir = 0
                self.action = 1
            else:
                self.dir = 1
                self.action = 1
            self.timeAttack = 100
    def collideHorizontal(self):
        super().collideHorizontal([0,1])
    def collideVertical(self):
        super().collideVertical([0])
class Scorpion(Enemy):
    def __init__(self,platforms, pos,speed=2, *groups):
        super().__init__(platforms,pos)
        asset = SS_ENEMIES["scorpion"]
        self.speed = speed
        self.hp = 4
        self.damage = 2
        #0=Idle,1=Walk,2=Attack,3=Hurt,4=Dead
        self.lim=[4,4,4,3,5,4]
        self.dead=4
        self.action=0
        self.mR=asset
        self.mL=funciones.spriteFlip(asset)
        self.image=self.mR[self.action][self.con]
        self.pain = pygame.mixer.Sound("SFX/snakePain.ogg")
        self.spit = pygame.mixer.Sound("SFX/spit.ogg")
        self.spit.set_volume(0.1)
        self.rect= self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-8,-16)
        self.hitbox.midbottom = self.rect.midbottom
        self.gun = Rect(0,0,256,2)
        self.gun.center = self.hitbox.center
        self.refreshNearby()

    def gotHit(self,hit):
        super().gotHit(hit,180,3)
    def shot(self,p):
        if p.rect.x > self.rect.x:
            self.dir = 1
        else:
            self.dir = 0
        self.action = 5
        if self.onCamera:self.spit.play()
        self.spit.set_volume(0.1)
    def update(self,player,dt,items,*args):
        #0=idle
        self.checkNearby()
        if not player.onGround and self.act == 2:
            super().move()
        if self.act == 5:
            self.spit.set_volume(0.2)
            self.vel.x = 0
            if self.con == 1:
                self.animationTime = 1.7
            else:
                self.spit.set_volume(2.0)
                self.animationTime = 0.1
            if self.con == 2:
                if self.gun.colliderect(player.hitbox):
                    player.gotHit(self.damage*2.5,2,self.hitbox)

        if self.action==self.dead and not self.itemDroped:
            r = random.randint(0,5)
            if r == 1:self.spawnItem(items,random.randint(0,4))
            self.itemDroped = True
        self.checkLifespan()
        if not self.onGround:
            #only accelerate with gravity if in the air
            self.vel += GRAVITY
            #max falling speed
            if self.vel.y > 50: self.vel.y=50
        elif self.act <= 1:
            if self.dir==1:
                self.vel.x = self.speed
            else:
                self.vel.x = -self.speed
            if self.immunity > 0 or self.timeAttack > 0:
                self.vel.x *= 2
        if self.act == 2:
            if self.dir==1:
                self.vel.x = 0.5
            else:
                self.vel.x = -0.5
        # increment in x direction
        self.rect.left += self.vel.x
        self.hitbox.left += self.vel.x
        # do x-axis collisions
        self.collideHorizontal()
        # increment in y direction
        self.rect.top += self.vel.y
        self.hitbox.top += self.vel.y
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collideVertical()
        if self.dir == 1:
            self.gun.midleft = self.hitbox.midright
        else:
            self.gun.midright = self.hitbox.midleft
        self.collidePlayer(player)
        self.animation_mat(dt)
        if self.immunity > 0:
            self.immunity -=1
            if self.immunity == 0:
                self.shot(player)
        if self.timeAttack > 0:
            self.timeAttack -= 1
            self.action = 1
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False
    def collidePlayer(self,p):
        if self.rect.colliderect(p.hitbox):
            if self.timeAttack == 0 and self.immunity == 0:
                if p.rect.x > self.rect.x:
                    self.dir = 1
                else:
                    self.dir=0
                self.action = 2
                self.timeAttack = 100
            if self.act == 2:
                if p.rect.x > self.rect.x:self.dir = 1
                else:self.dir=0
                if self.con >=2:
                    p.gotHit(self.damage)
    def collideHorizontal(self):
        super().collideHorizontal([0,1])
    def collideVertical(self):
        super().collideVertical([0])
class Slime(Enemy):
    def __init__(self,platforms, pos,speed=1, *groups):
        super().__init__(platforms,pos)
        asset = SS_ENEMIES["slime"]
        self.speed = speed
        self.hp = 2
        #0=Idle,1=Walk,2=Attack,3=Hurt,4=Dead
        self.lim=[4,4,4,5]
        self.dead=3
        self.action=0
        self.mL=asset
        self.mR=funciones.spriteFlip(asset)
        self.image=self.mR[self.action][self.con]
        self.pain = pygame.mixer.Sound("SFX/slimePain.ogg")
        self.rect= self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(0,-6)
        self.hitbox.bottom = self.rect.bottom
        self.refreshNearby()

    def gotHit(self,hit):
        super().gotHit(hit,60)
        super().move()
    def update(self,player,dt,items,*args):
        #0=idle
        self.checkNearby()
        if self.action==self.dead and not self.itemDroped:
            r = random.randint(0,5)
            if r == 1:self.spawnItem(items,random.randint(0,4))
            self.itemDroped = True
        self.checkLifespan()
        if not self.onGround:
            self.vel.x = 0
            #only accelerate with gravity if in the air
            self.vel += GRAVITY
            #max falling speed
            if self.vel.y > 50: self.vel.y=50
        elif self.act == 1:
            if self.dir==1:
                self.vel.x = self.speed
            else:
                self.vel.x = -self.speed
        # increment in x direction
        self.rect.left += self.vel.x
        self.hitbox.left += self.vel.x
        self.collidePlayer(player)
        # do x-axis collisions
        self.collideHorizontal()
        # increment in y direction
        self.rect.top += self.vel.y
        self.hitbox.top += self.vel.y
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collideVertical()
        self.animation_mat(dt,[2,3])
        if self.immunity > 0:
            self.immunity -=1
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False
    def collidePlayer(self,p):
        if self.hitbox.colliderect(p.hitbox):
            p.jump(6.5,True)
            p.shooting = False
            self.gotHit(0)
    def collideHorizontal(self):
        super().collideHorizontal([0,1])
    def collideVertical(self):
        super().collideVertical([0])

class Santa(Enemy):
    def __init__(self,platforms, pos,speed=2, *groups):
        super().__init__(platforms,pos)
        asset = SS_ALLIES["santa"]
        self.speed = speed
        self.hp = 3
        #0=Idle,1=Walk,2=Attack,3=Hurt,4=Dead
        self.lim=[5,8,5,5,6,9,8,6,5,4,7]
        self.dead=10
        self.action=0
        self.mR=asset
        self.mL=funciones.spriteFlip(asset)
        self.image=self.mR[self.action][self.con]
        self.rect= self.image.get_rect(center=pos)
        self.hitbox = self.rect
        self.pain = pygame.mixer.Sound("SFX/snakePain.ogg")
        self.refreshNearby()
        self.linea1 =""
        self.linea2 =""
        self.linea3 =""
        self.linea4 =""
        self.text = 0
        self.textCD = 0


    def gotHit(self,hit):
        if self.immunity == 0:
            print("ow")
            self.immunity = 150
    def resetText(self):
        if self.text > 1:
            if self.text < 5:
                self.text = 2
            elif self.text < 7:
                self.text = 5

    def changeText(self,sc):
        if self.text == 0:
            self.linea1.update("Saludos aventurero!",sc)
            self.linea2.update("Eres nuevo por aqui?",sc)
            self.linea3.update("No viene mucha gente",sc)
            self.linea4.update("Que te trae a este lugar?(presiona W)",sc)
        if self.text == 1:
            self.linea1.update("Ah ya veo, vienes por eso...",sc)
            self.linea2.update("Es un camino dificil...",sc)
            self.linea3.update("Pero mi trabajo no es desmotivarte",sc)
            self.linea4.update("Te ayudare un poco, pon atencion",sc)
        if self.text == 2:
            self.linea1.update("Con W entras en puertas, como esa de al fondo",sc)
            self.linea2.update("Oh, pero esta cerrada",sc)
            self.linea3.update("Ves ese esqueleto de abajo?",sc)
            self.linea4.update("Tendras que quitarle la llave...",sc)
        if self.text == 3:
            self.linea1.update("Con Shift puedes ir mas rapido",sc)
            self.linea2.update("Ah y con J podras aporrear a ese esqueleto",sc)
            self.linea3.update("Ve a intentarlo, pero cuidado con la cobra",sc)
            self.linea4.update("Es peligrosa y puede envenenarte",sc)
        if self.text == 4:
            self.linea1.update("Con E puedes tomar una pocion",sc)
            self.linea2.update("Por si te golpeas mucho",sc)
            self.linea3.update("Y con R un antidoto",sc)
            self.linea4.update("Para evitar ese sucio veneno",sc)
        if self.text == 5:
            self.linea1.update("Oh, veo q tienes una espada",sc)
            self.linea2.update("Te sera muy util en este lugar",sc)
            self.linea3.update("Pero ten cuidado, no todo es bueno",sc)
            self.linea4.update("No podras correr",sc)
        if self.text == 6:
            self.linea1.update("Pruebala, con F la sacas",sc)
            self.linea2.update("Golpeas con J, haras mas daño",sc)
            self.linea3.update("Pero no podras saltar si la tienes afuera",sc)
            self.linea4.update("Si la quieres soltar usa la Q",sc)
        if self.text == 7:
            self.linea1.update("Y como ultimo consejo mio",sc)
            self.linea2.update("Abajo encontraras un arco y flecha",sc)
            self.linea3.update("Con la K lo disparas, no lo dejes",sc)
            self.linea4.update("Ahora si, ve con todo!",sc)

    def update(self,player,dt,i,p,e,mobs,sc,*args):
        #0=idle
        if self.linea1 == "":
            self.linea1 = ChatBox("I",sc,20)
            self.linea2 = ChatBox("I",sc,20)
            self.linea3 = ChatBox("I",sc,20)
            self.linea4 = ChatBox("I",sc,20)
        self.changeText(sc)
        self.checkNearby()
        self.checkLifespan()
        if not self.onGround:
            self.vel.x = 0
            #only accelerate with gravity if in the air
            self.vel += GRAVITY
            #max falling speed
            if self.vel.y > 50: self.vel.y=50
        # increment in x direction
        self.rect.left += self.vel.x
        self.collidePlayer(player,sc)
        self.hitbox.left += self.vel.x
        # do x-axis collisions
        self.collideHorizontal()
        # increment in y direction
        self.rect.top += self.vel.y
        self.hitbox.top += self.vel.y
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collideVertical()
        self.animation_mat(dt)
        if self.immunity > 0:
            self.immunity -=1
        if self.textCD > 0:
            self.textCD -= 1
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False

    def collidePlayer(self,p,sc):
        next_ = False
        if self.rect.colliderect(p.rect):
            sc.blit(self.linea1.image,(200,40))
            sc.blit(self.linea2.image,(200,60))
            sc.blit(self.linea3.image,(200,80))
            sc.blit(self.linea4.image,(200,100))
            if self.action == 2:
                print("saludos")
            if p.activate:
                if self.text < 4 and self.textCD == 0:
                    self.text += 1
                    self.textCD = 50
                if p.sword and self.text >= 4 and self.textCD == 0:
                    if self.text < 7:
                        self.text +=1
                        self.textCD = 50
            self.action = 0
            if self.hitbox.center[0]<p.hitbox.center[0]:
                self.dir = 1
            else:
                self.dir = 0
        else:
            self.action = 2
            self.resetText()
            #if next_:
            #    self.text += 1

    def collideHorizontal(self):
        super().collideHorizontal([0])
    def collideVertical(self):
        super().collideVertical([0])
class ChatBox(pygame.sprite.Sprite):
    def __init__(self,string,screen,size):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, size)
        self.image = self.font.render(string, 0, (255, 255, 255),screen)

    def update(self, string,screen):
        self.image = self.font.render(string, 0, (255, 255, 255),screen)
class SkeletonArcherBase(Enemy):
    def __init__(self,platforms, pos,key_=False,items = None,speed=3, *groups):
        super().__init__(platforms,pos)
        self.hp = 10
        self.damage = 3
        self.timeSpecial = 0
        asset = SS_ENEMIES["sArcherA"]
        self.originalSpeed = speed
        self.speed = self.originalSpeed
        self.type=0
        #0=Idle,1=Walk,2=Attack,3=Hurt,4=Dead
        self.lim=[8,8,11,21,20]
        self.dead=3
        self.action=0
        self.timeAttack = -1
        self.attackType = 0
        self.rapidArrows = 5
        self.mR=asset
        self.mL=funciones.spriteFlip(asset)
        self.image=self.mR[self.action][self.con]
        self.rect= self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-40,-20)
        self.dir = 1
        self.hitbox.left = self.rect.left +10
        self.hitbox.bottom = self.rect.bottom -4
        self.pain = pygame.mixer.Sound("SFX/undeadPain.ogg")
        self.refreshNearby()
        if key_:
            self.createKey(items)

    def gotHit(self,hit):
        super().gotHit(hit,180,2)
        self.attackType = 1
        self.timeAttack = 0

    def createFx(self,effects,t=0):
        if t == 1:
            t = 2
        elif t == 2:
            t = 0
        self.fx = CastEffects(self.hitbox.center,t)
        effects.add(self.fx)
    def updateFx(self):
        if self.fx!=None:
            self.fx.rect.center = self.hitbox.center


    def checkHitbox(self):
        if self.dir==1:
            self.rect.left=self.hitbox.left-10
        else:
            self.rect.right=self.hitbox.right+10
    def shot(self,projectiles,a=0):
        if self.attackType == 1:
            self.damage = 5
            self.tripleShot(projectiles,a)
        if self.attackType == 2:
            self.damage = 2
            self.rapidFire(projectiles,a)
        else:
            self.damage = 3
            self.singleShot(projectiles,a)
    def rapidFire(self,projectiles,a):
        if self.timeAttack == 0:
            p = projectiles
            shot=Arrow(self.platforms,self.rect.center,self.dir,self.damage,a)
            p.add(shot)
            projectiles = p
            self.rapidArrows-=1
            self.timeAttack = 30
    def singleShot(self,projectiles,a):
        if self.timeAttack == 0:
            p = projectiles
            shot=Arrow(self.platforms,self.rect.center,self.dir,self.damage,a)
            p.add(shot)
            projectiles = p
            self.timeAttack = 200
    def tripleShot(self,projectiles,a):
        if self.timeAttack == 0:
            p = projectiles
            shot=Arrow(self.platforms,self.rect.center,self.dir,self.damage,a)
            p.add(shot)
            shot=Arrow(self.platforms,(self.rect.center[0],self.rect.center[1]-15),self.dir,self.damage,a)
            p.add(shot)
            if DIFFICULTY == 2:
                shot=Arrow(self.platforms,(self.rect.center[0],self.rect.center[1]+15),self.dir,self.damage,a)
                p.add(shot)
            projectiles = p
            self.attackType = 0
            self.timeAttack = 100
    def attack(self,p):
        if self.act < 2:
            self.action=4
            if p.rect[0]>self.hitbox[0]:
                self.dir = 1
            else:
                self.dir = 0
    def animation_mat(self,dt,priority=[3,4],usual=[0,1]):
        #Time dependant
        #Prioridad de animaciones
        if (self.action in priority) and self.act != self.action:
            self.act = self.action
            self.con = 0
            self.vel.x = 0.1
        #Cambiar en cualquier momento de animacion
        if (self.act in usual) and self.act != self.action:
            self.act = self.action
            self.con = 0
        #Direccion
        if self.dir == 1: #derecha
            sprite = self.mR
        else:#izquierda
            sprite = self.mL
        #Cantidad de imagenes de la accion
        images = self.lim[self.act]
        self.currentTime += dt
        if self.currentTime >= self.animationTime:
            self.currentTime = 0
            self.con = (self.con % images)
            index = self.con
            self.checkHitbox()#acomodar el hitbox
            self.image = sprite[self.act][index]
            self.con += 1
            #reset de animacion
            if index == self.lim[self.act]-1:
                if self.act == self.dead: self.kill()
                if self.vel.x != 0: self.action = self.move
                else: self.action=self.idle
                self.act = self.action
                self.con = 0
    def update(self,player,dt,items,projectiles,effects,*args):
        #0=idle
        self.checkNearby()
        if self.act==self.dead and self.con > 15:
            if self.hasKey:
                self.key.kill()
                self.dropKey(items)
                self.hasKey = False
        if self.act in [0,1,3,4]:
            self.animationTime = 0.1
        if self.act == 4:
            if self.attackType == 2:
                self.animationTime = 0.05
            if self.attackType == 1:
                self.animationTime = 0.02
        if self.act == 2:
            self.animationTime = 0.03
        if self.rapidArrows == 0:
            self.attackType = 0
            self.rapidArrows = 5
            self.timeAttack = 100
        if self.action==self.dead and not self.itemDroped:
            r = random.randint(0,5)
            if r == 1:self.spawnItem(items,random.randint(0,4))
            self.itemDroped = True
        if self.act == 4 and self.con >=  9 and self.con < 16:
            self.shot(projectiles)
        self.checkLifespan()
        if not self.onGround:
            self.vel.x = 0
            #only accelerate with gravity if in the air
            self.vel += GRAVITY
            #max falling speed
            if self.vel.y > 50: self.vel.y=50
        elif self.act == 1:
            if self.dir==1:
                self.vel.x = self.speed
            else:
                self.vel.x = -self.speed
        if self.act > 1 or self.act == 0:
            self.vel.x = 0
        # increment in x direction
        self.rect.left += self.vel.x
        self.hitbox.left += self.vel.x
        self.checkPlayer(player)
        self.collidePlayer(player)
        # do x-axis collisions
        self.collideHorizontal()
        # increment in y direction
        self.rect.top += self.vel.y
        self.hitbox.top += self.vel.y
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collideVertical()
        self.updateKey()
        self.animation_mat(dt,[2,3])
        if self.immunity > 0:
            self.immunity -=1
        if self.timeAttack == 0:
            self.attack(player)
        if self.timeAttack > 0:
            self.timeAttack -= 1


        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False
    def checkPlayer(self,p):
        distx=abs(p.rect[0]-self.rect[0])
        disty=abs(p.rect[1]-self.rect[1])
        if (distx+disty)/2 < 100:
            if self.action < 2 and self.attackType == 0:
                self.action = 1
                if p.hitbox.center[0] > self.hitbox.center[0]:
                    self.dir = 0
                else:
                    self.dir = 1
            if self.timeAttack == -1:
                self.timeAttack = 100
        if (distx+disty)/2 > 300:
            self.action = 0
            self.timeAttack = -1
    def collidePlayer(self,p):
        if self.rect.colliderect(p.hitbox) and (self.act < 2 or self.act == 4):
            self.attackType = 1
            self.timeAttack = 20
            self.attack(p)
    def collideHorizontal(self):
        blocks = [0]
        for p in self.nearbyTiles:
            if (p.type in blocks) and self.hitbox.colliderect(p.rect):
                if self.vel.x > 0:
                    self.hitbox.right = p.rect.left
                    self.vel.x = 0
                    self.dir = 0
                    self.attackType = 2
                    self.timeAttack = 0
                if self.vel.x < 0:
                    self.hitbox.left = p.rect.right
                    self.vel.x = 0
                    self.dir = 1
                    self.attackType = 2
                    self.timeAttack = 0
    def collideVertical(self):
        super().collideVertical([0],4)
class SkeletonArcher(SkeletonArcherBase):
    def __init__(self,platforms, pos,type_=1,key_=False,items = None,speed=3, *groups):
        super().__init__(platforms,pos)
        self.hp = 10
        if type_==1:
            asset = SS_ENEMIES["sArcherB"]
        else:
            asset = SS_ENEMIES["sArcherC"]
        self.originalSpeed = speed
        self.speed = self.originalSpeed
        self.type=type_
        self.mR=asset
        self.mL=funciones.spriteFlip(asset)
        self.image=self.mR[self.action][self.con]
        self.rect= self.image.get_rect(midbottom=pos)
        self.hitbox = self.rect.inflate(-40,-20)
        self.hitbox.left = self.rect.left +10
        self.hitbox.bottom = self.rect.bottom -4
        if key_:
            self.createKey(items)

    def shot(self,projectiles):
        if self.attackType == 1:
            self.damage = 5
            self.tripleShot(projectiles)
        if self.attackType == 2:
            self.damage = 2
            self.rapidFire(projectiles)
        else:
            self.damage = 3
            self.singleShot(projectiles)
    def rapidFire(self,projectiles):
        if self.timeAttack == 0:
            p = projectiles
            if self.type == 1:
                shot = ExplosiveArrow(self.platforms,self.rect.center,self.dir,self.damage)
            else:
                shot = FrostArrow(self.platforms,self.rect.center,self.dir,self.damage)
            p.add(shot)
            projectiles = p
            self.rapidArrows-=1
            self.timeAttack = 30
    def singleShot(self,projectiles):
        if self.timeAttack == 0:
            p = projectiles
            if self.type == 1:
                shot = ExplosiveArrow(self.platforms,self.rect.center,self.dir,self.damage)
            else:
                shot = FrostArrow(self.platforms,self.rect.center,self.dir,self.damage)
            p.add(shot)
            projectiles = p
            self.timeAttack = 200
    def tripleShot(self,projectiles):
        if self.timeAttack == 0:
            p = projectiles
            if self.type == 1:
                shot = ExplosiveArrow(self.platforms,self.rect.center,self.dir,self.damage)
                p.add(shot)
            else:
                shot = FrostArrow(self.platforms,self.rect.center,self.dir,self.damage)
                p.add(shot)
            r = random.randint(0,1)
            if r == 1:
                shot = shot=Arrow(self.platforms,(self.rect.center[0],self.rect.center[1]-15),self.dir,self.damage,self.type)
                p.add(shot)
            else:
                shot=Arrow(self.platforms,(self.rect.center[0],self.rect.center[1]+15),self.dir,self.damage,self.type)
                p.add(shot)
            projectiles = p
            self.attackType = 0
            self.timeAttack = 100
    def update(self,player,dt,items,projectiles,effects,*args):
        #0=idle
        self.checkNearby()
        self.checkLifespan()
        if self.fx == None and self.hp == 10:
            self.createFx(effects,self.type)
        if self.hp < 6 and self.fx != None:
            self.fx.loop = False
            self.fx = None
        if self.act==self.dead and self.con > 15:
            if self.fx!= None:
                self.fx.kill()
            if self.hasKey:
                self.key.kill()
                self.dropKey(items)
                self.hasKey = False
        if self.act in [0,1,3,4]:
            self.animationTime = 0.1
        if self.act == 4:
            if self.attackType == 2:
                self.animationTime = 0.05
            if self.attackType == 1:
                self.animationTime = 0.02
        if self.act == 2:
            self.animationTime = 0.03
        if self.rapidArrows == 0:
            self.attackType = 0
            self.rapidArrows = 5
            self.timeAttack = 100
        if self.action==self.dead and not self.itemDroped:
            r = random.randint(0,5)
            if r == 1:self.spawnItem(items,random.randint(0,4))
            self.itemDroped = True
        if self.act == 4 and self.con >=  9 and self.con < 16:
            self.shot(projectiles)
        if not self.onGround:
            self.vel.x = 0
            #only accelerate with gravity if in the air
            self.vel += GRAVITY
            #max falling speed
            if self.vel.y > 50: self.vel.y=50
        elif self.act == 1:
            if self.dir==1:
                self.vel.x = self.speed
            else:
                self.vel.x = -self.speed
        if self.act > 1 or self.act == 0:
            self.vel.x = 0
        # increment in x direction
        self.rect.left += self.vel.x
        self.hitbox.left += self.vel.x
        self.checkPlayer(player)
        self.collidePlayer(player)
        # do x-axis collisions
        self.collideHorizontal()
        # increment in y direction
        self.rect.top += self.vel.y
        self.hitbox.top += self.vel.y
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collideVertical()
        self.updateKey()
        self.animation_mat(dt,[2,3])
        if self.immunity > 0:
            self.immunity -=1
        if self.timeAttack == 0:
            self.attack(player)
        if self.timeAttack > 0:
            self.timeAttack -= 1

        self.updateFx()

        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False
class SkeletonWarriorBase(Enemy):
    def __init__(self,platforms, pos,key_=False,items = None,speed=1.5, *groups):
        super().__init__(platforms,pos)
        self.hp = 5
        self.damage = 4
        asset = SS_ENEMIES["sWarriorA"]
        self.originalSpeed = speed
        self.speed = self.originalSpeed
        self.type=0
        #[sWIdle,SWRun,SWHurt,SWDie,SWAttack,SWBlock]
        self.lim=[8,8,11,21,19,12]
        self.dead=3
        self.action=0
        self.mR=asset
        self.mL=funciones.spriteFlip(asset)
        self.image=self.mR[self.action][self.con]
        self.rect= self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-40,-20)
        self.dir = 1
        self.hitbox.left = self.rect.left + 15
        self.hitbox.bottom = self.rect.bottom -5
        self.pain = pygame.mixer.Sound("SFX/undeadPain.ogg")
        self.refreshNearby()
        if key_:
            self.createKey(items)

    def gotHit(self,hit):
        if self.act == 5 and self.con > 5:
            pass
        else:
            super().gotHit(hit,200,2)

    def createFx(self,effects,t=0):
        if t == 1:
            t = 2
        elif t == 2:
            t = 0
        self.fx = CastEffects(self.hitbox.center,t)
        effects.add(self.fx)
    def updateFx(self):
        if self.fx!=None:
            self.fx.rect.center = self.hitbox.center

    def checkHitbox(self):
        if self.dir==1:
            self.rect.left=self.hitbox.left-15
        else:
            self.rect.right=self.hitbox.right+15

    def animation_mat(self,dt,priority=[3,4],usual=[0,1]):
        #Time dependant
        #Prioridad de animaciones
        if (self.action in priority) and self.act != self.action:
            self.act = self.action
            self.con = 0
            self.vel.x = 0.1
        #Cambiar en cualquier momento de animacion
        if (self.act in usual) and self.act != self.action:
            self.act = self.action
            self.con = 0
        #Direccion
        if self.dir == 1: #derecha
            sprite = self.mR
        else:#izquierda
            sprite = self.mL
        #Cantidad de imagenes de la accion
        images = self.lim[self.act]
        self.currentTime += dt
        if self.currentTime >= self.animationTime:
            self.currentTime = 0
            self.con = (self.con % images)
            index = self.con
            self.checkHitbox()#acomodar el hitbox
            self.image = sprite[self.act][index]
            self.con += 1
            #reset de animacion
            if index == self.lim[self.act]-1:
                if self.act == self.dead: self.kill()
                if self.act == 4: self.timeAttack = 100
                if self.vel.x != 0: self.action = self.move
                else: self.action=self.idle
                self.act = self.action
                self.con = 0

    def update(self,player,dt,items,*args):
        #0=idle
        self.checkNearby()
        if self.act==self.dead and self.con > 15:
            if self.hasKey:
                self.key.kill()
                self.dropKey(items)
                self.hasKey = False
            if not self.itemDroped:
                self.dropWeapon(items,0)
                self.itemDroped = True
        self.checkLifespan()
        if not self.onGround:
            self.vel.x = 0
            #only accelerate with gravity if in the air
            self.vel += GRAVITY
            #max falling speed
            if self.vel.y > 50: self.vel.y=50
        elif self.act == 1:
            if self.dir==1:
                self.vel.x = self.speed
            else:
                self.vel.x = -self.speed
        if self.act > 1:
            self.vel.x = 0
        # increment in x direction
        self.rect.left += self.vel.x
        self.hitbox.left += self.vel.x
        self.collidePlayer(player)
        # do x-axis collisions
        self.collideHorizontal()
        # increment in y direction
        self.rect.top += self.vel.y
        self.hitbox.top += self.vel.y

        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collideVertical()
        self.updateKey()
        if self.action == 0:
            self.action = 1
            super().move()
        self.animation_mat(dt,[2,3])
        if self.immunity > 0:
            self.immunity -=1

        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False

    def collidePlayer(self,p):
        playerIsRight = p.hitbox.center[0] > self.hitbox.center[0]
        if self.rect.colliderect(p.hitbox):
            if self.act == 4 and self.con > 9 and self.con < 13:
                if playerIsRight  and self.dir == 1:
                    p.gotHit(self.damage)
                elif not playerIsRight and self.dir == 0:
                    p.gotHit(self.damage)
        if self.hitbox.colliderect(p.hitbox):
            if self.act < 2:
                if playerIsRight:
                    self.dir = 1
                else:
                    self.dir = 0
                self.action = 4

    def collideHorizontal(self,blocks=[0],changeDir = True):

        for p in self.nearbyTiles:
            if (p.type in blocks) and self.hitbox.colliderect(p.rect):
                if self.vel.x > 0:
                    self.hitbox.right = p.rect.left
                    self.vel.x = 0
                    if changeDir:self.dir = 0
                if self.vel.x < 0:
                    self.hitbox.left = p.rect.right
                    self.vel.x = 0
                    if changeDir:self.dir = 1
    def collideVertical(self):
        super().collideVertical([0],5)
class SkeletonWarrior(SkeletonWarriorBase):
    def __init__(self,platforms, pos,type_=2,key_=False,items = None,speed=1.5, *groups):
        super().__init__(platforms,pos)
        if type_==1:
            asset = SS_ENEMIES["sWarriorB"]
            self.damage = 6
            self.hp = 10
        else:
            asset = SS_ENEMIES["sWarriorC"]
            self.hp = 14
            self.damage = 4
        self.maxHp = self.hp
        self.originalSpeed = speed
        self.speed = self.originalSpeed
        self.type=type_
        self.mR=asset
        self.mL=funciones.spriteFlip(asset)
        self.image=self.mR[self.action][self.con]
        self.rect= self.image.get_rect(midbottom=pos)
        self.hitbox = self.rect.inflate(-40,-20)
        self.hitbox.left = self.rect.left + 15
        self.hitbox.bottom = self.rect.bottom -5
        self.playeronSight = False
        self.timeAttack = 100
        if key_:
            self.createKey(items)
    def update(self,player,dt,items,projectiles,effects,*args):
        #0=idle
        if self.hp<=0:
            self.action=self.dead
            self.vel.x=0
        self.checkNearby()
        self.checkLifespan()
        if self.lifespan > 0:
            self.itemDroped = True
        if self.fx == None and self.hp == self.maxHp:
            self.createFx(effects,self.type)
        if self.hp < 6 and self.fx != None:
            self.fx.loop = False
            self.fx = None
        #Prioridad de actiones
        if (self.action in [2,3]) and self.act != self.action:
            self.act = self.action
            self.con = 0
        if self.act==self.dead and self.con > 15:
            if self.fx!= None:
                self.fx.kill()
            if self.hasKey:
                self.key.kill()
                self.dropKey(items)
                self.hasKey = False
            if not self.itemDroped:
                self.dropWeapon(items,0)
                self.itemDroped = True
        if not self.onGround:
            self.vel.x = 0
            #only accelerate with gravity if in the air
            self.vel += GRAVITY
            #max falling speed
            if self.vel.y > 50: self.vel.y=50
        elif self.act == 1:
            if self.dir==1:
                self.vel.x = self.speed
            else:
                self.vel.x = -self.speed
        if self.act > 1 or self.act == 0:
            self.vel.x = 0
        # increment in x direction
        self.rect.left += self.vel.x
        self.hitbox.left += self.vel.x
        # do x-axis collisions
        self.collideHorizontal()
        # increment in y direction
        self.rect.top += self.vel.y
        self.hitbox.top += self.vel.y
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collideVertical()
        self.updateKey()
        self.checkClose(player,projectiles)
        self.collidePlayer(player)
        if self.hp < 5:
            self.checkArrows(projectiles)
        self.animationTime = 0.1
        if self.act >= 4:
            self.animationTime = 0.035
        self.animation_mat(dt,[2,3])
        if self.immunity > 0:
            self.immunity -=1
        if self.timeAttack > 0:
            self.timeAttack -= 1

        self.updateFx()
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False
    def checkArrows(self,projectiles):
        for a in projectiles:
            dy=abs(a.hitbox[1]-self.hitbox[1])
            dx = self.hitbox[0]-a.hitbox[0]
            if dy < 100:
                if dx < 0 and dx > -200 and self.dir == 1:
                    self.action = 5
                    if self.act == 5 and self.con > 10:
                        self.con = 10
                elif dx > 0 and dx < 200 and self.dir == 0:
                    self.action = 5
                    if self.act == 5 and self.con > 10:
                        self.con = 10
    def checkClose(self,p,projectiles):
        pright = self.hitbox.center[0] < p.hitbox.center[0]
        dx=abs(p.hitbox.center[0]-self.hitbox.center[0])
        dy=abs(p.hitbox.center[1]-self.hitbox.center[1])
        dist = (dx+dy)/2
        pbow= False
        arrow = False
        for a in projectiles:
            if self.hitbox.colliderect(a.hitbox):
                arrow = True
        if dy > 100:
            self.action = 0
        else:
            if dx < 400 and dx > 150:
                self.action = 1
                self.playeronSight = False
            if dx <= 150:
                self.playeronSight=True
                self.action = 1
                if pright:
                    self.dir = 1
                else: self.dir = 0
                if not p.onGround:
                    self.action = 5
                    if self.act == 5 and self.con > 10:
                        self.con = 10

    def collidePlayer(self,p):
        pright = self.hitbox.center[0] < p.hitbox.center[0]
        pup = self.hitbox.center[1] < p.hitbox.center[1]
        if self.hitbox.colliderect(p.hitbox):
            if pright:
                self.dir = 1
            else: self.dir = 0
        if self.rect.colliderect(p.hitbox):
            if pright and self.dir == 1:
                if self.timeAttack > 0:
                    self.action = 5
                else:
                    self.action = 4
            elif not pright and self.dir == 0:
                if self.timeAttack > 0:
                    self.action = 5
                else:
                    self.action = 4
            if self.act == 5 and self.con > 10:
                self.con = 10
            if self.act == 4 and self.con > 7 and self.con< 12:
                if pright and self.dir == 1:
                    p.gotHit(self.damage)
                elif not pright and self.dir == 0:
                    p.gotHit(self.damage)
                if pup and self.con < 10:
                    p.gotHit(self.damage)

    def collideHorizontal(self):
        if self.playeronSight:
            super().collideHorizontal([0],False)
            self.checkHitbox()
        else:
            super().collideHorizontal([0],True)
class Knight(Enemy):
    def __init__(self,platforms, pos,speed=2, *groups):
        super().__init__(platforms,pos)
        asset = SS_ENEMIES["knight"]
        self.speed = speed
        self.hp = 10
        self.maxHP = self.hp
        self.damage = 4
        #[kIdle,kRun,kRoll,kJump,kAttack,kShield,kDeath]
        self.lim=[15,8,10,9,22,7,15]
        self.dead=6
        self.chunkSize=(WIN_WIDTH,WIN_HEIGHT)
        self.action=1
        self.jump_strength = 4
        self.shield = False
        self.shieldTime= 0
        self.selfCD = 0
        self.dodge =  False
        self.mR=asset
        self.mL=funciones.spriteFlip(asset)
        self.image=self.mR[self.action][self.con]
        self.rect= self.image.get_rect(center=pos)
        self.hitbox = Rect(0,0,32,36)
        self.hitbox.center = self.rect.center
        self.pain = pygame.mixer.Sound("SFX/knightPain.ogg")
        self.refreshNearby()
        self.hasKey = False

    def gotHit(self,hit):
        if not self.dodge and not self.shield and self.immunity <= 50:
            self.pain.play()
            self.hp -= hit
            self.immunity = 120
            print("ow")
            self.selfCD = 1

    def checkHitbox(self):
        self.rect.width = self.image.get_rect().width
        self.rect.center = self.hitbox.center
        if self.act == 4:
            if self.dir == 1:
                self.rect.left = self.hitbox.left-9
            else:
                self.rect.right = self.hitbox.right+9
        if self.act == 5:
            if self.dir == 1:
                self.rect.left = self.hitbox.left-8
            else:
                self.rect.right = self.hitbox.right+8

    def animation_mat(self,dt,priority=[2,5,6],usual=[0,1]):
        #Time dependant
        #Prioridad de animaciones
        if self.act in priority:
            self.action = self.act
        #Cambiar en cualquier momento de animacion
        if (self.act in usual) and self.act != self.action:
            self.act = self.action
            self.con = 0
            if self.act == 4:
                self.con = 3

        #Direccion
        if self.dir == 1: #derecha
            sprite = self.mR
        else:#izquierda
            sprite = self.mL
        #Cantidad de imagenes de la accion
        images = self.lim[self.act]
        self.currentTime += dt
        if self.currentTime >= self.animationTime:
            self.currentTime = 0
            self.con = (self.con % images)
            index = self.con
            self.image = sprite[self.act][index]
            if self.act == 4 and index > 12 and index < 17:
                if self.dir == 1:
                    self.vel.x = 1
                else:
                    self.vel.x = -1
            self.checkHitbox()
            self.con += 1
            #reset de animacion
            if index == self.lim[self.act]-1:
                if self.act == self.dead: self.kill()
                self.action = self.idle
                self.act=self.action
                self.con = 0

    def update(self,player,dt,items,projectiles,*args):
        #0=idle
        if not self.hasKey and self.hp == self.maxHP:
            self.createKey(items)
        if self.hp<=0:
            self.action=self.dead
            self.vel.x=0
        if self.act==self.dead and self.con > 0:
            if self.hasKey:
                self.key.kill()
                self.dropKey(items)
                self.hasKey = False
        self.checkNearby()
        if self.act == 4 and self.con == 21:
            self.selfCD = 100
        #velocidad de animaciones
        if self.act in [0,1,4,6]:
            self.animationTime = 0.1
        if self.act in [2,3,5]:
            self.animationTime = 0.05
        #Escudo y dodge
        self.dodge = False
        if self.act == 2:
            self.dodge = True
        if self.shield:
            self.action = 5
            if self.act == 5 and self.con > 3:
                self.con = 4
        #Prioridad de actiones
        if (self.action in [2,5,6]) and self.act != self.action:
            self.act = self.action
            self.con = 0
        #movimiento en Y
        if self.onGround and self.act == 3 and self.con < 3:
            self.vel.y = -self.jump_strength
        if not self.onGround:
            #only accelerate with gravity if in the air
            self.vel += GRAVITY
            if self.act == 3:
                if self.con > 7:self.con = 7
            #max falling speed
            if self.vel.y > 50: self.vel.y=50
        #movimiento en X
        if self.act == 1 or self.act == 2:
            if self.dir==1:
                self.vel.x = self.speed
            else:
                self.vel.x = -self.speed
            if self.act == 2: self.vel.x *= 2
        if self.act in [0,4,5,6]:
            if self.con <= 5:
                self.vel.x = 0
            if self.act == 4 and self.con >=17:
                self.vel.x = 0
        # increment in x direction
        self.rect.left += self.vel.x
        self.hitbox.left += self.vel.x
        self.collideHorizontal()
        # increment in y direction
        self.rect.top += self.vel.y
        self.hitbox.top += self.vel.y
        # assuming we're in the air
        self.onGround = False;
        self.collideVertical()
        if self.selfCD == 0:
            self.checkPlayer(player)
            self.collidePlayer(player)#colision con jugador
            self.checkArrows(projectiles)
        else:self.action = 0
        self.updateKey()
        self.animation_mat(dt)#animacion
        #timers
        if self.immunity > 0:
            self.immunity -=1
        if self.shieldTime > 0:
            self.shieldTime -= 1
            if self.shieldTime == 0:
                self.shield = False
        if self.selfCD > 0:
            self.selfCD -= 1

        #checkear camara
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False
    def checkArrows(self,projectiles):
        for a in projectiles:
            dy=abs(a.hitbox[1]-self.hitbox[1])
            dx = self.hitbox[0]-a.hitbox[0]
            if dx < 0 and dx > -100 and self.dir == 1:
                self.shield= True
                self.shieldTime = 50
            elif dx > 0 and dx < 100 and self.dir == 0:
                self.shield= True
                self.shieldTime =50

    def collidePlayer(self,p):
        if self.rect.colliderect(p.hitbox):
            dx=abs(p.hitbox[0]-self.hitbox[0])
            pright = self.hitbox[0] < p.hitbox[0]
            if pright and self.dir == 1 and not self.shield:
                self.action = 4
                if self.act == 4:
                    if self.con in [5,6,10,11] and dx <=40:
                        p.gotHit(self.damage)
                    if (self.con == 17 or self.con == 18) and dx <= 55:
                        p.gotHit(self.damage,2,self.hitbox)
            elif not pright and self.dir == 0 and not self.shield:
                self.action = 4
                if self.act == 4:
                    if self.con in [5,6,10,11] and dx <=40:
                        p.gotHit(self.damage)
                    if (self.con == 17 or self.con == 18) and dx <= 55:
                        p.gotHit(self.damage,2,self.hitbox)
            else:
                if self.act != 4:
                    self.action = 2
        else:
            if self.act == 4:
                if not self.con in [5,6] and self.con < 10:
                    self.act = 1
                    self.con = 0

    def checkPlayer(self,p):
        dx=abs(p.hitbox[0]-self.hitbox[0])
        dy=abs(p.hitbox[1]-self.hitbox[1])
        dist = (dx+dy)/2
        if dist > 150:
            self.action = 0
        else:
            if self.act != 2:
                if p.hitbox[0]<self.hitbox[0]:
                    self.dir = 0
                else:
                    self.dir = 1
                self.action = 1
            if not p.onGround and self.act != 4:
                if dist < 35:
                    self.shield = True
                    self.shieldTime =50
                else:
                    if not self.shield:
                        self.action = 2
                        if p.hitbox[0]<self.hitbox[0]:
                            self.dir = 1
                        else:
                            self.dir = 0

    def collideHorizontal(self):
        super().collideHorizontal([0])
    def collideVertical(self):
        super().collideVertical([0])
class Berserker(Enemy):
    def __init__(self,platforms, pos,speed=2, *groups):
        super().__init__(platforms,pos)
        asset = SS_ENEMIES["berserker"]
        self.speed = speed
        self.hp = 3
        self.lim=[16,8,8,18,30,30,25,40,40]
        self.dead=6
        self.action=0
        self.mR=asset
        self.mL=funciones.spriteFlip(asset)
        self.image=self.mR[self.action][self.con]
        self.rect= self.image.get_rect(center=pos)
        self.hitbox = self.rect
        self.pain = pygame.mixer.Sound("SFX/snakePain.ogg")
        self.refreshNearby()

    def gotHit(self,hit):
        super().gotHit(hit,180,3)

    def animation(self):
        super().animation(0.2)

    def update(self,player,dt,items,*args):
        #0=idle
        self.checkNearby()
        if self.action==self.dead and not self.itemDroped:
            r = random.randint(0,5)
            if r == 1:self.spawnItem(items,random.randint(0,4))
            self.itemDroped = True
        self.checkLifespan()
        if not self.onGround:
            self.vel.x = 0
            #only accelerate with gravity if in the air
            self.vel.y += 0.3
            #max falling speed
            if self.vel.y > 50: self.vel.y=50
        elif self.act == 1:
            if self.dir==1:
                self.vel.x = self.speed
            else:
                self.vel.x = -self.speed
            if self.immunity > 0 or self.timeAttack > 0:
                self.vel.x *= 2
        # increment in x direction
        self.rect.left += self.vel.x
        #self.collidePlayer(player)
        self.hitbox.center = self.rect.center
        self.hitbox.bottom = self.rect.bottom
        # do x-axis collisions
        self.collideHorizontal()
        # increment in y direction
        self.rect.top += self.vel.y
        self.hitbox.bottom = self.rect.bottom
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collideVertical()
        self.animation()
        if self.immunity > 0:
            self.immunity -=1
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False

    def collidePlayer(self,p):
        if self.hitbox.colliderect(p.hitbox) and self.immunity == 0:
            print(true)

    def collideHorizontal(self):
        super().collideHorizontal([0])
    def collideVertical(self):
        super().collideVertical([0])
class Minotaur(Enemy):
    def __init__(self,platforms, pos,key_=False,items = None,speed=2, *groups):
        super().__init__(platforms,pos)
        asset = SS_ENEMIES["minotaur"]
        self.speed = speed
        self.hp = 10
        self.damage = 4
        #0=Idle,1=run,2=Attack1,3=attack2,4=hurt,5=dead,6=jump
        self.lim=[0,5,11,21,30,34,42,48]
        self.idle = 0
        self.action = self.idle
        self.dead=5
        self.attack = 2
        self.dir = 0
        self.playeronSight = False
        self.mL=asset
        self.mR=funciones.spriteFlip(asset)
        self.image=self.mR[self.con]
        self.pain = pygame.mixer.Sound("SFX/minoPain.ogg")
        self.rect= self.image.get_rect(center=pos)
        self.hitbox = Rect(0,0,60,70)
        self.hitbox.right = self.rect.right-15
        self.hitbox.bottom = self.rect.bottom
        self.refreshNearby()
        if key_:
            self.createKey(items)

    def gotHit(self,hit):
        self.timeAttack = 500
        super().gotHit(hit,100,4)

    def checkHitbox(self):
        if self.dir==1:
            self.rect.left=self.hitbox.left-15
        else:
            self.rect.right=self.hitbox.right+15
    def animation_list(self,dt,priority=[4,5],usual=[0,1]):
        #Time dependant
        if self.dir == 1: #derecha
            sprite = self.mR
        else:#izquierda
            sprite = self.mL
        #Prioridad de animaciones
        if (self.action in priority) and self.act != self.action:
            self.act = self.action
            self.con = 0
        #Cambiar en cualquier momento de animacion
        if (self.act in usual) and self.act != self.action:
            self.act = self.action
            self.con = 0
        #Cantidad de imagenes de la accion
        images =self.lim[self.act+1] - self.lim[self.act]
        self.currentTime += dt
        if self.currentTime >= self.animationTime:
            self.currentTime = 0
            self.con = ((self.con) % images)
            index = self.con + self.lim[self.act]
            self.checkHitbox()
            self.image = sprite[index]
            self.con += 1
            #reset de animacion
            if index == self.lim[self.act+1]-1:
                if self.act == self.dead: self.kill()
                if self.vel.x != 0: self.action = self.move
                else: self.action=self.idle
                self.act = self.action
                self.con = 0

    def update(self,player,dt,items,projectiles,*args):
        #0=idle
        self.checkNearby()
        if (self.action in [4,5]) and self.act != self.action:
            self.act = self.action
            self.con = 0
        if self.act==self.dead and self.con > 5:
            if self.hasKey:
                self.key.kill()
                self.dropKey(items)
                self.hasKey = False
        if not self.onGround:
            #only accelerate with gravity if in the air
            self.vel += GRAVITY
            #max falling speed
            if self.vel.y > 50: self.vel.y=50
        elif self.act == 1:
            if self.dir==1:
                self.vel.x = self.speed
            else:
                self.vel.x = -self.speed
        if self.act in [0,2,3,4,5]:
            self.vel.x = 0
        # increment in x direction
        self.rect.left += self.vel.x
        self.hitbox.left += self.vel.x
        # do x-axis collisions
        self.collideHorizontal()
        # increment in y direction
        self.rect.top += self.vel.y
        self.hitbox.top += self.vel.y
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collideVertical()
        self.updateKey()
        self.checkClose(player,projectiles)
        self.collidePlayer(player)
        self.checkArrows(projectiles)
        self.animationTime = 0.1
        if self.act == 2:
            self.animationTime = 0.05
        self.animation_list(dt)
        if self.immunity > 0:
            self.immunity -=1
        if self.timeAttack > 0:
            self.attack = 3
            self.timeAttack -= 1
            if self.timeAttack == 0:
                self.attack = 2
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False
    def checkArrows(self,projectiles):
        for a in projectiles:
            dy=abs(a.hitbox[1]-self.hitbox[1])
            dx = self.hitbox[0]-a.hitbox[0]
            if dy < 100:
                if dx < 0 and dx > -200 and self.dir == 1:
                    self.action = 2
                elif dx > 0 and dx < 200 and self.dir == 0:
                    self.action = 2
                if self.rect.colliderect(a.hitbox):
                    if self.act == 2 and self.con > 4:
                        a.gotHit()
                    if self.act == 3 and self.con > 4:
                        a.gotHit()
    def checkClose(self,p,projectiles):
        pright = self.hitbox.center[0] < p.hitbox.center[0]
        dx=abs(p.hitbox.center[0]-self.hitbox.center[0])
        dy=abs(p.hitbox.center[1]-self.hitbox.center[1])
        dist = (dx+dy)/2
        pbow= False
        arrow = False
        for a in projectiles:
            if self.hitbox.colliderect(a.hitbox):
                arrow = True
        if dy > 100:
            self.action = 0
        else:
            if dx < 400 and dx > 150:
                self.action = 1
                self.playeronSight = False
            if dx <= 150:
                self.playeronSight=True
                self.action = 1
                if pright:
                    self.dir = 1
                else: self.dir = 0
                if p.assets == 2:
                    pbow = True
                if not p.onGround:
                    self.action = self.attack
                    if self.con in [3,4] and not self.rect.colliderect(p.rect) and not pbow and not arrow:
                        if self.con == 4:
                            self.con = 3
                else:
                    if pbow:
                        self.action = 2



    def collidePlayer(self,p):
        pright = self.hitbox.center[0] < p.hitbox.center[0]
        pup = self.hitbox.center[1] < p.hitbox.center[1]
        if self.hitbox.colliderect(p.hitbox):
            if pright:
                self.dir = 1
            else: self.dir = 0
        if self.rect.colliderect(p.hitbox):
            self.action = self.attack
            if self.act == 2 and self.con in [5,6]:
                if pright and self.dir == 1:
                    p.gotHit(self.damage)
                elif not pright and self.dir == 0:
                    p.gotHit(self.damage)
                if pup:
                    p.gotHit(self.damage)
            if self.act == 3 and self.con in [5,6,7]:
                p.gotHit(self.damage+2,2,self.hitbox)


    def collideHorizontal(self):
        if self.playeronSight:
            super().collideHorizontal([0],False)
            self.checkHitbox()
        else:
            super().collideHorizontal([0],True)
    def collideVertical(self):
        super().collideVertical([0])
class GranImp(Enemy):
    def __init__(self,platforms, pos,action=1,speed=2, *groups):
        super().__init__(platforms,pos)
        asset = SS_ENEMIES["granimp"]
        self.speed = (speed,speed)
        self.hp = 3
        #0=Idle,1=Walk,2=Attack,3=Hurt,4=Dead
        self.lim=[0,5,10,21,24,33,44]
        self.action = action
        self.act = self.action
        self.dead=4
        self.flee = False
        self.timeDir= 0
        self.mL=asset
        self.mR=funciones.spriteFlip(asset)
        self.image=self.mR[self.con+self.lim[self.action]]
        self.pain = pygame.mixer.Sound("SFX/impPain.ogg")
        self.rect= self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-10,-20)
        self.hitbox.center = self.rect.center
        self.chunkSize=(WIN_WIDTH,WIN_HEIGHT)
        self.refreshNearby()

    def gotHit(self,hit):
        super().gotHit(hit,120,3)
    def Fanimation(self,*args):
        #Frame dependant
        if self.dir == 1: #derecha
            sprite = self.mR
        else:#izquierda
            sprite = self.mL
        #Prioridad de animaciones
        if (self.action>=3) and self.act != self.action:
            self.act = self.action
            self.con = 0
        #Cambiar en cualquier momento de animacion
        if self.act <= 1 and self.act != self.action:
            self.act = self.action
            self.con = 0
        #Cantidad de imagenes de la accion
        images =self.lim[self.act+1] - self.lim[self.act]
        self.currentFrame += 1
        if self.currentFrame >= self.animationFrames:
            self.currentFrame = 0
            self.con = ((self.con + 1) % images)
            index = self.con + self.lim[self.act]
            self.image = sprite[index]
            #reset de animacion
            if index == self.lim[self.act+1]-1:
                if self.act == self.dead: self.kill()
                if self.vel.x != 0: self.action = self.move
                else: self.action=self.idle
                self.act = self.action
                self.con = 0
    def attack(self,projectiles):
        if self.timeAttack == 0:
            p = projectiles
            shot=GranImpShot(self.platforms,self.rect.center,self.dir,3)
            p.add(shot)
            projectiles = p
            self.timeAttack = 200
    def update(self,player,dt,items,projectiles,*args):
        #0=idle
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        self.checkNearby()
        if self.action==self.dead and self.onGround and not self.itemDroped:
            self.spawnItem(items,random.randint(0,4))
            self.itemDroped = True
        if self.act == 2 and self.con == 5:
            self.attack(projectiles)
        self.checkLifespan()
        if not self.onGround:
            self.vel.x = 0
            if self.act == self.dead or self.act == 5:
                self.vel += GRAVITY
        if self.act == 1:
            if self.dir==1:
                self.vel.x = self.speed[0]
            else:
                self.vel.x = -self.speed[0]

        self.flee = False
        if self.immunity > 30:
            self.flee = True
        if self.act < 2 and ((disty+distx)/2) < 200:
            self.checkPlayer(player)
        if self.immunity > 80 and self.act < 3:
            self.vel.y = -self.speed[1]
        if self.timeAttack > 150 and self.act < 3:
            self.vel.y = -self.speed[1]
        if player.rect[1]-self.rect[1] > 100 and self.vel.y < 0:
            self.vel.y = 0
        if player.rect[1]-self.rect[1] < -100 and self.vel.y > 0:
            self.vel.y = 0
        if self.act==2:
            self.vel.y = 0
        # increment in x direction
        self.rect.left += self.vel.x
        self.hitbox.left += self.vel.x
        # do x-axis collisions
        self.collideHorizontal()
        # increment in y direction
        self.rect.top += self.vel.y
        self.hitbox.top += self.vel.y
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collideVertical()
        self.animation_list(dt)
        if self.immunity > 0:
            self.immunity -=1
        if self.timeDir > 0:
            self.timeDir -= 1
        if self.timeAttack > 0:
            self.timeAttack -=1
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False
    def checkPlayer(self,p):
        distx=abs(p.rect[0]-self.rect[0])
        disty=abs(p.rect[1]-self.rect[1])
        if not self.flee and distx < 80:
            self.flee = True
        if p.rect[0] > self.hitbox[0]:
            if not self.flee and self.timeDir == 0 and distx > 150:
                self.dir = 1
                self.timeDir = 30
            if self.flee:
                self.dir = 0
        else:
            if not self.flee and self.timeDir == 0 and distx > 150:
                self.dir = 0
                self.timeDir = 30
            if self.flee:
                self.dir = 1

        super().move(self.speed[0])
        if self.timeAttack <= 5 and not self.flee:
            if p.rect.center[1] < self.hitbox.center[1]:
                self.vel.y = -self.speed[1]
            else:
                self.vel.y = self.speed[1]
        if disty < 10 and self.timeAttack == 0:
            if p.rect[0] < self.rect[0]:
                self.dir = 0
            else:
                self.dir = 1
            self.action = 2
    def collideHorizontal(self):
        blocks = [0]
        for p in self.nearbyTiles:
            if (p.type in blocks) and self.rect.colliderect(p.rect):
                if self.vel.x > 0:
                    self.rect.right = p.rect.left
                    self.vel.x = 0
                if self.vel.x < 0:
                    self.rect.left = p.rect.right
                    self.vel.x = 0
                self.hitbox.center = self.rect.center
    def collideVertical(self):
        blocks = [0]
        for p in self.nearbyTiles:
            if (p.type in blocks) and self.rect.colliderect(p.rect):
                if self.vel.y < 0:
                    self.vel.y=0
                    self.rect.top = p.rect.bottom
                if self.vel.y > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                self.hitbox.center=self.rect.center
class Necromancer(Spawner,Enemy):
    def __init__(self,platforms, pos,key_=False,items = None,speed=1, *groups):
        super().__init__(platforms,pos,0)
        asset = SS_ENEMIES["necromancer"]
        self.speed = speed
        self.hp = 20
        self.maxHP = self.hp
        self.damage = 2
        self.speed = speed
        #0=Idle,1=Walk,2=Attack,3=Hurt,4=Dead
        self.lim=[0,4,10,16,22,25,35]
        self.idle = 0
        self.action = self.idle
        self.dead=5
        self.mL=asset
        self.mR=funciones.spriteFlip(asset)
        self.image=self.mR[self.con]
        self.pain = pygame.mixer.Sound("SFX/undeadPain.ogg")
        self.rect= self.image.get_rect(center=pos)
        self.hitbox = self.rect
        self.chunkSize=(WIN_WIDTH,WIN_HEIGHT)
        self.refreshNearby()
        self.hasKey = False
        self.tPoints = []
        self.checkPoints()
        self.lastPoint = self.rect.center
        self.currentPoint = self.rect.center
        self.tp = False
        self.summonTime = 100
        self.tpCD = 0
        self.shotCD=0

    def checkPoints(self):
        for e in self.platforms:
            if e.type == 6:
                self.tPoints += [e.rect.center]

    def teleport(self,e ):
        r = random.choice(self.tPoints)
        while(r== self.currentPoint):
            r = random.choice(self.tPoints)
        self.createFx(self.rect.midbottom,e)
        self.rect.midbottom = r
        self.createFx(r,e)
        self.lastPoint = self.rect.midbottom
        self.currentPoint = r
        self.tp = False
        self.tpCD = 500

    def summon(self,effects,enemies,player):
        r = random.choice(self.tPoints)
        q = random.choice(self.tPoints)
        t = random.randint(1,2)
        while(q== r):
            q = random.choice(self.tPoints)
        if self.hp < 15:
            self.createFx(q,effects)
            mob = SkeletonArcher(self.platforms, q,1)
            mob.lifespan = 1000
            mob.hp = 9
            enemies.add(mob)
        if self.hp < 10:
            self.createFx(r,effects)
            mob = SkeletonArcher(self.platforms, r,2)
            mob.lifespan = 1000
            mob.hp = 9
            enemies.add(mob)
        self.createFx(player.rect.midbottom,effects)
        mob = SkeletonWarrior(self.platforms,self.rect.midbottom,t)
        mob.lifespan = 1000
        mob.maxHp += 1
        enemies.add(mob)
        mob = GranImp(self.platforms,player.rect.center)
        mob.lifespan = 1000
        enemies.add(mob)
        if self.tpCD == 0:
            self.tp = True
        self.summonTime = 1500

    def gotHit(self,hit):
        if self.immunity <= 50:
            self.pain.play()
            self.hp -= hit
            self.immunity = 180
            self.action = 4
            self.vel.x = 0
            if self.hp<=0:
                self.action = 5
            else:
                self.tp = True
    def createFx(self,pos,effects,t=0):
        if t ==0:
            pos = (pos[0],pos[1]-40)
            self.fx = CastEffects(pos,4)
            effects.add(self.fx)

    def updateFx(self):
        if self.fx!=None:
            self.fx.rect.center = self.hitbox.center

    def checkHitbox(self):
        if self.dir==1:
            self.rect.left=self.hitbox.left-15
        else:
            self.rect.right=self.hitbox.right+15

    def update(self,player,dt,items,projectiles,effects,mobs,*args):
        #0=idle
        if not self.hasKey and self.hp == self.maxHP:
            self.createKey(items)
        if self.act==self.dead and self.con > 4:
            if self.hasKey:
                self.key.kill()
                self.dropKey(items)
                self.hasKey = False
        if self.hp <= 0:
            self.action = self.dead
        if self.action == 3 and self.act != 4 and self.act != 5:
            self.act = 3
        if self.tp and self.action != 4:
            self.action = 3
        if self.tp and self.act == 3 and self.con > 3:
            self.teleport(effects)
        if self.act == 2 and self.con == 4 and self.shotCD == 0:
            shot = GranImpShot(self.platforms,self.rect.center,self.dir,self.damage)
            projectiles.add(shot)
            self.shotCD = 200
        if self.summonTime == 0 and self.act == 3 and self.con > 2:
            self.summon(effects,mobs,player)
        self.checkNearby()
        self.checkLifespan()
        if (self.action in [4,5]) and self.act != self.action:
            self.act = self.action
            self.con = 0
        if not self.onGround:
            #only accelerate with gravity if in the air
            self.vel += GRAVITY
            #max falling speed
            if self.vel.y > 50: self.vel.y=50
        elif self.act == 1:
            if self.dir==1:
                self.vel.x = self.speed
            else:
                self.vel.x = -self.speed
        if self.act > 1 or self.act == 0:
            self.vel.x = 0
        # increment in x direction
        self.rect.left += self.vel.x
        self.hitbox.left += self.vel.x
        self.collidePlayer(player)
        # do x-axis collisions
        self.collideHorizontal()
        # increment in y direction
        self.rect.top += self.vel.y
        self.hitbox.top += self.vel.y
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collideVertical()
        self.checkClose(player,projectiles)
        self.updateKey()
        self.animationTime = 0.1
        if self.act == 3:
            self.animationTime = 0.1
        self.animation_list(dt,[4,5])
        if self.immunity > 0:
            self.immunity -=1
        if self.tpCD > 0:
            self.tpCD -= 1
        if self.shotCD > 0:
            self.shotCD-=1
        if self.summonTime > 0:
            self.summonTime -= 1
            if self.summonTime == 0:
                self.action = 3

        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False

    def checkClose(self,p,projectiles):
        pright = self.hitbox.center[0] < p.hitbox.center[0]
        dx=abs(p.hitbox.center[0]-self.hitbox.center[0])
        dy=abs(p.hitbox.center[1]-self.hitbox.center[1])
        dist = (dx+dy)/2
        if dy > 100:
            self.action = 0
        else:
            if dx < 400 and dx > 150:
                self.playeronSight = False
            if dx <= 150:
                self.playeronSight=True
                if pright:
                    self.dir = 1
                else: self.dir = 0
                if self.shotCD == 0:
                    self.action = 2


    def collidePlayer(self,p):
        pass

    def collideHorizontal(self):
        super().collideHorizontal([0])
    def collideVertical(self):
        super().collideVertical([0])
"""PLAYER"""
class Player(Sprite):
    """Clase del jugador"""
    def __init__(self, platforms,obstacles, pos,level, *groups):
        """Setup del jugador"""
        super().__init__(platforms)
        sprites = [SS_ALLIES["pUnarmed"],SS_ALLIES["pSword"],SS_ALLIES["pBow"]]
        #player config
        self.speed = 4
        self.animationTime = 0.08
        self.jump_strength = 5.3
        self.originalJumpS = self.jump_strength
        self.damage = [1,3,2]
        # Life Meter
        self.lifetotal = ["", "l", "ll", "lll", "llll", "lllll", "llllll", "lllllll", "llllllll", "lllllllll"]
        self.hp = 18
        self.maxHp = self.hp
        #player sprites setup
        self.lim=[
        [0,4,8,13,18,24,28,30,32,39,46,52,58,64,70,74,78,84,92,94,96,99,102,109,115],
        [0,4,8,14,22,24,26,29,33,38,42,48,53,59,62,69,73,77,79,81,85,90,93,97,100,106,112,118],
        [0,9,15]
        ]

        self.idle = 14
        self.action = self.idle
        mUnarmedL = funciones.spriteFlip(sprites[0])
        mSwordL = funciones.spriteFlip(sprites[1])
        mBowL = funciones.spriteFlip(sprites[2])
        self.spritesR = sprites
        self.spritesL = [mUnarmedL,mSwordL,mBowL]
        self.image=self.spritesR[0][self.action]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = Rect(0,0,26,30)
        self.hitbox.center = self.rect.center
        self.top = Rect(0,0,32,2)
        self.top.midbottom = (self.hitbox.center[0],self.hitbox.top-4)
        self.head = Rect(0,0,32,2)
        self.head.midtop = (self.hitbox.center[0],self.hitbox.top)
        #player rendering tiles
        self.chunkSize=(WIN_WIDTH*3,WIN_HEIGHT)
        self.startPos=(-2000,-2000)
        self.obstacles = obstacles
        self.mobs = []
        self.spawns = []
        self.items = []
        #player buffs
        self.poison = 0
        self.poisonTick =0
        self.jumpBuffTime = 0
        #player fx
        self.pain = pygame.mixer.Sound('SFX/pPain.ogg')
        self.pain.set_volume(0.3)
        #player items
        self.potion = 1
        self.antidote = 1
        self.consume=0#consume potion[0] or antidote[1]
        self.sword=False
        self.bow=False
        self.arrows = 0
        #player keys
        self.onCorner = False
        self.grab=False
        self.rectCol=False
        self.sliding=False
        self.incapacitated = False
        self.running = False
        self.onWall = False
        self.crouch = False
        self.taunt = False
        self.swordDrawed = False
        self.shooting = False
        self.dead=False
        self.bigDamage = False#Si recibe un golpe fuerte
        self.bowSpeed = 40
        self.attackCount = 0 #timer de combo
        self.combo1 = 0#ataques consecutivos sin espada
        self.combo2 = 10#ataques consecutivos con espada
        self.combo3 = 22#ataques consecutivos en aire
        self.assets = 0 #indica el set de sprites a usar [0,1,2][nada,espada,arco]
        self.con=self.lim[self.assets][self.action]
        #Timers
        self.bowCD = 0
        self.arrowShoot = False
        self.drawCd=0
        self.consumeTime=0
        self.wallRunning=10
        self.godCD = 0
        #level Keys
        self.stage=0
        self.levelC=False
        self.level=level
        self.key=[False,False]#llave dorada y plateada
        self.activate=False
        self.pause=False
        self.godMode = False
        self.fly = False
        self.game = False

    def startingPos(self,pos):
        self.rect = self.image.get_rect(center=pos)

    def newStage(self,platforms,obstacles,pos=(100,100)):
        self.rect.center = pos
        self.platforms = platforms
        self.obstacles = obstacles
        self.startPos = (-2000,0)
        self.hitbox.center = self.rect.center
        self.top.midbottom = (self.hitbox.center[0],self.hitbox.top-4)
        self.head.midtop = (self.hitbox.center[0],self.hitbox.top)
    def nextStage(self):
        self.stage+=1
        self.key=[False,False]
        self.levelC=False
        self.poison = 0
        self.poisonTick = 0
    def setBuff(self,t):
        if t == 0:
            self.potion +=1
            print("potion obtained")
        if t == 1:#antidote
            if self.antidote < 3:
                self.antidote += 1
                print("antidote obtained")
            else:
                print("already got max antidotes")
        if t == 2:
            print("less damage with sword")
            if self.damage[1] > 1:
                self.damage[1] -= 1
        if t == 3:
            print("more jump")
            self.jump_strength = self.originalJumpS + 1
            self.jumpBuffTime = 500
        if t == 4:
            print("more damage with sword")
            self.damage[1] += 1
        #more bow speed
    def setPoison(self,damage):
        if self.immunity == 0:
            self.poison = damage
            self.poisonTick = 1200
    def removePoison(self):
        self.poison = 0
        self.poisonTick = 0
        print("antiote consumed")
        self.antidote-=1
    def consumePotion(self):
        if self.potion > 0 and self.hp < self.maxHp:
            self.consumeTime = 40
            self.consume = 0
            if self.sword: self.action = 26
            else: self.action = 23
    def consumeAntidote(self):
        if self.antidote > 0 and self.poison > 0:
            self.consumeTime = 10
            self.consume = 1
            if self.sword: self.action = 26
            else: self.action = 23
    def emptyDie(self):
        if self.rect.top > 770:
            self.dead=True
    def die(self):
        self.immunity = 500
        if self.sword:
            self.assets=1
            self.action = 14

        else:
            self.assets=0
            self.action = 22
    def gotHit(self,hit,power=1,rect=(0,0,0,0)):
        if self.immunity == 0 and not self.godMode:
            self.incapacitated = True
            self.pain.play()
            print("hit")
            self.hp -= hit
            self.immunity = 30
            if power==1:
                self.vel.x = 0
                if self.sword:
                    self.assets=1
                    self.action = 13
                else:
                    self.assets=0
                    self.action = 21
                self.con=0
            if power == 2:
                self.heavyHit(rect)
    def heavyHit(self,r):
        self.immunity = 60
        self.bigDamage = True
        #set direccion opuesta y velocidad x y
        if self.sword:
            self.lostSword()
        self.action = 8
        if self.hitbox.x < r.x:
            self.dir = 1
            self.vel.x = -3
        else:
            self.dir = 0
            self.vel.x = 3
        self.vel.y = -3
    def gotSword(self):
        self.sword = True
        self.assets = 1
        self.idle = 0
        self.action = 16
    def lostSword(self):
        self.sword = False
        self.assets = 0
        self.idle = 14
        self.action = self.idle
        if self.dir == 1:
            item=SwordItem(self.rect.midright)
        else:
            item=SwordItem((self.rect.left-16,self.rect.center[1]))
        self.items.add(item)
    def bowAttack(self):
        if self.bow and self.arrows > 0 and self.bowCD == 0:
            self.assets = 2
            self.con = 0
            self.shooting = True
            if self.onGround:
                self.action = 0
            else:
                self.action = 1
            self.bowCD = self.bowSpeed
            self.arrows -= 1
    def shootArrow(self,projectiles):
        p = projectiles
        arrow = Arrow(self.platforms,self.hitbox.center,self.dir,self.damage[2],0,300,True)
        p.add(arrow)
        projectiles = p
        self.arrowShoot = True
    def animation_list(self,dt):
        #Time dependant
        #Cambios de animacion
        if self.sword and (self.action==18 or self.action==7) and not self.onWall:
            self.action=4
            self.con = 0
            self.vel.y = 2
        if self.sword and self.action==8 and not self.onCorner:
            self.action=4
            self.con = 0
            self.vel.y = 0
        if self.running and self.action == 13 and not self.onWall :
            self.action=17
            self.con = 2
        #Cantidad de imagenes de la accion
        images =self.lim[self.assets][self.action+1] - self.lim[self.assets][self.action]
        #Checkeos
        if self.act != self.action:
            self.act = self.action
            self.con = 0
        #animacion al consumir pociones
        if self.consumeTime>0 and self.con == images-1:
            if (self.sword and self.action == 26) or (not self.sword and self.action == 23):
                self.con = images - 3
            else:
                self.consumeTime = 0
        #animacion del golpe  fuerte
        if not self.sword and self.bigDamage and not self.onGround and self.con == images-3:
            self.action = 8
            self.con= images - 4
        #Ataque al piso con espada
        if self.sword and not self.onGround and self.action == 24 and self.con == images - 3:
            self.con = images - 5
        #Prioridad del arco
        if self.shooting:
            self.vel.x = 0
            if self.action==1:self.vel.y = 0
        #Direccion
        if self.dir == 1: #derecha
            sprite = self.spritesR[self.assets]
        else:#izquierda
            sprite = self.spritesL[self.assets]
        #Animacion
        self.currentTime += dt
        if self.currentTime >= self.animationTime:
            self.currentTime = 0
            self.con = (self.con % images)
            index = self.con + self.lim[self.assets][self.action]
            self.image = sprite[index]
            self.con+=1
            #reset de animacion
            if index == self.lim[self.assets][self.action+1]-1:
                if self.sword:
                    if self.action == 14:self.dead=True
                    self.assets = 1
                    self.idle = 0
                    tmp = self.action
                    if self.swordDrawed: self.idle = 9
                    self.action = self.idle
                    if not self.onGround:self.action=4
                    if tmp==7 and self.grab:self.action = tmp
                else:
                    if self.action == 22:self.dead=True
                    self.assets = 0
                    self.idle = 14
                    tmp = self.action
                    self.action = self.idle
                    if not self.onGround:self.action=18
                    if tmp == 6 or tmp == 7 and self.vel.x != 0:self.action = 7
                    if self.bigDamage:
                        self.action = 9
                        self.bigDamage = False
                self.shooting = False
                self.con=0
    def resetHitbox(self,t=0):
        if t==0:
            if self.sword and self.action != 1 and self.crouch:
                self.crouch = False
                self.hitbox.height = 30
                self.hitbox.bottom = self.rect.bottom - 1
            elif not self.sword and (self.action != 15 and self.action != 11) and self.crouch:
                self.crouch = False
                self.hitbox.height = 30
                self.hitbox.bottom = self.rect.bottom - 1
        else:
            if self.sword and self.sliding:
                self.hitbox.width = 26
                self.hitbox.center = self.rect.center
                self.sliding = False
    def jump(self,strength,force=False):
        if not self.bigDamage and not self.incapacitated:
            if self.sword:
                self.assets = 1
                if not self.swordDrawed or force:
                    self.action = 3
                    self.vel.y = -strength
                    self.onGround = False
            else:
                self.assets = 0
                self.action=17
                self.vel.y = -strength
                self.onGround = False
    def createFx(self,effects,t=0):
        self.fx = StatusEffect1(self.head.center,0)
        #self.fx = CastEffects(self.hitbox.center,0)
        effects.add(self.fx)
    def updateFx(self):
        if self.fx!=None:
            self.fx.rect.center = self.top.center
    def update(self,mobs,spawns,projectiles,items,effects,dt):
        #actualizacion del personaje
        #Disparar flecha
        if self.assets == 2 and not self.arrowShoot:
            if self.action == 0:
                if self.con == 7:
                    self.shootArrow(projectiles)
            else:
                if self.con == 5:
                    self.shootArrow(projectiles)
        if self.poison > 0:
            if self.fx == None:
                self.createFx(effects)
        else:
            if self.fx != None:
                self.fx.loop = False
                self.fx = None
        self.activate = False
        self.checkNearby()
        self.mobs = mobs
        self.spawns = spawns
        self.items = items
        self.checkStatus()
        self.updateStatus(dt)
        self.updateFx()
        self.emptyDie()
        items = self.items
    def updateStatus(self,dt):
        self.resetHitbox()
        self.rectCol=False
        self.grab=False
        self.onCorner = False
        # increment in x direction
        self.rect.left += self.vel.x
        self.hitbox.left += self.vel.x
        self.top.left += self.vel.x
        self.head.left += self.vel.x
        # do x-axis collisions
        self.onWall = False
        self.collide(self.vel.x, 0)
        # increment in y direction
        self.rect.bottom += self.vel.y
        self.hitbox.bottom += self.vel.y
        self.top.bottom += self.vel.y
        self.head.bottom += self.vel.y
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.vel.y)
        self.animationTime = 0.08
        if self.sword:
            if self.action == 3:
                self.animationTime = 0.05
        else:
            if self.action == 17:
                self.animationTime = 0.05
        self.animation_list(dt)
        #Timers
        if self.immunity > 0 :
            self.immunity -=1
            if self.immunity < 15 and not self.bigDamage:
                self.incapacitated = False
        if self.bowCD > 0:
            self.bowCD -= 1
            if self.bowCD == 0:
                self.arrowShoot = False
        if self.attackCount > 0:
            self.attackCount -= 1
            if self.attackCount == 0:
                self.combo1 = 0
                self.combo2 = 10
                self.combo3 = 22
        if self.poisonTick > 0:
            self.poisonTick -=1
            if self.poisonTick % 100 == 0:self.gotHit(self.poison)
        if self.jumpBuffTime > 0:
            self.jumpBuffTime -= 1
            if self.jumpBuffTime == 0:
                self.jump_strength = self.originalJumpS
        if self.wallRunning < 0:
            self.wallRunning += 1
            if self.wallRunning == 0:
                self.wallRunning = 10
        if self.drawCd > 0:
            self.drawCd -=1
        if self.godMode:
            self.key = [True,True]
        if self.godCD > 0:
            self.godCD -= 1
        if self.consumeTime > 0:
            self.consumeTime-=1
            if self.consumeTime == 0:
                if self.consume == 0:
                    self.hp += 5
                    self.potion -= 1
                    print("potion")
                if self.consume == 1:
                    self.removePoison()
        #Reset el hitbox si no esta tocando bloques
        if not self.rectCol:
            if self.sliding:
                self.resetHitbox(1)

    def setGod(self):
        if self.godMode:
            self.godMode = False
            self.damage = [1,3,2]
        else:
            self.godMode = True
            self.key = [True,True]
            self.damage = [20,20,20]
        self.godCD = 50
    def checkStatus(self):
        pressed = pygame.key.get_pressed()
        up = pressed[K_w]
        left = pressed[K_a]
        right = pressed[K_d]
        down = pressed[K_s]
        attack = pressed[K_j]
        bowAttack = pressed[K_k]
        running = pressed[K_LSHIFT]
        jump = pressed[K_SPACE]
        consume1 = pressed[K_e]
        consume2 = pressed[K_r]
        drop = pressed[K_q]
        draw = pressed[K_f]
        p = pressed[K_p]
        o = pressed[K_o]
        i = pressed[K_i]
        u = pressed[K_u]
        h = pressed[K_h]
        god = p and u
        fly = i and h
        if god and self.godCD == 0:
            print("extra")
            self.setGod()
        if fly and self.godCD == 0:
            if self.fly:
                self.fly = False
            else:
                self.fly = True
                print("1")
        #pegarse en pared con espada
        if self.grab and self.sword:
            if self.vel.y >=0 and self.vel.y < 4:
                if (self.action ==3 or  self.action==4) and self.action != 8:
                    self.action=7
                    self.sliding = True
                    self.hitbox.width = 20
                    self.hitbox.center = self.rect.center
        #reset del wallRunning y poner animacion idle en piso
        if self.onGround:
            if self.hp <= 0:
                self.die()
            elif not self.shooting and not self.incapacitated:
                if self.sword and (self.action in [4,18]):
                    self.action = self.idle
                elif (not self.sword) and self.action in [7,18]:
                    self.action = self.idle
            if (self.wallRunning >= 0 and self.wallRunning < 7):
                self.wallRunning = -100

        #TECLAS
        if draw:
            if self.sword and self.drawCd == 0:
                if self.swordDrawed:
                    self.action=16
                    self.swordDrawed = False
                else:
                    self.action=15
                    self.swordDrawed = True
                self.drawCd = 20
        #tira la espada
        if drop:
            if self.sword:self.lostSword()
        if consume1 and self.onGround:
            self.consumePotion()
        if consume2 and self.onGround:
            self.consumeAntidote()
        #activar o trepar en esquinas
        if up:
            if self.vel.x == 0 and self.onGround and not self.shooting:
                self.activate = True
            if self.onCorner and self.sword:
                if self.action == 4 or self.action == 7:
                    self.action = 8
            if self.fly:
                self.vel.y = -5
        if down and self.fly and not self.onGround:
            self.vel.y = 5
        if (not down and not up) and self.fly:
            self.vel.y=0
        #agacharse
        if down and self.onGround and not self.shooting and not self.onWall:
            if self.sword and self.action in [0,1,9,2,25,26]:
                self.action = 1
                self.crouch = True
                self.hitbox.height = 19
                self.hitbox.bottom = self.rect.bottom -1
            elif not(self.sword) and self.action in [15,10,12,14,16,23]:
                self.crouch = True
                self.action=15
                self.hitbox.height = 19
                self.hitbox.bottom = self.rect.bottom -1
        #deslizarse en pared hacia abajo
        if down and self.grab and self.vel.y >=0:
            if (self.action ==3 or  self.action==4 or self.action==18 or self.action==7):
                if self.vel.y >4:
                    self.vel.y = 4
                self.action=18
                self.sliding = True
                self.hitbox.width = 20
                self.hitbox.center = self.rect.center
        if jump and not self.shooting and self.hp > 0:
            # only jump if on the ground
            if self.onGround:
                self.jump(self.jump_strength)
        #animaciones de movimiento con y sin espada
        if left and not self.shooting and not self.incapacitated:
            self.vel.x = -self.speed
            self.dir = 0
            if self.onGround:
                if self.sword:
                    if self.action in [0,9,2,25,26]:
                        if self.swordDrawed:self.action=25
                        else:self.action = 2
                    else:
                        if self.action == 12 and self.con<57:
                            pass
                        else:self.vel.x = 0
                else:
                    if self.action in [10,12,14,16,23]:
                        self.action = 16
                    else:
                        if down:
                            self.action=11
                            self.crouch = True
                        elif not down and self.action == 11:
                            self.action = 16
                        else:self.vel.x = 0
        #animaciones de movimiento con y sin espada
        if right and not self.shooting and not self.incapacitated:
            self.vel.x = self.speed
            self.dir = 1
            if self.onGround:
                if self.sword:
                    if self.action in [0,9,2,25,26]:
                        if self.swordDrawed:self.action=25
                        else:self.action = 2
                    else:
                        if self.action == 12 and self.con<57:
                            pass
                        else:self.vel.x = 0
                else:
                    if self.action in [10,12,14,16,23]:
                        self.action = 16
                    else:
                        if down:
                            self.action=11
                            self.crouch = True
                        elif not down and self.action == 11:
                            self.action = 16
                        else:self.vel.x = 0
        if running and not self.incapacitated:#solo corre sin espada, y puede correr en pared
            if not self.sword and not down:
                self.running = True
                self.vel.x *= 1.5
                if self.onGround and self.action == 16:
                    self.action = 12
                min_=self.lim[self.assets][self.action]
                if self.onWall and self.action in [12,13,17,18] and self.wallRunning > 0:
                    if self.action == 17:
                        if self.con > min_+1:
                            self.action = 13
                            self.vel.y = -4
                            self.wallRunning -=1
                    else:
                        self.action = 13
                        self.vel.y = -4
                        self.wallRunning -=1
        else:
            self.running = False
        if attack  and self.hp > 0 and self.immunity < 15:
            #Ataques en piso
            if self.onGround:

                if self.sword:
                    if not self.action in [10,11,12] and self.swordDrawed:
                        self.action = self.combo2
                        self.attackCount = 50
                        if self.combo2<12:self.combo2+=1
                        else: self.combo2 = 10
                        self.combo1 = 0
                        self.combo3 = 22
                        if self.action != 12:
                            self.vel.x = 0
                    #else:

                elif not self.sword and not self.action in [0,1,2,3,4,5]:
                    self.action = self.combo1
                    self.attackCount = 50
                    if self.combo1<5:self.combo1+=1
                    else: self.combo1 = 0
                    self.combo2 = 10
                    self.combo3 = 22
                    self.vel.x = 0
            #ataques en aire
            else:
                if self.sword:
                    if not self.action in [22,23,24]:
                        self.action = self.combo3
                        if self.combo3 == 24:
                            self.vel.y = 7
                            self.vel.x = 0
                        self.attackCount = 50
                        if self.combo3<24:self.combo3+=1
                        else: self.combo3 = 22
                        self.combo1 = 0
                        self.combo2 = 10

                else:
                    if self.action != 6 and self.action != 7:
                        self.action= 6
                        self.vel.y += 1
        if bowAttack:
            self.bowAttack()

        #Gravedad
        if not self.onGround and not self.shooting:
            # only accelerate with gravity if in the air
            if not self.fly:
                self.vel += GRAVITY
            # max falling speed
            if self.vel.y > 100: self.vel.y = 100
            #falling
            if self.sword:
                if self.action == 7:
                    self.vel.y = 0
                if self.action == 8:
                    self.vel.y = -2
                if (self.action==2 or self.action==25):
                    self.action = 4
            elif (not self.sword) and self.action==16:
                self.action = 18


        #Dejar de moverse
        if not(left or right) and self.assets != 2 and not self.bigDamage:
            self.vel.x = 0
            if self.onGround:
                if self.sword and (self.action in [1,2,25,4]):
                    if not down:self.action = self.idle
                    else: self.action = 1
                elif (not self.sword) and self.action in [18,10,11,12,15,16]:
                    if not down:self.action = self.idle
                    else: self.action = 15
    def collide(self, xvel, yvel):
        corner = True
        grab = False
        for p in self.nearbyTiles:
            if p.type==0:
                if self.top.colliderect(p.rect):
                    corner = False
                if self.rect.colliderect(p.rect):
                    self.rectCol = True
                if self.hitbox.colliderect(p.rect):
                    if isinstance(p, ExitBlock):
                        pygame.event.post(pygame.event.Event(QUIT))
                    if self.head.colliderect(p.rect):
                        grab = True
                    if xvel > 0:
                        self.hitbox.right = p.rect.left
                        self.rect.center = self.hitbox.center
                        self.onWall = True
                    if xvel < 0:
                        self.hitbox.left = p.rect.right
                        self.rect.center = self.hitbox.center
                        self.onWall = True
                    if yvel > 0:
                        self.hitbox.bottom = p.rect.top
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        if yvel > 15:
                            print(4)
                            self.gotHit(yvel%10)
                        self.vel.y = 3
                    if yvel < 0:
                        self.hitbox.top = p.rect.bottom
                        self.rect.center = self.hitbox.center
                    self.top.midbottom = (self.hitbox.center[0],self.hitbox.top-4)
                    self.head.midtop = (self.hitbox.center[0],self.hitbox.top)
        if self.onWall and not self.onGround:
            if grab:
                self.grab = True
            if corner:
                self.onCorner = True
        self.levelComplete()
        if self.assets != 2:
            self.enemiesCheck()
            self.spawnsCheck()
        self.obstaclesCheck()
    def levelComplete(self):
        if self.key[0] == True:
            for e in self.level:
                if self.hitbox.colliderect(e.rect):
                    self.levelC=True
    def obstaclesCheck(self):
        for e in self.nearbyObst:
            if self.hitbox.colliderect(e.rect):
                if e.type == 0:
                    self.gotHit(10)
                if e.type == 1 or e.type ==5:
                    if self.hitbox.top <= e.rect.top: self.gotHit(1)
                if e.type == 2 or e.type == 6:
                    if self.hitbox.bottom >= e.rect.bottom: self.gotHit(1)
                if e.type == 3 or e.type == 7:
                    if self.hitbox.right >= e.rect.right: self.gotHit(1)
                if e.type == 4 or e.type == 8:
                    if self.hitbox.left <= e.rect.left: self.gotHit(1)
    def enemiesCheck(self):
        for e in self.mobs:
            if self.rect.colliderect(e.hitbox):
                if self.sword:
                    #ataques 10,11,12-22,23,24
                    if self.action in [10,11,12] and self.con == 3:
                        e.gotHit(self.damage[1])
                    if (self.action == 22 or self.action == 23) and self.con == 1:
                        e.gotHit(2)
                    if self.action == 24 and self.con > 1:
                        e.gotHit(2)

                else:
                    if self.hitbox.colliderect(e.hitbox):
                    #ataques 0,1,2,3,4,5-7
                        if self.action in [0,1,2,3,4,5] and self.con < 4:
                            e.gotHit(self.damage[0])
                        if self.action == 7:
                            e.gotHit(self.damage[0])
    def spawnsCheck(self):
        for e in self.spawns:
            if self.rect.colliderect(e.hitbox):
                if self.sword:
                    #ataques 10,11,12-22,23,24
                    if self.action in [10,11,12] and self.con == 3:
                        e.gotHit(self.damage[1])
                    if (self.action == 22 or self.action == 23) and self.con == 1:
                        e.gotHit(2)
                    if self.action == 24 and self.con > 1:
                        e.gotHit(2)

                else:
                    if self.hitbox.colliderect(e.hitbox):
                    #ataques 0,1,2,3,4,5-7
                        if self.action in [0,1,2,3,4,5] and self.con < 4:
                            e.gotHit(self.damage[0])
                        if self.action == 7:
                            e.gotHit(self.damage[0])
"""Projectiles"""
class Projectiles(Sprite):
    def __init__(self,platforms,damage, *args):
        super().__init__(platforms)
        self.damage = damage
        self.playerHurt = True
        self.lifespan = 300

    def gotHit(self):
        self.kill()
    def checkLifespan(self):
        if self.lifespan > 1:
            self.lifespan -=1
            if self.lifespan == 1:
                self.kill()
    def collide(self,player,enemies,spawns):
        self.collideWalls()
        if self.playerHurt:
            self.collidePlayer(player)
        else:
            self.collideEnemy(enemies)
            self.collideSpawns(spawns)
    def collideWalls(self):
        for p in self.nearbyTiles:
            if (p.type == 0) and self.hitbox.colliderect(p.rect):
                self.gotHit()
    def collidePlayer(self,p):
        if self.hitbox.colliderect(p.hitbox):
            if self.damage > 4:
                p.gotHit(self.damage,2,self.hitbox)
            else:
                p.gotHit(self.damage)
            self.gotHit()
    def collideEnemy(self,enemies):
        for e in enemies:
            if self.hitbox.colliderect(e.hitbox):
                e.gotHit(self.damage)
                self.gotHit()
    def collideSpawns(self,spawns):
        for e in spawns:
            if self.hitbox.colliderect(e.hitbox):
                e.gotHit(self.damage)
                self.gotHit()
class Arrow(Projectiles):
    def __init__(self,platforms, pos,dir_,damage=1,type_=0,speed=300,playerShooter=False, *args):
        super().__init__(platforms,damage)
        asset = SS_PROJECTILES["arrowA"]
        if playerShooter:
            self.playerHurt = False
            asset = SS_PROJECTILES["pArrow"]
        else:
            if type_ == 0:
                asset = SS_PROJECTILES["arrowA"]
            elif type_ == 1:
                asset = SS_PROJECTILES["arrowB"]
            else:
                asset = SS_PROJECTILES["arrowC"]
        self.dir = dir_
        if dir_ == 1:
            self.m=asset
            self.speed = speed
        else:
            self.m=funciones.spriteFlip(asset)
            self.speed = -speed
        self.image=self.m[self.action][self.con]
        self.rect= self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(20,0)
        self.hitbox.center = self.rect.center
        self.chunkSize=(WIN_WIDTH,self.rect.height)
        self.refreshNearby()

    def update(self,player,dt,enemies,spawners,*args):
        self.checkNearby()
        self.checkLifespan()
        self.rect.left += self.speed*dt
        self.hitbox.left += self.speed*dt
        self.collide(player,enemies,spawners)
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False
class ExplosiveArrow(Arrow):
    def __init__(self,platforms, pos,dir_,damage=1,speed=300, *args):
        super().__init__(platforms,pos,dir_,damage,1,speed)
        self.start = False
        self.boom = pygame.mixer.Sound("SFX/explosion.ogg")

    def gotHit(self):
        self.start = True

    def explode(self,effects):
        ex = CastEffects(self.hitbox.center,1,5)
        ex.loop = False
        effects.add(ex)
        self.boom.play()
        self.kill()
    def update(self,player,dt,e,s,effects,*args):
        if self.start:
            self.explode(effects)
        self.checkNearby()
        self.checkLifespan()
        self.rect.left += self.speed*dt
        self.hitbox.left += self.speed*dt
        self.collide(player)
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False

    def collide(self,p):
        if self.hitbox.colliderect(p.hitbox):
            p.gotHit(self.damage)
            self.gotHit()
        self.collideWalls()
    def collideWalls(self):
        for p in self.nearbyTiles:
            if (p.type == 0) and self.hitbox.colliderect(p.rect):
                self.gotHit()
class FrostArrow(Arrow):
    def __init__(self,platforms, pos,dir_,damage=1,speed=300, *args):
        super().__init__(platforms,pos,dir_,damage,2,speed)
        self.start = False
        self.r = random.randint(150,250)
        self.boom = pygame.mixer.Sound("SFX/iceshatter.ogg")

    def gotHit(self):
        self.start = True

    def explode(self,effects,projectiles):
        ex = CastEffects(self.hitbox.center,3,2)
        ex.loop = False
        effects.add(ex)
        left = (self.hitbox.left,self.hitbox.center[1])
        right = (self.hitbox.right,self.hitbox.center[1])
        shot = IcePick(self.platforms,right,1)
        projectiles.add(shot)
        shot = IcePick(self.platforms,left,0)
        projectiles.add(shot)
        self.boom.play()
        self.kill()
    def update(self,player,dt,e,s,effects,projectiles,*args):
        if self.start:
            self.explode(effects,projectiles)
        self.checkNearby()
        self.checkLifespan()
        if self.lifespan <= self.r:
            self.start = True
        self.rect.left += self.speed*dt
        self.hitbox.left += self.speed*dt
        self.collide(player)
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False

    def collide(self,p):
        if self.hitbox.colliderect(p.hitbox):
            p.gotHit(self.damage)
            self.gotHit()
        self.collideWalls()
    def collideWalls(self):
        for p in self.nearbyTiles:
            if (p.type == 0) and self.hitbox.colliderect(p.rect):
                self.gotHit()
class IcePick(Projectiles):
    def __init__(self,platforms, pos,dir_,damage=3, *args):
        super().__init__(platforms,damage)
        asset = SS_PROJECTILES["icepick"]
        self.dir = dir_
        self.con = 0
        self.speed = 0
        if dir_ == 1:
            self.m=asset
            self.speed = 300
        else:
            self.speed = -300
            self.m=funciones.spriteFlip(asset)
        self.image=self.m[0][self.con]
        self.max = len(self.m[0])
        self.rect= self.image.get_rect(center=pos)
        self.hitbox = Rect(0,0,64,20)
        self.hitbox.center = self.rect.center
        self.chunkSize=(WIN_WIDTH,self.rect.height)
        self.refreshNearby()
    def animation(self,dt):
        self.currentTime += dt
        if self.currentTime >= self.animationTime:
            self.currentTime = 0
            self.con = (self.con) % self.max
            self.image = self.m[0][self.con]
            self.con+=1
    def update(self,player,dt,*args):
        self.checkNearby()
        self.checkLifespan()
        self.animation(dt)
        self.rect.left += self.speed*dt
        self.hitbox.left += self.speed*dt
        super().collideWalls()
        super().collidePlayer(player)
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False
class ImpShot(Projectiles):
    def __init__(self,platforms, pos,dir_,damage=1, *args):
        super().__init__(platforms,damage)
        asset = SS_PROJECTILES["impShot"]
        self.dir = dir_
        self.con = 0
        self.speed = 0
        if dir_ == 1:
            self.m=asset

        else:
            self.m=funciones.spriteFlip(asset)

        self.image=self.m[self.con]
        self.rect= self.image.get_rect(center=pos)
        self.hitbox = Rect(0,0,10,5)
        self.hitbox.center = pos
        self.chunkSize=(WIN_WIDTH,self.rect.height)
        self.refreshNearby()
    def animation(self,dt):
        self.currentTime += dt
        if int(self.con) == 3:
            if self.dir == 1:
                self.speed = 240
            else:
                self.speed = -240
        if self.currentTime >= self.animationTime and self.con < 5:
            self.currentTime = 0
            self.con = (self.con) % 5
            self.image = self.m[self.con]
            self.con+=1
    def update(self,player,dt,*args):
        self.checkNearby()
        self.checkLifespan()
        self.animation(dt)
        self.rect.left += self.speed*dt
        self.hitbox.left += self.speed*dt
        super().collideWalls()
        super().collidePlayer(player)
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False
class GranImpShot(Projectiles):
    def __init__(self,platforms, pos,dir_,damage=1, *args):
        super().__init__(platforms,damage)
        asset = SS_PROJECTILES["GImpShot"]
        self.dir = dir_
        self.con = 0
        self.speed = 0
        if dir_ == 0:
            self.m=asset
            self.speed = -120
        else:
            self.speed = 120
            self.m=funciones.spriteFlip(asset)
        self.image=self.m[self.action][self.con]
        self.rect= self.image.get_rect(center=pos)
        self.hitbox = self.rect
        self.chunkSize=(WIN_WIDTH,self.rect.height)
        self.refreshNearby()
    def animation(self,dt):
        self.currentTime += dt
        if self.currentTime >= self.animationTime:
            self.currentTime = 0
            self.con = (self.con) % 3
            self.image = self.m[0][self.con]
            self.con+=1
    def update(self,player,dt,*args):
        self.checkNearby()
        self.checkLifespan()
        self.animation(dt)
        self.rect.left += self.speed*dt
        self.hitbox.left += self.speed*dt
        super().collideWalls()
        super().collidePlayer(player)
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False
"""Items"""
class Item(Sprite):
    """Clase abstracta de los items"""
    def __init__(self, pos, *args):
        super().__init__(pos)
        asset = SS_ITEM["items"]
        self.m=asset

    def update(self,player):
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False

    def staticAnimation(self):
        self.image=self.m[self.action][int(self.con)]
        if self.con < self.lim[self.action]-0.2:
            self.con+=0.2
        else:
            self.con=0
class Potion(Item):
    def __init__(self, pos,type_=0, *args):
        super().__init__(None)
        asset = SS_ITEM["potions"]
        self.image=self.m[5][1]
        self.rect= self.image.get_rect(topleft=pos)
        self.hitbox = self.rect
        self.type=type_
        if type_ == 0:self.image=self.m[13][1]#heal
        if type_ == 1:self.image=self.m[13][3]#antidote
        if type_ == 2:self.image=self.m[4][15]#less damage
        if type_ == 3:self.image=self.m[5][0]#more jump
        if type_ == 4:self.image=self.m[5][1]#more damage

    def update(self,player):
        self.collidePlayer(player)
        super().update(player)

    def collidePlayer(self,p):
        if self.hitbox.colliderect(p.hitbox):
            p.setBuff(self.type)
            self.kill()
class ArrowItem(Item):
    def __init__(self, pos, *args):
        super().__init__(pos)
        asset = SS_ITEM["items"]
        self.m=asset
        self.image=self.m[0][4]
        self.rect= self.image.get_rect(topleft=pos)
        self.hitbox = self.rect
    def update(self,player):
        self.collidePlayer(player)
        super().update(player)

    def collidePlayer(self,p):
        if self.hitbox.colliderect(p.hitbox):
            p.arrows += 1
            self.kill()
class SwordItem(Item):
    def __init__(self, pos, *args):
        super().__init__(pos)
        asset = SS_ITEM["items"]
        self.m=asset
        self.image=self.m[18][3]
        self.rect= self.image.get_rect(topleft=pos)
        self.hitbox = self.rect
    def update(self,player):
        self.collidePlayer(player)
        super().update(player)

    def collidePlayer(self,p):
        if self.hitbox.colliderect(p.hitbox):
            if not p.incapacitated:
                p.gotSword()
                self.kill()
class BowItem(Item):
    def __init__(self, pos, *args):
        super().__init__(pos)
        asset = SS_ITEM["items"]
        self.m=asset
        self.image=self.m[3][14]
        self.rect= self.image.get_rect(topleft=pos)
        self.hitbox = self.rect
    def update(self,player):
        self.collidePlayer(player)
        super().update(player)

    def collidePlayer(self,p):
        if self.hitbox.colliderect(p.hitbox):
            p.bow = True
            self.kill()
class Key(Item):
    def __init__(self, pos,type_=0,obj=True, *args):
        super().__init__(pos)
        asset = SS_ITEM["keys"]
        self.obj = obj
        self.m=asset
        self.image=self.m[self.action][self.con]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect
        self.lim=[12,6,12,6]
        self.action=type_

    def update(self,player):
        super().staticAnimation()
        if self.obj:
            self.collidePlayer(player)
        super().update(player)

    def collidePlayer(self,p):
        #si recoge llave dorada el key[0] es true para pasar el nivel
        if self.hitbox.colliderect(p.hitbox):
            if self.action < 2:
                p.key[0] = True
            else:
                p.key[1] = True
            self.kill()
"""Effects"""
class Effect(Sprite):
    """Clase abstracta de los efectos"""
    def __init__(self, pos, *args):
        super().__init__(pos)
        asset = SS_FX["status1"]
        self.m=asset
        self.loop = True

    def animation(self,dt):
        #Time dependant
        sprite = self.m
        #Cantidad de imagenes de la accion
        images =self.lim[self.action+1] - self.lim[self.action]
        self.currentTime += dt
        if self.currentTime >= self.animationTime:
            self.currentTime = 0
            self.con = ((self.con) % images)
            index = self.con + self.lim[self.action]
            self.image = sprite[index]
            self.con += 1
            #reset de animacion
            if index == self.lim[self.action+1]-1:
                if not self.loop:self.kill()
                self.con = 0

    def update(self,player):
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False
class StatusEffect1(Effect):
    def __init__(self, pos,type_=0, *args):
        super().__init__(pos)
        asset = SS_FX["status1"]
        self.m=asset
        self.action = type_
        self.lim = [0,8,14,20,24,30]
        self.image = self.m[self.con+self.lim[self.action]]
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect

    def update(self,player,dt,*args):
        super().animation(dt)
        self.hitbox.center = self.rect.center
class StatusEffect2(Effect):
    def __init__(self, pos,type_=0, *args):
        super().__init__(pos)
        asset = SS_FX["status2"]
        self.m=asset
        self.action = type_
        self.lim = [0,8,16,21,29,37]
        self.image = self.m[self.con+self.lim[self.action]]
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect

    def update(self,player,dt,*args):
        super().animation(dt)
        self.hitbox.center = self.rect.center
class CastEffects(Effect):
    def __init__(self, pos,type_=0,damage = 0, *args):
        super().__init__(pos)
        self.animationTime = 0.05
        self.type = 0
        if type_ == 0:
            asset = SS_FX["icecast"]
            self.hitbox = Rect(0,0,60,60)
            self.type = 1
        elif type_ == 1:
            asset = SS_FX["xplosion"]
            self.hitbox = Rect(0,0,60,60)
            self.animationTime = 0.01
        elif type_ == 2:
            asset = SS_FX["firecast"]
            self.hitbox = Rect(0,0,60,60)
            self.type = 1
        elif type_ == 3:
            asset = SS_FX["iceshatter"]
            self.hitbox = Rect(0,0,60,60)
            self.animationTime = 0.01
        elif type_ == 4:
            asset = SS_FX["shock"]
            self.hitbox = Rect(0,0,60,60)
            self.loop = False
        l=len(asset)
        self.lim = [0,l]
        self.damage = damage
        self.m=asset
        self.image = self.m[self.con]
        self.rect = self.image.get_rect(center = pos)
        self.hitbox.center = self.rect.center

    def update(self,player,dt,projectiles,*args):
        super().animation(dt)
        self.hitbox.center = self.rect.center
        if self.damage > 0:
            self.checkPlayer(player)
        if self.type == 1:
            self.checkProjectiles(projectiles)

    def checkPlayer(self,p):
        if self.hitbox.colliderect(p.hitbox):
            p.gotHit(self.damage)
    def checkProjectiles(self,projectiles):
        for a in projectiles:
            if not a.playerHurt:
                if self.rect.colliderect(a.hitbox):
                    a.gotHit()
"""Structures"""
class Door(Sprite):
    def __init__(self,pos,type_=2, *groups):
        super().__init__(None, *groups)
        asset = SS_STRUCTURES["doors"]
        self.action=type_
        self.mR=asset
        self.image=self.mR[self.action][int(self.con)]
        self.rect = self.image.get_rect(left=pos[0],bottom=pos[1]+16)
        self.hitbox = self.rect
        self.lim=[4,4,4,4,4,4]
        self.opened=False
        self.activated= False

    def open(self):
        self.image=self.mR[self.action][int(self.con)]
        if self.con < self.lim[self.action]-0.1:
            self.con+=0.1
        else:
            self.opened=True

    def update(self,player):
        if self.con > 0 and self.con < self.lim[self.action]:self.open()
        if not self.activated:self.collidePlayer(player)
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False

    def collidePlayer(self,p):
        if self.hitbox.colliderect(p.hitbox):
            if not self.opened:
                if self.action < 3:
                    if p.key[1]:self.open()
                else:
                    if p.key[0]:self.open()
            elif p.activate:
                print("go")
                p.levelC = True
                if p.stage == 3:
                    p.game =True
                #accion al meterse a la puerta
                self.activated = True
class BearTrap(Sprite):
    def __init__(self, pos, *args):
        super().__init__(None)
        asset = SS_STRUCTURES["bearTrap"]
        self.mR=asset
        self.lim=[4]
        self.image=self.mR[self.action][self.con]
        self.rect= Rect(pos[0]-8,pos[1]-2,32,32)
        self.hitbox = self.rect.inflate(-24,-24)
        self.hitbox.center = self.rect.center
        self.activated=False

    def activate(self,prey):
        self.image=self.mR[self.action][int(self.con)]
        if self.con < self.lim[self.action]-0.7:
            self.con+=0.7
        else:
            if not self.activated:prey.gotHit(5)
            self.activated=True

    def update(self,player):
        if self.con > 0 and self.con < self.lim[self.action]:self.activate(player)
        if not self.activated:
            self.collidePlayer(player)
        distx=abs(player.rect[0]-self.rect[0])
        disty=abs(player.rect[1]-self.rect[1])
        if(distx <= WIN_WIDTH and disty <= WIN_HEIGHT):
            self.onCamera = True
        else:
            self.onCamera = False

    def collidePlayer(self,p):
        if self.hitbox.colliderect(p.hitbox):
            if p.immunity == 0:
                self.activate(p)
class Platform(Entity):
    def __init__(self,type_, pos,tset, *groups):
        super().__init__(Color("#DDDDDD"), pos, *groups)
        self.type = 0
        self.tset = tset
        if type_ == 0:
            self.image = self.tset[0][random.randrange(2,3)]
        elif type_ == 1:
            self.image = Surface((TILE_SIZE, TILE_SIZE),pygame.SRCALPHA)
            self.type = 1
        elif type_ == 2:#BOX-RIGHT
            self.image = self.tset[3][3]
        elif type_ == 3:#BOX-LEFT
            self.image = self.tset[4][3]
        elif type_ == 4:#MIDDLE BOX
            self.image = self.tset[6][4]
        elif type_ == 5:#FULL BOX
            self.image = self.tset[6][5]
        elif type_ == 6:
            self.image = Surface((TILE_SIZE, TILE_SIZE),pygame.SRCALPHA)
            self.type = 6
        self.rect = self.image.get_rect()
        self.rect.topleft=(pos[0],pos[1])
        self.rect.height = TILE_SIZE
        self.rect.width = TILE_SIZE
        self.hitbox=self.rect.inflate(0,-8)
        self.hitbox.top=self.rect.top
class Platform2(Entity):
    def __init__(self,type_, pos,tset, *groups):
        super().__init__(Color("#DDDDDD"), pos, *groups)
        self.type = 0
        self.tset = tset
        if type_ == 0:
            self.image = self.tset[0][6]
        elif type_ == 1:
            self.image = Surface((TILE_SIZE, TILE_SIZE),pygame.SRCALPHA)
            self.type = 1
        elif type_ == 2:
            self.image = self.tset[7][7]
        elif type_ == 3:
            self.image = self.tset[7][11]
        elif type_ == 4:
            self.image = self.tset[7][12]
        elif type_ == 5:
            self.image = self.tset[7][13]


        self.rect = self.image.get_rect()
        self.rect.topleft=(pos[0],pos[1])
        self.rect.height = TILE_SIZE
        self.rect.width = TILE_SIZE
        self.hitbox=self.rect.inflate(0,-8)
        self.hitbox.top=self.rect.top
class BossPlatform(Entity):
    def __init__(self,type_, pos,tset, *groups):
        super().__init__(Color("#DDDDDD"), pos, *groups)
        self.type = 0
        self.tset = tset
        if type_ == 0:
            self.image = self.tset[9][15]
        elif type_ == 1:
            self.image = Surface((TILE_SIZE, TILE_SIZE),pygame.SRCALPHA)
            self.type = 1
        elif type_ == 2:
            self.image = self.tset[0][17]
        elif type_ == 3:
            self.image = self.tset[0][18]
        elif type_ == 4:
            self.image = self.tset[0][19]
        elif type_ == 5:
            self.image = self.tset[1][14]
        elif type_ == 6:
            self.image = self.tset[1][15]
        elif type_ == 7:
            self.image = self.tset[1][16]
        elif type_ == 8:
            self.image = self.tset[3][14]
        elif type_ == 9:
            self.image = self.tset[3][15]
        elif type_ == 10:
            self.image = self.tset[3][16]
class MovilPlatform(Entity):
    def __init__(self, pos,tset, *groups):
        super().__init__(Color("#DDDDDD"), pos, *groups)
        self.type = 0
        self.tset = tset
        self.imagen=tset[6][3]
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0], pos[1])
        self.rect.height = TILE_SIZE
        self.rect.width = TILE_SIZE
        self.hitbox=self.rect.inflate(0,-8)
        self.hitbox.top=self.rect.top

class CreateMap1(Entity):
    def __init__(self,type_, pos,tset, *groups):
        super().__init__(Color("#DDDDDD"), pos, *groups)
        self.type = 0
        self.tset = tset
        if type_ == 0:#TO COL-DOWN
            self.image = self.tset[6][0]
        elif type_ == 1:#TO COL-MIDDLE
            self.image=self.tset[7][5]
        elif type_ == 2:#TO COL-UP
            self.image=self.tset[7][4]
        elif type_ == 3:
            self.image = self.tset[5][6]
        elif type_ == 4:
            self.image = self.tset[5][7]
        elif type_ == 5:  #
            self.image = self.tset[5][10]
        elif type_ == 6:
            self.image = self.tset[6][6]
        elif type_ == 7:
            self.image = self.tset[6][7]
        elif type_ == 8:#
            self.image = self.tset[6][12]
        self.rect = self.image.get_rect()
        self.rect.topleft=(pos[0],pos[1])
        self.rect.height = TILE_SIZE
        self.rect.width = TILE_SIZE
class CreateMap(Entity):
    def __init__(self,type_, pos,tset, *groups):
        super().__init__(Color("#DDDDDD"), pos, *groups)
        self.type = 0
        self.tset = tset
        if type_ == 0:#TO COL-DOWN
            self.image = self.tset[6][0]
        elif type_ == 1:#TO COL-MIDDLE
            self.image=self.tset[7][5]
        elif type_ == 2:#TO COL-UP
            self.image=self.tset[7][4]
        elif type_ == 3:#TO COL-UP-DAMAGED
            self.image=self.tset[8][4]
        elif type_ == 4:#TO COL-DOWN-DAMAGED
            self.image=self.tset[8][5]
        elif type_== 5:#CHAINS
            self.image=self.tset[9][2]
        elif type_== 6:#CHAINS BOSS
            self.image=self.tset[8][18]
        elif type_== 7:#CHAINS BOSS
            self.image=self.tset[9][18]
        elif type_== 8:#CHAINS BOSS
            self.image=self.tset[0][12]
        elif type_== 9:#CHAINS BOSS
            self.image=self.tset[1][12]
        elif type_== 10:#CHAINS BOSS
            self.image=self.tset[2][12]

        self.rect = self.image.get_rect()
        self.rect.topleft=(pos[0],pos[1])
        self.rect.height = TILE_SIZE
        self.rect.width = TILE_SIZE
class HitItems(Entity):
    def __init__(self,type_, pos,tset, *groups):
        super().__init__(Color("#DDDDDD"), pos, *groups)
        self.type = type_
        self.tset = tset
        if type_ == 0:#LAVA
            self.image = self.tset[9][5]
        elif type_ == 1:#PEAKS UP
            self.image=self.tset[6][2]
        elif type_ == 2:#PEAKS DOWN
            self.image=self.tset[8][3]
        elif type_ == 3:#PEAKS LEFT
            self.image=self.tset[8][2]
        elif type_ == 4:#PEAKS RIGHT
            self.image = self.tset[8][1]
        elif type_ == 5: #PU Boss
            self.image = self.tset[10][20]
        elif type_ == 6: #PD Boss
            self.image = self.tset[10][21]
        elif type_ == 7: #PR Boss
            self.image = self.tset[9][21]
        elif type_ == 8: #PL Boss
            self.image = self.tset[8][21]
        self.rect = self.image.get_rect(center = (pos[0]+8,pos[1]+8))
        self.rect.height = TILE_SIZE-8
        self.rect.width = TILE_SIZE-8
class ExitBlock(Platform):
    def __init__(self, pos, *groups):
        super().__init__(Color("#0033FF"), pos, *groups)
class Display(pygame.sprite.Sprite):
    def __init__(self,string,screen,size):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, size)
        self.image = self.font.render(string, 0, (255, 0, 255),screen)

    def update(self, string,screen):
        self.image = self.font.render(string, 0, (255, 0, 255),screen)
class Status(Display):
    def __init__(self,type_,screen,cant=0,size=16):
        super().__init__("",screen,size)
        self.font = pygame.font.Font(None, size)
        assets = SS_ITEM["items"]
        if type_ == 0:
            self.icon = assets[4][9]
        elif type_ == 1:
            self.icon = assets[18][3]
        elif type_ == 2:
            self.icon = assets[3][14]
        elif type_ == 3:
            self.icon = assets[0][4]
        elif type_ == 4:
            self.icon = assets[13][1]
        elif type_ == 5:
            self.icon = assets[13][3]
        text = "x"+str(cant)
        self.cant = self.font.render(text, 0, (255, 0, 255),screen)
        self.image = self.icon
        self.images = 1

    def update(self, cant,screen):
        self.images = cant
        text = "x"+str(cant)
        self.cant = self.font.render(text, 0, (255, 0, 255),screen)

#Para Menu Principal
def objetotext(text,color,tam):
    if tam == "pequeño":
        textSurface = pequenafuente.render(text, True, color)
    if tam == "mediano":
        textSurface = medianafuente.render(text, True, color)
    if tam == "grande":
        textSurface = grandefuente.render(text, True, color)
    return textSurface,textSurface.get_rect()
def textboton(msg,color,botonx,botony,ancho,alto,tamaño="pequeño"):
    textSurface,textRect = objetotext(msg,color,tamaño)
    textRect.center = (botonx+(ancho/2),botony+(alto/2))
    screen.blit(textSurface,textRect)
def message(msg,color,desy,desx,tam="mediano"):
    textSurface, textRect = objetotext(msg, color, tam)
    textRect.center = ((WIN_WIDTH / 2)+desx, desy + (WIN_HEIGHT / 2))
    screen.blit(textSurface, textRect)
def prev():

    prev1 = pygame.image.load('Dg/textprev1.png')
    prev2 = pygame.image.load('Dg/textprev2.png')
    prev3 = pygame.image.load('Dg/textprev3.png')
    prev4 = pygame.image.load('Dg/textprev4.png')

    fin_prev=False
    cont_p=0

    while not fin_prev:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin_prev = True
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    cont_p += 1
                if event.key == pygame.K_a:
                    fin_prev = True
                    main()

        if cont_p == 0:
            screen.fill(negro)
            screen.blit(prev1,[30,100])
            pygame.display.update()

        elif cont_p == 1:
            screen.fill(negro)
            screen.blit(prev2,[30,100])
            pygame.display.update()

        elif cont_p == 2:
            screen.fill(negro)
            screen.blit(prev3,[30,100])
            pygame.display.update()

        elif cont_p == 3:
            screen.fill(negro)
            screen.blit(prev4,[30,100])
            pygame.display.update()

        elif cont_p == 4:
            screen.fill(negro)
            pygame.display.update()
            main()
def creditos():

    cred = pygame.image.load('Dg/creditos.png')

    fin_cred = False
    cont_c = 0

    while not fin_cred:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin_cred = True
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    fin_cred = True
                    introMenu()

            screen.blit(bgBoss,[0,0])
            screen.blit(cred,[10,10])
            pygame.display.update()

def botones(text,surface,state,pos,tam,id=None):
    global DIFFICULTY
    cursor = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if pos[0] + tam[0] > cursor[0] > tam[0] and pos[1] + tam[1] > cursor[1] > tam[1] and pos[1] + tam[1] < cursor[1] + tam[1]:
        if click[0] == 1:
            if id == "start":
                MenuDif()
            elif id == "exit":
                raise SystemExit
            elif id == "credits":
                creditos()
            elif id == "1":
                DIFFICULTY=0
                prev()
            elif id == "2":
                DIFFICULTY=1
                prev()
            elif id == "3":
                DIFFICULTY=2
                prev()
        boton = pygame.draw.rect(surface,state[1],(pos[0],pos[1],tam[0],tam[1]))
    else:
        boton = pygame.draw.rect(surface, state[0], (pos[0], pos[1], tam[0], tam[1]))
    textboton(text,negro,pos[0],pos[1],tam[0],tam[1])
    return boton
def MenuDif():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                return

        # imagen del Juego
        screen.blit(bgBoss, [0, 0])
        # Botones Inicio
        message("DIFICULTAD",plomo,-70, 0)
        botones("Facil", screen, colorboton, (boton1[0]-150,boton1[1]), tamboton, id="1")
        botones("Normal", screen, colorboton, (boton2[0]-150,boton2[1]), tamboton, id="2")
        botones("Dificil", screen, colorboton, (boton3[0]-150,boton3[1]), tamboton, id="3")
        pygame.display.update()
def introMenu():
    intro=True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro=False
                return

        #imagen del Juego
        fondo=pygame.image.load('Dg/adv.png')
        fondo2=pygame.image.load('Dg/overcrawl_text.png')
        screen.blit(bgBoss,[0,0])
        screen.blit(fondo,[0,0])
        screen.blit(fondo2,[320,85])
        #Botones Inicio
        #message("OVERCRAWL",plomo,-70, 150)
        botones("Iniciar",screen,colorboton,boton1,tamboton,id="start")
        botones("Creditos", screen, colorboton, boton2, tamboton,id="credits")
        botones("Salir", screen, colorboton, boton3, tamboton,id="exit")
        pygame.display.update()

if __name__ == "__main__":
    introMenu()

