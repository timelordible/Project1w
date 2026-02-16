# TODO: Replace the code below with your implementation of a FM synthesis
# Hint: You should really be doing PM.
def fm_synth(carrier_type, carrier_freq, mod_index, mod_ratio, dur, fs=44100, amp=1, modulator_type='sine'):

    if dur <= 0:
        return np.array([], dtype=np.float32)
    if fs <= 0:
        raise ValueError("fs must be > 0")
    if carrier_freq < 0:
        raise ValueError("carrier_freq must be >= 0")
    if mod_ratio < 0:
        raise ValueError("mod_ratio must be >= 0")
    if carrier_type not 'sine', 'triangle', 'saw', 'square'
        raise ValueError("carrier_type must be sine, square, saw, or triangle')

    mod_freq = (carrier_freq * mod_ratio)
    I = mod_index

    time_arr = np.arange(0, dur, 1/fs)
    modulator = np.sin(2*np.pi * mod_freq * time_arr)

    sig = (np.sin((2*np.pi * carrier_freq * time_arr) + (I * modulator))

    sig = gen_wave(carrier_type, carrier_freq, dur, fs=fs)
    return sig

    '''
    Returns:
    The function should return a numpy array
    sig (numpy array) = frequency modulated signal
    
    sig = gen_wave(carrier_type, carrier_freq, dur, fs=fs)
    return sig


    def fmSynth(carrier_freq, mod_freq, index, dur, fs=44100):
    time_arr = np.arange(0, dur, 1/fs)
    modulator = np.sin(2*np.pi * mod_freq * time_arr)

    
    Args:
    carrier_type (str) = carrier waveform type: 'sine', 'square', 'saw', or 'triangle'
    carrier_freq (float) = frequency of carrier in Hz
    mod_index (float) = index of modulation
    mod_ratio (float) = modulator frequency = carrier_freq * mod_ratio 
    dur (float) = duration of the sinusoid (in seconds)
    fs (float) = sampling frequency of the sinusoid in Hz
    amp (float) = amplitude of the carrier
    modulator_type (str) = modulator waveform type: 'sine', 'square', 'saw', or 'triangle'
    '''

   

