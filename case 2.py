import numpy as np
import matplotlib.pyplot as plt

# 1. Define Simulation Parameters from Presentation [cite: 190, 198]
N_bits = 10000
EbN0_dB_range = np.arange(0, 11, 2)  # Range from 0 to 10 dB [cite: 198]

# Initialize storage for BER results [cite: 262]
ber_awgn_list = []
ber_multi_list = []

# ==========================================
# BPSK Simulation Core Logic [cite: 248]
# ==========================================
for EbN0_dB in EbN0_dB_range:
    # 1. Map random bits to BPSK (+1, -1) [cite: 248]
    bits = np.random.randint(0, 2, N_bits)
    symbols = 2 * bits - 1

    # 2. Convert SNR dB to linear & compute noise std dev [cite: 248, 254]
    EbN0 = 10 ** (EbN0_dB / 10)
    N0 = 1 / EbN0
    sigma = np.sqrt(N0 / 2)

    # --- CASE 1: AWGN ONLY --- [cite: 248]
    noise_awgn = sigma * np.random.randn(N_bits)
    r_awgn = symbols + noise_awgn
    bits_hat_awgn = (r_awgn >= 0).astype(int)  # Decision Rule [cite: 256]
    ber_awgn = np.mean(bits != bits_hat_awgn)  # BER Calculation [cite: 261]
    ber_awgn_list.append(ber_awgn)

    # --- CASE 2: MULTIPATH (Coherent Combining) --- [cite: 249]
    # Received signal = (1.0 + 0.5) * symbols = 1.5 * symbols
    received_signal = 1.0 * symbols + 0.5 * symbols
    noise_multi = sigma * np.random.randn(N_bits)
    r_multi = received_signal + noise_multi
    bits_hat_multi = (r_multi >= 0).astype(int)
    ber_multi = np.mean(bits != bits_hat_multi)
    ber_multi_list.append(ber_multi)

    print(f"Eb/N0: {EbN0_dB} dB | AWGN BER: {ber_awgn:.5e} | Multipath BER: {ber_multi:.5e}")

# ==========================================
# PLOTTING SECTION
# ==========================================
plt.figure(figsize=(10, 6))
plt.semilogy(EbN0_dB_range, ber_awgn_list, 'bo-', label='AWGN')
plt.semilogy(EbN0_dB_range, ber_multi_list, 'rs-', label='Multipath + AWGN')

plt.title('BER Comparison')
plt.xlabel('Eb/N0 (dB)')
plt.ylabel('Bit Error Rate (BER)')
plt.grid(True, which="both", ls="--")
plt.legend()
plt.show()
