import signal
import sys
import threading
from collections import deque
from pathlib import Path
from typing import TypeVar

import numpy as np
from toml import load, dump

import pyqtgraph as pg
from PySide6.QtCore import QTimer, Slot
from PySide6.QtWidgets import QApplication, QDialog, QFileDialog, QGraphicsScene, QMainWindow, QMessageBox, \
    QPlainTextEdit
from pymcuprog.pymcuprog_errors import PymcuprogSerialUpdiError
from pymcuprog.serialupdi.application import UpdiApplication
from serial import SerialException
from serial.tools.list_ports import comports

from lib.linkermap import LinkerMapParser, Section
from lib.monitor_gui import Ui_Dialog
from lib.smartsignal import SmartSignal
from lib.updi_terminal_gui import Ui_MainWindow

state = threading.Event()

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    state.set()
    
signal.signal(signal.SIGINT, signal_handler)

T = TypeVar('T', bool, int, str)

def parse_bytes(bytearray: bytearray, data_type: T) -> T:
    if isinstance(data_type, bool):
        return bool.from_bytes(bytearray)
    elif isinstance(data_type, int):
        return int.from_bytes(bytearray, 'little')
    elif isinstance(data_type, str):
        return bytearray.decode()
    
    raise TypeError("bytearray is of invalid type")
        
class UpdiTerminal(QMainWindow, Ui_MainWindow, SmartSignal):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.transport = None
        self.parser = None
        self.section = None
        self.section_type = None
        self.update_freq = 2
        self.monitors: list[UpdiMonitor] = []
        self.ports: list[str] = []
        
        self.monitor_timer = QTimer(self)
        self.ports_timer = QTimer(self)

        self.set_update_freq.setMinimum(1)
        self.set_update_freq.setMaximum(45)

        self.auto_connect()

        self.load_settings()
        
        self._type_options: dict[str, int|bool|str] = {"int": int(),
                                                       "bool": bool(),
                                                       "str": str()}
        
        self.update_ports()
        self.select_section_type.addItems(list(self._type_options))
        
        interval_int = int(1/self.update_freq*1e3)
        self.monitor_timer.setInterval(interval_int)
        self.monitor_timer.setObjectName("timer")
        self.monitor_timer.start()
        
        self.ports_timer.setInterval(1000)
        self.ports_timer.setObjectName("ports_timer")
        self.ports_timer.start()

    def load_settings(self):
        settings_path = Path(__file__).parent / "settings.toml"

        if not settings_path.exists():
            return

        with open(settings_path, 'r') as toml_file:
            settings = load(toml_file)

        if "map_file" in settings:
            self.map_file.setText(settings["map_file"])
            self.map_file.editingFinished.emit()

        if "set_update_freq" in settings:
            self.set_update_freq.setValue(settings["set_update_freq"])

    def dump_settings(self):
        settings_path = Path(__file__).parent / "settings.toml"

        settings = {
            "map_file": self.map_file.text(),
            "set_update_freq": self.set_update_freq.value()
        }

        with open(settings_path, 'w') as toml_file:
            dump(settings, toml_file)
        
    def update_ports(self):
        updated = sorted([p for p, d, h in comports()])
        
        if updated == self.ports:
            return
        
        self.ports = updated
        
        current = self.set_port.currentText()
        self.set_port.clear()
        self.set_port.addItems(self.ports)
            
        if current in self.ports:
            index = self.ports.index(current)
            self.set_port.setCurrentIndex(index)
            
        
    @Slot()
    def ports_timer__timeout_receiver(self):
        self.update_ports()
        
    @Slot()
    def serial_connect__clicked_receiver(self):
        if self.transport:
            QMessageBox.warning(self, "Connection Already Exists", "Serial connection already established")
            return
        
        port = self.set_port.currentText()
        if port not in self.ports:
            QMessageBox.warning(self, "Missing Selection", "Select a COM port before connecting")
            return
        
        try:
            self.transport = UpdiApplication(port, 9600)
        except SerialException:
            QMessageBox.warning(self, "Connection Failed", f"Failed to open port '{port}'")
            self.transport = None
            return
        except PymcuprogSerialUpdiError:
            QMessageBox.warning(self, "Initialisation Failed", "Failed to initialise UPDI")
            self.transport = None
            return

        self.serial_connect.setStyleSheet("color: green")

    @Slot()
    def browse__clicked_receiver(self):
        open_dir = ""
        if self.map_file.text():
            open_dir = str(Path(self.map_file.text()).parent)

        path_str, filter_str = QFileDialog.getOpenFileName(self, "Select a memory map file", open_dir, filter="Memory Map (*.map),All Files (*)")
        if path_str:
            self.map_file.setText(path_str)
            self.map_file.editingFinished.emit()

    @Slot()
    def map_file__editingFinished_receiver(self):
        path = Path(self.map_file.text())
        
        if not path.exists():
            QMessageBox.warning(self, "Invalid path", "The path provided does not exist")
            return
            
        if not path.is_file():
            QMessageBox.warning(self, "Invalid file", "The path provided does point to a file")
            return
        
        if not path.suffix == '.map':
            QMessageBox.warning(self, "Invalid file", "The file provided is not a .map")
            return
        
        print(f"Path entered: {path}")
            
        self.parser = LinkerMapParser.from_file(path)
        
        self.select_section.addItems(list(self.parser.memory_sections.keys()))
    
    @Slot()
    def select_section__currentIndexChanged_receiver(self):
        if not self.parser:
            QMessageBox.warning(self, "Map file missing", "Please enter a .map file path")
            return
        
        section_name = self.select_section.currentText()
        
        print(f"Section selected: {section_name}")
        self.section = self.parser.memory_sections[section_name]

    @Slot()
    def select_section_type__currentIndexChanged_receiver(self):
        section_type_str = self.select_section_type.currentText()
        print(f"Section type selected: {section_type_str}")
        self.section_type = self._type_options[section_type_str]


    @Slot()
    def set_update_freq__valueChanged_receiver(self):
        self.update_freq = self.set_update_freq.value()
        print(f"Update Frequency set: {self.update_freq}")
        interval_int = int(1/self.update_freq*1e3)
        self.monitor_timer.setInterval(interval_int)
        
    @Slot()
    def monitor__clicked_receiver(self):
        if not self.transport:
            QMessageBox.warning(self, "No Connection", "Please create a connection first")
            return
        
        if not self.section:
            QMessageBox.warning(self, "Missing entry", "Please select a section")
            return
        
        if self.section_type is None:
            QMessageBox.warning(self, "Missing entry", "Please select a section type")
            return
        
        monitor = UpdiMonitor(self, self.section, self.section_type)
        self.monitors.append(monitor)
        monitor.show()
        
    @Slot()
    def monitor_timer__timeout_receiver(self):
        if not self.transport:
            return
        
        self.monitors = [m for m in self.monitors if not m.result()]
        for monitor in self.monitors:
            res: bytearray = self.transport.read_data(monitor.section.address, monitor.section.size)
            monitor.update_value(res)

    def closeEvent(self, event):
        self.dump_settings()
        super().closeEvent(event)


