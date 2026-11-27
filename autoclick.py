
import random
import time
import threading
import pyautogui
import keyboard

running = threading.Event()
shutdown = threading.Event()


def automation():
    try:
        print("[START] Автоматизация запущена")

        while running.is_set() and not shutdown.is_set():

            dx = random.randint(-3, 3)
            dy = random.randint(-3, 3)
            pyautogui.moveRel(dx, dy, duration=random.uniform(0.05, 0.15))

            # 1. Короткий клик ЛКМ
            pyautogui.mouseDown(button="left")
            time.sleep(random.uniform(0.06, 0.14))
            pyautogui.mouseUp(button="left")
            print("[MOUSE] Короткий клик ЛКМ")

            # 2. Ожидание около 2 секунд
            wait_time = random.uniform(1.8, 2.3)
            if shutdown.wait(wait_time) or not running.is_set():
                break

            # 3. Зажатие ЛКМ
            hold_duration = random.uniform(58.5, 62.0)
            pyautogui.mouseDown(button="left")
            print(f"[MOUSE] ЛКМ зажата на {hold_duration:.1f} секунд")

            start_time = time.monotonic()

            while time.monotonic() - start_time < hold_duration:
                if shutdown.is_set() or not running.is_set():
                    break
                time.sleep(0.05)

            # 4. Отпускаем ЛКМ
            pyautogui.mouseUp(button="left")
            print("[MOUSE] ЛКМ отпущена")

            if shutdown.is_set() or not running.is_set():
                break

            if shutdown.wait(random.uniform(0.15, 0.4)) or not running.is_set():
                break

            # 5. Нажатие пробела
            pyautogui.keyDown("space")
            time.sleep(random.uniform(0.07, 0.16))
            pyautogui.keyUp("space")
            print("[KEYBOARD] Пробел")

            # 6. Пауза перед следующим циклом
            if shutdown.wait(random.uniform(0.4, 0.9)) or not running.is_set():
                break

    finally:
        pyautogui.mouseUp(button="left")
        pyautogui.keyUp("space")
        running.clear()
        print("[STOP] Цикл завершён")


def start():
    if shutdown.is_set():
        return

    if not running.is_set():
        running.set()
        threading.Thread(target=automation, daemon=True).start()
        print("[CONTROL] Запуск по F6")


def stop():
    if running.is_set():
        running.clear()
        print("[CONTROL] Остановка по F7")


def exit_program():
    print("[CONTROL] Выход по F8")
    running.clear()
    shutdown.set()
    pyautogui.mouseUp(button="left")
    pyautogui.keyUp("space")


# Регистрация горячих клавиш
keyboard.add_hotkey("F6", start)
keyboard.add_hotkey("F7", stop)
keyboard.add_hotkey("F8", exit_program)

print("================================")
print("       AUTOMATION CONTROL")
print("================================")
print("[F6] Запуск")
print("[F7] Остановка")
print("[F8] Выход")
print("================================")
print("Ожидание команды..")

# Ожидание выхода
shutdown.wait()

keyboard.unhook_all()
print("[EXIT] Программа завершена")
