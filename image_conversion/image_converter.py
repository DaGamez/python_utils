import os
from PIL import Image
import pillow_heif
import cv2

def convert_heic_to_jpg(input_path, output_path):
    """Convert HEIC file to JPG."""
    heif_file = pillow_heif.read_heif(input_path)
    image = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data,
        "raw",
    )
    image.save(output_path, "JPEG")
    print(f"Converted HEIC to JPG: {output_path}")

def convert_mp4_to_jpg(input_path, output_folder):
    """Convert 3 evenly-spaced frames from MP4 to JPG."""
    video = cv2.VideoCapture(input_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Calculate frame positions (start, middle, end)
    frame_positions = [
        int(total_frames * 0.1),  # 10% into video
        int(total_frames * 0.5),  # middle
        int(total_frames * 0.9),  # 90% into video
    ]
    
    for i, frame_pos in enumerate(frame_positions):
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_pos)
        success, frame = video.read()
        if success:
            output_path = os.path.join(output_folder, f"frame_{i+1}.jpg")
            cv2.imwrite(output_path, frame)
            print(f"Saved frame as JPG: {output_path}")
    
    video.release()

def process_files(input_folder, output_folder):
    """Process all HEIC and MP4 files in the folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        if filename.lower().endswith('.heic'):
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.jpg")
            convert_heic_to_jpg(input_path, output_path)
        elif filename.lower().endswith('.mp4'):
            video_output_folder = output_folder
            if not os.path.exists(video_output_folder):
                os.makedirs(video_output_folder)
            convert_mp4_to_jpg(input_path, video_output_folder)

# Example usage
input_folder = "input_files"
output_folder = "output_files"
process_files(input_folder, output_folder)
