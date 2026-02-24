import tkinter
from tkinter import ttk
import tkinter.messagebox
import pickle
from PIL import Image, ImageTk
import random

saveloc = "Data/game_data.dat"
playerturn = True
playerdamagelabel = None
enemydamagelabel = None
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
        "Enemrng" : 50
        }


gamedata = loadData()

# ENEMY RNG TABLE DEFAULTS: 50
# For attack: This will be default when nothing is needed
# When below half health: it will heal if RNG rolls below selected RNG value, will attack if above, which means higher RNG = harder fight. (100 would mean 100% chance, 0 would mean 0%)


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

    def __init__(self, health, damage, weapon,healsamm):
        self.health = health
        self.damage = damage
        self.weapon = weapon
        self.healsamm= healsamm
    
    def __str__(self):
        return f'{self.weapon} {self.damage} {self.weapon}'

class Enemparams():

    def __init__(self, health, damage, rng, weapon,healsamm):
        self.health= health
        self.damage = damage
        self.rng = rng
        self.weapon = weapon
        self.healsamm= healsamm

class LevelEnemparams():

    def __init__(self,health,damage,rng,weapon,healsamm,defense):
        self.health = health
        self.damage = damage
        self.rng = rng
        self.weapon = weapon
        self.healsamm = healsamm
        self.defense = defense

class LevelPlayerparams():

    def __init__(self, health, damage, weapon,healsamm,defense):
        self.health = health
        self.damage = damage
        self.weapon = weapon
        self.healsamm = healsamm
        self.defense = defense

#### player and enemy obj creation #### 

player = Playerparams(gamedata['Playerhealth'], gamedata['Playerdmg'], gamedata['Playerweap'],1) # CUSTOM GAME PLAYER!!! last line is healsamm placeholder
enemy = Enemparams(gamedata['Enemhealth'], gamedata['Enemdmg'], gamedata['Enemrng'], gamedata['Enemweap'], 1) # CUSTOM GAME ENEMY!!! last line is healsamm placeholder

##################################
###       BATTLE LOGIC         ###
##################################

def mainfight(enemy, player):
    global playerturn
    global fightbutton, defendbutton, itembutton, skipturnbutton
    global playerhealthlabel, enemyhealthlabel
    global battlewindow
    global itemslabel
    global playerdefending
    global turncountplaceholder
    global turnlabel
    global playerdamagelabel, enemydamagelabel

    battle_player = type(player)(*vars(player).values())
    battle_enemy = type(enemy)(*vars(enemy).values())

    battlewindow = tkinter.Toplevel(window)
    battlewindow.title("Battle!")
    battlewindow.resizable(0, 0)
    battlewindow.geometry("1080x800")


    playersprite = tkinter.PhotoImage(file="Media/playersprite.png") 
    playersprlabel = tkinter.Label(battlewindow, image=playersprite)
    playersprlabel.place(x=200, y=120)
    playersprlabel.image = playersprite
    playerdamagelabel = tkinter.Label(battlewindow, text="", font=('Arial', 14, 'bold'))
    playerdamagelabel.place(x=300, y=70)
    enemydamagelabel = tkinter.Label(battlewindow, text="", font=('Arial', 14, 'bold'))
    enemydamagelabel.place(x=910, y=70)
    Enemsprite = tkinter.PhotoImage(file="Media/enemysprite.png")
    Enemsprlabel = tkinter.Label(battlewindow, image=Enemsprite)
    Enemsprlabel.place(x=800, y=120)
    Enemsprlabel.image = Enemsprite


    playerhealthlabel = tkinter.Label(battlewindow, text=f"HP: {player.health}", font=('Arial', 10, 'bold'))
    playerhealthlabel.place(x=225, y=70)

    enemyhealthlabel = tkinter.Label(battlewindow, text=f"HP: {enemy.health}", font=('Arial', 10, 'bold'))
    enemyhealthlabel.place(x=835, y=70)

    turncountplaceholder = 1
    turnlabel = tkinter.Label(battlewindow, text=f"KOLO:{turncountplaceholder}", font=('Arial', 20, 'bold'))
    turnlabel.place(x=460, y=50)


    fightbutton = tkinter.Button(battlewindow, text="Útoč", background='grey', height=2, width=21,command=lambda: player_attack(battle_player, battle_enemy))
    fightbutton.place(x=220, y=400)

    itembutton = tkinter.Button(battlewindow, text="Použi bonus", background='grey',height=2, width=21, command=lambda: player_heal(battle_player))
    itembutton.place(x=400, y=400)

    defendbutton = tkinter.Button(battlewindow, text="Defend", background='grey',height=2, width=21, command= lambda: player_defend(battle_player))
    defendbutton.place(x=580, y=400)

    skipturnbutton = tkinter.Button(battlewindow, text="Skip Turn", background='grey',height=2, width=21, command= lambda: player_skip(battle_player))
    skipturnbutton.place(x=760, y=400)

    itemslabel = tkinter.Label(battlewindow, text=f"Zostavajuce bonusy: {battle_player.healsamm}")
    itemslabel.place(x=420, y=450)

    UIwarn = tkinter.Label(battlewindow,text="PLACEHOLDER UI!!!\nVSETKO TU BUDE VYZERAT LEPSIE!!",font=('Arial', 30, 'bold'))
    UIwarn.place(x=180, y=500)
    playerdefending = False
    playerturn = True
    fightbutton.config(state="normal")

