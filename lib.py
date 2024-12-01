import os
import cv2


def rename_images_sequentially(folder: str) -> list:
    """Renombra las imágenes en la carpeta para que tengan un nombre secuencial."""
    valid_extensions = (".png", ".jpg", ".jpeg")
    images = [img for img in os.listdir(
        folder) if img.lower().endswith(valid_extensions)]

    if not images:
        return []

    renamed_images = []
    for i, image in enumerate(sorted(images), start=1):
        ext = os.path.splitext(image)[1]
        new_name = f"dmq_{i:04d}{ext}"  # Formato: dmq_0001.jpg
        old_path = os.path.join(folder, image)
        new_path = os.path.join(folder, new_name)
        os.rename(old_path, new_path)
        renamed_images.append(new_name)

    return renamed_images


def resize_image(image, target_size):
    """Redimensiona la imagen manteniendo la proporción."""
    height, width = image.shape[:2]
    target_width, target_height = target_size
    scale = min(target_width / width, target_height / height)
    new_width = int(width * scale)
    new_height = int(height * scale)
    resized_image = cv2.resize(
        image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

    return resized_image


def create_timelapse(image_folder: str, output_video: str, total_duration: int, fps: int = 30) -> bool:
    images = rename_images_sequentially(image_folder)

    if not images:
        return -1

    # Leer la cantidad de imágenes
    num_images = len(images)

    # Calcular cuántos frames mostrar por cada imagen
    total_frames = total_duration * fps
    frames_per_image = total_frames // num_images

    # Leer la primera imagen para obtener las dimensiones
    first_image_path = os.path.join(image_folder, images[0])
    frame = cv2.imread(first_image_path)
    height, width, _ = frame.shape
    target_size = (width, height)

    # Crear el archivo de video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para MP4: 'mp4v' o 'x264'
    video = cv2.VideoWriter(output_video, fourcc, fps, target_size)

    for image_name in images:
        image_path = os.path.join(image_folder, image_name)
        frame = cv2.imread(image_path)

        # Verificar que las dimensiones coincidan
        if (frame.shape[1], frame.shape[0]) != target_size:
            frame = resize_image(frame, target_size)

        # Escribir cada imagen tantas veces como sea necesario
        for _ in range(frames_per_image):
            video.write(frame)

    video.release()
    return 1
