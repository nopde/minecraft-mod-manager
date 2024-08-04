import asyncio
import os
from keyboard import unhook_all

from modules.modpack import ModpackManager, Modpack
from modules.settings import settings
from modules.menu import OptionMenu, Options, Option, Action, InputMenu, EmptyMenu
from modules.downloader import Downloader


class App:
    def __init__(self):
        self.modpack_manager = ModpackManager(settings.modpacks_path)
        self.modpacks = []
        self.selected_modpack = None
        self.downloader = Downloader()

    def app_quit(self):
        unhook_all()
        quit()

    def update_modpacks(self):
        self.modpacks = []
        modpacks = self.modpack_manager.get_modpacks_data()

        if modpacks:
            for modpack in modpacks:
                self.modpacks.append(modpack)

    def main_menu(self):
        self.update_modpacks()

        options = Options(
            [
                Option("Add modpack", Action(self.add_modpack_menu)),
                Option("Quit", Action(self.app_quit)),
            ]
        )

        has_modpacks = len(self.modpacks) > 0
        if has_modpacks:
            options.options.insert(
                0,
                Option("Manage modpack", Action(self.select_modpack_menu)),
            )

        menu = OptionMenu("Minecraft Modpack Manager", "Options:", options)

        menu()

    def add_modpack_menu(self):
        name = InputMenu("Add modpack", "Enter the modpack ID:")()

        if not name:
            self.add_modpack_menu()
            return
        
        if name in [modpack["modpackID"] for modpack in self.modpacks]:
            self.add_modpack_menu()
            return

        manifest_name = InputMenu("Add modpack", "Enter the manifest file name:")()

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
        options = [
            Option("Go back", Action(self.main_menu)),
        ]

        def select_modpack(**kwargs):
            self.selected_modpack = kwargs["modpack_id"]

        for modpack in self.modpacks:
            options.append(
                Option(
                    modpack["modpackID"],
                    Action(select_modpack, modpack_id=modpack["modpackID"]),
                    self.modpack_menu,
                )
            )

        menu = OptionMenu(
            "Minecraft Modpack Manager",
            "Available modpacks:",
            Options(options),
        )

        menu()

    def downloading_modpack_menu(self, modpack: Modpack):
        EmptyMenu("Minecraft Modpack Manager")()
        print(f"Downloading modpack '{modpack.modpack_id}'...\r\n")

        time = asyncio.run(self.downloader.download_modpack(modpack))

        InputMenu(
            f"Minecraft Modpack Manager\r\n\r\nDownloaded modpack '{modpack.modpack_id}' in {time} seconds!",
            "Press Enter to return to the main menu.",
        )()

        self.main_menu()

    def modpack_menu(self):
        modpack = self.modpack_manager.get_modpack(self.selected_modpack)
        options = Options(
            [
                Option("Download", Action(self.downloading_modpack_menu, modpack)),
                Option(
                    "Remove this modpack",
                    Action(self.modpack_manager.remove_modpack, modpack.modpack_id),
                    self.main_menu,
                ),
                Option("Back to main menu", Action(self.main_menu)),
            ]
        )
        menu = OptionMenu(
            f"Minecraft Modpack Manager\r\n\r\nSelected modpack: {modpack.modpack_id}",
            "Select an option:",
            options,
        )

        menu()

    def start(self):
        os.makedirs("modpacks", exist_ok=True)

        if not os.path.exists(settings.modpacks_path):
            with open(settings.modpacks_path, "w") as f:
                f.write('{"modpacks": []}')

        self.main_menu()


if __name__ == "__main__":
    app = App()
    app.start()
