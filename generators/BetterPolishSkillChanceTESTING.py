__all__ = ["MOD_FOLDER_NAME", "MOD_NAME", "generateMod"]
from _util import *

MOD_FOLDER_NAME = "BetterPolishSkillChance" # Folder to store .zips in
MOD_NAME = MOD_FOLDER_NAME+"_P" # base mod name

def generateMod():
    clean_temp()
    # Step 1 : Extract Files
    extract_assets("/Game/Content/GameData/Skill/GDSSkillData.uasset")
    # Step 2 : Convert to json
    convert_all_assets_to_json("GDSSkillData.*")
    
    for multiplier in [10, 25, 50, 100]:#[2, 4, 8, 16]:
        with edit_json("/Game/Content/GameData/Skill/GDSSkillData.json") as skillData:
##            skillData = open_json("/Game/Content/GameData/Skill/GDSSkillData.json")
            base_map = skillData["Exports"][0]["Data"][0]["Value"]
            m_autostr = skillData["Exports"][0]["Data"][-1]#["Value"]
            m_autobin = skillData["Exports"][0]["Data"][-2]["Value"]
            for skill in base_map:
                skillName = skill[0]["Value"][1]["Value"]
                if "ps_equip_ex_" not in skillName:
                    continue
                print(skillName)
                for skillProperty in skill[1]["Value"]:
                    if "battle" in skillName or "gather" in skillName:
                        if skillProperty["Name"] == "skillEffectInfoList":
                            for skillEffectInfoParam in skillProperty["Value"][0]["Value"]:
                                if skillEffectInfoParam["Name"] == "effCondList":
                                    effCondArg = skillEffectInfoParam["Value"][0]["Value"][1]["Value"][0]
                                    m_offset = effCondArg["Value"][0]["Value"]
                                    m_dataSize = effCondArg["Value"][1]["Value"]
                                    if m_dataSize == 0:
                                        continue
                                    cur_type, cur_val = get_m_data(m_autobin, m_autostr, m_offset, m_dataSize)
                                    m_val = cur_val * multiplier
                                    set_m_data(m_autobin, m_autostr, m_offset, m_dataSize, m_val)
                    elif "craft" in skillName:
                        if skillProperty["Name"] == "Params":
                            param_0 = skillProperty["Value"][0]["Value"][0]
                            m_offset = param_0["Value"][0]["Value"]
                            m_dataSize = param_0["Value"][1]["Value"]
                            if m_dataSize == 0:
                                continue
                            cur_type, cur_val = get_m_data(m_autobin, m_autostr, m_offset, m_dataSize)
                            m_val = cur_val * multiplier
                            set_m_data(m_autobin, m_autostr, m_offset, m_dataSize, m_val)
                    
        # Step 4 : Convert to asset
        convert_all_json_to_asset()

        # Step 5 : Pack mod
        MOD_NAME_VARIANT = MOD_NAME[:-2]+"_x"+str(multiplier)+'_P'
        package_assets(MOD_NAME_VARIANT)

        # Step 6 : zip mod
        zip_mod(MOD_FOLDER_NAME + os.path.sep + MOD_NAME_VARIANT)
        
        # Step 7 : Cleanup
        clean_temp(extracted=False)
    clean_temp()

if __name__ == "__main__":
    generateMod()
