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
current_score = 0
current_level = "Custom"
difficulty_multiplier = 1.0
_next_level_func = None
def loadData():
    try:
        with open(saveloc, 'rb') as file:
            data = pickle.load(file)
        if 'TopScores' not in data:
            data['TopScores'] = {
                "Easy": 0,
                "Medium": 0,
                "Hard": 0,
                "VeryHard": 0,
                "Custom": 0
            }
        if 'PlayerName' not in data:
            data['PlayerName'] = None
        if 'musicon' not in data:
            data['musicon'] = True  
        if 'audioOn' not in data:
            data['audioOn'] = True 

        return data

    except (FileNotFoundError, EOFError, pickle.UnpicklingError, ImportError, MemoryError):
        tkinter.messagebox.showerror("Data Error", "Couldn't load save data, reverting to defaults.")
        return {
            "Playerhealth": 100,
            "Playerdmg": 5,
            "Playerweap": "None",
            "Enemhealth": 100,
            "Enemdmg": 5,
            "Enemweap": "None",
            "Enemrng": 50,
            "musicon": True,
            "audioOn": True,
            "PlayerName": None,
            "TopScores": {
                "Easy": 0,
                "Medium": 0,
                "Hard": 0,
                "VeryHard": 0,
                "Custom": 0
            }
        }

gamedata = loadData()

musicon = gamedata['musicon']
audioOn = gamedata['audioOn']
player_name = gamedata.get("PlayerName", None)

pygame.mixer.music.load("Media/audio/Test Instrumental - Friday Night Funkin.mp3")
if musicon == False:
    pass
else:
    pygame.mixer.music.play(loops=-1)

def ask_for_name():
    global player_name
    name_window = tkinter.Tk()
    name_window.title("Vitaj!")
    name_window.resizable(0, 0)
    name_window.geometry("500x520")

    tkinter.Label(name_window, text="Vitaj!!", font=('Arial', 18, 'bold')).pack(pady=15)

    tkinter.Label(name_window, text="─" * 55, fg='gray').pack()

    tkinter.Label(name_window, text="Ako sa hrá", font=('Arial', 13, 'bold')).pack(pady=8)

    tutorial_text = [
        ("Útoč",          '#4a9e4a', "Zaútočíš na nepriateľa za náhodné poškodenie."),
        ("Obránenie",     '#4a7abf', "Znížiš poškodenie nepriateľa na polovicu."),
        ("Použi bonus",   '#c8a800', "Vyliečiš sa o náhodné HP (max 15)."),
        ("Preskoč kolo",  '#888888', "Preskočíš svoj ťah a necháš nepriateľa útočiť."),
    ]

    for action, color, desc in tutorial_text:
        frame = tkinter.Frame(name_window)
        frame.pack(fill='x', padx=40, pady=3)
        tkinter.Label(frame, text=action, font=('Arial', 10, 'bold'), fg='white',
                      background=color, width=14, anchor='center').pack(side='left')
        tkinter.Label(frame, text=desc, font=('Arial', 10), wraplength=280,
                      justify='left').pack(side='left', padx=10)

    tkinter.Label(name_window, text="─" * 55, fg='gray').pack(pady=8)

    tkinter.Label(name_window, text="Zadaj svoje meno:", font=('Arial', 12)).pack()
    name_entry = tkinter.Entry(name_window, font=('Arial', 12), width=20)
    name_entry.pack(pady=8)

    def confirm():
        global player_name
        name = name_entry.get().strip()
        if name:
            player_name = name
            name_window.destroy()
        else:
            tkinter.messagebox.showwarning("Žiadne meno", "Prosím zadaj meno.", parent=name_window)

    tkinter.Button(name_window, text="Začať hrať", background='#4a9e4a', activebackground='#3a7e3a',
                   fg='white', font=('Arial', 11, 'bold'), width=16, command=confirm).pack(pady=10)

    name_window.mainloop()

if not player_name:
    ask_for_name()


window = tkinter.Tk()
def disable_event():
   pass
window.protocol("WM_DELETE_WINDOW", disable_event)
window.title("TmEsg")
window.resizable(0, 0)
window.geometry("950x700")


