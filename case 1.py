import numpy as np
import matplotlib.pyplot as plt  # 1. Import plotting library

# 1. Define Simulation Parameters
N_bits = 10000
L = 16
span = 6
EbN0_dB_range = np.arange(0, 12, 2)

# Initialize a list to store BER results
ber_results = []

# 2. Define simple RRC filter
rrc_filter = np.ones(span * L) / (span * L)

# ==========================================
# CORE BPSK SIMULATION LOOP
# ==========================================
for EbN0_dB in EbN0_dB_range:
    bits_tx = np.random.randint(0, 2, N_bits)
    symbols_tx = 1 - 2 * bits_tx

    sig_upsampled = np.zeros(len(symbols_tx) * L)
    sig_upsampled[::L] = symbols_tx
    sig_tx = np.convolve(sig_upsampled, rrc_filter, mode='full')

    EbN0_linear = 10 ** (EbN0_dB / 10.0)
    noise_variance = 1 / (2 * L * EbN0_linear)
    noise = np.sqrt(noise_variance) * np.random.randn(len(sig_tx))
    sig_rx_ideal = sig_tx + noise

    sig_rx_matched = np.convolve(sig_rx_ideal, rrc_filter, mode='full')
    ideal_delay = span * L
    sig_sampled = sig_rx_matched[ideal_delay:: L][:N_bits]

    bits_rx = (sig_sampled < 0).astype(int)
    ber = np.mean(bits_tx != bits_rx)

    # 2. Store the result
    ber_results.append(ber)
    print(f"Eb/N0: {EbN0_dB} dB | Simulated BER: {ber:.5e}")

# ==========================================
# PLOTTING SECTION
# ==========================================
plt.figure(figsize=(10, 6))
# Use semilogy because BER is a logarithmic scale [cite: 179]
plt.semilogy(EbN0_dB_range, ber_results, 'bo-', label='Simulated BER')
plt.title('BPSK over AWGN Channel')
plt.xlabel('Eb/N0 (dB)')
plt.ylabel('Bit Error Rate (BER)')
plt.grid(True, which="both", ls="--")
plt.legend()
plt.show()  # This will open the graph in a new window in PyCharm