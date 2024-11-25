import torch
import torchvision.transforms as transforms
import torch.nn.functional as F
from PIL import Image
import os
from torchvision.transforms import ToPILImage
from sklearn import preprocessing
from src.scan.ml.efficient_network import EfficientNetwork
from io import BytesIO
import base64
import cv2
import numpy as np
import pandas as pd


device = 'cpu'

gender_dict = {
    "female": 0,
    "male": 1
}

anatomy_dict = {
    "anterior torso": 0,
    "lower extremity": 3,
    "head/neck": 1,
    "upper extremity": 7,
    "posterior torso": 6,
    "palms/soles": 5,
    "oral/genital": 4,
    "lateral torso": 2
}
categories = {
    0: "АК (Актинический кератоз)",        # AK - Actinic Keratosis
    1: "БКК (Базальноклеточная карцинома)", # BCC - Basal Cell Carcinoma
    2: "БКЛ (Доброкачественное кератотическое поражение)", # BKL - Benign Keratosis-like Lesions
    3: "ДФ (Дерматофиброма)",               # DF - Dermatofibroma
    4: "МЕЛ (Меланома)",                    # MEL - Melanoma
    5: "НВ (Невус)",                        # NV - Nevus
    6: "ПСК (Плоскоклеточная карцинома)",   # SCC - Squamous Cell Carcinoma
    7: "СОС (Сосудистые поражения)"         # VASC - Vascular Lesions
}



def hair_remove(image):
    # convert image to grayScale
    grayScale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # kernel for morphologyEx
    kernel = cv2.getStructuringElement(1, (17, 17))

    # apply MORPH_BLACKHAT to grayScale image
    blackhat = cv2.morphologyEx(grayScale, cv2.MORPH_BLACKHAT, kernel)

    # apply thresholding to blackhat
    _, threshold = cv2.threshold(blackhat, 10, 255, cv2.THRESH_BINARY)

    # inpaint with original image and threshold image
    final_image = cv2.inpaint(image, threshold, 1, cv2.INPAINT_TELEA)

    return final_image


# Загрузка модели EfficientNet
def load_model(model_path, output_size=8, no_columns=3):
    model = EfficientNetwork(output_size=output_size, no_columns=no_columns,
                             b4=False, b2=True).to(device)

    if os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        model.eval()  # Перевод модели в режим предсказания
        return model
    else:
        raise FileNotFoundError("Model file not found.")


# Загрузка и преобразование изображения в тензор
def load_image(image_base64 : str):
    
    image_data = base64.b64decode(image_base64)
    image = Image.open(BytesIO(image_data)).convert("RGB")  # Конвертируем в RGB, если изображение в другом формате
    image = np.array(image)
    
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image = hair_remove(image)

    preprocess = transforms.Compose([
        ToPILImage(),  # Здесь ToPILImage() без transforms.
        transforms.Resize((224, 224)),  # Стандартный размер для EfficientNet
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image_preprocess = preprocess(image)
    # Добавляем batch dimension
    return image_preprocess

def preprocess_csv(csv_data):
    # Переименование столбцов для удобства
    csv_data = csv_data.rename(columns={
        'gender': 'sex',
        'body_part': 'anatomy'
    })

    # Преобразование в числа для пола и анатомии
    csv_data['sex'] = csv_data['sex'].map(gender_dict)
    csv_data['anatomy'] = csv_data['anatomy'].map(anatomy_dict)

    # Проверка на наличие NaN и выброс ошибки, если они есть
    if csv_data[['sex', 'age', 'anatomy']].isnull().values.any():
        raise ValueError("Input data contains NaN values. Please clean the data.")

    # Нормализация данных
    csv_data_normalized = preprocessing.normalize(csv_data[['sex', 'age', 'anatomy']])

    # Преобразование в numpy массив
    csv_data_preprocess = np.array(csv_data_normalized, dtype=np.float32)

    return csv_data_preprocess


# Предсказание
def predict(model, image, csv_data):
    image = torch.tensor(image, device=device, dtype=torch.float32)
    csv_data = torch.tensor(csv_data, device=device, dtype=torch.float32)

    image = image.clone().detach().float()  # Приведение к типу float
    if image.dim() == 3:  # Если это 3D тензор
        image = image.unsqueeze(0)  # Добавляем размерность батча
    # Подадим изображение и метаданные в модель
    with torch.no_grad():
        output = model(image, csv_data)
    # Получаем числовой ответ
    probabilities = F.softmax(output, dim=1)

    # Находим индекс класса с максимальной вероятностью
    predicted_class = probabilities.argmax().item()

    # Получаем вероятность этого класса
    max_probability = probabilities[0, predicted_class].item()

    # Возвращаем класс и вероятность в процентах
    return predicted_class, max_probability * 100

def get_result(gender : str, age : int, body_part : str, image_base64 : str = '') -> str:
    image_base64 = image_base64.split(',')[1]
    model_path = os.path.join(os.path.dirname(__file__), 'model.pth')
    model = load_model(model_path)
    image_tensor = load_image(image_base64)
    metadata_tensor = pd.DataFrame({'gender':[gender], 'age':[age],"body_part":[body_part]})
    metadata_tensor = preprocess_csv(metadata_tensor)
    prediction = predict(model, image_tensor, metadata_tensor)
    return (categories[prediction[0]], prediction[1])
    