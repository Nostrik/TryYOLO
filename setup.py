from distutils.core import setup
import py2exe

# Путь к основному скрипту вашего приложения
script = 'C:/Users/Maxim/tv-21-app/my-tv21-app/app.py'

# Настройки сборки
options = {
    'py2exe': {
        'bundle_files': 1,  # Создание одного исполняемого файла
        'compressed': True,  # Сжатие файлов
        'optimize': 2,  # Оптимизация скриптов
        # Другие параметры (если нужно)
    }
}

# Собираем приложение
setup(
    windows=[{'script': script}],
    options=options,
    zipfile=None  # Создание одного исполняемого файла без дополнительных зависимостей
)