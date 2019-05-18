
import pygame
import string
from pathlib import Path
from pygamegame import PygameGame
from GameObject import GameObject
from GameState1 import *
from GameState2 import *
from GameState3 import *
from GameBegin import *
from GameEnd import *
from GameFail import *

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)
        
def runGame():
    
    data = [0,0,0,0,0]
    screen = pygame.display.set_mode((800, 600))
    i = 0
    while(1):
        if i == 0:
            state = GameBegin(800, 600)
        if i == 1:
            state = GameState1(800,600)
        if i == 2:
            state = GameState2(800,600);  state.energ = energ
        if i == 3:
            state = GameState3(800,600);  state.energ = energ
        if i == 4:
            state = GameEnd(800,600)
            data[4] = (data[1]+data[2])*data[3]
            print(data)
            #check exists
            Gamedatafile = Path("Gamedata.txt")
            if not Gamedatafile.exists():
                rank = 1
                data.append(rank)
                writeFile("Gamedata.txt", str(data)+"\n")
            else:
                #rank calculate
                rankcnt = 0
                totalcnt = 0
                recordlst = readFile("Gamedata.txt")
                for record in recordlst.split("\n"):
                    record = record.strip("[").strip("]")
                    totalcnt += 1
                    if record.split(",")[-1]!="" and data[4] >= float(record.split(",")[4]):
                        rankcnt += 1     
                rank = totalcnt - rankcnt
                data.append(rank)
                #data store
                recordlst += str(data) + "\n"
                writeFile("Gamedata.txt", recordlst)
                # contentsToWrite = str(data)
        if i == 5:
            state = GameFail(800,600)
    
        clock = pygame.time.Clock()
        # set the title of the window
        pygame.display.set_caption(state.title)
    
        # stores all the keys currently being held down
        state._keys = dict()
    
        # call game-specific initialization
        state.init()
        playing = True
        while playing:
            if state.GameResume:
                state.init(); state.GameResume = False;
                if i != 1: state.energ = energ
            if not state.GamePause: time = clock.tick(state.fps)
            if not state.GamePause:
                if i != 4: state.timerFired(time, screen)
                else: state.timerFired(time, screen, data)
            for event in pygame.event.get():            
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:      
                    state.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    state.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                        event.buttons == (0, 0, 0)):
                    state.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                        event.buttons[0] == 1):
                    state.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    state._keys[event.key] = True
                    state.keyPressed(event.key, event.mod)
                    keyP, keyR = 112, 114
                    if(event.key == keyP): state.GamePause = not(state.GamePause)
                    if(event.key == keyR): state.GameResume = True
                elif event.type == pygame.KEYUP:
                    state._keys[event.key] = False
                    state.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
                    state.Gameover = True
            
            if state.GamePause: continue
            screen.fill(state.bgColor)
            state.redrawAll(screen)
            pygame.display.flip()
            
            if state.GameStart:
                if   i == 0: i = 1
                elif i == 1: data[1] = state.score; i = 2; energ = state.energ
                elif i == 2: data[2] = state.score; i = 3; energ = state.energ
                elif i == 3: data[3] = state.energ; i = 4
                elif i == 4: i = 1
                elif i == 5: i = 1
                break                
            if state.GameHome: i = 0; break
            if state.Gameover: break
            if state.Gamelose: i = 5; break
        if state.Gameover:
            pygame.quit(); break

runGame()



