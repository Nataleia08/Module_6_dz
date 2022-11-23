from pathlib import Path
# from os import rename, listdir
# from shutil import move, unpack_archive
# from os.path import join
import function


p = Path(input("Введіть шлях до папки:"))
if p.is_dir():
    list_path = function.creating_folder(p)

    result = function.sorting(p, list_path)
    print("Сортування виконано успішно!")
    print("Список відомих розширень файлів у папці:", result[1])
    print("Список невідомих розширень у папці:", result[0])
else:
    print("Це не шлях до папки!")
