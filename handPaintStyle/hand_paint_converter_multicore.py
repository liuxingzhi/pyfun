# 借鉴于中国MOOC大学python数据分析教程 嵩天教授
import multiprocessing
from PIL import Image
from typing import Iterator, Callable, Collection
import numpy as np
import os
import re

WITHOUT_TOPMOST_DIR_REGEX = r'^.*?(/+|\\+)(.*)'
topmost_dir_pattern = re.compile(WITHOUT_TOPMOST_DIR_REGEX)
queue = multiprocessing.Queue()


def sieve(path: str, desired: Collection) -> Iterator[str]:
    """walk can recursively list sub directories"""
    for root, dirs, files in os.walk(path):
        files.sort()
        for file_name in files:
            if os.path.splitext(file_name)[-1].lower() in desired:
                yield os.path.join(root, file_name)


def get_picture_names(path: str) -> Iterator[str]:
    img_extensions = {".jpg", ".png", ".jpeg"}
    return sieve(path, img_extensions)


def handify_dir(old_dir: str, new_dir: str):
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    for oldpath in get_picture_names(old_dir):
        parents_dir = os.path.split(oldpath)[0].replace(old_dir, new_dir, 1)
        if not os.path.exists(parents_dir):
            os.makedirs(parents_dir)
        newpath = os.path.join(new_dir, re.search(topmost_dir_pattern, oldpath).group(2))
        # print(newpath)
        queue.put((oldpath, newpath))
    worker_num = 4
    pool = multiprocessing.Pool(worker_num)
    for i in range(worker_num):
        queue.put(None)
    for i in range(worker_num):
        pool.apply_async(worker)
        print("start a new process", i)
    pool.close()
    pool.join()


def worker():
    while True:
        task = queue.get()
        if task is None:
            break
        img_path, save_path = task
        handify(img_path, save_path)
        print(f"handified {img_path} to {save_path}")


def handify(img_path: str, save_path: str):
    a = np.asarray(Image.open(img_path).convert('L')).astype('float')

    depth = 125.  # (0-100)，每张图片的最佳深度值不一样，需要自己调整
    grad = np.gradient(a)  # 取图像灰度的梯度值
    grad_x, grad_y = grad  # 分别取横纵图像梯度值
    grad_x = grad_x * depth / 100.
    grad_y = grad_y * depth / 100.

    # 构造x和y轴梯度的三维归一化单位坐标系
    A = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)
    uni_x = grad_x / A
    uni_y = grad_y / A
    uni_z = 1. / A

    vec_el = np.pi / 2.2  # 光源的俯视角度，弧度值
    vec_az = np.pi / 4  # 光源的方位角度，弧度值
    dx = np.cos(vec_el) * np.cos(vec_az)  # 光源对x 轴的影响
    dy = np.cos(vec_el) * np.sin(vec_az)  # 光源对y 轴的影响
    dz = np.sin(vec_el)  # 光源对z 轴的影响

    b = 255 * (dx * uni_x + dy * uni_y + dz * uni_z)  # 光源归一化
    b = b.clip(0, 255)  # 防止像素超出范围

    im = Image.fromarray(b.astype('uint8'))  # 重构图像
    im.save(save_path)


if __name__ == '__main__':
    # convert("beijing.jpg", "beijingHD.jpg")
    handify_dir("2222", "2333")
