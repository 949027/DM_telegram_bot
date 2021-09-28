# Телеграм-бот по обмену вещей

Бот предоставляет бесплатный сервис обмена вещами между пользователями.

### Как установить

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
```python
pip install -r requirements.txt
```

### Как запустить

Запустите main.py:
```python
python3 main.py
```
Рекомендуется использовать [virtualenv/venv] (https://docs.python.org/3/library/venv.html) для изоляции проекта

### Как пользоваться

1. Нажмите кнопку СТАРТ
2. Добавьте хотя бы одну вещь - загрузите фото и введите название вещи
3. Теперь можно приступить к поиску вещей.
Нажмите НАЙТИ ВЕЩЬ и выберите категорию.
4. При каждом запросе будет выводиться одна вещь.
Сначала Вам продемонстрируются вещи пользователей, которым понравилась одна из Ваших вещей, затем - в случайном порядке.
5. Нажмите ОБМЕНЯТЬСЯ под понравившейся вещью.
Если владелец вещи ранее интересовался или заинтересуется одной из Ваших вещей - Вам обоим придет сообщение с контактами (@Username).
