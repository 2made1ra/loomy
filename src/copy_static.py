import os
import shutil


def clear_directory(path: str) -> None:
    for entry in os.scandir(path):
        if os.path.isfile(entry.path):
            os.remove(entry.path)
        else:
            shutil.rmtree(entry.path)


def copy_static():
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(SCRIPT_DIR, "..", "static")
    dst = os.path.join(SCRIPT_DIR, "..", "public")
    clear_directory(dst)

    shutil.copytree(src, dst, dirs_exist_ok=True)

    print("Files was copied to public!")
