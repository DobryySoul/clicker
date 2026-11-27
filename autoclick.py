
import time
import threading
import pyautogui
import keyboard

# =================================
# НАСТРОЙКИ
# =================================

START_DELAY = 2
HOLD_TIME = 60
SPACE_DELAY = 0.2

# =================================
# СОСТОЯНИЕ
# =================================

running = threading.Event()
shutdown = threading.Event()

worker = None
lock = threading.Lock()


# =================================
# ОСНОВНОЙ ЦИКЛ
# =================================

def automation():
    try:
        print("[START] Автоматизация запущена")

        while running.is_set() and not shutdown.is_set():

            # Ожидание перед началом
            if shutdown.wait(START_DELAY):
                break

            if not running.is_set():
                break

            # Зажимаем ЛКМ
            pyautogui.mouseDown(button="left")
            print("[MOUSE] ЛКМ зажата")

            start_time = time.monotonic()

            # Удерживаем 60 секунд
            while time.monotonic() - start_time < HOLD_TIME:
                if shutdown.is_set() or not running.is_set():
                    break
                time.sleep(0.05)

            # Отпускаем ЛКМ
            pyautogui.mouseUp(button="left")
            print("[MOUSE] ЛКМ отпущена")

            if shutdown.is_set() or not running.is_set():
                break

            # Два нажатия пробела
            pyautogui.press("space")
            time.sleep(SPACE_DELAY)
            pyautogui.press("space")

            print("[KEYBOARD] Двойной пробел")

    except pyautogui.FailSafeException:
        print("[ERROR] Сработала аварийная защита PyAutoGUI")

    finally:
        pyautogui.mouseUp(button="left")
        running.clear()
        print("[STOP] Цикл завершён")


# =================================
# УПРАВЛЕНИЕ
# =================================

def start():
    global worker

    with lock:
        if shutdown.is_set():
            return

        if worker is not None and worker.is_alive():
            print("[INFO] Цикл уже работает или завершается")
            return

        running.set()

        worker = threading.Thread(
            target=automation,
            daemon=True
        )

        worker.start()


def stop():
    running.clear()
    pyautogui.mouseUp(button="left")
    print("[STOP] Остановка запрошена")


def close():
    if shutdown.is_set():
        return

    print("[EXIT] Закрытие программы")

    shutdown.set()
    running.clear()
    pyautogui.mouseUp(button="left")


# =================================
# ГОРЯЧИЕ КЛАВИШИ
# =================================

keyboard.add_hotkey("F6", start)
keyboard.add_hotkey("F7", stop)
keyboard.add_hotkey("F8", close)


# =================================
# ЗАПУСК ПРОГРАММЫ
# =================================

print("===================================")
print("          AUTOCLICKER")
print("===================================")
print("F6 - Запуск")
print("F7 - Остановка")
print("F8 - Выход")
print("===================================")
print("Ожидание команды...")

try:
    while not shutdown.is_set():
        time.sleep(0.2)

except KeyboardInterrupt:
    print("[INFO] Прерывание")

finally:
    shutdown.set()
    running.clear()

    pyautogui.mouseUp(button="left")
    keyboard.unhook_all()

    print("[EXIT] Программа закрыта")
