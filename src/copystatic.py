import os
import shutil

def copy_static(source_dir, destination_dir="docs"):
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    copy_files_recursively(source_dir, destination_dir)
    
            
def copy_files_recursively(source_dir, destination_dir):
    if not os.path.exists(destination_dir):
        os.mkdir(destination_dir)
        
    for filename in os.listdir(source_dir):
        source_path = os.path.join(source_dir, filename)
        dest_path = os.path.join(destination_dir, filename)
        print(f" * {source_path} -> {dest_path}")
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            copy_files_recursively(source_path, dest_path)