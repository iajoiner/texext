import argparse
import os
import texlexparse
import ply.yacc as yacc

def printfile(file_list):
    for file in file_list:
        print(f'{file}')
        if not (os.path.isfile(file) and os.access(file, os.R_OK)):
            #Do all files in the file list exist and are they all accessible?
            print(f"File {file} not found or inaccessible.")
            return None
            #TODO: Modify this to allow tolerance of bad files
            #file_list.remove(file)
    for file in file_list:
        print(f"File {file} is found!")
        with open(file, 'r') as f:
            data = f.read()
            proc_data = yacc.parse(data, debug = texlexparse.log)
            print(proc_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process the .prg files.')
    parser.add_argument('file', metavar='file', type=str, help='A file to process', nargs='+')
    printfile(vars(parser.parse_args()).get('file'))
