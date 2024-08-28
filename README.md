# Command Control Application

This is a GUI-based application built using PyQt5 that allows you to execute and manage system commands easily. The application provides a simple interface to run commands, and it also allows you to manage a list of commands with tags for quick access.

## Features

- **Execute Commands**: Run system commands directly from the application.
- **Tag Management**: Add, delete, and update tags associated with commands for easy reuse.
- **Frameless Window**: The application window is frameless with custom drag functionality.
- **Hotkeys**: Use `Esc` to close the application and `F4` to open settings.

## Requirements

- Python 3.x
- PyQt5
- Windows OS (utilizes Windows Registry)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/command-control.git
   cd command-control
   ```

2. **Install dependencies:**

   Install the required Python packages using `pip`:

   ```bash
   pip install PyQt5
   ```

3. **Ensure that the `RegFunctions` module is available:**

   The application depends on a module named `RegFunctions`. Ensure that this module is in your working directory or installed.

## Usage

1. **Run the Application:**

   Navigate to the directory where the script is located and run:

   ```bash
   python main.py
   ```
   Or Download the Binaries
   
3. **Execute a Command:**

   - Type your command in the text box and press `Enter` to execute it.

4. **Manage Tags:**

   - **Open Settings:** Press `F4` or access the settings from the interface to manage your command tags.
   - **Add a Tag:** Click on the "Add Tag" button in the settings window, fill in the tag name and path, and save.
   - **Delete a Tag:** Select a tag from the list and click "Delete Tag".
   - **Amend a Tag:** Double-click on a tag to modify its name or path.

5. **Drag the Window:**

   - Click and drag anywhere on the window to move it around the screen.

6. **Close the Application:**

   - Press `Esc` or close the window to exit the application.


## Troubleshooting

- Ensure that Python 3.x and PyQt5 are correctly installed.
- Make sure the `RegFunctions` module is accessible in your environment.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or raise an Issue on GitHub.
