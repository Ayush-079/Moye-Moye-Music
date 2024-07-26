import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsPixmapItem,QGraphicsScene,QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QRect, QPoint, QPropertyAnimation,QTimer
import player
import data_handel as dh
import time
import threading
import asyncio
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
            
        MainWindow.setObjectName("MainWindow")
        
        MainWindow.resize(676, 154)
        MainWindow.setStyleSheet("background-color: rgb(63, 63, 63);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Thumbnail = QtWidgets.QGraphicsView(self.centralwidget)
        self.Thumbnail.setGeometry(QtCore.QRect(10, 30, 150, 70))
        self.Thumbnail.setStyleSheet(
"                border: 4px rgb(88, 88, 88) ;\n"
"                border-radius: 10px;\n"
"                background-color: transparent;\n"
"            }")
        self.Thumbnail.setObjectName("Thumbnail")
        self.Song_bar = QtWidgets.QSlider(self.centralwidget)
        self.Song_bar.setGeometry(QtCore.QRect(220, 50, 341, 16))
        self.Song_bar.setAutoFillBackground(False)
        self.Song_bar.setStyleSheet("QSlider::groove:horizontal {\n"
"\n"
"        height: 5px;\n"
"    background-color: rgb(255, 255, 255);\n"
"        margin: 0px;\n"
"    }\n"
"\n"
"    QSlider::handle:horizontal {\n"
"\n"
"\n"
"    background-color: rgb(255, 255, 255);\n"
"        width: 20px;\n"
"        margin: -4px 0; /* handle is placed by default 2px inside groove border */\n"
"        border-radius: 5px;\n"
"    }")
        
        self.Song_bar.setOrientation(QtCore.Qt.Horizontal)
        self.Song_bar.setObjectName("Song_bar")
        self.commandLinkButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.commandLinkButton.setGeometry(QtCore.QRect(-390, 310, 222, 48))
        self.commandLinkButton.setObjectName("commandLinkButton")
        self.Title = QtWidgets.QLabel(self.centralwidget)
        self.Title.setGeometry(QtCore.QRect(25, 100,150 , 20))
        self.Title.setAlignment(QtCore.Qt.AlignLeft)
        self.Title.setStyleSheet("font-family: Arial; font-size: 18px; font-weight: bold; color: white;")
        self.Title.setObjectName("Title")
        self.title_animation = QPropertyAnimation(self.Title, b"geometry")
        self.title_animation.setDuration(5000)
        self.title_animation.setStartValue(QtCore.QRect(25, 100, 150, 20))  # adjust the start position and width
        self.title_animation.setEndValue(QRect(-150, 100, 150, 20))  # adjust the end position and width  # adjust the end position
        self.title_animation.setLoopCount(-1)# loop indefinitely
        self.Title.setWordWrap(True)
        self.Title.setMinimumWidth(150)
        self.Title.setMaximumWidth(300)

        # self.title_animation.start()
        self.Playpause = QtWidgets.QLabel(self.centralwidget)
        self.Playpause.setGeometry(QtCore.QRect(390, 90, 31, 31))
        self.Playpause.setStyleSheet("background-color: Transparent;")
        self.Playpause.setText("")
        self.Playpause.setPixmap(QtGui.QPixmap("icons_images/pause.png"))
        self.Playpause.setScaledContents(True)
        self.Playpause.setObjectName("Playpause")
        self.Forward = QtWidgets.QLabel(self.centralwidget)
        self.Forward.setGeometry(QtCore.QRect(470, 90, 31, 31))
        self.Forward.setStyleSheet("background-color: Transparent;")
        self.Forward.setText("")
        self.Forward.setPixmap(QtGui.QPixmap("icons_images/forward.png"))
        self.Forward.setScaledContents(True)
        self.Forward.setObjectName("Forward")
        self.backward = QtWidgets.QLabel(self.centralwidget)
        self.backward.setGeometry(QtCore.QRect(310, 90, 31, 31))
        self.backward.setStyleSheet("background-color: Transparent;")
        self.backward.setText("")
        self.backward.setPixmap(QtGui.QPixmap("icons_images/backward.png"))
        self.backward.setScaledContents(True)
        self.backward.setObjectName("backward")
        self.forward_button = QtWidgets.QPushButton(self.centralwidget)
        self.forward_button.setGeometry(QtCore.QRect(470, 90, 32, 32))
        self.forward_button.setStyleSheet("background-color:transparent;")
        self.forward_button.setText("")
        self.forward_button.setObjectName("forward_button")
        self.playpause_state = False
        self.playpause_button = QtWidgets.QPushButton(self.centralwidget)
        self.playpause_button.setGeometry(QtCore.QRect(390, 90, 32, 32))
        self.playpause_button.setStyleSheet("background-color:transparent;")
        self.playpause_button.setText("")
        self.playpause_button.setObjectName("playpause_button")
        self.playpause_button.clicked.connect(self.playpause_button_clicked)
        self.backward_button = QtWidgets.QPushButton(self.centralwidget)
        self.backward_button.setGeometry(QtCore.QRect(310, 90, 32, 32))
        self.backward_button.setStyleSheet("background-color:transparent;")
        self.backward_button.setText("")
        self.backward_button.setObjectName("backward_button")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(620, 10, 51, 51))
        self.label.setStyleSheet("font-family: Arial; font-size: 24px; font-weight: bold; color: white;")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(619, 10, 51, 50))
        self.pushButton.setStyleSheet("QPushButton {\n"
"        background-color: rgba(0, 0, 0, 0); /* transparent background */\n"
"        border: none;\n"
"        color: white;\n"
"    }\n"
"\n"
"    QPushButton:hover {\n"
"        background-color: rgba(255, 255, 255, 50); /* slightly translucent white background on hover */\n"
"    }")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.Search = QtWidgets.QFrame(self.centralwidget)
        self.Search.setGeometry(QtCore.QRect(0, 10, 611, 131))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        self.Search.setFont(font)
        self.Search.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.Search.setMouseTracking(True)
        self.Search.setWhatsThis("")
        self.Search.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Search.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Search.setObjectName("Search")
        self.search_bar = QtWidgets.QLineEdit(self.Search)
        self.search_bar.setGeometry(QtCore.QRect(150, 0, 311, 41))
        self.search_bar.setStyleSheet("QLineEdit {\n"
"        background-color: white;\n"
"        border: 1px solid rgb(63, 63, 63);\n"
"        border-radius: 20px;\n"
"        padding: 5px;\n"
"    }\n"
"\n"
"    QLineEdit::placeholder {\n"
"        color: #aaa;\n"
"        font-size: 12px;\n"
"        font-style: italic;\n"
"    }\n"
"\n"
"    QLineEdit:hover {\n"
"        border: 3px solid #007bff; /* blue border on hover */\n"
"    }\n"
"\n"
"    QLineEdit:pressed {\n"
"        border: 3px solid #007bff; /* blue border on click */\n"
"    }")
        self.search_bar.setText("")
        self.search_bar.returnPressed.connect(self.search_bar_enter_pressed)

        self.search_bar.setObjectName("search_bar")
        self.search_bar.setPlaceholderText("Enter your song")
        self.thumbnail_search = QtWidgets.QGraphicsView(self.Search)
        self.thumbnail_search.setGeometry(QtCore.QRect(60, 60, 80, 51))
        self.thumbnail_search.setObjectName("thumbnail_search")
        self.thumbnail_search.setStyleSheet("border: none;")
        self.Title_search = QtWidgets.QLabel(self.Search)
        self.Title_search.setGeometry(QtCore.QRect(210, 60, 281, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(70)
        self.Title_search.setFont(font)
        self.Title_search.setStyleSheet("QLabel {\n"
"    color: #ffffff; /* or simply \"white\" */\n"
"}")
        self.Title_search.setText("")
        self.Title_search.setObjectName("Title_search")
        self.pushButton_2 = QtWidgets.QPushButton(self.Search)
        self.pushButton_2.setGeometry(QtCore.QRect(60, 50, 451, 71))
        self.pushButton_2.setStyleSheet("QPushButton {\n"
"        background-color: rgba(0, 0, 0, 0); /* transparent background */\n"
"        border: none;\n"
"        color: white;\n"
"    }")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.pushButton_2_clicked)
        self.Thumbnail.raise_()
        self.Song_bar.raise_()
        self.commandLinkButton.raise_()
        self.Title.raise_()
        self.Playpause.raise_()
        self.backward.raise_()
        self.Forward.raise_()
        self.forward_button.raise_()
        self.playpause_button.raise_()
        self.backward_button.raise_()
        
        self.label.raise_()
        self.pushButton.raise_()
        self.Search.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.pushButton.clicked.connect(self.pushButton_clicked)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def pushButton_clicked(self):
        self.Search.setVisible(not self.Search.isVisible())
    def pushButton_clicked(self):
        if self.Search.isHidden():
                self.Search.show()
        else:
                self.Search.hide()
    def search(self,query):
            self.query=query
            
            try:
                print('searching...')
                data=dh.get(self.query) 
                
                return data
            except Exception as e:
                    player.fetch(self.query)

    global play_
    def search_bar_enter_pressed(self):
        
        search_text = self.search_bar.text()
        self.pushButton_2.setStyleSheet("QPushButton {\n"
"        background-color: rgba(0, 0, 0, 0); /* transparent background */\n"
"        border: none;\n"
"        color: white;\n"
"    }\n"
"\n"
"    QPushButton:hover {\n"
"        background-color: rgba(255, 255, 255, 50); /* slightly translucent white background on hover */\n"
"    }")
        
        try:
                
                result = self.search(search_text)  # Adjusted to call get function correctly
                image_data = result[1]  # Assuming thumbnail is the second element in the result
                self.Title_search.setText(result[3])
                if image_data:
                        # Convert the image data to a QPixmap
                        image = QImage()
                        if image.loadFromData(image_data):
                                pixmap = QPixmap.fromImage(image)

                                # Scale the pixmap to fit the thumbnail search scene
                                pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)  # adjust the size as needed

                                # Set the pixmap to the thumbnail search scene
                                self.thumbnail_search.setScene(QGraphicsScene())
                                item = QGraphicsPixmapItem(pixmap)
                                self.thumbnail_search.scene().addItem(item)
                                self.thumbnail_search.fitInView(item, QtCore.Qt.KeepAspectRatio)
                        else:
                                print("Failed to load image data")
                                print(f"Image data size: {len(image_data)} bytes")  # Debug info
                else:
                        print("No image data found")
        
        except Exception as e:
                print(e)
        return result[2]
    def set_slider(self,value):

        self.value=value   
        self.Song_bar.setMaximum(int(self.value))
        self.timer = QTimer()
        self.timer.setInterval(1000)  # 1000 milliseconds = 1 second
        self.timer.timeout.connect(self.update_song_bar)
        self.timer.start()
        # self.Song_bar.setValue(self.Song_bar.value()+1)
        
        
    def update_song_bar(self):
        self.value += 1
        self.Song_bar.setValue(self.value)
    def pushButton_2_clicked(self):
        
        if self.Title_search.text() !='':
                self.Title.setText(self.Title_search.text())
                pass
        else:
                return 0
        self.Search.hide()
        
        try:
                result = self.search(self.Title_search.text())  # Adjusted to call get function correctly
                image_data = result[1]  # Assuming thumbnail is the second element in the result
                self.Title.setText(result[3])
                if image_data:
                        # Convert the image data to a QPixmap
                        image = QImage()
                        if image.loadFromData(image_data):
                                pixmap = QPixmap.fromImage(image)

                                # Scale the pixmap to fit the Thumbnail widget
                                pixmap = pixmap.scaled(181, 61, QtCore.Qt.KeepAspectRatio)  # adjust the size as needed

                                # Set the pixmap to the Thumbnail widget
                                scene = QGraphicsScene()
                                item = QGraphicsPixmapItem(pixmap)
                                scene.addItem(item)
                                self.Thumbnail.setScene(scene)
                                self.Thumbnail.fitInView(item, QtCore.Qt.KeepAspectRatio)
                        else:
                                print("Failed to load image data")
                                print(f"Image data size: {len(image_data)} bytes")  # Debug info
                else:
                        print("No image data found")
        except Exception as e:
                print(e)
        global play_
        play_=player.Player(self.Title_search.text())
        self.Playpause.setPixmap(QtGui.QPixmap("icons_images/play.png"))
        play_.play()
    def playpause_button_clicked(self):
            
        if not self.playpause_state:
            self.Playpause.setPixmap(QtGui.QPixmap("icons_images/play.png"))
            play_.resume()
            self.playpause_state = True  # Set playpause_state to True (play)
        else:   
            self.Playpause.setPixmap(QtGui.QPixmap("icons_images/pause.png"))
            play_.pause()
            self.playpause_state = False
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Soundify"))
        self.commandLinkButton.setText(_translate("MainWindow", "CommandLinkButton"))
        self.label.setText(_translate("MainWindow", "<<<"))
        # MainWindow.setWindowFlags(Qt.FramelessWindowHint)

try:
        if __name__ == "__main__":
        
                app = QtWidgets.QApplication(sys.argv)
                MainWindow = QtWidgets.QMainWindow()
                ui = Ui_MainWindow()
                ui.setupUi(MainWindow)
                MainWindow.show()
                app.exec_()
except Exception as e:
        print(e)