import numpy as np
from scipy.io.wavfile import read, write
from scipy import signal


# TODO: Replace the code below with your implementation of the waveforms.
# Hint: You may want to write more helper functions to create the waveforms
# Note: How will you handle aliasing?
def gen_wave(type, freq, dur, fs=44100, amp=1, phi=0):
    """
    Args:
    type (str) = waveform type: 'sine', 'square', 'saw', or 'triangle'
    freq (float) = fundamental frequency in Hz
    dur (float) = duration of the sinusoid (in seconds)
    fs (float) = sampling frequency of the sinusoid in Hz
    amp (float) = amplitude of the fundamental
    phi (float) = initial phase of the wave in radians
    Returns:
    The function should return a numpy array
    wave (numpy array) = The generated waveform
    """
        
    t = np.arange(0, dur, 1/fs) # Time vector length (used for zeros_like safety)


    if freq <= 0:
        return np.zeros(len(t)) #for error

   
    nyquist = fs / 2
    max_harmonic = int(nyquist // freq)  # Nyquist limit for aliasing control
  
    wave = np.array([])

    if type == 'sine':
        # create sinusoid
        wave = genSine(freq, dur, amp, phi, fs)
    elif type == 'saw':
        # create saw
        wave = np.zeros_like(t)
        for k in range(1, max_harmonic + 1):
            harmonic = genSine(k * freq, dur, 1/k, phi, fs)
            wave += ((-1)**(k+1)) * harmonic
        wave = (2 / np.pi) * amp * wave

    elif type == 'square':
        # create square
        wave = np.zeros_like(t)
        for k in range(1, max_harmonic + 1, 2):
            harmonic = genSine(k * freq, dur, 1/k, phi, fs)
            wave += harmonic
        wave = (4 / np.pi) * amp * wave
         
    elif type == 'triangle':
        # create triangle
        wave = np.zeros_like(t)
        for k in range(1, max_harmonic + 1, 2):
            sign = (-1) ** ((k - 1) // 2)
            harmonic = genSine(k * freq, dur, 1/(k**2), phi, fs)
            wave += sign * harmonic
        wave = (8 / (np.pi**2)) * amp * wave
    return wave
    

# TODO: Replace the code below with your implementation of an ADSR
# Hint: If you use %'s for your ADSR lengths, what length should the sustain value be
# Note: How will you handle percentages that are too long? For example, attack is 50, decay is 50, release is 50?
def adsr(data, attack, decay, sustain, release, fs=44100):
    """
    Args:
    data (np.array) = signal to be modified
    attack (float) = value between 0-100 representing what percentage of the note duration the attack should be
    decay (float) = value between 0-100 representing what percentage of the note duration the attack should be
    sustain (float) = value between 0-1 representing the amplitude of the sustain
    release (float) = value between 0-100 representing what percentage of the note duration the attack should be
    fs (float) = sampling frequency of the sinusoid in Hz
    Returns:
    The function should return a numpy array
    sig (numpy array) = the modified, enveloped signal
    """
    if attack + decay + release > 100:
        print("Please insert values that are shorter than 100% total.")
        return data
    
    x = data
    attackSamps = int((attack / 100) * len(x))
    decaySamps = int((decay / 100) * len(x))
    releaseSamps = int((release / 100) * len(x))
    sustainSamps = len(x) - attackSamps - decaySamps - releaseSamps


    attackSamps = int((attack / 100) * len(x))
    decaySamps = int((decay / 100) * len(x))
    releaseSamps = int((release / 100) * len(x))

    sustainSamps = len(x) - (attackSamps + decaySamps + releaseSamps)
    attackDur = np.linspace(0, 1, attackSamps)
    decayDur = np.linspace(1, sustain, decaySamps)
    sustainDur = np.full(sustainSamps, sustain)
    releaseDur = np.linspace(sustain, 0, releaseSamps)
    env = np.concatenate([attackDur, decayDur, sustainDur, releaseDur])

    sig = x * env
    
    return sig


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
    if carrier_type not in ['sine', 'triangle', 'saw', 'square']:
        raise ValueError("carrier_type must be sine, square, saw, or triangle")

    mod_freq = (carrier_freq * mod_ratio)
    I = mod_index
    time_arr = np.arange(0, dur, 1/fs)
    modulator = np.sin(2*np.pi * mod_freq * time_arr)

    sig = np.sin((2*np.pi * carrier_freq * time_arr) + (I * modulator)) * amp
    return sig

# TODO: Replace the code below with your implementation of a AM synthesis
def am_synth(carrier_type, carrier_freq, mod_depth, mod_ratio, dur, fs=44100, amp=1, modulator_type='sine'):

    mod_freq = carrier_freq*mod_ratio
    time_arr = np.arange(0, dur, 1/fs)
    
    if modulator_type.casefold() == 'sine':
        mod = np.sin(np.pi*2 * mod_freq * time_arr)
    elif modulator_type.casefold() == 'square':
        mod = np.square(2*np.pi * mod_freq * time_arr)
    elif modulator_type.casefold() == 'saw':
        mod = np.saw(2*np.pi * mod_freq * time_arr)
    elif modulator_type.casefold() == 'triangle':
        mod = np.tri(2*np.pi * mod_freq * time_arr, width=0.5)
    else:
        print('Please enter sine, square, saw, or tri for modulator wave type')
        return None

    if carrier_type.casefold() == 'sine':
        carrier = np.sin(np.pi*2 * carrier_freq * time_arr)
    elif carrier_type.casefold() == 'square':
        carrier = np.square(2*np.pi * carrier_freq * time_arr)
    elif carrier_type.casefold() == 'saw':
        carrier = np.saw(2*np.pi * carrier_freq * time_arr)
    elif carrier_type.casefold() == 'triangle':
        carrier = np.tri(2*np.pi * carrier_freq * time_arr, width=0.5)
    else:
        print('Please enter sine, square, saw, or tri for carrier wave type')
        return None
    env = 1 + mod_depth * mod
    sig = (amp * env * carrier)
    return sig


# TODO: Complete at least one of the functions below: filter, reverb, delay.

# Note: I wrote this to only create low or highpass filters. You can alter to create bandpass/bandstop, but do not change the function definition.
def filter(data, type, cutoff_freq, fs=44100, order=5):
    """
    Args:
    data (np.array) = signal to be modified
    type (str) = filter type 'lowpass' or 'highpass'
    cutoff_freq (float) = cutoff frequency in Hz
    fs (float) = sampling frequency of the sinusoid in Hz
    order (int) = filter order

    Returns:
    The function should return a numpy array
    sig (numpy array) = filtered signal
    """
    sig = data
    return sig

def reverb(data, ir, dry_wet=0.5):
    """
    Args:
    data (np.array) = signal to be modified
    ir (str) = file path to impulse response
    dry_wet (float) = value between 0-1 dry/wet balance

    Returns:
    The function should return a numpy array
    sig (numpy array) = signal with reverb
    """
    sig = data
    return sig

def delay(data, delay_time, dry_wet=0.5, fs=44100):
 # Number of repeats (echo taps)
    repeats = 3

    # Convert delay time (seconds) to milliseconds logic like your notebook
    offset_ms = delay_time * 1000
    offset_samples = int(fs / 1000 * offset_ms)

    # Safety check
    if offset_samples <= 0 or len(data) == 0:
        return data

    # Create output buffer long enough to hold echoes
    total_length = len(data) + offset_samples * repeats
    sig = np.zeros(total_length)

    # Add original (dry signal)
    sig[:len(data)] += data * (1 - dry_wet)

    # Create repeated delayed copies using a FOR LOOP (like your screenshot)
    for i in range(1, repeats + 1):
        # Each repeat gets quieter (classic echo decay)
        decay = (dry_wet) ** i

        # Create padding before the delayed copy
        pad_beg = np.zeros(offset_samples * i)
        pad_end = np.zeros(total_length - len(data) - offset_samples * i)

        # Shifted (delayed) version of the signal
        delayed_copy = np.concatenate([pad_beg, data * decay, pad_end])

        # Add to output signal
        sig += delayed_copy

    # Normalize to prevent clipping
    max_val = np.max(np.abs(sig))
    if max_val > 1:
        sig = sig / max_val

    return sig
