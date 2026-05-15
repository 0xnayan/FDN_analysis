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

# Decay region in dB
START_DB = -5
END_DB = -60

# Numerical stability
EPS = 1e-8

# Maximum lag to display
MAX_LAG = 5000

# ============================================
# LOAD AUDIO
# ============================================

def load_audio(path):

    fs, x = wav.read(path)

    x = x.astype(np.float32)

    # Stereo → mono
    if len(x.shape) > 1:
        x = np.mean(x, axis=1)

    # Normalize
    peak = np.max(np.abs(x))

    if peak > 0:
        x = x / peak

    return fs, x

# ============================================
# ENVELOPE EXTRACTION
# ============================================

def get_envelope(x):

    env = np.abs(hilbert(x))

    env = np.maximum(env, EPS)

    return env

# ============================================
# dB CONVERSION
# ============================================

def to_db(x):

    x = np.maximum(x, EPS)

    return 20 * np.log10(x)

# ============================================
# TREND REMOVAL
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
# RESIDUAL EXTRACTION PIPELINE
# ============================================

def extract_residual(path):

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

    # Remove unstable transient edge
    env = env[100:]

    # ----------------------------------------
    # Adaptive smoothing
    # ----------------------------------------

    win = len(env) // 20

    if win % 2 == 0:
        win += 1

    win = max(101, min(win, 2001))

    env_smooth = savgol_filter(
        env,
        window_length=win,
        polyorder=3
    )

    # ----------------------------------------
    # dB conversion
    # ----------------------------------------

    db = to_db(env_smooth)

    # Normalize peak to 0 dB
    db = db - np.max(db)

    # ----------------------------------------
    # Extract decay region
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

    return residual

# ============================================
# AUTOCORRELATION
# ============================================

def autocorrelation(x):

    x = x - np.mean(x)

    corr = np.correlate(x, x, mode='full')

    corr = corr[len(corr)//2:]

    # Normalize
    corr = corr / np.max(np.abs(corr))

    return corr

# ============================================
# PERIODICITY METRICS
# ============================================

def periodicity_metrics(ac):

    # Ignore zero-lag peak
    ac_no_zero = ac[1:]

    peak_strength = np.max(ac_no_zero)

    mean_corr = np.mean(np.abs(ac_no_zero))

    return {
        "peak_periodicity": peak_strength,
        "mean_correlation": mean_corr
    }

# ============================================
# PLOTTING
# ============================================

def plot_autocorrelation(results):

    plt.figure(figsize=(10, 6))

    for name, ac in results.items():

        plt.plot(
            ac[:MAX_LAG],
            label=name
        )

    plt.title("Residual Autocorrelation")
    plt.xlabel("Lag")
    plt.ylabel("Normalized Correlation")

    plt.grid(True)
    plt.legend()

    plt.show()

# ============================================
# PRINT RESULTS
# ============================================

def print_metrics(metrics_dict):

    print("\n=== AUTOCORRELATION METRICS ===")

    for name, metrics in metrics_dict.items():

        print(f"\n{name}")

        for k, v in metrics.items():
            print(f"{k}: {v:.6f}")

# ============================================
# MAIN
# ============================================

def main():

    autocorr_results = {}

    metric_results = {}

    for name, path in FILES.items():

        try:

            residual = extract_residual(path)

            ac = autocorrelation(residual)

            metrics = periodicity_metrics(ac)

            autocorr_results[name] = ac

            metric_results[name] = metrics

        except Exception as e:

            print(f"\nError processing {name}")
            print(e)

    # ========================================
    # OUTPUT
    # ========================================

    print_metrics(metric_results)

    plot_autocorrelation(autocorr_results)

# ============================================
# ENTRY
# ============================================

if __name__ == "__main__":
    main()