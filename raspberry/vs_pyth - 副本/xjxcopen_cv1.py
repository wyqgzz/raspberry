import RPi.GPIO as gpio
import time
import cv2
import numpy as np

direction=0
a=12
c=20
b=30
d=0
e=10
f=3

# 定义引脚
pin1 = 18
pin2 = 17
pin3 = 23
pin4 = 24

# 设置GPIO口为BCM编号规范
gpio.setmode(gpio.BCM)

# 设置GPIO口为输出
gpio.setup(pin1, gpio.OUT)
gpio.setup(pin2, gpio.OUT)
gpio.setup(pin3, gpio.OUT)
gpio.setup(pin4, gpio.OUT)

# 设置PWM波,频率为500Hz
pwm1 = gpio.PWM(pin1, 500)
pwm2 = gpio.PWM(pin2, 500)
pwm3 = gpio.PWM(pin3, 500)
pwm4 = gpio.PWM(pin4, 500)

# pwm波控制初始化
pwm1.start(0)
pwm2.start(0)
pwm3.start(0)
pwm4.start(0)


# 设置曲率变化的阈值
threshold = 0.5  # 这里设置一个合适的阈值
# 设置标准中心点位置
standard_center = 320

# 打开摄像头
cap = cv2.VideoCapture(1)

# 前一帧的曲率值
prev_curvature = None

# 定义计算曲率的函数
def calculate_curvature(lines):
    curvatures = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        # 计算直线的斜率
        if x2 - x1 != 0:
            slope = (y2 - y1) / (x2 - x1)
        else:
            slope = 0  # 处理斜率为无穷大的情况

        # 计算曲率，这里只是一个示例，实际情况可能需要更复杂的计算方法
        curvature = slope  # 简单起见，直接使用斜率作为曲率的示例

        curvatures.append(curvature)

    avg_curvature = np.mean(curvatures)
    return avg_curvature

while True:
    # 读取一帧图像
    ret, frame = cap.read()
    if not ret:
        print("未能成功读取图像帧")
        break

    # 获取图像的高度和宽度
    height, width = frame.shape[:2]

    # 定义上部分图像的ROI
    roi = frame[0:int(height / 2), 0:width]

    # 转换为灰度图
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    # 大津法二值化
    _, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

    # 膨胀，白区域变大
    dst = cv2.dilate(dst, None, iterations=2)

    # 单看第200行的像素值
    color = dst[200]

    # 找到白色的像素点索引
    white_index = np.where(color == 255)[0]

    if white_index.size == 0:
        print("未检测到白色像素")
        continue

    # 找到白色像素的中心点位置
    M = cv2.moments(dst)
    if M["m00"] != 0:
        center = int(M["m10"] / M["m00"])
    else:
        center = 0
    # 计算出center与标准中心点的偏移量
    direction = center - standard_center

    # print("偏移量:", direction)
    # 在图像中标记中心点
    cv2.circle(roi, (center, int(height/4)), 5, (0, 255, 0), -1)
    # 对图像进行高斯模糊
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 应用Canny边缘检测
    edges = cv2.Canny(blurred, 50, 150)

    # 使用霍夫线条检测
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=200, maxLineGap=100)

    # 如果至少检测到一条线
    if lines is not None:
        # 绘制检测到的线条
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # 计算线条数量
        num_lines = len(lines)
        print("线条",num_lines)

    # 计算曲率变化
    if lines is not None:
        # 计算曲率
        avg_curvature = calculate_curvature(lines)

        # 检测曲率变化
        if prev_curvature is not None:
            curvature_change = abs(avg_curvature - prev_curvature)
            # 根据曲率变化触发转弯
            if curvature_change > threshold:
                # 触发转弯操作...
                if num_lines > 3:
                    if direction > 20:
                        pwm1.ChangeDutyCycle(b +e+ 10)
                        pwm2.ChangeDutyCycle(0)
                        pwm3.ChangeDutyCycle(0)
                        pwm4.ChangeDutyCycle(0)
                        time.sleep(f)
                    elif direction < -30:
                        pwm1.ChangeDutyCycle(0)
                        pwm2.ChangeDutyCycle(0)
                        pwm3.ChangeDutyCycle(b + 10)
                        pwm4.ChangeDutyCycle(0)
                        time.sleep(f)
                print("曲率",curvature_change)

        # 更新前一帧的曲率值
        prev_curvature = avg_curvature


    # 显示图像
    # cv2.imshow('frame', frame)
    # 停止
    if abs(direction) > 70:
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)
        pwm3.ChangeDutyCycle(0)
        pwm4.ChangeDutyCycle(0)
    #前进
    elif direction <= -3 and direction >= 3:
        pwm1.ChangeDutyCycle(a+e)
        pwm2.ChangeDutyCycle(0)
        pwm3.ChangeDutyCycle(a)
        pwm4.ChangeDutyCycle(0)
        time.sleep(100000)
    # 右转
    elif direction > 0:
        if direction > 60:
            direction = 60
        pwm1.ChangeDutyCycle(a+c+e+direction)
        pwm2.ChangeDutyCycle(0)
        pwm3.ChangeDutyCycle(a)
        pwm4.ChangeDutyCycle(0)
    # 左转
    elif direction <= 0:
        # 限制在70以内
        if direction > -60:
            direction = -60

        pwm1.ChangeDutyCycle(a+e)
        pwm2.ChangeDutyCycle(0)
        pwm3.ChangeDutyCycle(a+c-direction)
        pwm4.ChangeDutyCycle(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()
pwm1.stop()
pwm2.stop()
pwm3.stop()
pwm4.stop()
gpio.cleanup()
