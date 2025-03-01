import mpu6050
import time
import matplotlib.pyplot as plt
import streamlit as st
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

def calibrate_gyro():


    measurement_interval = 0.01
    calibration_time = 3
    num_samples = calibration_time/measurement_interval
    
    gyrox_accumul = 0
    gyroy_accumul = 0
    gyroz_accumul = 0
    for isample in  range(int(num_samples)):
        accelerometer_data, gyroscope_data, temperature = read_sensor_data()
        gyrox_accumul += gyroscope_data['x']
        gyroy_accumul += gyroscope_data['y']
        gyroz_accumul += gyroscope_data['z']
        time.sleep(measurement_interval)
    
    gyrox_bias = gyrox_accumul/num_samples
    gyroy_bias = gyroy_accumul/num_samples
    gyroz_bias = gyroz_accumul/num_samples

    return gyrox_bias, gyroy_bias, gyroz_bias



if 'button' not in st.session_state:
    st.session_state.button = False

def click_button():
    st.session_state.button = not st.session_state.button


# Create a new Mpu6050 object
mpu6050 = mpu6050.mpu6050(0x68)

# Global variables
gyrox_bias = 0
gyroy_bias = 0
gyroz_bias = 0



# Prepares the placeholders for the layout
col01,_,_ = st.columns(3)
col1, col2, col3, col4 = st.columns(4)
with col01:
    temp_metric = st.empty()
with col1:
    gyrox_metric = st.empty()
    accelx_metric = st.empty()
with col2:
    gyroy_metric = st.empty()
    accely_metric = st.empty()
with col3:
    gyroz_metric = st.empty()
    accelz_metric = st.empty()
with col4:
    calibrate_gyro_button = st.button("CALIBRATE", icon=None, on_click=click_button)


prev_temperature = 0
prev_gyrox = 0
prev_gyroy = 0
prev_gyroz = 0
prev_accelx = 0
prev_accely = 0
prev_accelz = 0



while True:

    # Read the sensor data
    accelerometer_data, gyroscope_data, temperature = read_sensor_data()



    # Prepares the data
    gyro_x = gyroscope_data['x']
    gyro_y = gyroscope_data['y']
    gyro_z = gyroscope_data['z']

    accel_x = accelerometer_data['x']
    accel_y = accelerometer_data['y']
    accel_z = accelerometer_data['z']

    delta_gyrox = gyro_x - prev_gyrox
    delta_gyroy = gyro_y - prev_gyroy
    delta_gyroz = gyro_z - prev_gyroz

    if st.session_state.button:
        #if np.abs(delta_gyrox) + np.abs(delta_gyroy) + np.abs(delta_gyroz) < 0.1: 
        gyrox_bias, gyroy_bias, gyroz_bias = calibrate_gyro()
        st.session_state.button = False
        print('Calibrated!')



    # Updates the graphical elements
    temp_metric.metric(label="Temperature", value=f'{temperature:.2f} °C', delta=f'{temperature-prev_temperature:.2f} °C')

    gyrox_metric.metric(label="Gyro X (°/s):", value=f'{gyro_x-gyrox_bias:.2f}', delta=f'{delta_gyrox:.2f}')
    gyroy_metric.metric(label="Gyro Y (°/s):", value=f'{gyro_y-gyroy_bias:.2f}', delta=f'{delta_gyroy:.2f}')
    gyroz_metric.metric(label="Gyro Z (°/s):", value=f'{gyro_z-gyroz_bias:.2f}', delta=f'{delta_gyroz:.2f}')

    accelx_metric.metric(label="Accelerometer X (m/s):", value=f'{accel_x:.2f}')
    accely_metric.metric(label="Accelerometer Y (m/s):", value=f'{accel_y:.2f}')
    accelz_metric.metric(label="Accelerometer Z (m/s):", value=f'{accel_z:.2f}')

    # Prepares for the next loop
    prev_temperature = temperature
    prev_gyrox = gyro_x
    prev_gyroy = gyro_y
    prev_gyroz = gyro_z

    time.sleep(0.5)

