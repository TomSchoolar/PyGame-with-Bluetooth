import pygame
import time
import random
from nxt.bluesock import BlueSock
from nxt.sensor import *
from nxt.motor import *

ID = '00:16:53:12:47:F3'

sock = BlueSock(ID)
brick = sock.connect()
Mid=(Motor(brick,PORT_A).get_tacho().block_tacho_count)
print(Mid)
TriggerMid=(Motor(brick,PORT_B).get_tacho().block_tacho_count)
print(TriggerMid)

grey=(96,96,96)
bright_grey=(160,160,160)
red=(255,0,0)
orange=(255,128,0)

pygame.mixer.init()

Hit_Sound=pygame.mixer.Sound("Images/Hit_Sound.wav")

pygame.mixer.music.load("All Along the Watchtower.mp3")

pygame.mixer.music.play(-1)

screen_w=1900
screen_h=950

pygame.display.init()

info = pygame.display.Info()
screen_w = info.current_w
screen_h = info.current_h
screen=pygame.display.set_mode((screen_w,screen_h),pygame.RESIZABLE)

PlayerReady=pygame.image.load('Images/PlayerTrollRaised.png').convert_alpha()
EnemyReady=pygame.image.load('Images/EnemyTrollRaised.png').convert_alpha()
Player=pygame.image.load('Images/PlayerTroll.png').convert_alpha()
Enemy=pygame.image.load('Images/EnemyTroll.png').convert_alpha()

Float_Height=(screen_h/4)*3
Float_Height=round(Float_Height)
Height=int(Float_Height)

PlayerReady=pygame.transform.scale(PlayerReady,(int(Height/2),Height))
EnemyReady=pygame.transform.scale(EnemyReady,(int(Height/2),Height))
Player=pygame.transform.scale(Player,(int(Height/2),Height))
Enemy=pygame.transform.scale(Enemy,(int(Height/2),Height))

PlayerReady.set_colorkey(grey)
EnemyReady.set_colorkey(grey)
Player.set_colorkey(grey)
Enemy.set_colorkey(grey)

Logo=pygame.image.load('Images/Logo.png')
pygame.display.set_icon(Logo)

Background=pygame.image.load('Images/DungeonPicHigherRes.png').convert()
Background=pygame.transform.scale(Background,(screen_w,screen_h))

Top=''
Med=''
Bot=''

Attack=False
Menu=True
Health=5
Fish=0
Option=0
Level=4
EnemyHealth=5
Dodge=2
Person_Place=0
Player_y=(screen_h/12)*3
Paused=False
OriginalEnemyHealth=EnemyHealth
OriginalPlayerHeath=Health

FirstLetter='a'
SecondLetter='b'
LastLetter='c'

def Draw_Line(LineStartx,LineStarty,LineEndx,LineEndy,color):
    global screen
    LineStart=(LineStartx,LineStarty)
    LineEnd=(LineEndx,LineEndy)
    pygame.draw.line(screen,color,LineStart,LineEnd)
    return

def Draw_Rectangle(Rectx,Recty,Rectw,Recth,color):
    global screen
    pygame.draw.rect(screen,color,[Rectx,Recty,Rectw,Recth])
    return

def Write_Draw(msg,xcord,ycord,size):
    global screen
    global bright_grey
    global grey
    myfont = pygame.font.SysFont("twcencondensed",size)
    if msg=='Health: 1'or msg=='Enemy Health: 1'or msg=='Health: 2'or msg=='Enemy Health: 2'or msg=='Health: 0'or msg=='Enemy Health: 0':
        if msg=='Health: 1'or msg=='Enemy Health: 1'or msg=='Health: 0'or msg=='Enemy Health: 0':
            mytext = myfont.render(msg, True, red)
        if msg=='Health: 2'or msg=='Enemy Health: 2':
            mytext = myfont.render(msg, True, orange)
    else:
        mytext = myfont.render(msg, True, bright_grey)
    mytext = mytext.convert_alpha()
    xchange=mytext.get_width()
    xchange=xchange/2
    ychange=mytext.get_height()
    ychange=ychange/2
    if msg=='Quit' or msg=='Begin':
        Draw_Rectangle((xcord-xchange)-30,ycord-ychange,mytext.get_width()+60,mytext.get_height(),grey)
    else:
        Draw_Rectangle(xcord-xchange,ycord-ychange,mytext.get_width(),mytext.get_height(),grey)
    screen.blit(mytext,(xcord-xchange,ycord-ychange))
    pygame.display.flip()
    return

