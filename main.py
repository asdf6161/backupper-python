import datetime
import os
import zipfile
from subprocess import Popen
import subprocess

FILE_DIR_LIST = "dir.lst"


def get_dir_list():
    """
    :return: returl directory list from file
    """
    dir_list = []
    res = os.path.exists(FILE_DIR_LIST)
    if res:
        file = open(FILE_DIR_LIST, 'r', encoding='utf-8')
        dir_list = file.read().split("\n")
        if not dir_list[-1]:
            dir_list.pop()
        file.close()
    else:
        print("File not found {}".format(FILE_DIR_LIST))
    return dir_list


def print_zip_info(archive_name):
    zf = zipfile.ZipFile(archive_name)
    for info in zf.infolist():
        print(info.filename)
        print('\tComment:\t', info.comment)
        print('\tModified:\t', datetime.datetime(*info.date_time))
        print('\tSystem:\t\t', info.create_system, '(0 = Windows, 3 = Unix)')
        print('\tZIP version:\t', info.create_version)
        print('\tCompressed:\t', info.compress_size, 'bytes')
        print('\tUncompressed:\t', info.file_size, 'bytes')


def zip_all_paths(dir_list, path_to_save='', file_name='zipfile_write.zip'):
    zip_path = path_to_save + file_name
    print('Creating archive')
    if path_to_save:
        if not (path_to_save.endswith('/') or path_to_save.endswith('\\')):
            path_to_save += '/'
    zf = zipfile.ZipFile(zip_path, mode='w')
    print("Getting file count")
    files_count = 0
    for el in dir_list:
        files_count += get_files_cnt(el)
    print("IS total files - ", files_count)
    try:
        for el in dir_list:
            print('\rAdding to archive\t{}'.format(el))
            if os.path.isdir(el):
                for folder, subfolders, files in os.walk(el):
                    for file in files:
                        print('\rAdding to archive\t{}'.format(folder+"\\"+file))
                        zf.write(os.path.join(folder, file),
                                 os.path.relpath(os.path.join(folder, file), el),
                                 compress_type=zipfile.ZIP_DEFLATED)
            else:
                zf.write(el)
    finally:
        print('Archive closing {}'.format(zip_path))
        zf.close()
    print_zip_info(zip_path)


def get_files_cnt(path):
    """
    :param path: Папка в которой нужно посчитать число файлов
    :return: File count
    """
    if os.path.isdir(path):
        return 0
    return 0


def run_bat(path, file_name):
    p = Popen(path + file_name, stdout=subprocess.PIPE, shell=True)
    # stdout, stderr = p.communicate()
    for line in p.stdout.readlines():
        print(line.decode("utf-8"), end='')

    ret_code = p.wait()
    # print("Вывод = ", stdout)
    # print("Ошибка", stderr)
    print("Код завершения = ", ret_code)


if __name__ == '__main__':
    # run_bat("E:/", "test.bat")
    lst = get_dir_list()
    zip_all_paths(dir_list=lst)
    print(lst)
