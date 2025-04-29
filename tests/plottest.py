import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav

# Load the data
data = np.loadtxt("audio.csv", delimiter=",")

# data = np.clip(data, -1.0, 1.0)  # Ensure values are in [-1.0, 1.0]
data_int16 = np.int16(data * 32767)  # Convert to 16-bit PCM format

# Define sample rate (modify if different)
sample_rate = 48000

# Save to WAV
wav.write("output.wav", sample_rate, data_int16)

# Plot it
plt.plot(data)
plt.title("Audio Amplitude Over Time")
plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.grid(True)
plt.show()
