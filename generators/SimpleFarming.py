__all__ = ["MOD_FOLDER_NAME", "MOD_NAME", "generateMod"]
from _util import *

MOD_FOLDER_NAME = "SimpleFarming" # Folder to store .zips in
MOD_NAME = MOD_FOLDER_NAME+"_P" # base mod name

def generateMod():
    clean_temp()
    # Step 1 : Extract Files
    extract_assets("/Game/Content/Program/Craft/common/BP_CraftGlobalParam.uasset", "/Game/Content/GameData/Cultivation/GDSVegetableGrowthTable.uasset")
    # Step 2 : Convert to json
    convert_all_assets_to_json("*CraftGlobalParam.*", "*VegetableGrowthTable.*")
    # Step 3 : Edit

    ## Faster Crop Growth
    example_ArrayProperty = json.loads("""{
                        "$type": "UAssetAPI.PropertyTypes.Objects.ArrayPropertyData, UAssetAPI",
                        "ArrayType": "IntProperty",
                        "Name": "{AP_NAME}",
                        "ArrayIndex": 0,
                        "IsZero": false,
                        "PropertyTagFlags": "None",
                        "PropertyTagExtensions": "NoExtension",
                        "Value": [
                          {
                            "$type": "UAssetAPI.PropertyTypes.Objects.IntPropertyData, UAssetAPI",
                            "Name": "0",
                            "ArrayIndex": 0,
                            "IsZero": false,
                            "PropertyTagFlags": "None",
                            "PropertyTagExtensions": "NoExtension",
                            "Value": 0
                          },
                          {
                            "$type": "UAssetAPI.PropertyTypes.Objects.IntPropertyData, UAssetAPI",
                            "Name": "1",
                            "ArrayIndex": 0,
                            "IsZero": false,
                            "PropertyTagFlags": "None",
                            "PropertyTagExtensions": "NoExtension",
                            "Value": 0
                          },
                          {
                            "$type": "UAssetAPI.PropertyTypes.Objects.IntPropertyData, UAssetAPI",
                            "Name": "2",
                            "ArrayIndex": 0,
                            "IsZero": false,
                            "PropertyTagFlags": "None",
                            "PropertyTagExtensions": "NoExtension",
                            "Value": 1
                          }
                        ]
                      }""")

    with edit_json("Game/Content/Program/Craft/common/BP_CraftGlobalParam.json") as craftGlobalParamData:
        base_map = craftGlobalParamData["Exports"][1]["Data"]

        for new_element_name in ["m_vegetableFieldSeedGrowthTime", "m_vegetableFieldNormalSproutGrowthTime", "m_vegetableFieldBossSproutGrowthTime"]:
            new_element = copy.deepcopy(example_ArrayProperty)
            new_element["Name"] = new_element_name
            new_element["Value"][0]["Value"] = 0 # hours
            new_element["Value"][1]["Value"] = 0 # minutes
            new_element["Value"][2]["Value"] = 1 # seconds
            base_map.append(new_element)
            
    convert_all_json_to_asset()
    MOD_NAME_VARIANT = 'FasterCropGrowth_P'
    package_assets(MOD_NAME_VARIANT)
    zip_mod(MOD_FOLDER_NAME + os.path.sep + MOD_NAME_VARIANT)

    clean_temp(extracted=False)

    ## Simple Farming
    customVegGrowthTables = {
        "NO_WITHER": {
            "seq_10_0000": {"seq_30_0000": (100, 100), "seq_20_0000": (0, 0)},
            "seq_10_0001": {"seq_30_0000": (100, 100), "seq_20_0000": (0, 0)},
        },
        "SIMPLE_100percent": {
            "seq_00_0000": {
                "seq_10_0000": (0, 0),
                "seq_30_0000": (0, 0),
                "seq_10_0001": (0, 0),
                "seq_10_0002": (0, 100),
                "seq_10_0003": (100, 0),
            },
            "seq_10_0000": {"seq_30_0000": (100, 100), "seq_20_0000": (0, 0)},
            "seq_10_0001": {"seq_30_0000": (100, 100), "seq_20_0000": (0, 0)},
            "seq_10_0002": {"seq_30_0001": (100, 0), "seq_30_0000": (0, 100)},
        },
        "SIMPLE_40percent": {
            "seq_00_0000": {
                "seq_10_0000": (0, 0),
                "seq_30_0000": (0, 0),
                "seq_10_0001": (0, 0),
                "seq_10_0002": (60, 100),
                "seq_10_0003": (40, 0),
            },
            "seq_10_0000": {"seq_30_0000": (100, 100), "seq_20_0000": (0, 0)},
            "seq_10_0001": {"seq_30_0000": (100, 100), "seq_20_0000": (0, 0)},
            "seq_10_0002": {"seq_30_0001": (40, 0), "seq_30_0000": (60, 100)},
        },
        "SIMPLE_20percent": {
            "seq_00_0000": {
                "seq_10_0000": (0, 0),
                "seq_30_0000": (0, 0),
                "seq_10_0001": (0, 0),
                "seq_10_0002": (80, 100),
                "seq_10_0003": (20, 0),
            },
            "seq_10_0000": {"seq_30_0000": (100, 100), "seq_20_0000": (0, 0)},
            "seq_10_0001": {"seq_30_0000": (100, 100), "seq_20_0000": (0, 0)},
            "seq_10_0002": {"seq_30_0001": (20, 0), "seq_30_0000": (80, 100)},
        },
        "SIMPLE_5percent": {
            "seq_00_0000": {
                "seq_10_0000": (0, 0),
                "seq_30_0000": (0, 0),
                "seq_10_0001": (0, 0),
                "seq_10_0002": (95, 100),
                "seq_10_0003": (5, 0),
            },
            "seq_10_0000": {"seq_30_0000": (100, 100), "seq_20_0000": (0, 0)},
            "seq_10_0001": {"seq_30_0000": (100, 100), "seq_20_0000": (0, 0)},
            "seq_10_0002": {"seq_30_0001": (5, 0), "seq_30_0000": (95, 100)},
        },
        "SIMPLE_40percent_ALT": {
            "seq_00_0000": {
                "seq_10_0000": (0, 0),
                "seq_30_0000": (0, 0),
                "seq_10_0001": (0, 0),
                "seq_10_0002": (60, 60),
                "seq_10_0003": (40, 40),
            },
            "seq_10_0000": {"seq_30_0000": (100, 100), "seq_20_0000": (0, 0)},
            "seq_10_0001": {"seq_30_0000": (100, 100), "seq_20_0000": (0, 0)},
            "seq_10_0002": {"seq_30_0001": (40, 40), "seq_30_0000": (60, 60)},
        },
        "SIMPLE_20percent_ALT": {
            "seq_00_0000": {
                "seq_10_0000": (0, 0),
                "seq_30_0000": (0, 0),
                "seq_10_0001": (0, 0),
                "seq_10_0002": (80, 80),
                "seq_10_0003": (20, 20),
            },
            "seq_10_0000": {"seq_30_0000": (100, 100), "seq_20_0000": (0, 0)},
            "seq_10_0001": {"seq_30_0000": (100, 100), "seq_20_0000": (0, 0)},
            "seq_10_0002": {"seq_30_0001": (20, 20), "seq_30_0000": (80, 80)},
        },
        "SIMPLE_5percent_ALT": {
            "seq_00_0000": {
                "seq_10_0000": (0, 0),
                "seq_30_0000": (0, 0),
                "seq_10_0001": (0, 0),
                "seq_10_0002": (95, 95),
                "seq_10_0003": (5, 5),
            },
            "seq_10_0000": {"seq_30_0000": (100, 100), "seq_20_0000": (0, 0)},
            "seq_10_0001": {"seq_30_0000": (100, 100), "seq_20_0000": (0, 0)},
            "seq_10_0002": {"seq_30_0001": (5, 5), "seq_30_0000": (95, 95)},
        },
    }

    for variant in customVegGrowthTables:
        customVegGrowthTable = customVegGrowthTables[variant]
        with edit_json("/Game/Content/GameData/Cultivation/GDSVegetableGrowthTable.json") as vegGrowthTableData:
            base_map = vegGrowthTableData["Exports"][0]["Data"][0]["Value"]
            for veg_data in base_map:
                veg_data_id = veg_data[0]["Value"][1]["Value"]
                if veg_data_id in customVegGrowthTable:
                    for inner_veg_data in veg_data[1]["Value"]:
                        if inner_veg_data["Name"] == "Table":
                            for growth_data in inner_veg_data["Value"]:
                                for growth_data_property in growth_data["Value"]:
                                    if growth_data_property["Name"] == "nextTableId":
                                        next_name = growth_data_property["Value"][1]["Value"]
                                    elif growth_data_property["Name"] == "weight_watering":
                                        weight_watering = growth_data_property
                                    elif growth_data_property["Name"] == "weight_notWatering":
                                        weight_notWatering = growth_data_property
                                if next_name in customVegGrowthTable[veg_data_id]:
                                    weight_watering["Value"], weight_notWatering["Value"] = customVegGrowthTable[veg_data_id][next_name]
                            break


        # Step 4 : Convert to asset
        convert_all_json_to_asset()

        # Step 5 : Pack mod
        if variant == "NO_WITHER":
            MOD_NAME_QUALIFIER = '_NoWithering'
        elif variant == "SIMPLE_100percent":
            #MOD_NAME_QUALIFIER = '_Simple_100percentBoss'
            MOD_NAME_QUALIFIER = '_SuperSimple'
        elif variant == "SIMPLE_40percent":
            MOD_NAME_QUALIFIER = '_Simple_40percentBoss'
        elif variant == "SIMPLE_20percent":
            MOD_NAME_QUALIFIER = '_Simple_20percentBoss'
        elif variant == "SIMPLE_5percent":
            MOD_NAME_QUALIFIER = '_Simple_5percentBoss'
        elif variant == "SIMPLE_40percent_ALT":
            MOD_NAME_QUALIFIER = '_Simple_40percentBoss_ALT'
        elif variant == "SIMPLE_20percent_ALT":
            MOD_NAME_QUALIFIER = '_Simple_20percentBoss_ALT'
        elif variant == "SIMPLE_5percent_ALT":
            MOD_NAME_QUALIFIER = '_Simple_5percentBoss_ALT'
        MOD_NAME_VARIANT = MOD_NAME[:-2] + MOD_NAME_QUALIFIER + '_P'
        package_assets(MOD_NAME_VARIANT)

        # Step 6 : zip mod
        zip_mod(MOD_FOLDER_NAME + os.path.sep + MOD_NAME_VARIANT)
        
        # Step 7 : Cleanup
        clean_temp(extracted=False)
    clean_temp()

if __name__ == "__main__":
    generateMod()
