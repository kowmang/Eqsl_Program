import sys
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QByteArray

class ImageViewerDialog(QDialog):
    """Displays a list of images (as QByteArray) in a clickable gallery."""
    def __init__(self, image_data_list: list[QByteArray], parent=None):
        super().__init__(parent)
        self.setWindowTitle("eQSL Gallery View")
        self.image_data_list = image_data_list
        self.current_index = 0
        
        # --- UI Elements ---
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setScaledContents(True)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.image_label.setMinimumSize(700, 400)
        
        self.prev_button = QPushButton("<- Back")
        self.next_button = QPushButton("Next ->")
        self.counter_label = QLabel()
        self.counter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # --- Layouts ---
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.counter_label)
        button_layout.addWidget(self.next_button)
        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(button_layout)
        
        # --- Connections ---
        self.prev_button.clicked.connect(self.show_previous)
        self.next_button.clicked.connect(self.show_next)
        
        self.update_viewer()

    def update_viewer(self):
        """Loads the current image and updates the controls."""
        if not self.image_data_list:
            self.image_label.setText("No images available.")
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)
            return

        # Load QPixmap from QByteArray
        pixmap = QPixmap()
        blob_data = self.image_data_list[self.current_index]
        
        if pixmap.loadFromData(blob_data):
            # Scales the image to the size of the label
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.size(), 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            ))
        else:
            self.image_label.setText("Load error (Invalid image format).")
        
        # Update button status and counter
        self.prev_button.setEnabled(self.current_index > 0)
        self.next_button.setEnabled(self.current_index < len(self.image_data_list) - 1)
        self.counter_label.setText(f"Image {self.current_index + 1} of {len(self.image_data_list)}")

    def show_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_viewer()

    def show_next(self):
        if self.current_index < len(self.image_data_list) - 1:
            self.current_index += 1
            self.update_viewer()

    def resizeEvent(self, event):
        """Ensures the image scales when the window size changes."""
        super().resizeEvent(event)
        self.update_viewer()