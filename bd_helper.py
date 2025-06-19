import shutil, os, json, msvcrt

# Console colors
class colors:
    reset = '\033[0m'
    bold = '\033[01m'

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

# # Main menu
def mainMenu():
    clear = lambda: os.system('cls')
    title = "Beyond Depth Helper v1.3.0"
    total_width = len(title) + 16
    dashes = "-" * total_width

    while True:
        clear()
        processProfiles(0)

        print(
            colors.reset + colors.lightgrey + f"\n{dashes}\n" +
            colors.yellow + colors.bold + f"\n\t{title}\n" +
            colors.reset + colors.lightgrey + f"\n{dashes}\n" +
            colors.lightgrey + colors.bold + f"Selected profile: {selected_profile["Name"]}\n\n" + colors.reset +
            colors.green + " 1 " +
            colors.lightgrey + "Select profile\n" +
            colors.green + " 2 "+
            colors.lightgrey+"Add new profile\n" +
            colors.green + " 3 "+
            colors.lightgrey+"Remove profile\n" +
            colors.green + " 4 "+
            colors.lightgrey+"Save configs\n" +
            colors.green + " 5 "+
            colors.lightgrey+"Load configs\n" +
            colors.green + " 6 "+
            colors.lightgrey+"Remove mods\n" +
            colors.green + " 7 "+
            colors.lightgrey+"Copy mods\n\n" +
            colors.green + " 9 " +
            colors.lightgrey + "Help\n" +
            colors.green + " 0 " +
            colors.lightgrey + "Exit\n" +
            colors.reset + colors.lightgrey + dashes
            )
        print()
        try:
            option = int(input("Option: "))
            print()
        except ValueError:
            print(colors.red + colors.bold + "Enter a valid option!" + colors.reset)
            continue

        match option:
            case 0:
                return
            case 1:
                clear()
                print(colors.yellow + colors.bold + "\nSelect profile\n" + colors.reset)
                selectProfile()
            case 2:
                clear()
                print(colors.yellow + colors.bold + "\nAdd profile\n" + colors.reset)
                addProfile(0)
            case 3:
                clear()
                print(colors.yellow + colors.bold + "\nRemove profile\n" + colors.reset)
                removeProfile()
            case 4:
                if processProfiles(2):
                    clear()
                    print(colors.yellow + colors.bold + "\nSave configs\n" + colors.reset)
                    saveConfigs()
            case 5:
                if processProfiles(2):
                    clear()
                    print(colors.yellow + colors.bold + "\nLoad configs\n" + colors.reset)
                    loadConfigs()
            case 6:
                if processProfiles(1):
                    clear()
                    print(colors.yellow + colors.bold + "\nRemove mods\n" + colors.reset)
                    removeMods()
            case 7:
                if processProfiles(0):
                    clear()
                    print(colors.yellow + colors.bold + "\nCopy mods\n" + colors.reset)
                    copyMods()
            case 9:
                clear()
                print(colors.yellow + colors.bold + "\nHelp\n" + colors.reset)
                showHelp()
            case _:
                print(colors.red + colors.bold + "Entered option not found!" + colors.reset)

# Waiting for input
def waitForInput():
    print(colors.bold + colors.lightgrey + "\nPress any button to continue..." + colors.reset, end="", flush=True)
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

# Help
def showHelp():
    print(colors.reset + colors.lightgrey + "Beyond Depth Helper somewhat automates tedious tasks when updating modpacks.\n")
    print("How to use:\n1. Add as many profiles as you want and select the one you want to work with\n2. Update profiles.json with your preferences and add mods you want to copy over after updating to 'saved_mods' directory\n3. Before updating the modpack, use 'Save configs'\n4. After updating use 'Load configs'\n5. After updating use 'Remove mods'\n6. After updating use 'Copy mods'")

    waitForInput()

# Process added profiles
def processProfiles(type):
    global profiles
    global selected_profile
    global path
    global configs_to_process
    global mods_to_remove

    if not os.path.exists("./saved_mods"):
        os.mkdir("./saved_mods")

    if not os.path.exists("./profiles.json"):
        print(colors.lightgrey + "Welcome to BD Helper. To continue, please add a new profile!")

        addProfile(1)

    f = open("./profiles.json")
    data = json.load(f)

    profiles = data
    selected_profile = data[data[0]["Selected"]]
    path = selected_profile["Path"]

    for i in range(1, len(profiles), 1):
        if not os.path.exists(f"./saved_mods/{profiles[i]["Name"]}"):
            os.mkdir(f"./saved_mods/{profiles[i]["Name"]}")

    if type == 1:
        mods_to_remove = selected_profile["ModsToRemove"]
        if len(mods_to_remove) == 0:
            print(colors.bold + colors.red + "Add at least 1 mod under the selected profile to \"ModsToRemove\" inside profiles.json!")
            waitForInput()
            return False
        
    if type == 2:
        configs_to_process = selected_profile["ConfigsToSave"]
        if len(configs_to_process) == 0:
            print(colors.bold + colors.red + "Add at least 1 config file under the selected profile to \"ConfigsToSave\" inside profiles.json!")
            waitForInput()
            return False

    f.close()
        
    return True

