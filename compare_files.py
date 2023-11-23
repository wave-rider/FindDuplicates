# Desktop_Windows.csv D:\Helen\From_Dell_15_11_2023\Desktop Desktop_MAC_Normalized.csv /Users/wasabi/Desktop result.txt
import sys
import os
import chardet
import send2trash
import unicodedata

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
        return result['encoding']

def normalize_file_name(file_name):
    # Normalize to NFC (composed) form
    return unicodedata.normalize('NFC', file_name)

print('Len:', len(sys.argv))
if len(sys.argv) != 6:
    print("Usage: python compare_files.py <file1> <file2> <output_file>")
    sys.exit(1)

file1 = sys.argv[1]
prefix1 = sys.argv[2]
file2 = sys.argv[3]
prefix2 = sys.argv[4]
output_file = sys.argv[5]
encoding1 = detect_encoding(file1)
encoding2 = detect_encoding(file2)
print(encoding1, encoding2)

class FileInfo:
    def __init__(self, full_path, size, hash_value, file_name_to_delete):
        self.full_path = full_path
        self.size = size
        self.name = os.path.basename(full_path)
        self.hash_value = hash_value
        self.file_name_to_delete = file_name_to_delete

    def __repr__(self):
        return f"FileInfo(path ={self.full_path}, name={self.name}, size={self.size}, hash_value={self.hash_value})"

try:
    with open(file1, 'r', encoding=encoding1) as f1, open(file2, 'r', encoding=encoding2) as f2:
        lines1 = []
        for line in f1:
            lines1.append(line)
        lines2 = []
        for line in f2:
            lines2.append(line)

    compare_dict1 = {}
    compare_dict2 = {}
    delete_count = 0
    with open(output_file, 'w', encoding='utf-8') as output:
        i, j = 0, 0
        cnt = 0
        size = 0
        total_size = 0
        prev_i = None
        prev_j = None
        while i < len(lines1) and j < len(lines2):
            if i != prev_i:
                prev_i = i
                line1 = lines1[i]
                elements1 = line1.strip().split('|')
                file_1_size = int(elements1[-1])
                file_1_hash = elements1[-2].upper()
                filename1 = "".join(elements1[:-2]).replace(prefix1, '').replace('\\', '/')
                #filename_to_delete = "".join(elements1[:-2]).replace('"','')
                filename_to_delete = "".join(elements1[:-2]).replace('"', '')#.replace(prefix1, r"D:\Helen\From_Dell_15_11_2023\Downloads\Downloads_from_mac_28_03_2021")
                #filename_to_delete = "\\\\?\\"+filename_to_delete
                if file_1_hash not in compare_dict1:
                    compare_dict1[file_1_hash] = []
                compare_dict1[file_1_hash].append(FileInfo(filename1, file_1_size, file_1_hash, filename_to_delete))

            if j != prev_j:
                prev_j = j
                line2 = lines2[j]
                elements2 = line2.strip().split(',')
                file_2_size = int(elements2[-1])
                file_2_hash = elements2[-2].upper()
                filename2 = ",".join(elements2[:-2]).replace(prefix2, '')
                if file_2_hash not in compare_dict2:
                    compare_dict2[file_2_hash] = []
                compare_dict2[file_2_hash] = FileInfo(filename2, file_2_size, file_2_hash, '')

            if file_1_hash == '' or file_1_hash =='':
                raise ValueError('Empty hash detected')

            if '.DS_Store' in filename1:
                if os.path.exists(filename_to_delete) is True:
                    print(delete_count, "Deleting a file:", filename_to_delete)
                    # output.write(f"{filename_to_delete}\n")
                    # test = os.path.isabs(filename_to_delete)
                    delete_count += 1
                    send2trash.send2trash(filename_to_delete)
            if normalize_file_name(filename1) == filename2:
                if file_1_size == file_2_size and file_1_hash == file_2_hash:
                    cnt += 1
                    size += file_1_size
                    if os.path.exists(filename_to_delete) is True:
                        print(delete_count, "Deleting a file:", filename_to_delete)
                        delete_count += 1
                        send2trash.send2trash(filename_to_delete)
                i += 1
                j += 1
                total_size += file_1_size
            elif filename1 < filename2:
                i += 1
                total_size += file_1_size
            else:
                j += 1
            
            #print(i,filename1, filename2)
        print("Count:", cnt, "Size:", size/ (1024.0 ** 2), "Mb", "Total size:", total_size / (1024.0 ** 2), "Mb")
        print("Remained: ", total_size-size)
    common_keys = set(compare_dict1.keys()) & set(compare_dict2.keys())
    common_keys_count=0
    for key in common_keys:
        # Finding duplicates
        #if len(compare_dict1[key]) > 1:
            #print("=======")
        for item in compare_dict1[key]:
            if os.path.exists(item.file_name_to_delete) is True:
                print(item)
                send2trash.send2trash(item.file_name_to_delete)
                common_keys_count += 1
        #else:
        #    common_keys_count += 1
    print('source count:', len(lines1))
    print('dest count:', len(lines2))
    print('Common unique key count:', len(common_keys))
    print('Common keys count:', common_keys_count)
    print('Delete key count:', delete_count)
    print('Dict1 key count:', len(compare_dict1))
    print('Dict2 key count:', len(compare_dict2))
    
    print(f"Differences written to {output_file}")
except FileNotFoundError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
