from pathlib import Path
import shutil
import os


def translate_name_file(name) -> str:
    """Функція транслітерації назв файлів та папок"""

    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЄІЇҐ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "A", "B", "V", "G", "D", "E", "E", "J", "Z", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U",
                   "F", "H", "Ts", "Ch", "Sh", "Sch", "E", "Yu", "Ya", "Je", "I", "Ji", "G")
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
    new_name = name.translate(TRANS)
    return new_name


def replacement_symbols_file_name(name) -> str:
    """Фунція заміни всіх небажаних символів в іменах файлів та папок"""

    list_name = list(name)
    i = 0
    for n in list_name:
        if (not n.isalpha()) and (not n.isdigit()):
            list_name[i] = "_"
        i = i + 1
    new_name = "".join(list_name)
    return new_name


def normalize(path: Path) -> Path:
    """Функція нормацізації імен файлів та папок"""

    if path.is_dir():
        full_name = path.name
        full_transtale_name = translate_name_file(full_name)
        full_clear_name = replacement_symbols_file_name(full_transtale_name)
        if full_clear_name != full_name:
            try:
                new_path = os.path.join(path.parent, full_clear_name)
                os.rename(path, new_path)
                return Path(new_path)
            except OSError as e:
                print(f"Папку {path} не перейменовано! Причина: {e.strerror}")
                return path
        else:
            return path
    elif path.is_file():
        full_name = path.name
        list_name = full_name.split(".")
        list_name[0] = translate_name_file(list_name[0])
        list_name[0] = replacement_symbols_file_name(list_name[0])
        new_name = ".".join(list_name)
        if new_name != full_name:
            try:
                new_path = os.path.join(path.parent, new_name)
                os.rename(path, new_path)
                return Path(new_path)
            except OSError as e:
                print(f"Файл {path} не перейменовано! Причина: {e.strerror}")
                return path
        else:
            return path


def delete(path: Path):
    """Функція видалення порожньої папки"""

    try:
        path.rmdir()
    except OSError as e:
        print(
            f'Не вдалось видалити порожню папку за шляхом {path}. Помилка: {e.strerror}')


def sorting(path: Path, video_path: Path, archive_path: Path, audio_path: Path, document_path: Path, image_path: Path) -> list:
    unknown_list = []
    known_list = []
    if not len(os.listdir(path)):
        delete(path)
        return []
    else:
        new_path_name = normalize(path)
        for i in new_path_name.iterdir():
            if (i.name == "video") or (i.name == "audio") or (i.name == "archives") or (i.name == "documents") or (i.name == "images"):
                continue
            i_path = new_path_name / i
            if i_path.is_dir():
                new_path = normalize(i_path)
                l = sorting(new_path, video_path, archive_path,
                            audio_path, document_path, image_path)
                if len(l):
                    unknown_list.extend(l[0])
                    known_list.extend(l[1])
            else:
                i_new = normalize(i_path)
                #i_roz_with = i_new.name.split(".")
                i_roz = i_new.suffix.removeprefix(".")
                if (i_roz == "jpg") or (i_roz == "png") or (i_roz == "jpeg") or (i_roz == "svg") or (i_roz == "bmp"):
                    known_list.append(i_roz)
                    try:
                        shutil.move(i_new, image_path)
                    except OSError as e:
                        print(
                            f"Не вдалося перемістити файл {i_new.name}. Помилка: {e.strerror}")
                elif (i_roz == "avi") or (i_roz == "mp4") or (i_roz == "mov") or (i_roz == "mkv"):
                    known_list.append(i_roz)
                    try:
                        shutil.move(i_new, video_path)
                    except OSError as e:
                        print(
                            f"Не вдалося перемістити файл {i_new.name}. Помилка: {e.strerror}")
                elif (i_roz == "doc") or (i_roz == "docx") or (i_roz == "txt") or (i_roz == "pdf") or (i_roz == "rtf") or (i_roz == "xlsx") or (i_roz == "xls") or (i_roz == "pptx") or (i_roz == "ppt"):
                    known_list.append(i_roz)
                    try:
                        shutil.move(i_new, document_path)
                    except OSError as e:
                        print(
                            f"Не вдалося перемістити файл {i_new.name}. Помилка: {e.strerror}")
                elif (i_roz == "mp3") or (i_roz == "ogg") or (i_roz == "wav") or (i_roz == "amr"):
                    known_list.append(i_roz)
                    try:
                        shutil.move(i_new, audio_path)
                    except OSError as e:
                        print(
                            f"Не вдалося перемістити файл {i_new.name}. Помилка: {e.strerror}")
                elif (i_roz == "zip") or (i_roz == "tar") or (i_roz == "gz") or (i_roz == "rar") or (i_roz == "ZIP") or (i_roz == "7z"):
                    try:
                        shutil.move(i_new, archive_path)
                    except OSError as e:
                        print(
                            f"Не вдалось перемістити файл {i_new.name}. Помилка: {e.strerror}")
                    try:
                        arh_p = archive_path / \
                            i_new.name.removesuffix(i_new.suffix)
                        shutil.unpack_archive(arh_p)
                    except OSError as e:
                        print(
                            f'Не вдалось розпакуати архів {i_new.name}. Помилка: {e.strerror}')
                    known_list.append(i_roz)
                else:
                    unknown_list.append(i_roz)
    if not len(os.listdir(path)):
        delete(new_path_name)
    return [unknown_list, known_list]


p = Path(input("Введіть шлях до папки:"))
if p.is_dir():
    video_path = p / 'video'
    video_path.mkdir(exist_ok=True)
    archive_path = p / "archives"
    archive_path.mkdir(exist_ok=True)
    audio_path = p / "audio"
    audio_path.mkdir(exist_ok=True)
    document_path = p / "documents"
    document_path.mkdir(exist_ok=True)
    image_path = p / "images"
    image_path.mkdir(exist_ok=True)
    result = sorting(p, video_path, archive_path,
                     audio_path, document_path, image_path)
    print("Сортування виконано успішно!")
    print("Список відомих розширень файлів у папці:", result[1])
    print("Список невідомих розширень у папці:", result[0])
else:
    print("Це не шлях до папки!")
