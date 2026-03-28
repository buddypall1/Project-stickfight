import tkinter
from tkinter import ttk
import tkinter.messagebox
import pickle
from PIL import Image, ImageTk
import random
import pygame


pygame.mixer.init()

saveloc = "Data/game_data.dat"
playerturn = True
playerstatuslabel = None
enemystatuslabel = None
def loadData():
    try:
        with open(saveloc, 'rb') as file:
            data = pickle.load(file)
        return data
    except (FileNotFoundError, EOFError, pickle.UnpicklingError, ImportError, MemoryError):
        tkinter.messagebox.showerror("Data Error", "Couldn't load save data, reverting to defaults.")
        return {
        "Playerhealth" : 100,
        "Playerdmg" : 5,
        "Playerweap" : "None",
        "Enemhealth" : 100,
        "Enemdmg" : 5,
        "Enemweap" : "None",
        "Enemrng" : 50,
        "musicon" : "True",
        "audioOn" : "True",
        "PlayerName" : None
        }


gamedata = loadData()

player_name = gamedata.get("PlayerName", None)

def ask_for_name():
    global player_name
    menowindow = tkinter.Tk()
    menowindow.title("Ahoj!")
    menowindow.resizable(0, 0)
    menowindow.geometry("350x150")

    tkinter.Label(menowindow, text="Nastav si prosím meno:", font=('Arial', 13)).pack(pady=15)
    name_entry = tkinter.Entry(menowindow, font=('Arial', 12))
    name_entry.pack()

    def confirm():
        global player_name
        name = name_entry.get().strip()
        if name:
            player_name = name
            menowindow.destroy()
        else:
            tkinter.messagebox.showwarning("Ziadne meno!", "Nezadal si si meno..", parent=menowindow)

    tkinter.Button(menowindow, text="Confirm", command=confirm).pack(pady=10)
    menowindow.mainloop()

if not player_name:
    ask_for_name()

musicon = gamedata['musicon']
audioOn = gamedata['audioOn']
pygame.mixer.music.load("Media/audio/Test Instrumental - Friday Night Funkin.mp3")
if musicon == False:
    pass
else:
    pygame.mixer.music.play(loops=-1)

#### window creation start ####
window = tkinter.Tk()
def disable_event():
   pass
window.protocol("WM_DELETE_WINDOW", disable_event)
window.title("TmEsg")
window.resizable(0, 0)
window.geometry("950x700")
#### window creation end ####

class Playerparams():

    def __init__(self, zivot, damage, weapon,healovanieamm):
        self.zivot = zivot
        self.damage = damage
        self.weapon = weapon
        self.healovanieamm= healovanieamm
    
    def __str__(self):
        return f'{self.weapon} {self.damage} {self.weapon}'

class Enemparams():

    def __init__(self, zivot, damage, rng, weapon,healovanieamm):
        self.zivot= zivot
        self.damage = damage
        self.rng = rng
        self.weapon = weapon
        self.healovanieamm= healovanieamm

class LevelEnemparams():

    def __init__(self,zivot,damage,rng,weapon,healovanieamm,defense):
        self.zivot = zivot
        self.damage = damage
        self.rng = rng
        self.weapon = weapon
        self.healovanieamm = healovanieamm
        self.defense = defense

class LevelPlayerparams():

    def __init__(self, zivot, damage, weapon,healovanieamm,defense):
        self.zivot = zivot
        self.damage = damage
        self.weapon = weapon
        self.healovanieamm = healovanieamm
        self.defense = defense

#### uzivatel a nepriatel obj creation #### 

uzivatel = Playerparams(gamedata['Playerhealth'], gamedata['Playerdmg'], gamedata['Playerweap'],1) # CUSTOM GAME PLAYER!!! last line is healovanieamm placeholder
nepriatel = Enemparams(gamedata['Enemhealth'], gamedata['Enemdmg'], gamedata['Enemrng'], gamedata['Enemweap'], 1) # CUSTOM GAME ENEMY!!! last line is healovanieamm placeholder

##################################
###       BATTLE LOGIC         ###
##################################

