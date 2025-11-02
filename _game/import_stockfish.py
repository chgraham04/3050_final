import os
import platform
from urllib.request import urlopen
from zipfile import ZipFile
from tarfile import open as taropen
from io import BytesIO

def import_stockfish(dir_path="assets/stockfish"):
    """ Automatically downloads and opens stockfish chess engine """

    stockfish_found = False
    system = platform.system()

    if system == "Windows":
        executable_extensions = ('.exe',)
    else:
        # no .exe extension on Unix
        executable_extensions = ('', 'stockfish')

    # Check if stockfish is already installed
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if 'stockfish' in file.lower():
                # WINDOWS
                if system == "Windows" and file.endswith('.exe'):
                    stockfish_found = True
                    path_to_stockfish = os.path.join(root, file)
                    return path_to_stockfish
                # MAC/LINUX
                elif system != "Windows":
                    stockfish_found = True
                    path_to_stockfish = os.path.join(root, file)
                    return path_to_stockfish

    # install if not installed
    if not stockfish_found:
        os.makedirs(dir_path, exist_ok=True)

        if system == "Windows":
            file_path = "https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-windows-x86-64-avx2.zip"
            zip_file = True
        elif system == "Linux":
            file_path = "https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-ubuntu-x86-64-avx2.tar"
            zip_file = False
        elif system == "Darwin":  # Mac
            file_path = "https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-macos-m1-apple-silicon.tar"
            zip_file = False
        else:
            raise Exception(f"Unsupported OS: {system}")

        try:
            # Open and read download link
            opened_file = urlopen(file_path)
            file_data = BytesIO(opened_file.read())

            # Extract - different types for windows and linux/mac
            if zip_file:
                with ZipFile(file_data) as zip_file_obj:
                    zip_file_obj.extractall(path=dir_path)
            else:
                with taropen(fileobj=file_data) as tar_file:
                    tar_file.extractall(path=dir_path)

            # Locate the executable stockfish file
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    if 'stockfish' in file.lower():
                        path_to_stockfish = os.path.join(root, file)

                        # Make executable on Unix systems
                        if system != "Windows":\
                            # set file permissions
                            os.chmod(path_to_stockfish, 0o755)

                        return path_to_stockfish

            print("Stockfish could not be installed")
            return None

        except FileNotFoundError:
            print("File could not be found")
            return None
