# 🧠 MOTIX IOT — Detecção Inteligente de Motos no Pátio

Este projeto utiliza **visão computacional** integrada ao modelo do [Roboflow](https://roboflow.com) para detectar automaticamente motos em imagens aéreas de pátios da Mottu. A identificação é baseada em coordenadas de bounding boxes e a associação é feita com uma matriz de slots (vagas) predefinida.

---

## 📸 Funcionalidade

- Envio de imagem aérea (vista superior) para o modelo de detecção.
- Recebimento das coordenadas dos objetos detectados (bounding boxes).
- Mapeamento automático das motos para suas vagas (slots) em uma matriz.
- Geração de imagem com as vagas desenhadas:
  - 🟩 Verde = vaga ocupada
  - 🟦 Azul escuro = vaga livre
- Saída textual informando a quantidade total de motos detectadas e status de cada vaga.

---

## 🧠 Modelo de Visão Computacional

- Plataforma: [Roboflow](https://universe.roboflow.com/ilyass/motor-detection)
- Endpoint utilizado: `https://detect.roboflow.com/motor-detection/1`
- Modelo treinado com exemplos de motos vistas de cima.
- Filtragem por `confidence >= 0.5`.

---

## ⚙️ Tecnologias Usadas

- Python 3
- Pillow (PIL) — Manipulação de imagens
- Requests — Comunicação com API Roboflow
- Roboflow Hosted Inference API

---

## ▶️ Como Usar

1. Instale as dependências:

```bash
pip install pillow requests
```

2. Salve a imagem da vista aérea como `top.png`

3. Execute o script:

```bash
python detectar_motos.py
```

4. Será gerado um arquivo `motos_com_slots.jpg` com a imagem anotada.

---

## 📦 Exemplo de Saída no Console

```
Quantidade total de detecções: 6
Quantidade de motos detectadas com confiança acima de 50.0%: 5
Moto 1: (x=234.5, y=120.0), Confiança: 0.78
Slot A1: Ocupado
Slot A2: Livre
Slot A3: Ocupado
...
```

---

## 📂 Estrutura

```
.
├── detectar_motos.py          # Script principal
├── top.png                    # Imagem de entrada (vista superior)
├── motos_com_slots.jpg        # Resultado com slots desenhados
└── README.md
```

---

## 🧪 Próximos Passos

- Integração com ESP32 + câmera para captura em tempo real
- Detecção em tempo real via stream (RTSP)
- Envio automático de dados para o app MOTIX
- Reconhecimento de placas (OCR)

---

## 👨‍💻 Desenvolvedores

- Kleber da Silva — RM: 557887
- Nicolas Barutti — RM: 554944
- Lucas Rainha — RM: 558471
