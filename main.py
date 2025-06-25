import shutil, os, profiles, utilities

# Main menu
def mainMenu():
    while True:
        utilities.fancy.clear()
        profiles.processProfiles(0)
        utilities.fancy.clear()

        print(
            utilities.colors.blue + utilities.colors.bold + "\nBeyond Depth Helper v1.5.0\n" +
            utilities.colors.lightgrey + utilities.colors.bold + "\nSelected profile: " + utilities.colors.purple + profiles.selected_profile["Name"] + utilities.colors.reset +
            utilities.colors.reset + utilities.colors.lightgrey + f"\n{utilities.fancy.dashes}\n" +
            utilities.colors.green + " 1 " +
            utilities.colors.lightgrey + "Select profile\n\n" +
            utilities.colors.green + " 2 "+
            utilities.colors.lightgrey+"Save configs\n" +
            utilities.colors.green + " 3 "+
            utilities.colors.lightgrey+"Load configs\n" +
            utilities.colors.green + " 4 "+
            utilities.colors.lightgrey+"Remove mods\n" +
            utilities.colors.green + " 5 "+
            utilities.colors.lightgrey+"Copy mods\n\n" +
            utilities.colors.green + " 6 "+
            utilities.colors.lightgrey+"Manage profiles\n\n" +
            utilities.colors.green + " 9 " +
            utilities.colors.lightgrey + "Help\n" +
            utilities.colors.green + " 0 " +
            utilities.colors.lightgrey + "Exit\n" +
            utilities.colors.reset + utilities.colors.lightgrey + utilities.fancy.dashes
            )
        print()
        try:
            option = int(input("Option: "))
            print()
        except ValueError:
            print(utilities.colors.red + utilities.colors.bold + "Enter a valid option!" + utilities.colors.reset)
            continue

        match option:
            case 0:
                return
            case 1:
                utilities.fancy.clear()
                print(utilities.colors.yellow + utilities.colors.bold + "\nSelect profile\n" + utilities.colors.reset)
                profiles.selectProfile()
            case 2:
                if profiles.processProfiles(2):
                    utilities.fancy.clear()
                    print(utilities.colors.yellow + utilities.colors.bold + "\nSave configs\n" + utilities.colors.reset)
                    saveConfigs()
            case 3:
                if profiles.processProfiles(2):
                    utilities.fancy.clear()
                    print(utilities.colors.yellow + utilities.colors.bold + "\nLoad configs\n" + utilities.colors.reset)
                    loadConfigs()
            case 4:
                if profiles.processProfiles(1):
                    utilities.fancy.clear()
                    print(utilities.colors.yellow + utilities.colors.bold + "\nRemove mods\n" + utilities.colors.reset)
                    removeMods()
            case 5:
                if profiles.processProfiles(0):
                    utilities.fancy.clear()
                    print(utilities.colors.yellow + utilities.colors.bold + "\nCopy mods\n" + utilities.colors.reset)
                    copyMods()
            case 6:
                utilities.fancy.clear()
                print(utilities.colors.yellow + utilities.colors.bold + "\nManage profiles\n" + utilities.colors.reset)
                profileMenu()
            case 9:
                utilities.fancy.clear()
                print(utilities.colors.yellow + utilities.colors.bold + "\nHelp\n" + utilities.colors.reset)
                showHelp()
            case _:
                print(utilities.colors.red + utilities.colors.bold + "Entered option not found!" + utilities.colors.reset)

