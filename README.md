# Beyond Depth Helper
Simple-to-use console application to somewhat automate tedious tasks when updating modpacks.

## Functions
- Save selected config files
- Load saved config files
- Remove preferred mods
- Copy over preferred mods
- Create different profiles for different modpacks

## Usage
- All features of this program are optional, use what you want!

### First use
1. Download the [latest release](https://github.com/sassvagyok/bd-helper/releases/latest)
2. On first use, you will be prompted to add a new profile. Name it, then set the path to the root directory of the chosen modpack (eg. `C:\Users\matte\curseforge\minecraft\Instances\BeyondDepth`)
3. Modify `profiles.json`'s `ConfigsToSave` and `ModsToRemove` fields to your prefered settings
   - Add new config file paths relatively from the set root folder (eg. `config/xaerominimap.txt`)
   - Name mods as accurately as possible (you can drop the version) (eg. `controllable-forge-1.20.1-0.21.7.jar` -> `controllable-forge`)
4. Add mods to `.\saved_mods\{profile_name}` that you want to copy over after an update

### Managing profiles
- To add a new profile use `Add new profile`. You can add as many profiles as you want as long as the name isn't a duplicate of an already existing profile
- To change the current profile, use `Select profile`
- To remove a profile, use `Remove profile`. If the removed profile is the one currently in use, the new selected profile will be the first profile added
- You can check the selected profile above the options

### Before updating the modpack
- Use `Save configs` to save the config file you have added to `profiles.json`

### After updating the modpack
- Use `Load configs` to load previously saved config files
- Use `Remove mods` to remove mods you have added to `profiles.json`
- Use `Copy mods` to copy mods from `.\saved_mods\{profile_name}` to the modpack's folder