__all__ = ["MOD_FOLDER_NAME", "MOD_NAME", "generateMod"]
from _util import *
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

MOD_FOLDER_NAME = "UnicornCode" # Folder to store .zips in
MOD_NAME = MOD_FOLDER_NAME+"_P" # base mod name

def password_encrypt(password):
    ENCRYPTION_KEY = b"vLQLuei5bE6q8a6sqbfui5fezREwaqaV"
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_ECB)
    if type(password) is bytes:
        bytes_password = password
    else:
        bytes_password = bytes(password,"utf-8")
    return base64.b64encode(cipher.encrypt(pad(bytes_password, 16))).decode("utf-8")

def password_decrypt(encrypted):
    ENCRYPTION_KEY = b"vLQLuei5bE6q8a6sqbfui5fezREwaqaV"
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_ECB)
    return unpad(cipher.decrypt(base64.b64decode(encrypted)), 16).decode("utf-8")
    

def generateMod():
    clean_temp()
    # Step 1 : Extract Files
    extract_assets("/Game/Content/GameData/Delivery")
    # Step 2 : Convert to json
    convert_all_assets_to_json("*PasswordData.*")
    # Step 3 : Edit

    with edit_json("Game/Content/GameData/Delivery/GDSPasswordData.json") as passwordData:
        data_map = passwordData["Exports"][0]["Data"][0]
        existing_password = data_map["Value"][0]
        new_password = copy.deepcopy(existing_password)
        new_password[0]["Value"] = "rompass_0000"
        new_password[1]["Value"][0]["Value"] = "rompass_0000"
        new_password[1]["Value"][1]["Value"][0]["Value"] = password_encrypt("WARBOB5K") #"c3IRzb3qAL3pIGVf3LfFKA==" # WARBOB5K
        new_password[1]["Value"][2]["Value"] = "password_recieve_001"
        rewards = new_password[1]["Value"][7]["Value"]
        new_password[1]["Value"][7]["Value"] = [rewards[0]]
        new_password[1]["Value"][7]["Value"][0]["Value"][0]["Value"] = "ive000206"
        data_map["Value"].append(new_password)
        passwordData["NameMap"].insert(6,"rompass_0000")
        passwordData["NameMap"].insert(6,"password_recieve_001")
        passwordData["NameMap"].insert(6,"ive000206")
        passwordData["NamesReferencedFromExportDataCount"] += 3

    # Step 4 : Convert to asset
    convert_all_json_to_asset()

    # Step 5 : Pack mod
    package_assets(MOD_NAME)

    # Step 6 : zip mod
    zip_mod(MOD_FOLDER_NAME + "/" + MOD_NAME)
    

    # Step 7 : Cleanup
    clean_temp()
    

if __name__ == "__main__":
    generateMod()
