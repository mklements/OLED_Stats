import os


def get_companion_configs():
    folder = "/home/cmxeon/_git/smartrack-pi/companion"
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]


print(get_companion_configs())
