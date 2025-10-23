# Mini Games Collection

Коллекция мини-игр, созданная на движке Ren'Py. Проект включает в себя несколько аркадных игр с простым управлением и увлекательным геймплеем.

## 🎮 Список игр

### 1. Space Shooter (Galaga Style)
Классический космический шутер в стиле Galaga 1981 года.

**Особенности:**
- Формации врагов с синхронным движением
- Атаки пикированием
- Система волн с возрастающей сложностью
- Счет очков и система жизней
- Стрельба из двух орудий

**Управление:**
- `W/↑` - Вверх
- `S/↓` - Вниз
- `A/←` - Влево
- `D/→` - Вправо
- `SPACE/E` - Стрельба из обоих орудий
- `Q` - Стрельба из левого орудия

## 📁 Структура проекта

```
TestIMatic/
├── game/
│   ├── script.rpy           # Главное меню и точка входа
│   ├── space_shooter.rpy    # Игра Space Shooter
│   ├── images/              # Графические ресурсы
│   │   ├── bgBlack.jpg
│   │   ├── bgSpaceBackground.jpg
│   │   ├── PlayerShipStill1.png
│   │   ├── PlayerShipStill2.png
│   │   ├── PlayerShipStill3.png
│   │   └── virus-36904.png
│   └── ...
├── README.md
└── ...
```

## 🚀 Запуск

1. Убедитесь, что установлен [Ren'Py SDK](https://www.renpy.org/latest.html)
2. Откройте Ren'Py Launcher
3. Добавьте проект через "preferences" → "Projects Directory"
4. Выберите проект "TestIMatic" в списке
5. Нажмите "Launch Project"

## 🛠️ Разработка

### Добавление новой игры

1. Создайте новый файл `game/your_game.rpy`
2. Определите переменные игры через `default`
3. Создайте логику игры в блоке `init python:`
4. Создайте экраны для отрисовки (screens)
5. Создайте точку входа `label game_your_game:`
6. Добавьте кнопку в главное меню (`script.rpy`)

### Пример структуры новой игры:

```renpy
# Переменные
default score = 0

# Логика
init python:
    def ResetGame():
        global score
        score = 0

# Экраны
screen game_screen():
    text "Score: [score]"

# Точка входа
label game_your_game:
    $ ResetGame()
    show screen game_screen
    $ renpy.pause(hard=True)
```

## ⚙️ Конфигурация

Основные настройки находятся в `script.rpy`:

```renpy
define config.has_quicksave = False      # Отключить быстрые сохранения
define config.has_autosave = False       # Отключить автосохранение
define config.autosave_on_quit = False   # Не сохранять при выходе
define config.autosave_on_choice = False # Не сохранять при выборе
```

## 🎨 Ресурсы

### Графика
- Фоны: 1920x1080 px
- Спрайты кораблей: ~128x128 px
- Спрайты врагов: ~64x64 px

### Анимации
- Анимация двигателя корабля: 3 кадра по 0.1 секунды
- Частота обновления игры: 50 FPS (timer 0.02)

## 🐛 Известные проблемы

- При изменении кода может потребоваться удаление старых сохранений из `%APPDATA%\RenPy\TestIMatic`
- Для корректной работы требуется Ren'Py версии 8.0+

## 📝 TODO

- [ ] Добавить звуковые эффекты
- [ ] Добавить музыку
- [ ] Реализовать Game 2
- [ ] Реализовать Game 3
- [ ] Добавить паузу во время игры

## 🔗 Ссылки

- **GitHub Repository:** https://github.com/kioshini/wooks_team_project
- **Ren'Py Engine:** https://www.renpy.org/

## 👨‍💻 Разработка

**Движок:** Ren'Py 8.4.1+  
**Язык:** Ren'Py Script Language + Python 