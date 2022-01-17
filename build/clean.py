from pathlib import Path

temp_image_dir = Path("./temp/captured_image")
temp_separated = Path("./temp/separated")
temp_audio_cutted = Path("./temp/cutted_audio")


def clean_dir(dir_path: Path):
    file_list = list(dir_path.glob('*'))
    for file in file_list:
        file.unlink()
    return


def cleanup():
    clean_dir(temp_image_dir)
    clean_dir(temp_separated)
    clean_dir(temp_audio_cutted)


def cleanup2():
    clean_dir(temp_image_dir)
    clean_dir(temp_audio_cutted)


if __name__ == "__main__":
    cleanup()
