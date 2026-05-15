import numpy as np
import matplotlib.pyplot as plt
import librosa
import os

files = [
"/Users/nayanmborah/Music/SuperCollider Recordings/feedback_6.wav",
"/Users/nayanmborah/Music/SuperCollider Recordings/feedback_7.wav",
"/Users/nayanmborah/Music/SuperCollider Recordings/feedback_8.wav",
"/Users/nayanmborah/Music/SuperCollider Recordings/feedback_9.wav"
]

plt.figure(figsize=(10,5))

for f in files:
    y, sr = librosa.load(f, sr=None, mono=True)

    # ALIGNMENT STEP
    peak_index = np.argmax(np.abs(y))
    y = y[peak_index:]   # trim before impulse

    # Energy decay
    energy = y**2
    edc = np.cumsum(energy[::-1])[::-1]
    edc = edc + 1e-10

    edc_db = 10 * np.log10(edc / np.max(edc))

    t = np.linspace(0, len(y)/sr, len(y))

    plt.plot(t, edc_db, label=os.path.basename(f))

plt.legend()
plt.title("Energy Decay Comparison")
plt.xlabel("Time (seconds)")
plt.ylabel("dB")
plt.ylim([-120, 0])
plt.grid()

plt.show()