import asyncio
from aiofiles.os import makedirs, path
from aiofiles.os import listdir
from argparse import ArgumentParser
from pathlib import Path
import shutil
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s\n")
logger = logging.getLogger(__name__)


async def copy_file(source_file: Path, target_dir: Path):
    """
    Copy a file to a target directory within a subdirectory based on its extension.
    """
    try:
        extension = source_file.suffix[1:]
        target_folder = target_dir / extension

        if not await path.exists(target_folder):
            await makedirs(target_folder, exist_ok=True)

        target_path = target_folder / source_file.name
        shutil.copy2(source_file, target_path)
        logger.info(f"Copied: {source_file} -> {target_path}")
    except Exception as e:
        logger.error(f"Error copying {source_file}: {e}")


async def read_folder(source_dir: Path, target_dir: Path):
    """
    Recursively reads a specified source directory, processes its files, and copies them
    to a target directory. If the function encounters any subdirectories, it recursively
    reads and processes them as well.
    """
    try:
        for item in await listdir(source_dir):
            source_path = source_dir / item
            if await path.isdir(source_path):
                await read_folder(source_path, target_dir)
            elif await path.isfile(source_path):
                await copy_file(source_path, target_dir)
    except Exception as e:
        logger.error(f"Error reading folder {source_dir}: {e}")


async def main():
    parser = ArgumentParser(description="Асинхронне сортування файлів за розширенням.")
    parser.add_argument("source", type=str, help="Шлях до вихідної папки.")
    parser.add_argument("target", type=str, help="Шлях до цільової папки.")
    args = parser.parse_args()

    source_dir = Path(args.source).resolve()
    target_dir = Path(args.target).resolve()

    if not source_dir.exists():
        logger.error(f"Source directory does not exist: {source_dir}")
        return

    if not target_dir.exists():
        await makedirs(target_dir, exist_ok=True)

    await read_folder(source_dir, target_dir)


if __name__ == "__main__":
    asyncio.run(main())