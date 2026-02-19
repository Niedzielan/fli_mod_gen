__all__ = ["MOD_FOLDER_NAME", "MOD_NAME", "generateMod"]
from _util import *

MOD_FOLDER_NAME = "WeakDragonTESTING" # Folder to store .zips in
MOD_NAME = MOD_FOLDER_NAME+"_P" # base mod name


# para_enm12400301
# para_enm12400301_weak
def generateMod():
    clean_temp()
    # Step 1 : Extract Files
    extract_assets("/Game/Content/GameData/Chara/GDSCharaParameterEnemy.uasset")
    # Step 2 : Convert to json
    convert_all_assets_to_json("*CharaParam*.*")
    # Step 3 : Edit

    with edit_json("/Game/Content/GameData/Chara/GDSCharaParameterEnemy.json") as charaData:
        base_map = charaData["Exports"][0]["Data"][0]["Value"]
        for data in base_map:
            name = data[0]["Value"][1]["Value"]
            if not name.startswith("para_enm12400301"):
                continue
            baseParamMin = data[1]["Value"][0]
            for i in baseParamMin["Value"]:
                if i["Name"] == "hp":
                    i["Value"] = 10
                elif i["Name"] in ["physicalOffense", "physicalDefense", "magicOffense", "magicDefense"]:
                    i["Value"] = 10
            baseParamMax = data[1]["Value"][3]
            for i in baseParamMax["Value"]:
                if i["Name"] == "hp":
                    i["Value"] = 10
                elif i["Name"] in ["physicalOffense", "physicalDefense", "magicOffense", "magicDefense"]:
                    i["Value"] = 10


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
