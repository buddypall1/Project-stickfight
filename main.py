import tkinter
from tkinter import ttk
import tkinter.messagebox
import pickle
from PIL import Image, ImageTk
import random

saveloc = "Data/game_data.dat"

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

    def __init__(self, health, damage, weapon):
        self.health = health
        self.damage = damage
        self.weapon = weapon
    
    def __str__(self):
        return f'{self.weapon} {self.damage} {self.weapon}'

class Enemparams():

    def __init__(self, health, damage, rng, weapon):
        self.health= health
        self.damage = damage
        self.rng = rng
        self.weapon = weapon

class LevelEnemparams():

    def __init__(self,health,damage,rng,weapon,healsamm):
        self.health = health
        self.damage = damage
        self.rng = rng
        self.weapon = weapon
        self.healsamm = healsamm

class LevelPlayerparams():

    def __init__(self, health, damage, weapon,healsamm):
        self.health = health
        self.damage = damage
        self.weapon = weapon
        self.healsamm = healsamm

#### player and enemy obj creation #### 

player = Playerparams(gamedata['Playerhealth'], gamedata['Playerdmg'], gamedata['Playerweap']) # CUSTOM GAME PLAYER!!!
enemy = Enemparams(gamedata['Enemhealth'], gamedata['Enemdmg'], gamedata['Enemrng'], gamedata['Enemweap']) # CUSTOM GAME ENEMY!!!

    ##################################
    ###       BATTLE LOGIC         ###
    ##################################

def mainfight(enemy, player):
    battlewindow = tkinter.Toplevel(window)
    battlewindow.title("Battle!")
    battlewindow.resizable(0, 0)
    battlewindow.geometry("1080x800")




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
    
    ##################################
    ###      EASY LEVEL LOGIC      ###
    ##################################

    def easylevelpress():
        easyenem = LevelEnemparams(health=50, damage=random.randint(1,5), rng=25, weapon="None", healsamm=2)
        easyplayer = LevelPlayerparams(health=100, damage=random.randint(1,15), weapon="Gun", healsamm=10)
        playwindow.destroy()
        mainfight(easyenem, easyplayer)
    
    def mediumlevelpress():
        mediumenem = LevelEnemparams(health=100, damage=random.randint(1,10), rng=35, weapon="Sword", healsamm=5)
        mediumplayer = LevelPlayerparams(health=100, damage=random.randint(1,10), weapon="Sword", healsamm=5)
        playwindow.destroy()
        mainfight(mediumenem,mediumplayer)
    
    def hardlevelpress():
        hardenem= LevelEnemparams(health=150, damage=random.randint(3,15), rng=45, weapon="Gun",healsamm=8)
        hardplayer = LevelPlayerparams(health=85, damage=random.randint(2,13),weapon="None",healsamm=3)
        playwindow.destroy()
        mainfight(hardenem,hardplayer)

    def veryhardlevelpress():
        vhardenem= LevelEnemparams(health=200, damage=random.randint(5,20), rng=70, weapon="Gun",healsamm=10)
        vhardplayer = LevelPlayerparams(health=50,damage=random.randint(3,15),weapon="None",healsamm=1)
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
