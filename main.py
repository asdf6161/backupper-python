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


def test_zip(archive_name):
    zf = zipfile.ZipFile(archive_name)
    res = zf.testzip()
    if res:
        print(res)
        raise Exception('check error {}'.format(archive_name))


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

    # check existing file
    res = os.path.exists(zip_path)
    if res:
        print("File exist, (1) to rewrite, (0) exit(2): ")
        inp = int(input())
        if inp != 1:
            exit(2)

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

    # adding files to archive
    try:
        for el in dir_list:
            if os.path.isdir(el):
                for folder, subfolders, files in os.walk(el):
                    for file in files:
                        zf.write(os.path.join(folder, file),
                                 os.path.relpath(os.path.join(folder, file), el),
                                 compress_type=zipfile.ZIP_DEFLATED)
                        files_count -= 1
                        print("\rОсталось файлов - {};\t".format(files_count), end='')
                        print('Adding to archive\t{}'.format(folder+"\\"+file), end='')
            else:
                zf.write(el)
    finally:
        print('Archive closing {}'.format(zip_path))
        zf.close()
    test_zip(zip_path)


def get_files_cnt(path):
    """
    :param path: Папка в которой нужно посчитать число файлов
    :return: File count
    """
    cnt = 0
    if not os.path.isdir(path):
        cnt += 1
    else:
        for i in os.listdir(path):
            if os.path.isdir(path+'/'+i):
                # recursive
                cnt += get_files_cnt(path+'/'+i)
            else:
                cnt += 1
    return cnt


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
