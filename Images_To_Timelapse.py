import os
import customtkinter as ctk
from tkinter import messagebox
from lib import create_timelapse


class App (ctk.CTk):
    # Configuración de la ventana principal
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    def __init__(self):
        super().__init__()

        self.title("SimpleLapse")
        self.geometry("400x350")
        self.resizable(False, False)
        self.fontV = ctk.CTkFont(
            family='Verdana', size=12, weight='bold', slant='roman')

        self.frame_root = ctk.CTkFrame(self)
        self.frame_root.pack(padx=10, pady=10)

        # Etiqueta y entrada para la carpeta de imágenes
        self.frame_folder = ctk.CTkFrame(self.frame_root)
        self.frame_folder.grid(row=0, column=0, padx=10, pady=10)

        self.label_folder = ctk.CTkLabel(
            self.frame_folder, text="Carpeta de imágenes:", font=self.fontV)
        self.label_folder.grid(row=0, column=0, padx=10,
                               pady=(10, 3), sticky=ctk.W)

        self.button_browse_folder = ctk.CTkButton(
            self.frame_folder, text="Buscar", command=self.browse_folder, font=self.fontV)
        self.button_browse_folder.grid(
            row=0, column=1, padx=10, pady=(10, 3), sticky=ctk.E)

        self.entry_folder = ctk.CTkEntry(
            self.frame_folder, width=340,
            height=28, placeholder_text="Selecciona la carpeta de imágenes")
        self.entry_folder.grid(row=1, column=0, padx=10,
                               pady=(3, 10), columnspan=2)

        # Etiqueta y entrada para la duración del video
        self.frame_duration = ctk.CTkFrame(self.frame_root)
        self.frame_duration.grid(
            row=1, column=0, padx=10, pady=10, sticky=ctk.W)

        self.label_duration = ctk.CTkLabel(
            self.frame_duration, text="Duración (s):", font=self.fontV)
        self.label_duration.grid(row=0, column=0, padx=(10, 5), pady=10)

        self.entry_duration = ctk.CTkEntry(
            self.frame_duration, width=150,
            height=28, placeholder_text="Introduce la duración", justify="center")
        self.entry_duration.grid(row=0, column=1, pady=5, padx=(5, 10))

        # Etiqueta y entrada para el archivo de salida
        self.frame_output = ctk.CTkFrame(self.frame_root)
        self.frame_output.grid(row=2, column=0, padx=10, pady=10, sticky=ctk.W)

        self.label_output = ctk.CTkLabel(
            self.frame_output, text="Archivo de salida:", font=self.fontV)
        self.label_output.grid(row=0, column=0, padx=10,
                               pady=(10, 3), sticky=ctk.W)

        self.button_save_file = ctk.CTkButton(
            self.frame_output, text="Guardar como", command=self.save_file, font=self.fontV)
        self.button_save_file.grid(
            row=0, column=1, padx=10, pady=(10, 3), sticky=ctk.E)

        self.entry_output = ctk.CTkEntry(
            self.frame_output, width=340,
            height=28, placeholder_text="Selecciona el archivo de salida")
        self.entry_output.grid(row=1, column=0, padx=10,
                               pady=(3, 10), columnspan=2)

        # Botón para generar el video
        self.button_generate = ctk.CTkButton(
            self.frame_root, text="Generar", command=self.generate_video, font=self.fontV)
        self.button_generate.grid(
            row=3, column=0, padx=20, pady=(20, 10), sticky=ctk.E)

    def browse_folder(self):
        folder_selected = ctk.filedialog.askdirectory(
            title="Seleccionar carpeta")
        if folder_selected:
            self.entry_folder.delete(0, ctk.END)
            self.entry_folder.insert(0, folder_selected)

    def save_file(self):
        file_path = ctk.filedialog.asksaveasfilename(
            title="Guardar video como",
            defaultextension=".mp4",
            filetypes=[("Archivos MP4", "*.mp4")]
        )
        if file_path:
            self.entry_output.delete(0, ctk.END)
            self.entry_output.insert(0, file_path)

    def generate_video(self):
        image_folder = self.entry_folder.get().strip()
        output_video = self.entry_output.get().strip()
        total_duration = int(self.entry_duration.get().strip())

        if not output_video.endswith((".mp4", ".MP4")):
            output_video = output_video + ".mp4"

        if not image_folder or not output_video or not total_duration:
            messagebox.showerror(
                "Error", "Por favor, completa todos los campos.")
            return

        if not os.path.isdir(image_folder):
            messagebox.showerror(
                "Error", "La carpeta seleccionada no es válida.")
            return

        try:
            if total_duration <= 2:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "La duración debe ser mayor a 2s.")
            return

        result = create_timelapse(image_folder, output_video, total_duration)

        if result == -1:
            messagebox.showerror(
                "Error", "No se encontraron imágenes en el directorio especificado.")
        else:
            messagebox.showinfo(
                "Éxito", f"Timelapse creado con éxito: {output_video}")


if __name__ == '__main__':
    app = App()
    app.mainloop()
