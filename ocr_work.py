import tesserocr
from PIL import Image,ImageDraw


class VerifyCodeOCR():
    def __init__(self):
        self.img = Image.open("ocr-test/freeze.jpg")

    def binary(self, img):
        imgry = img.convert("L")
        threshold = 140
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        out = imgry.point(table, '1')
        return out


    # 判断噪点,如果确认是噪点,用该点的上面一个点的灰度进行替换
    # 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值 N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
    # x, y: 像素点坐标
    # G: 图像二值化阀值
    # N: 降噪率 0 < N <8
    def get_pixel(self,image, x, y, G, N):
        # 获取像素值
        L = image.getpixel((x, y))

        # 与阈值比较
        if L > G:
            L = True
        else:
            L = False

        nearDots = 0

        if L == (image.getpixel((x - 1, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x - 1, y)) > G):
            nearDots += 1
        if L == (image.getpixel((x - 1, y + 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x, y + 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y + 1)) > G):
            nearDots += 1

        if nearDots < N:
            return image.getpixel((x, y - 1))
        else:
            return None


    # 降噪
    # Z: 降噪次数
    def clear_noise(self,image, G, N, Z):
        draw = ImageDraw.Draw(image)

        for i in range(0, Z):
            for x in range(1, image.size[0] - 1):
                for y in range(1, image.size[1] - 1):
                    color = self.get_pixel(image, x, y, G, N)
                    if color is not None:
                        draw.point((x, y), color)


    def run(self):
        out = self.binary(self.img)
        self.clear_noise(out,0,2,2)
        out.show()
        width = int(out.size[0])*20
        height = int(out.size[1])*20
        out = out.resize((width,height),Image.ANTIALIAS)
        out.show()
        # print(tesserocr.image_to_text(out))

vc = VerifyCodeOCR()
vc.run()
