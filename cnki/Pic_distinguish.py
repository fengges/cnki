from PIL import Image
from libsvm.python.svmutil import *
from libsvm.python.svm import *
def get_bin_table(threshold=80):
    """
    获取灰度转二值的映射table
    :param threshold:
    :return:
    """
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    return table

def sum_9_region(img, x, y):
    """
    9邻域框,以当前点为中心的田字框,黑点个数,作为移除一些孤立的点的判断依据
    :param img: Image
    :param x:
    :param y:
    :return:
    """
    cur_pixel = img.getpixel((x, y))  # 当前像素点的值
    width = img.width
    height = img.height

    if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
        return 0

    if y == 0:  # 第一行
        if x == 0:  # 左上顶点,4邻域
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 4 - sum
        elif x == width - 1:  # 右上顶点
            sum = cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 4 - sum
        else:  # 最上非顶点,6邻域
            sum = img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 6 - sum
    elif y == height - 1:  # 最下面一行
        if x == 0:  # 左下顶点
            # 中心点旁边3个点
            sum = cur_pixel \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x, y - 1))
            return 4 - sum
        elif x == width - 1:  # 右下顶点
            sum = cur_pixel \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y - 1))

            return 4 - sum
        else:  # 最下非顶点,6邻域
            sum = cur_pixel \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x, y - 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x + 1, y - 1))
            return 6 - sum
    else:  # y不在边界
        if x == 0:  # 左边非顶点
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))

            return 6 - sum
        elif x == width - 1:  # 右边非顶点
            # print('%s,%s' % (x, y))
            sum = img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1))

            return 6 - sum
        else:  # 具备9领域条件的
            sum = img.getpixel((x - 1, y - 1)) \
                  + img.getpixel((x - 1, y)) \
                  + img.getpixel((x - 1, y + 1)) \
                  + img.getpixel((x, y - 1)) \
                  + cur_pixel \
                  + img.getpixel((x, y + 1)) \
                  + img.getpixel((x + 1, y - 1)) \
                  + img.getpixel((x + 1, y)) \
                  + img.getpixel((x + 1, y + 1))
            return 9 - sum

def remove_noise_pixel(img, noise_point_list):
    """
    根据噪点的位置信息，消除二值图片的黑点噪声
    :type img:Image
    :param img:
    :param noise_point_list:
    :return:
    """
    for item in noise_point_list:
        img.putpixel((item[0], item[1]), 1)

def get_clear_bin_image(image):
    """
    获取干净的二值化的图片。
    图像的预处理：
    1. 先转化为灰度
    2. 再二值化
    3. 然后清除噪点
    参考:http://python.jobbole.com/84625/
    :type img:Image
    :return:
    """
    imgry = image.convert('L')  # 转化为灰度图

    table = get_bin_table()
    out = imgry.point(table, '1')  # 变成二值图片:0表示黑色,1表示白色

    noise_point_list = []  # 通过算法找出噪声点,第一步比较严格,可能会有些误删除的噪点
    for x in range(out.width):
        for y in range(out.height):
            res_9 = sum_9_region(out, x, y)
            if (0 < res_9 < 3) and out.getpixel((x, y)) == 0:  # 找到孤立点
                pos = (x, y)  #
                noise_point_list.append(pos)
    remove_noise_pixel(out, noise_point_list)
    return out

