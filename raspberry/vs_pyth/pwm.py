import RPi.GPIO as GPIO
import time

# 设置 GPIO 编号模式为 BCM
GPIO.setmode(GPIO.BCM)

# 设置 GPIO 引脚
led_pin = 18
GPIO.setup(led_pin, GPIO.OUT)

# 创建 PWM 实例，设置频率为 100 Hz
pwm = GPIO.PWM(led_pin, 100)

try:
    while True:
        # 从 0 慢慢增加到 100（亮度递增）
        for duty_cycle in range(0, 101, 1):
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.01)

        # 从 100 慢慢减少到 0（亮度递减）
        for duty_cycle in range(100, -1, -1):
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.01)

except KeyboardInterrupt:
    pass

# 停止 PWM
pwm.stop()

# 清理 GPIO
GPIO.cleanup()