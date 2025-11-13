"""
Main window for the Retro Audio Synthesizer
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QSlider, QComboBox, QGridLayout,
                             QGroupBox, QSpinBox, QFileDialog, QDialog, QDialogButtonBox)
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QPalette, QColor, QDesktopServices
from audio.synth_engine import SynthEngine
from gui.sequencer_canvas import SequencerCanvas
from audio.music_generator import MusicGenerator
import numpy as np
import sounddevice as sd
import os
import subprocess
import platform


class SequencerButton(QPushButton):
    """Custom button for sequencer with drag support"""
    def __init__(self, row, col, parent_window):
        super().__init__()
        self.row = row
        self.col = col
        self.parent_window = parent_window
        self.setAcceptDrops(True)
        # IMPORTANT: Disable auto-exclusive behavior
        self.setAutoExclusive(False)
        
    def mousePressEvent(self, event):
        """Handle mouse press - DON'T call super to prevent default toggle"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Toggle the button manually
            new_state = not self.isChecked()
            self.setChecked(new_state)
            
            # Start dragging with current state
            self.parent_window.is_dragging = True
            self.parent_window.drag_state = new_state
            self.parent_window.last_drag_pos = (self.row, self.col)
            
            # Accept the event to prevent propagation
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move - this is the key for drag"""
        if self.parent_window.is_dragging and event.buttons() & Qt.MouseButton.LeftButton:
            # Apply drag state to this button
            self.setChecked(self.parent_window.drag_state)
            self.parent_window.last_drag_pos = (self.row, self.col)
            event.accept()
        else:
            super().mouseMoveEvent(event)
    
    def enterEvent(self, event):
        """Handle mouse enter during drag"""
        if self.parent_window.is_dragging:
            # Apply drag state to this button
            self.setChecked(self.parent_window.drag_state)
            self.parent_window.last_drag_pos = (self.row, self.col)
        super().enterEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.parent_window.is_dragging = False
            self.parent_window.drag_state = None
            event.accept()
        else:
            super().mouseReleaseEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kokesynth by CodeKokeshi")
        self.setGeometry(100, 100, 1200, 700)
        
        # Initialize synth engine
        self.synth = SynthEngine()
        
        # Initialize music generator
        self.music_gen = MusicGenerator()
        
        # Sequencer state
        self.is_playing = False
        self.current_step = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.step_sequencer)
        
        # Drag state
        self.is_dragging = False
        self.drag_state = None
        self.last_drag_pos = None
        
        # Setup UI
        self.setup_ui()
        self.apply_dark_theme()
        
    def setup_ui(self):
        """Setup the main user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Top controls layout
        top_layout = QHBoxLayout()
        
        # Instrument selector
        self.create_instrument_selector(top_layout)
        
        # Sound parameters
        self.create_sound_controls(top_layout)
        
        main_layout.addLayout(top_layout)
        
        # Keyboard section
        keyboard_group = self.create_keyboard_section()
        main_layout.addWidget(keyboard_group)
        
        # Sequencer section
        sequencer_group = self.create_sequencer_section()
        main_layout.addWidget(sequencer_group)
        
        # Playback controls
        controls_layout = self.create_playback_controls()
        main_layout.addLayout(controls_layout)
        
    def create_instrument_selector(self, layout):
        """Create instrument selection controls"""
        group = QGroupBox("Instrument")
        group_layout = QVBoxLayout()
        
        self.instrument_combo = QComboBox()
        self.instrument_combo.addItems([
            "Square Wave (Classic Chiptune)",
            "Sawtooth Wave (Buzzy)",
            "Triangle Wave (Mellow)",
            "Pulse Wave (Retro Game)",
            "Noise (Drums/Effects)"
        ])
        self.instrument_combo.currentIndexChanged.connect(self.change_instrument)
        group_layout.addWidget(self.instrument_combo)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
    def create_sound_controls(self, layout):
        """Create sound parameter controls"""
        group = QGroupBox("Sound Controls")
        group_layout = QVBoxLayout()
        
        # Attack control
        attack_layout = QHBoxLayout()
        attack_layout.addWidget(QLabel("Attack:"))
        self.attack_slider = QSlider(Qt.Orientation.Horizontal)
        self.attack_slider.setMinimum(1)
        self.attack_slider.setMaximum(500)
        self.attack_slider.setValue(50)
        self.attack_slider.valueChanged.connect(lambda v: self.synth.set_attack(v))
        attack_layout.addWidget(self.attack_slider)
        self.attack_label = QLabel("50ms")
        attack_layout.addWidget(self.attack_label)
        self.attack_slider.valueChanged.connect(lambda v: self.attack_label.setText(f"{v}ms"))
        group_layout.addLayout(attack_layout)
        
        # Decay control
        decay_layout = QHBoxLayout()
        decay_layout.addWidget(QLabel("Decay:"))
        self.decay_slider = QSlider(Qt.Orientation.Horizontal)
        self.decay_slider.setMinimum(50)
        self.decay_slider.setMaximum(2000)
        self.decay_slider.setValue(200)
        self.decay_slider.valueChanged.connect(lambda v: self.synth.set_decay(v))
        decay_layout.addWidget(self.decay_slider)
        self.decay_label = QLabel("200ms")
        decay_layout.addWidget(self.decay_label)
        self.decay_slider.valueChanged.connect(lambda v: self.decay_label.setText(f"{v}ms"))
        group_layout.addLayout(decay_layout)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
        
    def create_keyboard_section(self):
        """Create the musical keyboard section"""
        group = QGroupBox("Click to Play")
        layout = QHBoxLayout()
        layout.setSpacing(3)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Notes for a retro feel - pentatonic scale for easy jamming
        self.notes = [
            ('C4', 261.63), ('D4', 293.66), ('E4', 329.63), ('G4', 392.00), ('A4', 440.00),
            ('C5', 523.25), ('D5', 587.33), ('E5', 659.25), ('G5', 783.99), ('A5', 880.00),
            ('C6', 1046.50), ('D6', 1174.66), ('E6', 1318.51), ('G6', 1567.98), ('A6', 1760.00)
        ]
        
        self.key_buttons = []
        
        # Create keyboard buttons in ONE horizontal row
        for note_name, freq in self.notes:
            btn = QPushButton(note_name)
            btn.setFixedSize(45, 35)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2c3e50;
                    color: #ecf0f1;
                    border: 1px solid #34495e;
                    border-radius: 3px;
                    font-size: 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #34495e;
                    border: 2px solid #3498db;
                }
                QPushButton:pressed {
                    background-color: #3498db;
                }
            """)
            btn.clicked.connect(lambda checked, f=freq: self.play_note(f))
            layout.addWidget(btn)
            self.key_buttons.append(btn)
        
        layout.addStretch()
        group.setLayout(layout)
        return group
        
    def create_sequencer_section(self):
        """Create the step sequencer section"""
        group = QGroupBox("Pattern Sequencer - Draw Notes Freely")
        layout = QVBoxLayout()
        
        # 15 rows (notes) x 16 steps - matches keyboard!
        self.seq_rows = 15
        self.seq_steps = 16
        
        # Note frequencies - same as keyboard (C4 to A6)
        self.seq_freqs = [
            1760.00,  # A6
            1567.98,  # G6
            1318.51,  # E6
            1174.66,  # D6
            1046.50,  # C6
            880.00,   # A5
            783.99,   # G5
            659.25,   # E5
            587.33,   # D5
            523.25,   # C5
            440.00,   # A4
            392.00,   # G4
            329.63,   # E4
            293.66,   # D4
            261.63    # C4
        ]
        
        # Create canvas-based sequencer
        self.sequencer_canvas = SequencerCanvas(rows=self.seq_rows, steps=self.seq_steps)
        layout.addWidget(self.sequencer_canvas)
        
        # Help text
        help_label = QLabel("💡 Click & Drag: Pattern Notes | Use MELODY GENERATOR for smooth curves")
        help_label.setStyleSheet("color: #7f8c8d; font-size: 11px; padding: 5px;")
        help_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(help_label)
        
        # Tempo control
        tempo_layout = QHBoxLayout()
        tempo_layout.addWidget(QLabel("Tempo (BPM):"))
        self.tempo_spin = QSpinBox()
        self.tempo_spin.setMinimum(60)
        self.tempo_spin.setMaximum(240)
        self.tempo_spin.setValue(120)
        self.tempo_spin.valueChanged.connect(self.update_tempo)
        tempo_layout.addWidget(self.tempo_spin)
        tempo_layout.addStretch()
        layout.addLayout(tempo_layout)
        
        group.setLayout(layout)
        return group
        
    def create_playback_controls(self):
        """Create playback control buttons"""
        layout = QHBoxLayout()
        
        self.play_btn = QPushButton("PLAY")
        self.play_btn.setMinimumSize(100, 50)
        self.play_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.play_btn.clicked.connect(self.toggle_playback)
        layout.addWidget(self.play_btn)
        
        self.stop_btn = QPushButton("STOP")
        self.stop_btn.setMinimumSize(100, 50)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #c0392b;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_playback)
        layout.addWidget(self.stop_btn)
        
        self.clear_btn = QPushButton("CLEAR")
        self.clear_btn.setMinimumSize(100, 50)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_pattern)
        layout.addWidget(self.clear_btn)
        
        # Generate section with dropdown
        gen_layout = QVBoxLayout()
        
        # Preset selector
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("Preset:"))
        
        self.preset_combo = QComboBox()
        self.preset_combo.addItems([
            "Random",
            "Chord Progression",
            "Bass + Melody",
            "Arpeggio",
            "Rhythmic Beat",
            "Video Game Theme",
            "Algorithmic Composer"
        ])
        self.preset_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                font-size: 12px;
                min-width: 150px;
            }
        """)
        preset_layout.addWidget(self.preset_combo)
        gen_layout.addLayout(preset_layout)
        
        # Generate button
        self.generate_btn = QPushButton("GENERATE")
        self.generate_btn.setMinimumSize(150, 40)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #8e44ad;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #9b59b6;
            }
        """)
        self.generate_btn.clicked.connect(self.generate_music)
        gen_layout.addWidget(self.generate_btn)
        
        # Melody Generator button
        self.melody_gen_btn = QPushButton("MELODY GENERATOR")
        self.melody_gen_btn.setMinimumSize(150, 40)
        self.melody_gen_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.melody_gen_btn.clicked.connect(self.open_melody_generator)
        gen_layout.addWidget(self.melody_gen_btn)
        
        layout.addLayout(gen_layout)
        
        # Export button
        self.export_btn = QPushButton("EXPORT WAV")
        self.export_btn.setMinimumSize(120, 50)
        self.export_btn.setStyleSheet("""
            QPushButton {
                background-color: #16a085;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #1abc9c;
            }
        """)
        self.export_btn.clicked.connect(self.export_audio)
        layout.addWidget(self.export_btn)
        
        # Status label - right next to buttons
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("""
            font-size: 13px;
            color: #3498db;
            padding: 5px;
            font-weight: bold;
        """)
        self.status_label.setMinimumWidth(200)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        return layout
        
    def apply_dark_theme(self):
        """Apply a dark retro theme"""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(44, 62, 80))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(236, 240, 241))
        palette.setColor(QPalette.ColorRole.Base, QColor(52, 73, 94))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(44, 62, 80))
        palette.setColor(QPalette.ColorRole.Text, QColor(236, 240, 241))
        palette.setColor(QPalette.ColorRole.Button, QColor(52, 73, 94))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(236, 240, 241))
        self.setPalette(palette)
        
    def play_note(self, frequency):
        """Play a single note"""
        self.synth.play_note(frequency, duration=0.3)
        
    def change_instrument(self, index):
        """Change the current instrument"""
        instruments = ['square', 'sawtooth', 'triangle', 'pulse', 'noise']
        self.synth.set_waveform(instruments[index])
        
    def toggle_playback(self):
        """Toggle sequencer playback"""
        if not self.is_playing:
            self.is_playing = True
            self.play_btn.setText("PAUSE")
            self.current_step = 0
            self.update_tempo()
            self.timer.start()
            self.status_label.setText("Playing...")
        else:
            self.is_playing = False
            self.play_btn.setText("PLAY")
            self.timer.stop()
            self.sequencer_canvas.set_current_step(-1)
            self.status_label.setText("Paused")
            
    def stop_playback(self):
        """Stop sequencer playback"""
        self.is_playing = False
        self.play_btn.setText("PLAY")
        self.timer.stop()
        self.current_step = 0
        self.sequencer_canvas.set_current_step(-1)
        self.status_label.setText("Stopped")
        
    def clear_pattern(self):
        """Clear all sequencer notes"""
        self.sequencer_canvas.clear_grid()
        self.stop_playback()
        self.status_label.setText("Pattern cleared")
    
    def generate_music(self):
        """Generate music using selected preset or random"""
        # Stop playback if playing
        if self.is_playing:
            self.stop_playback()
        
        # Get selected preset
        preset = self.preset_combo.currentText()
        
        # Map preset to technique
        technique_map = {
            "Random": None,
            "Chord Progression": "chord_progression",
            "Bass + Melody": "bass_and_melody",
            "Arpeggio": "arpeggio_pattern",
            "Rhythmic Beat": "rhythmic_pattern",
            "Video Game Theme": "video_game_theme",
            "Algorithmic Composer": "algorithmic"
        }
        
        selected_technique = technique_map.get(preset)
        
        # Generate pattern
        grid, settings, technique_name = self.music_gen.generate_pattern(
            self.seq_rows, 
            self.seq_steps,
            technique=selected_technique
        )
        
        # Apply to canvas
        self.sequencer_canvas.grid = grid
        self.sequencer_canvas.update()
        
        # Apply settings
        self.tempo_spin.setValue(settings["tempo"])
        self.attack_slider.setValue(settings["attack"])
        self.decay_slider.setValue(settings["decay"])
        
        # Show technique used in status label
        self.status_label.setText(f"Generated: {technique_name}")
    
    def open_melody_generator(self):
        """Open the melody generator window"""
        from gui.melody_generator_window import MelodyGeneratorWindow
        dialog = MelodyGeneratorWindow(self)
        if dialog.exec():
            # Apply generated melody curve points
            melody_points = dialog.get_melody_points()
            self.sequencer_canvas.set_melody_points(melody_points)
            self.status_label.setText(f"Melody curve applied! ({len(melody_points)} points)")
    
    def export_audio(self):
        """Export the current pattern to WAV file"""
        # Check if there's anything to export
        has_notes = any(self.sequencer_canvas.is_note_at(row, col) 
                       for row in range(self.seq_rows) 
                       for col in range(self.seq_steps))
        
        if not has_notes:
            self.status_label.setText("Nothing to export! Draw a pattern first.")
            return
        
        # Show loop count dialog
        loop_count = self._show_export_dialog()
        if loop_count is None:
            return
        
        # Open save dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Audio",
            "retro_music.wav",
            "WAV Files (*.wav)"
        )
        
        if not file_path:
            return
        
        # Stop playback if playing
        was_playing = self.is_playing
        if self.is_playing:
            self.stop_playback()
        
        self.status_label.setText("Rendering audio...")
        
        # Render the full pattern
        try:
            audio_data = self._render_pattern(loop_count)
            
            # Save to WAV file
            from scipy.io import wavfile
            wavfile.write(file_path, self.synth.sample_rate, audio_data)
            
            filename = os.path.basename(file_path)
            self.status_label.setText(f"Exported: {filename}")
            
            # Show "Locate File" option
            self._show_locate_dialog(file_path)
            
        except Exception as e:
            self.status_label.setText(f"Export failed: {str(e)}")
        
        # Resume playback if it was playing
        if was_playing:
            self.toggle_playback()
    
    def _show_export_dialog(self):
        """Show dialog to choose loop count"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Export Options")
        dialog.setFixedSize(300, 150)
        
        layout = QVBoxLayout()
        
        # Loop count selection
        loop_layout = QHBoxLayout()
        loop_layout.addWidget(QLabel("Loop count:"))
        
        loop_spin = QSpinBox()
        loop_spin.setMinimum(1)
        loop_spin.setMaximum(10)
        loop_spin.setValue(2)
        loop_layout.addWidget(loop_spin)
        
        layout.addLayout(loop_layout)
        
        # Info label
        info_label = QLabel("Choose how many times to repeat the pattern.\n(2 loops recommended)")
        info_label.setStyleSheet("font-size: 11px; color: #7f8c8d; padding: 10px;")
        layout.addWidget(info_label)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            return loop_spin.value()
        return None
    
    def _show_locate_dialog(self, file_path):
        """Show dialog to locate the exported file"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Export Complete")
        dialog.setFixedSize(350, 120)
        
        layout = QVBoxLayout()
        
        # Success message
        msg = QLabel(f"Successfully exported:\n{os.path.basename(file_path)}")
        msg.setStyleSheet("font-size: 12px; padding: 10px;")
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(msg)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        locate_btn = QPushButton("Show in Folder")
        locate_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        locate_btn.clicked.connect(lambda: self._open_file_location(file_path))
        locate_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(locate_btn)
        
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        close_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        dialog.setLayout(layout)
        
        dialog.exec()
    
    def _open_file_location(self, file_path):
        """Open file explorer and select the file"""
        if platform.system() == "Windows":
            # Windows: Use explorer with /select
            subprocess.Popen(f'explorer /select,"{os.path.normpath(file_path)}"')
        elif platform.system() == "Darwin":
            # macOS: Use 'open' with -R flag
            subprocess.Popen(["open", "-R", file_path])
        else:
            # Linux: Open the containing folder
            folder = os.path.dirname(file_path)
            QDesktopServices.openUrl(QUrl.fromLocalFile(folder))
    
    def _render_pattern(self, loop_count=2):
        """Render the entire pattern to audio data"""
        bpm = self.tempo_spin.value()
        step_duration = 60.0 / bpm / 4  # Duration of one 16th note in seconds
        
        # Calculate total duration
        total_steps = self.seq_steps * loop_count
        total_duration = total_steps * step_duration
        total_samples = int(total_duration * self.synth.sample_rate)
        
        # Create output buffer
        output = np.zeros(total_samples)
        
        # Render each step
        for loop in range(loop_count):
            for step in range(self.seq_steps):
                actual_step = loop * self.seq_steps + step
                step_start_sample = int(actual_step * step_duration * self.synth.sample_rate)
                
                # Check each row for notes
                for row in range(self.seq_rows):
                    if self.sequencer_canvas.is_note_at(row, step):
                        # Check if this is the start of a note
                        is_note_start = (step == 0 or 
                                       not self.sequencer_canvas.is_note_at(row, step - 1))
                        
                        if is_note_start:
                            # Count consecutive steps
                            duration_steps = 1
                            check_step = step + 1
                            while check_step < self.seq_steps and self.sequencer_canvas.is_note_at(row, check_step):
                                duration_steps += 1
                                check_step += 1
                            
                            # Calculate note duration
                            note_duration = step_duration * duration_steps
                            
                            # Generate waveform
                            freq = self.seq_freqs[row]
                            num_samples = int(note_duration * self.synth.sample_rate)
                            wave = self.synth.generate_waveform(freq, num_samples, 0)
                            
                            # Apply envelope
                            voice = {
                                'elapsed_samples': 0,
                                'total_samples': num_samples,
                                'attack_samples': int(self.synth.attack * self.synth.sample_rate),
                                'decay_samples': int(self.synth.decay * self.synth.sample_rate),
                            }
                            wave = self.synth.apply_envelope(wave, voice)
                            
                            # Mix into output
                            end_sample = min(step_start_sample + len(wave), len(output))
                            mix_length = end_sample - step_start_sample
                            output[step_start_sample:end_sample] += wave[:mix_length] * 0.3
        
        # Normalize
        max_val = np.max(np.abs(output))
        if max_val > 0:
            output = output / max_val * 0.8  # Leave some headroom
        
        # Convert to 16-bit PCM
        output = (output * 32767).astype(np.int16)
        
        return output

        
    def update_tempo(self):
        """Update the sequencer tempo"""
        bpm = self.tempo_spin.value()
        # Calculate interval in milliseconds (16th notes)
        interval = int(60000 / bpm / 4)
        if self.is_playing:
            self.timer.setInterval(interval)
            
    def step_sequencer(self):
        """Advance one step in the sequencer"""
        # Play notes for current step - with duration based on consecutive tiles
        for row in range(self.seq_rows):
            # Check pattern layer
            if self.sequencer_canvas.is_note_at(row, self.current_step):
                # Check if this is the start of a note (previous step was empty or we're at step 0)
                is_note_start = (self.current_step == 0 or 
                                not self.sequencer_canvas.is_note_at(row, self.current_step - 1))
                
                if is_note_start:
                    # Count how many consecutive steps have this note
                    duration_steps = 1
                    check_step = self.current_step + 1
                    
                    while check_step < self.seq_steps and self.sequencer_canvas.is_note_at(row, check_step):
                        duration_steps += 1
                        check_step += 1
                    
                    # Calculate duration based on tempo
                    bpm = self.tempo_spin.value()
                    step_duration = 60.0 / bpm / 4  # Duration of one 16th note
                    total_duration = step_duration * duration_steps
                    
                    # Play the note with calculated duration
                    freq = self.seq_freqs[row]
                    self.synth.play_note(freq, duration=total_duration)
        
        # Play smooth melody with pitch interpolation (FL Studio style!)
        if len(self.sequencer_canvas.melody_points) >= 2:
            # Get interpolated pitch at current step
            melody_row = self.sequencer_canvas.get_melody_at_step(self.current_step)
            if melody_row is not None:
                # Convert continuous row to frequency with smooth interpolation
                # Interpolate between discrete frequencies
                row_floor = int(melody_row)
                row_ceil = min(row_floor + 1, self.seq_rows - 1)
                t = melody_row - row_floor
                
                # Linear interpolation in frequency space
                freq_low = self.seq_freqs[row_floor]
                freq_high = self.seq_freqs[row_ceil]
                freq = freq_low + (freq_high - freq_low) * t
                
                # Play short note for smooth melody
                bpm = self.tempo_spin.value()
                step_duration = 60.0 / bpm / 4
                self.synth.play_note(freq, duration=step_duration * 0.8)
        
        # Update canvas to show current step
        self.sequencer_canvas.set_current_step(self.current_step)
        
        # Advance to next step
        self.current_step = (self.current_step + 1) % self.seq_steps
