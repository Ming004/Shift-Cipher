import sys
from pathlib import Path
import cv2
from PIL import Image
import pytesseract
import numpy as np
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor, QImage, QPixmap, QGuiApplication
from PyQt6.QtCore import Qt, QUrl
from shiftcipher import encrypt_check, encrypt_cipher, decrypt
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QSoundEffect

class CaesarCipherApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Caesar Cipher Translator")
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowIcon(QIcon("hiii.png"))  # icon

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Input Section
        input_layout = QHBoxLayout()
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter words here (at least 200 words)...")
        self.input_text.setFont(QFont("Century Gothic", 12))
        input_layout.addWidget(self.input_text)
        # Shift Selection
        shift_layout = QVBoxLayout()
        self.shift_slider = QSlider(Qt.Orientation.Horizontal)
        self.shift_slider.setRange(0, 26)
        self.shift_slider.valueChanged.connect(self.update_shift_label)
        self.shift_value = QLabel("Shift: 0")
        shift_layout.addWidget(self.shift_slider)
        shift_layout.addWidget(self.shift_value)
        # Buttons
        button_layout = QHBoxLayout()
        self.encrypt_btn = QPushButton("Encrypt", clicked=self.encrypt_text)
        self.decrypt_btn = QPushButton("Decrypt", clicked=self.decrypt_text)
        button_layout.addWidget(self.encrypt_btn)
        button_layout.addWidget(self.decrypt_btn)
        # Results
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("Results will be appear here...")
        self.result_text.setFont(QFont("Century Gothic", 12))
        # Theme and File Operations
        control_layout = QHBoxLayout()
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        self.file_btn = QPushButton("Save", clicked=self.file_operations)
        control_layout.addWidget(self.theme_combo)
        control_layout.addWidget(self.file_btn)
        self.ocr_btn = QPushButton("Import Image", clicked=self.ocr_preprocess_image)
        control_layout.addWidget(self.ocr_btn)
        self.image_preview = QLabel()
        self.layout.addWidget(self.image_preview)
        # Adding to main layout
        self.layout.addLayout(input_layout)
        self.layout.addLayout(shift_layout)
        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.result_text)
        self.layout.addLayout(control_layout)
        self.statusBar().showMessage('Version 2.0 Powered by Charles')

        # Theme setup
        self.custom_colors = {
            'background': QColor(240, 240, 240),
            'text': QColor(0, 0, 0),
            'button': QColor(220, 220, 220),
            'button_text': QColor(0, 0, 0)
        }
        self.change_theme()
    def ocr_preprocess_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open Image for OCR", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if not fname:
            return
        try:
            # Set here
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Ensure this path is correct

            # Load 
            img = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
            if img is None:
                raise ValueError("Unread ! ! !")

            # Preprocessing 
            _, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            img_bin = 255 - img_bin  # Invert the binary image for better OCR

            # Display
            qImg = QImage(img_bin.data, img_bin.shape[1], img_bin.shape[0], QImage.Format.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qImg)
            self.image_preview.setPixmap(pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))

            # Perform OCR
            text = pytesseract.image_to_string(img_bin)

            # 使用OCR结果
            self.input_text.setPlainText(text)

            QMessageBox.information(self, "Success", "successfully.")
            self.statusBar().showMessage('OCR completed', 5000)
        except Exception as e:
            error_message = f"Failed to process the image: {str(e)}"
            QMessageBox.warning(self, "Image Processing Error", error_message)
            self.statusBar().showMessage(error_message, 10000)

    def update_shift_label(self, value):
        self.shift_value.setText(f"Shift: {value}")

    def encrypt_text(self):
        raw = self.input_text.toPlainText()
        shift = self.shift_slider.value()
        check_result = encrypt_check(raw)
        if check_result == "valid....":
            encrypted = encrypt_cipher(raw, shift)
            self.result_text.setText(encrypted)
            self.statusBar().showMessage('Text encrypted', 5000)
        else:
            self.result_text.setText(check_result)
            self.statusBar().showMessage('Encryption Error: ' + check_result, 5000)

    def decrypt_text(self):
        cipher = self.input_text.toPlainText()
        result = ""
        for shift in range(26):
            decrypted = decrypt(cipher, shift)
            result += f"Shift {shift}: {decrypted}\n\n"
        self.result_text.setText(result)
        self.statusBar().showMessage('Text decrypted', 5000)

    def change_theme(self):
        if self.theme_combo.currentText() == "Dark":
            self.set_dark_theme()
        elif self.theme_combo.currentText() == "Light":
            self.set_light_theme()

    def set_light_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 250))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 255))
        palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Button, QColor(220, 220, 220))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        self.setPalette(palette)

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(10, 10, 10))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(20, 20, 20))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
        self.setPalette(palette)

    def file_operations(self):
        action, ok = QInputDialog.getItem(self, "File Operation",
                                          "Choose an action:", ["Load", "Save"], 0, False)
        if ok:
            if action == "Load":
                fname, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text Files (*.txt)")
                if not fname:
                    return
                with open(fname, 'r') as f:
                    self.input_text.setText(f.read())
            elif action == "Save":
                fname, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text Files (*.txt)")
                if not fname:
                    return
                with open(fname, 'w') as f:
                    f.write(self.result_text.toPlainText())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CaesarCipherApp()
    window.show()
    sys.exit(app.exec())