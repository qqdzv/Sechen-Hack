import torch
from PIL import Image
import torchvision.transforms as transforms
import segmentation_models_pytorch as smp
import matplotlib.pyplot as plt
import io
import base64
import string
import random
import os


plt.switch_backend('Agg')

def png_to_base64(png_file_path):
    # Открываем изображение
    with Image.open(png_file_path) as image:
        # Создаем объект BytesIO для хранения бинарных данных изображения
        buffered = io.BytesIO()
        # Сохраняем изображение в формате PNG в объекте BytesIO
        image.save(buffered, format="PNG")
        # Получаем бинарные данные изображения
        img_bytes = buffered.getvalue()
        # Кодируем данные в Base64
        img_base64 = f"data:image/png;base64,{base64.b64encode(img_bytes).decode('utf-8')}"
    return img_base64

def generate_random_string(length=15):
    letters = string.ascii_letters  # Содержит как заглавные, так и строчные буквы
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string

def get_segmentation(image_base64 : str) -> str:
    model_path = os.path.join(os.path.dirname(__file__), 'model_checkpoint.pth')
    checkpoint = torch.load(model_path, map_location=torch.device("cpu"))
    model = smp.UnetPlusPlus(
        encoder_name=checkpoint["config"]["encoder_name"],
        encoder_weights=None,
        in_channels=checkpoint["config"]["in_channels"],
    )
    model.load_state_dict(checkpoint["model_state_dict"])

    if image_base64.startswith("data:image/jpeg;base64,"):
        image_base64 = image_base64.split(",")[1]
    if image_base64.startswith("data:image/png;base64,"):
        image_base64 = image_base64.split(",")[1]

    # Декодируем Base64 строку
    image_data = base64.b64decode(image_base64)

    # Создаем объект Image из байтового объекта
    image = Image.open(io.BytesIO(image_data))

    transform_for_prediction = transforms.Compose(
        [transforms.Resize((224, 224)), transforms.ToTensor()]
    )

    transformed_image = transform_for_prediction(image).unsqueeze(0)

    # Убедитесь, что модель в режиме оценки
    model.eval()

    # Получаем предсказание модели
    with torch.no_grad():  # отключаем градиенты
        output = model(transformed_image)

    # Проверка формы и значений выходного тензора
    tensor_image = output[0]
    # print(f"Форма выходного тензора: {tensor_image.shape}")
    # print("Минимальное значение:", tensor_image.min().item())
    # print("Максимальное значение:", tensor_image.max().item())
    
    path = generate_random_string()
    # plt.ioff()
    # Визуализация выходного тензора
    plt.imshow(tensor_image.detach().numpy().transpose(1, 2, 0))  # Преобразуем размерности

    # Сохраняем изображение без фона и осей
    plt.savefig(f'{path}.png', bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close()
    return f'{path}.png'
    
    