# List added profiles
def listProfiles():
    if len(profiles) < 3:
        print(colors.red + colors.bold + "There is only one profile added!" + colors.reset)
        return False

    profiles_formatted = ""
    for i in range(1, len(profiles), 1):
        profiles_formatted += colors.green + f"\n {i} " + colors.lightgrey + f"{profiles[i]["Name"]}"

    print(colors.bold + f"\nAvailable profiles:" + colors.reset + profiles_formatted + "\n")

# Select profile
def selectProfile():
    global selected_profile

    if processProfiles(0):
        if listProfiles() == False:
            return waitForInput()

        while True:
            try:
                selected = int(input(colors.reset + "Number of selected profile: "))

                if selected > len(profiles) - 1 or selected == 0:
                    print(colors.red + colors.bold + "Enter a valid option!" + colors.reset)
                    continue

                print()
                break
            except ValueError:
                print(colors.red + colors.bold + "Enter a valid option!" + colors.reset)
                continue

        selected_profile = profiles[selected]

        profiles[0]["Selected"] = selected

        with open("./profiles.json", "w", encoding="utf-8") as f:
            json.dump(profiles, f, indent=4)

        print(colors.bold + colors.green + f"Profile '{selected_profile["Name"]}' succesfully selected!")

        waitForInput()

# Add new profile
def addProfile(type):
    while True:
        name = input(colors.reset + "Enter the name of the new profile: ")

        if (type != 1 and any(profile.get("Name") == name for profile in profiles)):
            print(colors.bold + colors.red + "\nProfile with the entered name already exists!\n")
            continue
        else:
            break

    while True:
        new_path = input(colors.reset + "Enter the root directory of a modpack: ")
        if os.path.isdir(new_path):
            break
        print(colors.bold + colors.red + "Provided directory not found!")

    if type == 1:
        d = [
            {
                "Selected": 1
            },
            {
                "Name": name,
                "Path": new_path,
                "ConfigsToSave": [
                    "config/example.json"
                ],
                "ModsToRemove": [
                    "examplemod"
                ]
            }
        ]

        with open("./profiles.json", "w", encoding="utf-8") as f:
            json.dump(d, f, indent=4)

        print(colors.bold + colors.green + f"\nProfile '{name}' succesfully added and selected! Now replace the examples in 'profiles.json'!" + colors.reset)

    else:
        profiles.append(
            {
                "Name": name,
                "Path": new_path,
                "ConfigsToSave": [],
                "ModsToRemove": []
            }
        )

        with open("./profiles.json", "w", encoding="utf-8") as f:
            json.dump(profiles, f, indent=4)

        print(colors.bold + colors.green + f"\nProfile '{name}' succesfully added!" + colors.reset)

    waitForInput()

