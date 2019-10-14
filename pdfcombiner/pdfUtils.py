import os
import stat
import codecs
import os.path
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import time
import img2pdf
import sys


def timeit(func):
    """一个计时器"""

    def wrapper(*args, **kwargs):
        start = time.clock()
        response = func(*args, **kwargs)
        end = time.clock()
        print('time spend:', end - start)
        return response

    return wrapper


def get_pdf_names(path):
    """first convert all imgs to corresponding pdfs"""
    all_pictures2pdf(path, fixed_size=True)

    """walk can recursively list sub directories"""
    for root, dirs, files in os.walk(path):
        files.sort()
        for file_name in files:
            if os.path.splitext(file_name)[-1].lower() == ".pdf":
                yield os.path.join(root, file_name)


def get_picture_names(path):
    img_extensions = [".jpg", ".png"]
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if os.path.splitext(file_name)[1].lower() in img_extensions:
                yield os.path.join(root, file_name)


def all_pictures2pdf(path, fixed_size=False):
    # specify paper size (A4)
    a4inpt = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
    layout_fun = img2pdf.get_layout_fun(a4inpt) if fixed_size else img2pdf.get_layout_fun()
    for pic_name in get_picture_names(path):
        pdf_name = pic_name[:-4] + ".pdf"
        with open(pdf_name, "wb") as pdf:
            pdf.write(img2pdf.convert(pic_name, layout_fun=layout_fun))


@timeit
def merge_pdf(path, output_filename, bookmark_separator="", bookmark_start_index=1, password=""):
    """
    合并一个文件里所有的pdf
    :param path: 文件夹路径
    :param output_filename: 输出文件名(包含路径)
    :param bookmark_separator: 用来分割每一个pdf的书签格式，会自动给你添加后缀
    :bookmark_start_index: 书签后缀开始的序号
    :password: 如果pdf有加密，这里填pdf的密码
    :return:
    """
    if os.path.exists(output_filename):
        os.remove(output_filename)
    os.chmod(path, stat.S_IRWXU)  # ensure we have permission
    output_pdf = PdfFileMerger()
    output_page_num = 0
    for index, pdf_path_with_name in enumerate(get_pdf_names(path), bookmark_start_index):
        print(pdf_path_with_name)
        with open(pdf_path_with_name, "rb") as pdf:
            content = PdfFileReader(pdf)
            if content.isEncrypted:
                content.decrypt(password)
            # add bookmark at the beginning of each merged pdf if bookmark_separator is not None
            if bookmark_separator:
                output_pdf.addBookmark(bookmark_separator + str(index), output_page_num)
            else:
                output_pdf.addBookmark(pdf_path_with_name.split("/")[-1], output_page_num)
            output_pdf.append(content)
            output_page_num += content.numPages

    with codecs.open(output_filename, "wb") as f:
        output_pdf.write(f)
    print("mission complete")


def print_usage():
    print("usage: python <directory_name> <combined.pdf>")


if __name__ == '__main__':
    # print("\n".join(get_file_name('.')))
    # print(os.listdir('.'))
    if len(sys.argv) == 1:
        merge_pdf("cs425", "425combined.pdf")
    elif len(sys.argv) == 3:
        merge_pdf(sys.argv[1], sys.argv[2])
    else:
        print_usage()
