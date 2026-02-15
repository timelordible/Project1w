# TODO: Replace the code below with your implementation of a FM synthesis
# Hint: You should really be doing PM.
def fm_synth(carrier_type, carrier_freq, mod_index, mod_ratio, dur, fs=44100, amp=1, modulator_type='sine'):
    """
    Args:
    carrier_type (str) = carrier waveform type: 'sine', 'square', 'saw', or 'triangle'
    carrier_freq (float) = frequency of carrier in Hz
    mod_index (float) = index of modulation
    mod_ratio (float) = modulation ratio, where modulator frequency = carrier_freq * mod_ratio
    dur (float) = duration of the sinusoid (in seconds)
    fs (float) = sampling frequency of the sinusoid in Hz
    amp (float) = amplitude of the carrier
    modulator_type (str) = modulator waveform type: 'sine', 'square', 'saw', or 'triangle'

    Returns:
    The function should return a numpy array
    sig (numpy array) = frequency modulated signal
    """
    sig = gen_wave(carrier_type, carrier_freq, dur, fs=fs)
    return sig
