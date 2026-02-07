__all__ = ["MOD_FOLDER_NAME", "MOD_NAME", "generateMod"]
from _util import *

MOD_FOLDER_NAME = "ImprovedCamera" # Folder to store .zips in
MOD_NAME = MOD_FOLDER_NAME+"_P" # base mod name

def generateMod():
    clean_temp()
    # Step 1 : Extract Files
    extract_assets("/Game/Content/BluePrints/Camera")
    if os.path.exists("../temp/extracted/Game/Content/BluePrints/Camera/CameraShake"):
        shutil.rmtree("../temp/extracted/Game/Content/BluePrints/Camera/CameraShake")
        os.remove("../temp/extracted/Game/Content/BluePrints/Camera/BP_HugeMapChaseCameraActorMap000200.uasset")
        os.remove("../temp/extracted/Game/Content/BluePrints/Camera/BP_HugeMapChaseCameraActorMap000200.uexp")
    # Step 2 : Convert to json
    convert_all_assets_to_json("BP_BaseCamp*.*","BP_ChaseCamera*.*","BP_ChaseOffset*.*", "BP_Dungeon*.*", "BP_Huge*.*")
    # Step 3 : Edit

    for default_fov in [90, 75, 60]:
        for root, directories, files in os.walk("../temp/extracted"):
            for fil in files:
                fil_path = os.path.join(root, fil)
                fil_main, fil_ext = ".".join(fil_path.split(".")[:-1]), fil_path.split(".")[-1]
                if fil_ext != "json":
                    continue
                with edit_json(fil_path[len("../temp/extracted"):]) as cameraData:
                    base_map = cameraData["Exports"][1]["Data"]
                    for data in base_map:
                        data_name = data["Name"]
                        if data_name == "m_chaseCameraLen":
                            continue # change CameraLenLookUp and CameraLenLookDown, maybe?
                        elif data_name == "m_photoModeParam":
                            data["Value"][0]["Value"] = 105 # MaxFov
                            data["Value"][1]["Value"] = 10 # MinFov
                            continue # change MaxFov, MinFov
                        elif data_name == "m_chaseCameraFov":
                            cameraFovArray = data["Value"][0]
                            cameraFovArray["Value"].append(copy.deepcopy(cameraFovArray["Value"][0]))
                            cameraFovArray["Value"].append(copy.deepcopy(cameraFovArray["Value"][1]))
                            cameraFovArray["Value"][0]["Value"] = 90
                            cameraFovArray["Value"][1]["Value"] = 75
                            cameraFovArray["Value"][2]["Name"] = "2"
                            cameraFovArray["Value"][3]["Name"] = "3"
                            while default_fov < cameraFovArray["Value"][0]["Value"]:
                                cameraFovArray["Value"][0]["Value"], cameraFovArray["Value"][1]["Value"], cameraFovArray["Value"][2]["Value"], cameraFovArray["Value"][3]["Value"] = cameraFovArray["Value"][1]["Value"], cameraFovArray["Value"][2]["Value"], cameraFovArray["Value"][3]["Value"], cameraFovArray["Value"][0]["Value"]
                            continue # add more to CameraFovArray
                        elif data_name == "m_basicSP":
                            for basicSP in data["Value"]:
                                if basicSP["Name"] == "RotLookDown_Ver":
                                    basicSP["Value"] = -89
                                elif basicSP["Name"] == "RotLookUp_Ver":
                                    basicSP["Value"] = 40
                            continue # change RotLookDown_Ver to -89, RotLookUp_Ver to 40
                    base_map2 = cameraData["Exports"][2]["Data"]
                    for data2 in base_map2:
                        if data2["Name"] == "FieldOfView":
                            if data2["Value"] < default_fov:
                                data2["Value"] = default_fov

        # Step 4 : Convert to asset
        convert_all_json_to_asset()

        # Step 5 : Pack mod
        MOD_NAME_VARIANT = MOD_NAME[:-2]+'_'+str(default_fov)+'_P'
        package_assets(MOD_NAME_VARIANT)

        # Step 6 : zip mod
        zip_mod(MOD_FOLDER_NAME + os.path.sep + MOD_NAME_VARIANT)
        
        # Step 7 : Cleanup
        clean_temp(extracted=False)
    clean_temp()

if __name__ == "__main__":
    generateMod()
