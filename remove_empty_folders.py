import os
import sys

def delete_empty_subfolders(folder_path):
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir_name in dirs:
            full_path = os.path.join(root, dir_name)
            try:
                if not os.listdir(full_path):  # Check if the folder is empty
                    print(full_path)
                    os.rmdir(full_path)  # Delete the empty folder
            except PermissionError as pe:
                print(f"PermissionError: {pe}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    delete_empty_subfolders(input_file)
