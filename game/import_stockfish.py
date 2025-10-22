import os
import platform
from urllib.request import urlopen
from zipfile import ZipFile
from tarfile import open as taropen
from io import BytesIO

#Function automatically downloads and opens stockfish chess engine
def import_stockfish(dir_path = "assets/stockfish"):

    #Check if stockfish is already installed
    for root, dirs, files in os.walk(dir_path):
            for file in files:
                if 'stockfish' in file.lower() and (file.endswith('.exe')):

                    path_to_stockfish = os.path.join(root, file)

                    return path_to_stockfish
                
                #If not installed, install it
                else:
                    os.makedirs(dir_path, exist_ok=True)

                    system = platform.system()

                    #Get different install link per platform
                    if (system == "Windows"):
                        file_path = "https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-windows-x86-64-avx2.zip" #file path
                        zip_file = True

                    elif (system == "Linux"):
                        file_path = "https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-ubuntu-x86-64-avx2.tar"
                        zip_file = False

                    #Mac
                    elif (system == "Darwin"):
                        file_path = "https://github.com/official-stockfish/Stockfish/releases/latest/download/stockfish-macos-m1-apple-silicon.tar"
                        zip_file = False
                    
                    else:
                        raise Exception(f"Unsupported OS: {system}")

                    try:
                        #Open and read download link
                        opened_file = urlopen(file_path)
                        file_data = BytesIO(opened_file.read())

                        #Extract - different types for windows and linux/mac
                        if (zip_file):
                            with ZipFile(file_data) as zip_file:
                                zip_file.extractall(path=dir_path)
                        
                        else:
                            with taropen(fileobj = file_data) as tar_file:
                                tar_file.extractall(path=dir_path)

                        #Locate the executable stockfish file
                        for root, dirs, files in os.walk(dir_path):
                            for file in files:
                                if 'stockfish' in file.lower() and (file.endswith('.exe')):
                                    path_to_stockfish = os.path.join(root, file)

                                    return path_to_stockfish
                        
                        print("Stockfish could not be installed")
                        return None
                        

                    except FileNotFoundError:
                        print("File could not be found")
                        return None