def bojokno(nepriatel, uzivatel):
    global uzivatelovekolo
    global fightbutton, defendbutton, itembutton, skipturnbutton
    global uzivatelzivotlabel, nepriatelzivotstatus
    global bojoveokno
    global pomockylabel
    global UzivatelObranuje
    global kololabelinteger
    global kololabel
    global uzivatelstatuslabel, nepriatelstatuslabel, uzivatelsprite, uzivatelspritelabel, nepriatelsprite, nepriatelspritelabel

    battle_player = type(uzivatel)(*vars(uzivatel).values())
    battle_enemy = type(nepriatel)(*vars(nepriatel).values())

    bojoveokno = tkinter.Toplevel(window)
    bojoveokno.title("Battle!")
    bojoveokno.resizable(0, 0)
    bojoveokno.geometry("1080x600")
    bojoveokno.update_idletasks()
    bojoveokno.geometry(f"1080x600+{window.winfo_x() + (window.winfo_width() - 1080) // 2}+{window.winfo_y() + (window.winfo_height() - 600) // 2}")


    kololabelinteger = 1
    kololabel = tkinter.Label(bojoveokno, text=f"KOLO: {kololabelinteger}", font=('Arial', 20, 'bold'))
    kololabel.place(x=540, y=20, anchor='center')


    uzivatelzivotlabel = tkinter.Label(bojoveokno, text=f"HP: {uzivatel.zivot}", font=('Arial', 10, 'bold'))
    uzivatelzivotlabel.place(x=250, y=70, anchor='center')


    uzivatelstatuslabel = tkinter.Label(bojoveokno, text="", font=('Arial', 14, 'bold'))
    uzivatelstatuslabel.place(x=225, y=95, anchor='center')

    uzivatelsprite = tkinter.PhotoImage(file="Media/uzivatelsprite.png")
    uzivatelspritelabel = tkinter.Label(bojoveokno, image=uzivatelsprite)
    uzivatelspritelabel.place(x=200, y=110)
    uzivatelspritelabel.image = uzivatelsprite
    namelabel = tkinter.Label(bojoveokno, text=player_name, font=('Arial', 10, 'bold'))
    namelabel.place(x=200 + (uzivatelsprite.width() // 2), y=90, anchor='center')

    nepriatelzivotstatus = tkinter.Label(bojoveokno, text=f"HP: {nepriatel.zivot}", font=('Arial', 10, 'bold'))
    nepriatelzivotstatus.place(x=860, y=70, anchor='center')

    nepriatelmeno = tkinter.Label(bojoveokno, text="Nepriateľ", font=('Arial', 10, 'bold'))
    nepriatelmeno.place(x=860, y=90, anchor='center')

    nepriatelsprite = tkinter.PhotoImage(file="Media/nepriatelsprite.png")
    nepriatelspritelabel = tkinter.Label(bojoveokno, image=nepriatelsprite)
    nepriatelspritelabel.place(x=800, y=110)
    nepriatelspritelabel.image = nepriatelsprite

    UIvs = tkinter.Label(bojoveokno, text="VS", font=('Arial', 50, 'bold'))
    UIvs.place(x=540, y=220, anchor='center')


    tkinter.Frame(bojoveokno, height=2, bg='black').place(x=0, y=420, width=1080)

    fightbutton = tkinter.Button(bojoveokno, text="Útoč", background='grey', height=2, width=21, command=lambda: UzivatelUtoc(battle_player, battle_enemy))
    fightbutton.place(x=270, y=450, anchor='center')

    itembutton = tkinter.Button(bojoveokno, text="Použi bonus", background='grey', height=2, width=21, command=lambda: UzivatelBonus(battle_player))
    itembutton.place(x=450, y=450, anchor='center')

    defendbutton = tkinter.Button(bojoveokno, text="Obránenie", background='grey', height=2, width=21, command=lambda: UzivatelObrana(battle_player))
    defendbutton.place(x=630, y=450, anchor='center')

    skipturnbutton = tkinter.Button(bojoveokno, text="Preskoč kolo", background='grey', height=2, width=21, command=lambda: UzivatelPreskoc(battle_player))
    skipturnbutton.place(x=810, y=450, anchor='center')

    pomockylabel = tkinter.Label(bojoveokno, text=f"Zostavajuce bonusy: {battle_player.healovanieamm}", font=('Arial', 10))
    pomockylabel.place(x=540, y=490, anchor='center')

    UzivatelObranuje = False
    uzivatelovekolo = True
    fightbutton.config(state="normal")
def UzivatelPreskoc(uzivatel):
    global uzivatelovekolo
    uzivatelovekolo = False
    buttonystatus("disabled")
    bojoveokno.after(1000, lambda: nepriatelutok(uzivatel, nepriatel))

def UzivatelObrana(uzivatel):
    global uzivatelovekolo
    global UzivatelObranuje
    if not uzivatelovekolo:
        return
    
    UzivatelObranuje = True
    uzivatelovekolo = False
    buttonystatus("disabled")
    bojoveokno.after(1000, lambda: nepriatelutok(uzivatel, nepriatel))


def UzivatelBonus(uzivatel):
    global uzivatelovekolo
    global uzivatelstatuslabel
    global uzivatelsprite
    if not uzivatelovekolo or uzivatel.healovanieamm == 0 or uzivatel.zivot == 100:
        return
    
    healsila = random.randint(1, 15)
    maximalnehealovanie = 100 - uzivatel.zivot
    healovanie = min(healsila, maximalnehealovanie)
    uzivatel.zivot += healovanie
    uzivatel.healovanieamm -= 1
    pomockylabel.config(text=f"Zostavajuce bonusy: {uzivatel.healovanieamm}")
    uzivatelzivotlabel.config(text=f"HP: {uzivatel.zivot}")
    uzivatelsprite.config(file="Media/uzivatelspriteheal.png")
    uzivatelstatuslabel.config(text=f"+{healovanie}", fg="green")
    bojoveokno.after(1000, lambda:uzivatelstatuslabel.config(text=""))
    uzivatelovekolo = False
    buttonystatus("disabled")
    bojoveokno.after(1000, lambda: uzivatelsprite.config(file="Media/uzivatelsprite.png"))
    bojoveokno.after(1000, lambda: nepriatelutok(uzivatel, nepriatel))

    

def UzivatelUtoc(uzivatel, nepriatel):
    global UzivatelObranuje
    global uzivatelovekolo
    global nepriatelstatuslabel, nepriatelsprite
    global sfxvar
    Zvukrandom = ""
    zvukrandomrng = random.randint(1,4)
    if sfxvar.get():
        if zvukrandomrng == 1:
            print("Pain1")
            Zvukrandom = pygame.mixer.Sound("Media/audio/pain1.mp3")
            Zvukrandom.play()
        elif zvukrandomrng == 2:
            print("Pain2")
            Zvukrandom = pygame.mixer.Sound("Media/audio/pain2.mp3")
            Zvukrandom.play()
        elif zvukrandomrng == 3:
            print("Pain3")
            Zvukrandom = pygame.mixer.Sound("Media/audio/pain3.mp3")
            Zvukrandom.play()
        elif zvukrandomrng == 4:
            print("Pain4")
            Zvukrandom = pygame.mixer.Sound("Media/audio/pain4.mp3")
            Zvukrandom.play()
    else: 
        pass
    UzivatelObranuje = False
    if not uzivatelovekolo:
        return


    utoksila = random.randint(1, uzivatel.damage)
    nepriatel.zivot -= utoksila
    nepriatelzivotstatus.config(text=f"HP: {nepriatel.zivot}")
    nepriatelstatuslabel.config(text=f"-{utoksila}", fg="red")
    nepriatelsprite.config(file="Media/nepriatelspritehit.png")
    bojoveokno.after(1000, lambda:nepriatelstatuslabel.config(text=""))
    print(f"Player attacks for {utoksila}")

    if nepriatel.zivot <= 0:
        tkinter.messagebox.showinfo("Výhra", "Vyhral si nad nepriateľom!")
        return
    bojoveokno.after(1000, lambda: nepriatelsprite.config(file="Media/nepriatelsprite.png"))
    uzivatelovekolo = False
    buttonystatus("disabled")

    bojoveokno.after(1000, lambda: nepriatelutok(uzivatel, nepriatel))


def nepriatelutok(uzivatel, nepriatel):
    global uzivatelovekolo
    global UzivatelObranuje
    global kololabelinteger
    global kololabel
    global uzivatelstatuslabel, uzivatelsprite, uzivatelspritelabel
    global sfxvar
    Zvukrandom = ""
    zvukrandomrng = random.randint(1,4)
    if sfxvar.get():
        if zvukrandomrng == 1:
            print("Pain1")
            Zvukrandom = pygame.mixer.Sound("Media/audio/pain1.mp3")
            Zvukrandom.play()
        elif zvukrandomrng == 2:
            print("Pain2")
            Zvukrandom = pygame.mixer.Sound("Media/audio/pain2.mp3")
            Zvukrandom.play()
        elif zvukrandomrng == 3:
            print("Pain3")
            Zvukrandom = pygame.mixer.Sound("Media/audio/pain3.mp3")
            Zvukrandom.play()
        elif zvukrandomrng == 4:
            print("Pain4")
            Zvukrandom = pygame.mixer.Sound("Media/audio/pain4.mp3")
            Zvukrandom.play()
    else: 
        pass
    print(f"{UzivatelObranuje}")
    if UzivatelObranuje == False:
        enemattackpow = random.randint(1, nepriatel.damage) 
    else:  
        enemattackpow = random.randint(1, nepriatel.damage // 2)
        print(f"Defending success! UzivatelObranuje={UzivatelObranuje}")

    uzivatel.zivot -= enemattackpow
    uzivatelzivotlabel.config(text=f"HP: {uzivatel.zivot}")
    uzivatelstatuslabel.config(text=f"-{enemattackpow}", fg="red")
    uzivatelsprite.config(file="Media/uzivatelspritehit.png")
    bojoveokno.after(1000, lambda: uzivatelstatuslabel.config(text=""))
    print(f"Enemy attacks for {enemattackpow}")


    if uzivatel.zivot <= 0:
        print("Player defeated!")
        tkinter.messagebox.showinfo("Defeat", "You were defeated!")
        bojoveokno.destroy()
        return
    bojoveokno.after(1000, lambda: uzivatelsprite.config(file="Media/uzivatelsprite.png"))
    uzivatelovekolo = True
    buttonystatus("normal")
    kololabelinteger += 1
    kololabel.config(text=f"KOLO:{kololabelinteger}")
    



def buttonystatus(state):
    fightbutton.config(state=state)
    defendbutton.config(state=state)
    itembutton.config(state=state)
    skipturnbutton.config(state=state)

#### UI buttons handling ####
def exitpressed():
    window.destroy()
    savedata()

    
def playpressed():
    global uzivatel, nepriatel

    playwindow = tkinter.Toplevel(window)
    playwindow.resizable(0,0)
    playwindow.title('TmEsg')
    playwindow.geometry('950x700')

    selectlevlabel = tkinter.Label(playwindow, text="Vyber si level:", font=('Arial', 15, 'bold'))
    selectlevlabel.place(x=420, y=100)

    def easylevelpress():
        easyenem = LevelEnemparams(zivot=50, damage=5, rng=25, weapon="None", healovanieamm=2, defense=1)
        easyplayer = LevelPlayerparams(zivot=100, damage=15, weapon="Gun", healovanieamm=10, defense= 1)
        playwindow.destroy()
        bojokno(easyenem, easyplayer)
    
    def mediumlevelpress():
        mediumenem = LevelEnemparams(zivot=100, damage=10, rng=35, weapon="Sword", healovanieamm=5, defense=1)
        mediumplayer = LevelPlayerparams(zivot=100, damage=10, weapon="Sword", healovanieamm=5, defense=1)
        playwindow.destroy()
        bojokno(mediumenem,mediumplayer)
    
    def hardlevelpress():
        hardenem= LevelEnemparams(zivot=150, damage=25, rng=45, weapon="Gun",healovanieamm=8, defense=1)
        hardplayer = LevelPlayerparams(zivot=85, damage=15,weapon="None",healovanieamm=3, defense=1)
        playwindow.destroy()
        bojokno(hardenem,hardplayer)

    def veryhardlevelpress():
        vhardenem= LevelEnemparams(zivot=200, damage=50, rng=70, weapon="Gun",healovanieamm=10, defense=1)
        vhardplayer = LevelPlayerparams(zivot=50,damage=25,weapon="None",healovanieamm=1, defense=1)
        playwindow.destroy()
        bojokno(vhardenem,vhardplayer)


    easylev = tkinter.Button(playwindow, text="Ľahké", background="Green", activebackground="Dark Green", height=2, width=21, command=easylevelpress)
    easylev.place(x=150, y=200)
    mediumlev = tkinter.Button(playwindow, text="Stredné", background="Yellow", activebackground="Goldenrod", height=2, width=21, command=mediumlevelpress)
    mediumlev.place(x=320, y=200)
    hardlev = tkinter.Button(playwindow, text="Ťažké", background="Orange", activebackground="Orange3", height=2, width=21, command=hardlevelpress)
    hardlev.place(x=490, y=200)
    vhardlev = tkinter.Button(playwindow, text="Veľmi Ťažké", background="Red", activebackground="Red3", height=2, width=21, command=veryhardlevelpress)
    vhardlev.place(x=660, y=200)



    ##################################
    ###    CUSTOM GAME SETTINGS    ###
    ##################################

    def vlastnahrapress():
        global uzivatel, nepriatel

        customlevelwindow = tkinter.Toplevel(window)
        customlevelwindow.title("Vlastná Hra")
        customlevelwindow.resizable(0, 0)
        customlevelwindow.geometry("500x450")
        customlevelwindow.update_idletasks()
        customlevelwindow.geometry(f"500x450+{window.winfo_x() + (window.winfo_width() - 500) // 2}+{window.winfo_y() + (window.winfo_height() - 450) // 2}")

        tkinter.Button(customlevelwindow, text="Späť", background='grey', height=2, width=10,
            command=lambda: customlevelwindow.destroy()).place(x=20, y=10)
        tkinter.Button(customlevelwindow, text="Hrať", background='grey', height=2, width=10,
            command=lambda: [customlevelwindow.destroy(), playwindow.destroy(), bojokno(nepriatel, uzivatel)]).place(x=370, y=10)

        tkinter.Label(customlevelwindow, text="Vlastná Hra", font=('Arial', 20, 'bold')).place(x=250, y=55, anchor='center')
        tkinter.Label(customlevelwindow, text="─" * 44, fg='gray').place(x=250, y=80, anchor='center')

        # Player section
        tkinter.Label(customlevelwindow, text="Hráč", font=('Arial', 12, 'bold')).place(x=250, y=100, anchor='center')

        tkinter.Label(customlevelwindow, text="Zdravie:").place(x=80, y=125)
        zivotentry = tkinter.Entry(customlevelwindow, width=10)
        zivotentry.place(x=180, y=125)
        zivotentry.insert(0, str(uzivatel.zivot))
        def aktualizujzivot():
            try:
                novyzivot = int(zivotentry.get())
                if novyzivot <= 0 or novyzivot > 100:
                    tkinter.messagebox.showerror('Out of range', 'Range: 1-100')
                else:
                    uzivatel.zivot = novyzivot
                    tkinter.messagebox.showinfo('Úspech!', 'Zdravie zmenené!')
            except ValueError:
                tkinter.messagebox.showerror('Chyba', 'Zadajte číslo.')
        tkinter.Button(customlevelwindow, text="Nastaviť", command=aktualizujzivot).place(x=280, y=123)

        tkinter.Label(customlevelwindow, text="Poškodenie:").place(x=80, y=155)
        damage_entry = tkinter.Entry(customlevelwindow, width=10)
        damage_entry.place(x=180, y=155)
        damage_entry.insert(0, str(uzivatel.damage))
        def updatedamage():
            try:
                new_damage = int(damage_entry.get())
                if new_damage <= 0 or new_damage > 10:
                    tkinter.messagebox.showerror('Out of range', 'Range: 1-10')
                else:
                    uzivatel.damage = new_damage
                    tkinter.messagebox.showinfo('Úspech!', 'Poškodenie zmenené!')
            except ValueError:
                tkinter.messagebox.showerror('Chyba', 'Zadajte číslo.')
        tkinter.Button(customlevelwindow, text="Nastaviť", command=updatedamage).place(x=280, y=153)

        tkinter.Label(customlevelwindow, text="─" * 44, fg='gray').place(x=250, y=185, anchor='center')

        # Enemy section
        tkinter.Label(customlevelwindow, text="Nepriateľ", font=('Arial', 12, 'bold')).place(x=250, y=200, anchor='center')

        tkinter.Label(customlevelwindow, text="Zdravie:").place(x=80, y=225)
        healthEnemy_entry = tkinter.Entry(customlevelwindow, width=10)
        healthEnemy_entry.place(x=180, y=225)
        healthEnemy_entry.insert(0, str(nepriatel.zivot))
        def updateEnem_health():
            try:
                new_healthEnemy = int(healthEnemy_entry.get())
                if new_healthEnemy <= 0 or new_healthEnemy > 100:
                    tkinter.messagebox.showerror('Out of range', 'Range: 1-100')
                else:
                    nepriatel.zivot = new_healthEnemy
                    tkinter.messagebox.showinfo('Úspech!', 'Zdravie zmenené!')
            except ValueError:
                tkinter.messagebox.showerror('Chyba', 'Zadajte číslo.')
        tkinter.Button(customlevelwindow, text="Nastaviť", command=updateEnem_health).place(x=280, y=223)

        tkinter.Label(customlevelwindow, text="Poškodenie:").place(x=80, y=255)
        damageEnemy_entry = tkinter.Entry(customlevelwindow, width=10)
        damageEnemy_entry.place(x=180, y=255)
        damageEnemy_entry.insert(0, str(nepriatel.damage))
        def updatedEnemamage():
            try:
                newEnemy_damage = int(damageEnemy_entry.get())
                if newEnemy_damage <= 0 or newEnemy_damage > 10:
                    tkinter.messagebox.showerror('Out of range', 'Range: 1-10')
                else:
                    nepriatel.damage = newEnemy_damage
                    tkinter.messagebox.showinfo('Úspech!', 'Poškodenie zmenené!')
            except ValueError:
                tkinter.messagebox.showerror('Chyba', 'Zadajte číslo.')
        tkinter.Button(customlevelwindow, text="Nastaviť", command=updatedEnemamage).place(x=280, y=253)

        tkinter.Label(customlevelwindow, text="RNG:").place(x=80, y=285)
        rngEnemy_entry = tkinter.Entry(customlevelwindow, width=10)
        rngEnemy_entry.place(x=180, y=285)
        rngEnemy_entry.insert(0, str(nepriatel.rng))
        def rngEnem():
            try:
                newEnemy_rng = int(rngEnemy_entry.get())
                if newEnemy_rng <= 0 or newEnemy_rng > 100:
                    tkinter.messagebox.showerror('Out of range', 'Range: 1-100')
                else:
                    nepriatel.rng = newEnemy_rng
                    tkinter.messagebox.showinfo('Úspech!', 'RNG zmenené!')
            except ValueError:
                tkinter.messagebox.showerror('Chyba', 'Zadajte číslo.')
        tkinter.Button(customlevelwindow, text="Nastaviť", command=rngEnem).place(x=280, y=283)

    customlev = tkinter.Button(playwindow, text="Vlastná Hra", background="MediumOrchid1", activebackground="MediumOrchid3", height=2, width=21, command=vlastnahrapress)
    customlev.place(x=400, y=250)

    customlev = tkinter.Button(playwindow, text="Vlastná Hra",background="MediumOrchid1",activebackground="MediumOrchid3",height=2, width=21,command=vlastnahrapress)
    customlev.place(x=400, y=250)

    ##################################
    #### CUSTOM GAME SETTINGS END #### 
    ##################################   

    def backmainpress():
        playwindow.destroy()
    backmain = tkinter.Button(playwindow, text="Vrátiť sa do menu", background="Gray", activebackground="Dark Gray", height=2, width=21, command=backmainpress)
    backmain.place(x=400, y=350)

    #### level select setup End ####

audiovar = tkinter.BooleanVar()
audiovar.set(musicon)

def musicsetter():
    global musicon
    global audiovar

    if audiovar.get():
        pygame.mixer.music.play()
        print("Musicon set to True")
        musicon = True
    else:
        pygame.mixer.music.pause()
        print("Musicon set to False")
        musicon = False

sfxvar = tkinter.BooleanVar()
sfxvar.set(audioOn)

def sfxsetter():
    global audioOn
    global sfxvar

    if sfxvar.get():
        audioOn = True
    else:
        audioOn = False

def settingspressed():
    global musicon
    global audiovar, sfxvar
    settingswindow = tkinter.Toplevel(window)
    settingswindow.title("Nastavenia")
    settingswindow.resizable(0,0)
    settingswindow.geometry("400x300")

    tkinter.Label(settingswindow, text="Nastavenia", font=('Arial', 20, 'bold')).place(x=200, y=20, anchor='center')


    tkinter.Label(settingswindow, text="─" * 40, fg='gray').place(x=200, y=45, anchor='center')


    tkinter.Label(settingswindow, text="Zvuk", font=('Arial', 12, 'bold')).place(x=200, y=70, anchor='center')

    tkinter.Label(settingswindow, text="Hudba:").place(x=100, y=100)
    audiocheck = tkinter.Checkbutton(settingswindow, variable=audiovar, command=musicsetter)
    audiocheck.place(x=200, y=100)

    tkinter.Label(settingswindow, text="Zvukové efekty:").place(x=100, y=130)
    sfxcheck = tkinter.Checkbutton(settingswindow, variable=sfxvar, command=sfxsetter)
    sfxcheck.place(x=200, y=130)


    tkinter.Label(settingswindow, text="─" * 40, fg='gray').place(x=200, y=165, anchor='center')


    tkinter.Label(settingswindow, text="Hráč", font=('Arial', 12, 'bold')).place(x=200, y=180, anchor='center')

    tkinter.Label(settingswindow, text="Meno hráča:").place(x=100, y=210)
    nameentry = tkinter.Entry(settingswindow)
    nameentry.place(x=200, y=210)
    nameentry.insert(0, player_name)

    def confirmname():
        global player_name
        newname = nameentry.get().strip()
        if newname:
            player_name = newname
            tkinter.messagebox.showinfo("Úspech!", "Meno bolo zmenené!", parent=settingswindow)
        else:
            tkinter.messagebox.showerror("Chyba", "Meno nemôže byť prázdne.", parent=settingswindow)

    tkinter.Button(settingswindow, text="Nastaviť meno", background='grey', command=confirmname).place(x=200, y=250, anchor='center')
#### UI buttons handling ####


#### main menu UI ####
def temp():
    pass
logo = tkinter.PhotoImage(file="Media/logo.png")  
logolabel = tkinter.Label(window, image=logo)
logolabel.place(x=0, y=0)  # initial creation, will be overidden later 
playbutton = tkinter.Button(window, text= "Hrať", background='grey', height= 2, width= 21, command=playpressed)
settingsbuttonmainmenu = tkinter.Button(window, text= "Nastavenia", background='grey', height= 2, width= 21, command = settingspressed)
exitbutton = tkinter.Button(window, text='Exit', background='grey', height= 2, width= 21, command= exitpressed)





def center_logo(item, window_width, y_position):
    item.update_idletasks() # AI
    item_width = item.winfo_width()
    x_position = (window_width - item_width) // 2
    item.place(x=x_position, y=y_position)
    


def center_item(item, window_width, y_position):
    item.update_idletasks()  # AI 
    item_width = item.winfo_width()
    x_position = (window_width - item_width) // 2
    item.place(x=x_position, y=y_position, anchor= 'center')



#### handling of centering ####

center_logo(logolabel, 950, 70) 
center_item(playbutton, 950, 340)
center_item(settingsbuttonmainmenu, 950, 440)
center_item(exitbutton, 950, 540)

#### handling of centering ####

def savedata():
    data = {
        "Playerhealth" : uzivatel.zivot,
        "Playerdmg" : uzivatel.damage,
        "Playerweap" : uzivatel.weapon,
        "Enemhealth" : nepriatel.zivot,
        "Enemdmg" : nepriatel.damage,
        "Enemweap" : nepriatel.weapon,
        "Enemrng" : nepriatel.rng,
        "musicon" : musicon,
        "audioOn" : audioOn,
        "PlayerName" : player_name
    }
    with open(saveloc, "wb") as file:
        pickle.dump(data, file)







window.mainloop()