# Remove profiles
def removeProfile():
    if listProfiles() == False:
        return waitForInput()

    while True:
        try:
            selected = int(input(colors.reset + "Number of profile to remove: "))

            if selected > len(profiles) - 1 or selected == 0:
                print(colors.red + colors.bold + "Enter a valid option!" + colors.reset)
                continue

            print()
            break
        except ValueError:
            print(colors.red + colors.bold + "Enter a valid option!" + colors.reset)
            continue

    removed = profiles[selected]

    if selected_profile == removed:
        print("a")
        selected_profile == profiles[1]
        profiles[0]["Selected"] = 1

    profiles.pop(selected)
    
    with open("./profiles.json", "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=4)

    print(colors.bold + colors.green + f"Profile '{removed["Name"]}' succesfully removed!")

    waitForInput()

# Save configs
def saveConfigs():
    if os.path.isdir(f"./saved_configs/{selected_profile["Name"]}"):
        if (getInput(f"There are saved configs for profile '{selected_profile["Name"]}'. Do you want to overwrite them?")):
            print()
            shutil.rmtree(f"./saved_configs/{selected_profile["Name"]}")
        else:
            return waitForInput()

    saved = 0
    for to_save in configs_to_process:
        src = os.path.join(path, to_save).replace('/', '\\')
        dst = os.path.join(f"./saved_configs/{selected_profile["Name"]}", to_save).replace('/', '\\')

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(src):
            if os.path.exists(dst):
                os.remove(dst)
            shutil.copy(src, dst)
            print(colors.bold + colors.green + f"Config saved: " + colors.reset + colors.lightgrey + src)
            saved += 1
        else:
            print(colors.bold + colors.red + f"Config not found: " + colors.reset + colors.lightgrey + src)

    if saved == 0:
        print(colors.reset + colors.bold + colors.red + f"\nFailed to save any configs! ({saved}/{len(configs_to_process)})")
    else:
        print(colors.reset + colors.bold + colors.green + f"\nSuccessfully saved configs! ({saved}/{len(configs_to_process)})")

    waitForInput()

# Load configs
def loadConfigs():
    if not os.path.isdir(f"./saved_configs/{selected_profile["Name"]}") or len(os.listdir(f"./saved_configs/{selected_profile["Name"]}")) == 0:
        print(colors.bold + colors.red + f"There are no saved configs for profile '{selected_profile["Name"]}'!")
        return waitForInput()

    loaded = 0
    for to_save in configs_to_process:
        src = os.path.join(f"./saved_configs/{selected_profile["Name"]}", to_save).replace('/', '\\')
        dst = os.path.join(path, to_save).replace('/', '\\')

        if os.path.exists(src):
            if os.path.exists(dst):
                os.remove(dst)
            shutil.move(src, dst)
            print(colors.bold + colors.green + f"Config loaded: " + colors.reset + colors.lightgrey + src)
            loaded += 1
        else:
            print(colors.bold + colors.red + f"Config not found: " + colors.reset + colors.lightgrey + src)

    if os.path.isdir(f"./saved_configs/{selected_profile["Name"]}"):
        shutil.rmtree(f"./saved_configs/{selected_profile["Name"]}")

    if loaded == 0:
        print(colors.reset + colors.bold + colors.red + f"\nFailed to load any configs! ({loaded}/{len(configs_to_process)})")
    else:
        print(colors.reset + colors.bold + colors.green + f"\nSuccessfully loaded configs! ({loaded}/{len(configs_to_process)})")

    waitForInput()

# Remove mods
def removeMods():
    bd_mods = path + "\\mods"

    removed = 0
    for mod in mods_to_remove:
        found = False

        for root, dirs, files in os.walk(bd_mods):
            for file in files:
                if mod.lower() in file.lower():
                    full_path = os.path.join(root, file)
                    print(colors.bold + colors.green + f"Mod removed: " + colors.reset + colors.lightgrey + mod)
                    os.remove(full_path)
                    removed += 1
                    found = True
                    break
            
            if found:
                break
    
        if not found:
            print(colors.bold + colors.red + f"Mod not found: " + colors.reset + colors.lightgrey + mod)

    if removed == 0:
        print(colors.reset + colors.bold + colors.red + f"\nFailed to remove any mods! ({removed}/{len(mods_to_remove)})")
    else:
        print(colors.reset + colors.bold + colors.green + f"\nSuccessfully removed mods! ({removed}/{len(mods_to_remove)})")

    waitForInput()

# Copy mods
def copyMods():
    if not os.path.isdir(f"./saved_mods/{selected_profile["Name"]}") or len(os.listdir(f"./saved_mods/{selected_profile["Name"]}")) == 0:
        print(colors.bold + colors.red + "There are no mods to copy!")
        waitForInput()
    
    bd_mods = path + "\\mods"

    copied = 0
    mods_to_copy = os.listdir(f"./saved_mods/{selected_profile["Name"]}")
    
    for mod in mods_to_copy:
        src = os.path.join(f"./saved_mods/{selected_profile["Name"]}", mod).replace('/', '\\')
        dst = os.path.join(bd_mods, mod).replace('/', '\\')
        
        if os.path.isfile(src):
            try:
                if os.path.exists(dst):
                    if not getInput(f"'{mod}' already exists. Do you want to overwrite it?"):
                        print(colors.bold + colors.orange + f"Skipped: " + colors.reset + colors.lightgrey + mod + colors.reset)
                        continue
                    os.remove(dst)
                
                shutil.copy2(src, dst)
                print(colors.bold + colors.green + f"Mod copied: " + colors.reset + colors.lightgrey + mod + colors.reset)
                copied += 1
            except Exception as e:
                print(colors.bold + colors.red + f"Failed to copy: " + colors.reset + colors.lightgrey + mod + colors.reset)
    
    if copied == 0:
        print(colors.reset + colors.bold + colors.red + f"\nFailed to copy mods! ({copied}/{len(mods_to_copy)})")
    else:
        print(colors.reset + colors.bold + colors.green + f"\nSuccessfully copied mods! ({copied}/{len(mods_to_copy)})")

    waitForInput()

mainMenu()