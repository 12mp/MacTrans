import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QFont

from ui.main_window import MainWindow
from core.storage.config import ConfigManager

# Импортируем PyQtDarkTheme
import qdarktheme

def setup_directories():
    """Создание необходимых директорий для приложения"""
    home_dir = os.path.expanduser("~")
    
    # Директории для данных приложения
    app_support_dir = os.path.join(home_dir, "Library/Application Support/MacTrans")
    docs_dir = os.path.join(home_dir, "Documents/MacTrans")
    transcripts_dir = os.path.join(docs_dir, "Transcripts")
    chats_dir = os.path.join(docs_dir, "Chats")
    
    # Создаем директории, если они не существуют
    for directory in [app_support_dir, docs_dir, transcripts_dir, chats_dir]:
        os.makedirs(directory, exist_ok=True)
    
    return {
        "app_support": app_support_dir,
        "docs": docs_dir,
        "transcripts": transcripts_dir,
        "chats": chats_dir
    }

def main():
    """Основная функция запуска приложения"""
    # Создаем необходимые директории
    directories = setup_directories()
    
    # Инициализируем конфигурацию
    config_path = os.path.join(directories["app_support"], "config.json")
    config_manager = ConfigManager(config_path)
    
    # Устанавливаем высокое DPI для ретина дисплеев
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Создаем приложение
    app = QApplication(sys.argv)
    app.setApplicationName("MacTrans")
    app.setOrganizationName("MacTrans")
    
    # Применяем тему с доработанными стилями для лучшей читаемости
    custom_styles = """
        /* Основные настройки для лучшей читаемости */
        QMainWindow, QDialog {
            background-color: #f7f7f7;
        }
        
        /* Заголовок приложения */
        #appHeader {
            background-color: #ffffff;
            border-bottom: 1px solid #d0d0d0;
        }
        
        #appLogo {
            background-color: #0078d4;
            color: white;
            font-weight: bold;
            border-radius: 6px;
            font-size: 16px;
            qproperty-alignment: AlignCenter;
        }
        
        #appTitle {
            font-size: 18px;
            font-weight: bold;
            color: #202020;
        }
        
        /* Панели */
        #panelHeader {
            background-color: #f7f7f7;
            border-bottom: 1px solid #d0d0d0;
            padding: 5px;
        }
        
        #panelTitle {
            font-weight: bold;
            color: #202020;
            font-size: 15px;
        }
        
        /* Кнопки с четким контрастом */
        QPushButton {
            background-color: #f0f0f0;
            color: #202020;
            border: 1px solid #d0d0d0;
            border-radius: 4px;
            padding: 6px 12px;
            font-weight: normal;
        }
        
        QPushButton:hover {
            background-color: #e0e0e0;
        }
        
        QPushButton#primaryButton {
            background-color: #0078d4;
            color: white;
            border: none;
            font-weight: 500;
        }
        
        QPushButton#primaryButton:hover {
            background-color: #0069c0;
        }
        
        QPushButton#dangerButton {
            background-color: #d9534f;
            color: white;
            border: none;
        }
        
        QPushButton#dangerButton:hover {
            background-color: #c9302c;
        }
        
        /* Чат и сообщения с четким контрастом */
        #userMessage {
            background-color: #0078d4;
            color: white;
            border-radius: 10px;
            border-bottom-right-radius: 2px;
            padding: 8px 12px;
        }
        
        #assistantMessage {
            background-color: #e6e6e6;
            color: #202020;
            border-radius: 10px;
            border-bottom-left-radius: 2px;
            padding: 8px 12px;
        }
        
        #messageTime {
            font-size: 12px;
            color: rgba(255, 255, 255, 0.8);
        }
        
        #assistantMessage #messageTime {
            color: #606060;
        }
        
        /* Поле ввода более заметное */
        #messageInput {
            background-color: white;
            border: 1px solid #c0c0c0;
            border-radius: 6px;
            padding: 8px;
            color: #202020;
        }
        
        /* Кнопка отправки */
        #sendButton {
            background-color: #0078d4;
            color: white;
            border: none;
            border-radius: 50%;
            font-size: 16px;
        }
        
        /* Чекбокс более читаемый */
        QCheckBox {
            color: #202020;
            spacing: 5px;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border: 1px solid #c0c0c0;
            border-radius: 3px;
            background-color: white;
        }
        
        QCheckBox::indicator:checked {
            background-color: #0078d4;
            border-color: #0078d4;
        }
        
        /* Выпадающий список более читаемый */
        QComboBox {
            background-color: white;
            border: 1px solid #c0c0c0;
            border-radius: 4px;
            padding: 4px 8px;
            color: #202020;
            selection-background-color: #0078d4;
        }
        
        /* Область транскрипции */
        #transcriptArea {
            background-color: white;
            color: #202020;
            border: 1px solid #e0e0e0;
            font-family: 'Menlo', monospace;
            font-size: 13px;
            padding: 5px;
        }
        
        /* Статусная строка */
        QStatusBar {
            background-color: #f7f7f7;
            color: #505050;
            border-top: 1px solid #d0d0d0;
        }
        
        /* Индикатор статуса */
        #statusIndicator {
            color: #909090;
            font-size: 14px;
        }
        
        #statusIndicator.active {
            color: #4CAF50;
        }
        
        /* Селектор чата и индикаторы */
        #chatSelector, #modelIndicator {
            background-color: #f0f0f0;
            color: #202020;
            border: 1px solid #d0d0d0;
            border-radius: 4px;
            padding: 4px 8px;
        }
        
        /* Сплиттер */
        QSplitter::handle {
            background-color: #d0d0d0;
        }
        
        /* Полоса прокрутки */
        QScrollBar:vertical {
            border: none;
            background: #f0f0f0;
            width: 10px;
            border-radius: 5px;
        }
        
        QScrollBar::handle:vertical {
            background: #c0c0c0;
            border-radius: 5px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: #a0a0a0;
        }
    """
    
    # Применяем светлую тему с улучшенными стилями
    qdarktheme.setup_theme(theme="light", custom_colors={"primary": "#0078d4"}, additional_qss=custom_styles)
    
    # Установим системный шрифт с хорошей читаемостью
    app.setFont(QFont(".AppleSystemUIFont", 12))
    
    # Создаем и показываем главное окно
    window = MainWindow(config_manager, directories)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()