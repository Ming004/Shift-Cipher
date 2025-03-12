import sys
import cv2, os
import pytesseract
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QMessageBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, \
    QTextEdit, QLabel, QSlider, QPushButton, QComboBox, QFileDialog, QInputDialog, QApplication
from PyQt6.QtGui import QIcon, QFont, QPalette, QColor, QImage, QPixmap
from PyQt6.QtCore import Qt, QUrl, QTimer, QTime
from shiftcipher2 import encrypt_check, encrypt_cipher, decrypt, cal_word_count_of_cipher


class DistributionWindow(QWidget):
    def __init__(self, char_count):
        super().__init__()
        self.setWindowTitle("Character Distribution")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout(self)

        # Create bar chart
        chars = list(char_count.keys())
        counts = list(char_count.values())

        plt.figure(figsize=(10, 6))
        plt.bar(chars, counts, color='blue')
        plt.xlabel('Characters')
        plt.ylabel('Frequency')
        plt.title('Character Distribution')
        plt.xticks(rotation=90)
        plt.tight_layout()

        # Save the plot to a file
        plt.savefig('char_distribution.png')
        plt.close()

        # Display the plot in the new window
        pixmap = QPixmap('char_distribution.png')
        label = QLabel()
        label.setPixmap(pixmap.scaled(1000, 700, Qt.AspectRatioMode.KeepAspectRatio))
        self.layout.addWidget(label)


class CaesarCipherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Caesar Cipher Translator")  # title
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowIcon(QIcon("hiii.png"))  # icon

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Top layout for timer, character count, word count, clear button, and copy button
        top_layout = QHBoxLayout()
        self.timer_label = QLabel()
        top_layout.addWidget(self.timer_label)
        self.char_count_label = QLabel("Characters: 0")
        top_layout.addWidget(self.char_count_label)
        self.word_count_label = QLabel("Words: 0")
        top_layout.addWidget(self.word_count_label)
        self.clear_btn = QPushButton("Clear", clicked=self.clear_text)
        top_layout.addWidget(self.clear_btn)
        self.copy_btn = QPushButton("Copy to Clipboard", clicked=self.copy_to_clipboard)
        top_layout.addWidget(self.copy_btn)
        self.help_btn = QPushButton("Help", clicked=self.show_help)
        top_layout.addWidget(self.help_btn)
        self.layout.addLayout(top_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update every second

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
        self.decrypt_btn = QPushButton("Decrypt", clicked=self.decrypt_text)
        button_layout.addWidget(self.encrypt_btn)
        button_layout.addWidget(self.decrypt_btn)
        # Add this in the __init__ method where other buttons are defined
        self.count_btn = QPushButton("Count Words", clicked=self.count_words)
        button_layout.addWidget(self.count_btn)
        self.distribution_btn = QPushButton("Show Distribution", clicked=self.show_text_distribution)
        button_layout.addWidget(self.distribution_btn)
        # results
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText("Results will be appear here...")
        self.result_text.setFont(QFont("Century Gothic", 12))
        # theme and file operations
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
        self.statusBar().showMessage('Version 2.1 Powered by Charles')

        # Theme setup
        self.custom_colors = {
            'background': QColor(240, 240, 240),
            'text': QColor(0, 0, 0),
            'button': QColor(220, 220, 220),
            'button_text': QColor(0, 0, 0)
        }
        self.change_theme()
        self.apply_3d_effect(self.input_text)
        self.apply_3d_effect(self.result_text)

        # Connect textChanged signal to update methods
        self.input_text.textChanged.connect(self.update_char_count)
        self.input_text.textChanged.connect(self.update_word_count)

    def apply_3d_effect(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(90)
        shadow.setXOffset(10)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 150))
        widget.setGraphicsEffect(shadow)

    def update_timer(self):
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.timer_label.setText(current_time)

    def show_text_distribution(self):
        raw = self.input_text.toPlainText()
        if not raw:
            QMessageBox.warning(self, "Input Error", "empty.")
            return

        # Calculate character frequency
        char_count = cal_word_count_of_cipher(raw)

        # Create and show the distribution window
        self.distribution_window = DistributionWindow(char_count)
        self.distribution_window.show()

    def ocr_preprocess_image(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open Image for OCR", "",
                                               "Image Files (*.png *.jpg *.jpeg *.bmp*.pdf)")
        if not fname:
            return
        try:
            # Set Tesseract path here
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Ensure this path is correct

            # Load the image
            img = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
            if img is None:
                raise ValueError("Unread ! ! !")

            # Preprocessing
            _, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            img_bin = 255 - img_bin  # Invert the binary image for better OCR

            # Display the processed image
            qImg = QImage(img_bin.data, img_bin.shape[1], img_bin.shape[0], QImage.Format.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qImg)
            self.image_preview.setPixmap(pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))

            # Perform OCR
            text = pytesseract.image_to_string(img_bin)

            # 使用OCR结果更新input_text
            self.input_text.setPlainText(text)

            QMessageBox.information(self, "Success", "successfully.")
            self.statusBar().showMessage('OCR completed', 5000)
        except Exception as e:
            error_message = f"Failed to process the image: {str(e)}"
            QMessageBox.warning(self, "Image Processing Error", error_message)
            self.statusBar().showMessage(error_message, 10000)

    def update_shift_label(self, value):
        self.shift_value.setText(f"Shift: {value}")  # update

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
            result = result + f"Shift {shift}: {decrypted}\n\n"
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
                if fname:
                with open(fname, 'r') as file:
                    self.input_text.setText(file.read())
            elif action == "Save":
                fname, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text Files (*.txt)")
                if fname:
                with open(fname, 'w') as file:
                    f.write(self.result_text.toPlainText())

    def count_words(self):
        raw = self.input_text.toPlainText()
        word_count = cal_word_count_of_cipher(raw)
        QMessageBox.information(self, "Word Count", f"Word count: {word_count}")

    def update_char_count(self):
        char_count = len(self.input_text.toPlainText())
        self.char_count_label.setText(f"Characters: {char_count}")

    def update_word_count(self):
        word_count = len(self.input_text.toPlainText().split())
        self.word_count_label.setText(f"Words: {word_count}")

    def clear_text(self):
        self.input_text.clear()
        self.result_text.clear()
        self.update_char_count()
        self.update_word_count()

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.result_text.toPlainText())
        self.statusBar().showMessage('Text copied to clipboard', 5000)

    def show_help(self):
        help_text = (
            "Caesar Cipher Translator Help:\n\n"
            "1. 加密： 使用指定移位值的凱撒密碼來加密輸入文字。\n"
            "2. 解密： 透過嘗試所有可能的移位值來解密輸入的文字。\n"
            "3. Count Words（計算字數）： 計算輸入文字的字數。\n"
            "4. 顯示分佈： 顯示輸入文字的字元頻率分佈。\n"
            "5. 清除： 清除輸入和結果文字欄位。\n"
            "6. 複製到剪貼簿： 將結果文字複製到剪貼簿。\n"
            "7. 匯入影像： 匯入影像並執行 OCR 以擷取文字。\n"
            "8. 儲存： 將結果文字儲存至檔案。\n"
            "9. 主題： 在淺色與深色模式之間變更應用程式主題。\n"
        )
        QMessageBox.information(self, "Help", help_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CaesarCipherApp()
    window.show()
    sys.exit(app.exec())