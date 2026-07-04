import os
import shutil


def clear_directory(path: str) -> None:
    for entry in os.scandir(path):
        if entry.is_file():
            os.remove(entry.path)
        else:
            shutil.rmtree(entry.path)


def copy_static(src, dst):
    clear_directory(dst)
    shutil.copytree(src, dst, dirs_exist_ok=True)
    print("Files was copied to docs!")