def player_skip(player):
    global playerturn
    print("Player skipped")
    playerturn = False
    set_buttons("disabled")
    battlewindow.after(1000, lambda: enemy_attack(player, enemy))

def player_defend(player):
    global playerturn
    global playerdefending
    if not playerturn:
        return
    
    playerdefending = True
    playerturn = False
    set_buttons("disabled")
    battlewindow.after(1000, lambda: enemy_attack(player, enemy))


def player_heal(player):
    global playerturn

    if not playerturn or player.healsamm == 0 or player.health == 100:
        return
    
    healpow = random.randint(1, 15)
    maxheal = 100 - player.health
    heal = min(healpow, maxheal)
    player.health += heal
    player.healsamm -= 1
    itemslabel.config(text=f"Zostavajuce bonusy: {player.healsamm}")
    playerhealthlabel.config(text=f"HP: {player.health}")
    print(f"Player heals for {healpow}")
    
    playerturn = False
    set_buttons("disabled")

    battlewindow.after(1000, lambda: enemy_attack(player, enemy))

    

def player_attack(player, enemy):
    global playerdefending
    global playerturn
    global enemydamagelabel
    playerdefending = False
    if not playerturn:
        return


    attackpow = random.randint(1, player.damage)
    enemy.health -= attackpow
    enemyhealthlabel.config(text=f"HP: {enemy.health}")
    enemydamagelabel.config(text=f"-{attackpow}", fg="red")
    battlewindow.after(1000, lambda:enemydamagelabel.config(text=""))
    print(f"Player attacks for {attackpow}")

    if enemy.health <= 0:
        print("Enemy defeated!")
        tkinter.messagebox.showinfo("Victory", "You defeated the enemy!")
        return

    playerturn = False
    set_buttons("disabled")

    battlewindow.after(1000, lambda: enemy_attack(player, enemy))


