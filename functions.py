import json

def read_guildsFile():
    """
    Gets the content from guilds.json file. The file must be located in the same directory as the root file.
    """
    try:
        with open('guilds.json') as guilds_file:
            guilds = json.load(guilds_file)
            return guilds
    except Exception as e:
        print(e)

def write_guildsFile(var):
    """
    Writes the content of var to guilds.json. The file must be located in the same directory as the root file.
    """
    try:
        with open('guilds.json', 'w') as outfile:
            json.dump(var, outfile, indent=4)
            return True
    except Exception as e:
        print(e)
        return False