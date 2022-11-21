from pathlib import Path
import shutil


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
        if (not n.isalpha()) or (not n.isdigit()):
            list_name[i] = "_"
        i = i + 1
    new_name = "".join(list_name)
    return new_name


def normalize(path):
    full_name = path.name()
    list_name = ".".split(full_name)
    list_name[0] = translate_name_file(list_name[0])
    list_name[0] = replacement_symbols_file_name(list_name[0])
    new_name = ".".join(list_name)
    path.rename(new_name)


def delete(path):
    try:
        path.rmdir()
    except OSError as e:
        print(
            f'Не вдалось видалити порожню папку за шляхом {path}. Помилка: {e.strerror}')


def sorting(path, video_path, archive_path, audio_path, document_path, image_path):
    unknown_list = []
    known_list = []
    normalize(path)
    if not len(p.iterdir()):
        delete(p)
    for i in p.iterdir():
        if i.is_dir:
            sorting(i, video_path, archive_path,
                    audio_path, document_path, image_path)
        else:
            normalize(i)
            p_name = i.name()
            list_name = p_name.split(".")
            if (list_name[1] == "jpg") or (list_name[1] == "png") or (list_name[1] == "jpeg") or (list_name[1] == "svg"):
                known_list.append(list_name[1])
                shutil.move(i, image_path)
            elif (list_name[1] == "avi") or (list_name[1] == "mp4") or (list_name[1] == "mov") or (list_name[1] == "mkv"):
                shutil.move(i, video_path)
                known_list.append(list_name[1])
            elif (list_name[1] == "doc") or (list_name[1] == "docx") or (list_name[1] == "txt") or (list_name[1] == "pdf") or (list_name[1] == "rtf") or (list_name[1] == "xslx") or (list_name[1] == "slx") or (list_name[1] == "pptx") or (list_name[1] == "ppt"):
                shutil.move(i, document_path)
                known_list.append(list_name[1])
            elif (list_name[1] == "mp3") or (list_name[1] == "ogg") or (list_name[1] == "wav") or (list_name[1] == "amr"):
                shutil.move(i, audio_path)
                known_list.append(list_name[1])
            elif (list_name[1] == "zip") or (list_name[1] == "tar") or (list_name[1] == "gz"):
                shutil.move(i, archive_path)
                arh_p = i + "/" + list_name[0]
                shutil.unpack_archive(arh_p)
                known_list.append(list_name[1])
            else:
                unknown_list.append(list_name[1])


p = Path(input("Введіть шлях до папки:"))
if not p.is_dir:
    print("Це не шлях до папки!")
else:
    video_path = p / '/video'
    video_path.mkdir()
    archive_path = p / "/archives"
    archive_path.mkdir()
    audio_path = p / "/audio"
    audio_path.mkdir()
    document_path = p / "/documents"
    document_path.mkdir()
    image_path = p / "/images"
    image_path.mkdir()
    sorting(p, video_path, archive_path, audio_path, document_path, image_path)
