import cv2
import numpy as np
import base64


        
contever = {
    "Меньше 5 мм (ластик на карандаше)" : 1,
    "От 5 до 10 мм (горошина)" : 2,
    "Больше 10 мм (монета)" : 3,
    "Не уверен(а)" : 4,
    }

class SkinLesionAnalyzer:
    def load_image(self, img_base64):
        img_data = base64.b64decode(img_base64)
        nparr = np.frombuffer(img_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        preprocessed = cv2.GaussianBlur(image_rgb, (5, 5), 0)
        return image_rgb, preprocessed

    def segment_lesion(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # Otsu's thresholding
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Find contours
        contours, _ = cv2.findContours(
            binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        lesion_contour = max(contours, key=cv2.contourArea)

        return binary, lesion_contour

    def analyze_asymmetry(self, binary_mask, contour):
        M = cv2.moments(contour)
        if M["m00"] == 0:
            return 0

        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        height, width = binary_mask.shape

        left_half = binary_mask[:, :cx]
        right_half = binary_mask[:, cx:]

        if left_half.shape[1] != right_half.shape[1]:
            new_width = left_half.shape[1]
            right_half = cv2.resize(right_half, (new_width, height))

        right_half_flipped = cv2.flip(right_half, 1)

        left_half = (left_half > 0).astype(np.uint8)
        right_half_flipped = (right_half_flipped > 0).astype(np.uint8)

        intersection = np.logical_and(left_half, right_half_flipped)
        union = np.logical_or(left_half, right_half_flipped)
        union_sum = np.sum(union)
        if union_sum == 0:
            return 0
        overlap_score = np.sum(intersection) / union_sum
        asymmetry_score = 1 - overlap_score
        return min(max(asymmetry_score, 0), 1)

    def analyze_border(self, contour):
        perimeter = cv2.arcLength(contour, True)
        area = cv2.contourArea(contour)

        if area == 0:
            return 0

            # Calculate circularity
        circularity = 4 * np.pi * area / (perimeter * perimeter)

        return 1 - circularity

    def analyze_color(self, image, binary_mask):
        masked_image = cv2.bitwise_and(image, image, mask=binary_mask.astype(np.uint8))

        color_vars = []
        for channel in range(3):
            channel_values = masked_image[:, :, channel][binary_mask > 0]
            if len(channel_values) > 0:
                color_vars.append(np.std(channel_values))

        if not color_vars:
            return 0

        # Normalize color variation score
        color_score = np.mean(color_vars) / 255.0
        return min(color_score, 1.0)


def get_absd_score(image_base64 : str, size_answer : str) -> str:
    
    analyzer = SkinLesionAnalyzer()
    image_base64 = image_base64.split(',')[1]
    original, preprocessed = analyzer.load_image(image_base64)
    binary_mask, contour = analyzer.segment_lesion(preprocessed)
    asymmetry_score = analyzer.analyze_asymmetry(binary_mask, contour)  # A
    border_score = analyzer.analyze_border(contour)  # B
    color_score = analyzer.analyze_color(original, binary_mask)  # С
    user_diameter_mm = {
        1: 0.04742587317756678,
        2: 0.7310585786300049,
        3: 0.9975273768433653,
        4: 0.2689414213699951,
    }  ## в зависимости от кнопки (по порядку)
    size_index = contever.get(size_answer)
    if size_index==None:
        return "Not found"
    
    diameter_score = user_diameter_mm[size_index]  ## ключ из словаря выше

    weights = {"asymmetry": 1.3, "border": 0.1, "color": 0.5, "diameter": 0.5}

    total_score = (
        asymmetry_score * weights["asymmetry"]
        + border_score * weights["border"]
        + color_score * weights["color"]
        + diameter_score * weights["diameter"]
    ) / sum(
        weights.values()
    )  ## TOTAL -- умножение каждого из параметров на коэффициенты

    return total_score
