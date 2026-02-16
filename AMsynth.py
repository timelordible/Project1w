# TODO: Replace the code below with your implementation of a AM synthesis
def am_synth(carrier_type, carrier_freq, mod_depth, mod_ratio, dur, fs=44100, amp=1, modulator_type='sine'):

    mod_freq = carrier_freq*mod_ratio
    time_arr = np.arange(0, dur, 1/fs)
    
    if modulator_type.casefold() == 'sine':
        mod = np.sin(np.pi*2 * mod_freq * time_arr)
    elif modulator_type.casefold() == 'square':
        mod = square(2*np.pi * mod_freq * time_arr)
    elif modulator_type.casefold() == 'saw':
        mod = saw(2*np.pi * mod_freq * time_arr)
    elif modulator_type.casefold() == 'triangle':
        mod = tri(2*np.pi * mod_freq * time_arr, width=0.5)
    else:
        print('Please enter sine, square, saw, or tri for modulator wave type')
        return None

    if carrier_type.casefold() == 'sine':
        carrier = np.sin(np.pi*2 * carrier_freq * time_arr)
    elif carrier_type.casefold() == 'square':
        carrier = square(2*np.pi * carrier_freq * time_arr)
    elif carrier_type.casefold() == 'saw':
        carrier = saw(2*np.pi * carrier_freq * time_arr)
    elif carrier_type.casefold() == 'triangle':
        carrier = tri(2*np.pi * carrier_freq * time_arr, width=0.5)
    else:
        print('Please enter sine, square, saw, or tri for carrier wave type')
        return None
    env = 1 + mod_depth * mod
    sig = (amp * env * carrier)
    return sig



    """
    Args:
    carrier_type (str) = carrier waveform type: 'sine', 'square', 'saw', or 'triangle'
    carrier_freq (float) = frequency of carrier in Hz
    mod_depth (float) = depth of the modulator
    mod_ratio (float) = modulation ratio, where 1:mod_ratio is C:M
    dur (float) = duration of the sinusoid (in seconds)
    fs (float) = sampling frequency of the sinusoid in Hz
    amp (float) = amplitude of the carrier
    modulator_type (str) = modulator waveform type: 'sine', 'square', 'saw', or 'triangle'

    Returns:
    The function should return a numpy array
    sig (numpy array) = amplitude modulated signal

     sig = gen_wave(carrier_type, carrier_freq, dur, fs=fs, am)
