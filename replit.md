# Python Plugin Framework

## Overview
This is a Python CLI/TUI application with a plugin architecture. It uses `questionary` for interactive terminal menus, allowing users to select and execute different plugin modules.

## Project Structure
```
.
├── main.py              # Application entry point
├── core/
│   ├── app.py           # Main application class (MyApplication)
│   ├── util.py          # Plugin loading utilities
│   ├── Interfaces/
│   │   └── Iplugins.py  # Plugin interface definition
│   └── exepcions/
│       └── exception.py # Custom exceptions
├── plugins/
│   ├── bzhelp/          # BzHelp plugin
│   │   └── Bzhelp.py
│   └── xsales/          # Xsales plugin
│       ├── Xsales.py
│       ├── confi.py
│       ├── inputquestion.py
│       └── util.py
└── tests/               # Test directory
```

## How It Works
1. The application loads plugins dynamically from the `plugins/` directory
2. Users select a plugin using an interactive menu
3. The selected plugin's `execute()` method is called

## Running the Application
```bash
python main.py
```

## Dependencies
Key dependencies include:
- questionary - Interactive terminal prompts
- requests - HTTP library
- beautifulsoup4, lxml, pyquery - HTML/XML parsing
- pandas, openpyxl - Data manipulation and Excel files
- rich - Terminal formatting
- PyYAML - YAML configuration

## Plugin Development
Plugins should:
1. Be placed in a subdirectory under `plugins/`
2. Have a main file with the same name as the directory (capitalized)
3. Implement the `IPluging` interface with a `Plugin` class containing an `execute()` method
