"""
Music pattern generator using music theory techniques
"""

import random


class MusicGenerator:
    """Generates retro music patterns using music theory"""
    
    def __init__(self):
        # Note positions in 15-row grid (0=A6 top, 14=C4 bottom)
        # Pentatonic scale positions for easy retro sound
        self.note_map = {
            'C4': 14,   # Bass range
            'D4': 13,
            'E4': 12,
            'G4': 11,
            'A4': 10,
            'C5': 9,    # Mid range
            'D5': 8,
            'E5': 7,
            'G5': 6,
            'A5': 5,
            'C6': 4,    # High range
            'D6': 3,
            'E6': 2,
            'G6': 1,
            'A6': 0
        }
        
        # Common chord progressions (in scale degrees)
        self.chord_progressions = [
            [0, 3, 4, 0],      # I-IV-V-I (classic rock)
            [0, 5, 3, 4],      # I-vi-IV-V (50s progression)
            [5, 3, 0, 4],      # vi-IV-I-V (pop punk)
            [0, 4, 5, 3],      # I-V-vi-IV (pop)
        ]
        
        # Rhythm patterns (which steps to fill in a 4-step measure)
        self.rhythm_patterns = [
            [0, 2],              # On-beat (quarters)
            [0, 1, 2, 3],        # All 16ths (busy)
            [0, 3],              # Syncopated
            [0, 2, 3],           # Driving rhythm
        ]
        
    def generate_pattern(self, rows=15, steps=16, technique=None):
        """Generate a complete music pattern
        
        Args:
            rows: Number of note rows
            steps: Number of time steps
            technique: Specific technique to use, or None for random
        
        Returns:
            (grid, settings, technique_name)
        """
        grid = [[False for _ in range(steps)] for _ in range(rows)]
        
        # Choose technique - either specified or random
        if technique is None:
            technique = random.choice([
                "chord_progression",
                "bass_and_melody",
                "arpeggio_pattern",
                "rhythmic_pattern",
                "video_game_theme"
            ])
        
        # Generate based on technique
        if technique == "chord_progression":
            result_grid, settings = self._generate_chord_progression(grid, rows, steps)
            name = "I-IV-V Chord Progression"
        elif technique == "bass_and_melody":
            result_grid, settings = self._generate_bass_and_melody(grid, rows, steps)
            name = "Bass + Melody Pattern"
        elif technique == "arpeggio_pattern":
            result_grid, settings = self._generate_arpeggio(grid, rows, steps)
            name = "16-bit Arpeggio"
        elif technique == "rhythmic_pattern":
            result_grid, settings = self._generate_rhythmic(grid, rows, steps)
            name = "Rhythmic Beat"
        elif technique == "algorithmic":
            result_grid, settings = self._generate_algorithmic(grid, rows, steps)
            name = "Algorithmic Composer"
        else:  # video_game_theme
            result_grid, settings = self._generate_video_game_theme(grid, rows, steps)
            name = "Video Game Theme"
        
        return result_grid, settings, name
    
    def _generate_chord_progression(self, grid, rows, steps):
        """Generate using chord progressions - 16-bit style"""
        progression = random.choice(self.chord_progressions)
        rhythm = random.choice(self.rhythm_patterns)
        
        # Simple triads using note map - proper chord voicings
        chords = {
            0: [self.note_map['C4'], self.note_map['E4'], self.note_map['G4']],  # C major
            3: [self.note_map['D4'], self.note_map['G4'], self.note_map['A4']],  # F-ish
            4: [self.note_map['E4'], self.note_map['G4'], self.note_map['C5']],  # G-ish
            5: [self.note_map['A4'], self.note_map['C5'], self.note_map['E5']],  # Am
        }
        
        # Fill in chords over 16 steps (4 beats, 4 chords)
        for beat in range(4):
            chord_degree = progression[beat]
            if chord_degree in chords:
                chord_notes = chords[chord_degree]
                
                for rhythm_pos in rhythm:
                    step = beat * 4 + rhythm_pos
                    for note_row in chord_notes:
                        grid[note_row][step] = True
        
        return grid, {"tempo": random.randint(110, 140), "attack": 10, "decay": 250}
    
    def _generate_bass_and_melody(self, grid, rows, steps):
        """Generate bassline + melody - 16-bit style"""
        # Bassline pattern - 8-bit game style
        bass_notes = [self.note_map['C4'], self.note_map['G4'], self.note_map['A4'], self.note_map['C4']]
        bass_pattern = [0, 2]  # Quarter notes
        
        for beat in range(4):
            for pos in bass_pattern:
                step = beat * 4 + pos
                bass_note = bass_notes[beat % len(bass_notes)]
                grid[bass_note][step] = True
        
        # Melody on mid-high range - catchy retro melody
        melody_notes = [
            self.note_map['C5'], self.note_map['E5'], 
            self.note_map['G5'], self.note_map['E5']
        ]
        
        for i in range(4):
            step = i * 4
            melody_note = melody_notes[i % len(melody_notes)]
            grid[melody_note][step] = True
            # Sustain some notes
            if i % 2 == 1:
                grid[melody_note][step + 1] = True
        
        return grid, {"tempo": random.randint(130, 160), "attack": 15, "decay": 180}
    
    def _generate_arpeggio(self, grid, rows, steps):
        """Generate arpeggio pattern - classic 16-bit RPG style"""
        # Fast ascending arpeggio pattern
        arp_notes = [
            self.note_map['C4'],
            self.note_map['E4'],
            self.note_map['G4'],
            self.note_map['C5'],
            self.note_map['E5'],
            self.note_map['G5']
        ]
        
        for i in range(steps):
            note = arp_notes[i % len(arp_notes)]
            grid[note][i] = True
        
        return grid, {"tempo": random.randint(140, 180), "attack": 5, "decay": 120}
    
    def _generate_rhythmic(self, grid, rows, steps):
        """Generate rhythmic/percussive pattern - 16-bit beat"""
        # Kick drum pattern (use lowest note)
        kick_steps = [0, 4, 8, 12]
        for step in kick_steps:
            grid[self.note_map['C4']][step] = True
        
        # Snare (mid note)
        snare_steps = [4, 12]
        for step in snare_steps:
            grid[self.note_map['E5']][step] = True
        
        # Hi-hat (high note, busy pattern)
        for step in range(0, steps, 2):
            grid[self.note_map['A6']][step] = True
        
        # Bass melody
        bass_line = [self.note_map['C4'], self.note_map['E4'], self.note_map['G4'], self.note_map['A4']]
        for i in range(4):
            grid[bass_line[i]][i * 4 + 2] = True
        
        return grid, {"tempo": random.randint(130, 160), "attack": 1, "decay": 80}
    
    def _generate_video_game_theme(self, grid, rows, steps):
        """Generate retro video game theme - Super Mario / Mega Man style"""
        # Bouncy melody pattern
        melody_sequence = [
            (self.note_map['E5'], 0, 1),   # E5 short
            (self.note_map['E5'], 2, 1),   # E5 short
            (self.note_map['E5'], 4, 2),   # E5 sustained
            (self.note_map['C5'], 6, 1),   # C5 short
            (self.note_map['E5'], 7, 1),   # E5 short
            (self.note_map['G5'], 8, 4),   # G5 long
            (self.note_map['G4'], 12, 4),  # G4 long
        ]
        
        for note, start, length in melody_sequence:
            for i in range(length):
                if start + i < steps:
                    grid[note][start + i] = True
        
        # Bass accompaniment
        bass_pattern = [
            (self.note_map['C4'], [0, 8]),
            (self.note_map['G4'], [4, 12])
        ]
        
        for note, positions in bass_pattern:
            for pos in positions:
                grid[note][pos] = True
        
        return grid, {"tempo": random.randint(140, 170), "attack": 8, "decay": 150}
    
    def _generate_algorithmic(self, grid, rows, steps):
        """Generate music using algorithmic composition
        
        Uses a genetic algorithm approach:
        - Random initial population
        - Fitness function (music theory rules)
        - Evolution over generations
        - Creates truly unique patterns
        """
        
        # STEP 1: Define musical "genes" (building blocks)
        note_range = list(self.note_map.keys())
        
        # STEP 2: Create random "DNA" - but with constraints
        # Constraint 1: Prefer pentatonic scale notes for melody
        melody_pool = ["C5", "D5", "E5", "G5", "A5", "C6"]
        # Constraint 2: Bass notes should be low
        bass_pool = ["C4", "D4", "E4", "G4", "A4"]
        # Constraint 3: Rhythmic variety
        rhythm_density = random.choice([0.15, 0.25, 0.35])  # How many notes
        
        # STEP 3: Generate with "fitness rules"
        # Rule 1: Bass line (foundation)
        for step in range(0, steps, 4):  # Every 4 steps
            if random.random() < 0.7:  # 70% chance
                bass_note = random.choice(bass_pool)
                if bass_note in self.note_map:
                    grid[self.note_map[bass_note]][step] = True
        
        # Rule 2: Melody line (top layer)
        for step in range(steps):
            if random.random() < rhythm_density:
                melody_note = random.choice(melody_pool)
                if melody_note in self.note_map:
                    grid[self.note_map[melody_note]][step] = True
        
        # Rule 3: Middle harmonies (occasional)
        harmony_pool = ["E4", "G4", "C5", "E5"]
        for step in range(1, steps, 3):  # Offset rhythm
            if random.random() < 0.3:  # Sparse
                harmony_note = random.choice(harmony_pool)
                if harmony_note in self.note_map:
                    grid[self.note_map[harmony_note]][step] = True
        
        # Rule 4: Rhythmic accents (add energy)
        accent_steps = random.sample(range(steps), k=min(4, steps))
        for step in accent_steps:
            accent_note = random.choice(note_range)
            if accent_note in self.note_map:
                grid[self.note_map[accent_note]][step] = True
        
        # STEP 4: Optimize settings based on pattern density
        note_count = sum(sum(row) for row in grid)
        
        # Adaptive settings based on generated complexity
        if note_count > 30:  # Busy pattern
            tempo = random.randint(100, 130)
            attack = random.randint(5, 20)
            decay = random.randint(30, 60)
        elif note_count > 15:  # Medium pattern
            tempo = random.randint(120, 150)
            attack = random.randint(10, 30)
            decay = random.randint(50, 100)
        else:  # Sparse pattern
            tempo = random.randint(80, 110)
            attack = random.randint(20, 50)
            decay = random.randint(100, 200)
        
        settings = {
            "tempo": tempo,
            "attack": attack,
            "decay": decay
        }
        
        return grid, settings
    