def get_crop_imgs(image):
    width, height = image.size
    startLine = 0
    endLine = width - 1

    # 确定竖直起始位置（如果噪点在边缘未消去可能会影响结果）
    black_num = 0
    for i in range(0, width):
        if (black_num != 0):
            break
        for j in range(0, height):
            if (image.getpixel((i, j)) == 0):
                startLine = i
                black_num += 1
    # print("startLine:",startLine)
    black_num = 0
    for i in range(width - 1, -1, -1):
        if (black_num != 0):
            break
        for j in range(0, height):
            if (image.getpixel((i, j)) == 0):
                endLine = i + 1
                black_num += 1
    # print("endLine",endLine)

    # len:区间的长度,offset:偏移量（这里取整丧失了精度，在后面做处理减少误差
    len = int((endLine - startLine) / 5)
    offset = 7
    # print ("len:",int(len))


    # 字符的切割位置,五个数对应四个split_x
    split_x = [1, 1, 1, 1]

    # 求第一个切割线
    min_num = 5  # 默认分界线像素不超过五
    for x in range(startLine + len - 1, startLine + len - 1 + offset):
        black_num = 0
        for y in range(5, 9):
            if (image.getpixel((x, y)) == 0):
                black_num += 1
        x -= 1
        for y in range(9, 13):
            if (image.getpixel((x, y)) == 0):
                black_num += 1
        x -= 1
        for y in range(13, 19):
            if (image.getpixel((x, y)) == 0):
                black_num += 1
        x += 2
        if (black_num < min_num):
            min_num = black_num
            split_x[0] = x
    # print ("diyige:",split_x[0])

    # 求第二个切割线
    min_num = 5  # 默认分界线像素不超过五
    for x in range(startLine + 2 * len - 3, startLine + 2 * len + offset):
        black_num = 0
        for y in range(5, 9):
            if (image.getpixel((x, y)) == 0):
                black_num += 1
        x -= 1
        for y in range(9, 13):
            if (image.getpixel((x, y)) == 0):
                black_num += 1
        x -= 1
        for y in range(13, 19):
            if (image.getpixel((x, y)) == 0):
                black_num += 1
        x += 2
        if (black_num < min_num):
            min_num = black_num
            # print (min_num)
            split_x[1] = x
    # print ("diyige:",split_x[1])

    # 求第四个切割线
    min_num = 5  # 默认分界线像素不超过五
    for x in range(endLine - len - 2 + offset, endLine - len - 2, -1):
        black_num = 0
        for y in range(5, 9):
            if (image.getpixel((x, y)) == 0):
                black_num += 1
        x -= 1
        for y in range(9, 13):
            if (image.getpixel((x, y)) == 0):
                black_num += 1
        x -= 1
        for y in range(13, 19):
            if (image.getpixel((x, y)) == 0):
                black_num += 1
        x += 2
        if (black_num < min_num):
            min_num = black_num
            split_x[3] = x - 1
    # print("diyige:", split_x[3])

    # 求第三个切割线
    min_num = 5  # 默认分界线像素不超过五
    for x in range(endLine - 2 * len - 3 + offset, endLine - 2 * len - 5, -1):
        black_num = 0
        for y in range(5, 9):
            if (image.getpixel((x, y)) == 0):
                black_num += 1
        x -= 1
        for y in range(9, 13):
            if (image.getpixel((x, y)) == 0):
                black_num += 1
        x -= 1
        for y in range(13, 19):
            if (image.getpixel((x, y)) == 0):
                black_num += 1
        x += 2
        if (black_num < min_num):
            min_num = black_num
            split_x[2] = x - 1
    # print("diyige:", split_x[2])

    child_img_list = []
    child_img_list.append(image.crop([startLine, 5, split_x[0], 17]))
    child_img_list.append(image.crop([split_x[0], 5, split_x[1], 17]))
    child_img_list.append(image.crop([split_x[1], 5, split_x[2], 17]))
    child_img_list.append(image.crop([split_x[2], 5, split_x[3], 17]))
    child_img_list.append(image.crop([split_x[3], 5, endLine, 17]))
    return child_img_list

def resize_imgs(image_list):
    newImg_list = []
    for im in image_list:
        newImg = Image.new("1", (13, 12), 1)
        newImg.paste(im)
        newImg_list.append(newImg)
    return newImg_list

def get_feature(img):
    """
    获取指定图片的特征值,
    1. 按照每排的像素点,高度为10,则有10个维度,然后为6列,总共16个维度
    :param img_path:
    :return:一个维度为10（高度）的列表
    """
    width, height = img.size

    pixel_cnt_list = []
    for y in range(height):
        pix_cnt_x = 0
        for x in range(width):
            if img.getpixel((x, y)) == 0:  # 黑色点
                pix_cnt_x += 1

        pixel_cnt_list.append(pix_cnt_x)

    for x in range(width):
        pix_cnt_y = 0
        for y in range(height):
            if img.getpixel((x, y)) == 0:  # 黑色点
                pix_cnt_y += 1

        pixel_cnt_list.append(pix_cnt_y)

    return pixel_cnt_list

def convert_feature_to_vector(feature_list):
    """

    :param feature_list:
    :return:
    """
    index = 1
    xt_vector = []
    feature_dict = {}
    for item in feature_list:
        feature_dict[index] = item
        index += 1
    xt_vector.append(feature_dict)
    return xt_vector

def pic2str(image):
    pic_str = ""

    #图片初步处理，转换为二值图
    bin_clear_img = get_clear_bin_image(image)
    # 切割图片为单个字符，保存在内存中（5个child）
    child_img_list = get_crop_imgs(bin_clear_img)
    #标准化子图的大小
    child_img_list = resize_imgs(child_img_list)


    # 加载SVM模型进行预测
    model = svm_load_model('cnki//data//model_file')

    for child_img in child_img_list:
        img_feature_list = get_feature(child_img)  # 使用特征算法，将图像进行特征化降维

        yt = [0]  # 测试数据标签
        # xt = [{1: 1, 2: 1}]  # 测试数据输入向量
        xt = convert_feature_to_vector(img_feature_list)  # 将所有的特征转化为标准化的SVM单行的特征向量
        p_label, p_acc, p_val = svm_predict(yt, xt, model)
        pic_str += (chr(int(p_label[0])))  # 将识别结果合并起来

    return pic_str

# if __name__ == '__main__':
#     for i in range(1,11):
#         im = Image.open("image//"+str(i)+".gif")
#         pic_str = pic2str(im)
#         im.save("image//"+pic_str+".gif")
#         print(pic_str)
def readCode():
    im = Image.open("cnki/image/test.gif")
    pic_str = pic2str(im)
    return pic_str