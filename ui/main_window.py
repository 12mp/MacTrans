from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QSplitter, QLabel, QPushButton, QStatusBar, QToolButton
)
from PySide6.QtCore import Qt, QSize, Slot
from PySide6.QtGui import QIcon

from ui.panels.transcription import TranscriptionPanel
from ui.panels.chat import ChatPanel

class MainWindow(QMainWindow):
    """Главное окно приложения MacTrans"""
    
    def __init__(self, config_manager, directories):
        super().__init__()
        
        self.config_manager = config_manager
        self.directories = directories
        
        self.setWindowTitle("MacTrans")
        self.setMinimumSize(1000, 700)
        
        # Настраиваем интерфейс
        self.setup_ui()
        
        # Соединяем сигналы между панелями
        self.connect_panels()
    
    def setup_ui(self):
        """Настройка UI-компонентов"""
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной вертикальный лейаут
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Добавляем шапку приложения
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Создаем сплиттер для панелей
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(1)
        self.splitter.setChildrenCollapsible(False)
        
        # Создаем панель транскрипции
        self.transcription_panel = TranscriptionPanel(self.config_manager)
        
        # Создаем панель AI-ассистента
        self.chat_panel = ChatPanel(self.config_manager)
        
        # Добавляем панели в сплиттер
        self.splitter.addWidget(self.transcription_panel)
        self.splitter.addWidget(self.chat_panel)
        
        # Устанавливаем равные размеры для панелей
        self.splitter.setSizes([500, 500])
        
        # Добавляем сплиттер в основной лейаут
        main_layout.addWidget(self.splitter)
        
        # Создаем и устанавливаем статусную строку
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        # Добавляем индикатор статуса
        self.status_indicator = QLabel("●")
        self.status_indicator.setObjectName("statusIndicator")
        self.status_label = QLabel("Готов к работе")
        
        status_layout = QHBoxLayout()
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.addWidget(self.status_indicator)
        status_layout.addWidget(self.status_label)
        
        status_widget = QWidget()
        status_widget.setLayout(status_layout)
        
        self.statusbar.addWidget(status_widget)
        
        # Добавляем информацию о модели
        model_info = QLabel("Whisper Base | Русский")
        self.statusbar.addPermanentWidget(model_info)
    
    def create_header(self):
        """Создание шапки приложения"""
        header = QWidget()
        header.setFixedHeight(60)
        header.setObjectName("appHeader")
        
        # Устанавливаем лейаут для шапки
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        # Создаем простой логотип "MT"
        logo_label = QLabel("MT")
        logo_label.setObjectName("appLogo")
        logo_label.setFixedSize(36, 36)
        logo_label.setAlignment(Qt.AlignCenter)
        
        app_title = QLabel("MacTrans")
        app_title.setObjectName("appTitle")
        
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(10)
        title_layout.addWidget(logo_label)
        title_layout.addWidget(app_title)
        
        header_layout.addLayout(title_layout)
        
        # Добавляем растягивающийся элемент
        header_layout.addStretch()
        
        # Добавляем кнопку настроек
        settings_button = QPushButton("Настройки")
        settings_button.setObjectName("settingsButton")
        settings_button.clicked.connect(self.open_settings)
        header_layout.addWidget(settings_button)
        
        return header
    
    def connect_panels(self):
        """Соединение сигналов между панелями"""
        # Соединяем сигнал отправки транскрипции со слотом установки транскрипции
        self.transcription_panel.transcriptionSent.connect(self.set_transcript_to_ai)
    
    @Slot()
    def open_settings(self):
        """Открытие окна настроек"""
        # Пока просто выводим сообщение в консоль
        print("Открытие окна настроек (будет реализовано)")
    
    @Slot(str)
    def set_transcript_to_ai(self, transcript_text):
        """Установка текста транскрипции для AI-ассистента"""
        # Здесь будет код для передачи транскрипции в AI-ассистент
        print(f"Транскрипция отправлена в AI ({len(transcript_text)} символов)")