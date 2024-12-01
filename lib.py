import os
import cv2


def create_timelapse(image_folder: str, output_video: str, total_duration: int, fps: int = 30) -> bool:
    valid_extensions = (".png", ".jpg", ".jpeg")
    images = [img for img in os.listdir(
        image_folder) if img.lower().endswith(valid_extensions)]

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
            frame = cv2.resize(frame, target_size)

        # Escribir cada imagen tantas veces como sea necesario
        for _ in range(frames_per_image):
            video.write(frame)

    video.release()
    return 1
