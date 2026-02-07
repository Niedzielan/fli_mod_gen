__all__ = ["MOD_FOLDER_NAME", "MOD_NAME", "generateMod"]
from _util import *

MOD_FOLDER_NAME = "IncreasedEventSpawns" # Folder to store .zips in
MOD_NAME = MOD_FOLDER_NAME+"_P" # base mod name

def generateMod():
    clean_temp()
    # Step 1 : Extract Files
    extract_assets("/Game/Content/common/RPG/BP_RpgGlobalParam.uasset")
    # Step 2 : Convert to json
    convert_all_assets_to_json("*RpgGlobalParam.*")
    # Step 3 : Edit

    with edit_json("/Game/Content/common/RPG/BP_RpgGlobalParam") as rpgGlobalParamData:
        base_map = rpgGlobalParamData["Exports"][1]["Data"]
        added_bool = False
        for data in base_map:
            if data["Name"] == "appearActiveEventNum":
                data["Value"] = 120
            elif not added_bool and (data["Name"] in ["EnableAutoDecideJumpWhenFallThroughInDungeonTree","combineUpdatePhaseIndexOnActiveEventReset", "isEnableAutoRotateCameraToRear"]):
                new_data = copy.deepcopy(data)
                new_data["Name"] = "preventLegendEventMultipleEmergingOnSolo"
                new_data["Value"] = False
                base_map.append(new_data)
                added_bool = True

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
