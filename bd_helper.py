import shutil, os, json, msvcrt

# Console colors
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

# Main menu
def mainMenu():
    title = "Beyond Depth Helper v1.2.0"
    total_width = len(title) + 16
    dashes = "-" * total_width

    while True:
        processConfig(0)

        print(
            colors.reset + colors.fg.lightgrey + f"\n{dashes}\n" +
            colors.fg.yellow + colors.bold + f"\n\t{title}\n" + 
            colors.reset + colors.fg.lightgrey + f"\n{dashes}\n" +
            colors.fg.green + " 1 " +
            colors.fg.lightgrey + "Change path\n" +
            colors.fg.green + " 2 "+
            colors.fg.lightgrey+"Save configs\n" +
            colors.fg.green + " 3 "+
            colors.fg.lightgrey+"Load configs\n" +
            colors.fg.green + " 4 "+
            colors.fg.lightgrey+"Remove mods\n" +
            colors.fg.green + " 5 "+
            colors.fg.lightgrey+"Copy mods\n\n" +
            colors.fg.green + " 9 " +
            colors.fg.lightgrey + "Help\n" +
            colors.fg.green + " 0 " +
            colors.fg.lightgrey + "Exit\n" +
            colors.reset + colors.fg.lightgrey + dashes
            )
        print()
        try:
            option = int(input("Option: "))
            print()
        except ValueError:
            print(colors.fg.red + colors.bold + "Enter a valid option!" + colors.reset)
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
            case 5:
                if processConfig(0):
                    copyMods()
            case 9:
                showHelp()
            case _:
                print(colors.fg.red + colors.bold + "Entered option not found!" + colors.reset)

# Waiting for input
def waitForInput():
    print(colors.bold + colors.fg.lightgrey + "\nPress a button to continue...", end="", flush=True)
    msvcrt.getch()
    print()

# Yes/No choice
def getInput(q):
    while True:
        answer = input(f"{q} [y/n]: ").strip().lower()
        if answer in ["yes", "y"]:
            return True
        elif answer in ["no", "n"]:
            return False
        else:
            continue

