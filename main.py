import mpu6050
import time
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pandas as pd

# Create a new Mpu6050 object
mpu6050 = mpu6050.mpu6050(0x68)

# Define a function to read the sensor data
def read_sensor_data():
    # Read the accelerometer values
    accelerometer_data = mpu6050.get_accel_data()

    # Read the gyroscope values
    gyroscope_data = mpu6050.get_gyro_data()

    # Read temp
    temperature = mpu6050.get_temp()

    return accelerometer_data, gyroscope_data, temperature

# Start a while loop to continuously read the sensor data
temp_metric = st.empty()
prev_temperature = 0
while True:

    # Read the sensor data
    accelerometer_data, gyroscope_data, temperature = read_sensor_data()

    # Print the sensor data
    # print("Accelerometer data:", accelerometer_data)
    # print("Gyroscope data:", gyroscope_data)
    # print("Temp:", temperature)

    temp_metric.metric(label="Temperature", value=f'{temperature:.2f} °C', delta=f'{temperature-prev_temperature:.2f} °C')

    prev_temperature = temperature

    

    # Wait for 1 second
    time.sleep(1)