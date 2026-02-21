__all__ = ["MOD_FOLDER_NAME", "MOD_NAME", "generateMod"]
from _util import *

MOD_FOLDER_NAME = "ExpMultiplier" # Folder to store .zips in
MOD_NAME = MOD_FOLDER_NAME+"_P" # base mod name

def generateMod():
    clean_temp()
    # Step 1 : Extract Files
    extract_assets("/Game/Content/GameData/Chara/GDSExpLevelConfig.uasset")
    # Step 2 : Convert to json
    convert_all_assets_to_json("*ExpLevel*.*")
    # Step 3 : Edit

    for multiplier in [2, 4, 8, 16, 255]:
        with edit_json("/Game/Content/GameData/Chara/GDSExpLevelConfig") as expData:
            

            base_map = expData["Exports"][0]["Data"][0]["Value"]

            for expConfig in base_map:
                expLevelConfig = expConfig[1]["Value"][1]["Value"]
                for expInfo in expLevelConfig:
                    expInfoInner = expInfo["Value"][1]
                    if not expInfoInner["IsZero"]:
                        #print(expInfoInner["Value"])
                        expInfoInner["Value"] *= multiplier 

        # Step 4 : Convert to asset
        convert_all_json_to_asset()

        # Step 5 : Pack mod
        MOD_NAME_VARIANT = MOD_NAME[:-2] + "_x" + str(multiplier) + "_P"
        package_assets(MOD_NAME_VARIANT)

        # Step 6 : zip mod
        zip_mod(MOD_FOLDER_NAME + os.path.sep + MOD_NAME_VARIANT)

        # Step 7 : Cleanup
        clean_temp(extracted=False)
    clean_temp()

if __name__ == "__main__":
    generateMod()
