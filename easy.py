import pygame
import os
import subprocess

# Setup
pygame.init()
width, height = 200, 300
win = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Parameters
y = 150
dir = 1
fps = 30
duration = 5  # seconds
total_frames = fps * duration

# Create frames directory
frames_dir = "frames"
os.makedirs(frames_dir, exist_ok=True)

# Generate and save frames
for frame_num in range(total_frames):
    win.fill((0, 0, 0))

    # Bounce logic
    y += dir
    if y > 160 or y < 140:
        dir *= -1

    # Draw stick figure
    pygame.draw.circle(win, (255, 255, 255), (100, y - 40), 10, 1)
    pygame.draw.line(win, (255, 255, 255), (100, y - 30), (100, y), 1)
    pygame.draw.line(win, (255, 255, 255), (85, y - 20), (115, y - 20), 1)
    pygame.draw.line(win, (255, 255, 255), (100, y), (85, y + 30), 1)
    pygame.draw.line(win, (255, 255, 255), (100, y), (115, y + 30), 1)

    # Save frame
    filename = os.path.join(frames_dir, f"frame_{frame_num:04d}.png")
    pygame.image.save(win, filename)

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
print("Frames saved.")

# Assemble video with ffmpeg
output_video = "output_video.mp4"
audio_file = "my_soundtrack.mp3"

# Run FFmpeg to create video with audio
ffmpeg_cmd = [
    "ffmpeg",
    "-y",  # Overwrite output file if it exists
    "-framerate", str(fps),
    "-i", os.path.join(frames_dir, "frame_%04d.png"),
    "-i", audio_file,
    "-shortest",  # Stop when the shortest input ends (audio or video)
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    output_video
]

print("Running FFmpeg...")
subprocess.run(ffmpeg_cmd)
print(f"Video saved as: {output_video}")
