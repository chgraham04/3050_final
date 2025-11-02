"""Module for automatically downloading and importing Stockfish chess engine."""
import os
import platform
from urllib.request import urlopen
from zipfile import ZipFile
from tarfile import open as taropen
from io import BytesIO


def import_stockfish(dir_path="_assets/stockfish"):
    """
    Automatically downloads and opens stockfish chess engine.

    Args:
        dir_path: Directory path where Stockfish will be stored
    Returns:
        Path to Stockfish executable, or None if installation fails
    """
    print(f"Checking for Stockfish in: {dir_path}")

    stockfish_found = False
    system = platform.system()
    print(f"Detected OS: {system}")

    # Check if stockfish is already installed
    if os.path.exists(dir_path):
        print(f"Directory exists, searching for Stockfish...")
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                print(f"Found file: {file}")
                if 'stockfish' in file.lower():
                    # On Windows, must end with .exe
                    if system == "Windows" and file.endswith('.exe'):
                        stockfish_found = True
                        path_to_stockfish = os.path.join(root, file)
                        print(f"Found Stockfish (Windows): {path_to_stockfish}")
                        return path_to_stockfish
                    # On Mac/Linux, just needs 'stockfish' in name and no .exe
                    elif system != "Windows" and not file.endswith('.exe'):
                        stockfish_found = True
                        path_to_stockfish = os.path.join(root, file)
                        print(f"Found Stockfish (Unix): {path_to_stockfish}")
                        return path_to_stockfish
    else:
        print(f"Directory does not exist yet")

    # install if not found
    if not stockfish_found:
        print("Stockfish not found. Downloading...")
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

        print(f"Downloading from: {file_path}")

        try:
            # Open and read download link
            print("Opening URL...")
            opened_file = urlopen(file_path, timeout=30)
            print("Reading file data...")
            file_data = BytesIO(opened_file.read())
            print("Download complete. Extracting...")

            # Extract - different types for windows and linux/mac
            if zip_file:
                with ZipFile(file_data) as zip_file_obj:
                    zip_file_obj.extractall(path=dir_path)
                    print("Extraction complete (ZIP)")
            else:
                with taropen(fileobj=file_data) as tar_file:
                    tar_file.extractall(path=dir_path)
                    print("Extraction complete (TAR)")

            # Locate the executable stockfish file
            print("Searching for extracted Stockfish executable...")
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    print(f"Checking extracted file: {file}")
                    if 'stockfish' in file.lower():
                        path_to_stockfish = os.path.join(root, file)

                        # Make executable on Unix systems
                        if system != "Windows":
                            print(f"Making file executable: {path_to_stockfish}")
                            # file privileges
                            os.chmod(path_to_stockfish, 0o755)

                        print(f"Stockfish ready at: {path_to_stockfish}")
                        return path_to_stockfish

            print("ERROR: Stockfish could not be found after extraction")
            return None

        except Exception as e:
            print(f"ERROR: Failed to download/install Stockfish: {e}")
            return None