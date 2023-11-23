import os
import hashlib
import csv
import unicodedata
import sys

def hash_file(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def normalize_file_name(file_name):
    # Normalize to NFC (composed) form
    return unicodedata.normalize('NFC', file_name)
def process_directory(directory_path, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='|')
        #csv_writer.writerow(['Full File Path', 'File Hash', 'File Size'])

        for foldername, subfolders, filenames in os.walk(directory_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                #this is needed for MacOS
                #file_path = normalize_file_name(the_name)
                file_size = os.path.getsize(file_path)
                file_hash = hash_file(file_path)
                print(file_path, file_hash, file_size)
                csv_writer.writerow([file_path, file_hash, file_size])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <directory_path> <output_file>")
        sys.exit(1)
    directory_path = sys.argv[1]
    output_file = sys.argv[2]
    process_directory(directory_path, output_file)