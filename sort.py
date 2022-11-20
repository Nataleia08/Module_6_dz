from pathlib import Path


def normalize(path):
    return new_path


def img_file(path):


def video_file(path):


def document_file(path):


def audio_file(path):


def archive_file(path):


def delete_file(path):


def sorting(path):
    unknown_list = []
    known_list = []
    if len(p.iterdir()):
        delete_file(p)
    for i in p.iterdir():
        if i.is_dir:
            sorting(i)
        else:
            n_name = normalize(i)
            p_name = n_name.name()
            list_name = p_name.split(".")
            if (list_name[1] == "jpg") or (list_name[1] == "png") or (list_name[1] == "jpeg") or (list_name[1] == "svg"):
                img_file(n_name)
                known_list.append(list_name[1])
            elif (list_name[1] == "avi") or (list_name[1] == "mp4") or (list_name[1] == "mov") or (list_name[1] == "mkv"):
                video_file(n_name)
                known_list.append(list_name[1])
            elif (list_name[1] == "doc") or (list_name[1] == "docx") or (list_name[1] == "txt") or (list_name[1] == "pdf") or (list_name[1] == "rtf") or (list_name[1] == "xslx") or (list_name[1] == "slx") or (list_name[1] == "pptx") or (list_name[1] == "ppt"):
                document_file(n_name)
                known_list.append(list_name[1])
            elif (list_name[1] == "mp3") or (list_name[1] == "ogg") or (list_name[1] == "wav") or (list_name[1] == "amr"):
                audio_file(n_name)
                known_list.append(list_name[1])
            elif (list_name[1] == "zip") or (list_name[1] == "tar") or (list_name[1] == "gz"):
                archive_file(n_name)
                known_list.append(list_name[1])
            else:
                unknown_list.append(list_name[1])


p = Path(input("Введіть шлях до папки:"))
if not p.is_dir:
    print("Це не шлях до папки!")
else:
    sorting(p)
