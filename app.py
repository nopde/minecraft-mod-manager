import asyncio
import os

from modules.modpack import ModpackManager, Modpack
from modules.settings import settings
from modules.menu import OptionsMenu, Options, Option, InputMenu, EmptyMenu
from modules.downloader import Downloader


class App:
    def __init__(self):
        self.modpack_manager = ModpackManager(settings.modpacks_path)
        self.modpacks = []
        self.selected_modpack = None
        self.downloader = Downloader()

    def update_modpacks(self):
        modpacks = self.modpack_manager.get_modpacks_data()

        if modpacks:
            for modpack in modpacks:
                if modpack not in self.modpacks:
                    self.modpacks.append(modpack)

    def main_menu(self):
        self.update_modpacks()

        options = Options(
            [
                Option("Add modpack", self.add_modpack_menu),
                Option("Quit", quit),
            ]
        )

        has_modpacks = len(self.modpacks) > 0
        if has_modpacks:
            options.options.insert(
                0,
                Option("Manage modpack", self.select_modpack_menu),
            )

        menu = OptionsMenu("Minecraft Modpack Manager", "Options:", options)

        menu.render()

    def add_modpack_menu(self):
        name = InputMenu("Add modpack", "Enter the modpack ID:").render()
        manifest_name = InputMenu(
            "Add modpack", "Enter the manifest file name:"
        ).render()

        if not os.path.exists(
            manifest_name
            if manifest_name.endswith(".json")
            else f"{manifest_name}.json"
        ):
            self.add_modpack_menu()
            return

        modpack = self.modpack_manager.build_modpack(name, manifest_name)

        self.modpack_manager.add_modpack(modpack)

        self.main_menu()

    def select_modpack_menu(self):
        self.update_modpacks()
        options = []

        def select_modpack(**kwargs):
            self.selected_modpack = kwargs["modpack_id"]

        for modpack in self.modpacks:
            options.append(
                Option(
                    modpack["modpackID"],
                    select_modpack,
                    modpack_id=modpack["modpackID"],
                )
            )

        menu = OptionsMenu(
            "Minecraft Modpack Manager",
            "Available modpacks:",
            Options(options),
            "Select a modpack:",
        )

        menu.render()

        self.modpack_menu()

    def downloading_modpack_menu(self, modpack: Modpack):
        EmptyMenu("Minecraft Modpack Manager").render()
        print(f"Downloading modpack '{modpack.modpack_id}'...\r\n")

        asyncio.run(self.downloader.download_modpack(modpack))

    def remove_modpack(self, modpack_id: str):
        self.modpack_manager.remove_modpack(modpack_id)

        self.main_menu()

    def modpack_menu(self):
        modpack = self.modpack_manager.get_modpack(self.selected_modpack)
        options = Options(
            [
                Option("Download", self.downloading_modpack_menu, modpack),
                Option("Remove this modpack", self.remove_modpack, modpack.modpack_id),
                Option("Back to main menu", self.main_menu),
            ]
        )
        menu = OptionsMenu(
            f"Minecraft Modpack Manager\r\n\r\nSelected modpack: {modpack.modpack_id}",
            "Select an option:",
            options,
        )

        menu.render()

    def start(self):
        os.makedirs("modpacks", exist_ok=True)

        if not os.path.exists(settings.modpacks_path):
            with open(settings.modpacks_path, "w") as f:
                f.write('{"modpacks": []}')

        self.main_menu()


if __name__ == "__main__":
    app = App()
    app.start()
