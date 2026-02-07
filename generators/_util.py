import subprocess, shutil, fnmatch, os, json, copy, struct

import configparser

def fetch_constants_from_config():
    print("Reading Config")
    config = configparser.ConfigParser()
    config.read("../config.ini")
    MAPPING = config.get("ModGen", "MAPPING")
    AES_KEY = config.get("ModGen", "AES_KEY")
    GAME_DIRECTORY = config.get("ModGen", "GAME_DIRECTORY")

    if AES_KEY[:2] != "0x":
        AES_KEY = "0x" + AES_KEY

    if GAME_DIRECTORY.split("/")[-1] != "Paks":
        GAME_DIRECTORY = os.path.join(GAME_DIRECTORY, "Game/Content/Paks")

    print("Mapping is: " + MAPPING)
    print("Key is: " + AES_KEY)
    print("Game Pak directory is: " + GAME_DIRECTORY)
    # TODO: Check Game Pak Directory exists
    # TODO: Check Mapping exists in AppData
    
    return MAPPING, AES_KEY, GAME_DIRECTORY
##if "MAPPING" not in globals():
MAPPING, AES_KEY, GAME_DIRECTORY = fetch_constants_from_config()

def include_patterns(*patterns):
    """Factory function that can be used with copytree() ignore parameter.

    Arguments define a sequence of glob-style patterns
    that are used to specify what files to NOT ignore.
    Creates and returns a function that determines this for each directory
    in the file hierarchy rooted at the source directory when used with
    shutil.copytree().
    """
    def _ignore_patterns(path, names):
        keep = set(name for pattern in patterns for name in fnmatch.filter(names, pattern))
        ignore = set(name for name in names if name not in keep and not os.path.isdir(os.path.join(path, name)))
        return ignore
    return _ignore_patterns

def convert_all_assets_to_json(*pattern):
    """Converts matching glob-style pattern (default "*") from uasset to json
    """
    if len(pattern) == 0:
        pattern = ("*")
    print("Converting from assets with include pattern: " + str(pattern))
    for root, directories, files in os.walk("../temp/extracted"):
        include_func = include_patterns(*pattern)
        ignore = include_func(root, files)
        for fil in files:
            if fil in ignore:
                continue
            fil_path = os.path.join(root, fil)
            fil_main, fil_ext = ".".join(fil_path.split(".")[:-1]), fil_path.split(".")[-1]
            if fil_ext != "uasset":
                continue
            print("Converting: " + fil_path[len("../temp/extracted/"):])
            subprocess.run('../tools/UAssetGUI tojson '+fil_main+'.uasset '+fil_main+'.json VER_UE5_4 ' + MAPPING)

def convert_all_json_to_asset(*pattern):
    """Converts matching glob-style pattern (default "*") from json to uasset
    """
    if len(pattern) == 0:
        pattern = ("*")
    print("Converting to assets with include pattern: " + str(pattern))
    for root, directories, files in os.walk("../temp/edited"):
        include_func = include_patterns(*pattern)
        ignore = include_func(root, files)
        for fil in files:
            if fil in ignore:
                continue
            fil_path = os.path.join(root, fil)
            fil_main, fil_ext = ".".join(fil_path.split(".")[:-1]), fil_path.split(".")[-1]
            if fil_ext != "json":
                continue
            print("Converting: " + fil_path[len("../temp/edited/"):])
            subprocess.run('../tools/UAssetGUI fromjson '+fil_main+'.json '+fil_main+'.uasset ' + MAPPING)

def extract_assets(*filters):
    print("Extracting to assest with filters: " + str(filters))
    for asset_filter in filters:
        print("Extracting asset with filter: " + asset_filter)
        subprocess.run('../tools/retoc.exe --aes-key '+AES_KEY+'   to-legacy --debug --version=UE5_4 -f='+asset_filter+' "'+GAME_DIRECTORY+'" "../temp/extracted"')

