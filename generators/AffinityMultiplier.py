__all__ = ["MOD_FOLDER_NAME", "MOD_NAME", "generateMod"]
from _util import *

import base64

MOD_FOLDER_NAME = "AffinityMultiplier" # Folder to store .zips in
MOD_NAME = MOD_FOLDER_NAME+"_P" # base mod name

def generateMod():
    clean_temp()
    # Step 1 : Extract Files
    extract_assets("/Game/Content/GameData/Friend/GDSFriendshipAddSetting","/Game/Content/GameData/Friend/GDSFriendNpcPresentSetting")
    # Step 2 : Convert to json
    convert_all_assets_to_json("*Friend*.*")
    # Step 3 : Edit
    
    # GDSFriendshipAddSetting - Affinity gain
    
    for multiplier in [2, 4, 8, 16]:
        with edit_json("Game/Content/GameData/Friend/GDSFriendshipAddSetting") as friendshipAddData:
            base_map = friendshipAddData["Exports"][0]["Data"][0]["Value"]
            
            for index in base_map:
                index[1]["Value"][1]["Value"] *= multiplier

        # Step 4 : Convert to asset
        convert_all_json_to_asset("*GDSFriendshipAddSetting*")
        
        # Step 5 : Pack mod
        MOD_NAME_VARIANT = MOD_NAME[:-2] + "_x" + str(multiplier) + "_P"
        package_assets(MOD_NAME_VARIANT)

        # Step 6 : zip mod
        zip_mod(MOD_FOLDER_NAME + os.path.sep + MOD_NAME_VARIANT)
        

        # Step 7 : Cleanup
        clean_temp(extracted=False)
        
    # GDSFriendNpcPresentSetting - present friendship value

    with edit_json("Game/Content/GameData/Friend/GDSFriendNpcPresentSetting") as friendPresentData:
        if "RawExport" in friendPresentData["Exports"][0]["$type"]:
            print("GDSFriendNpcPresentSetting didn't convert correctly, waiting on UAssetGUI issue https://github.com/atenfyr/UAssetGUI/issues/190")
            rawData = friendPresentData["Exports"][0]["Data"]
            decRawData = base64.b64decode(rawData)
            decRawData = decRawData.replace(b'\x05\x0A\x0F\x1E\x32',b'\x19\x32\x4B\x96\xFA') # 5 10 15 30 50 -> 25 50 75 150 250
            friendPresentData["Exports"][0]["Data"] = base64.b64encode(decRawData).decode("utf-8")
        else:
            print("GDSFriendNpcPresentSetting DID convert correctly, unexpectedly - LOGIC NOT IMPLEMENTED YET")


    # Step 4 : Convert to asset
    convert_all_json_to_asset("*GDSFriendNpcPresentSetting*")
    
    # Step 5 : Pack mod
    package_assets("AffinityGift_x5_P")

    # Step 6 : zip mod
    zip_mod(MOD_FOLDER_NAME + os.path.sep + "AffinityGift_x5_P")
    

    # Step 7 : Cleanup
    clean_temp()

    
    # TODO: CharaGlobalParam
    #   totalMoveDistanceForFriendship = 120000
    #   totalDefeatEnemyNumForFriendship = 6
    #   totalPickNumForFriendship = 3
    #   totalPickVegetableNumForFriendship = 5
    
if __name__ == "__main__":
    generateMod()
