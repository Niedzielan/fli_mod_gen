__all__ = ["MOD_FOLDER_NAME", "MOD_NAME", "generateMod"]
from _util import *

MOD_FOLDER_NAME = "StrongerGear" # Folder to store .zips in
MOD_NAME = MOD_FOLDER_NAME+"_P" # base mod name

def modifyValue(value, exponent, divisor):
    return value + int((value / 10) ** exponent + (value / divisor) - (value / 10) ** (exponent-1))

def generateMod():
    clean_temp()
    # Step 1 : Extract Files
    extract_assets("/Game/Content/GameData/Item/GDSItemWeaponData.uasset", "/Game/Content/GameData/Item/GDSItemArmorData.uasset", "/Game/Content/GameData/Item/GDSItemLifeToolsData.uasset", "/Game/Content/GameData/Item/GDSItemRodData.uasset")
    # Step 2 : Convert to json
    convert_all_assets_to_json("*Item*Data.*")
    # Step 3 : Edit

    with edit_json("/Game/Content/GameData/Item/GDSItemWeaponData.json") as weaponData:
        base_map = weaponData["Exports"][0]["Data"][0]["Value"]
        for data in base_map:
            phys = data[1]["Value"][1]["Value"]
            for i in phys:
                if i["Value"] > 1:
                    i["Value"] = modifyValue(i["Value"], 1.3, 10)
            mag = data[1]["Value"][2]["Value"]
            for i in mag:
                if i["Value"] > 1:
                    i["Value"] = modifyValue(i["Value"], 1.3, 10)

    with edit_json("/Game/Content/GameData/Item/GDSItemLifeToolsData.json") as lifetoolData:
        base_map = lifetoolData["Exports"][0]["Data"][0]["Value"]
        for data in base_map:
            param = data[1]["Value"][2]["Value"]
            for i in param:
                if i["Value"] > 1:
                    i["Value"] = modifyValue(i["Value"], 1.2, 10)

    with edit_json("/Game/Content/GameData/Item/GDSItemRodData.json") as rodData:
        base_map = rodData["Exports"][0]["Data"][0]["Value"]
        for data in base_map:
            param = data[1]["Value"][1]["Value"]
            data[1]["Value"][1]["Value"] = modifyValue(data[1]["Value"][1]["Value"], 1.3, 10)

    with edit_json("/Game/Content/GameData/Item/GDSItemArmorData.json") as weaponData:
        base_map = weaponData["Exports"][0]["Data"][0]["Value"]
        for data in base_map:
            phys = data[1]["Value"][1]["Value"]
            for i in phys:
                if i["Value"] > 1:
                    i["Value"] = modifyValue(i["Value"], 1.3, 5)
            mag = data[1]["Value"][2]["Value"]
            for i in mag:
                if i["Value"] > 1:
                    i["Value"] = modifyValue(i["Value"], 1.3, 5)


    # Step 4 : Convert to asset
    convert_all_json_to_asset()

    # Step 5 : Pack mod
    package_assets(MOD_NAME)

    # Step 6 : zip mod
    zip_mod(MOD_FOLDER_NAME + os.path.sep + MOD_NAME)
    
##    # Step 7 : Cleanup
##    clean_temp()

if __name__ == "__main__":
    generateMod()
