import sys
import cv2
import pytesseract
from PyQt6.QtWidgets import QApplication, QMessageBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QSlider, QPushButton, QComboBox, QFileDialog, QInputDialog
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor, QImage, QPixmap
from PyQt6.QtCore import Qt
from shiftcipher2 import encrypt_check, encrypt_cipher, decrypt, cal_word_count_of_cipher

def validate_input_text(text):
    min_length = 200
    if len(text) < min_length:
        raise ValueError(f"Input text must be at least {min_length} characters long.")

def sanitize_input_text(text):
    import re
    sanitized_text = re.sub(r'[^A-Za-z0-9\s]', '', text)  # Allow only alphanumeric and whitespace
    return sanitized_text

class OCRProcessor:
    def __init__(self, tesseract_cmd):
        self.tesseract_cmd = tesseract_cmd
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_cmd

    def preprocess_image(self, fname):
        img = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError("Unreadable image!")
        _, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        img_bin = 255 - img_bin  # Invert the binary image for better OCR
        return img_bin

    def perform_ocr(self, img_bin):
        return pytesseract.image_to_string(img_bin)

class CaesarCipherApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Caesar Cipher Translator") # title
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowIcon(QIcon("hiii.png"))  # icon

        self.ocr_processor = OCRProcessor(r'C:\Program Files\Tesseract-OCR\tesseract.exe')

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # input Section
        input_layout = QHBoxLayout()
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter words here (at least 200 words)...")
        self.input_text.setFont(QFont("Century Gothic", 12))
        input_layout.addWidget(self.input_text)
        # shift selection
        shift_layout = QVBoxLayout()
        self.shift_slider = QSlider(Qt.Orientation.Horizontal)
        self.shift_slider.setRange(0, 26)
        self.shift_slider.valueChanged.connect(self.update_shift_label)
        self.shift_value = QLabel("Shift: 0")
        shift_layout.addWidget(self.shift_slider)
        shift_layout.addWidget(self.shift_value)
        # buttons
        button_layout = QHBoxLayout()
        self.encrypt_btn = QPushButton("Encrypt", clicked=self.encrypt_text)
        self.encrypt_btn.setToolTip("Click to encrypt the text")
        self.decrypt_btn = QPushButton("Decrypt", clicked=self.decrypt_text)
        self.decrypt_btn.setToolTip("Click to decrypt the text")
        button_layout.addWidget(self.encrypt_btn)
        button_layout.addWidget(self.decrypt_btn)
        # Add this in the __init__ method where other buttons are defined
        self.count_btn = QPushButton("Count Words", clicked=self.count_words)
        self.count_btn.setToolTip("Click to count words in the text")
        button_layout.addWidget(self.count_btn)
        # results
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("Results will appear here...")
        self.result_text.setFont(QFont("Century Gothic", 12))
        # theme and file operations
        control_layout = QHBoxLayout()
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        self.theme_combo.setToolTip("Select theme")
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        self.file_btn = QPushButton("Save", clicked=self.file_operations)
        self.file_btn.setToolTip("Click to save the result to a file")
        control_layout.addWidget(self.theme_combo)
        control_layout.addWidget(self.file_btn)
        self.ocr_btn = QPushButton("Import Image", clicked=self.ocr_preprocess_image)
        self.ocr_btn.setToolTip("Click to import an image for OCR")
        control_layout.addWidget(self.ocr_btn)
        self.image_preview = QLabel()
        self.layout.addWidget(self.image_preview)
        # Adding to main layout
        self.layout.addLayout(input_layout)
        self.layout.addLayout(shift_layout)
        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.result_text)
        self.layout.addLayout(control_layout)
        self.statusBar().showMessage('Version 2.1 Powered by Charles')

        # Theme setup
        self.custom_colors = {
            'background': QColor(240, 240, 240),
            'text': QColor(0, 0, 0),
            'button': QColor(220, 220, 220),
            'button_text': QColor(0, 0, 0)
        }
        self.change_theme()

    def ocr_preprocess_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open Image for OCR", "", "Image Files (*.png *.jpg *.jpeg *.bmp*.pdf)")
        if not fname:
            return
        try:
            img_bin = self.ocr_processor.preprocess_image(fname)
            qImg = QImage(img_bin.data, img_bin.shape[1], img_bin.shape[0], QImage.Format.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qImg)
            self.image_preview.setPixmap(pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))

            text = self.ocr_processor.perform_ocr(img_bin)
            self.input_text.setPlainText(text)

            QMessageBox.information(self, "Success", "OCR completed successfully.")
            self.statusBar().showMessage('OCR completed', 5000)
        except Exception as e:
            error_message = f"Failed to process the image: {str(e)}"
            QMessageBox.warning(self, "Image Processing Error", error_message)
            self.statusBar().showMessage(error_message, 10000)

    def update_shift_label(self, value):
        self.shift_value.setText(f"Shift: {value}") # update

    def encrypt_text(self):
        raw = self.input_text.toPlainText()
        try:
            validate_input_text(raw)
            sanitized_text = sanitize_input_text(raw)
            shift = self.shift_slider.value()
            check_result = encrypt_check(sanitized_text)
            if check_result == "valid....":
                encrypted = encrypt_cipher(sanitized_text, shift)
                self.result_text.setText(encrypted)
                self.statusBar().showMessage('Text encrypted', 5000)
            else:
                self.result_text.setText(check_result)
                self.statusBar().showMessage('Encryption Error: ' + check_result, 5000)
        except ValueError as e:
            self.result_text.setText(str(e))
            self.statusBar().showMessage('Input Error: ' + str(e), 5000)

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

    def set_theme(self, theme_colors):
        palette = QPalette()
        for role, color in theme_colors.items():
            palette.setColor(role, QColor(*color))
        self.setPalette(palette)

    def set_light_theme(self):
        light_colors = {
            QPalette.ColorRole.Window: (240, 240, 240),
            QPalette.ColorRole.WindowText: (0, 0, 0),
            QPalette.ColorRole.Base: (255, 255, 250),
            QPalette.ColorRole.AlternateBase: (245, 245, 245),
            QPalette.ColorRole.ToolTipBase: (255, 255, 255),
            QPalette.ColorRole.ToolTipText: (0, 0, 255),
            QPalette.ColorRole.Text: (0, 0, 0),
            QPalette.ColorRole.Button: (220, 220, 220),
            QPalette.ColorRole.ButtonText: (0, 0, 0),
            QPalette.ColorRole.PlaceholderText: (0, 0, 10),
            QPalette.ColorRole.Highlight: (42, 130, 218),
            QPalette.ColorRole.HighlightedText: (255, 255, 255)
        }
        self.set_theme(light_colors)

    def set_dark_theme(self):
        dark_colors = {
            QPalette.ColorRole.Window: (53, 53, 53),
            QPalette.ColorRole.WindowText: (255, 255, 255),
            QPalette.ColorRole.Base: (10, 10, 10),
            QPalette.ColorRole.AlternateBase: (20, 20, 20),
            QPalette.ColorRole.ToolTipBase: (0, 0, 0),
            QPalette.ColorRole.ToolTipText: (255, 255, 255),
            QPalette.ColorRole.Text: (255, 255, 255),
            QPalette.ColorRole.Button: (53, 53, 53),
            QPalette.ColorRole.ButtonText: (255, 255, 255),
            QPalette.ColorRole.Highlight: (42, 130, 218),
            QPalette.ColorRole.HighlightedText: (0, 0, 0)
        }
        self.set_theme(dark_colors)

    def file_operations(self):
        action, ok = QInputDialog.getItem(self, "File Operation",
                                          "Choose an action:", ["Load", "Save"], 0, False)
        if ok:
            if action == "Load":
                fname, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text Files (*.txt*.pdf)")
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

    def count_words(self):
        text = self.input_text.toPlainText()
        word_count = cal_word_count_of_cipher(text)
        QMessageBox.information(self, "Word Count", f"Word count: {word_count}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CaesarCipherApp()
    window.show()
    sys.exit(app.exec())