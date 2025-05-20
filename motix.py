import requests
from PIL import Image, ImageDraw
from io import BytesIO

# Configurações
ROBOFLOW_API_KEY = "jcEigZlCdDknLWT56L1n"
ROBOFLOW_MODEL_ENDPOINT = "https://detect.roboflow.com/motor-detection/1"
CONFIDENCE_THRESHOLD = 0.5
SLOTS_PER_ROW = 3  # Quantidade de slots por linha no setor A
SLOTS_PER_COLUMN = 2  # Quantidade de slots por coluna no setor A

# Lendo a imagem
target_sector = "A"
image_path = "Motocicletas.png"
with open(image_path, "rb") as image_file:
    image_data = image_file.read()

# Enviando imagem para Roboflow
response = requests.post(
    f"{ROBOFLOW_MODEL_ENDPOINT}?api_key={ROBOFLOW_API_KEY}",
    files={"file": image_data},
)
result = response.json()
predictions = result.get("predictions", [])

# Carregar a imagem
image = Image.open(BytesIO(image_data))
draw = ImageDraw.Draw(image)

# Tamanho da imagem
image_width, image_height = image.size

# Tamanho de cada slot
slot_width = image_width / SLOTS_PER_ROW
slot_height = image_height / SLOTS_PER_COLUMN

# Criar slots apenas para o setor A
slots = {}
for row in range(SLOTS_PER_COLUMN):
    for col in range(SLOTS_PER_ROW):
        slot_name = f"{chr(65 + row)}{col + 1}"
        slots[slot_name] = {
            "x_min": col * slot_width,
            "x_max": (col + 1) * slot_width,
            "y_min": row * slot_height,
            "y_max": (row + 1) * slot_height,
            "occupied": False
        }


# Filtrar motos confiáveis
motos_confiaveis = [pred for pred in predictions if pred["confidence"] >= CONFIDENCE_THRESHOLD]

# Mostrar informações
print(f"Quantidade total de detecções: {len(predictions)}")
print(f"Quantidade de motos detectadas com confiança acima de {CONFIDENCE_THRESHOLD * 100}%: {len(motos_confiaveis)}")

for idx, moto in enumerate(motos_confiaveis, 1):
    print(f"Moto {idx}: (x={moto['x']:.1f}, y={moto['y']:.1f}), Confiança: {moto['confidence']:.2f}")

# Processar motos detectadas
for moto in motos_confiaveis:
    x_center = moto["x"]
    y_center = moto["y"]

    # Verificar em qual slot a moto está
    for slot_name, slot in slots.items():
        if slot["x_min"] <= x_center <= slot["x_max"] and slot["y_min"] <= y_center <= slot["y_max"]:
            slots[slot_name]["occupied"] = True
            # Desenhar bounding box
            width = moto["width"]
            height = moto["height"]
            x0 = x_center - width / 2
            y0 = y_center - height / 2
            x1 = x_center + width / 2
            y1 = y_center + height / 2
            draw.rectangle([x0, y0, x1, y1], outline="#A5FF00", width=3)
            draw.text((x0, y0 - 10), f"{moto['confidence']:.2f}", fill="#A5FF00")
            break  # Quando encontrar o slot certo, parar o loop

# Desenhar os slots
for slot_name, slot in slots.items():
    color = "#A5FF00" if slot["occupied"] else "#1F2A44"  # Verde se ocupado, Azul escuro se livre
    draw.rectangle(
        [slot["x_min"], slot["y_min"], slot["x_max"], slot["y_max"]],
        outline=color,
        width=2
    )
    draw.text((slot["x_min"] + 5, slot["y_min"] + 5), slot_name, fill=color)

# Salvar a imagem com slots
image.save("motos_com_slots.jpg")
print("Imagem com slots gerada: 'motos_com_slots.jpg'")

# Mostrar status dos slots
for slot_name, slot in slots.items():
    status = "Ocupado" if slot["occupied"] else "Livre"
    print(f"Slot {slot_name}: {status}")
