import cv2
import numpy as np
import os


def show_image(title, image):
    """Отображение изображения с обработкой ошибок"""
    if image is None or not isinstance(image, np.ndarray):
        print("Ошибка: некорректное изображение")
        return

    try:
        cv2.namedWindow(title, cv2.WINDOW_NORMAL)
        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyWindow(title)
    except Exception as e:
        print(f"Ошибка отображения: {str(e)}")


def select_image():
    """Выбор изображения с обработкой ошибок камеры"""
    while True:
        print("\n1. Загрузить изображение")
        print("2. Сделать снимок с камеры")
        print("0. Назад")

        choice = input("Выберите источник: ")

        if choice == "0":
            return None

        if choice == "1":
            path = input("Введите путь к изображению: ").strip()
            if not os.path.exists(path):
                print("Файл не найден!")
                continue

            img = cv2.imread(path)
            if img is None:
                print("Некорректный файл изображения!")
                continue

            print(f"Успешно загружено: {img.shape[1]}x{img.shape[0]} пикселей")
            return img

        elif choice == "2":
            # Отключаем логирование (альтернативный способ)
            cv2.setNumThreads(0)  # Уменьшаем количество потоков

            cap = cv2.VideoCapture(0)  # Убрали CAP_DSHOW для совместимости

            if not cap.isOpened():
                print("Камера недоступна! Проверьте:")
                print("- Подключение камеры")
                print("- Разрешения антивируса")
                continue

            print("Нажмите ПРОБЕЛ для снимка, ESC для отмены")
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Ошибка захвата кадра")
                    break

                cv2.imshow("Камера - ПРОБЕЛ:снимок ESC:отмена", frame)
                key = cv2.waitKey(1)

                if key == 27:  # ESC
                    break
                elif key == 32:  # ПРОБЕЛ
                    cap.release()
                    cv2.destroyAllWindows()
                    return frame

            cap.release()
            cv2.destroyAllWindows()

        else:
            print("Некорректный выбор!")


def show_color_channel(image):
    """Показ выбранного цветового канала"""
    print("\nДоступные каналы:")
    print("1 - Красный (R)")
    print("2 - Зеленый (G)")
    print("3 - Синий (B)")

    try:
        channel = int(input("Выберите канал (1-3): "))
        if channel not in [1, 2, 3]:
            raise ValueError

        # Создаем пустые каналы
        zeros = np.zeros_like(image[:, :, 0])

        if channel == 1:  # Красный
            result = cv2.merge([zeros, zeros, image[:, :, 2]])
        elif channel == 2:  # Зеленый
            result = cv2.merge([zeros, image[:, :, 1], zeros])
        else:  # Синий
            result = cv2.merge([image[:, :, 0], zeros, zeros])

        show_image("Цветовой канал", result)

    except ValueError:
        print("Ошибка: введите число от 1 до 3")


def highlight_red(image):
    """Выделение красных областей по порогу"""
    try:
        threshold = int(input("Введите порог для красного (0-255): "))
        if not 0 <= threshold <= 255:
            raise ValueError

        # Получаем только красный канал
        red_channel = image[:, :, 2]

        # Создаем маску (белые пиксели где красный > порога)
        mask = np.where(red_channel > threshold, 255, 0).astype(np.uint8)

        # Преобразуем маску в 3-канальное изображение
        result = cv2.merge([mask, mask, mask])

        show_image("Маска красных областей", result)

    except ValueError:
        print("Ошибка: введите целое число от 0 до 255")


def sharpen_image(image):
    """Увеличение резкости изображения"""
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])
    sharpened = cv2.filter2D(image, -1, kernel)
    show_image("Увеличение резкости", sharpened)


def draw_green_line(image):
    """Рисование зеленой линии"""
    try:
        print("\nВведите координаты линии:")
        x1 = int(input("X начальной точки: "))
        y1 = int(input("Y начальной точки: "))
        x2 = int(input("X конечной точки: "))
        y2 = int(input("Y конечной точки: "))
        thickness = int(input("Толщина линии (1-10): "))

        if thickness < 1 or thickness > 10:
            print("Толщина должна быть от 1 до 10")
            return

        # Создаем копию изображения
        result = image.copy()

        # Рисуем зеленую линию (BGR: 0,255,0)
        cv2.line(result, (x1, y1), (x2, y2), (0, 255, 0), thickness)

        show_image("Изображение с линией", result)

    except ValueError:
        print("Ошибка: введите целые числа")


def main():
    print("=== РЕДАКТОР ИЗОБРАЖЕНИЙ ===")
    print("Версия 2.1 - Совместимость с OpenCV 4.5.5")

    while True:
        print("\nГЛАВНОЕ МЕНЮ:")
        print("1. Показать цветовой канал")
        print("2. Выделить красные области")
        print("3. Увеличить резкость")
        print("4. Нарисовать линию")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "0":
            print("Завершение работы...")
            cv2.destroyAllWindows()
            break

        image = select_image()
        if image is None:
            continue

        show_image("Исходное изображение", image)

        if choice == "1":
            show_color_channel(image)
        elif choice == "2":
            highlight_red(image)
        elif choice == "3":
            sharpen_image(image)
        elif choice == "4":
            draw_green_line(image)
        else:
            print("Некорректный выбор!")


if __name__ == "__main__":
    main()