class Playerparams():
    def __init__(self, zivot, damage, weapon, healovanieamm):
        self.zivot = zivot
        self.damage = damage
        self.weapon = weapon
        self.healovanieamm = healovanieamm

    def __str__(self):
        return f'{self.weapon} {self.damage} {self.weapon}'

class Enemparams():
    def __init__(self, zivot, damage, rng, weapon, healovanieamm):
        self.zivot = zivot
        self.damage = damage
        self.rng = rng
        self.weapon = weapon
        self.healovanieamm = healovanieamm

class LevelEnemparams():
    def __init__(self, zivot, damage, rng, weapon, healovanieamm, defense):
        self.zivot = zivot
        self.damage = damage
        self.rng = rng
        self.weapon = weapon
        self.healovanieamm = healovanieamm
        self.defense = defense

class LevelPlayerparams():
    def __init__(self, zivot, damage, weapon, healovanieamm, defense):
        self.zivot = zivot
        self.damage = damage
        self.weapon = weapon
        self.healovanieamm = healovanieamm
        self.defense = defense


uzivatel = Playerparams(gamedata['Playerhealth'], gamedata['Playerdmg'], gamedata['Playerweap'], 1)
nepriatel = Enemparams(gamedata['Enemhealth'], gamedata['Enemdmg'], gamedata['Enemrng'], gamedata['Enemweap'], 1)


def add_score(points):
    global current_score, scorelabel
    current_score += points
    scorelabel.config(text=f"Skóre: {current_score}")

def finish_score(remaining_hp, rounds_taken, next_level_func=None):
    global current_score, current_level, difficulty_multiplier
    hp_bonus = remaining_hp * 2
    round_bonus = max(0, 200 - (rounds_taken * 10))
    final_score = int((current_score + hp_bonus + round_bonus) * difficulty_multiplier)

    is_new_high = final_score > gamedata['TopScores'][current_level]
    if is_new_high:
        gamedata['TopScores'][current_level] = final_score
        savedata()

    win_window = tkinter.Toplevel(bojoveokno)
    win_window.title("Výhra!")
    win_window.resizable(0, 0)
    win_window.geometry("400x250")
    win_window.update_idletasks()
    win_window.geometry(f"400x250+{bojoveokno.winfo_x() + (bojoveokno.winfo_width() - 400) // 2}+{bojoveokno.winfo_y() + (bojoveokno.winfo_height() - 250) // 2}")

    if is_new_high:
        tkinter.Label(win_window, text="🏆 Nové Vysoké Skóre!", font=('Arial', 16, 'bold'), fg='gold').place(x=200, y=30, anchor='center')
    else:
        tkinter.Label(win_window, text="Vyhral si!", font=('Arial', 16, 'bold')).place(x=200, y=30, anchor='center')

    tkinter.Label(win_window, text=f"Skóre: {final_score}", font=('Arial', 13)).place(x=200, y=70, anchor='center')
    tkinter.Label(win_window, text=f"Najvyššie skóre: {gamedata['TopScores'][current_level]}", font=('Arial', 11), fg='gray').place(x=200, y=100, anchor='center')

    tkinter.Label(win_window, text="─" * 40, fg='gray').place(x=200, y=130, anchor='center')

    def go_to_menu():
        win_window.destroy()
        bojoveokno.destroy()

    def go_next_level():
        win_window.destroy()
        bojoveokno.destroy()
        if next_level_func:
            next_level_func()

    tkinter.Button(win_window, text="Hlavné Menu", background='#4a7abf', fg='white', font=('Arial', 11, 'bold'), height=2, width=14, command=go_to_menu).place(x=100, y=170, anchor='center')

    if next_level_func:
        tkinter.Button(win_window, text="Ďalší Level", background='#4a9e4a', fg='white', font=('Arial', 11, 'bold'), height=2, width=14, command=go_next_level).place(x=300, y=170, anchor='center')
    else:
        tkinter.Label(win_window, text="(Toto je posledný level)", font=('Arial', 10), fg='gray').place(x=200, y=170, anchor='center')




