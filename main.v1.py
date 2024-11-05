from PIL import Image
from utils import *
import numpy as np

def main():
    imgfile = 'RubixMosaic/test.jpg'
    img = Image.open(imgfile)
    w, h = img.size
    m = min(w, h)
    x, y = (w-m)//2, (h-m)//2
    crop_img = img.crop((x, y, x+m, y+m))
    N = 10
    # crop_img = img[x:x+m, y:y+m]
    crop_img = crop_img.resize((200, 200))
    mosaic_matrix = mosaic(crop_img, N)
    
    for i in range(N):
        for j in range(N):
            print('{:4}'.format(str(mosaic_matrix[i][j])))
        print()

    blank_canvas = Image.new('RGB', (w, h), (0, 0, 0))

    color_list = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 127, 0),
        (255, 255, 0),
        (255, 255, 255)
    ]

    colors_image_list = [Image.new('RGB', (int(m / N), int(m / N)), c) for c in color_list]

    for i in range(N):
        for j in range(N):
            color_index = get_closest_color(mosaic_matrix[i][j], color_list)
            blank_canvas.paste(colors_image_list[color_index], (int(x + i * m / N), int(y + j * m / N)))


    blank_canvas.show()
    # crop_img = cv2.resize(crop_img, (500, 500))
    # # cv2.imshow("cropped", crop_img)
    # # cv2.waitKey(0)
    # mosaic_ = mosaic(crop_img, 6)
    # print('shape:', mosaic_.shape)
    # print('im shape:', crop_img.shape)
    # # mosaic_img = cv2.cvtColor(mosaic_, cv2.COLOR_BGR2RGB)
    # mosaic_img = cv2.resize(mosaic_img, (500, 500))
    # cv2.imshow("mosaic", mosaic_img)
    # cv2.waitKey(0)

if __name__ == '__main__':
    main()
    # a = (1, 2, 3)
    # print(a+a)
