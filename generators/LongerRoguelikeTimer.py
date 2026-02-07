__all__ = ["MOD_FOLDER_NAME", "MOD_NAME", "generateMod"]
from _util import *

MOD_FOLDER_NAME = "LongerRoguelikeTimer" # Folder to store .zips in
MOD_NAME = MOD_FOLDER_NAME+"_P" # base mod name

def generateMod():
    clean_temp()
    # Step 1 : Extract Files
    extract_assets("/Game/Content/Program/Roguelike/BP_RoguelikeGlobalParam.uasset")
    # Step 2 : Convert to json
    convert_all_assets_to_json("*RoguelikeGlobalParam.*")
    # Step 3 : Edit

    with edit_json("Game/Content/Program/Roguelike/BP_RoguelikeGlobalParam.json") as roguelikeGlobalParamData:
        base_map = roguelikeGlobalParamData["Exports"][1]["Data"]
        for data in base_map:
            if data["Name"] == "roguelikeTimeLimit":
                data["Value"] = 7200
                new_data = copy.deepcopy(data)
                new_data["Name"] = "challengeTimeLimit"
                new_data["Value"] = 1800
                base_map.append(new_data)

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