def Start_Menu_Setup():
    global OriginalEnemyHealth
    global OriginalPlayerHeath
    global Health
    global EnemyHealth
    global Level
    global Fish
    global Attack
    global Background
    global Menu
    global mainloop
    global Option
    global FirstLetter
    global SecondLetter
    global LastLetter
    Attack=False
    Menu=True
    mainloop=True
    pygame.init()
    pygame.display.set_caption("Troll Civil War")
    screen.blit(Background, (0,0))
    Write_Draw("Troll Civil War!",screen_w/2,screen_h/4,150)
    Write_Draw("- Begin -",screen_w/2,screen_h/4+screen_h/4,75)
    Write_Draw("Quit",screen_w/2,screen_h/2+screen_h/8,75)
    Write_Draw("Show game Controls (SPACE)",210,50,50)
    FirstLetter='a'
    SecondLetter='b'
    LastLetter='c'
    Health=OriginalPlayerHeath
    EnemyHealth=OriginalEnemyHealth
    Level=4
    Fish=0
    return

def Attacking(Changeable):
    global screen
    global Background
    global screen_h
    global screen_w
    global PlayerReady
    global Player
    global Enemy
    global EnemyReady
    global Health
    global EnemyHealth
    global Fish
    global Dodge
    global Player_y
    EnemyAttacking=''
    PlayerAttacking=''
    if Changeable==Player:
        PlayerAttacking=Changeable
        EnemyAttacking=EnemyReady
    if Changeable==Enemy:
        Changeable.set_colorkey(grey)
        EnemyAttacking=Changeable
        PlayerAttacking=PlayerReady
    pygame.display.flip()
    screen.blit(Background, (0,0))
    screen.blit(PlayerReady,(screen_w/Dodge - PlayerReady.get_width(),Player_y))
    screen.blit(EnemyReady,(screen_w/2,Player_y))
    Write_Draw("Health: "+str(Health),100,50,50)
    Write_Draw("Fish: "+str(Fish),100,100,50)
    Write_Draw("Enemy Health: "+str(EnemyHealth),screen_w-150,50,50)
    time.sleep(0.2)
    pygame.display.flip()
    screen.blit(Background, (0,0))
    screen.blit(PlayerAttacking,(screen_w/Dodge - PlayerReady.get_width(),Player_y))
    screen.blit(EnemyAttacking,(screen_w/2,Player_y))
    Write_Draw("Health: "+str(Health),100,50,50)
    Write_Draw("Fish: "+str(Fish),100,100,50)
    Write_Draw("Enemy Health: "+str(EnemyHealth),screen_w-150,50,50)
    pygame.mixer.Sound.play(Hit_Sound)
    time.sleep(0.2)
    pygame.display.flip()
    screen.blit(Background, (0,0))
    screen.blit(PlayerReady,(screen_w/Dodge - PlayerReady.get_width(),Player_y))
    screen.blit(EnemyReady,(screen_w/2,Player_y))
    Write_Draw("Health: "+str(Health),100,50,50)
    Write_Draw("Fish: "+str(Fish),100,100,50)
    Write_Draw("Enemy Health: "+str(EnemyHealth),screen_w-150,50,50)
    return

def Enemy_Attack():
    global Level
    global Health
    global Enemy
    YesOrNo=random.randint(0,Level)
    if YesOrNo==1:
        Attacking(Enemy)
        if Dodge==2:
            Health=Health-1
    return

def AttackMovment():
    global Health
    global Fish
    global EnemyHealth
    global Background
    global screen
    global screen_h
    global screen_w
    global Player
    global PlayerReady
    global EnemyReady
    global Attack
    pygame.display.flip()
    if Attack==True:
        Attacking(Player)
        Attack=False
        EnemyHealth=EnemyHealth-1
        if EnemyHealth==0:
            Health=OriginalPlayerHeath
            Fish=Fish+1
            EnemyHealth=OriginalEnemyHealth+Fish
            Write_Draw("Next Round!",screen_w/2,screen_h/2,200)
            time.sleep(2)
            pygame.display.flip()
            Game_loop()
    else:
        pygame.display.flip()
        Enemy_Attack()
    return

