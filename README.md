# Woler - Wake-on-LAN Tool

A Wake-on-LAN tool with multiple interfaces:
- Command-line interface (`woler.py`)
- Tkinter GUI (`wolergui.py`)
- Curses interface (`gui.py`)
- **NEW: Modern Electron GUI with React and BlueprintJS**

## Features

- Wake up individual computers or all computers at once
- Load PC list from CSV file
- Multiple interface options for different use cases
- Modern, responsive web-based GUI

## CSV Format

Your `list.csv` file should have the following format:
```csv
name,mac,ip
PC1,00:11:22:33:44:55,192.168.1.100
PC2,AA:BB:CC:DD:EE:FF,192.168.1.101
```

## Installation & Usage

### Command Line Interface
```bash
python woler.py
```

### Tkinter GUI
```bash
python wolergui.py
```

### Curses Interface
```bash
python gui.py
```

### Modern Electron GUI (NEW!)

1. **Install Node.js dependencies:**
```bash
npm install
```

2. **Run in development mode:**
```bash
npm run electron-dev
```

3. **Build for production:**
```bash
npm run electron-pack
```

## Requirements

### Python Dependencies
- wakeonlan==3.0.0
- windows-curses-2.4.0 (Windows only)

### Node.js Dependencies (for Electron GUI)
- React 18
- BlueprintJS 5
- Electron 25
- wakeonlan (Node.js version)

## Features of the Electron GUI

- **Modern UI**: Clean, professional interface using BlueprintJS
- **Responsive Design**: Works on different screen sizes
- **Real-time Feedback**: Loading states and success/error messages
- **Easy to Use**: Simple click-to-wake interface
- **Cross-platform**: Works on Windows, macOS, and Linux

## File Structure

```
woler/
├── woler.py          # Command-line interface
├── wolergui.py       # Tkinter GUI
├── gui.py           # Curses interface
├── list.csv         # PC configuration file
├── package.json     # Node.js dependencies
├── public/
│   ├── electron.js  # Electron main process
│   └── index.html   # HTML template
└── src/
    ├── index.js     # React entry point
    └── App.js       # Main React component
```

