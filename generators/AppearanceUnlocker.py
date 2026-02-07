__all__ = ["MOD_FOLDER_NAME", "MOD_NAME", "generateMod"]
from _util import *

MOD_FOLDER_NAME = "AppearanceUnlocker" # Folder to store .zips in
MOD_NAME = MOD_FOLDER_NAME+"_P" # base mod name

def generateMod():
    clean_temp()
    # Step 1 : Extract Files
    extract_assets("/Game/Content/GameData/Avatar/")
    # Step 2 : Convert to json
    convert_all_assets_to_json("*AvatarEyePartsData.*","*AvatarHairModelData.*","*AvatarOptionPartsData.*")
    # Step 3 : Edit

    for partDataFilename in ["GDSAvatarEyePartsData", "GDSAvatarHairModelData", "GDSAvatarOptionPartsData"]:
        partDataData = open_json("Game/Content/GameData/Avatar/"+partDataFilename)
        base_map = partDataData["Exports"][0]["Data"][0]["Value"]

        for part in base_map:
            for part_property in part[1]["Value"]:
                if part_property["Name"] == "cond":
                    part_property["Value"] = []

        save_json(partDataData, "Game/Content/GameData/Avatar/"+partDataFilename)

    # Step 4 : Convert to asset
    convert_all_json_to_asset()

    # Step 5 : Pack mod
    package_assets(MOD_NAME)

    # Step 6 : zip mod
    zip_mod(MOD_FOLDER_NAME + os.path.sep + MOD_NAME)
    

    # Step 7 : Cleanup
    clean_temp()
    
if __name__ == "__main__":
    generateMod()
