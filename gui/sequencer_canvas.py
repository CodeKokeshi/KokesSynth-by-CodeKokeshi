"""
Canvas-based sequencer for drawing notes freely
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush


class SequencerCanvas(QWidget):
    """Canvas widget for drawing sequencer patterns"""
    
    def __init__(self, rows=8, steps=16, parent=None):
        super().__init__(parent)
        self.rows = rows
        self.steps = steps
        
        # Grid state - 2D array of booleans
        self.grid = [[False for _ in range(steps)] for _ in range(rows)]
        
        # Drawing state
        self.is_drawing = False
        self.draw_mode = True  # True = add notes, False = erase notes
        
        # Colors
        self.bg_color = QColor(52, 73, 94)
        self.grid_color = QColor(44, 62, 80)
        self.note_color = QColor(231, 76, 60)
        self.playing_color = QColor(243, 156, 18)
        self.hover_color = QColor(52, 152, 219)
        
        # Playback
        self.current_step = -1
        
        # Mouse tracking
        self.setMouseTracking(True)
        self.hover_cell = None
        
        # Minimum size - taller to fit more rows
        self.setMinimumSize(700, 380)
        
    def get_cell_size(self):
        """Calculate cell size based on widget size"""
        width = self.width() - 60  # Reserve space for labels
        height = self.height()
        
        cell_width = width // self.steps
        cell_height = height // self.rows
        
        return cell_width, cell_height
    
    def get_cell_at_pos(self, x, y):
        """Get the grid cell at the given position"""
        cell_width, cell_height = self.get_cell_size()
        
        # Account for label offset
        x_offset = 50
        
        if x < x_offset:
            return None, None
            
        col = (x - x_offset) // cell_width
        row = y // cell_height
        
        if 0 <= row < self.rows and 0 <= col < self.steps:
            return row, col
        return None, None
    
    def mousePressEvent(self, event):
        """Handle mouse press"""
        if event.button() == Qt.MouseButton.LeftButton:
            row, col = self.get_cell_at_pos(event.pos().x(), event.pos().y())
            if row is not None and col is not None:
                # Toggle the cell
                self.grid[row][col] = not self.grid[row][col]
                self.draw_mode = self.grid[row][col]
                self.is_drawing = True
                self.update()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move"""
        row, col = self.get_cell_at_pos(event.pos().x(), event.pos().y())
        
        # Update hover cell
        if row is not None and col is not None:
            self.hover_cell = (row, col)
        else:
            self.hover_cell = None
        
        # Drawing mode
        if self.is_drawing and event.buttons() & Qt.MouseButton.LeftButton:
            if row is not None and col is not None:
                self.grid[row][col] = self.draw_mode
                self.update()
        else:
            self.update()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_drawing = False
    
    def paintEvent(self, event):
        """Paint the sequencer grid"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        cell_width, cell_height = self.get_cell_size()
        x_offset = 50
        
        # Note labels - matches keyboard layout (A6 to C4)
        note_labels = ['A6', 'G6', 'E6', 'D6', 'C6', 'A5', 'G5', 'E5', 'D5', 'C5', 'A4', 'G4', 'E4', 'D4', 'C4']
        
        # Draw background
        painter.fillRect(self.rect(), self.bg_color)
        
        # Draw grid and cells
        for row in range(self.rows):
            for col in range(self.steps):
                x = x_offset + col * cell_width
                y = row * cell_height
                
                rect = QRect(x, y, cell_width - 1, cell_height - 1)
                
                # Determine cell color
                if self.current_step == col and self.grid[row][col]:
                    # Playing this note
                    painter.fillRect(rect, self.playing_color)
                elif self.current_step == col:
                    # Current step but no note
                    painter.fillRect(rect, self.hover_color.darker(150))
                elif self.grid[row][col]:
                    # Note present
                    painter.fillRect(rect, self.note_color)
                else:
                    # Empty cell
                    painter.fillRect(rect, self.grid_color)
                
                # Hover effect
                if self.hover_cell == (row, col) and not self.is_drawing:
                    pen = QPen(self.hover_color, 2)
                    painter.setPen(pen)
                    painter.drawRect(rect)
                else:
                    pen = QPen(self.grid_color.darker(120), 1)
                    painter.setPen(pen)
                    painter.drawRect(rect)
        
        # Draw row labels (smaller font)
        painter.setPen(QColor(236, 240, 241))
        font = painter.font()
        font.setPointSize(9)
        painter.setFont(font)
        for row in range(self.rows):
            y = row * cell_height + cell_height // 2
            rect = QRect(5, y - 12, 42, 24)
            painter.drawText(rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, note_labels[row])
    
    def set_current_step(self, step):
        """Set the currently playing step"""
        self.current_step = step
        self.update()
    
    def clear_grid(self):
        """Clear all notes"""
        self.grid = [[False for _ in range(self.steps)] for _ in range(self.rows)]
        self.update()
    
    def is_note_at(self, row, col):
        """Check if there's a note at the given position"""
        return self.grid[row][col]
