# Beyond Depth Helper
Simple-to-use console application to somewhat automate tedious tasks when updating modpacks.

## Functions
- Save preferred config files before updating a modpack
- Load saved config files after updating a modpack
- Removed preferred mods after updating
- Copy over preferred mods after updating

## Usage
- All features of this program are optional, use what you want!

### First use
1. Download the [latest version](https://github.com/sassvagyok/bd-helper/releases/latest)
2. On first run, set the path to the **root directory** of the chosen modpack (eg. `C:\Users\matte\curseforge\minecraft\Instances\BeyondDepth`)
3. The newly created `config.json` has some example config files to save and mods to remove, modify the contents of this file to your liking
4. Add mods to `.\saved_mods` that you want to copy over to the modpack's folder after an update

### Before updating the modpack
- Use `Save configs` to save the config file you have added to `config.json`

### After updating the modpack
- Use `Load configs` to load previously saved config files
- Use `Remove mods` to remove mods you have added to `config.json`
- Use `Copy mods` to copy mods from `.\saved_mods` to the modpack's folder