# Profile menu
def profileMenu():
    while True:
        utilities.fancy.clear()
        profiles.processProfiles(0)
        utilities.fancy.clear()

        print(
            utilities.colors.yellow + utilities.colors.bold + "\nManage profiles\n" +
            utilities.colors.reset +utilities.colors.lightgrey + utilities.colors.bold + "\nSelected profile: " + utilities.colors.purple + profiles.selected_profile["Name"] + utilities.colors.reset +
            utilities.colors.reset + utilities.colors.lightgrey + f"\n{utilities.fancy.dashes}\n" +
            utilities.colors.green + " 1 "+
            utilities.colors.lightgrey+"Add new profile\n" +
            utilities.colors.green + " 2 "+
            utilities.colors.lightgrey+"Remove profile\n\n" +
            utilities.colors.green + " 0 " +
            utilities.colors.lightgrey + "Back\n" +
            utilities.colors.reset + utilities.colors.lightgrey + utilities.fancy.dashes
            )
        print()
        try:
            option = int(input("Option: "))
            print()
        except ValueError:
            print(utilities.colors.red + utilities.colors.bold + "Enter a valid option!" + utilities.colors.reset)
            continue

        match option:
            case 0:
                return
            case 1:
                utilities.fancy.clear()
                print(utilities.colors.yellow + utilities.colors.bold + "\nAdd profile\n" + utilities.colors.reset)
                profiles.addProfile(0)
            case 2:
                utilities.fancy.clear()
                print(utilities.colors.yellow + utilities.colors.bold + "\nRemove profile\n" + utilities.colors.reset)
                profiles.removeProfile()
            case _:
                print(utilities.colors.red + utilities.colors.bold + "Entered option not found!" + utilities.colors.reset)

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
    print(utilities.colors.reset + utilities.colors.lightgrey + "Beyond Depth Helper somewhat automates tedious tasks when updating modpacks.\n")
    print("How to use:\n1. Add as many profiles as you want and select the one you want to work with\n2. Update profiles.json with your preferences and add mods you want to copy over after updating to 'saved_mods' directory\n3. Before updating the modpack, use 'Save configs'\n4. After updating use 'Load configs'\n5. After updating use 'Remove mods'\n6. After updating use 'Copy mods'")

    utilities.waitForInput()

# Save configs
def saveConfigs():
    if os.path.isdir(f"./saved_configs/{profiles.selected_profile["Name"]}"):
        if (getInput(f"There are saved configs for profile '{profiles.selected_profile["Name"]}'. Do you want to overwrite them?")):
            print()
            shutil.rmtree(f"./saved_configs/{profiles.selected_profile["Name"]}")
        else:
            return utilities.waitForInput()

    saved = 0
    for to_save in profiles.configs_to_process:
        src = os.path.join(profiles.path, to_save).replace('/', '\\')
        dst = os.path.join(f"./saved_configs/{profiles.selected_profile["Name"]}", to_save).replace('/', '\\')

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(src):
            if os.path.exists(dst):
                os.remove(dst)

            if os.path.isfile(src):
                shutil.copy(src, dst)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            print(utilities.colors.bold + utilities.colors.green + f"Config saved: " + utilities.colors.reset + utilities.colors.lightgrey + src)
            saved += 1
        else:
            print(utilities.colors.bold + utilities.colors.red + f"Config not found: " + utilities.colors.reset + utilities.colors.lightgrey + src)

    if saved == 0:
        print(utilities.colors.reset + utilities.colors.bold + utilities.colors.red + f"\nFailed to save any configs! ({saved}/{len(profiles.configs_to_process)})")
    else:
        print(utilities.colors.reset + utilities.colors.bold + utilities.colors.green + f"\nSuccessfully saved configs! ({saved}/{len(profiles.configs_to_process)})")

    utilities.waitForInput()

