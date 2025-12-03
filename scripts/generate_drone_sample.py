import cv2
import numpy as np

# Crear imagen simulada de cultivo bajo pivote (vista cenital)
height, width = 1080, 1920
img = np.ones((height, width, 3), dtype=np.uint8) * 240  # fondo claro

# Dibujar círculo de pivote
center = (width // 2, height // 2)
cv2.circle(img, center, 400, (34, 139, 34), -1)  # verde sano
cv2.circle(img, center, 300, (50, 205, 50), -1)

# Añadir sector con estrés (NE)
pts = np.array([
    [center[0], center[1]],
    [center[0] + 350, center[1] - 200],
    [center[0] + 250, center[1] - 400]
], np.int32)
cv2.fillPoly(img, [pts], (170, 170, 50))  # amarillento

# Ruido realista
noise = np.random.normal(0, 5, img.shape).astype(np.int16)
img = cv2.add(img, noise.astype(np.uint8))
img = cv2.GaussianBlur(img, (3, 3), 0)

# Guardar
cv2.imwrite("data/samples/drone_rgb_sample.jpg", img)
print("✅ data/samples/drone_rgb_sample.jpg generado (simulado, con sector en estrés).")
