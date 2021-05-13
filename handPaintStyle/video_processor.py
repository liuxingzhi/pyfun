import numpy as np
import cv2
from moviepy.editor import *

def handify(image: np.ndarray):
    # a = np.asarray(Image.open(img_path).convert('L')).astype('float')
    # a = np.asarray(frame)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    depth = 20.  # (0-100)，每张图片的最佳深度值不一样，需要自己调整
    grad = np.gradient(gray_image)  # 取图像灰度的梯度值
    grad_x, grad_y = grad  # 分别取横纵图像梯度值
    grad_x = grad_x * depth / 100.
    grad_y = grad_y * depth / 100.

    # 构造x和y轴梯度的三维归一化单位坐标系
    A = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)
    uni_x = grad_x / A
    uni_y = grad_y / A
    uni_z = 1. / A

    vec_el = np.pi / 2.2  # 光源的俯视角度，弧度值
    vec_az = np.pi / 2  # 光源的方位角度，弧度值
    dx = np.cos(vec_el) * np.cos(vec_az)  # 光源对x 轴的影响
    dy = np.cos(vec_el) * np.sin(vec_az)  # 光源对y 轴的影响
    dz = np.sin(vec_el)  # 光源对z 轴的影响

    b = 255 * (dx * uni_x + dy * uni_y + dz * uni_z)  # 光源归一化
    b = b.clip(0, 255)  # 防止像素超出范围

    return b.astype(np.uint8)  # important, this is the datatype opencv write accept
    # im = Image.fromarray(b.astype('uint8'))  # 重构图像
    # im.save(save_path)


def handify_video(input_path, output_path='output.flv'):
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    video_writer = cv2.VideoWriter('output.flv', cv2.VideoWriter_fourcc(*'FLV1'), fps, (width, height), False)

    while (cap.isOpened()):
        ret, frame = cap.read()
        handified_frame = handify(frame)
        video_writer.write(handified_frame)
        # cv2.imshow('frame', handified_frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    cv2.destroyAllWindows()
    cap.release()
    # video_writer.release()

if __name__ == '__main__':
    handify_video("zhongli-pv.flv")

