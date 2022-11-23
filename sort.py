from pathlib import Path
# from os import rename, listdir
# from shutil import move, unpack_archive
# from os.path import join
import function


p = Path(input("Введіть шлях до папки:"))
if p.is_dir():
    # -----------Створення папок для відео-----------
    video_path = p / 'video'
    video_path.mkdir(exist_ok=True)
    list_video_path = ['AVI', 'MP4', 'MOV', 'MKV']
    for name_path in list_video_path:
        pod_video_path = video_path / name_path
        pod_video_path.mkdir(exist_ok=True)
    # ------Створення папок для архівів--------------
    archive_path = p / "archives"
    zip_path = archive_path / 'ZIP'
    list_arhive_path = ['RAR', '7Z', 'TAR', 'GZ']
    for name_path in list_arhive_path:
        pod_video_path = video_path / name_path
        pod_video_path.mkdir(exist_ok=True)
    # ------Створення папок для аудио-файлів--------------
    audio_path = p / "audio"
    audio_path.mkdir(exist_ok=True)
    list_audio_path = ['MP3', 'OGG', 'WAV', 'AMR']
    for name_path in list_audio_path:
        pod_video_path = video_path / name_path
        pod_video_path.mkdir(exist_ok=True)
    # ------Створення папок для документів--------------
    document_path = p / "documents"
    document_path.mkdir(exist_ok=True)
    list_docum_path = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
    for name_path in list_docum_path:
        pod_video_path = video_path / name_path
        pod_video_path.mkdir(exist_ok=True)
    # ------Створення папок для зображень--------------
    image_path = p / "images"
    image_path.mkdir(exist_ok=True)
    list_images_path = ['JPEG', 'PNG', 'JPG', 'SVG']
    for name_path in list_docum_path:
        pod_video_path = video_path / name_path
        pod_video_path.mkdir(exist_ok=True)

    result = function.sorting(p, video_path, archive_path,
                              audio_path, document_path, image_path)
    print("Сортування виконано успішно!")
    print("Список відомих розширень файлів у папці:", result[1])
    print("Список невідомих розширень у папці:", result[0])
else:
    print("Це не шлях до папки!")
