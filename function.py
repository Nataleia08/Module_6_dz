from pathlib import Path
from os import rename, listdir
from shutil import move, unpack_archive
from os.path import join


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
                new_path = join(path.parent, full_clear_name)
                rename(path, new_path)
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
                new_path = join(path.parent, new_name)
                rename(path, new_path)
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


def move_files(path: Path, type_files: int, list_path: list):
    """Функция сортування зображень"""
    i_roz = path.suffix.removeprefix(".")
    for i_path in list_path[1][type_files]:
        if i_roz == i_path.lower():
            try:
                new_path = list_path[0][type_files] / i_path.lower()
                move(path, new_path)
            except OSError as e:
                print(
                    f"Не вдалося перемістити файл {path.name}. Помилка: {e.strerror}")


def sorting(path: Path, list_path) -> list:
    """Функція сортування папок та файлів"""

    unknown_list = set()
    known_list = set()
    if not len(listdir(path)):
        delete(path)
        return {}
    else:
        new_path_name = normalize(path)
        for i in new_path_name.iterdir():
            if (i.name == "video") or (i.name == "audio") or (i.name == "archives") or (i.name == "documents") or (i.name == "images"):
                continue
            i_path = new_path_name / i
            if i_path.is_dir():
                new_path = normalize(i_path)
                l = sorting(new_path, list_path)
                if len(l):
                    unknown_list.union(l[0])
                    known_list.union(l[1])
            else:
                i_new = normalize(i_path)
                # i_roz_with = i_new.name.split(".")
                i_roz = i_new.suffix.removeprefix(".")
                if (i_roz == "jpg") or (i_roz == "png") or (i_roz == "jpeg") or (i_roz == "svg") or (i_roz == "bmp"):
                    known_list.add(i_roz)
                    move_files(i_new, 4, list_path)
                elif (i_roz == "avi") or (i_roz == "mp4") or (i_roz == "mov") or (i_roz == "mkv"):
                    known_list.add(i_roz)
                    move_files(i_new, 0, list_path)
                elif (i_roz == "doc") or (i_roz == "docx") or (i_roz == "txt") or (i_roz == "pdf") or (i_roz == "rtf") or (i_roz == "xlsx") or (i_roz == "xls") or (i_roz == "pptx") or (i_roz == "ppt") or (i_roz == "vsdx"):
                    known_list.add(i_roz)
                    move_files(i_new, 3, list_path)
                elif (i_roz == "mp3") or (i_roz == "ogg") or (i_roz == "wav") or (i_roz == "amr"):
                    known_list.add(i_roz)
                    move_files(i_new, 2, list_path)
                elif (i_roz == "zip") or (i_roz == "tar") or (i_roz == "gz") or (i_roz == "rar") or (i_roz == "ZIP") or (i_roz == "7z"):
                    known_list.add(i_roz)
                    move_files(i_new, 1, list_path)
                    arh_temp_path = i_new.name.removesuffix(i_new.suffix)
                    arh_p = list_path[0][1] / arh_temp_path
                    try:
                        unpack_archive(arh_p)
                    except OSError as e:
                        print(
                            f'Не вдалось розпакуати архів {i_new.name}. Помилка: {e.strerror}')
                else:
                    unknown_list.add(i_roz)
                    try:
                        move(i_new, list_path[0][5])
                    except OSError as e:
                        print(
                            f"Не вдалось перемістити файл {i_new.name}. Помилка: {e.strerror}")
    if not len(listdir(path)):
        delete(new_path_name)
    return [unknown_list, known_list]


def creating_folder(path: Path) -> list:
    """Створення папок для перенесення файлів"""
# -----------Створення папок для відео-----------
    video_path = path / 'video'
    video_path.mkdir(exist_ok=True)
    list_video_path = ['AVI', 'MP4', 'MOV', 'MKV']
    for name_path in list_video_path:
        pod_video_path = video_path / name_path
        pod_video_path.mkdir(exist_ok=True)
    # ------Створення папок для архівів--------------
    archive_path = path / "archives"
    archive_path.mkdir(exist_ok=True)
    list_arhive_path = ['RAR', '7Z', 'TAR', 'GZ', 'ZIP']
    for name_path in list_arhive_path:
        pod_video_path = archive_path / name_path
        pod_video_path.mkdir(exist_ok=True)
    # ------Створення папок для аудио-файлів--------------
    audio_path = path / "audio"
    audio_path.mkdir(exist_ok=True)
    list_audio_path = ['MP3', 'OGG', 'WAV', 'AMR']
    for name_path in list_audio_path:
        pod_video_path = audio_path / name_path
        pod_video_path.mkdir(exist_ok=True)
    # ------Створення папок для документів--------------
    document_path = path / "documents"
    document_path.mkdir(exist_ok=True)
    list_docum_path = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
    for name_path in list_docum_path:
        pod_video_path = document_path / name_path
        pod_video_path.mkdir(exist_ok=True)
    # ------Створення папок для зображень--------------
    image_path = path / "images"
    image_path.mkdir(exist_ok=True)
    list_images_path = ['JPEG', 'PNG', 'JPG', 'SVG']
    for name_path in list_images_path:
        pod_video_path = image_path / name_path
        pod_video_path.mkdir(exist_ok=True)
    # ------Створення папки для іншого--------------
    other_path = path / "other"
    other_path.mkdir(exist_ok=True)
    main_list_dir = [video_path, archive_path,
                     audio_path, document_path, image_path, other_path]
    list_path = [list_video_path, list_video_path,
                 list_audio_path, list_docum_path, list_images_path]
    return [main_list_dir, list_path]
