# Desktop Entry Creator

Desktop Entry Creator is a modern, user-friendly GUI application for creating and editing `.desktop` files on Linux. It is built with Python and PyQt5, providing a streamlined way to generate, load, and save application launchers for your desktop environment.

## Features

- **Create new .desktop files** with all standard fields
- **Edit existing .desktop files** with a simple interface
- **Load and save** entries to user, system, or custom directories
- **Modern, dark-themed UI** inspired by the Nord color palette
- **Icon preview** and easy icon selection
- **Support for Exec parameters** and desktop entry types
- **Set categories, StartupWMClass, and other advanced options**
- **Mark entries as hidden or terminal-based**

## Screenshots

![Screenshot](logo.png)

## Requirements

- Python 3.6+
- PyQt5

## Installation

1. Clone this repository:

   ```bash
   git clone <repo-url>
   cd DesktopEntryCreator
   ```

2. Install dependencies:

   ```bash
   pip install PyQt5
   ```

## Usage

Run the application with:

```bash
python3 app.py
```

- Use the **Load Desktop Entry** button to open and edit existing `.desktop` files.
- Fill in the fields and use the **Save** buttons to write your entry to the desired location.
- The application will make the file executable automatically.

## Notes

- Saving to system directories (e.g., `/usr/share/applications/`) may require root permissions.
- The icon preview supports both file paths and icon theme names.

## License

MIT License

---

*Created by eurionyx, 2025.*
