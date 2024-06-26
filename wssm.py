#!/usr/bin/env python3

import subprocess
import sys
from math import log10

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (QApplication, QLabel, QProgressBar, QPushButton,
                             QVBoxLayout, QWidget)


class wifi_signal_monitor(QWidget):
    def __init__(self):
        super().__init__()
        self.initialize_gui()

    def initialize_gui(self):
        self.layout = QVBoxLayout()

        self.bssid_label = QLabel("BSSID: N/A")
        self.layout.addWidget(self.bssid_label)

        self.signal_strength_label = QLabel("Signal Strength: N/A")
        self.layout.addWidget(self.signal_strength_label)

        self.signal_strength_bar = QProgressBar()
        self.signal_strength_bar.setMinimum(0)
        self.signal_strength_bar.setMaximum(100)
        self.layout.addWidget(self.signal_strength_bar)

        self.best_distance_label = QLabel("Best Distance: Calculating...")
        self.layout.addWidget(self.best_distance_label)

        self.start_button = QPushButton("Start Monitoring")
        self.start_button.clicked.connect(self.start_monitoring)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

        self.setWindowTitle("Wireless Signal Monitor")
        self.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_signal_strength)

        self.best_signal_strength = -100
        self.best_distance = 0

    def start_monitoring(self):
        self.timer.start(500)

    def update_signal_strength(self):
        signal_strength, bssid = self.get_signal_strength_and_bssid()
        if signal_strength is not None:
            self.signal_strength_label.setText(f"Signal Strength: {signal_strength} dBm")
            self.signal_strength_bar.setValue(
                int(self.signal_strength_to_percentage(signal_strength))
            )
            if signal_strength > self.best_signal_strength:
                self.best_signal_strength = signal_strength
                self.best_distance = self.calculate_distance(signal_strength)
                self.best_distance_label.setText(
                    f"Best Distance: {self.best_distance:.2f} meters"
                )
        else:
            self.signal_strength_label.setText("Signal Strength: N/A")
            self.signal_strength_bar.setValue(0)

        if bssid is not None:
            self.bssid_label.setText(f"BSSID: {bssid}")
        else:
            self.bssid_label.setText("BSSID: N/A")

    def get_signal_strength_and_bssid(self):
        try:
            result = subprocess.run(["iwconfig"], capture_output=True, text=True)
            signal_strength = None
            bssid = None
            for line in result.stdout.split("\n"):
                if "Signal level=" in line:
                    signal_level = line.split("Signal level=")[1].split(" ")[0]
                    signal_strength = int(signal_level)
                if "Access Point:" in line:
                    bssid = line.split("Access Point:")[1].strip()
            return signal_strength, bssid
        except Exception as e:
            print(f"Error getting signal strength and BSSID: {e}")
            return None, None

    def calculate_distance(self, signal_strength):
        # Frequency in MHz (e.g., 2.4 GHz Wi-Fi)
        freq = 2400
        FSPL = abs(signal_strength)
        distance = 10 ** ((FSPL - (20 * log10(freq)) + 27.55) / 20)
        return distance

    def signal_strength_to_percentage(self, signal_strength):
        min_strength = -100
        max_strength = -30
        percentage = (
            (signal_strength - min_strength) * 100 / (max_strength - min_strength)
        )
        return max(0, min(100, percentage))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = wifi_signal_monitor()
    sys.exit(app.exec_())
