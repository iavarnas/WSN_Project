import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
plt.close('all')

Fs = 5000  # sampling frequency
time_step = 1/Fs  # step at sampling
frequency1 = 50  # fundamental
frequency3 = 150  # third harmonic
frequency5 = 550  # fifth harmonic

N = Fs/frequency1
freq_step = Fs/N

time_vec = np.arange(0, time_step*N, time_step)
freq_spectrum = np.arange(0, freq_step*N, freq_step)

signal = (np.sin(2*np.pi*frequency1*time_vec)
          + 0.3*np.sin(2*np.pi*frequency3*time_vec)
          + 0.5*np.sin(2*np.pi*frequency5*time_vec))

fourier_signal = np.fft.fft(signal)
fourier_signal_mag = np.abs(fourier_signal)/N

f_plot = freq_spectrum[0:int(N/2+1)]
fourier_signal_mag_plot = 2*fourier_signal_mag[0:int(N/2+1)]
fourier_signal_mag_plot[0] = fourier_signal_mag_plot[0]/2

fig, [ax1, ax2] = plt.subplots(2, 1)
ax1.plot(time_vec, signal)
ax2.plot(f_plot, fourier_signal_mag_plot)
plt.show()
