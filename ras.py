import smbus
import time
import RPi.GPIO as GPIO

# Define GPIO pins for ESCs (replace with your pins)
ESC1_PIN = 17
ESC2_PIN = 18
ESC3_PIN = 27
ESC4_PIN = 22

# Define GPIO pins for FS-CT6B receiver channels
THROTTLE_PIN = 23
PITCH_PIN = 24
ROLL_PIN = 25
YAW_PIN = 8

# MPU-6050 Registers
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# Initialize I2C (bus number depends on your Raspberry Pi model)
bus = smbus.SMBus(1)
device_address = 0x68  # MPU-6050 I2C address

# PID constants (to be tuned for your setup)
KP = 1.0
KI = 0.05
KD = 0.1

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ESC1_PIN, GPIO.OUT)
GPIO.setup(ESC2_PIN, GPIO.OUT)
GPIO.setup(ESC3_PIN, GPIO.OUT)
GPIO.setup(ESC4_PIN, GPIO.OUT)

# Setup GPIO for receiver channels
GPIO.setup(THROTTLE_PIN, GPIO.IN)
GPIO.setup(PITCH_PIN, GPIO.IN)
GPIO.setup(ROLL_PIN, GPIO.IN)
GPIO.setup(YAW_PIN, GPIO.IN)

# Create PWM objects for the ESCs
esc1 = GPIO.PWM(ESC1_PIN, 50)
esc2 = GPIO.PWM(ESC2_PIN, 50)
esc3 = GPIO.PWM(ESC3_PIN, 50)
esc4 = GPIO.PWM(ESC4_PIN, 50)

# Initialize PWM to 0 (motors off)
esc1.start(0)
esc2.start(0)
esc3.start(0)
esc4.start(0)


def MPU_Init():
    # Write to power management register to wake up the MPU-6050
    bus.write_byte_data(device_address, PWR_MGMT_1, 0)


def read_raw_data(addr):
    # Read raw 16-bit data from the MPU-6050
    high = bus.read_byte_data(device_address, addr)
    low = bus.read_byte_data(device_address, addr + 1)
    value = (high << 8) | low
    if value > 32768:
        value -= 65536
    return value


def calculate_pid(setpoint, measured_value, prev_error, integral):
    error = setpoint - measured_value
    integral += error
    derivative = error - prev_error
    output = KP * error + KI * integral + KD * derivative
    return output, error, integral


def control_motors(throttle, pid_pitch, pid_roll, pid_yaw):
    # Adjust motor speed based on PID output and RC input
    esc1_speed = throttle + pid_pitch - pid_roll - pid_yaw
    esc2_speed = throttle + pid_pitch + pid_roll + pid_yaw
    esc3_speed = throttle - pid_pitch + pid_roll - pid_yaw
    esc4_speed = throttle - pid_pitch - pid_roll + pid_yaw

    # Convert speed to duty cycle (assume 1000 to 2000 microseconds for ESCs)
    esc1.ChangeDutyCycle(convert_to_duty_cycle(esc1_speed))
    esc2.ChangeDutyCycle(convert_to_duty_cycle(esc2_speed))
    esc3.ChangeDutyCycle(convert_to_duty_cycle(esc3_speed))
    esc4.ChangeDutyCycle(convert_to_duty_cycle(esc4_speed))


def convert_to_duty_cycle(value):
    # Convert throttle value to duty cycle (0 to 100)
    return max(0, min(100, (value - 1000) / 10))


def read_pwm(channel_pin):
    # Measure the high pulse width of the PWM signal
    GPIO.wait_for_edge(channel_pin, GPIO.RISING)
    start_time = time.time()
    GPIO.wait_for_edge(channel_pin, GPIO.FALLING)
    end_time = time.time()
    return (end_time - start_time) * 1000000  # Convert to microseconds


MPU_Init()

# Initialize variables for PID
prev_pitch_error = 0
prev_roll_error = 0
pitch_integral = 0
roll_integral = 0

# Main loop
while True:
    # Read receiver PWM inputs
    throttle = read_pwm(THROTTLE_PIN)
    pitch_input = read_pwm(PITCH_PIN)
    roll_input = read_pwm(ROLL_PIN)
    yaw_input = read_pwm(YAW_PIN)

    # Read accelerometer data
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_XOUT_H + 2)

    # Basic angle estimation (simplified)
    pitch_angle = acc_x / 16384.0 * 90  # Convert to degrees (simplified)
    roll_angle = acc_y / 16384.0 * 90

    # Desired angles (set by remote control inputs)
    desired_pitch = (pitch_input - 1500) / 500 * 45  # Map PWM to degrees
    desired_roll = (roll_input - 1500) / 500 * 45
    desired_yaw = (yaw_input - 1500) / 500 * 45

    # Calculate PID outputs
    pid_pitch, prev_pitch_error, pitch_integral = calculate_pid(desired_pitch, pitch_angle, prev_pitch_error,
                                                                pitch_integral)
    pid_roll, prev_roll_error, roll_integral = calculate_pid(desired_roll, roll_angle, prev_roll_error, roll_integral)

    # Control motors with RC input and PID output
    control_motors(throttle, pid_pitch, pid_roll, desired_yaw)

    time.sleep(0.01)