def enemy_attack(player, enemy):
    global playerturn
    global playerdefending
    global turncountplaceholder
    global turnlabel
    global playerdamagelabel
    print(f"{playerdefending}")
    if playerdefending == False:
        enemattackpow = random.randint(1, enemy.damage)
    else:  
        enemattackpow = random.randint(1, enemy.damage // 2)
        print(f"Defending success! playerdefending={playerdefending}")

    player.health -= enemattackpow
    playerhealthlabel.config(text=f"HP: {player.health}")
    playerdamagelabel.config(text=f"-{enemattackpow}", fg="red")
    battlewindow.after(1000, lambda: playerdamagelabel.config(text=""))
    print(f"Enemy attacks for {enemattackpow}")


    if player.health <= 0:
        print("Player defeated!")
        tkinter.messagebox.showinfo("Defeat", "You were defeated!")
        battlewindow.destroy()
        return

    playerturn = True
    set_buttons("normal")
    turncountplaceholder += 1
    turnlabel.config(text=f"KOLO:{turncountplaceholder}")
    



def set_buttons(state):
    fightbutton.config(state=state)
    defendbutton.config(state=state)
    itembutton.config(state=state)
    skipturnbutton.config(state=state)

#### UI buttons handling ####
def exitpressed():
    window.destroy()
    savedata()

    
def playpressed():
    global player, enemy

    playwindow = tkinter.Toplevel(window)
    playwindow.resizable(0,0)
    playwindow.title('TmEsg')
    playwindow.geometry('950x700')

    selectlevlabel = tkinter.Label(playwindow, text="Select Level:", font=('Arial', 15, 'bold'))
    selectlevlabel.place(x=420, y=100)

    def easylevelpress():
        easyenem = LevelEnemparams(health=50, damage=5, rng=25, weapon="None", healsamm=2, defense=1)
        easyplayer = LevelPlayerparams(health=100, damage=15, weapon="Gun", healsamm=10, defense= 1)
        playwindow.destroy()
        mainfight(easyenem, easyplayer)
    
    def mediumlevelpress():
        mediumenem = LevelEnemparams(health=100, damage=10, rng=35, weapon="Sword", healsamm=5, defense=1)
        mediumplayer = LevelPlayerparams(health=100, damage=10, weapon="Sword", healsamm=5, defense=1)
        playwindow.destroy()
        mainfight(mediumenem,mediumplayer)
    
    def hardlevelpress():
        hardenem= LevelEnemparams(health=150, damage=25, rng=45, weapon="Gun",healsamm=8, defense=1)
        hardplayer = LevelPlayerparams(health=85, damage=15,weapon="None",healsamm=3, defense=1)
        playwindow.destroy()
        mainfight(hardenem,hardplayer)

    def veryhardlevelpress():
        vhardenem= LevelEnemparams(health=200, damage=50, rng=70, weapon="Gun",healsamm=10, defense=1)
        vhardplayer = LevelPlayerparams(health=50,damage=25,weapon="None",healsamm=1, defense=1)
        playwindow.destroy()
        mainfight(vhardenem,vhardplayer)


    easylev = tkinter.Button(playwindow, text="Easy", background="Green", activebackground="Dark Green", height=2, width=21, command=easylevelpress)
    easylev.place(x=150, y=200)
    mediumlev = tkinter.Button(playwindow, text="Medium", background="Yellow", activebackground="Goldenrod", height=2, width=21, command=mediumlevelpress)
    mediumlev.place(x=320, y=200)
    hardlev = tkinter.Button(playwindow, text="Hard", background="Orange", activebackground="Orange3", height=2, width=21, command=hardlevelpress)
    hardlev.place(x=490, y=200)
    vhardlev = tkinter.Button(playwindow, text="Very Hard", background="Red", activebackground="Red3", height=2, width=21, command=veryhardlevelpress)
    vhardlev.place(x=660, y=200)
    inflev = tkinter.Button(playwindow, text="Infinite", background="Light Blue", activebackground="RoyalBlue1", height=2, width=21)
    inflev.place(x=321, y=250)


    ##################################
    ###    CUSTOM GAME SETTINGS    ###
    ##################################

    def customlevpress():
        global player, enemy

        settingwindow = tkinter.Toplevel(window)
        settingwindow.title("Settings")
        settingwindow.resizable(0, 0)
        settingwindow.geometry("650x650")

        playersprite = tkinter.PhotoImage(file="Media/playersprite.png") 
        playersprlabel = tkinter.Label(settingwindow, image=playersprite)
        playersprlabel.place(x=440, y=100)
        playersprlabel.image = playersprite

        Enemsprite = tkinter.PhotoImage(file="Media/enemysprite.png")
        Enemsprlabel = tkinter.Label(settingwindow, image=Enemsprite)
        Enemsprlabel.place(x=440, y=370)
        Enemsprlabel.image = Enemsprite
        
        def confirmpress():
            settingwindow.destroy()
            playwindow.destroy()
            mainfight(player,enemy)
        
        confirmbuttn = tkinter.Button(settingwindow, text="Play", background='grey', height=2,width=21, command=confirmpress)
        confirmbuttn.place(x=490, y=20)


        def exitsett():
            settingwindow.destroy()

        exitbut = tkinter.Button(settingwindow, text="Back", background='grey', height=2, width=21, command=exitsett)
        exitbut.place(x=4, y=20)

        settingslabel = tkinter.Label(settingwindow, text="Settings", font=('Arial', 25))
        settingslabel.place(x=245, y=40)

        #### PLAYER HEALTH ####
        playerlabel = tkinter.Label(settingwindow, text="Player", font=('Arial', 25))
        playerlabel.place(x=160, y=100)

        health_label = tkinter.Label(settingwindow, text="Player Health:")
        health_label.place(x=50, y=150)
        health_entry = tkinter.Entry(settingwindow)
        health_entry.place(x=160, y=150)
        health_entry.insert(0, str(player.health))

        def update_health():
            try:
                new_health = int(health_entry.get())
                if new_health <= 0 or new_health > 100:
                    tkinter.messagebox.showerror('Out of range', 'Range: 1-100')
                else:
                    player.health = new_health
                    tkinter.messagebox.showinfo('Success!', 'Health Changed Successfully!')
            except ValueError:
                tkinter.messagebox.showerror('Non number value!', 'You entered a non-number.')

        tkinter.Button(settingwindow, text="Set Health", command=update_health).place(x=300, y=150)

        #### PLAYER DAMAGE ####
        damagelabel = tkinter.Label(settingwindow, text="Player Damage:")
        damagelabel.place(x=50, y=200)
        damage_entry = tkinter.Entry(settingwindow)
        damage_entry.place(x=160, y=200)
        damage_entry.insert(0, str(player.damage))

        def updatedamage():
            try:
                new_damage = int(damage_entry.get())
                if new_damage <= 0 or new_damage > 10:
                    tkinter.messagebox.showerror('Out of range', 'Range: 1-10')
                else:
                    player.damage = new_damage
                    tkinter.messagebox.showinfo('Success!', 'Damage Changed Successfully!')
            except ValueError:
                tkinter.messagebox.showerror('Non number value!', 'You entered a non-number.')

        tkinter.Button(settingwindow, text="Set Damage", command=updatedamage).place(x=300, y=200)

        #### PLAYER WEAPON ####
        def show():
            selected_weapon = cb.get()
            player.weapon = selected_weapon
            lbl.config(text=f"Weapon set to: {selected_weapon}")

        WeaponSelectPlayer = ["None", "Sword", "Gun"]
        cb = ttk.Combobox(settingwindow, values=WeaponSelectPlayer)
        cb.set(player.weapon)
        cb.place(x=151, y=250)

        tkinter.Button(settingwindow, text="Set Weapon", command=show).place(x=300, y=250)
        lbl = tkinter.Label(settingwindow, text="")
        lbl.place(x=151, y=280)

        tkinter.Label(settingwindow, text="Player Weapon:").place(x=50, y=250)

        #### ENEMY SECTION ####
        enemylabel = tkinter.Label(settingwindow, text="Enemy", font=('Arial', 25))
        enemylabel.place(x=160, y=340)

        healthEnemy_label = tkinter.Label(settingwindow, text="Enemy Health:")
        healthEnemy_label.place(x=50, y=390)
        healthEnemy_entry = tkinter.Entry(settingwindow)
        healthEnemy_entry.place(x=160, y=390)
        healthEnemy_entry.insert(0, str(enemy.health))

        def updateEnem_health():
            try:
                new_healthEnemy = int(healthEnemy_entry.get())
                if new_healthEnemy <= 0 or new_healthEnemy > 100:
                    tkinter.messagebox.showerror('Out of range', 'Range: 1-100')
                else:
                    enemy.health = new_healthEnemy
                    tkinter.messagebox.showinfo('Success!', 'Health Changed Successfully!')
            except ValueError:
                tkinter.messagebox.showerror('Non number value!', 'You entered a non-number.')

        tkinter.Button(settingwindow, text="Set Health", command=updateEnem_health).place(x=300, y=389)

        #### ENEMY DAMAGE ####
        damageEnemylabel = tkinter.Label(settingwindow, text="Enemy Damage:")
        damageEnemylabel.place(x=50, y=430)
        damageEnemy_entry = tkinter.Entry(settingwindow)
        damageEnemy_entry.place(x=160, y=430)
        damageEnemy_entry.insert(0, str(enemy.damage))

        def updatedEnemamage():
            try:
                newEnemy_damage = int(damageEnemy_entry.get())
                if newEnemy_damage <= 0 or newEnemy_damage > 10:
                    tkinter.messagebox.showerror('Out of range', 'Range: 1-10')
                else:
                    enemy.damage = newEnemy_damage
                    tkinter.messagebox.showinfo('Success!', 'Damage Changed Successfully!')
            except ValueError:
                tkinter.messagebox.showerror('Non number value!', 'You entered a non-number.')

        tkinter.Button(settingwindow, text="Set Damage", command=updatedEnemamage).place(x=300, y=429)
        def showEnem():
            selectedEnem_weapon = cbEnem.get()
            enemy.weapon = selectedEnem_weapon 
            lblEnem.config(text=f"Weapon set to: {selectedEnem_weapon}")  
            print(enemy.weapon)
    
        WeaponSelectEnemy = ["None", "Sword", "Gun"]


        cbEnem = ttk.Combobox(settingwindow, values=WeaponSelectEnemy)
        cbEnem.set(f"{enemy.weapon}")
        cbEnem.place(x=151, y=470)
        confirmEnemweap = tkinter.Button(settingwindow, text="Set Weapon", command=showEnem)
        confirmEnemweap.place(x=300, y=470)
        lblEnem = tkinter.Label(settingwindow, text="")
        lblEnem.place(x=151, y=495)
        weaponEnemlabl = tkinter.Label(settingwindow, text= "Enemy Weapon:")
        weaponEnemlabl.place(x=50, y = 470)
        #### ENEMY RNG ####
        rngEnemylabel = tkinter.Label(settingwindow, text="Enemy RNG:")
        rngEnemylabel.place(x=50, y=520)
        rngEnemy_entry = tkinter.Entry(settingwindow)
        rngEnemy_entry.place(x=160, y=520)
        rngEnemy_entry.insert(0, str(enemy.rng))

        def rngEnem():
            try:
                newEnemy_rng = int(rngEnemy_entry.get())
                if newEnemy_rng <= 0 or newEnemy_rng > 100:
                    tkinter.messagebox.showerror('Out of range', 'Range: 1-100')
                else:
                    enemy.rng = newEnemy_rng
                    tkinter.messagebox.showinfo('Success!', 'RNG Changed Successfully!')
            except ValueError:
                tkinter.messagebox.showerror('Non number value!', 'You entered a non-number.')

        tkinter.Button(settingwindow, text="Set RNG", command=rngEnem).place(x=300, y=519)

    customlev = tkinter.Button(playwindow, text="Custom",background="MediumOrchid1",activebackground="MediumOrchid3",height=2, width=21,command=customlevpress)
    customlev.place(x=489, y=250)

    ##################################
    #### CUSTOM GAME SETTINGS END #### 
    ##################################   

    def backmainpress():
        playwindow.destroy()
    backmain = tkinter.Button(playwindow, text="Back to Menu", background="Gray", activebackground="Dark Gray", height=2, width=21, command=backmainpress)
    backmain.place(x=410, y=350)

    #### level select setup End ####


#### UI buttons handling ####


#### main menu UI ####
def temp():
    pass
logo = tkinter.PhotoImage(file="Media/logo.png")  
logolabel = tkinter.Label(window, image=logo)
logolabel.place(x=0, y=0)  # initial creation, will be overidden later 
playbutton = tkinter.Button(window, text= "Play", background='grey', height= 2, width= 21, command=playpressed)
settingsbuttonmainmenu = tkinter.Button(window, text= "Settings", background='grey', height= 2, width= 21, command = temp)
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
        "Playerhealth" : player.health,
        "Playerdmg" : player.damage,
        "Playerweap" : player.weapon,
        "Enemhealth" : enemy.health,
        "Enemdmg" : enemy.damage,
        "Enemweap" : enemy.weapon,
        "Enemrng" : enemy.rng
    }
    with open(saveloc, "wb") as file:
        pickle.dump(data, file)







window.mainloop()
