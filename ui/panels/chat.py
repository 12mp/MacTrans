from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QTextEdit, QCheckBox, QFrame, QScrollArea, QSizePolicy,
    QToolButton, QSpacerItem
)
from PySide6.QtCore import Qt, Signal, Slot, QEvent
from PySide6.QtGui import QFont, QColor, QIcon, QTextCursor

class ChatPanel(QWidget):
    """Панель AI-ассистента с интерфейсом чата"""
    
    messageSent = Signal(str, bool)  # Сигнал отправки сообщения (текст, использовать_транскрипт)
    
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.transcript_mode = True  # Режим "Общение по транскрипту"
        
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка интерфейса панели"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Заголовок панели
        self.header = self.create_header()
        layout.addWidget(self.header)
        
        # Область чата со скроллингом
        self.chat_container = QScrollArea()
        self.chat_container.setWidgetResizable(True)
        self.chat_container.setFrameShape(QFrame.NoFrame)
        
        self.chat_widget = QWidget()
        self.chat_widget.setObjectName("chatWidget")
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setContentsMargins(16, 16, 16, 16)
        self.chat_layout.setSpacing(16)
        
        self.chat_container.setWidget(self.chat_widget)
        layout.addWidget(self.chat_container)
        
        # Панель ввода сообщения
        self.input_panel = self.create_input_panel()
        layout.addWidget(self.input_panel)
        
        # Добавляем примеры сообщений
        self.add_sample_messages()
        
        # Настраиваем обработку клавиш для поля ввода
        self.message_input.installEventFilter(self)
    
    def create_header(self):
        """Создание заголовка панели с улучшенной видимостью"""
        header = QFrame()
        header.setObjectName("panelHeader")
        header.setMaximumHeight(48)
        
        header_layout = QHBoxLayout(header)
        
        # Заголовок с лучшей видимостью
        title = QLabel("AI Ассистент")
        title.setObjectName("panelTitle")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Кнопка выбора чата
        chat_selector = QPushButton("Текущий чат")
        chat_selector.setObjectName("chatSelector")
        header_layout.addWidget(chat_selector)
        
        # Индикатор текущей модели с лучшей видимостью
        self.model_indicator = QLabel("GPT-4o")
        self.model_indicator.setObjectName("modelIndicator")
        header_layout.addWidget(self.model_indicator)
        
        # Кнопка сворачивания
        collapse_button = QToolButton()
        collapse_button.setText("▼")
        collapse_button.setObjectName("collapseButton")
        header_layout.addWidget(collapse_button)
        
        return header
    
    def create_input_panel(self):
        """Создание панели ввода сообщения с улучшенной видимостью"""
        input_panel = QFrame()
        input_panel.setObjectName("inputPanel")
        
        input_layout = QVBoxLayout(input_panel)
        input_layout.setContentsMargins(10, 10, 10, 10)
        
        # Чекбокс для режима "Общение по транскрипту" с лучшей видимостью
        mode_layout = QHBoxLayout()
        self.transcript_mode_checkbox = QCheckBox("Общение по транскрипту")
        self.transcript_mode_checkbox.setChecked(self.transcript_mode)
        self.transcript_mode_checkbox.stateChanged.connect(self.toggle_transcript_mode)
        
        mode_layout.addWidget(self.transcript_mode_checkbox)
        mode_layout.addStretch()
        
        input_layout.addLayout(mode_layout)
        
        # Область ввода сообщения и кнопка отправки
        message_layout = QHBoxLayout()
        
        self.message_input = QTextEdit()
        self.message_input.setObjectName("messageInput")
        self.message_input.setPlaceholderText("Введите сообщение...")
        self.message_input.setMaximumHeight(100)
        self.message_input.textChanged.connect(self.adjust_input_height)
        
        self.send_button = QPushButton("→")
        self.send_button.setObjectName("sendButton")
        self.send_button.setFixedSize(40, 40)
        self.send_button.clicked.connect(self.send_message)
        
        message_layout.addWidget(self.message_input)
        message_layout.addWidget(self.send_button)
        
        input_layout.addLayout(message_layout)
        
        return input_panel
    
    def adjust_input_height(self):
        """Регулировка высоты поля ввода в зависимости от содержимого"""
        document_height = self.message_input.document().size().height()
        
        # Устанавливаем высоту в зависимости от содержимого
        # с ограничением по максимальной высоте
        new_height = min(document_height + 20, 100)
        self.message_input.setMinimumHeight(max(new_height, 40))
    
    def eventFilter(self, obj, event):
        """Фильтр событий для обработки нажатий клавиш"""
        if obj is self.message_input and event.type() == QEvent.KeyPress:
            key_event = event
            
            # Enter без Shift отправляет сообщение
            if (key_event.key() == Qt.Key_Return or key_event.key() == Qt.Key_Enter) and not key_event.modifiers() & Qt.ShiftModifier:
                self.send_message()
                return True
                
            # Shift+Enter добавляет перенос строки
            elif (key_event.key() == Qt.Key_Return or key_event.key() == Qt.Key_Enter) and key_event.modifiers() & Qt.ShiftModifier:
                cursor = self.message_input.textCursor()
                cursor.insertText("\n")
                return True
                
        return super().eventFilter(obj, event)
    
    @Slot(int)
    def toggle_transcript_mode(self, state):
        """Переключение режима 'Общение по транскрипту'"""
        self.transcript_mode = bool(state)
    
    @Slot()
    def send_message(self):
        """Отправка сообщения"""
        message_text = self.message_input.toPlainText().strip()
        if message_text:
            # Добавляем сообщение пользователя в чат
            self.add_user_message(message_text)
            
            # Отправляем сигнал с сообщением
            self.messageSent.emit(message_text, self.transcript_mode)
            
            # Очищаем поле ввода
            self.message_input.clear()
            
            # В реальном приложении здесь будет код для получения ответа от AI
            # Пока просто добавляем заглушку-ответ
            import time
            time.sleep(0.5)  # Имитация задержки ответа
            response = "Это временный ответ AI-ассистента. В полной версии здесь будет ответ от выбранной модели."
            self.add_assistant_message(response)
    
    def add_user_message(self, message_text):
        """Добавление сообщения пользователя в чат"""
        message_widget = self.create_message_widget(message_text, is_user=True)
        self.chat_layout.addWidget(message_widget)
        self.scroll_to_bottom()
    
    def add_assistant_message(self, message_text):
        """Добавление сообщения ассистента в чат"""
        message_widget = self.create_message_widget(message_text, is_user=False)
        self.chat_layout.addWidget(message_widget)
        self.scroll_to_bottom()
    
    def create_message_widget(self, message_text, is_user=False):
        """Создание виджета сообщения с улучшенной читаемостью"""
        message_frame = QFrame()
        message_frame.setObjectName("userMessage" if is_user else "assistantMessage")
        
        message_layout = QVBoxLayout(message_frame)
        message_layout.setContentsMargins(10, 10, 10, 8)
        message_layout.setSpacing(4)
        
        # Добавляем текст сообщения с улучшенной читаемостью
        message_label = QLabel(message_text)
        message_label.setWordWrap(True)
        message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        # Устанавливаем минимальную и максимальную ширину
        message_label.setMinimumWidth(80)
        message_label.setMaximumWidth(400)
        
        # Улучшаем шрифт для читаемости
        font = message_label.font()
        font.setPointSize(13)
        message_label.setFont(font)
        
        message_layout.addWidget(message_label)
        
        # Добавляем время сообщения с лучшей видимостью
        import time
        timestamp = time.strftime("%H:%M")
        time_label = QLabel(timestamp)
        time_label.setObjectName("messageTime")
        time_label.setAlignment(Qt.AlignRight)
        message_layout.addWidget(time_label)
        
        # Устанавливаем выравнивание в зависимости от типа сообщения
        align_layout = QHBoxLayout()
        align_layout.setContentsMargins(0, 0, 0, 0)
        
        if is_user:
            align_layout.addStretch()
            align_layout.addWidget(message_frame)
        else:
            align_layout.addWidget(message_frame)
            align_layout.addStretch()
        
        align_widget = QWidget()
        align_widget.setLayout(align_layout)
        
        return align_widget
    
    def scroll_to_bottom(self):
        """Прокрутка чата вниз"""
        vbar = self.chat_container.verticalScrollBar()
        vbar.setValue(vbar.maximum())
    
    def add_sample_messages(self):
        """Добавление примеров сообщений для демонстрации"""
        self.add_user_message("Проанализируй, пожалуйста, текущий транскрипт и выдели основные обсуждаемые темы.")
        
        response = """На основе предоставленного транскрипта, я могу выделить следующие основные темы обсуждения:

1. Начало совещания и организационные вопросы
2. Обсуждение спецификации нового приложения
3. Планирование обсуждения трех ключевых вопросов: интерфейс, архитектура и API-интеграция
4. Конкретное предложение по интерфейсу — использование динамических блоков

Транскрипт довольно короткий, поэтому дальнейшее обсуждение этих тем пока не зафиксировано."""
        
        self.add_assistant_message(response)