#!/usr/bin/env python3

import sys
import os
import configparser
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QFormLayout, QLabel, QLineEdit, 
                             QPushButton, QComboBox, QCheckBox, QFileDialog,
                             QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap


MODERN_BLUE_STYLESHEET = """
    QMainWindow, QWidget {
        background-color: #2E3440; /* Nord Polar Night */
        color: #D8DEE9; /* Nord Snow Storm */
    }
    QLabel {
        color: #ECEFF4; /* Nord Snow Storm */
    }
    QLineEdit, QComboBox {
        background-color: #3B4252; /* Nord Polar Night */
        color: #ECEFF4;
        border: 1px solid #4C566A; /* Nord Polar Night */
        padding: 5px;
        border-radius: 4px;
    }
    QLineEdit:focus, QComboBox:focus {
        border: 1px solid #88C0D0; /* Nord Frost */
    }
    QComboBox::drop-down {
        border: none;
        width: 20px;
    }
    QComboBox::down-arrow {
        /* A simple arrow can be drawn with QStyle or use an SVG for better results */
        /* For simplicity, we'll rely on default or style-provided arrow if any */
        /* image: url(path/to/custom_arrow.svg); */
    }
    QPushButton {
        background-color: #5E81AC; /* Nord Frost */
        color: #ECEFF4;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #81A1C1; /* Nord Frost lighter */
    }
    QPushButton:pressed {
        background-color: #4C566A; /* Nord Polar Night darker */
    }
    QCheckBox {
        color: #D8DEE9;
        spacing: 5px; /* Spacing between indicator and text */
    }
    QCheckBox::indicator {
        width: 16px;
        height: 16px;
        border: 1px solid #4C566A;
        border-radius: 3px;
        background-color: #3B4252;
    }
    QCheckBox::indicator:checked {
        background-color: #5E81AC; /* Nord Frost */
        /* image: url(path/to/checkmark.svg); For a custom checkmark */
    }
    QCheckBox::indicator:unchecked {
        background-color: #3B4252;
    }
    QFormLayout {
        spacing: 10px; /* Vertical spacing */
        horizontalSpacing: 15px; /* Horizontal spacing between label and field */
    }
    #iconPreviewLabel { /* Specific ID for icon preview label styling */
        border: 1px solid #4C566A;
        background-color: #3B4252;
        min-width: 64px;
        min-height: 64px;
        max-width: 64px;
        max-height: 64px;
        color: #81A1C1; /* Text color for 'No Icon' / 'Invalid' */
    }
    QToolTip {
        background-color: #3B4252;
        color: #ECEFF4;
        border: 1px solid #4C566A;
        padding: 4px;
    }
"""


