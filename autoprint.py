import os
import time
import win32print
import win32api
import shutil

# --- НАСТРОЙКИ ---
FOLDER_PATH = "C:\\xampp\\htdocs\\snap_studio\\saves"
PRINTER_NAME = "My_Printer_Name"

# --- КОД СКРИПТА ---
def get_current_files(folder_path):
    files = set()
    try:
        for filename in os.listdir(folder_path):
            full_path = os.path.join(folder_path, filename)
            if os.path.isfile(full_path):
                files.add(filename)
    except FileNotFoundError:
        print(f"Ошибка: Папка {folder_path} не найдена. Создайте ее.")
        return files
    return files

def print_file(file_path):
    try:
        win32print.SetDefaultPrinter(PRINTER_NAME)
        win32api.ShellExecute(0, "print", file_path, None, ".", 0)
        print(f"Файл {os.path.basename(file_path)} отправлен на печать.")
        return True
    except Exception as e:
        print(f"Ошибка при печати файла {os.path.basename(file_path)}: {e}")
        return False

def main():
    print(f"Скрипт запущен. Отслеживание папки: {FOLDER_PATH}")
    
    existing_files = get_current_files(FOLDER_PATH)
    print(f"Обнаружено {len(existing_files)} существующих файлов.")
    
    archive_folder = os.path.join(FOLDER_PATH, "archive")
    if not os.path.exists(archive_folder):
        os.makedirs(archive_folder)
        
    while True:
        current_files = get_current_files(FOLDER_PATH)
        new_files = current_files - existing_files
        
        if new_files:
            print(f"\nОбнаружено {len(new_files)} новых файлов.")
            for filename in new_files:
                full_path = os.path.join(FOLDER_PATH, filename)
                
                if print_file(full_path):
                    try:
                        shutil.move(full_path, os.path.join(archive_folder, filename))
                        print(f"Файл {filename} перемещён в архив.")
                    except Exception as e:
                        print(f"Ошибка при перемещении файла {filename} в архив: {e}")
            
        existing_files = get_current_files(FOLDER_PATH)
        
        time.sleep(3) # Задержка уменьшена до 3 секунд
        
if __name__ == "__main__":
    main()