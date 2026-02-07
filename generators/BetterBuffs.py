__all__ = ["MOD_FOLDER_NAME", "MOD_NAME", "generateMod"]
from _util import *

MOD_FOLDER_NAME = "BetterBuffs" # Folder to store .zips in
MOD_NAME = MOD_FOLDER_NAME+"_P" # base mod name

def generateMod():
    clean_temp()
    # Step 1 : Extract Files
    extract_assets("/Game/Content/GameData/Item/GDSItemConsumeData.uasset", "/Game/Content/GameData/Battle/GDSBattleAddStatus.uasset")
    # Step 2 : Convert to json
    convert_all_assets_to_json("*ItemConsumeData.*", "*BattleAddStatus.*")
    # Step 3 : Edit

      ##    None = 0,                    
      ##    Hp = 1,                   
      ##    Sp = 2,                   
      ##    HpPercent = 3,                 
      ##    SpPercent = 4,               
      ##    AutoHealHp = 5,              
      ##    Revival = 6,                 
      ##    AllHealStatus = 7,           
      ##    HealPoison = 8,              
      ##    HealParalysis = 9,           
      ##    HealFrostbite = 10,          
      ##    HealBurn = 11,                   
      ##    OffenseUp = 12,              
      ##    DefenseUp = 13,              
      ##    DefenseDown = 14,            
      ##    MagicOffenseUp = 15,         
      ##    MagicDefenseUp = 16,         
      ##    KnockbackDisable = 17,       
      ##    TensionGaugeGainUp = 18,     
      ##    CiriticalRateUp = 19,        
      ##    DamageCut = 20,              
      ##    Invincible = 21,             
      ##    MeatCook = 22,               
      ##    FishCook = 23,               
      ##    EggCook = 24,                
      ##    DessertCook = 25,         
      ##    VegetablesCook = 26,      
      ##    PotCook = 27,                
      ##    ComboCook = 28,              
      ##    KnockbackDisableCook = 29,   
      ##    Exp = 30,                    
      ##    Other = 31,               
      ##    EItemEffectType_MAX = 32,

    val_map = {1: 20,
               2: 40,
               3: 70,
               4: 100,
               5: 150,
               6: 200}

    uses_val_map = [22, 23, 24, 25, 26, 27, 28] # *Cook type
    blacklist_types = []

    player_buffs = ["add_st_b01_offence_up_01", "add_st_b01_offence_up_02", "add_st_b04_use_sp_down_00", "add_st_b04_use_sp_down_01", "add_st_b04_defence_up_01_01", "add_st_b04_defence_up_01_02", "add_st_b04_defence_up_02_01", "add_st_b04_defence_up_02_02", "add_st_b04_superarmor", "add_st_b04_heal"]

    for time_multiplier in [1, 2, 5, 20]:
        if time_multiplier > 1:
            with edit_json("Game/Content/GameData/Battle/GDSBattleAddStatus") as battleStatusData:
                base_map0 = battleStatusData["Exports"][0]["Data"][0]["Value"]
                for battleStatus in base_map0:
                    if battleStatus[0]["Value"] in player_buffs:
                        for statusProperty in battleStatus[1]["Value"]:
                            if statusProperty["Name"] == "addStEffInfo":
                                for statusEffectProperty in statusProperty["Value"][0]["Value"]:
                                    if statusEffectProperty["Name"] == "cancelValue":

                                        statusEffectProperty["Value"] = min(32000, statusEffectProperty["Value"]*min(5,time_multiplier))

        for value_multiplier in [1, 2, 5, 10]:
            if value_multiplier == 1 and time_multiplier == 1:
                continue
            with edit_json("Game/Content/GameData/Item/GDSItemConsumeData") as itemConsumeData:
                base_map = itemConsumeData["Exports"][0]["Data"][0]["Value"]
                for consumable in base_map:
                    for consumable_property in consumable[1]["Value"]:
                        if consumable_property["Name"].startswith("effParam"):
                            effect_type = 0
                            for effect_property in consumable_property["Value"]:
                                if effect_property["Name"] == "val":
                                    effect_val = effect_property
                                elif effect_property["Name"] == "Time":
                                    effect_time = effect_property
                                elif effect_property["Name"] == "itemEffectType":
                                    effect_type = effect_property["Value"]
                                
                            if effect_type > 0 and effect_type not in blacklist_types:

                                if effect_type in uses_val_map and value_multiplier > 1:
                                    effect_val["Value"] = val_map[effect_val["Value"]]
                                effect_val["Value"] *= value_multiplier
                                effect_val["Value"] = min(32000, effect_val["Value"])
                                effect_time["Value"] *= time_multiplier
                                effect_time["Value"] = min(32000, effect_time["Value"])

            # Step 4 : Convert to asset
            convert_all_json_to_asset()

            # Step 5 : Pack mod
            if value_multiplier == 1:
                MOD_NAME_VARIANT = MOD_NAME[:-2] + "_x"+str(time_multiplier)+'_Longer_P'
            elif time_multiplier == 1:
                MOD_NAME_VARIANT = MOD_NAME[:-2] + "_x"+str(value_multiplier)+'_Stronger_P'
            else:
                MOD_NAME_VARIANT = MOD_NAME[:-2] + "_x"+str(time_multiplier)+'_Longer_x'+str(value_multiplier)+'_Stronger_P'
            package_assets(MOD_NAME_VARIANT)

            # Step 6 : zip mod
            zip_mod(MOD_FOLDER_NAME + os.path.sep + MOD_NAME_VARIANT)

            # Step 7 : Cleanup
            clean_temp(extracted=False)

    # Step 7 : Cleanup
    clean_temp()

if __name__ == "__main__":
    generateMod()
