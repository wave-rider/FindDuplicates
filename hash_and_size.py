import os
import hashlib
import csv
import unicodedata
import sys
import time
# F:\ D:\Drive_F.csv

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
    existing_data = set()
    #start_time = time.time()
    if os.path.isfile(output_file):
        with open(output_file, 'r', encoding='UTF-8') as f1:
            for line in f1:
                name = line.strip().split('|')[0]
                existing_data.add(name)
    with open(output_file, 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='|')
        #csv_writer.writerow(['Full File Path', 'File Hash', 'File Size'])

        for foldername, subfolders, filenames in os.walk(directory_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                #this is needed for MacOS
                #file_path = normalize_file_name(the_name)
                if (file_path not in existing_data) and os.path.exists(file_path):

                    file_size = os.path.getsize(file_path)
                    file_hash = ""
                    try:
                        file_hash = hash_file(file_path)
                        print(file_path, file_hash, file_size)
                    except Exception as e:
                        file_path="Error_path"
                        file_hash = f"Error occured {e}"

                    csv_writer.writerow([file_path, file_hash, file_size])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <directory_path> <output_file>")
        sys.exit(1)
    directory_path = sys.argv[1]
    output_file = sys.argv[2]

    process_directory(directory_path, output_file)