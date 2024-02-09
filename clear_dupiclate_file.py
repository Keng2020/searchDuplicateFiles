import os
import hashlib
from tqdm import tqdm
import shutil

def hash_file(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_duplicate_files(directory):
    file_hash_map = {}
    duplicate_files = []

    total_files = sum([len(files) for _, _, files in os.walk(directory)])

    with tqdm(total=total_files, desc="Scanning Files", unit="file") as pbar:
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                file_hash = hash_file(file_path)

                if file_hash in file_hash_map:
                    duplicate_files.append((file_path, file_hash_map[file_hash]))
                else:
                    file_hash_map[file_hash] = file_path

                pbar.update(1)

    return duplicate_files

def move_duplicate_files(duplicates, duplicate_folder, log_file):
    if not os.path.exists(duplicate_folder):
        os.makedirs(duplicate_folder)

    with open(log_file, 'w') as log:
        for file1, file2 in duplicates:
            duplicate_file_path = os.path.join(duplicate_folder, os.path.basename(file1))
            shutil.move(file1, duplicate_file_path)
            log.write(f"{file1} moved to {duplicate_file_path}\n")
            print(f"Moved {file1} to {duplicate_file_path}")

if __name__ == "__main__":
    directory_to_check = r"E:\Picture"
    duplicate_folder = os.path.join(directory_to_check, "duplicate")
    log_file = os.path.join(directory_to_check, "log.txt")

    duplicates = find_duplicate_files(directory_to_check)

    if duplicates:
        print("Duplicate files found. Moving to the 'duplicate' folder and creating a log.")
        move_duplicate_files(duplicates, duplicate_folder, log_file)
    else:
        print("No duplicate files found.")
