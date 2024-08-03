import aiohttp
import asyncio
import time
from urllib.parse import unquote

from modules.modpack import Modpack


class Downloader:
    async def download_mod(self, modpack_id: str, project_id: str, file_id: str):
        url = f"https://www.curseforge.com/api/v1/mods/{project_id}/files/{file_id}/download"
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        filename = unquote(str(response.url).split("/")[-1])
                        if response.status == 200:
                            print(f"Downloaded {filename}...")

                            with open(f"modpacks/{modpack_id}/{filename}", "wb") as f:
                                f.write(await response.content.read())

                            break
                        else:
                            print(f"Failed to download {filename}...")
            except (
                aiohttp.ClientResponseError,
                aiohttp.ClientOSError,
                aiohttp.ClientConnectorError,
            ):
                await asyncio.sleep(5)
            except Exception as e:
                print(e)
                break

    async def download_modpack(self, modpack: Modpack):
        start = time.time()
        semaphore = asyncio.Semaphore(5)
        tasks = []

        modpack.initialize()

        for mod in modpack.modlist:
            async with semaphore:
                tasks.append(
                    asyncio.create_task(
                        self.download_mod(
                            modpack.modpack_id, mod.project_id, mod.file_id
                        )
                    )
                )

        await asyncio.gather(*tasks)

        end = time.time()

        print(f"Downloaded modpack '{modpack.modpack_id}' in {end - start} seconds.")