class UpdiMonitor(QDialog, Ui_Dialog, SmartSignal):
    def __init__(self, parent: UpdiTerminal, section: Section, section_type) -> None:
        super().__init__(parent)
        self.test_timer = QTimer()

        self.setupUi(self)
        self.auto_connect()

        self.setWindowTitle(section.name)

        self.section = section
        self.section_type = section_type

        self.plot_widget.setBackground('w')
        self.plot_widget.setAntialiasing(True)
        self.plot_data = self.plot_widget.plot(pen={'color': 'b', 'width': 1})
        self.data_max_size = 100
        self.data = deque(maxlen=self.data_max_size)
        self.plot_length.setMaximum(1)
        self.plot_length.setMaximum(999)
        self.plot_length.setValue(self.data_max_size)

        self.test_timer.setInterval(100)
        self.test_timer.start()

    @Slot()
    def test_timer__timeout_receiver(self):
        value = np.random.randint(0, 100)
        sim = bytearray(value.to_bytes(2, "little"))
        self.update_value(sim)

    def update_value(self, value: bytearray):
        value = parse_bytes(value, self.section_type)
        self._update_value(value)
        self._update_roll(value)

    def _update_value(self, value):
        self.text_widget.setText(str(value))

    def _update_roll(self, value):
        self.data.append(value)

        # Update plot
        self.plot_data.setData(np.array(self.data))

    @Slot()
    def plot_length__valueChanged_receiver(self):
        current_data = self.data
        self.data_max_size = self.plot_length.value()
        self.data = deque(current_data, self.data_max_size)

    @Slot()
    def view_mode__clicked_receiver(self):
        match self.view_mode.text():
            case "Roll":
                self.view_mode.setText("Value")
                self.stackedWidget.setCurrentWidget(self.plot_page)
                print("View changed to Roll mode")
            case "Value":
                self.view_mode.setText("Roll")
                self.stackedWidget.setCurrentWidget(self.text_page)
                print("View changed to Value mode")

    def closeEvent(self, event):
        self.accept()
        super().closeEvent(event)

if __name__ == "__main__":

    app = QApplication()
    
    # window = UpdiTerminal()
    # window.show()
    dialog = UpdiMonitor(None, Section("foo", 0, 2), int())
    dialog.show()

    sys.exit(app.exec())

    # parser = LinkerMapParser.from_file(r"C:\Users\Finn\OneDrive\Shared Documents\Projects\CupWarmer\CupWarmer\firmware\CupWarmer.X\CupWarmer.X.map")
    
    # section = parser.memory_sections["monitor"]
    
    # port = "COM3"  # Replace with the appropriate COM port

    # transport = UpdiApplication(port, 9600)

    # while not state.is_set():
    #     res: bytearray = transport.read_data(section.address, section.size)
        
    #     value = parse_bytes(res, int())
    #     print("       ", end="\r")
    #     print(value, end="\r")
    #     sleep(0.5)