class DesktopEntryCreator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Desktop Entry Creator')
        self.setGeometry(300, 300, 600, 500)
        
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Add Load Entry button at the top
        load_button_layout = QHBoxLayout()
        self.load_entry_btn = QPushButton('Load Desktop Entry')
        self.load_entry_btn.clicked.connect(self.load_desktop_entry)
        load_button_layout.addWidget(self.load_entry_btn)
        load_button_layout.addStretch()
        main_layout.addLayout(load_button_layout)
        
        # Form layout for entry fields
        form_layout = QFormLayout()
        
        # Entry fields
        self.name_entry = QLineEdit()
        self.generic_name_entry = QLineEdit()
        self.comment_entry = QLineEdit()
        
        # Type selection
        self.type_combo = QComboBox()
        self.type_combo.addItems(['Application', 'Link', 'Directory'])
        
        # Executable path with browse button and parameter options
        exec_layout = QHBoxLayout()
        self.exec_entry = QLineEdit()
        self.exec_browse_btn = QPushButton('Browse')
        self.exec_browse_btn.clicked.connect(self.browse_executable)
        self.exec_param_combo = QComboBox()
        self.exec_param_combo.addItems(['None', '%f', '%F', '%u', '%U', '%i', '%c', '%k'])
        self.exec_param_combo.setToolTip(
            "%f: Single file path\n"
            "%F: Multiple file paths\n"
            "%u: Single URL\n"
            "%U: Multiple URLs\n"
            "%i: Icon option\n"
            "%c: Name field\n"
            "%k: Desktop file path"
        )
        exec_layout.addWidget(self.exec_entry)
        exec_layout.addWidget(self.exec_browse_btn)
        exec_layout.addWidget(QLabel("Exec Parameter:"))
        exec_layout.addWidget(self.exec_param_combo)
        
        # Icon path with browse button and preview
        icon_layout = QHBoxLayout()
        self.icon_entry = QLineEdit()
        self.icon_entry.textChanged.connect(self._update_icon_preview)
        self.icon_browse_btn = QPushButton('Browse')
        self.icon_browse_btn.clicked.connect(self.browse_icon)
        
        self.icon_preview_label = QLabel()
        self.icon_preview_label.setObjectName("iconPreviewLabel")
        self.icon_preview_label.setFixedSize(64, 64)
        self.icon_preview_label.setAlignment(Qt.AlignCenter)
        
        icon_layout.addWidget(self.icon_entry)
        icon_layout.addWidget(self.icon_browse_btn)
        icon_layout.addWidget(self.icon_preview_label) # Add preview to the layout
        
        # StartupWMClass field
        self.wmclass_entry = QLineEdit()
        self.wmclass_entry.setPlaceholderText("Application class name")
        
        # Categories
        self.categories_entry = QLineEdit()
        self.categories_entry.setPlaceholderText("Utility;Development;")
        
        # Terminal option
        self.terminal_checkbox = QCheckBox()
        
        # NoDisplay option
        self.nodisplay_checkbox = QCheckBox()
        
        # Add fields to form layout
        form_layout.addRow('Name:', self.name_entry)
        form_layout.addRow('Generic Name:', self.generic_name_entry)
        form_layout.addRow('Comment:', self.comment_entry)
        form_layout.addRow('Type:', self.type_combo)
        form_layout.addRow('Executable:', exec_layout)
        form_layout.addRow('Icon:', icon_layout)
        form_layout.addRow('StartupWMClass:', self.wmclass_entry)
        form_layout.addRow('Categories:', self.categories_entry)
        form_layout.addRow('Run in Terminal:', self.terminal_checkbox)
        form_layout.addRow('Hidden from menus:', self.nodisplay_checkbox)
        
        # Save buttons
        button_layout = QHBoxLayout()
        
        self.save_user_btn = QPushButton('Save to User Directory')
        self.save_user_btn.clicked.connect(self.save_user_entry)
        
        self.save_system_btn = QPushButton('Save to System Directory')
        self.save_system_btn.clicked.connect(self.save_system_entry)
        
        self.save_custom_btn = QPushButton('Save to Custom Location')
        self.save_custom_btn.clicked.connect(self.save_custom_entry)
        
        button_layout.addWidget(self.save_user_btn)
        button_layout.addWidget(self.save_system_btn)
        button_layout.addWidget(self.save_custom_btn)
        
        # Add layouts to main layout
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        self._update_icon_preview() # Set initial state of icon preview

    def _update_icon_preview(self, text=None): # text arg from textChanged signal
        icon_path_or_name = self.icon_entry.text()

        if not icon_path_or_name:
            self.icon_preview_label.clear()
            self.icon_preview_label.setText('No Icon')
            return

        pixmap = QPixmap(icon_path_or_name) # Try as direct path first

        if pixmap.isNull(): # If direct path fails, try as theme icon
            icon = QIcon.fromTheme(icon_path_or_name)
            if not icon.isNull():
                # Request a pixmap of the label's size for best quality
                pixmap = icon.pixmap(self.icon_preview_label.size())

        if not pixmap.isNull():
            self.icon_preview_label.setPixmap(pixmap.scaled(
                self.icon_preview_label.width(),
                self.icon_preview_label.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))
        else:
            self.icon_preview_label.clear()
            self.icon_preview_label.setText('Invalid')
            
    def browse_executable(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Executable', 
                                                 os.path.expanduser('~'), 
                                                 'All Files (*)')
        if file_path:
            self.exec_entry.setText(file_path)
            
    def browse_icon(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Icon', 
                                                 os.path.expanduser('~'), 
                                                 'Images (*.png *.xpm *.jpg *.svg);;All Files (*)') # Added All Files
        if file_path:
            self.icon_entry.setText(file_path)
            # _update_icon_preview is called by textChanged signal

    def create_desktop_entry_content(self):
        content = "[Desktop Entry]\n"
        content += f"Name={self.name_entry.text()}\n"
        
        if self.generic_name_entry.text():
            content += f"GenericName={self.generic_name_entry.text()}\n"
        
        if self.comment_entry.text():
            content += f"Comment={self.comment_entry.text()}\n"
        
        content += f"Type={self.type_combo.currentText()}\n"
        
        if self.exec_entry.text():
            exec_value = self.exec_entry.text()
            param = self.exec_param_combo.currentText()
            if param != 'None':
                exec_value += f" {param}"
            content += f"Exec={exec_value}\n"
        
        if self.icon_entry.text():
            content += f"Icon={self.icon_entry.text()}\n"
            
        if self.wmclass_entry.text():
            content += f"StartupWMClass={self.wmclass_entry.text()}\n"
        
        if self.categories_entry.text():
            content += f"Categories={self.categories_entry.text()}\n"
        
        content += f"Terminal={'true' if self.terminal_checkbox.isChecked() else 'false'}\n"
        content += f"NoDisplay={'true' if self.nodisplay_checkbox.isChecked() else 'false'}\n"
        
        return content
    
    def save_user_entry(self):
        self.save_desktop_entry(os.path.expanduser('~/.local/share/applications/'))
    
    def save_system_entry(self):
        self.save_desktop_entry('/usr/share/applications/')
    
    def save_custom_entry(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if directory:
            self.save_desktop_entry(directory + '/')
    
    def save_desktop_entry(self, directory):
        if not self.name_entry.text():
            QMessageBox.warning(self, 'Missing Information', 'Name field is required.')
            return
        
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except PermissionError:
                QMessageBox.critical(self, 'Permission Error', 
                                   f'Cannot create directory: {directory}. Permission denied.')
                return
        
        filename = self.name_entry.text().lower().replace(' ', '-') + '.desktop'
        filepath = os.path.join(directory, filename)
        
        content = self.create_desktop_entry_content()
        
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            
            # Make the file executable
            os.chmod(filepath, 0o755)
            
            QMessageBox.information(self, 'Success', f'Desktop entry saved to {filepath}')
        except PermissionError:
            QMessageBox.critical(self, 'Permission Error', 
                               f'Cannot write to {filepath}. Permission denied.')
    
    def load_desktop_entry(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Open Desktop Entry', 
            os.path.expanduser('~/.local/share/applications/'),
            'Desktop Files (*.desktop);;All Files (*)'
        )
        
        if not file_path:
            return
            
        try:
            self.parse_desktop_file(file_path)
            QMessageBox.information(self, 'Success', f'Loaded desktop entry from {file_path}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load desktop entry: {str(e)}')
    
    def parse_desktop_file(self, file_path):
        config = configparser.ConfigParser()
        config.read(file_path)
        
        if 'Desktop Entry' not in config:
            raise ValueError('Invalid desktop entry file: Missing [Desktop Entry] section')
            
        desktop_entry = config['Desktop Entry']
        
        # Set basic fields
        self.name_entry.setText(desktop_entry.get('Name', ''))
        self.generic_name_entry.setText(desktop_entry.get('GenericName', ''))
        self.comment_entry.setText(desktop_entry.get('Comment', ''))
        
        # Set type
        entry_type = desktop_entry.get('Type', 'Application')
        type_index = self.type_combo.findText(entry_type)
        if type_index >= 0:
            self.type_combo.setCurrentIndex(type_index)
        
        # Set Exec path and parameter
        exec_value = desktop_entry.get('Exec', '')
        self.exec_entry.setText(exec_value)
        
        # Check for parameters in the Exec line
        for param in ['%f', '%F', '%u', '%U', '%i', '%c', '%k']:
            if param in exec_value:
                self.exec_param_combo.setCurrentText(param)
                # Remove the parameter from the exec field
                self.exec_entry.setText(exec_value.replace(param, '').strip())
                break
        else:
            # No parameter found
            self.exec_param_combo.setCurrentText('None')
        
        # Set Icon path
        self.icon_entry.setText(desktop_entry.get('Icon', ''))
        # _update_icon_preview is called by textChanged signal of icon_entry
        
        # Set StartupWMClass
        self.wmclass_entry.setText(desktop_entry.get('StartupWMClass', ''))
        
        # Set Categories
        self.categories_entry.setText(desktop_entry.get('Categories', ''))
        
        # Set checkboxes
        terminal_value = desktop_entry.get('Terminal', 'false').lower()
        self.terminal_checkbox.setChecked(terminal_value == 'true')
        
        nodisplay_value = desktop_entry.get('NoDisplay', 'false').lower()
        self.nodisplay_checkbox.setChecked(nodisplay_value == 'true')


def main():
    app = QApplication(sys.argv)
    # app.setStyle('Fusion') # Stylesheet will provide the main look and feel
    window = DesktopEntryCreator()
    window.setStyleSheet(MODERN_BLUE_STYLESHEET) # Apply the stylesheet
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
