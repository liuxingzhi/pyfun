import os
import stat
import codecs
import os.path
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import time
import img2pdf
import sys
from typing import Iterator, Callable, Collection


def timeit(func: Callable) -> Callable:
    """一个计时器"""

    def wrapper(*args, **kwargs):
        start = time.process_time()
        response = func(*args, **kwargs)
        end = time.process_time()
        print('time spend:', end - start)
        return response

    return wrapper


def sieve(path: str, desired: Collection) -> Iterator[str]:
    """walk can recursively list sub directories"""
    for root, dirs, files in os.walk(path):
        files.sort()
        for file_name in files:
            if os.path.splitext(file_name)[-1].lower() in desired:
                yield os.path.join(root, file_name)


def get_pdf_names(path: str) -> Iterator[str]:
    """first convert all imgs to corresponding pdfs"""
    all_pictures2pdf(path, fixed_size=True)
    return sieve(path, [".pdf"])


def get_picture_names(path: str) -> Iterator[str]:
    img_extensions = {".jpg", ".png", ".jpeg"}
    return sieve(path, img_extensions)


def all_pictures2pdf(path: str, fixed_size: bool = False) -> None:
    # specify paper size (A4)
    a4inpt = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
    layout_fun = img2pdf.get_layout_fun(a4inpt, auto_orient=True) if fixed_size else img2pdf.get_layout_fun(
        auto_orient=True)
    for pic_name in get_picture_names(path):
        pdf_name = pic_name.split(".")[-1] + ".pdf"
        with open(pdf_name, "wb") as pdf:
            pdf.write(img2pdf.convert(pic_name, layout_fun=layout_fun))


@timeit
def merge_pdf(path: str, output_filename: str, bookmark_separator: str = "", bookmark_start_index: int = 1,
              password: str = "") -> None:
    """
    合并一个文件里所有的pdf
    :param str path: 文件夹路径
    :param str output_filename: 输出文件名(包含路径)
    :param str bookmark_separator: 用来分割每一个pdf的书签格式，会自动给你添加后缀
    :param int bookmark_start_index: 书签后缀开始的序号
    :param str password: 如果pdf有加密，这里填pdf的密码
    """
    if os.path.exists(output_filename):
        os.remove(output_filename)
    os.chmod(path, stat.S_IRWXU)  # ensure we have permission
    output_pdf = PdfFileMerger()
    output_page_num = 0
    for index, pdf_path_with_name in enumerate(get_pdf_names(path), bookmark_start_index):
        # print(pdf_path_with_name)
        with open(pdf_path_with_name, "rb") as pdf:
            content = PdfFileReader(pdf)
            if content.isEncrypted:
                content.decrypt(password)
            # add bookmark at the beginning of each merged pdf if bookmark_separator is not None
            if bookmark_separator:
                output_pdf.addBookmark(bookmark_separator + str(index), output_page_num)
            else:
                output_pdf.addBookmark(pdf_path_with_name.split("/")[-1] + str(index), output_page_num)
            output_pdf.append(content)
            output_page_num += content.numPages

    with codecs.open(output_filename, "wb") as f:
        output_pdf.write(f)
    print("mission complete")


def rotate_pdf(input_filename: str, output_filename: str, degree: int, output_dir='.') -> None:
    """
    Rotates a page clockwise by increments of 90 degrees.
    :param str input_filename: input_pdf name
    :param str output_filename: output_pdf name
    :param int degree: Angle to rotate the page.  Must be an increment of 90 deg.
    :param str output_dir: directory of output file
    """
    pdf_in = open(input_filename, 'rb')
    pdf_reader = PdfFileReader(pdf_in)
    pdf_writer = PdfFileWriter()

    for page_number in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_number)
        page.rotateClockwise(degree)
        pdf_writer.addPage(page)

    if os.path.exists(output_filename):
        os.remove(output_filename)
    os.chmod(output_dir, stat.S_IRWXU)  # ensure we have permission

    pdf_out = open(output_filename, 'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()


def print_usage() -> None:
    print("usage: python <directory_name> <combined.pdf>")


if __name__ == '__main__':
    # print("\n".join(get_file_name('.')))
    # print(os.listdir('.'))
    if len(sys.argv) == 1:
        merge_pdf("imgs", "testimg.pdf")
    elif len(sys.argv) == 3:
        merge_pdf(sys.argv[1], sys.argv[2])
    else:
        print_usage()
