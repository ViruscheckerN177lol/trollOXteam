# -*- coding: utf-8 -*-
"""
TROLL SCRIPT v2
- ASCII-арт "OXTEAM"
- Бегущая строка с текстом
- Разноцветные цвета
- Фоновая музыка (если есть файл music.wav рядом)
- Бесконечный цикл, бегущая строка стартует через 10 минут
"""

import os
import sys
import time
import ctypes
import threading
import winsound

# ================== НАСТРОЙКИ ==================
TITLE = "OXTEAM"
DELAY = 0.25                    # скорость смены цвета
SCROLL_DELAY = 0.08             # скорость бегущей строки
TICKER_START_AFTER = 600        # через сколько секунд включится бегущая строка (600 = 10 мин)

TICKER_TEXT = (
    "  ★ OXTEAM ★ OXTEAM ★ OXTEAM ★ OXTEAM ★ OXTEAM ★  "
    "  ЛУЧШАЯ КОМАНДА ★ ЛУЧШАЯ КОМАНДА ★  "
    "  OXTEAM FOREVER ★ OXTEAM FOREVER ★  "
)

# ASCII-арт OXTEAM (большой)
ASCII_ART = r"""
 ██████╗ ██╗  ██╗████████╗███████╗ █████╗ ███╗   ███╗
██╔═══██╗╚██╗██╔╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
██║   ██║ ╚███╔╝    ██║   █████╗  ███████║██╔████╔██║
██║   ██║ ██╔██╗    ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║
╚██████╔╝██╔╝ ██╗   ██║   ███████╗██║  ██║██║ ╚═╝ ██║
 ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
"""

# Цвета: ярко-красный, жёлтый, зелёный, голубой, синий, фиолетовый, ярко-белый
COLORS = [12, 14, 10, 11, 9, 13, 15]

# ================== WINAPI ==================
kernel32 = ctypes.windll.kernel32
user32 = ctypes.windll.user32
STD_OUTPUT_HANDLE = -11


def set_color(c):
    kernel32.SetConsoleTextAttribute(kernel32.GetStdHandle(STD_OUTPUT_HANDLE), c)


def clear():
    os.system("cls")


def maximize():
    hwnd = kernel32.GetConsoleWindow()
    user32.ShowWindow(hwnd, 3)


# ================== МУЗЫКА ==================
def play_music():
    """Играет music.wav из папки со скриптом по кругу."""
    base = os.path.dirname(os.path.abspath(sys.argv[0]))
    path = os.path.join(base, "music.wav")
    if os.path.exists(path):
        while True:
            try:
                winsound.PlaySound(path, winsound.SND_FILENAME)
            except Exception:
                break
    else:
        # Если файла нет — просто пищим "фоновый бит"
        while True:
            try:
                winsound.Beep(600, 150)
                time.sleep(0.05)
                winsound.Beep(900, 150)
                time.sleep(0.5)
            except Exception:
                break


# ================== БЕГУЩАЯ СТРОКА ==================
ticker_running = False  # флаг: включать ли бегущую строку


def ticker_worker():
    """Бегущая строка — включается только через TICKER_START_AFTER секунд."""
    global ticker_running
    time.sleep(TICKER_START_AFTER)
    ticker_running = True

    pos = 0
    width = 80
    text = TICKER_TEXT * 3
    while True:
        if not ticker_running:
            time.sleep(0.2)
            continue
        line = (text * 2)[pos:pos + width]
        # Курсор вниз экрана, чтобы не сбивать арт
        try:
            sys.stdout.write("\033[s")           # сохранить позицию (не везде работает)
            print(f"\n\n\n\n  {line}")
            sys.stdout.write("\033[u")
        except Exception:
            pass
        pos = (pos + 1) % len(text)
        time.sleep(SCROLL_DELAY)


# ================== ОСНОВНОЙ ЦИКЛ ==================
def main():
    kernel32.SetConsoleTitleW(TITLE)
    os.system("mode con: cols=100 lines=35")
    time.sleep(0.6)
    maximize()

    # Фоновая музыка в отдельном потоке
    threading.Thread(target=play_music, daemon=True).start()
    # Бегущая строка — тоже в отдельном потоке (включится через 10 минут)
    threading.Thread(target=ticker_worker, daemon=True).start()

    i = 0
    try:
        while True:
            # Цвет каждые DELAY сек
            set_color(COLORS[i % len(COLORS)])
            clear()
            print(ASCII_ART)
            print("                     ★  O X T E A M  ★")
            print()

            # Если бегущая строка уже "включена" — показываем её здесь же
            if ticker_running:
                text = TICKER_TEXT * 4
                offset = int(time.time() * 10) % len(TICKER_TEXT)
                line = text[offset:offset + 90]
                print(f"\n\n\n  {line}")

            time.sleep(DELAY)
            i += 1

    except KeyboardInterrupt:
        set_color(7)
        clear()
        print("Выход...")


if __name__ == "__main__":
    main()