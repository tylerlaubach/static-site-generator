import os
import shutil
from textnode import TextNode, TextType

def copy_dir(source_dir, destination_dir):
    if not os.path.exists(source_dir):
        raise Exception("source directory does not exist")
    
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    os.makedirs(destination_dir)

    for item in os.listdir(source_dir):
        path = os.path.join(source_dir, item)
        if os.path.isfile(path):
            print(f"Copying {path}")
            shutil.copy(path, destination_dir)
        else:
            destination_path = os.path.join(destination_dir, item)
            print(f"Copying dir {path} to {destination_path}")
            copy_dir(path, destination_path)

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))  # This gets 'root_dir/src'
    static_dir = os.path.join(root_dir, "..", "static")
    public_dir = os.path.join(root_dir, "..", "public")

    # Normalize paths (resolves "..")
    static_dir = os.path.abspath(static_dir)
    public_dir = os.path.abspath(public_dir)

    print(f"Copying from {static_dir} to {public_dir}")
    copy_dir(static_dir, public_dir)

main()