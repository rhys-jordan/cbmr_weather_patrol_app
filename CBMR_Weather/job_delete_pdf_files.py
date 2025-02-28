import os

directory = "./past_pdfs/"

def delete_files():
    for file in os.scandir(directory):
        if file.is_file():
            os.remove(file)
