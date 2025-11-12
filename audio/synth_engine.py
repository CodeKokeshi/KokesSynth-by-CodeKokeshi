"""
Synthesizer engine for generating retro sounds
OPTIMIZED VERSION - No thread spam, uses audio mixer
"""

import numpy as np
import sounddevice as sd
from threading import Lock
import time


class SynthEngine:
    def __init__(self, sample_rate=44100, buffer_size=2048):
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.waveform = 'square'
        self.attack = 0.05  # seconds
        self.decay = 0.2    # seconds
        
        # Audio mixer - stores active voices
        self.active_voices = []
        self.voices_lock = Lock()
        self.max_voices = 16  # Limit polyphony
        
        # Start the audio stream
        self.stream = sd.OutputStream(
            samplerate=self.sample_rate,
            channels=1,
            callback=self._audio_callback,
            blocksize=buffer_size
        )
        self.stream.start()
        
    def __del__(self):
        """Cleanup audio stream"""
        if hasattr(self, 'stream'):
            self.stream.stop()
            self.stream.close()
        
    def set_waveform(self, waveform):
        """Set the waveform type"""
        self.waveform = waveform
        
    def set_attack(self, attack_ms):
        """Set attack time in milliseconds"""
        self.attack = attack_ms / 1000.0
        
    def set_decay(self, decay_ms):
        """Set decay time in milliseconds"""
        self.decay = decay_ms / 1000.0
        
    def generate_waveform(self, frequency, num_samples, start_phase=0):
        """Generate a waveform based on current settings"""
        t = (np.arange(num_samples) + start_phase) / self.sample_rate
        
        if self.waveform == 'square':
            wave = np.sign(np.sin(2 * np.pi * frequency * t))
        elif self.waveform == 'sawtooth':
            wave = 2 * (t * frequency - np.floor(t * frequency + 0.5))
        elif self.waveform == 'triangle':
            wave = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
        elif self.waveform == 'pulse':
            # Pulse wave with 25% duty cycle
            wave = np.where(np.sin(2 * np.pi * frequency * t) > 0.5, 1, -1)
        elif self.waveform == 'noise':
            wave = np.random.uniform(-1, 1, num_samples)
        else:
            wave = np.sin(2 * np.pi * frequency * t)
            
        return wave
        
    def apply_envelope(self, wave, voice):
        """Apply ADSR envelope to the waveform"""
        samples = len(wave)
        envelope = np.ones(samples)
        
        for i in range(samples):
            elapsed = voice['elapsed_samples'] + i
            
            # Attack phase
            if elapsed < voice['attack_samples']:
                envelope[i] = elapsed / voice['attack_samples']
            # Decay phase
            elif elapsed > voice['total_samples'] - voice['decay_samples']:
                remaining = voice['total_samples'] - elapsed
                envelope[i] = remaining / voice['decay_samples']
            
            # Clamp to valid range
            envelope[i] = max(0, min(1, envelope[i]))
        
        return wave * envelope
        
    def _audio_callback(self, outdata, frames, time_info, status):
        """Audio callback for mixing and output - runs in audio thread"""
        if status:
            print(f"Audio status: {status}")
        
        # Initialize output buffer with silence
        output = np.zeros(frames)
        
        with self.voices_lock:
            # Mix all active voices
            finished_voices = []
            
            for voice in self.active_voices:
                remaining = voice['total_samples'] - voice['elapsed_samples']
                to_render = min(frames, remaining)
                
                if to_render > 0:
                    # Generate waveform chunk
                    chunk = self.generate_waveform(
                        voice['frequency'],
                        to_render,
                        voice['elapsed_samples']
                    )
                    
                    # Apply envelope
                    chunk = self.apply_envelope(chunk, voice)
                    
                    # Mix into output
                    output[:to_render] += chunk * voice['volume']
                    
                    voice['elapsed_samples'] += to_render
                
                # Mark finished voices
                if voice['elapsed_samples'] >= voice['total_samples']:
                    finished_voices.append(voice)
            
            # Remove finished voices
            for voice in finished_voices:
                self.active_voices.remove(voice)
        
        # Normalize and apply master volume
        if len(output) > 0:
            max_val = np.max(np.abs(output))
            if max_val > 1.0:
                output = output / max_val  # Prevent clipping
            output *= 0.5  # Master volume
        
        # Write to output buffer
        outdata[:, 0] = output
        
    def play_note(self, frequency, duration=0.5):
        """Play a note with given frequency and duration"""
        with self.voices_lock:
            # Remove oldest voice if we hit the limit
            if len(self.active_voices) >= self.max_voices:
                self.active_voices.pop(0)
            
            # Create new voice
            voice = {
                'frequency': frequency,
                'volume': 0.3,
                'elapsed_samples': 0,
                'total_samples': int(duration * self.sample_rate),
                'attack_samples': int(self.attack * self.sample_rate),
                'decay_samples': int(self.decay * self.sample_rate),
                'waveform': self.waveform
            }
            
            self.active_voices.append(voice)
