from moviepy import VideoFileClip
import os
import flet as ft

def main(page: ft.Page):
    my_var = ""
    my_var2 = ""

    def on_change(e):
        nonlocal my_var
        nonlocal my_var2
        if e.control.label == "Input path":
            my_var = e.control.value
        else:
            my_var2 = e.control.value
        print(my_var)
        print(my_var2)

    input = ft.TextField(label="Input path", on_change=on_change)
    output = ft.TextField(label="Output path", on_change=on_change)
    
    start_button = ft.ElevatedButton("Start", 
        on_click=lambda e: split_video(my_var, my_var2, 60))

    page.add(input)
    page.add(output)
    page.add(start_button)

    def split_video(input_path, output_dir, chunk_duration):
        os.makedirs(output_dir, exist_ok=True)
        
        video = VideoFileClip(input_path)
        total_duration = video.duration
       
        start = 0
        part = 1
        while start < total_duration:
            end = min(start + chunk_duration, total_duration)
            
            chunk = video.subclipped(start, end)
            output_path = os.path.join(output_dir, f"part_{part:03d}.mp4")
           
            chunk.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                logger=None
            )
           
            print(f"Сохранён {output_path} ({start:.0f}s – {end:.0f}s)")
           
            start += chunk_duration
            part += 1
        video.close()
        print(f"\nAll parts: {part - 1}")

ft.app(target=main)