def Game_loop():
    global screen
    global screen_h
    global screen_w
    global Background
    global PlayerReady
    global EnemyReady
    global Fish
    global Health
    global EnemyHealth
    global Level
    global Player_y
    screen.blit(Background, (0,0))
    screen.blit(PlayerReady,(screen_w/2 - PlayerReady.get_width(),Player_y))
    screen.blit(EnemyReady,(screen_w/2,Player_y))
    Write_Draw("Health: "+str(Health),100,50,50)
    Write_Draw("Fish: "+str(Fish),100,100,50)
    Write_Draw("Enemy Health: "+str(EnemyHealth),screen_w-150,50,50)
    pygame.display.flip()
    if Fish!=0:
        Level=3
    if Fish!=0 and Fish!=1:
        Level=2
    if Fish>2:
        Level=1
    if Health !=0:
        AttackMovment()
    else:
        Write_Draw("Defeated",screen_w/2,screen_h/2,200)
        time.sleep(3)
        Start_Menu_Setup()
    return

def Pause():
    global mainloop
    global Paused
    global Background
    global screen
    global screen_h
    global screen_w
    screen.blit(Background,(0,0))
    pygame.mixer.music.pause()
    Write_Draw("Paused",screen_w/2,screen_h/2,200)
    while Paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
                Paused = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
                    Paused = False
                if Touch(brick, PORT_4).get_sample() == True:
                    Paused = False
                    pygame.mixer.music.unpause()
                    Game_loop()
    return

Start_Menu_Setup()

mainloop = True

while mainloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False
            if Menu:
                while True:
                    if Option==0:
                        Current=(Motor(brick,PORT_A).get_tacho().block_tacho_count)
                        print("a:"+str(Current)+",mid:"+str(Mid))
                        pygame.display.flip()
                        if Current<Mid:
                            Option=Option+1
                            screen.blit(Background, (0,0))
                            Write_Draw("Troll Civil War!",screen_w/2,screen_h/4,150)
                            Write_Draw("Begin",screen_w/2,screen_h/4+screen_h/4,75)
                            Write_Draw("- Quit -",screen_w/2,screen_h/2+screen_h/8,75)
                            Write_Draw("Show game Controls (SPACE)",210,50,50)
                        CurrentT=(Motor(brick,PORT_B).get_tacho().block_tacho_count)
                        print("b:"+str(CurrentT)+",mid:"+str(TriggerMid))
                        if CurrentT>TriggerMid:
                            pygame.display.flip()
                            Menu=False
                            break
                            Game_loop()
                    else:
                        Current=(Motor(brick,PORT_A).get_tacho().block_tacho_count)
                        print("a:"+str(Current)+",mid:"+str(Mid))
                        pygame.display.flip()
                        if Current>Mid:
                            Option=Option-1
                            screen.blit(Background, (0,0))
                            Write_Draw("Troll Civil War!",screen_w/2,screen_h/4,150)
                            Write_Draw("- Begin -",screen_w/2,screen_h/4+screen_h/4,75)
                            Write_Draw("Quit",screen_w/2,screen_h/2+screen_h/8,75)
                            Write_Draw("Show game Controls (SPACE)",210,50,50)
                        CurrentT=(Motor(brick,PORT_B).get_tacho().block_tacho_count)
                        print("b:"+str(CurrentT)+",mid:"+str(TriggerMid))
                        pygame.display.flip()
                        if CurrentT>TriggerMid:
                            mainloop = False
                            break
                    if Touch(brick, PORT_4).get_sample() == True:
                        screen.blit(Background, (0,0))
                        pygame.mixer.Sound.play(Hit_Sound)
                        Write_Draw("Game Controls",screen_w/2,screen_h/10,100)
                        Write_Draw("Joystick - Up/Down",screen_w/2,(screen_h/10)*3,50)
                        Write_Draw("Escape - Quit",screen_w/2,(screen_h/10)*4,50)
                        Write_Draw("Trigger - Select",screen_w/2,(screen_h/10)*5,50)
                        Write_Draw("Exit (Joystick)",screen_w/4*3,(screen_h/10)*8,75)
                        Write_Draw("+ Button - Toggle Pause",screen_w/2,(screen_h/10)*6,50)
                        Write_Draw("I Button - Attack",screen_w/2,(screen_h/10)*7,50)
            else:
                while True:
                    if Health<0:
                        break
                        Game_loop()
                    if Touch(brick, PORT_3).get_sample() == True:
                        Attack = True
                        Game_loop()
                    if EnemyHealth!=10:
                        Enemy_Attack()
                    if Touch(brick, PORT_4).get_sample() == True:
                        if Health != 0:
                            Paused = True
                            Pause()
    pygame.display.flip()
pygame.quit()
sock.close()
