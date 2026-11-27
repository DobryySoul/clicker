import random  # Обязательно добавьте этот импорт в начало файла

def automation():
    try:
        print("[START] Автоматизация запущена")

        while running.is_set() and not shutdown.is_set():

            # Небольшой случайный сдвиг курсора (на 1-3 пикселя), чтобы клики не были в одну точку
            dx = random.randint(-3, 3)
            dy = random.randint(-3, 3)
            pyautogui.moveRel(dx, dy, duration=random.uniform(0.05, 0.15))

            # 1. Короткий клик ЛКМ с человеческой длительностью нажатия
            pyautogui.mouseDown(button="left")
            time.sleep(random.uniform(0.06, 0.14))
            pyautogui.mouseUp(button="left")
            print("[MOUSE] Короткий клик ЛКМ")

            # 2. Ожидание ~2 секунды (от 1.8 до 2.3 сек)
            wait_time = random.uniform(1.8, 2.3)
            if shutdown.wait(wait_time) or not running.is_set():
                break

            # 3. Зажатие ЛКМ на ~60 секунд (от 58.5 до 62.0 сек)
            hold_duration = random.uniform(58.5, 62.0)
            pyautogui.mouseDown(button="left")
            print(f"[MOUSE] ЛКМ зажата на {hold_duration:.1f} секунд")

            start_time = time.monotonic()

            while time.monotonic() - start_time < hold_duration:
                if shutdown.is_set() or not running.is_set():
                    break
                time.sleep(0.05)

            # 4. Обязательно отпускаем ЛКМ
            pyautogui.mouseUp(button="left")
            print("[MOUSE] ЛКМ отпущена")

            if shutdown.is_set() or not running.is_set():
                break

            # Небольшая пауза перед пробелом (от 0.15 до 0.4 сек)
            if shutdown.wait(random.uniform(0.15, 0.4)) or not running.is_set():
                break

            # 5. Нажатие пробела с естественной длительностью удержания клавиши
            pyautogui.keyDown("space")
            time.sleep(random.uniform(0.07, 0.16))
            pyautogui.keyUp("space")
            print("[KEYBOARD] Пробел")

            # Пауза перед началом следующего цикла (от 0.4 до 0.9 сек)
            if shutdown.wait(random.uniform(0.4, 0.9)) or not running.is_set():
                break

    finally:
        pyautogui.mouseUp(button="left")
        pyautogui.keyUp("space")  # На всякий случай отпускаем и пробел при экстренной остановке
        running.clear()
        print("[STOP] Цикл завершён")
