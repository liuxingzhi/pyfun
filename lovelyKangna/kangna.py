import os
import platform
from time import sleep


class Kangna:
    def __init__(self, filename):
        self.outlook_matrix = []
        self.steplen = 20
        self.leftcol = 0
        self.display_limit = 200
        self.interval = 0.5
        with open(filename) as f:
            for line in f.readlines():
                self.outlook_matrix.append(line.strip("\n"))

    def run(self):
        """
        1.清屏
        2.右移康纳矩阵
        3.画康纳
        4.循环
        :return:
        """
        while self.leftcol < self.display_limit:
            if platform.system() == "Windows":
                os.system("cls")
            else:
                os.system("clear")
            self.shift()
            self.show()
            self.leftcol += self.steplen
            sleep(self.interval)

    def shift(self):
        for index, line in enumerate(self.outlook_matrix, 0):
            self.outlook_matrix[index] = line[:self.steplen] + line
            # print(line)

    def show(self):
        for line in self.outlook_matrix:
            print(line)

    def __str__(self):
        return "".join(self.outlook_matrix)


if __name__ == '__main__':
    kangna = Kangna("kanna.txt")
    kangna.run()
    # kangna.show()
