__all__ = ["MOD_FOLDER_NAME", "MOD_NAME", "generateMod"]
from _util import *

MOD_FOLDER_NAME = "BetterDropExpDoshSkills" # Folder to store .zips in
MOD_NAME = MOD_FOLDER_NAME+"_P" # base mod name

def generateMod():
    clean_temp()
    # Step 1 : Extract Files
    extract_assets("/Game/Content/GameData/Skill/GDSSkillData.uasset")
    # Step 2 : Convert to json
    convert_all_assets_to_json("*SkillData.*")
    # Step 3 : Edit

    effect_type_whitelist = ["drop_item_up", "gain_rich_up", "gain_exp_up", "gain_all_exp_up"]

    for multiplier in [2, 4, 8, 16]:
        with edit_json("/Game/Content/GameData/Skill/GDSSkillData.json") as skillData:
##            skillData = open_json("/Game/Content/GameData/Skill/GDSSkillData.json")
            base_map = skillData["Exports"][0]["Data"][0]["Value"]
            m_autostr = skillData["Exports"][0]["Data"][-1]#["Value"]
            m_autobin = skillData["Exports"][0]["Data"][-2]["Value"]
            for skill in base_map:
                is_whitelist = False
                for skillProperty in skill[1]["Value"]:
                    if skillProperty["Name"] == "Params":
                        skillParams = skillProperty
                    elif skillProperty["Name"] == "skillEffectInfoList":
                        # for each skill effect, if effId not in effect_type_whitelist, move to next skill
                        # or does each correspond to a skill param of the same index? if so can buff individual effects
                        for skillEffectInfo in skillProperty["Value"]:
                            if skillEffectInfo["Value"][0]["Value"] in effect_type_whitelist:
                                is_whitelist = True
                            else:
                                is_whitelist = False
                                break
                if is_whitelist:
                    for skillParam in skillParams["Value"][0]["Value"]:
                        m_offset = skillParam["Value"][0]["Value"]
                        m_dataSize = skillParam["Value"][1]["Value"]
                        if m_dataSize == 0:
                            continue
                        cur_type, cur_val = get_m_data(m_autobin, m_autostr, m_offset, m_dataSize)
                        #m_type = cur_type
                        m_val = cur_val * multiplier
                        set_m_data(m_autobin, m_autostr, m_offset, m_dataSize, m_val)
##            save_json(skillData, "/Game/Content/GameData/Skill/GDSSkillData.json")
                    
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
