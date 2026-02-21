__all__ = ["MOD_FOLDER_NAME", "MOD_NAME", "generateMod"]
from _util import *

MOD_FOLDER_NAME = "AreaPointMultiplier" # Folder to store .zips in
MOD_NAME = MOD_FOLDER_NAME+"_P" # base mod name

def generateMod():
    clean_temp()
    # Step 1 : Extract Files
    extract_assets("/Game/Content/GameData/Map/GDSAreaPoint.uasset", "/Game/Content/GameData/Quest/GDSActiveEventRewardData.uasset")
    # Step 2 : Convert to json
    convert_all_assets_to_json("*AreaPoint.*", "*ActiveEventRewardData.*")
    # Step 3 : Edit

    for multiplier in [2, 4, 8]:
        with edit_json("/Game/Content/GameData/Map/GDSAreaPoint") as areaPointData:
            base_map = areaPointData["Exports"][0]["Data"][0]["Value"]

            for area in base_map:
                for item in area[1]["Value"][1]["Value"]:
                    item["Value"] *= multiplier


        with edit_json("/Game/Content/GameData/Quest/GDSActiveEventRewardData") as activeEventRewardData:
            base_map1 = activeEventRewardData["Exports"][0]["Data"][0]["Value"]

            for typ in base_map1:
                for item in typ[1]["Value"][1]["Value"]:
                    if item["Name"] == "AreaPoint":
                        item["Value"] *= multiplier

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
