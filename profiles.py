import os, json, utilities

# Update profiles.json
def updateProfiles(new):
    with open("./profiles.json", "w", encoding="utf-8") as f:
        json.dump(new, f, indent=4)

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
        print(utilities.colors.lightgrey + "Welcome to BD Helper. To continue, please add a new profile!")

        addProfile(1)

    f = open("./profiles.json")
    data = json.load(f)
    f.close()

    if len(data) < 2:
        print(utilities.colors.lightgrey + "No profiles found. To continue, please add a new profile!")

        addProfile(1)
    
        f = open("./profiles.json")
        data = json.load(f)
        f.close()

    profiles = data
    selected_profile = data[data[0]["Selected"]]
    path = selected_profile["Path"]

    for i in range(1, len(profiles), 1):
        if not os.path.exists(f"./saved_mods/{profiles[i]["Name"]}"):
            os.mkdir(f"./saved_mods/{profiles[i]["Name"]}")

    if type == 1:
        mods_to_remove = selected_profile["ModsToRemove"]
        if len(mods_to_remove) == 0:
            print(utilities.colors.bold + utilities.colors.red + "Add at least 1 mod under the selected profile to \"ModsToRemove\" inside profiles.json!")

            utilities.waitForInput()

            return False
        
    if type == 2:
        configs_to_process = selected_profile["ConfigsToSave"]
        if len(configs_to_process) == 0:
            print(utilities.colors.bold + utilities.colors.red + "Add at least 1 config file under the selected profile to \"ConfigsToSave\" inside profiles.json!")

            utilities.waitForInput()

            return False
        
    return True

# List added profiles
def listProfiles():
    profiles_formatted = ""
    for i in range(1, len(profiles), 1):
        profiles_formatted += utilities.colors.green + f"\n {i} " + utilities.colors.lightgrey + f"{profiles[i]["Name"]}"

    print(utilities.colors.bold + f"\nAvailable profiles:" + utilities.colors.reset + profiles_formatted + "\n")

# Select profile
def selectProfile():
    global selected_profile

    if processProfiles(0):
        if len(profiles) < 3:
            print(utilities.colors.red + utilities.colors.bold + "There is only one profile added!" + utilities.colors.reset)
            
            return utilities.waitForInput()

        listProfiles()

        while True:
            try:
                selected = int(input(utilities.colors.reset + "Number of selected profile: "))

                if selected > len(profiles) - 1 or selected == 0:
                    print(utilities.colors.red + utilities.colors.bold + "Enter a valid option!" + utilities.colors.reset)
                    continue

                print()
                break
            except ValueError:
                print(utilities.colors.red + utilities.colors.bold + "Enter a valid option!" + utilities.colors.reset)
                continue

        selected_profile = profiles[selected]
        profiles[0]["Selected"] = selected

        updateProfiles(profiles)

        print(utilities.colors.bold + utilities.colors.green + f"Profile '{selected_profile["Name"]}' succesfully selected!")

        utilities.waitForInput()

# Add new profile
def addProfile(type):
    while True:
        name = input(utilities.colors.reset + "Enter the name of the new profile: ")

        if any(c in "\/:*?\"<>|" for c in name):
            print(utilities.colors.bold + utilities.colors.red + "\nProfile name can't contain these characters: '\/:*?\"<>|'\n")
            continue
        if type != 1 and any(profile.get("Name") == name for profile in profiles):
            print(utilities.colors.bold + utilities.colors.red + "\nProfile with the entered name already exists!\n")
            continue
        else:
            break

    while True:
        new_path = input(utilities.colors.reset + "Enter the root directory of a modpack: ")
        if os.path.isdir(new_path):
            break

        print(utilities.colors.bold + utilities.colors.red + "Provided directory not found!")

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

        updateProfiles(d)

        print(utilities.colors.bold + utilities.colors.green + f"\nProfile '{name}' succesfully added and selected! Now replace the examples in 'profiles.json'!" + utilities.colors.reset)

    else:
        profiles.append(
            {
                "Name": name,
                "Path": new_path,
                "ConfigsToSave": [],
                "ModsToRemove": []
            }
        )

        updateProfiles(profiles)

        print(utilities.colors.bold + utilities.colors.green + f"\nProfile '{name}' succesfully added!" + utilities.colors.reset)

    utilities.waitForInput()

# Remove profiles
def removeProfile():
    listProfiles()

    while True:
        try:
            selected = int(input(utilities.colors.reset + "Number of profile to remove: "))

            if selected > len(profiles) - 1 or selected == 0:
                print(utilities.colors.red + utilities.colors.bold + "Enter a valid option!" + utilities.colors.reset)
                continue

            print()
            break
        except ValueError:
            print(utilities.colors.red + utilities.colors.bold + "Enter a valid option!" + utilities.colors.reset)
            continue

    removed = profiles[selected]

    if selected_profile == removed:
        selected_profile == profiles[1]
        profiles[0]["Selected"] = 1

    profiles.pop(selected)
    
    updateProfiles(profiles)

    print(utilities.colors.bold + utilities.colors.green + f"Profile '{removed["Name"]}' succesfully removed!")

    utilities.waitForInput()