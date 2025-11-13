# 🎵 Melody Generator Feature - Kokesynth

## Overview
Added a dual-layer sequencer system with pattern + melody layers that can be mixed together!

## What's New

### ✨ Features Added

1. **Melody Generator Window** 🪟
   - Opens via "MELODY GENERATOR" button (red button next to GENERATE)
   - Popup dialog with multiple interpolation types
   - Parameters: note count, pitch range, density
   - Apply or cancel generated melodies

2. **Dual-Layer Canvas** 🎨
   - **Pattern Layer** (Green) - Your main 16-bit patterns
   - **Melody Layer** (Red/Orange) - Generated or hand-drawn melodies
   - **Mixed Notes** (Yellow) - When both layers have notes on same cell
   - Both layers play simultaneously during playback!

3. **Multiple Input Methods** 🖱️
   - **Left-click**: Draw pattern notes (green)
   - **Right-click**: Draw melody notes (red)
   - **Ctrl+Click**: Also draws melody notes (red)
   - **Drag**: Works with all input methods!

4. **7 Interpolation Types** 📊
   - **Linear**: Straight line between key points
   - **Cubic**: Smooth curved interpolation
   - **Step (Staircase)**: Holds each note until next key point
   - **Wave (Sine)**: Sine wave pattern across pitch range
   - **Random Walk**: Wanders randomly within range
   - **Arpeggio Up**: Ascending pattern
   - **Arpeggio Down**: Descending pattern

5. **Customizable Parameters** ⚙️
   - **Note Count**: 2-16 key points for interpolation
   - **Pitch Range**: Low (Bass), Mid (Melody), High (Lead), Full Range
   - **Density**: 10%-100% note placement probability

## How to Use

### Method 1: Generate Melody
1. Click **"MELODY GENERATOR"** button
2. Choose interpolation type (e.g., "Linear", "Wave")
3. Set note count (how many key points)
4. Select pitch range (Low/Mid/High/Full)
5. Adjust density slider (how many notes)
6. Click **"GENERATE MELODY"**
7. Preview the count in info label
8. Click **"Apply Melody"** to add to sequencer
9. Red/orange notes appear on canvas!

### Method 2: Draw Melody Manually
1. **Right-click** on canvas cells to place melody notes
2. Or hold **Ctrl + Left-click** to draw melody
3. **Drag** while right-clicking to draw longer sustained notes
4. Melody notes appear in red/orange color

### Method 3: Mix Both
1. Use **"GENERATE"** button for pattern presets (green notes)
2. Use **"MELODY GENERATOR"** for melody overlay (red notes)
3. Or hand-draw patterns (left-click) and melodies (right-click)
4. Notes stack: Pattern + Melody = Yellow mixed notes!

## Visual Guide

### Canvas Colors
- **Dark Gray**: Empty cell
- **Green**: Pattern note (left-click)
- **Red/Orange**: Melody note (right-click or Ctrl+click)
- **Yellow**: Both pattern AND melody on same cell
- **Orange Glow**: Currently playing step
- **Blue Border**: Hover effect

### UI Elements
- **GENERATE**: Creates full 16-bit patterns (chord, bass, arpeggio, etc.)
- **MELODY GENERATOR**: Opens melody creation dialog (red button)
- **CLEAR**: Removes ALL notes (both pattern and melody layers)
- Help text shows: "Left-click: Pattern (Green) | Right-click: Melody (Red) | Ctrl+Click: Melody"

## Technical Details

### File Structure
```
gui/
├── main_window.py              # Added melody_gen_btn, open_melody_generator()
├── sequencer_canvas.py         # Added melody_grid, dual-layer rendering
└── melody_generator_window.py  # NEW! Melody generation dialog
```

### Key Changes
1. **SequencerCanvas**: Added `melody_grid` (15×16 boolean array)
2. **Mouse Events**: Added right-click and Ctrl+click for melody editing
3. **Paint Event**: Renders both layers with color mixing
4. **Step Sequencer**: Plays both pattern and melody notes each step
5. **Clear Function**: Clears both layers

### Algorithm Notes
- **Linear/Cubic**: Standard interpolation math
- **Step**: Hold note until next key point
- **Wave**: `y = mid + amplitude * sin(step * 2π / steps)`
- **Random Walk**: Current position ± 1, clamped to range
- **Arpeggio**: Cycle through notes in range sequentially
- **Density**: Probability filter for each step

## Examples

### Example 1: Bass + Melody
1. Generate "Bass + Melody" preset → Green bass pattern
2. Open Melody Generator → Set "High (Lead)" range
3. Choose "Linear" interpolation, 8 notes, 70% density
4. Generate and apply → Red melody on top!
5. Play → Hear bass + lead melody together

### Example 2: Video Game Theme + Wave
1. Generate "Video Game Theme" → Green bouncy pattern
2. Open Melody Generator → Set "Mid (Melody)" range
3. Choose "Wave (Sine)" interpolation, 50% density
4. Generate and apply → Wavy counter-melody!
5. Export as WAV → Save your creation

### Example 3: Hand-Drawn Harmony
1. Left-click drag: Create chord pattern (rows 5-7, step 0-4)
2. Right-click drag: Add melody line (rows 10-12, step 0-8)
3. Left-click drag: Add bass (rows 0-2, step 0-15)
4. Play → Full arrangement with bass, chords, melody!

## Tips & Tricks

### For Best Results
- **Low density (20-40%)** for sparse melodic lines
- **High density (70-90%)** for sustained notes
- **Wave interpolation** works great for ambient melodies
- **Arpeggio** perfect for video game style leads
- **Random Walk** creates unpredictable but musical phrases
- **Mix ranges**: Bass pattern + High melody = classic combo

### Workflow Tips
1. Start with preset pattern (GENERATE button)
2. Add melody on top (MELODY GENERATOR)
3. Fine-tune by hand (right-click individual notes)
4. Adjust tempo/attack/decay for feel
5. Export when satisfied!

### Creative Ideas
- Generate multiple melodies, keep the best one
- Use "Step" interpolation for retro staccato effect
- Combine "Bass + Melody" preset with "Wave" generator
- Draw rhythm pattern, generate melodic overlay
- Try "Full Range" for chaotic wild melodies!

## Future Enhancements (Potential)
- [ ] More interpolation types (exponential, logarithmic)
- [ ] Melody layer volume control
- [ ] Different waveforms for melody vs pattern
- [ ] Melody layer solo/mute buttons
- [ ] Copy melody to pattern layer
- [ ] Reverse/transpose melody tools
- [ ] Save/load melody presets separately

---

**Created by:** CodeKokeshi (Kokeshi Aikawa)  
**Version:** 1.1.0 - Melody Generator Update  
**Date:** November 13, 2025
