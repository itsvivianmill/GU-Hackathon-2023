import pygame 
import worldRender
import tileset
import playerObj
import random
import bullet
import time
import math
import home
from homepagebutton import homepageButtons
from pygame import mixer
#init
gameState="Start"
screen = pygame.display.set_mode((600, 600)) 
pygame.display.set_caption("Menu -> Time to Duck it Up!")
pygame.init()
tileMapAssetList = [
    r"asset\mapTiles\grass.png",            #0
    r"asset\mapTiles\grassFlower.png",      #1
    r"asset\mapTiles\grassFlower2.png",     #2
    r"asset\mapTiles\grassTree.png",        #3
    r"asset\mapTiles\rock.png",             #4
    r"asset\mapTiles\water.png",            #5
    r"asset\mapTiles\boderbottom.png",      #6
    r"asset\mapTiles\borderleft.png",       #7
    r"asset\mapTiles\borderright.png",      #8
    r"asset\mapTiles\bordertop.png",        #9
    r"asset\mapTiles\cornertopright.png",   #10
    r"asset\mapTiles\cornertopleft.png",    #11
    r"asset\mapTiles\cornerbottomright.png",#12
    r"asset\mapTiles\cornerbottomleft.png", #13
    r"asset\mapTiles\watertipleft.png",     #14
    r"asset\mapTiles\watertipright.png",     #15
    r"asset\mapTiles\littlewaterbottomleftTip.png", #16
    r"asset\mapTiles\littlewaterbottomrightTip.png",#17
    r"asset\mapTiles\bottomTreeBorder.png",         #18
    r"asset\mapTiles\leftTreeBorder.png",           #19
    r"asset\mapTiles\rightTreeBorder.png",          #20
    r"asset\mapTiles\treecorner.png",              #21
    r"asset\mapTiles\middleTree.png",              #22
    r"asset\mapTiles\topTreeBorder.png", #23
    r"asset\mapTiles\toprightcorner.png", #24
    r"asset\mapTiles\bottomleftborder.png", #25
    r"asset\mapTiles\topleftcorner.png", #26
]

duckAssetList = [
    r"asset\duck\standfront.png", #0
    r"asset\duck\right1.png",
    r"asset\duck\right2.png",
    r"asset\duck\left1.png",
    r"asset\duck\left2.png",
    r"asset\duck\backwalk1.png",
    r"asset\duck\backwalk2.png",
    r"asset\duck\frontwalk1.png",
    r"asset\duck\frontwalk2.png",
    r"asset\duck\gunleft.png",
    r"asset\duck\gunright.png",
    r"asset\duck\gunback.png",
    r"asset\duck\gunforward.png"
]

enemyAsset = [
    r"asset\enemy\idle1.png",
    r"asset\enemy\idle2.png",
    r"asset\enemy\idle3.png",
    r"asset\enemy\deadvillain.png"
]

tilemap = tileset.tileset(tileMapAssetList)
duckTileMap = tileset.tileset(duckAssetList)
enemyTileMap = tileset.tileset(enemyAsset)
bulletTile = tileset.tileset([r"asset\duck\bullet.png"])

duck = playerObj.duck(duckTileMap)
bulletPool =[]
enemyPool = []
worldObj = worldRender.world(25,25,32,32,tilemap)
worldObj.loadTileMap("map.txt")
running = True

for i in range(8):
    enemyPool.append(playerObj.enemy(enemyTileMap))
    enemyPool[len(enemyPool)-1].x = random.randint(20,700)
    enemyPool[len(enemyPool)-1].y = random.randint(20,700)
deltaT = 0.1
start = 0
#start music
mixer.init()
mixer.Channel(0).set_volume(1)
mixer.Channel(0).play(pygame.mixer.Sound(r"cottagecore.mp3"),loops=-1)
#main loop
Score = 0
while running:  
    start = time.time()
    for event in pygame.event.get():    
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and gameState=="Run":
            w, h = pygame.display.get_surface().get_size()
            mpos = pygame.mouse.get_pos()
            dirX = (w/2-16) - mpos[0]
            dirY = (h/2-16-10) - mpos[1]
            print(mpos,duck.x,duck.y)
            length = math.sqrt(dirX**2+dirY**2)
            dirX/=-length
            dirY/=-length
            bulletPool.append(bullet.bullet(duck.x,duck.y-10,dirX,dirY,bulletTile))
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("a")
            if home.PLAY_Button.checkForInput(pygame.mouse.get_pos()):
                print("aa")
                gameState="Run"
            if home.QUIT_Button.checkForInput(pygame.mouse.get_pos()):
                pygame.quit()
                quit()
    
    if gameState=="Run":
        w, h = pygame.display.get_surface().get_size()
        duck.playerMove(deltaT)
        #background = pygame.image.load(r"asset\mapTiles\1600middleTree.png")
        #backgroundrect=background.get_rect()
        #backgroundrect.x = (-duck.x)*(w/300)
        #backgroundrect.y = (-duck.y)*(h/300)
        screen.fill((0,0,0))
        #screen.blit(background, backgroundrect)
        worldObj.renderSelf(screen,w/300,duck)
        for i in enemyPool:
            i.renderSelf(screen,w/300,duck)
            if i.DeadTimer<=0:
                enemyPool.remove(i)

        for i in bulletPool:
            i.bulletUpdate(deltaT)
            i.bulletCheckCollide(enemyPool,duck,w/300)
            i.renderSelf(screen,w/300,duck)
            if i.lifeTime <= 0:
                Score+=1
                print(Score)
                bulletPool.remove(i)
                if (len(enemyPool)<5):
                    enemyPool.append(playerObj.enemy(enemyTileMap))
                    enemyPool[len(enemyPool)-1].x = random.randint(20,700)
                    enemyPool[len(enemyPool)-1].y = random.randint(20,700)
                print(len(enemyPool))
        duck.playerRender(screen,w/300)
    elif gameState=="Start":
        home.draw_start_menu(screen)
        

    pygame.display.update()

    deltaT = time.time() - start
    start = time.time()