import smbus
import time

# 设置OLED的I2C地址，根据实际情况进行更改
OLED_ADDR = 0x3C

# 定义命令和数据传输的常量
COMMAND_MODE = 0x00
DATA_MODE = 0x40

# 初始化I2C总线
bus = smbus.SMBus(1)
time.sleep(0.1)

def send_command(command):
    # 发送命令到OLED
    bus.write_byte_data(OLED_ADDR, COMMAND_MODE, command)

def send_data(data):
    # 发送数据到OLED
    bus.write_byte_data(OLED_ADDR, DATA_MODE, data)

def initialize_oled():
    # 初始化OLED
    send_command(0xAE)  # 关闭OLED显示
    send_command(0xD5)  # 设置时钟分频因子
    send_command(0x80)  # 默认分频因子为0x80
    send_command(0xA8)  # 设置驱动路数
    send_command(0x3F)  # 设置为0x3F，即1/64duty
    send_command(0xD3)  # 设置显示偏移
    send_command(0x00)  # 默认偏移为0x00
    send_command(0x40)  # 设置起始行
    send_command(0x8D)  # 电荷泵设置
    send_command(0x14)  # 使能电荷泵
    send_command(0x20)  # 设置内存地址模式
    send_command(0x00)  # 设置为水平寻址模式
    send_command(0xA1)  # 设置段重定义
    send_command(0xC8)  # 设置COM扫描方向
    send_command(0xDA)  # 设置COM引脚硬件配置
    send_command(0x12)  # 设置为0x12，即Alternative COM pin configuration
    send_command(0x81)  # 对比度设置
    send_command(0xCF)  # 默认对比度为0xCF
    send_command(0xD9)  # 预充电周期设置
    send_command(0xF1)  # 默认为0xF1
    send_command(0xDB)  # VCOMH电压倍率设置
    send_command(0x40)  # 设置为0x40，即0.77*VCC
    send_command(0xA4)  # 设置全局显示开启
    send_command(0xA6)  # 设置正常显示
    send_command(0xAF)  # 打开OLED显示

def display_text(text):
    # 在OLED上显示文本
    for char in text:
        send_data(ord(char))

# 主程序
try:
    initialize_oled()  # 初始化OLED显示屏

    while True:
        display_text("Hello, World!")
        time.sleep(2)
        display_text("This is an OLED display.")
        time.sleep(2)

except KeyboardInterrupt:
    pass
finally:
    # 清理GPIO资源
    bus.close()