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
            if os.path.splitext(file_name)[1].lower() == ".pdf":
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
def merge_pdf(path, output_filename):
    if os.path.exists(output_filename):
        os.remove(output_filename)
    os.chmod(path, stat.S_IRWXU)  # ensure we have permission
    output_pdf = PdfFileMerger()
    output_page_num = 0
    for pdf_name in get_pdf_names(path):
        print(pdf_name)
        with open(pdf_name, "rb") as pdf:
            content = PdfFileReader(pdf)
            output_pdf.append(content)
            # content = PdfFileReader(pdf)
            # if content.isEncrypted:
            #     password = "password"
            #     content.decrypt(password)
            #
            # output_page_num += content.numPages
            #
            # for i in range(content.numPages):
            #     output_pdf.addPage(content.getPage(i))
    with codecs.open(output_filename, "wb") as f:
        output_pdf.write(f)
    print("mission complete")


def print_usage():
    print("usage: python <directory_name> <combined.pdf>")


if __name__ == '__main__':
    # print("\n".join(get_file_name('.')))
    # print(os.listdir('.'))
    if len(sys.argv) == 1:
        merge_pdf("ling_exam2", "ling_combine.pdf")
    elif len(sys.argv) == 3:
        merge_pdf(sys.argv[1], sys.argv[2])
    else:
        print_usage()
