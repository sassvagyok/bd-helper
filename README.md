# Beyond Depth Helper
Simple-to-use console application to somewhat automate tedious tasks when updating Minecraft modpacks.

## Functions
- Save & Load selected config files
- Remove & Copy over selected mods
- Create multiple profiles

## Usage
### First use
1. Download the [latest release](https://github.com/sassvagyok/bd-helper/releases/latest)
2. To get started, create a profile when running the program:
   - First, give the profile a name
   - Then specify the root directory of a modpack (eg. `C:\Users\matte\curseforge\minecraft\Instances\BeyondDepth`)
3. Modify `profiles.json`'s *ConfigsToSave* and *ModsToRemove* fields:
   - Add new config file paths relatively from the set root folder (eg. `config/xaerominimap.txt`)
   - Specified mod names don't have to be the exact file names (eg. `controllable-forge-1.20.1-0.21.7.jar` -> `controllable-forge`)
4. (Optional) Add mods that you want to copy over after an update to `.\saved_mods\{profile_name}` folder

### Before updating the modpack
- Use `Save configs (2)` to save the config files you have added to *ConfigsToSave*

### After updating the modpack
- Use `Load configs (3)` to load previously saved config files
- Use `Remove mods (4)` to remove mods you have added to *ModsToRemove*
- Use `Copy mods (5)` to copy mods from `.\saved_mods\{profile_name}` to the modpack's folder

## Managing profiles
- To change the current profile, use `Select profile (1)`
- For profile management, use `Manage profiles (6)`:
   - To add a new profile, use `Add new profile (1)`
   - To remove a profile, use `Remove profile (2)`