__all__ = ["MOD_FOLDER_NAME", "MOD_NAME", "generateMod"]
from _util import *

MOD_FOLDER_NAME = "ItemMultiplier" # Folder to store .zips in
MOD_NAME = "ExtraDropTable_P" # base mod name

def generateMod():
    clean_temp()
    # Step 1 : Extract Files
    extract_assets("/Game/Content/GameData/Item")
    if os.path.exists("../temp/extracted/Game/Content/GameData/ItemCraft"):
        shutil.rmtree("../temp/extracted/Game/Content/GameData/ItemCraft")
    # Step 2 : Convert to json
    convert_all_assets_to_json("GDSBattleItemTableSetting.*","GDSCommonItemTableSetting.*", "GDSBattleItemTableGroupSetting.*")
    # Step 3 : Edit

    allowed_cond = ["CondCmd_ActiveEventMultiFeatureEnable_True",
                    "CondCmd_GetGlobalItemGetFlag_True",
                    "CondCmd_GetGlobalItemGetFlag_False",
                    "CondCmd_DropOwnerLevelNotLessThan",
                    "CondCmd_DropOwnerLevelNotGreaterThan",
                    "CondCmd_Phase_Greater",
                    "CondCmd_IsRoguelikeAreaClearCount_Equal",
                    "CondCmd_IsRoguelikeAreaClearCount_Greater",
                    "CondCmd_IsRoguelikeBossType",
                    "CondCmd_AvatarLife_Equal"]

    whitelist_important = ["iky01000880",
                           "iky01000190",
                           "iky01000420",
                           "iky01000430",
                           "iky01000330"] # golden cluster, goddess fruit, clestia's gift, gold celestia's gift, myserious slate

    search_content = open_json("Game/Content/GameData/Item/GDSBattleItemTableSetting")

    tables = []

    base_map = search_content["Exports"][0]["Data"][0]["Value"]
    for table in base_map:
        has_nonstackable = False
        table_name = table[0]["Value"]
        for item in table[1]["Value"][1]["Value"]:
            item_name = item["Value"][0]["Value"]
            if not (item_name.startswith("ics") or item_name.startswith("imt") or item_name.startswith("irt") or item_name in whitelist_important):
                has_nonstackable = True
                break
        if not has_nonstackable:
            tables.append(table_name)

    

    tables2 = []

    base_map = search_content["Exports"][0]["Data"][0]["Value"]
    for table in base_map:
        has_nonstackable = False
        table_name = table[0]["Value"]
        for item in table[1]["Value"][1]["Value"]:
            item_name = item["Value"][0]["Value"]
            if not (item_name.startswith("ics") or item_name.startswith("imt") or item_name.startswith("irt") or item_name.startswith("ive") or item_name.startswith("irp") or item_name in whitelist_important):
                has_nonstackable = True
                break
        if not has_nonstackable:
            tables2.append(table_name)


    tables3 = []

    base_map = search_content["Exports"][0]["Data"][0]["Value"]
    for table in base_map:
        has_nonstackable = False
        table_name = table[0]["Value"]
        for item in table[1]["Value"][1]["Value"]:
            item_name = item["Value"][0]["Value"]
            if not (item_name.startswith("iam") or item_name.startswith("iwp") or item_name.startswith("ilt") or item_name.startswith("ics") or item_name.startswith("imt") or item_name.startswith("irt") or item_name in whitelist_important):
                has_nonstackable = True
                break
        if not has_nonstackable:
            tables3.append(table_name)

    for ITEM_MULTIPLIER in [1, 2, 4, 8, 16, "16_4"]:
        if (type(ITEM_MULTIPLIER) == int and ITEM_MULTIPLIER > 1) or (type(ITEM_MULTIPLIER) == str and int(ITEM_MULTIPLIER.split("_")[0]) > 1):
            with edit_json("Game/Content/GameData/Item/GDSCommonItemTableSetting") as common_content:
                base_common_map = common_content["Exports"][0]["Data"][0]["Value"]
                for common in base_common_map:
                    common_list = common[1]["Value"][1]["Value"]
                    for common_item in common_list:
                        common_name = common_item["Value"][0]["Value"]
                        if common_name.startswith("ics") or common_name.startswith("imt") or common_name.startswith("irt") or common_name in whitelist_important:
                            for tmp in common_item["Value"]:
                                tmp_name = tmp["Name"]
                                if tmp_name == "cond":
                                    if len(tmp["Value"]) == 0:
                                        common_item["Value"][1]["Value"] *= (ITEM_MULTIPLIER if type(ITEM_MULTIPLIER) == int else int(ITEM_MULTIPLIER.split("_")[0]))
                                    break
        add_rate = [0]
        if ITEM_MULTIPLIER == 1:
            add_rate = [10, 50, 100]
        for rate in add_rate:
            for all_mats in [False, True]:
                if type(ITEM_MULTIPLIER) == str and not all_mats:
                    continue
