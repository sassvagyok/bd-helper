import shutil, os, json, msvcrt

# Konzol színek
class colors:
    reset = '\033[0m'
    bold = '\033[01m'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

# Főmenü
def mainMenu():
    while True:
        processConfig(0)
        print(
            colors.reset + colors.fg.lightgrey + "\n----------------------------------------\n" +
            colors.fg.yellow + colors.bold + "\n\tBeyond Depth Helper v1.1.0\t\n" + 
            colors.reset + colors.fg.lightgrey + "\n----------------------------------------\n" +
            colors.fg.green + " 1 " +
            colors.fg.lightgrey + "Elérési útvonal megváltotatása\n" +
            colors.fg.green + " 2 "+
            colors.fg.lightgrey+"Beállítások mentése\n" +
            colors.fg.green + " 3 "+
            colors.fg.lightgrey+"Beállítások betöltése\n" +
            colors.fg.green + " 4 "+
            colors.fg.lightgrey+"Modok törlése\n\n" +
            colors.fg.green + " 0 " +
            colors.fg.lightgrey + "Kilépés\n" +
            colors.reset + colors.fg.lightgrey+"----------------------------------------"
            )
        print()
        try:
            option = int(input("Választott opció: "))
            print()
        except ValueError:
            print(colors.fg.red + colors.bold + "Számot adj meg!" + colors.reset)
            continue

        match option:
            case 0:
                return
            case 1:
                processConfig(1)
            case 2:
                if processConfig(3):
                    saveConfigs()
            case 3:
                if processConfig(3):
                    loadConfigs()
            case 4:
                if processConfig(2):
                    removeMods()
            case _:
                print(colors.fg.red + colors.bold + "Opció nem található!" + colors.reset)

# Gombnyomásra várás
def waitForInput():
    print(colors.bold + colors.fg.lightgrey + "\nNyomj egy gombot a folytatáshoz...", end="", flush=True)
    msvcrt.getch()
    print()

# Yes/No eldöntés
def getInput(q):
    while True:
        answer = input(f"{q} [y/n]: ").strip().lower()
        if answer in ["yes", "y"]:
            return True
        elif answer in ["no", "n"]:
            return False
        else:
            continue

# Config.json feldolgozása
def processConfig(type):
    global mods_to_remove
    global bd_config
    global bd_path

    if not os.path.exists("./config.json"):
        d = {
            "BDPath": "",
            "ConfigsToSave": [
                "options.txt",
                "config/xaerominimap.txt",
                "config/xaeroworldmap.txt",
                "config/betterdays-common.toml",
                "config/majruszsdifficulty.json",
                "config/borninconfiguration-general.toml",
                "config/incontrol/spawn.json",
                "config/simplyswords_extra/loot_config.json5",
                "kubejs/server_scripts/custom.js"
            ],
            "ModsToRemove": [
                "vivecraft",
                "vivecraftcompat",
                "firstperson",
                "shouldersurfing",
                "controllable",
                "bettercombat",
                "do_a_barrel_roll"
            ]
        }

        with open("./config.json", "w", encoding="utf-8") as f:
            json.dump(d, f, indent=4)

    f = open("./config.json")
    data = json.load(f)

    if data["BDPath"] == "" or not os.path.isdir(data["BDPath"]) or type == 1:
        if type == 1:
            print(f"Beállított útvonal: {data["BDPath"]}")
        while True:
            new_path = input(colors.reset + "Add meg a Beyond Depth mappáját: ")
            if os.path.isdir(new_path):
                break
            print(colors.bold + colors.fg.red + "A megadott mappa nem található!")

        data["BDPath"] = new_path
        with open("./config.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print(colors.bold + colors.fg.green + "Elérési útvonal sikeresen hozzáadva!")

    bd_path = data["BDPath"]

    if type == 2:
        mods_to_remove = data["ModsToRemove"]
        if len(mods_to_remove) == 0:
            print(colors.bold + colors.fg.red + "Adj hozzá leglább 1 modot a config.json-ba!")
            return False
        
    if type == 3:
        bd_config = data["ConfigsToSave"]
        if len(bd_config) == 0:
            print(colors.bold + colors.fg.red + "Adj hozzá leglább 1 beállítás fájlt a config.json-ba!")
            return False

    f.close()
        
    return True

# Configok mentése
def saveConfigs():
    if os.path.isdir("./saved_configs"):
        if (getInput("Már vannak mentett beállítások, felül akarod ezeket írni?")):
            print()
            shutil.rmtree("./saved_configs")
        else:
            return

    saved = 0
    for to_save in bd_config:
        src = os.path.join(bd_path, to_save).replace('/', '\\')
        dst = os.path.join("./saved_configs", to_save).replace('/', '\\')

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(src):
            if os.path.exists(dst):
                os.remove(dst)
            shutil.copy(src, dst)
            print(colors.bold + colors.fg.green + f"Beállítás elmentve: {src}")
            saved += 1
        else:
            print(colors.bold + colors.fg.red + f"Beállítás nem található: {src}")

    if saved == 0:
        print(colors.reset + colors.bold + colors.fg.red + f"\nBeállítások elmentése sikertelen! ({saved}/{len(bd_config)})")
    else:
        print(colors.reset + colors.bold + colors.fg.green + f"\nBeállítások elmentve! ({saved}/{len(bd_config)})")

    waitForInput()

# Configok betöltése
def loadConfigs():
    if not os.path.isdir("./saved_configs") or len(os.listdir("./saved_configs")) == 0:
        return print(colors.bold + colors.fg.red + "Nincsenek mentett beállítások!")

    loaded = 0
    for to_save in bd_config:
        src = os.path.join("./saved_configs", to_save).replace('/', '\\')
        dst = os.path.join(bd_path, to_save).replace('/', '\\')

        if os.path.exists(src):
            if os.path.exists(dst):
                os.remove(dst)
            shutil.move(src, dst)
            print(colors.bold + colors.fg.green + f"Beállítás betöltve: {src}")
            loaded += 1
        else:
            print(colors.bold + colors.fg.red + f"Beállítás nem található: {src}")

    if os.path.isdir("./saved_configs"):
        shutil.rmtree("./saved_configs")

    if loaded == 0:
        print(colors.reset + colors.bold + colors.fg.red + f"\nBeállítások betöltése sikertelen! ({loaded}/{len(bd_config)})")
    else:
        print(colors.reset + colors.bold + colors.fg.green + f"\nBeállítások betöltve! ({loaded}/{len(bd_config)})")

    waitForInput()

# Modok törlése
def removeMods():
    bd_mods = bd_path + "\\mods"

    removed = 0
    for mod in mods_to_remove:
        found = False

        for root, dirs, files in os.walk(bd_mods):
            for file in files:
                if mod.lower() in file.lower():
                    full_path = os.path.join(root, file)
                    print(colors.bold + colors.fg.green + f"\nMod törölve: {mod}")
                    os.remove(full_path)
                    removed += 1
                    found = True
                    break
            
            if found:
                break
    
        if not found:
            print(colors.bold + colors.fg.red + f"Mod nem található: {mod}")

    if removed == 0:
        print(colors.reset + colors.bold + colors.fg.red + f"\nModok törlése sikertelen! ({removed}/{len(mods_to_remove)})")
    else:
        print(colors.reset + colors.bold + colors.fg.green + f"\nModok törölve! ({removed}/{len(mods_to_remove)})")

    waitForInput()

mainMenu()