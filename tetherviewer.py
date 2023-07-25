import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout
from PyQt6.QtGui import QIcon
from view_latest_jpg import *
import threading
import sys
import trace
import threading
import time

class thread_with_trace(threading.Thread):
  def __init__(self, *args, **keywords):
    threading.Thread.__init__(self, *args, **keywords)
    self.killed = False
 
  def start(self):
    self.__run_backup = self.run
    self.run = self.__run     
    threading.Thread.start(self)
 
  def __run(self):
    sys.settrace(self.globaltrace)
    self.__run_backup()
    self.run = self.__run_backup
 
  def globaltrace(self, frame, event, arg):
    if event == 'call':
      return self.localtrace
    else:
      return None
 
  def localtrace(self, frame, event, arg):
    if self.killed:
      if event == 'line':
        raise SystemExit()
    return self.localtrace
 
  def kill(self):
    self.killed = True

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.name = 'TetherViewer'
        self.setWindowTitle(self.name)
        #self.setWindowIcon(QIcon('maps.ico'))
        self.resize(500,250) # width heights

        layout = QVBoxLayout()
        self.setLayout(layout)

        # widgets
        self.inputField  = QLineEdit()
        button = QPushButton('&Start')
        button.setStyleSheet("background-color: green")
        button.clicked.connect(self.start_tv)

        stop_button = QPushButton('&Stop')
        stop_button.setStyleSheet("background-color: red")
        stop_button.clicked.connect(self.stop_tv)
        self.output = QTextEdit()

        layout.addWidget(self.inputField)
        layout.addWidget(button)
        layout.addWidget(self.output)
        layout.addWidget(stop_button)

        self.folder = ''
    
    def start_tv(self):
        input = self.inputField.text()
        if self.check_exists(input):
            self.output.setText(f'Starting {self.name} on folder: {input}')
            self.folder = input

            self.thread = thread_with_trace(target=self.start_thread)
            self.thread.start()
        else:
            self.output.setText(f'Path: {input} Does not exist, please try another path.')

    def stop_tv(self):
        if self.folder != '':
            self.output.setText(f'Stopping {self.name} on folder: {self.folder}')
            self.thread.kill()
            self.thread.join()
            if not self.thread.is_alive():
               print("Killed Thread")
            self.folder = ''
        else:
            self.output.setText(f'Nothing to stop {self.name} on.')

    def check_exists(self, dir):
        if os.path.exists(dir):
            return dir
        return False
    
    def start_thread(self):
        path=self.folder
        time_period=0.1
        viewed_images = []
        while True:
            time.sleep(time_period)
            latest_image_path = open_latest_image(path=path)
            if latest_image_path and latest_image_path not in viewed_images:
                open_image(latest_image_path)
                viewed_images.append(latest_image_path)
            global running
            running = True
            if not running:
                break
    

app = QApplication(sys.argv)
app.setStyleSheet('''
    QWidget {
        font-size: 25px;
    }
    QPushButton {
        font-size: 20px;
    }
''')
window = MyApp()
window.show()
app.exec()
        