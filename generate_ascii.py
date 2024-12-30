from PIL import Image, UnidentifiedImageError

def image_to_ascii(image_path: str, width: int = 80, ratioH: float = 2.5, reversed: bool = False, chars='@%#*+=-:. ') -> str:
    try:
        img = Image.open(image_path)
    except UnidentifiedImageError:
        text_error = 'UnidentifiedImageError'
        return text_error
    
    chars = chars  # Символы для отображения (от плотных к редким)
    if reversed:
        chars = chars[::-1]

    img = img.resize((width, int(img.height * width / img.width / ratioH)))  # Масштабирование
    img = img.convert("L")  # Перевод в оттенки серого

    ascii_art = ""

    for y in range(img.height):
        for x in range(img.width):
            gray = img.getpixel((x, y))  # Уровень серого
            ascii_art += chars[gray * len(chars) // 256]  # Выбор символа
        ascii_art += "\n"

    return ascii_art

def generate_ascii_file(file_name, text, encoding="utf-8"):
    with open(file_name,'w') as f:
        f.write(text)

    # Пример использования
if __name__ == '__main__':
    ascii_art = image_to_ascii("hp.jpg", width=80)
    print(ascii_art)
    generate_ascii_file(file_name="result.txt", text=ascii_art)
