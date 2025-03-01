import mpu6050
import time
import numpy as np
import pandas as pd


# Define a function to read the sensor data
def read_sensor_data():
    # Read the accelerometer values
    accelerometer_data = mpu6050.get_accel_data()

    # Read the gyroscope values
    gyroscope_data = mpu6050.get_gyro_data()

    # Read temp
    temperature = mpu6050.get_temp()

    return accelerometer_data, gyroscope_data, temperature


# Create a new Mpu6050 object
mpu6050 = mpu6050.mpu6050(0x68)


while True:

    # Read the sensor data
    accelerometer_data, gyroscope_data, temperature = read_sensor_data()

    print(temperature)


    # Prepares for the next loop
    time.sleep(0.5)