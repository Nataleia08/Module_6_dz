from pathlib import Path
import shutil
import os


def translate_name_file(name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЄІЇҐ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "A", "B", "V", "G", "D", "E", "E", "J", "Z", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U",
                   "F", "H", "Ts", "Ch", "Sh", "Sch", "E", "Yu", "Ya", "Je", "I", "Ji", "G")
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
    new_name = name.translate(TRANS)
    return new_name


def replacement_symbols_file_name(name):
    list_name = list(name)
    i = 0
    for n in list_name:
        if (not n.isalpha()) and (not n.isdigit()):
            list_name[i] = "_"
        i = i + 1
    new_name = "".join(list_name)
    return new_name


def normalize(path: Path):
    if path.is_dir():
        full_name = path.name
        full_transtale_name = translate_name_file(full_name)
        full_clear_name = replacement_symbols_file_name(full_transtale_name)
        if full_clear_name != full_name:
            return path.replace(full_clear_name)
        else:
            return path
    elif path.is_file():
        full_name = path.name
        list_name = full_name.split(".")
        list_name[0] = translate_name_file(list_name[0])
        list_name[0] = replacement_symbols_file_name(list_name[0])
        new_name = ".".join(list_name)
        if new_name != full_name:
            new_path = path.parent / new_name
            return path.replace(new_path)
        else:
            return path


def delete(path: Path):
    try:
        path.rmdir()
    except OSError as e:
        print(
            f'Не вдалось видалити порожню папку за шляхом {path}. Помилка: {e.strerror}')


def sorting(path: Path, video_path: Path, archive_path: Path, audio_path: Path, document_path: Path, image_path: Path):
    unknown_list = []
    known_list = []
    path = normalize(path)
    if not len(os.listdir(path)):
        delete(p)
    for i in p.iterdir():
        if i.is_dir():
            l = sorting(i, video_path, archive_path,
                        audio_path, document_path, image_path)
            unknown_list.extend(l[0])
            known_list.extend(l[0])
        else:
            i = normalize(i)
            i_roz_with = i.name.split(".")
            i_roz = i_roz_with[1]
            if (i_roz == "jpg") or (i_roz == "png") or (i_roz == "jpeg") or (i_roz == "svg"):
                known_list.append(i_roz)
                shutil.move(i, image_path)
            elif (i_roz == "avi") or (i_roz == "mp4") or (i_roz == "mov") or (i_roz == "mkv"):
                shutil.move(i, video_path)
                known_list.append(i_roz)
            elif (i_roz == "doc") or (i_roz == "docx") or (i_roz == "txt") or (i_roz == "pdf") or (i_roz == "rtf") or (i_roz == "xslx") or (i_roz == "slx") or (i_roz == "pptx") or (i_roz == "ppt"):
                shutil.move(i, document_path)
                known_list.append(i_roz)
            elif (i_roz == "mp3") or (i_roz == "ogg") or (i_roz == "wav") or (i_roz == "amr"):
                shutil.move(i, audio_path)
                known_list.append(i_roz)
            elif (i_roz == "zip") or (i_roz == "tar") or (i_roz == "gz"):
                shutil.move(i, archive_path)
                arh_p = i + "/" + i_roz_with[0]
                shutil.unpack_archive(arh_p)
                known_list.append(i_roz)
            else:
                unknown_list.append(i_roz)
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
    print("Список невідомих розширень у папці:", l[0])
else:
    print("Це не шлях до папки!")
