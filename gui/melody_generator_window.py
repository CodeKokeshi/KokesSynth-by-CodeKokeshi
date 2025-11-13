"""
Melody Generator Window for Kokesynth
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QComboBox, QSpinBox, QGroupBox, QSlider)
from PyQt6.QtCore import Qt
import random
import numpy as np


class MelodyGeneratorWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Melody Generator")
        self.setModal(True)
        self.setMinimumSize(500, 400)
        
        self.melody_points = []  # List of (step, row) tuples
        self.rows = 15
        self.steps = 16
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("🎵 Melody Generator")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Interpolation type
        interp_group = QGroupBox("Interpolation Type")
        interp_layout = QVBoxLayout()
        
        self.interp_combo = QComboBox()
        self.interp_combo.addItems([
            "Linear",
            "Cubic",
            "Step (Staircase)",
            "Wave (Sine)",
            "Random Walk",
            "Arpeggio Up",
            "Arpeggio Down"
        ])
        interp_layout.addWidget(self.interp_combo)
        interp_group.setLayout(interp_layout)
        layout.addWidget(interp_group)
        
        # Melody parameters
        params_group = QGroupBox("Parameters")
        params_layout = QVBoxLayout()
        
        # Note count
        note_layout = QHBoxLayout()
        note_layout.addWidget(QLabel("Note Count:"))
        self.note_count_spin = QSpinBox()
        self.note_count_spin.setRange(2, 16)
        self.note_count_spin.setValue(8)
        note_layout.addWidget(self.note_count_spin)
        params_layout.addLayout(note_layout)
        
        # Pitch range
        range_layout = QHBoxLayout()
        range_layout.addWidget(QLabel("Pitch Range:"))
        self.range_combo = QComboBox()
        self.range_combo.addItems([
            "Low (Bass)",
            "Mid (Melody)",
            "High (Lead)",
            "Full Range"
        ])
        self.range_combo.setCurrentIndex(1)
        range_layout.addWidget(self.range_combo)
        params_layout.addLayout(range_layout)
        
        # Density
        density_layout = QHBoxLayout()
        density_layout.addWidget(QLabel("Density:"))
        self.density_slider = QSlider(Qt.Orientation.Horizontal)
        self.density_slider.setRange(1, 10)
        self.density_slider.setValue(5)
        density_layout.addWidget(self.density_slider)
        self.density_label = QLabel("50%")
        density_layout.addWidget(self.density_label)
        self.density_slider.valueChanged.connect(
            lambda v: self.density_label.setText(f"{v*10}%")
        )
        params_layout.addLayout(density_layout)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        # Generate button
        self.generate_btn = QPushButton("GENERATE MELODY")
        self.generate_btn.setMinimumHeight(50)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.generate_btn.clicked.connect(self.generate_melody)
        layout.addWidget(self.generate_btn)
        
        # Preview info
        self.info_label = QLabel("Click Generate to create melody")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("padding: 10px; color: #7f8c8d;")
        layout.addWidget(self.info_label)
        
        # Dialog buttons
        buttons_layout = QHBoxLayout()
        
        self.apply_btn = QPushButton("Apply Melody")
        self.apply_btn.setEnabled(False)
        self.apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.apply_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(self.apply_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
    
    def generate_melody(self):
        """Generate melody based on selected parameters"""
        # Clear previous melody
        self.melody_points = []
        
        # Get parameters
        interp_type = self.interp_combo.currentText()
        note_count = self.note_count_spin.value()
        pitch_range = self.range_combo.currentText()
        
        # Define pitch range
        if pitch_range == "Low (Bass)":
            min_row, max_row = 0, 5
        elif pitch_range == "Mid (Melody)":
            min_row, max_row = 5, 10
        elif pitch_range == "High (Lead)":
            min_row, max_row = 10, 14
        else:  # Full Range
            min_row, max_row = 0, 14
        
        # Generate key points (control points for the curve)
        for i in range(note_count):
            step = i * (self.steps - 1) / (note_count - 1)
            row = random.uniform(min_row, max_row)  # Use float for smooth curves
            self.melody_points.append((step, row))
        
        # Apply interpolation to create smooth curve
        if interp_type == "Cubic":
            self.melody_points = self._smooth_cubic(self.melody_points)
        elif interp_type == "Wave (Sine)":
            self.melody_points = self._generate_wave(min_row, max_row)
        elif interp_type == "Random Walk":
            self.melody_points = self._generate_random_walk(min_row, max_row)
        elif interp_type == "Arpeggio Up":
            self.melody_points = self._generate_arpeggio(min_row, max_row, "up")
        elif interp_type == "Arpeggio Down":
            self.melody_points = self._generate_arpeggio(min_row, max_row, "down")
        # Linear and Step use the key points as-is
        
        # Update UI
        self.info_label.setText(f"✓ Melody curve generated! ({len(self.melody_points)} points)")
        self.apply_btn.setEnabled(True)
    
    def _interpolate_linear(self, key_points, density):
        """Linear interpolation between key points"""
        for i in range(len(key_points) - 1):
            x1, y1 = key_points[i]
            x2, y2 = key_points[i + 1]
            
            steps = x2 - x1
            for step in range(steps + 1):
                if random.random() < density:
                    x = x1 + step
                    y = int(y1 + (y2 - y1) * step / steps)
                    if 0 <= x < self.steps and 0 <= y < self.rows:
                        self.melody_grid[y][x] = True
    
    def _interpolate_cubic(self, key_points, density):
        """Cubic spline interpolation"""
        if len(key_points) < 3:
            self._interpolate_linear(key_points, density)
            return
        
        x_points = [p[0] for p in key_points]
        y_points = [p[1] for p in key_points]
        
        # Simple cubic interpolation
        for step in range(self.steps):
            if random.random() < density:
                # Find surrounding points
                for i in range(len(x_points) - 1):
                    if x_points[i] <= step <= x_points[i + 1]:
                        t = (step - x_points[i]) / (x_points[i + 1] - x_points[i])
                        # Cubic easing
                        t = t * t * (3 - 2 * t)
                        y = int(y_points[i] + (y_points[i + 1] - y_points[i]) * t)
                        if 0 <= y < self.rows:
                            self.melody_grid[y][step] = True
                        break
    
    def _interpolate_step(self, key_points, density):
        """Step/staircase interpolation"""
        for i in range(len(key_points)):
            x, y = key_points[i]
            # Hold each note until next key point
            if i < len(key_points) - 1:
                next_x = key_points[i + 1][0]
                for step in range(x, next_x):
                    if random.random() < density:
                        self.melody_grid[y][step] = True
            else:
                # Last note
                for step in range(x, self.steps):
                    if random.random() < density:
                        self.melody_grid[y][step] = True
    
    def _interpolate_wave(self, min_row, max_row, density):
        """Sine wave melody"""
        mid_row = (min_row + max_row) // 2
        amplitude = (max_row - min_row) // 2
        
        for step in range(self.steps):
            if random.random() < density:
                # Sine wave
                angle = step * 2 * np.pi / self.steps
                y = int(mid_row + amplitude * np.sin(angle))
                if 0 <= y < self.rows:
                    self.melody_grid[y][step] = True
    
    def _interpolate_random_walk(self, min_row, max_row, density):
        """Random walk melody"""
        current_row = (min_row + max_row) // 2
        
        for step in range(self.steps):
            if random.random() < density:
                self.melody_grid[current_row][step] = True
            
            # Random walk
            change = random.choice([-1, 0, 1])
            current_row = max(min_row, min(max_row, current_row + change))
    
    def _interpolate_arpeggio(self, min_row, max_row, density, direction="up"):
        """Arpeggio pattern"""
        if direction == "up":
            rows = list(range(min_row, max_row + 1))
        else:
            rows = list(range(max_row, min_row - 1, -1))
        
        row_idx = 0
        for step in range(self.steps):
            if random.random() < density:
                row = rows[row_idx % len(rows)]
                self.melody_grid[row][step] = True
                row_idx += 1
    
    def get_melody_points(self):
        """Return the generated melody curve points"""
        return self.melody_points
    
    def _smooth_cubic(self, points):
        """Apply cubic smoothing to points"""
        if len(points) < 3:
            return points
        # For now, just return original points (can add spline later)
        return points
    
    def _generate_wave(self, min_row, max_row):
        """Generate sine wave melody"""
        points = []
        mid_row = (min_row + max_row) / 2
        amplitude = (max_row - min_row) / 2
        
        for step in np.linspace(0, self.steps - 1, 32):  # 32 points for smooth curve
            angle = step * 2 * np.pi / self.steps
            row = mid_row + amplitude * np.sin(angle)
            points.append((step, row))
        
        return points
    
    def _generate_random_walk(self, min_row, max_row):
        """Generate random walk melody"""
        points = []
        current_row = (min_row + max_row) / 2
        
        for step in range(self.steps):
            points.append((float(step), current_row))
            # Random walk with smaller steps
            change = random.uniform(-0.5, 0.5)
            current_row = max(min_row, min(max_row, current_row + change))
        
        return points
    
    def _generate_arpeggio(self, min_row, max_row, direction):
        """Generate arpeggio pattern"""
        points = []
        rows = np.linspace(min_row, max_row, 5)  # 5 notes in arpeggio
        
        if direction == "down":
            rows = rows[::-1]
        
        for step in range(self.steps):
            row_idx = step % len(rows)
            points.append((float(step), rows[row_idx]))
        
        return points
