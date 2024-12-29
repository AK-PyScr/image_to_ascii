import sys
import generate_ascii

from PySide6 import QtWidgets
from PySide6.QtWidgets import QPushButton, QFileDialog, QLabel,  QTextEdit, QSlider
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

r = 2.5
d: int

class MyWidget(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(400, 100, 220, 280)
        self.setWindowTitle("Погода")
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.slider_layout = QtWidgets.QVBoxLayout()
        self.control_layout = QtWidgets.QHBoxLayout()
        
        # Кнопка для выбора файла
        self.button = QPushButton("Выбрать файл", self)
        self.button.setFixedSize(200, 38)
        self.button.clicked.connect(self.open_file_dialog)
        self.layout.addWidget(self.button, alignment=Qt.AlignCenter)

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
        self.slider.setValue(250)  # Начальное значение
        self.slider_layout.addWidget(self.slider)
        self.slider.valueChanged.connect(self.slider_ratio)


        self.control_layout.addLayout(self.slider_layout)
        self.layout.addLayout(self.control_layout)



        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)
        

    def open_file_dialog(self):
        # Открыть диалоговое окно для выбора файла
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", "Все файлы (*.*);;Изображения (*.png *.jpg *.bmp);;Текстовые файлы (*.txt)")
        if file_path:
            self.label.setText(f"Выбран файл:\n{file_path}")
            ascii_art = generate_ascii.image_to_ascii(file_path, 90)
            font = QFont("Cascadia Mono Light")
            self.text_edit.setFont(font)
            self.text_edit.setText(ascii_art)
        else:
            self.label.setText("Файл не выбран")
    
        return file_path
    
    def update_width(self, value):
        global d
        d = value
        ascii_art = generate_ascii.image_to_ascii("hp.jpg", width=d, ratioH=r)
        font = QFont("Cascadia Mono Light")
        self.text_edit.setFont(font)
        self.text_edit.setText(ascii_art)

    def slider_ratio(self, value):
        global r 
        r = value / 100
        ascii_art = generate_ascii.image_to_ascii("hp.jpg", ratioH=r)
        font = QFont("Cascadia Mono Light")
        self.text_edit.setFont(font)
        self.text_edit.setText(ascii_art)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.show()

    sys.exit(app.exec())