import os
import shutil


def clear_directory(path: str) -> None:
    for entry in os.scandir(path):
        if entry.is_file():
            os.remove(entry.path)
        else:
            shutil.rmtree(entry.path)


def copy_static(src, dst):
    if os.path.exists(dst):
        clear_directory(dst)
    else:
        os.mkdir(dst)

    entrys = os.listdir(src)

    for entry in entrys:
        path_to_entry = os.path.join(src, entry)
        if os.path.isfile(path_to_entry):
            dest_path = os.path.join(dst, entry)
            shutil.copy(path_to_entry, dest_path)
        else:
            new_dest_dir = os.path.join(dst, entry)
            copy_static(path_to_entry, new_dest_dir)
    # shutil.copytree(src, dst, dirs_exist_ok=True)
    # print("Files was copied to docs!")
