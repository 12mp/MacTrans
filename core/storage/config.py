import json
import os
from typing import Dict, Any, Optional

class ConfigManager:
    """Класс для управления конфигурацией приложения"""
    
    DEFAULT_CONFIG = {
        "audio": {
            "microphone": "",  # Выбранный микрофон
            "system_audio": "",  # Выбранное устройство системного звука
            "auto_save": True,  # Автоматическое сохранение транскрипции
            "save_path": "",  # Путь для сохранения транскрипций
            "auto_send": False  # Автоматическая отправка в AI ассистент
        },
        "whisper": {
            "model": "base",  # Модель Whisper (tiny, base, small, medium, large)
            "language": "ru",  # Язык транскрипции
            "temperature": 0  # Температура для генерации
        },
        "ai": {
            "provider": "openai",  # Текущий провайдер (openai, claude, local)
            "openai_key": "",  # API ключ OpenAI
            "claude_key": "",  # API ключ Claude
            "model": "",  # Выбранная модель
            "temperature": 0.7,  # Температура для генерации
            "max_tokens": 1000  # Максимальное количество токенов в ответе
        },
        "local_models": {
            "installed": [],  # Список установленных локальных моделей
            "path": ""  # Путь для хранения локальных моделей
        },
        "templates": {
            # Предустановленные шаблоны будут добавлены при первом запуске
        },
        "system_prompt": """
Вот ваша прошлая история переписки с пользователем {messagestory}. 
Отвечай на вопросы пользователя: {usermessage} по транскрипту совещания: {audiotranscript}.
""",
        "ui": {
            "theme": "system",  # Тема интерфейса (system, light, dark)
            "transcript_font_size": "medium",  # Размер шрифта транскрипции
            "chat_mode_default": True  # Активация режима "Общение по транскрипту" по умолчанию
        },
        "format": {
            "transcription": "txt",  # Формат сохранения транскрипции (txt, srt, json)
            "include_timestamps": True,  # Включать временные метки
            "include_sources": True  # Включать источники (MIC/SPEAKER)
        }
    }
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Загрузка конфигурации из файла или создание новой"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Проверяем и дополняем конфигурацию недостающими полями
                for key, value in self.DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                    elif isinstance(value, dict):
                        for subkey, subvalue in value.items():
                            if subkey not in config[key]:
                                config[key][subkey] = subvalue
                
                return config
            else:
                # Если файл не существует, создаем конфигурацию по умолчанию
                return self._create_default_config()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка при загрузке конфигурации: {e}")
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Создание конфигурации по умолчанию"""
        # Добавляем предустановленные шаблоны
        config = self.DEFAULT_CONFIG.copy()
        config["templates"] = {
            "default": {
                "name": "Краткое резюме",
                "description": "Стандартный шаблон для краткого резюме транскрипта",
                "prompt": """
Создай краткое резюме (не более 300 слов) следующего транскрипта встречи:

{audiotranscript}

Выдели 3-5 основных обсуждаемых тем и ключевые решения.
"""
            },
            "detailed": {
                "name": "Детальный анализ",
                "description": "Шаблон для детального анализа транскрипта",
                "prompt": """
Сделай детальный анализ следующего транскрипта встречи:

{audiotranscript}

Структурируй анализ по следующим разделам:
1. Основные темы и вопросы
2. Ключевые аргументы и точки зрения
3. Принятые решения
4. Открытые вопросы, требующие дальнейшего обсуждения
5. Общие выводы и рекомендации
"""
            },
            "tasks": {
                "name": "Список задач",
                "description": "Шаблон для извлечения задач из транскрипта",
                "prompt": """
Извлеки из транскрипта встречи все упомянутые задачи и дела:

{audiotranscript}

Для каждой задачи укажи:
1. Описание задачи
2. Ответственное лицо (если указано)
3. Срок выполнения (если указан)
4. Приоритет (если можно определить)

Представь результат в виде четко структурированного списка задач.
"""
            },
            "decisions": {
                "name": "Ключевые решения",
                "description": "Шаблон для выделения принятых решений",
                "prompt": """
Проанализируй транскрипт встречи и выдели все принятые решения:

{audiotranscript}

Для каждого решения укажи:
1. Суть принятого решения
2. Краткое обоснование
3. Кто выступал за и против (если применимо)
4. Какие следующие шаги были определены

Дополнительно отметь, какие решения требуют дополнительного согласования.
"""
            }
        }
        
        # Сохраняем новую конфигурацию
        self.save_config(config)
        return config
    
    def save_config(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Сохранение конфигурации в файл"""
        try:
            if config is not None:
                self.config = config
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка при сохранении конфигурации: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Получение значения из конфигурации по ключу"""
        # Поддержка вложенных ключей через точку (например, "audio.microphone")
        if "." in key:
            parts = key.split(".")
            value = self.config
            for part in parts:
                if part not in value:
                    return default
                value = value[part]
            return value
        
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Установка значения в конфигурации по ключу"""
        # Поддержка вложенных ключей через точку
        if "." in key:
            parts = key.split(".")
            config = self.config
            
            # Проходим по всем частям ключа, кроме последней
            for part in parts[:-1]:
                if part not in config:
                    config[part] = {}
                config = config[part]
            
            # Устанавливаем значение для последней части ключа
            config[parts[-1]] = value
        else:
            self.config[key] = value
        
        self.save_config()