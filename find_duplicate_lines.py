def find_duplicate_lines(file_path):
    seen_lines = set()

    with open(file_path, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=1):
            # Remove leading and trailing whitespaces from the line
            cleaned_line = line.strip()

            # Check for duplicates
            if cleaned_line in seen_lines:
                print(f"Duplicate line found at line {line_number}: {cleaned_line}")
            else:
                seen_lines.add(cleaned_line)

# Replace 'your_file.txt' with the actual path to your file
#find_duplicate_lines('your_file.txt')

str1 = r'~'
str2 = r'A'
t = [str1, str2]
t = sorted(t)#, key=str.lower)
print(t)