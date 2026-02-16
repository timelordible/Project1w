import numpy as np
from scipy.io.wavfile import read, write
from scipy import signal

def genSine(f=None, dur=1, A=1, phi=0, fs=44100):
    A = float(A)
    f = float(f)
    phi = float(phi)
    fs = float(fs)
    dur = float(dur)
    
    t = np.arange(0, dur, 1/fs)
    x = A * np.sin(2*np.pi*f*t + phi)
    return x

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
    