def bojokno(nepriatel, uzivatel, level_name="Custom", diff_multiplier=1.0,next_level_func_param=None):
    global uzivatelovekolo
    global fightbutton, defendbutton, itembutton, skipturnbutton
    global uzivatelzivotlabel, nepriatelzivotstatus
    global bojoveokno
    global pomockylabel
    global UzivatelObranuje
    global kololabelinteger
    global kololabel
    global uzivatelstatuslabel, nepriatelstatuslabel, uzivatelsprite, uzivatelspritelabel, nepriatelsprite, nepriatelspritelabel
    global current_score, current_level, difficulty_multiplier, scorelabel
    global _next_level_func

    _next_level_func = next_level_func_param
    current_score = 0
    current_level = level_name
    difficulty_multiplier = diff_multiplier

    battle_player = type(uzivatel)(*vars(uzivatel).values())
    battle_enemy = type(nepriatel)(*vars(nepriatel).values())

    bojoveokno = tkinter.Toplevel(window)
    bojoveokno.title("Battle!")
    bojoveokno.resizable(0, 0)
    bojoveokno.geometry("1080x600")
    bojoveokno.update_idletasks()
    bojoveokno.geometry(f"1080x600+{window.winfo_x() + (window.winfo_width() - 1080) // 2}+{window.winfo_y() + (window.winfo_height() - 600) // 2}")
    exitfightbutton = tkinter.Button(bojoveokno, text="Menu", background='#bf4a4a', fg='white', font=('Arial', 9, 'bold'), height=1, width=8, command=lambda: [bojoveokno.destroy()])
    exitfightbutton.place(x=60, y=450, anchor='center')
    kololabelinteger = 1
    kololabel = tkinter.Label(bojoveokno, text=f"KOLO: {kololabelinteger}", font=('Arial', 20, 'bold'))
    kololabel.place(x=540, y=20, anchor='center')
    
    uzivatelzivotlabel = tkinter.Label(bojoveokno, text=f"HP: {uzivatel.zivot}", font=('Arial', 10, 'bold'))
    uzivatelzivotlabel.place(x=250, y=70, anchor='center')

    uzivatelsprite = tkinter.PhotoImage(file="Media/uzivatelsprite.png")
    namelabel = tkinter.Label(bojoveokno, text=player_name, font=('Arial', 10, 'bold'))
    namelabel.place(x=200 + (uzivatelsprite.width() // 2), y=90, anchor='center')


    uzivatelstatuslabel = tkinter.Label(bojoveokno, text="", font=('Arial', 14, 'bold'))
    uzivatelstatuslabel.place(x=300, y=95, anchor='center')

    uzivatelspritelabel = tkinter.Label(bojoveokno, image=uzivatelsprite)
    uzivatelspritelabel.place(x=200, y=110)
    uzivatelspritelabel.image = uzivatelsprite

    nepriatelzivotstatus = tkinter.Label(bojoveokno, text=f"HP: {nepriatel.zivot}", font=('Arial', 10, 'bold'))
    nepriatelzivotstatus.place(x=860, y=70, anchor='center')


    nepriatelmeno = tkinter.Label(bojoveokno, text="Nepriateľ", font=('Arial', 10, 'bold'))
    nepriatelmeno.place(x=860, y=90, anchor='center')


    nepriatelstatuslabel = tkinter.Label(bojoveokno, text="", font=('Arial', 14, 'bold'))
    nepriatelstatuslabel.place(x=800, y=95, anchor='center')

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

    scorelabel = tkinter.Label(bojoveokno, text="Skóre: 0", font=('Arial', 10, 'bold'))
    scorelabel.place(x=540, y=510, anchor='center')

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
    add_score(5)
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
    bojoveokno.after(1000, lambda: uzivatelstatuslabel.config(text=""))
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
    zvukrandomrng = random.randint(1, 4)
    if sfxvar.get():
        if zvukrandomrng == 1:
            Zvukrandom = pygame.mixer.Sound("Media/audio/pain1.mp3")
            Zvukrandom.play()
        elif zvukrandomrng == 2:
            Zvukrandom = pygame.mixer.Sound("Media/audio/pain2.mp3")
            Zvukrandom.play()
        elif zvukrandomrng == 3:
            Zvukrandom = pygame.mixer.Sound("Media/audio/pain3.mp3")
            Zvukrandom.play()
        elif zvukrandomrng == 4:
            Zvukrandom = pygame.mixer.Sound("Media/audio/pain4.mp3")
            Zvukrandom.play()

    UzivatelObranuje = False
    if not uzivatelovekolo:
        return

    utoksila = random.randint(1, uzivatel.damage)
    nepriatel.zivot -= utoksila
    add_score(utoksila)
    nepriatelzivotstatus.config(text=f"HP: {nepriatel.zivot}")
    nepriatelstatuslabel.config(text=f"-{utoksila}", fg="red")
    nepriatelsprite.config(file="Media/nepriatelspritehit.png")
    bojoveokno.after(1000, lambda: nepriatelstatuslabel.config(text=""))

    if nepriatel.zivot <= 0:
        finish_score(uzivatel.zivot, kololabelinteger, _next_level_func)
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
    zvukrandomrng = random.randint(1, 4)
    if sfxvar.get():
        if zvukrandomrng == 1:
            Zvukrandom = pygame.mixer.Sound("Media/audio/pain1.mp3")
            Zvukrandom.play()
        elif zvukrandomrng == 2:
            Zvukrandom = pygame.mixer.Sound("Media/audio/pain2.mp3")
            Zvukrandom.play()
        elif zvukrandomrng == 3:
            Zvukrandom = pygame.mixer.Sound("Media/audio/pain3.mp3")
            Zvukrandom.play()
        elif zvukrandomrng == 4:
            Zvukrandom = pygame.mixer.Sound("Media/audio/pain4.mp3")
            Zvukrandom.play()

    if UzivatelObranuje == False:
        enemattackpow = random.randint(1, nepriatel.damage)
    else:
        enemattackpow = random.randint(1, nepriatel.damage // 2)

    uzivatel.zivot -= enemattackpow
    uzivatelzivotlabel.config(text=f"HP: {uzivatel.zivot}")
    uzivatelstatuslabel.config(text=f"-{enemattackpow}", fg="red")
    uzivatelsprite.config(file="Media/uzivatelspritehit.png")
    bojoveokno.after(1000, lambda: uzivatelstatuslabel.config(text=""))

    if uzivatel.zivot <= 0:
        tkinter.messagebox.showinfo("Prehra", "Bol si porazený!")
        bojoveokno.destroy()
        return

    bojoveokno.after(1000, lambda: uzivatelsprite.config(file="Media/uzivatelsprite.png"))
    UzivatelObranuje = False
    uzivatelovekolo = True
    buttonystatus("normal")
    kololabelinteger += 1
    kololabel.config(text=f"KOLO:{kololabelinteger}")


def buttonystatus(state):
    fightbutton.config(state=state)
    defendbutton.config(state=state)
    itembutton.config(state=state)
    skipturnbutton.config(state=state)




def exitpressed():
    window.destroy()
    savedata()


def scorespressed():
    scoreswindow = tkinter.Toplevel(window)
    scoreswindow.title("Vysoké Skóre")
    scoreswindow.resizable(0, 0)
    scoreswindow.geometry("400x350")
    scoreswindow.update_idletasks()
    scoreswindow.geometry(f"400x350+{window.winfo_x() + (window.winfo_width() - 400) // 2}+{window.winfo_y() + (window.winfo_height() - 350) // 2}")

    tkinter.Label(scoreswindow, text="Vysoké Skóre", font=('Arial', 20, 'bold')).place(x=200, y=20, anchor='center')
    tkinter.Label(scoreswindow, text="─" * 40, fg='gray').place(x=200, y=50, anchor='center')

    levels = [("Ľahké", "Easy"), ("Stredné", "Medium"), ("Ťažké", "Hard"), ("Veľmi Ťažké", "VeryHard"), ("Vlastná", "Custom")]
    for i, (label, key) in enumerate(levels):
        tkinter.Label(scoreswindow, text=label, font=('Arial', 11, 'bold')).place(x=120, y=80 + i * 45)
        tkinter.Label(scoreswindow, text=str(gamedata['TopScores'][key]), font=('Arial', 11)).place(x=280, y=80 + i * 45)

    tkinter.Button(scoreswindow, text="Zavrieť", background='grey', height=2, width=10, command=scoreswindow.destroy).place(x=200, y=300, anchor='center')


def playpressed():
    global uzivatel, nepriatel

    playwindow = tkinter.Toplevel(window)
    playwindow.resizable(0, 0)
    playwindow.title('TmEsg')
    playwindow.geometry('950x700')
    playwindow.update_idletasks()
    playwindow.geometry(f"950x700+{window.winfo_x() + (window.winfo_width() - 950) // 2}+{window.winfo_y() + (window.winfo_height() - 700) // 2}")

    def easylevelpress():
        easyenem = LevelEnemparams(zivot=50, damage=5, rng=25, weapon="None", healovanieamm=2, defense=1)
        easyplayer = LevelPlayerparams(zivot=100, damage=15, weapon="Gun", healovanieamm=10, defense=1)
        playwindow.destroy()
        bojokno(easyenem, easyplayer, level_name="Easy", diff_multiplier=1.0, next_level_func_param=mediumlevelpress)

    def mediumlevelpress():
        mediumenem = LevelEnemparams(zivot=100, damage=10, rng=35, weapon="Sword", healovanieamm=5, defense=1)
        mediumplayer = LevelPlayerparams(zivot=100, damage=10, weapon="Sword", healovanieamm=5, defense=1)
        bojokno(mediumenem, mediumplayer, level_name="Medium", diff_multiplier=1.5, next_level_func_param=hardlevelpress)

    def hardlevelpress():
        hardenem = LevelEnemparams(zivot=150, damage=25, rng=45, weapon="Gun", healovanieamm=8, defense=1)
        hardplayer = LevelPlayerparams(zivot=85, damage=15, weapon="None", healovanieamm=3, defense=1)
        bojokno(hardenem, hardplayer, level_name="Hard", diff_multiplier=2.0, next_level_func_param=veryhardlevelpress)

    def veryhardlevelpress():
        vhardenem = LevelEnemparams(zivot=200, damage=50, rng=70, weapon="Gun", healovanieamm=10, defense=1)
        vhardplayer = LevelPlayerparams(zivot=50, damage=25, weapon="None", healovanieamm=1, defense=1)
        bojokno(vhardenem, vhardplayer, level_name="VeryHard", diff_multiplier=3.0, next_level_func_param=None)

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
            command=lambda: [customlevelwindow.destroy(), playwindow.destroy(), bojokno(nepriatel, uzivatel, level_name="Custom", diff_multiplier=1.0)]).place(x=370, y=10)

        tkinter.Label(customlevelwindow, text="Vlastná Hra", font=('Arial', 20, 'bold')).place(x=250, y=55, anchor='center')
        tkinter.Label(customlevelwindow, text="─" * 44, fg='gray').place(x=250, y=80, anchor='center')

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

    tkinter.Label(playwindow, text="Vyber si level", font=('Arial', 22, 'bold')).place(x=475, y=60, anchor='center')
    tkinter.Label(playwindow, text="─" * 80, fg='gray').place(x=475, y=90, anchor='center')

    levels = [
        ("Ľahké",       '#4a9e4a', '#3a7e3a', "Nepriateľ: 50 HP  |  Ty: 100 HP",  easylevelpress),
        ("Stredné",     '#c8a800', '#a88a00', "Nepriateľ: 100 HP  |  Ty: 100 HP", mediumlevelpress),
        ("Ťažké",       '#d4721a', '#b45a10', "Nepriateľ: 150 HP  |  Ty: 85 HP",  hardlevelpress),
        ("Veľmi Ťažké", '#bf4a4a', '#9f3a3a', "Nepriateľ: 200 HP  |  Ty: 50 HP",  veryhardlevelpress),
    ]

    for i, (text, bg, hover, desc, cmd) in enumerate(levels):
        x = 125 + i * 195
        tkinter.Button(playwindow, text=text, background=bg, activebackground=hover,
                       fg='white', font=('Arial', 11, 'bold'), height=3, width=14,
                       command=cmd).place(x=x, y=200)
        tkinter.Label(playwindow, text=desc, font=('Arial', 9), fg='gray').place(x=x + 70, y=275, anchor='center')

    tkinter.Label(playwindow, text="─" * 80, fg='gray').place(x=475, y=310, anchor='center')

    tkinter.Label(playwindow, text="Vlastná hra", font=('Arial', 13, 'bold')).place(x=475, y=340, anchor='center')
    tkinter.Label(playwindow, text="Nastav si vlastné parametre pre hráča a nepriateľa", font=('Arial', 10), fg='gray').place(x=475, y=365, anchor='center')

    tkinter.Button(playwindow, text="Vlastná Hra", background='#7a4abf', activebackground='#5a3a9f',
                   fg='white', font=('Arial', 11, 'bold'), height=2, width=21,
                   command=vlastnahrapress).place(x=475, y=400, anchor='center')

    tkinter.Label(playwindow, text="─" * 80, fg='gray').place(x=475, y=450, anchor='center')

    tkinter.Button(playwindow, text="Vrátiť sa do menu", background='#555555', activebackground='#333333',
                   fg='white', font=('Arial', 11, 'bold'), height=2, width=21,
                   command=lambda: playwindow.destroy()).place(x=475, y=490, anchor='center')


audiovar = tkinter.BooleanVar()
audiovar.set(musicon)

def musicsetter():
    global musicon
    global audiovar
    if audiovar.get():
        pygame.mixer.music.play(loops=-1)
        musicon = True
    else:
        pygame.mixer.music.pause()
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
    settingswindow.resizable(0, 0)
    settingswindow.geometry("400x300")
    settingswindow.update_idletasks()
    settingswindow.geometry(f"400x300+{window.winfo_x() + (window.winfo_width() - 400) // 2}+{window.winfo_y() + (window.winfo_height() - 300) // 2}")

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

    tkinter.Button(settingswindow, text="Nastaviť meno", background='grey', command=confirmname).place(x=200, y=240, anchor='center')




logo = tkinter.PhotoImage(file="Media/logo.png")
logolabel = tkinter.Label(window, image=logo)
logolabel.place(x=0, y=0)

playbutton = tkinter.Button(window, text="Hrať", background='#4a9e4a', activebackground='#3a7e3a', fg='white', font=('Arial', 12, 'bold'), height=2, width=21, command=playpressed)
settingsbuttonmainmenu = tkinter.Button(window, text="Nastavenia", background='#4a7abf', activebackground='#3a5a9f', fg='white', font=('Arial', 12, 'bold'), height=2, width=21, command=settingspressed)
scoresbutton = tkinter.Button(window, text="Vysoké Skóre", background='#bf9a2a', activebackground='#9f7a1a', fg='white', font=('Arial', 12, 'bold'), height=2, width=21, command=scorespressed)
exitbutton = tkinter.Button(window, text="Exit", background='#bf4a4a', activebackground='#9f3a3a', fg='white', font=('Arial', 12, 'bold'), height=2, width=21, command=exitpressed)


def center_logo(item, window_width, y_position):
    item.update_idletasks()
    item_width = item.winfo_width()
    x_position = (window_width - item_width) // 2
    item.place(x=x_position, y=y_position)


def center_item(item, window_width, y_position):
    item.update_idletasks()
    item_width = item.winfo_width()
    x_position = (window_width - item_width) // 2
    item.place(x=x_position, y=y_position, anchor='center')


center_logo(logolabel, 950, 70)
center_item(playbutton, 950, 370)
center_item(settingsbuttonmainmenu, 950, 440)
center_item(scoresbutton, 950, 510)
center_item(exitbutton, 950, 580)


def savedata():
    data = {
        "Playerhealth": uzivatel.zivot,
        "Playerdmg": uzivatel.damage,
        "Playerweap": uzivatel.weapon,
        "Enemhealth": nepriatel.zivot,
        "Enemdmg": nepriatel.damage,
        "Enemweap": nepriatel.weapon,
        "Enemrng": nepriatel.rng,
        "musicon": musicon,
        "audioOn": audioOn,
        "PlayerName": player_name,
        "TopScores": gamedata['TopScores']
    }
    with open(saveloc, "wb") as file:
        pickle.dump(data, file)


window.mainloop()