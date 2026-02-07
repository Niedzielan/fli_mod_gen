# fli_mod_gen
Automatically generate mods for Fantasy Life i

## Usage

1.  
Modify config.ini:  
Note that a mapping needs to be loaded in via UAssetGUI. To do so, go into tools and run UAssetGUI, then Utils -> import mappings, and select a Fantasy Life i usmap  
You can either manually dump a .usmap using UE4SS or download one from https://github.com/DRayX/FLi-FModel  
In config.ini change the MAPPING= name to your loaded UE4SS.  
If the encryption has changed, change AES_KEY=. The encryption key can also be found in https://github.com/DRayX/FLi-FModel  
Also change GAME_DIRECTORY= to point to your Fantasy Life i game directory  

2.  
Each python file in generators will create a set of mod files in output  
Either run gen.py to generate every mod, or run the generators individually in the generators folder.  



## credits

retoc by trumank : https://github.com/trumank/retoc  
UAssetGUI by atenfyr : https://github.com/atenfyr/UAssetGUI  