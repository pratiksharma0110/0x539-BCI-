import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial
import time

SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200
BUFFER_SIZE = 1024

# open the serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)  # Allow time for Arduino reset

# initialize buffers for live data
data_buffer = np.zeros(BUFFER_SIZE)
time_buffer = np.arange(0, BUFFER_SIZE) / BUFFER_SIZE

# FFT parameters
sampling_rate = 1000

# figure and axes for the two plots
fig, (ax_wave, ax_fft) = plt.subplots(2, 1)
fig.suptitle("Real-time Waveform and Frequency Spectrum")

# waveform plot
(line_wave,) = ax_wave.plot(time_buffer, data_buffer, color="blue")
ax_wave.set_title("Input Waveform")
ax_wave.set_xlabel("Time (s)")
ax_wave.set_ylabel("Amplitude")
ax_wave.grid(True)

# FFT plot
(line_fft,) = ax_fft.plot([], [], color="red")
ax_fft.set_title("Frequency Spectrum")
ax_fft.set_xlabel("Frequency (Hz)")
ax_fft.set_ylabel("Amplitude")
ax_fft.grid(True)


def init():
    """Initialize plots."""
    line_wave.set_ydata([0] * BUFFER_SIZE)
    ax_fft.set_xlim(0, sampling_rate / 2)
    ax_fft.set_ylim(0, 1)
    return line_wave, line_fft


def update(frame):
    """Update function for animation."""
    global data_buffer

    while ser.in_waiting:
        try:
            # Read and parse the incoming data
            value = float(ser.readline().strip())
            data_buffer = np.roll(data_buffer, -1)
            data_buffer[-1] = value
        except ValueError:

            continue

    # update waveform plot
    line_wave.set_ydata(data_buffer)

    # perform FFT
    fft_data = np.fft.fft(data_buffer)
    fft_magnitude = np.abs(fft_data[: BUFFER_SIZE // 2])  # One-sided spectrum
    freqs = np.fft.fftfreq(BUFFER_SIZE, d=1 / sampling_rate)[: BUFFER_SIZE // 2]

    # normalize FFT magnitude for visualization
    fft_magnitude = fft_magnitude / np.max(fft_magnitude)

    # update FFT plot
    line_fft.set_data(freqs, fft_magnitude)
    ax_fft.set_ylim(0, 1.1)  # Adjust as needed

    target_freq = 20
    target_index = np.argmin(np.abs(freqs - target_freq))
    if fft_magnitude[target_index] >= 0.4:
        ser.write(b"HIGH\n")
    else:
        ser.write(b"LOW\n")
    return line_wave, line_fft


ani = FuncAnimation(fig, update, init_func=init, interval=10, blit=True)


plt.tight_layout()
plt.show()


ser.close()
