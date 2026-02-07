__all__ = ["MOD_FOLDER_NAME", "MOD_NAME", "generateMod"]
from _util import *

MOD_FOLDER_NAME = "ShopGuaranteed" # Folder to store .zips in
MOD_NAME = MOD_FOLDER_NAME+"_P" # base mod name

def generateMod():
    clean_temp()
    # Step 1 : Extract Files
    extract_assets("/Game/Content/GameData/Shop", "/Game/Content/Program/Menu/common/BP_MenuGlobalParam")
    # Step 2 : Convert to json
    convert_all_assets_to_json("*TraderShopData.*","*RoguelikeShopData.*", "BP_MenuGlobalParam.*")
    # Step 3 : Edit

    with edit_json("/Game/Content/Program/Menu/common/BP_MenuGlobalParam") as menuGlobalParamData:
        base_map0 = menuGlobalParamData["Exports"][1]["Data"]
        for data in base_map0:
            if data["Name"] == "staffRollScrollTime":
                for new_element in ["traderShopItemCount", "traderShopItemCountRecipe", "roguelikeShopItemCount", "roguelikeShopItemCountRecipe"]:
                    new_data = copy.deepcopy(data)
                    new_data["Name"] = new_element
                    new_data["Value"] = 240
                    new_data["$type"] = "UAssetAPI.PropertyTypes.Objects.BytePropertyData, UAssetAPI"
                    new_data["ByteType"] = "Byte"
                    new_data["EnumType"] = None
                    base_map0.append(new_data)
                break
    for x in ["GDSRoguelikeShopData.json", "GDSTraderShopData.json"]:
        with edit_json("Game/Content/GameData/Shop/"+x) as shopData:
            for i in shopData["Exports"]:
                if i["Data"][0]["Name"] == "m_dataMap":
                    base_map = i["Data"][0]["Value"]
                    break

            for shop in base_map:
                items = shop[1]["Value"][2]["Value"]
                for item in items:
                    for item_property in item["Value"]:
                        if item_property["Name"] == "isLottery":
                            item_property["Value"] = False
                        elif item_property["Name"] == "Rate" and item_property["Value"] != 0:
                            item_property["Value"] = 100


    # Step 4 : Convert to asset
    convert_all_json_to_asset()

    # Step 5 : Pack mod
    package_assets(MOD_NAME)

    # Step 6 : zip mod
    zip_mod(MOD_FOLDER_NAME + os.path.sep + MOD_NAME)

    clean_temp(extracted=False, edited=False)
    
    # Merge peddlers
    peddlers_dict = {}
    item_dict = {}
    with edit_json("../temp/edited/Game/Content/GameData/Shop/GDSTraderShopData") as shopData:
        base_map = shopData["Exports"][0]["Data"][0]["Value"]
        for shop in base_map:
            shop_name = shop[0]["Value"]
            if "peddler" not in shop_name:
                continue
            items = shop[1]["Value"][2]["Value"]
            for item in items:
                for item_property in item["Value"]:
                    if item_property["Name"] == "ItemId":
                        item_name = item_property["Value"]
                        if item_name not in item_dict:
                            item_dict[item_name] = copy.deepcopy(item)
                        if shop_name not in peddlers_dict:
                            peddlers_dict[shop_name] = [item_name]
                        else:
                            peddlers_dict[shop_name].append(item_name)
        for shop in base_map:
            shop_name = shop[0]["Value"]
            if "peddler" not in shop_name:
                continue
            items = shop[1]["Value"][2]["Value"]
            for item in item_dict:
                if item not in peddlers_dict[shop_name]:
                    items.append(item_dict[item])

    # Step 4 : Convert to asset
    convert_all_json_to_asset()

    # Step 5 : Pack mod
    MOD_NAME_VARIANT = MOD_NAME[:-2] + "_MergeTraders" + '_P'
    package_assets(MOD_NAME_VARIANT)

    # Step 6 : zip mod
    zip_mod(MOD_FOLDER_NAME + os.path.sep + MOD_NAME_VARIANT)

    
    
    # Step 7 : Cleanup
    clean_temp()

if __name__ == "__main__":
    generateMod()
