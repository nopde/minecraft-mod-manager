import json
import os

from modules.mod import Mod


class Modpack:
    def __init__(self, modpack_id: str):
        self.modpack_id = modpack_id
        self.modlist: list[Mod] = []
        self.data = {"modpackID": modpack_id, "mods": []}

    def initialize(self):
        for mod in self.modlist:
            self.data["mods"].append(
                {"projectID": mod.project_id, "fileID": mod.file_id}
            )

    def get_data(self):
        return self.data


class ModpackManager:
    def __init__(self, modpacks_path: str):
        self.modpacks_path = modpacks_path

    def get_json_data(self):
        with open(self.modpacks_path) as f:
            return json.load(f)

    def get_modpacks_data(self):
        return self.get_json_data()["modpacks"]

    def get_modpack(self, modpack_id: str):
        modpacks = self.get_modpacks_data()
        for modpack in modpacks:
            if modpack["modpackID"] == modpack_id:
                modpack_obj = Modpack(modpack["modpackID"])
                for mod in modpack["mods"]:
                    modpack_obj.modlist.append(Mod(mod["projectID"], mod["fileID"]))
                return modpack_obj
        return None

    def add_modpack(self, modpack: Modpack):
        os.makedirs(os.path.join("modpacks", modpack.modpack_id), exist_ok=True)
        modpacks = self.get_json_data()
        modpacks["modpacks"].append(modpack.get_data())
        with open(self.modpacks_path, "w") as f:
            json.dump(modpacks, f, indent=4)
        return True

    def remove_modpack(self, modpack_id: str):
        modpacks = self.get_json_data()
        for modpack in modpacks["modpacks"]:
            if modpack["modpackID"] == modpack_id:
                modpacks["modpacks"].remove(modpack)
                with open(self.modpacks_path, "w") as f:
                    json.dump(modpacks, f, indent=4)
                return True
        return False

    def read_manifest(self, manifest_path: str):
        with open(manifest_path, encoding="utf-8-sig") as f:
            manifest = json.load(f)
            return manifest

    def get_modlist(self, manifest_path: str):
        manifest_data = self.read_manifest(manifest_path)
        modlist = []
        for mod in manifest_data["files"]:
            modlist.append(Mod(mod["projectID"], mod["fileID"]))
        return modlist

    def build_modpack(self, modpack_id: str, manifest_path: str):
        modpack = Modpack(modpack_id)

        if not manifest_path.endswith(".json"):
            manifest_path += ".json"

        modpack.modlist = self.get_modlist(manifest_path)
        modpack.initialize()
        return modpack
