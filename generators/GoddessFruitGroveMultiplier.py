__all__ = ["MOD_FOLDER_NAME", "MOD_NAME", "generateMod"]
from _util import *

MOD_FOLDER_NAME = "GoddessFruitGroveMultiplier" # Folder to store .zips in
MOD_NAME = MOD_FOLDER_NAME+"_P" # base mod name

def generateMod():
    clean_temp()
    # Step 1 : Extract Files
    extract_assets("/Game/Content/Program/PlantDungeon/BP_PlantDungeonGlobalParamPreset.uasset")
    # Step 2 : Convert to json
    convert_all_assets_to_json("*PlantDungeonGlobalParam*.*")
    # Step 3 : Edit

    for multiplier in [4, 16]:
        with edit_json("/Game/Content/Program/PlantDungeon/BP_PlantDungeonGlobalParamPreset") as plantGlobalParamData:
            base_map = plantGlobalParamData["Exports"][1]["Data"][0]["Value"]
            for data in base_map:
                if "Name" in data and data["Name"] == "lotFruitTypeInfo":
                    for lotFruit in data["Value"]:
                        lotFruit["Value"][2]["Value"][0]["Value"][0]["Value"] *= multiplier

        # Step 4 : Convert to asset
        convert_all_json_to_asset()

        MOD_NAME_VARIANT = MOD_NAME[:-2] + f"_x{multiplier}" + "_P"
        # Step 5 : Pack mod
        package_assets(MOD_NAME_VARIANT)

        # Step 6 : zip mod
        zip_mod(MOD_FOLDER_NAME + os.path.sep + MOD_NAME_VARIANT)
        
        # Step 7 : Cleanup
        clean_temp(extracted=False, edited=False)
    clean_temp()

if __name__ == "__main__":
    generateMod()
