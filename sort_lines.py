import sys

def sort_lines_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        sorted_lines = sorted(lines)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(sorted_lines)

        print("Lines sorted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    sort_lines_in_file(input_file)