##                if all_mats:
##                    print("Step 4.c - Creating Battle Table Content for multiplier: " + str(ITEM_MULTIPLIER) + " [Materials + Gear]")
##                else:
##                    print("Step 4.c - Creating Battle Table Content for multiplier: " + str(ITEM_MULTIPLIER) + " [Materials]")
                with edit_json("Game/Content/GameData/Item/GDSBattleItemTableGroupSetting") as group_content:
                    base_group_map = group_content["Exports"][0]["Data"][0]["Value"]

                    for group in base_group_map:
                        group_name = group[0]["Value"]
                        group_list = group[1]["Value"][1]["Value"]
                        new_list = []
                        for group_stuff in group_list:
                            group_table_name = group_stuff["Value"][1]["Value"]
                            if rate > 0 and (all_mats or group_table_name in tables2):
                                cur_rate = group_stuff["Value"][0]["Value"]
                                group_stuff["Value"][0]["Value"] = min(100, cur_rate+rate)
                            group_table_cond = group_stuff["Value"][3]["Value"]
                            cond_allow = True
                            if len(group_table_cond) != 0:
                                for tmp_cond in group_table_cond:
                                    tmp_cond_name = tmp_cond["Value"][0]["Value"]
                                    if tmp_cond_name not in allowed_cond:
                                        cond_allow = False
                            if type(ITEM_MULTIPLIER) == int:
                                if cond_allow and ((all_mats and group_table_name in tables3) or (group_table_name in tables)):
                                    for i in range(ITEM_MULTIPLIER-1):
                                        new_list.append(copy.deepcopy(group_stuff))
                            elif type(ITEM_MULTIPLIER) == str:
                                if cond_allow:
                                    mat_mult = int(ITEM_MULTIPLIER.split("_")[0])
                                    gear_mult = int(ITEM_MULTIPLIER.split("_")[1])
                                    if group_table_name in tables:
                                        for i in range(mat_mult-1):
                                            new_list.append(copy.deepcopy(group_stuff))
                                    elif group_table_name in tables3:
                                        for i in range(gear_mult-1):
                                            new_list.append(copy.deepcopy(group_stuff))
                                        
                                        
                    
                        group_list += new_list

                # Step 4 : Convert to asset
                convert_all_json_to_asset()

                # Step 5 : Pack mod
                if rate > 0:
                    mod_qualifier = "_+"+str(rate)+"%_rate"
                else:
                    mod_qualifier = "_x"+str(ITEM_MULTIPLIER)
                if all_mats:
                    mod_qualifier += "_ALL"
                else:
                    mod_qualifier += "_MAT"
                MOD_NAME_VARIANT = MOD_NAME[:-2] + mod_qualifier + "_P"
                package_assets(MOD_NAME_VARIANT)

                # Step 6 : zip mod
                zip_mod(MOD_FOLDER_NAME + os.path.sep + MOD_NAME_VARIANT)
                
                # Step 7 : Cleanup
                clean_temp(extracted=False, edited=False)
    clean_temp()

if __name__ == "__main__":
    generateMod()
