import numpy as np
import matplotlib.pyplot as plt
import librosa
import os

files = [
"/Users/nayanmborah/Music/SuperCollider Recordings/delay_uniform.wav",
"/Users/nayanmborah/Music/SuperCollider Recordings/delay_irregular.wav",
"/Users/nayanmborah/Music/SuperCollider Recordings/delay_optimized.wav"
]

plt.figure(figsize=(10,5))

results = {}

for f in files:
    y, sr = librosa.load(f, sr=None, mono=True)

    # 🔹 ALIGN impulse
    peak_index = np.argmax(np.abs(y))
    y = y[peak_index:]

    # 🔹 Normalize length (fair comparison)
    max_len = int(sr * 5)
    y = y[:max_len]

    # 🔹 Energy decay (EDC)
    energy = y**2
    edc = np.cumsum(energy[::-1])[::-1]
    edc = edc + 1e-10
    edc_db = 10 * np.log10(edc / np.max(edc))

    t = np.linspace(0, len(y)/sr, len(y))

    plt.plot(t, edc_db, label=os.path.basename(f))

    # 🔹 Smoothness (global)
    slope = np.diff(edc_db)
    smoothness = np.var(slope)

    # Local fluctuation (more sensitive)
    frame_size = 512
    hop = 256
    energies = []

    for i in range(0, len(y)-frame_size, hop):
        frame = y[i:i+frame_size]
        energies.append(np.sum(frame**2))

    energies = np.array(energies)
    fluctuation = np.var(np.diff(energies))

    # 🔵 NEW: Raw early variance
    raw_var = np.var(y[:10000])

    results[os.path.basename(f)] = {
        "smoothness": smoothness,
        "fluctuation": fluctuation,
        "raw_variance": raw_var
    }

plt.legend()
plt.title("Effect of Delay Distribution on Decay")
plt.xlabel("Time (seconds)")
plt.ylabel("dB")
plt.ylim([-120, 0])
plt.grid()
plt.show()

#ZOOMED EDC (important)
plt.figure(figsize=(10,5))

zoom_time = 0.5  # seconds

for f in files:
    y, sr = librosa.load(f, sr=None, mono=True)

    # align impulse
    peak_index = np.argmax(np.abs(y))
    y = y[peak_index:]

    # energy decay
    energy = y**2
    edc = np.cumsum(energy[::-1])[::-1] + 1e-10
    edc_db = 10 * np.log10(edc / np.max(edc))

    # time axis
    t = np.linspace(0, len(y)/sr, len(y))

    # safe slicing
    n = min(len(t), int(zoom_time * sr))

    plt.plot(t[:n], edc_db[:n], label=os.path.basename(f))

plt.legend()
plt.title("Zoomed EDC Comparison (First 0.5s)")
plt.xlabel("Time (seconds)")
plt.ylabel("dB")
plt.grid()

plt.show()

#Print results
print("\nComparison metrics:\n")
for k, v in results.items():
    print(f"{k}")
    print(f"  Smoothness   : {v['smoothness']:.8f}")
    print(f"  Fluctuation  : {v['fluctuation']:.8f}")
    print(f"  Raw Variance : {v['raw_variance']:.8f}")
    print()

# arly reflections
plt.figure(figsize=(10,4))
for f in files:
    y, sr = librosa.load(f, sr=None, mono=True)
    peak_index = np.argmax(np.abs(y))
    y = y[peak_index:]
    plt.plot(y[:2000], label=os.path.basename(f))

plt.legend()
plt.title("Early Reflections Comparison")
plt.show()