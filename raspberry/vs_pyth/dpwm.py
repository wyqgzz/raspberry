from threading import Thread  # 导入线程模块
import RPi.GPIO as GPIO  # 导入树莓派GPIO模块
import time  # 导入时间模块

# 设置编码方式
GPIO.setmode(GPIO.BOARD)

# 设置引脚
OUT1 = 11  # 第一个LED的引脚号
OUT2 = 16  # 第二个LED的引脚号
GPIO.setup(OUT1, GPIO.OUT)  # 设置引脚11为输出模式
GPIO.setup(OUT2, GPIO.OUT)  # 设置引脚16为输出模式

# 实例化PWM，设置频率为60Hz
pwm1 = GPIO.PWM(OUT1, 60)  # 初始化第一个LED的PWM对象，频率为60Hz
pwm2 = GPIO.PWM(OUT2, 60)  # 初始化第二个LED的PWM对象，频率为60Hz

# 开启PWM
pwm1.start(0)  # 启动第一个LED的PWM，初始占空比为0
pwm2.start(0)  # 启动第二个LED的PWM，初始占空比为0

# 控制LED呼吸的函数
def breathe(pwm):
    # 控制LED呼吸的循环，重复3次
    for _ in range(3):
        # 增加占空比，让LED亮度逐渐增加
        for dc in range(0, 101, 5):  # 循环从0增加到100，步长为5
            pwm.ChangeDutyCycle(dc)  # 设置占空比
            time.sleep(0.1)  # 等待0.1秒

        # 减小占空比，让LED亮度逐渐减小
        for dc in range(100, -1, -5):  # 循环从100减小到0，步长为5
            pwm.ChangeDutyCycle(dc)  # 设置占空比
            time.sleep(0.1)  # 等待0.1秒

# 主函数
def main():
    # 实例化线程，分别控制两个LED的呼吸效果
    pwm1_thread = Thread(target=breathe, args=(pwm1, ))  # 初始化第一个LED的呼吸效果线程
    pwm2_thread = Thread(target=breathe, args=(pwm2, ))  # 初始化第二个LED的呼吸效果线程

    # 开启线程
    pwm1_thread.start()  # 启动第一个LED的呼吸效果线程
    pwm2_thread.start()  # 启动第二个LED的呼吸效果线程

    # 阻塞主线程，直到两个LED的呼吸效果完成
    pwm1_thread.join()  # 等待第一个LED的呼吸效果线程结束
    pwm2_thread.join()  # 等待第二个LED的呼吸效果线程结束

    # 释放GPIO引脚资源
    GPIO.cleanup()  # 清理GPIO资源

# 程序入口
if __name__ == '__main__':
    main()  # 调用主函数