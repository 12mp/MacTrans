from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QTextEdit, QComboBox, QToolBar, QSizePolicy, QFrame,
    QToolButton
)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QFont, QColor, QIcon, QTextCursor

class TranscriptionPanel(QWidget):
    """Панель транскрипции с функциями захвата и отображения аудио"""
    
    transcriptionSent = Signal(str)  # Сигнал отправки транскрипции в AI
    
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.is_recording = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка интерфейса панели"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Заголовок панели
        self.header = self.create_header()
        layout.addWidget(self.header)
        
        # Панель инструментов
        self.toolbar = self.create_toolbar()
        layout.addWidget(self.toolbar)
        
        # Область для текста транскрипции
        self.transcript_area = self.create_transcript_area()
        layout.addWidget(self.transcript_area)
        
        # Панель управления
        self.control_panel = self.create_control_panel()
        layout.addWidget(self.control_panel)
    
    def create_header(self):
        """Создание заголовка панели с улучшенной видимостью"""
        header = QFrame()
        header.setObjectName("panelHeader")
        header.setMaximumHeight(48)
        
        header_layout = QHBoxLayout(header)
        
        # Иконка и заголовок
        title = QLabel("Транскрипция")
        title.setObjectName("panelTitle")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Индикатор текущей модели
        self.model_indicator = QLabel("Whisper Base")
        self.model_indicator.setObjectName("modelIndicator")
        header_layout.addWidget(self.model_indicator)
        
        # Кнопка сворачивания
        collapse_button = QToolButton()
        collapse_button.setText("▼")
        collapse_button.setObjectName("collapseButton")
        header_layout.addWidget(collapse_button)
        
        return header
    
    def create_toolbar(self):
        """Создание панели инструментов"""
        toolbar_widget = QWidget()
        toolbar_layout = QHBoxLayout(toolbar_widget)
        
        # Кнопка создания саммари
        summary_button = QPushButton("Создать саммари")
        summary_button.setObjectName("secondaryButton")
        
        self.summary_templates = QComboBox()
        self.summary_templates.addItems([
            "Краткое резюме", 
            "Детальный анализ", 
            "Список задач", 
            "Ключевые решения"
        ])
        self.summary_templates.setFixedWidth(180)
        
        # Кнопка истории транскриптов
        history_button = QPushButton("История транскриптов")
        history_button.setObjectName("secondaryButton")
        
        toolbar_layout.addWidget(summary_button)
        toolbar_layout.addWidget(self.summary_templates)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(history_button)
        
        return toolbar_widget
    
    def create_transcript_area(self):
        """Создание области для отображения транскрипции"""
        transcript_area = QTextEdit()
        transcript_area.setObjectName("transcriptArea")
        transcript_area.setReadOnly(True)
        
        # Устанавливаем моноширинный шрифт
        font = QFont("Menlo", 12)
        transcript_area.setFont(font)
        
        # Добавляем пример текста для демонстрации
        sample_text = """[12:34:56] [MIC] Добрый день, коллеги. Давайте начнем наше совещание.
[12:35:03] [SPEAKER] Привет всем! Я предлагаю сегодня обсудить спецификацию нового приложения.
[12:35:12] [MIC] Да, конечно. У нас есть три основных вопроса: интерфейс, архитектура и API-интеграция.
[12:35:25] [SPEAKER] По интерфейсу предлагаю использовать динамические блоки, как мы обсуждали ранее.
[12:35:30] [SYSTEM] Транскрипция активна..."""
        
        transcript_area.setPlainText(sample_text)
        
        # Устанавливаем отступы и настройки отображения
        transcript_area.document().setDocumentMargin(12)
        
        return transcript_area
    
    def create_control_panel(self):
        """Создание панели управления транскрипцией с улучшенной видимостью"""
        control_panel = QFrame()
        control_panel.setObjectName("controlPanel")
        control_panel.setMaximumHeight(70)
        
        control_layout = QHBoxLayout(control_panel)
        
        # Кнопка Старт/Стоп с ясным контрастом
        self.start_button = QPushButton("Начать")
        self.start_button.setObjectName("primaryButton")
        self.start_button.clicked.connect(self.toggle_recording)
        
        self.stop_button = QPushButton("Стоп")
        self.stop_button.setObjectName("dangerButton")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.toggle_recording)
        
        # Дополнительные кнопки с улучшенной видимостью
        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self.clear_transcript)
        
        self.save_button = QPushButton("Сохранить")
        
        self.send_to_ai_button = QPushButton("Отправить в AI")
        self.send_to_ai_button.clicked.connect(self.send_to_ai)
        
        # Добавляем кнопки с достаточным расстоянием между ними
        control_layout.addWidget(self.start_button)
        control_layout.addSpacing(5)
        control_layout.addWidget(self.stop_button)
        control_layout.addStretch()
        control_layout.addWidget(self.clear_button)
        control_layout.addSpacing(5)
        control_layout.addWidget(self.save_button)
        control_layout.addSpacing(5)
        control_layout.addWidget(self.send_to_ai_button)
    
        return control_panel
    
    def toggle_recording(self):
        """Переключение состояния записи"""
        self.is_recording = not self.is_recording
        
        if self.is_recording:
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.add_system_message("Транскрипция активна...")
            # Здесь будет код для запуска транскрипции
        else:
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.add_system_message("Транскрипция остановлена")
            # Здесь будет код для остановки транскрипции
    
    @Slot()
    def clear_transcript(self):
        """Очистка области транскрипции"""
        self.transcript_area.clear()
    
    def add_system_message(self, message):
        """Добавление системного сообщения в транскрипцию"""
        import time
        timestamp = time.strftime("[%H:%M:%S]")
        
        system_msg = f"{timestamp} [SYSTEM] {message}"
        
        cursor = self.transcript_area.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        if not self.transcript_area.toPlainText().endswith('\n') and self.transcript_area.toPlainText():
            cursor.insertText('\n')
        
        cursor.insertText(system_msg)
        self.transcript_area.setTextCursor(cursor)
        self.transcript_area.ensureCursorVisible()
    
    @Slot()
    def send_to_ai(self):
        """Отправка текущей транскрипции в AI-ассистент"""
        transcript_text = self.transcript_area.toPlainText()
        if transcript_text:
            self.transcriptionSent.emit(transcript_text)
            self.add_system_message("Транскрипция отправлена в AI-ассистент")