import sys
import os
import generate_ascii

from PySide6 import QtWidgets
from PySide6.QtWidgets import QPushButton, QFileDialog, QLabel,\
    QTextEdit, QSlider, QMessageBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class MyWidget(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()

        self.file_path = None  # Атрибут для хранения пути к файлу
        self.ratio_height = 2.5
        self.win_size = 25
        

        self.setGeometry(400, 100, 820, 750)
        self.setWindowTitle("Image to ascii")
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.slider_layout = QtWidgets.QVBoxLayout()
        self.control_layout = QtWidgets.QHBoxLayout()
        self.button_layout = QtWidgets.QHBoxLayout()
        
        # Кнопка для выбора файла
        self.button = QPushButton("Выбрать файл", self)
        self.button.setFixedSize(200, 38)
        self.button.clicked.connect(self.open_file_dialog)
        self.button_layout.addWidget(self.button, alignment=Qt.AlignCenter)

        # button for save file
        self.save_button = QPushButton("Сохранить файл в Downloads")
        self.save_button.setFixedSize(200, 38)
        self.save_button.clicked.connect(self.save_to_downloads)
        self.button_layout.addWidget(self.save_button, alignment=Qt.AlignCenter)
        
        self.layout.addLayout(self.button_layout)
        
        # Метка для отображения выбранного файла
        self.label = QLabel("Файл не выбран", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.control_layout.addWidget(self.label)

        self.sliderWidth = QSlider(Qt.Horizontal)
        self.sliderWidth.setMinimumWidth(50)
        self.sliderWidth.setMaximumWidth(500)
        self.sliderWidth.setMinimum(25)  # Минимальное значение
        self.sliderWidth.setMaximum(150)  # Максимальное значение
        self.sliderWidth.setValue(80)  # Начальное значение
        self.slider_layout.addWidget(self.sliderWidth)
        self.sliderWidth.valueChanged.connect(self.update_width)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimumWidth(50)
        self.slider.setMaximumWidth(500)
        self.slider.setMinimum(100)  # Минимальное значение
        self.slider.setMaximum(500)  # Максимальное значение
        self.slider.setValue(200)  # Начальное значение
        self.slider_layout.addWidget(self.slider)
        self.slider.valueChanged.connect(self.slider_ratio)


        self.control_layout.addLayout(self.slider_layout)
        self.layout.addLayout(self.control_layout)



        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)
        

    def open_file_dialog(self):
        # Открыть диалоговое окно для выбора файла
        self.file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Все файлы (*.*);;Изображения (*.png *.jpg *.bmp);;Текстовые файлы (*.txt)")
        if self.file_path:
            self.label.setText(f"Выбран файл:\n{self.file_path}")
            ascii_art = generate_ascii.image_to_ascii(self.file_path, self.win_size, self.ratio_height)
            font = QFont("Cascadia Mono Light")
            self.text_edit.setFont(font)
            self.text_edit.setText(ascii_art)
        else:
            self.label.setText("Файл не выбран")


    def save_to_downloads(self):
        downloads_path = os.path.join(os.path.expanduser('~'), "Downloads")
        file_name = "image.txt"
        save_path = os.path.join(downloads_path, file_name)
        try:
            ascii_art = generate_ascii.image_to_ascii(self.file_path, self.win_size, self.ratio_height) 
            with open(save_path, 'w') as f:
                f.write(ascii_art)
            QMessageBox.information(self, "Успех", f"Файл сохранён в: {save_path}")
        except Exception as e:
             QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {e}")


    def update_width(self, value):
        if self.file_path is None or len(self.file_path) == 0:
            self.label.setText("Выберите файл")
        else:
            print('12345678', len(self.file_path))
            self.win_size = value
            ascii_art = generate_ascii.image_to_ascii(self.file_path, self.win_size, self.ratio_height)
            font = QFont("Cascadia Mono Light")
            self.text_edit.setFont(font)
            self.text_edit.setText(ascii_art)

    def slider_ratio(self, value):
        if self.file_path is None or len(self.file_path) == 0:
            self.label.setText("Выберите файл")
        else:
            print('12345678', self.file_path)
            self.ratio_height = value / 100
            ascii_art = generate_ascii.image_to_ascii(self.file_path, self.win_size, self.ratio_height)
            font = QFont("Cascadia Mono Light")
            self.text_edit.setFont(font)
            self.text_edit.setText(ascii_art)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.show()

    sys.exit(app.exec())