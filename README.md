# � Kokesynth

<div align="center">

**A 16-bit retro audio synthesizer with sandbox-style music creation**

*Create chiptune music without music knowledge - just click, drag, and generate!*

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.4+-green.svg)](https://pypi.org/project/PyQt6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## ✨ Features

### 🎹 Interactive Keyboard
- **15 pentatonic notes** (C4 to A6) - click to play instantly
- **Real-time audio playback** with optimized voice mixing
- No music theory required!

### 🎨 Canvas-Based Sequencer
- **Click and drag** to draw musical notes
- **15 rows × 16 steps** pattern grid
- Visual feedback with hover effects
- Playback position indicator

### 🎛️ 5 Retro Waveforms
- **Square Wave** - Classic 8-bit NES sound
- **Sawtooth Wave** - Buzzy retro arcade feel
- **Triangle Wave** - Smooth Game Boy vibes
- **Pulse Wave** - Atari-style depth
- **Noise** - Perfect for drums and percussion

### 🤖 Music Generation
Choose from **7 generation modes**:
- **Random** - Picks any technique randomly
- **Chord Progression** - I-IV-V-I patterns
- **Bass + Melody** - 8-bit game style with bassline
- **Arpeggio** - Classic RPG ascending patterns
- **Rhythmic Beat** - Kick/snare/hi-hat drums
- **Video Game Theme** - Super Mario/Mega Man style
- **Algorithmic Composer** - Genetic algorithm creates unique patterns every time!

### 🎚️ Sound Shaping
- **Attack**: 0-200ms (how quickly sound starts)
- **Decay**: 0-500ms (how quickly it fades)
- **Tempo**: 60-200 BPM with live adjustment

### 💾 Export & Share
- **Export to WAV** (16-bit, 44.1kHz)
- **Loop selection** (1-10 times)
- **Locate file** button after export
- Status feedback for all actions

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13+ (or 3.8+)
- Windows/macOS/Linux

### Installation

```bash
# Clone the repository
git clone https://github.com/CodeKokeshi/Kokesynth.git
cd Kokesynth

# Create virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

---

## 🎮 How to Use

### 1️⃣ Playing Notes
- Click any **keyboard button** to hear a note instantly
- Select different **waveforms** from the dropdown
- Adjust **Attack** and **Decay** sliders for different sound envelopes

### 2️⃣ Creating Patterns
- **Click and drag** on the sequencer canvas to draw notes
- Each **row** = different note pitch
- Each **column** = time step (16 steps total)
- Click **PLAY** to hear your pattern loop
- Use **PAUSE** to stop temporarily, **STOP** to reset
- **CLEAR** removes all notes

### 3️⃣ Generating Music
- Select a **preset** from the dropdown (or "Random")
- Click **GENERATE** to create instant music
- Try **Algorithmic Composer** for unique patterns every time!

### 4️⃣ Exporting
- Click **EXPORT WAV**
- Choose **loop count** (1-10 times)
- Click **OK** to save
- Use **LOCATE FILE** to open the export folder

---

## 🎵 Tips & Tricks

### For Beginners
- Start with **"Random"** or **"Video Game Theme"** presets
- Use **slower tempos** (80-100 BPM) to hear details
- **Square wave** is the most classic 8-bit sound
- Notes are pentatonic - most combinations sound good!

### For Experimenters
- Try **"Algorithmic Composer"** multiple times for inspiration
- Layer **bass** (low rows) + **melody** (high rows)
- Use **noise** for percussion on beat 1, 5, 9, 13
- Adjust **decay** low (30-60ms) for staccato, high (200-300ms) for sustained

### For Advanced Users
- Create **call-and-response** patterns (4 steps melody, 4 steps rest, repeat)
- Use **pulse wave** for sub-bass (bottom 3 rows)
- Mix **attack** settings: fast attack (5-10ms) for punchy, slow (40-60ms) for pads
- Export multiple loops and **layer in DAW** for full tracks

---

## 📦 Dependencies

```
PyQt6>=6.4.0
numpy>=1.24.0
sounddevice>=0.4.6
scipy>=1.10.0
```

---

## 🗂️ Project Structure

```
Kokesynth/
├── main.py                 # Entry point
├── gui/
│   ├── main_window.py      # Main UI window
│   └── sequencer_canvas.py # Custom canvas widget
├── audio/
│   ├── synth_engine.py     # Audio synthesis engine
│   └── music_generator.py  # AI pattern generation
├── requirements.txt        # Dependencies
├── README.md              # You are here!
└── FUTURE_PLANS.md        # Roadmap
```

---

## 🛣️ Roadmap

See [FUTURE_PLANS.md](FUTURE_PLANS.md) for detailed future features:
- 🎼 Advanced melody generator with interpolation
- 🎚️ Effects chain (reverb, delay, filters)
- 💾 MIDI import/export
- 🎨 Custom themes
- 🤖 Enhanced AI composer with learning
- And much more!

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features (add to [FUTURE_PLANS.md](FUTURE_PLANS.md))
- Submit pull requests

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

## 👨‍💻 Author

**CodeKokeshi** (Kokeshi Aikawa)

- Other projects: [Kokeshprite](https://github.com/CodeKokeshi/Kokeshprite) (Aseprite in PyQt6)
- Style: Retro tools with modern implementation

---

## 🎉 Acknowledgments

- Inspired by classic 8-bit/16-bit game consoles
- Built with love for retro gaming music
- Special thanks to the chiptune community

---

<div align="center">

**Have fun creating retro music! �✨**

*No music theory required - just pure sandbox creativity!*

</div>
