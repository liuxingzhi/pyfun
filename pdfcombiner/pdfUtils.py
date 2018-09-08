import os, sys, stat
import codecs
import os.path
from PyPDF2 import PdfFileReader,PdfFileWriter,PdfFileMerger
import time
# import img2pdf
from PIL import Image
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
    """walk can recursively list sub directories"""
    for root,dirs,files in os.walk(path):
        for file_name in files:
            if os.path.splitext(file_name)[1].lower() == ".pdf":
                yield os.path.join(root,file_name)

def get_picture_names(path):
    for root,dirs,files in os.walk(path):
        for file_name in files:
            if os.path.splitext(file_name)[1].lower() == ".jpg":
                yield os.path.join(root,file_name)

def pictures_to_pdf(path):
    for pic_name in get_picture_names(path):
        print(pic_name)
        # with open("name.pic_name","wb") as f:
        # f.write(img2pdf.convert('test.jpg'))

@timeit
def merge_pdf(path,outfile):
    if os.path.exists(outfile):
        os.remove(outfile)
    os.chmod(path,stat.S_IRWXU)
    output_pdf=PdfFileMerger()
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
    with codecs.open(outfile,"wb") as f:
        output_pdf.write(f)
    print("mission complete")


if __name__ == '__main__':
    # print("\n".join(get_file_name('.')))
    # print(os.listdir('.'))
    merge_pdf("pdfs","temp.pdf")

