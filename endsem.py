import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import upfirdn, lfilter
from scipy.special import erfc

# ==========================================
# 1. System Parameters
# ==========================================
N_bits = 50000          # Number of bits to simulate per SNR point
L = 16                  # Oversampling factor (samples per symbol)
alpha = 0.5             # Roll-off factor for Root-Raised Cosine (RRC) filter
span = 6                # Span of the RRC filter in symbols
EbN0_dB_range = np.arange(0, 12, 1) # Eb/N0 range in dB

# Channel & Degradation Parameters
channel_attenuation = 0.05  # Severe channel attenuation (A << 1)
timing_offset_fraction = 0.1 # Timing offset as a fraction of Ts (e.g., 10%)
timing_offset_samples = int(timing_offset_fraction * L)

# AGC Parameters
agc_target_rms = 1.0
agc_alpha = 0.01        # Forgetting factor for RMS estimation
agc_beta = 0.05         # Loop gain for updating the AGC multiplier

# ==========================================
# 2. Helper Functions
# ==========================================
def rrcosfilter(N, alpha, Ts, Fs):
    """Generates a Root-Raised Cosine (RRC) filter."""
    T_delta = 1/Fs
    time_idx = np.arange(-N/2, N/2) * T_delta
    # Avoid division by zero
    time_idx += 1e-8

    # RRC equation
    num = np.sin(np.pi * time_idx * (1-alpha) / Ts) + \
          4 * alpha * (time_idx / Ts) * np.cos(np.pi * time_idx * (1+alpha) / Ts)
    den = np.pi * (time_idx / Ts) * (1 - (4 * alpha * (time_idx / Ts))**2)
    h = num / den
    return h / np.sqrt(np.sum(h**2)) # Normalize energy

def agc_loop(signal, target_rms, alpha, beta):
    """Simple feedback Automatic Gain Control (AGC) loop."""
    out_signal = np.zeros_like(signal)
    gain = 1.0
    v_rms = 0.0

    for i in range(len(signal)):
        # Apply current gain
        out_signal[i] = signal[i] * gain

        # Estimate short-term RMS (using absolute value for simplicity)
        v_rms = (1 - alpha) * v_rms + alpha * np.abs(out_signal[i])

        # Calculate error and update gain
        error = target_rms - v_rms
        gain = gain + beta * error

    return out_signal

# ==========================================
# 3. Simulation Loop
# ==========================================
# Generate RRC Filter
rrc_filter = rrcosfilter(span * L, alpha, 1, L)

ber_simulated_ideal = []
ber_simulated_degraded = []
ber_theoretical = []

print("Starting CommLink-BPSK Simulation...")

for EbN0_dB in EbN0_dB_range:
    # A. Transmitter (Tx)
    bits_tx = np.random.randint(0, 2, N_bits)
    symbols_tx = 1 - 2 * bits_tx # BPSK Mapping: 0 -> +1, 1 -> -1

    # Upsample and apply Tx Pulse Shaping
    sig_upsampled = upfirdn([1], symbols_tx, L)
    sig_tx = np.convolve(sig_upsampled, rrc_filter, 'full')

    # B. Channel
    # Apply attenuation
    sig_rx_clean = sig_tx * channel_attenuation

    # Calculate Noise Power
    EbN0_linear = 10 ** (EbN0_dB / 10.0)
    # SNR adjustment for oversampling and BPSK
    noise_variance = 1 / (2 * L * EbN0_linear)
    noise = np.sqrt(noise_variance) * np.random.randn(len(sig_rx_clean))

    # Received signal
    sig_rx = sig_rx_clean + noise

    # C. Receiver (Rx) - Degraded Path (With AGC & Timing Offset)
    # 1. AGC
    sig_rx_agc = agc_loop(sig_rx, agc_target_rms, agc_alpha, agc_beta)

    # 2. Matched Filter
    sig_rx_matched = np.convolve(sig_rx_agc, rrc_filter, 'full')

    # 3. Timing Synchronization & Downsampling
    # The filter delay is span * L. We add the timing offset here.
    delay = span * L + timing_offset_samples
    sig_rx_sampled_degraded = sig_rx_matched[delay :: L][:N_bits]

    # 4. Decision (Degraded)
    bits_rx_degraded = (sig_rx_sampled_degraded < 0).astype(int)
    errors_degraded = np.sum(bits_tx != bits_rx_degraded)
    ber_simulated_degraded.append(errors_degraded / N_bits)

    # D. Receiver (Rx) - Ideal Path (Perfect Synch, No AGC needed if perfectly scaled)
    # Reverse attenuation for ideal comparison and apply matched filter
    sig_rx_ideal_matched = np.convolve((sig_rx_clean/channel_attenuation) + noise/channel_attenuation, rrc_filter, 'full')
    sig_rx_sampled_ideal = sig_rx_ideal_matched[span * L :: L][:N_bits]
    bits_rx_ideal = (sig_rx_sampled_ideal < 0).astype(int)
    errors_ideal = np.sum(bits_tx != bits_rx_ideal)
    ber_simulated_ideal.append(errors_ideal / N_bits)

    # E. Theoretical BER
    ber_theo = 0.5 * erfc(np.sqrt(EbN0_linear))
    ber_theoretical.append(ber_theo)

    print(f"Eb/N0: {EbN0_dB} dB | Ideal BER: {ber_simulated_ideal[-1]:.5e} | Degraded BER: {ber_simulated_degraded[-1]:.5e}")

# ==========================================
# 4. Visualization & Reporting
# ==========================================
plt.figure(figsize=(10, 6))
plt.semilogy(EbN0_dB_range, ber_theoretical, 'k-', linewidth=2, label='Theoretical BPSK')
plt.semilogy(EbN0_dB_range, ber_simulated_ideal, 'bo--', label='Simulated Ideal (Perfect Sync)')
plt.semilogy(EbN0_dB_range, ber_simulated_degraded, 'r*-.', label=f'Simulated Degraded (AGC + {timing_offset_fraction*100}% Timing Offset)')

# Formatting
plt.title('CommLink-BPSK: BER Sensitivity to Timing Offset & AGC')
plt.xlabel('$E_b/N_0$ (dB)')
plt.ylabel('Bit Error Rate (BER)')
plt.grid(True, which='both', linestyle='--', alpha=0.6)
plt.legend()
plt.ylim([1e-5, 1])
plt.xlim([0, 11])

# Highlight the 10^-5 target line
plt.axhline(1e-5, color='gray', linestyle=':', label='Target BER ($10^{-5}$)')

plt.tight_layout()
plt.show()