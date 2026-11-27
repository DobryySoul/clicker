
import random
import time
import threading
import pyautogui
import keyboard

running = threading.Event()
shutdown = threading.Event()


def interruptible_wait(duration):
    """Ожидание с возможностью немедленной остановки."""
    return shutdown.wait(duration) or not running.is_set()


def automation():
    try:
        print("[START] Автоматизация начнётся через 5 секунд...")

        if interruptible_wait(5):
            return

        original_x, original_y = pyautogui.position()

        print("[START] Автоматизация запущена")

        while running.is_set() and not shutdown.is_set():

            # Случайное, более заметное перемещение курсора
            current_x, current_y = pyautogui.position()

            while True:
                target_x = original_x + random.randint(-60, 60)
                target_y = original_y + random.randint(-45, 45)

                distance = ((target_x - current_x) ** 2 +
                            (target_y - current_y) ** 2) ** 0.5

                if distance >= 25:
                    break

            pyautogui.moveTo(
                target_x,
                target_y,
                duration=random.uniform(0.3, 0.5)
            )

            if not running.is_set() or shutdown.is_set():
                break

            # 1. Удержание ЛКМ + случайное нажатие Mouse 4
            click_duration = random.uniform(0.4, 0.87)

            pyautogui.mouseDown(button="left")

            print(f"[MOUSE] ЛКМ зажата на {click_duration:.2f} сек")

            # Случайный момент нажатия Mouse 4 внутри удержания ЛКМ
            mouse4_delay = random.uniform(0.05, max(0.05, click_duration - 0.1))

            if interruptible_wait(mouse4_delay):
                break

            pyautogui.mouseDown(button="x1")
            print("[MOUSE] Mouse 4 нажата")

            if interruptible_wait(click_duration - mouse4_delay):
                break

            pyautogui.mouseUp(button="x1")
            pyautogui.mouseUp(button="left")

            print("[MOUSE] ЛКМ и Mouse 4 отпущены")

            # 2. Пауза около 2 секунд
            wait_time = random.uniform(1.8, 2.3)

            if interruptible_wait(wait_time):
                break

            # 3. Длительное удержание ЛКМ
            hold_duration = random.uniform(58.5, 62.0)
            right_click_duration = random.uniform(2.7, 3.3)

            pyautogui.mouseDown(button="left")

            print(
                f"[MOUSE] ЛКМ + SHIFT: "
                f"{hold_duration:.2f} сек"
            )

            start_time = time.monotonic()
            right_click_done = False

            while time.monotonic() - start_time < hold_duration:

                if shutdown.is_set() or not running.is_set():
                    break

                elapsed = time.monotonic() - start_time
                remaining = hold_duration - elapsed

                # 4. ПКМ в последние 3 секунды
                if not right_click_done and remaining <= right_click_duration:

                    pyautogui.mouseDown(button="right")
                    right_click_done = True

                    print(
                        f"[MOUSE] ПКМ зажата: "
                        f"{right_click_duration:.2f} сек"
                    )

                time.sleep(0.05)

            # Отпускание всех кнопок после длительного удержания
            pyautogui.mouseUp(button="right")
            pyautogui.mouseUp(button="left")

            print("[MOUSE] ЛКМ, ПКМ и SHIFT отпущены")

            if shutdown.is_set() or not running.is_set():
                break

            # 5. Небольшая пауза перед пробелом
            if interruptible_wait(random.uniform(0.15, 0.4)):
                break

            # 6. Нажатие пробела
            pyautogui.keyDown("space")
            print("[KEYBOARD] Пробел")

            if interruptible_wait(random.uniform(0.07, 0.16)):
                break

            pyautogui.keyUp("space")

            # 7. Пауза перед следующим циклом
            if interruptible_wait(random.uniform(0.4, 0.9)):
                break

    finally:
        # Гарантированное отпускание всех кнопок
        pyautogui.mouseUp(button="left")
        pyautogui.mouseUp(button="right")
        pyautogui.keyUp("space")
        pyautogui.mouseUp(button="x1")

        running.clear()

        print("[STOP] Цикл завершён")


def start():
    if shutdown.is_set():
        return

    if not running.is_set():
        running.set()

        threading.Thread(
            target=automation,
            daemon=True
        ).start()

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
    pyautogui.mouseUp(button="right")
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
