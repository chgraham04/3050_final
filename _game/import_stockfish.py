""" Module for importing and downloading Stockfish chess engine """
import os
import platform
import ssl
from urllib.request import urlopen
from zipfile import ZipFile
from tarfile import open as taropen
from io import BytesIO


def import_stockfish(dir_path="_assets/stockfish"):
    """
    Automatically downloads and opens stockfish chess engine

    Args:
        dir_path: Directory path where Stockfish will be stored (_assets/stockfish)
    Returns:
        Path to Stockfish executable, or None if installation fails
    """
    stockfish_found = False
    system = platform.system()
    print(f"Detected OS: {system}")

    # Check if stockfish is already installed
    if os.path.exists(dir_path):
        print("Directory exists, checking for Stockfish...")
        for root, _, files in os.walk(dir_path):
            for file in files:
                print(f"Found file: {file}")
                if 'stockfish' in file.lower():
                    # On Windows, look for .exe
                    if system == "Windows" and file.endswith('.exe'):
                        stockfish_found = True
                        path_to_stockfish = os.path.join(root, file)
                        print(f"Found Stockfish (Windows): {path_to_stockfish}")
                        return path_to_stockfish
                    # On Unix, check if executable
                    if system != "Windows" and file.lower() == 'stockfish':
                        path_to_stockfish = os.path.join(root, file)
                        if os.access(path_to_stockfish, os.X_OK):
                            print(f"Found Stockfish (Unix): {path_to_stockfish}")
                            return path_to_stockfish

    # If not installed, install it
    if not stockfish_found:
        print("Stockfish not found, downloading...")
        context = ssl._create_unverified_context()  # pylint: disable=protected-access
        os.makedirs(dir_path, exist_ok=True)

        # Get different install link per platform
        if system == "Windows":
            file_path = "https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-windows-x86-64-avx2.zip"
            is_zip = True
        elif system == "Linux":
            file_path = "https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-ubuntu-x86-64-avx2.tar"
            is_zip = False
        elif system == "Darwin":
            file_path = "https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-macos-m1-apple-silicon.tar"
            is_zip = False
        else:
            print(f"ERROR: Unsupported OS: {system}")
            return None

        try:
            print(f"Downloading from: {file_path}")
            # Open and read download link with timeout
            with urlopen(file_path, context=context, timeout=30) as opened_file:
                print("Reading file data...")
                file_data = BytesIO(opened_file.read())

            print("Download complete, extracting...")

            # Extract
            if is_zip:
                with ZipFile(file_data) as zip_file_obj:
                    zip_file_obj.extractall(path=dir_path)
                print("Extracted ZIP file")
            else:
                with taropen(fileobj=file_data) as tar_file:
                    tar_file.extractall(path=dir_path)
                print("Extracted TAR file")

            # Locate the executable stockfish file
            print("Searching for Stockfish executable...")
            for root, _, files in os.walk(dir_path):
                for file in files:
                    print(f"Checking file: {file}")
                    # Windows - look for .exe
                    if system == "Windows" and 'stockfish' in file.lower() and file.endswith('.exe'):
                        path_to_stockfish = os.path.join(root, file)
                        print(f"Found Stockfish: {path_to_stockfish}")
                        return path_to_stockfish
                    # Unix - look for executable named "stockfish"
                    if system != "Windows" and file.lower() == 'stockfish':
                        path_to_stockfish = os.path.join(root, file)
                        print("Making file executable...")
                        os.chmod(path_to_stockfish, 0o755)
                        print(f"Found Stockfish: {path_to_stockfish}")
                        return path_to_stockfish

            print("ERROR: Stockfish executable not found after extraction")
            return None

        except Exception as error:
            print(f"ERROR: Failed to download/install Stockfish: {error}")
            import traceback
            traceback.print_exc()
            return None

    return None
