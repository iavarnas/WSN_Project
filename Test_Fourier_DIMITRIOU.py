import numpy as np
import matplotlib.pyplot as plt
import serial.tools.list_ports
import serial

FFT_time_window = 8000.0
Current_time = 0.0

X_accel = np.array([])
Time_accel = np.array([])
RPM_values = np.array([])  # Array to store RPM values
RPM_times = np.array([])   # Array to store times corresponding to RPM values
Start_FFT_time = Current_time
# arduino_Serial_Data = serial.Serial('COM3',9600)

ports = serial.tools.list_ports.comports()  # which ports are ready
serialInst = serial.Serial()  # creation of Arduino serial destination

portList = []  # creation of empty list
#
for onePort in ports:  # scan one by one
    portList.append(str(onePort))  # write to the list
    print(str(onePort))  # print the list

val = input("select Port: COM")  # ask user value

for x in range(0, len(portList)):  # execute ports times
    if portList[x].startswith("COM" + str(val)):  # find which is the user port
        portVar = "COM" + str(val)  # connect Arduino with serial destination
        print(portList[x])  # print out

serialInst.baudrate = 9600  # baudrate setting
serialInst.port = "COM" + str(val)  # connect-define virtual port
serialInst.open()

j = 0
while (1 == 1):
    if serialInst.in_waiting:
        # packet = serialInst.readline()
        # new_data = float(packet)
        j += 1
        myData = str(serialInst.readline())
        # print(myData)
        x_start = int(myData.find("X-Coordinate:"))

        t_start = int(myData.find(",Time ="))
        end = int(myData.find("."))
        x_accel = float(myData[x_start + len("X-Coordinate:"):t_start])

        Current_time = float(myData[t_start + len(",Time ="):end])
        if (j == 1):
            Start_FFT_time = Current_time
        # I have read the new values from the serial
        # I will store the new values to my arrays for FFT

        X_accel = np.append(X_accel, [x_accel])

        Time_accel = np.append(Time_accel, [Current_time])
        # I have added the latest value of acceleration and time

        # I will check if the time is right to perform FFT
        if ((Current_time - Start_FFT_time) > FFT_time_window):
            N_FFT = Time_accel.size  # The number of samples
            Average_time_difference = (Current_time - Start_FFT_time) / float(
                Time_accel.size - 1)  # this is the constant time diff for FFT
            Fs = 1000 / Average_time_difference  # the maximum frequency
            Df = Fs / float(N_FFT)  # the frequency step in the FFT
            Time_Sequence_For_FFT = np.linspace(Start_FFT_time, Current_time,
                                                N_FFT)  # my time sequence is regularly spaced
            f = np.linspace(0, (N_FFT - 1) * Df, int(N_FFT))  # frequency steps, x axis in frequency domain

            X_accel_interp = np.interp(Time_Sequence_For_FFT, Time_accel,
                                       X_accel)  # I am creating the interpolated values at the corresponding FFT time slots

            # FFT
            X_FFT = np.fft.fft(X_accel_interp)

            X_mag = np.abs(X_FFT) / N_FFT

            # Let's plot half of the FFT spectrum, since the spectrum after the first half is "fake"
            f_plot = f[1:int(N_FFT / 2 + 1)]
            X_mag_plot = 2 * X_mag[1:int(N_FFT / 2 + 1)]

            dominant_frequency_index = np.argmax(X_mag_plot)  # Find the index of the maximum magnitude
            dominant_frequency = f_plot[dominant_frequency_index]  # Get the corresponding frequency
            rpm = 60 * dominant_frequency

            RPM_values = np.append(RPM_values, rpm)
            RPM_times = np.append(RPM_times, Current_time)

            # Check if RPM exceeds 500
            if rpm >= 500:
                print(f"Alarm! RPM is too high: {rpm}")

            print("dominant frequency =", dominant_frequency)
            print("RPM", rpm)

            # from tkinter import messagebox
            ## Inside the RPM check
            # if rpm >= 500:
            # messagebox.showwarning("Alarm", f"RPM is too high: {rpm}")

            # plots
            fig, ((ax1),(ax3) ,(ax4)) = plt.subplots(3, 1)
            ax1.plot(Time_Sequence_For_FFT, X_accel_interp, '.-')
            ax3.plot(RPM_times, RPM_values, '.-')
            ax4.plot(f_plot, X_mag_plot, '.-')
            ax1.set_xlabel("time (ms)")
            ax3.set_xlabel("Time (ms)")
            ax3.set_ylabel("RPM")
            ax4.set_xlabel("frequency (Hz)")

            ax1.grid()

            ax3.grid()

            ax4.grid()

            plt.tight_layout()
            plt.show()

            X_accel = np.delete(X_accel, 0)

            Time_accel = np.delete(Time_accel, 0)
            Start_FFT_time = Current_time
            j = 0
