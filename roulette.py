import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QPalette, QPixmap, QIcon, QFontDatabase, QFont
import random


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tanks = ['1к свободного опыта', 'T1 Heavy Tank', 'M4 Sherman',
                      'AMX M4 45', 'Leopard 1', 'IS-7']
        self.win_chance = [0.7, 0.35, 0.3, 0.15, 0.10, 0.10]
        self.tank_images = [
            "data/img/bump.jpg",
            "data/img/m4.png",
            "data/img/t1.png",
            "data/img/amx.png",
            "data/img/leopard.png",
            "data/img/is7.png"
        ]
        menu = self.menuBar()
        prize_menu = menu.addMenu("Меню")
        prize_action = prize_menu.addAction("Шансы")
        prize_action.triggered.connect(self.show_prizes)
        color_menu = menu.addMenu("Палитра")
        color_action = color_menu.addAction("Изменить палитру")
        color_action.triggered.connect(self.change_color)
        self.colors = ['white', 'lightgray', 'darkgray', 'gray']
        self.current_color = 0
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("white"))
        self.setPalette(palette)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        roulette_text = QLabel("Раскрути Рулетку")
        roulette_text.setAlignment(Qt.AlignCenter)
        self.spin_button = QPushButton("Крутануть")
        self.spin_button.clicked.connect(self.spin)
        self.result_text = QLabel("")
        self.result_text.setAlignment(Qt.AlignCenter)
        self.image_label = QLabel("")
        self.image_label.setAlignment(Qt.AlignCenter)
        v_layout = QVBoxLayout()
        v_layout.addWidget(roulette_text)
        v_layout.addWidget(self.spin_button)
        v_layout.addWidget(self.result_text)
        v_layout.addWidget(self.image_label)
        central_widget.setLayout(v_layout)

    def spin(self):
        self.spin_button.setEnabled(False)
        self.spinning_results = [random.choices(
            self.tanks, weights=self.win_chance, k=1)[0] for i in range(10)]
        self.spinning_results.append(random.choices(
            self.tanks, weights=self.win_chance, k=1)[0])
        self.spin_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_spin)
        self.timer.start(100)

    def update_spin(self):
        self.result_text.setText(
            f'Крутится...{self.spinning_results[self.spin_index]}')
        tank_image = self.spinning_results[self.spin_index]
        tank_index = self.tanks.index(tank_image)
        self.image_label.setPixmap(
            QPixmap(self.tank_images[tank_index]).scaledToHeight(200))
        self.spin_index += 1
        if self.spin_index >= len(self.spinning_results):
            self.timer.stop()
            self.result_text.setText(
                f'Вы выиграли: {self.spinning_results[-1]}')
            self.spin_button.setEnabled(True)

    def show_prizes(self):
        prizes = "\n".join(
            [f"{tank}: {chance*100}%" for tank, chance in zip(self.tanks, self.win_chance)])
        QMessageBox.information(self, "Шансы", prizes)

    def change_color(self):
        self.current_color = (self.current_color + 1) % len(self.colors)
        color = self.colors[self.current_color]
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


app = QApplication(os.environ.get("APP_ARGS", []))
window = MyWindow()
font_id = QFontDatabase.addApplicationFont("Roboto-Regular.ttf")
if font_id != -1:
    font_name = QFontDatabase.applicationFontFamilies(font_id)[0]
    app.setFont(QFont(font_name))
window.setWindowTitle("Roulette")
window.setWindowIcon(QIcon("data/img/icon.png"))
window.setFixedSize(400, 300)
window.show()
app.exec_()