def clean_temp(extracted = True, edited = True, packed = True):
    if extracted and os.path.exists("../temp/extracted"):
        print("Cleaning temp extracted")
        shutil.rmtree("../temp/extracted")
    if edited and os.path.exists("../temp/edited"):
        print("Cleaning temp edited")
        shutil.rmtree("../temp/edited")
    if packed:
        temp_mod_folder = "../temp/Game/Content/Paks/~mods"
        if os.path.isdir(temp_mod_folder):
            print("Cleaning temp packed mods")
            for filename in os.listdir(temp_mod_folder):
                file_path = os.path.join(temp_mod_folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
        else:
            os.makedirs("../temp/Game/Content/Paks/~mods")

def package_assets(file_name):
    print("Packaging asset to file: " + file_name)
    if not os.path.exists("../temp/Game/Content/Paks/~mods"):
        os.makedirs("../temp/Game/Content/Paks/~mods")
    subprocess.run('../tools/retoc.exe --aes-key '+AES_KEY+'   to-zen --debug --version=UE5_4  "../temp/edited" "../temp/Game/Content/Paks/~mods/"'+file_name+'.utoc"')

def zip_mod(file_name):
    print("Zipping mod to: " + file_name)
    shutil.make_archive("../output/"+file_name, "zip", "../temp", "Game")

def open_json(file_path):
    if not file_path.endswith(".json"):
        file_path += ".json"
    if file_path.startswith("/") or file_path.startswith("\\"):
        file_path = file_path[1:]
    if not file_path.startswith(".."):
        file_path = os.path.join("../temp/extracted",file_path)
    print("Reading json: " + file_path)
    with open(file_path, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)
    return json_data

def save_json(json_data, file_path):
    if not file_path.endswith(".json"):
        file_path += ".json"
    if file_path.startswith("/") or file_path.startswith("\\"):
        file_path = file_path[1:]
    if not file_path.startswith(".."):
        file_path = os.path.join("../temp/edited",file_path)
    file_dirpath = os.path.dirname(file_path)
    if not os.path.exists(file_dirpath):
        print("Creating directory: " + file_dirpath)
        os.makedirs(file_dirpath, exist_ok=True)
    print("Writing json: " + file_path)
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=2, ensure_ascii=False)

import contextlib

# Allows with edit_json(file_path) as jsonData:
#   do edits
#
# no need to end with save_json
@contextlib.contextmanager
def edit_json(file_path):
    json_data = open_json(file_path)
    try:
        yield json_data
    finally:
        save_json(json_data, file_path)

def get_m_data(m_autobin, m_autostr, m_offset, m_datasize):
    m_type = m_autobin[m_offset+16]["Value"]
    if m_type == 50: # int
        m_val = struct.unpack("i", bytes([binData["Value"] for binData in m_autobin[m_offset+16+1:m_offset+16+5]]))[0]
        return m_type, m_val
    elif m_type == 51: # float
        m_val = struct.unpack("f", bytes([binData["Value"] for binData in m_autobin[m_offset+16+1:m_offset+16+5]]))[0]
        return m_type, m_val
    elif m_type == 52: # string
        m_val = int.from_bytes(bytes([binData["Value"] for binData in m_autobin[m_offset+16+1:m_offset+16+5]]), "little")
        m_str = m_autostr[m_val:m_val+m_datasize]
        return m_type, m_str
    return "Err"

def set_m_data(m_autobin, m_autostr, m_offset, m_datasize,  m_val):
##    if m_type != m_autobin[m_offset+16]["Value"]:
##        print("Setting different m_type!!!")
    m_type = m_autobin[m_offset+16]["Value"]
    if m_type == 50:
        new_val = list(struct.pack("i", m_val))
        for part_val in range(len(new_val)):
            m_autobin[m_offset+16+1+part_val]["Value"] = new_val[part_val]
    return
