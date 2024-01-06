import os

def delete_all_files_in_directory(directory):
    file_list = os.listdir(directory)

    for file_name in file_list:
        file_path = os.path.join(directory, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error {file_path}: {e}")

if __name__ == "__main__":
    directory_path = "./out"
    delete_all_files_in_directory(directory_path)