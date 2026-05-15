import numpy as np
import scipy.io.wavfile as wav
from scipy.signal import hilbert, savgol_filter
import matplotlib.pyplot as plt

# ============================================
# CONFIGURATION
# ============================================

FILES = {
    "original": "/Users/nayanmborah/Music/SuperCollider Recordings/delay_uniform.wav",
    "irregular": "/Users/nayanmborah/Music/SuperCollider Recordings/delay_irregular.wav",
    "optimized": "/Users/nayanmborah/Music/SuperCollider Recordings/delay_optimized.wav",
    "quasi_uniform": "/Users/nayanmborah/Music/SuperCollider Recordings/delay_quasiUniform.wav",
    "golden_ratio": "/Users/nayanmborah/Music/SuperCollider Recordings/delay_goldenRatio.wav"
}


# Ripple frequency split
HF_SPLIT_RATIO = 0.7

# dB analysis region
START_DB = -5
END_DB = -60

# Numerical floor
EPS = 1e-8

# ============================================
# LOAD AUDIO
# ============================================

def load_audio(path):
    fs, x = wav.read(path)

    x = x.astype(np.float32)

    # Stereo → mono
    if len(x.shape) > 1:
        x = np.mean(x, axis=1)

    # Normalize safely
    peak = np.max(np.abs(x))
    if peak > 0:
        x = x / peak

    return fs, x

# ============================================
# ENVELOPE EXTRACTION
# ============================================

def get_envelope(x):
    env = np.abs(hilbert(x))

    # Prevent invalid values
    env = np.maximum(env, EPS)

    return env

# ============================================
# dB CONVERSION
# ============================================

def to_db(x):
    x = np.maximum(x, EPS)
    return 20 * np.log10(x)

# ============================================
# TREND FITTING
# ============================================

def remove_trend(y):

    t = np.arange(len(y))

    coeffs = np.polyfit(t, y, 1)

    trend = np.polyval(coeffs, t)

    residual = y - trend

    # Center residual
    residual = residual - np.mean(residual)

    return residual, trend

# ============================================
# METRICS
# ============================================

def variance_metric(r):
    return np.var(r)

def mad_metric(r):
    return np.mean(np.abs(r))

def derivative_energy(r):
    return np.mean(np.diff(r) ** 2)

def fft_ripple(r):

    # Remove DC before FFT
    r = r - np.mean(r)

    R = np.fft.rfft(r)

    mag = np.abs(R)

    power = mag ** 2

    split = int(HF_SPLIT_RATIO * len(power))

    hf_energy = np.sum(power[split:])

    total_energy = np.sum(power)

    if total_energy == 0:
        return 0.0

    return hf_energy / total_energy

# ============================================
# ANALYSIS PIPELINE
# ============================================

def analyze(path):

    fs, x = load_audio(path)

    # ----------------------------------------
    # Envelope
    # ----------------------------------------

    env = get_envelope(x)

    # ----------------------------------------
    # Peak alignment
    # ----------------------------------------

    peak_idx = np.argmax(env)

    env = env[peak_idx:]

    # ----------------------------------------
    # Adaptive smoothing
    # ----------------------------------------

    win = len(env) // 20

    # Ensure odd
    if win % 2 == 0:
        win += 1

    # Clamp range
    win = max(101, min(win, 2001))

    env_smooth = savgol_filter(
        env,
        window_length=win,
        polyorder=3
    )

    # ----------------------------------------
    # Convert to dB
    # ----------------------------------------

    db = to_db(env_smooth)

    # Normalize peak to 0 dB
    db = db - np.max(db)

    # ----------------------------------------
    # Extract continuous decay region
    # ----------------------------------------

    valid = np.where(
        (db <= START_DB) &
        (db >= END_DB)
    )[0]

    if len(valid) < 10:
        raise ValueError("Decay region too small.")

    start = valid[0]
    end = valid[-1]

    db = db[start:end]

    # ----------------------------------------
    # Trend removal
    # ----------------------------------------

    residual, trend = remove_trend(db)

    # ========================================
    # METRICS
    # ========================================

    metrics = {
        "variance": variance_metric(residual),
        "mad": mad_metric(residual),
        "derivative_energy": derivative_energy(residual),
        "fft_ripple": fft_ripple(residual)
    }

    return db, trend, residual, metrics

# ============================================
# PLOTTING
# ============================================

def plot_decay(results):

    plt.figure(figsize=(8, 5))

    for name, (db, _, _, _) in results.items():
        plt.plot(db, label=name)

    plt.title("Decay Comparison")
    plt.xlabel("Samples")
    plt.ylabel("Amplitude (dB)")
    plt.grid(True)
    plt.legend()

    plt.show()

def plot_residual(results):

    plt.figure(figsize=(8, 5))

    for name, (_, _, residual, _) in results.items():
        plt.plot(residual, label=name)

    plt.axhline(0, linestyle='--')

    plt.title("Ripple Residual Comparison")
    plt.xlabel("Samples")
    plt.ylabel("Residual (dB)")
    plt.grid(True)
    plt.legend()

    plt.show()

def plot_signal_vs_trend(results):

    plt.figure(figsize=(10, 6))

    for name, (db, trend, _, _) in results.items():

        plt.plot(
            db,
            label=f"{name} signal",
            alpha=0.8
        )

        plt.plot(
            trend,
            '--',
            label=f"{name} trend",
            alpha=0.9
        )

    plt.title("Signal vs Trend")
    plt.xlabel("Samples")
    plt.ylabel("Amplitude (dB)")
    plt.grid(True)
    plt.legend()

    plt.show()

# ============================================
# RESULTS
# ============================================

def print_results(results):

    print("\n=== METRICS ===")

    for name, (_, _, _, metrics) in results.items():

        print(f"\n{name}")

        for k, v in metrics.items():
            print(f"{k}: {v:.8f}")

    # ----------------------------------------
    # Relative comparison
    # ----------------------------------------

    if "original" in results:

        base = results["original"][3]

        print("\n=== CHANGE vs ORIGINAL ===")

        for name, (_, _, _, metrics) in results.items():

            if name == "original":
                continue

            print(f"\n{name}")

            for k in metrics:

                change = (
                    (metrics[k] - base[k])
                    / abs(base[k])
                ) * 100

                direction = "better"

                # Lower is better for all metrics
                if change > 0:
                    direction = "worse"

                print(
                    f"{k}: "
                    f"{abs(change):.2f}% {direction}"
                )

# ============================================
# MAIN
# ============================================

def main():

    results = {}

    for name, path in FILES.items():

        try:

            db, trend, residual, metrics = analyze(path)

            results[name] = (
                db,
                trend,
                residual,
                metrics
            )

        except Exception as e:

            print(f"\nError processing {name}")
            print(e)

    # ========================================
    # OUTPUT
    # ========================================

    print_results(results)

    plot_decay(results)

    plot_residual(results)

    plot_signal_vs_trend(results)

# ============================================
# ENTRY
# ============================================

if __name__ == "__main__":
    main()