# Load configs
def loadConfigs():
    if not os.path.isdir(f"./saved_configs/{profiles.selected_profile["Name"]}") or len(os.listdir(f"./saved_configs/{profiles.selected_profile["Name"]}")) == 0:
        print(utilities.colors.bold + utilities.colors.red + f"There are no saved configs for profile '{profiles.selected_profile["Name"]}'!")
        return utilities.waitForInput()

    loaded = 0
    for to_save in profiles.configs_to_process:
        src = os.path.join(f"./saved_configs/{profiles.selected_profile["Name"]}", to_save).replace('/', '\\')
        dst = os.path.join(profiles.path, to_save).replace('/', '\\')

        if os.path.exists(src):
            if os.path.exists(dst):
                if os.path.isfile(dst):
                    os.remove(dst)
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
            shutil.move(src, dst)
            print(utilities.colors.bold + utilities.colors.green + f"Config loaded: " + utilities.colors.reset + utilities.colors.lightgrey + src)
            loaded += 1
        else:
            print(utilities.colors.bold + utilities.colors.red + f"Config not found: " + utilities.colors.reset + utilities.colors.lightgrey + src)

    if os.path.isdir(f"./saved_configs/{profiles.selected_profile["Name"]}"):
        shutil.rmtree(f"./saved_configs/{profiles.selected_profile["Name"]}")

    if loaded == 0:
        print(utilities.colors.reset + utilities.colors.bold + utilities.colors.red + f"\nFailed to load any configs! ({loaded}/{len(profiles.configs_to_process)})")
    else:
        print(utilities.colors.reset + utilities.colors.bold + utilities.colors.green + f"\nSuccessfully loaded configs! ({loaded}/{len(profiles.configs_to_process)})")

    utilities.waitForInput()

# Remove mods
def removeMods():
    bd_mods = profiles.path + "\\mods"

    removed = 0
    for mod in profiles.mods_to_remove:
        found = False

        for root, dirs, files in os.walk(bd_mods):
            for file in files:
                if mod.lower() in file.lower():
                    full_path = os.path.join(root, file)
                    print(utilities.colors.bold + utilities.colors.green + f"Mod removed: " + utilities.colors.reset + utilities.colors.lightgrey + mod)
                    os.remove(full_path)
                    removed += 1
                    found = True
                    break
            
            if found:
                break
    
        if not found:
            print(utilities.colors.bold + utilities.colors.red + f"Mod not found: " + utilities.colors.reset + utilities.colors.lightgrey + mod)

    if removed == 0:
        print(utilities.colors.reset + utilities.colors.bold + utilities.colors.red + f"\nFailed to remove any mods! ({removed}/{len(profiles.mods_to_remove)})")
    else:
        print(utilities.colors.reset + utilities.colors.bold + utilities.colors.green + f"\nSuccessfully removed mods! ({removed}/{len(profiles.mods_to_remove)})")

    utilities.waitForInput()

# Copy mods
def copyMods():
    if not os.path.isdir(f"./saved_mods/{profiles.selected_profile["Name"]}") or len(os.listdir(f"./saved_mods/{profiles.selected_profile["Name"]}")) == 0:
        print(utilities.colors.bold + utilities.colors.red + "There are no mods to copy!")

        return utilities.waitForInput()
    
    bd_mods = profiles.path + "\\mods"

    copied = 0
    mods_to_copy = os.listdir(f"./saved_mods/{profiles.selected_profile["Name"]}")
    
    for mod in mods_to_copy:
        src = os.path.join(f"./saved_mods/{profiles.selected_profile["Name"]}", mod).replace('/', '\\')
        dst = os.path.join(bd_mods, mod).replace('/', '\\')
        
        if os.path.isfile(src):
            try:
                if os.path.exists(dst):
                    if not getInput(f"'{mod}' already exists. Do you want to overwrite it?"):
                        print(utilities.colors.bold + utilities.colors.orange + f"Skipped: " + utilities.colors.reset + utilities.colors.lightgrey + mod + utilities.colors.reset)
                        continue
                    os.remove(dst)
                
                shutil.copy2(src, dst)
                print(utilities.colors.bold + utilities.colors.green + f"Mod copied: " + utilities.colors.reset + utilities.colors.lightgrey + mod + utilities.colors.reset)
                copied += 1
            except Exception as e:
                print(utilities.colors.bold + utilities.colors.red + f"Failed to copy: " + utilities.colors.reset + utilities.colors.lightgrey + mod + utilities.colors.reset)
    
    if copied == 0:
        print(utilities.colors.reset + utilities.colors.bold + utilities.colors.red + f"\nFailed to copy mods! ({copied}/{len(mods_to_copy)})")
    else:
        print(utilities.colors.reset + utilities.colors.bold + utilities.colors.green + f"\nSuccessfully copied mods! ({copied}/{len(mods_to_copy)})")

    utilities.waitForInput()

mainMenu()