# Processing config.json
def processConfig(type):
    global mods_to_remove
    global bd_config
    global bd_path

    if not os.path.exists("./saved_mods"):
        os.mkdir("./saved_mods")

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
            print(f"Set path: {data["BDPath"]}")
        while True:
            new_path = input(colors.reset + "Enter the root directory of a modpack: ")
            if os.path.isdir(new_path):
                break
            print(colors.bold + colors.fg.red + "Provided directory not found!")

        data["BDPath"] = new_path
        with open("./config.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print(colors.bold + colors.fg.green + "Path added successfully!")

    bd_path = data["BDPath"]

    if type == 2:
        mods_to_remove = data["ModsToRemove"]
        if len(mods_to_remove) == 0:
            print(colors.bold + colors.fg.red + "Add at least 1 mod to \"ModsToRemove\" inside config.json!")
            return False
        
    if type == 3:
        bd_config = data["ConfigsToSave"]
        if len(bd_config) == 0:
            print(colors.bold + colors.fg.red + "Add at least 1 config file to \"ConfigsToSave\" inside config.json!")
            return False

    f.close()
        
    return True

# Help
def showHelp():
    print(colors.reset + colors.fg.lightgrey + "Beyond Depth Helper somewhat automates tedious tasks when updating modpacks.\n")
    print("How to use:\n1. Set the root directory of the desired modpack\n2. Update config.json with your preferences and add mods you want to copy over after updating to 'saved_mods' directory\n3. Before updating the modpack, use 'Save configs'\n4. After updating use 'Load configs'\n5. After updating use 'Remove mods'\n6. After updating use 'Copy mods'")

    waitForInput()

# Save configs
def saveConfigs():
    if os.path.isdir("./saved_configs"):
        if (getInput("There are saved configs, do you want to overwrite them?")):
            print()
            shutil.rmtree("./saved_configs")
        else:
            return waitForInput()

    saved = 0
    for to_save in bd_config:
        src = os.path.join(bd_path, to_save).replace('/', '\\')
        dst = os.path.join("./saved_configs", to_save).replace('/', '\\')

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(src):
            if os.path.exists(dst):
                os.remove(dst)
            shutil.copy(src, dst)
            print(colors.bold + colors.fg.green + f"Config saved: " + colors.reset + colors.fg.lightgrey + src)
            saved += 1
        else:
            print(colors.bold + colors.fg.red + f"Config not found: " + colors.reset + colors.fg.lightgrey + src)

    if saved == 0:
        print(colors.reset + colors.bold + colors.fg.red + f"\nFailed to save configs! ({saved}/{len(bd_config)})")
    else:
        print(colors.reset + colors.bold + colors.fg.green + f"\nSuccessfully saved configs! ({saved}/{len(bd_config)})")

    waitForInput()

# Load configs
def loadConfigs():
    if not os.path.isdir("./saved_configs") or len(os.listdir("./saved_configs")) == 0:
        print(colors.bold + colors.fg.red + "There are no saved configs!")
        waitForInput()

    loaded = 0
    for to_save in bd_config:
        src = os.path.join("./saved_configs", to_save).replace('/', '\\')
        dst = os.path.join(bd_path, to_save).replace('/', '\\')

        if os.path.exists(src):
            if os.path.exists(dst):
                os.remove(dst)
            shutil.move(src, dst)
            print(colors.bold + colors.fg.green + f"Config loaded: " + colors.reset + colors.fg.lightgrey + src)
            loaded += 1
        else:
            print(colors.bold + colors.fg.red + f"Config not found: " + colors.reset + colors.fg.lightgrey + src)

    if os.path.isdir("./saved_configs"):
        shutil.rmtree("./saved_configs")

    if loaded == 0:
        print(colors.reset + colors.bold + colors.fg.red + f"\nFailed to load configs! ({loaded}/{len(bd_config)})")
    else:
        print(colors.reset + colors.bold + colors.fg.green + f"\nSuccessfully loaded configs! ({loaded}/{len(bd_config)})")

    waitForInput()

# Remove mods
def removeMods():
    bd_mods = bd_path + "\\mods"

    removed = 0
    for mod in mods_to_remove:
        found = False

        for root, dirs, files in os.walk(bd_mods):
            for file in files:
                if mod.lower() in file.lower():
                    full_path = os.path.join(root, file)
                    print(colors.bold + colors.fg.green + f"\nMod removed: " + colors.reset + colors.fg.lightgrey + mod)
                    os.remove(full_path)
                    removed += 1
                    found = True
                    break
            
            if found:
                break
    
        if not found:
            print(colors.bold + colors.fg.red + f"Mod not found: " + colors.reset + colors.fg.lightgrey + mod)

    if removed == 0:
        print(colors.reset + colors.bold + colors.fg.red + f"\nFailed to remove mods! ({removed}/{len(mods_to_remove)})")
    else:
        print(colors.reset + colors.bold + colors.fg.green + f"\nSuccessfully removed mods! ({removed}/{len(mods_to_remove)})")

    waitForInput()

# Copy mods
def copyMods():
    if not os.path.isdir("./saved_mods") or len(os.listdir("./saved_mods")) == 0:
        print(colors.bold + colors.fg.red + "There are no mods to copy!")
        waitForInput()
    
    bd_mods = bd_path + "\\mods"

    copied = 0
    mods_to_copy = os.listdir("./saved_mods")
    
    for mod in mods_to_copy:
        src = os.path.join("./saved_mods", mod).replace('/', '\\')
        dst = os.path.join(bd_mods, mod).replace('/', '\\')
        
        if os.path.isfile(src):
            try:
                if os.path.exists(dst):
                    if not getInput(f"'{mod}' already exists. Do you want to overwrite it?"):
                        print(colors.bold + colors.fg.yellow + f"Skipped: " + colors.reset + colors.fg.lightgrey + mod)
                        continue
                    os.remove(dst)
                
                shutil.copy2(src, dst)
                print(colors.bold + colors.fg.green + f"Mod copied: " + colors.reset + colors.fg.lightgrey + mod)
                copied += 1
            except Exception as e:
                print(colors.bold + colors.fg.red + f"Failed to copy: " + colors.reset + colors.fg.lightgrey + mod)
    
    if copied == 0:
        print(colors.reset + colors.bold + colors.fg.red + f"\nFailed to copy mods! ({copied}/{len(mods_to_copy)})")
    else:
        print(colors.reset + colors.bold + colors.fg.green + f"\nSuccessfully copied mods! ({copied}/{len(mods_to_copy)})")

    waitForInput()

mainMenu()