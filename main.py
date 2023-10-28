import flet as ft

from pytube import YouTube
import os
import pathlib as pt
import flet as ft
from flet import Text, TextField, ElevatedButton, Row, Column, Image
from flet_core.control_event import ControlEvent

# replace destination with the path where you want to save the downloaded file
destination = "downloads/"
video: str = 'video'
audio: str = 'audio'
both: str = 'both'
# pt.Path.joinpath(os.getcwd(), )


def main(page: ft.Page):
    page.title = "YouTube downloder"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    # page.window_width = 400
    # page.window_height = 400
    title: Text = Text(value="")
    link_txt_box: TextField = TextField(
        hint_text='click here to enter youtube link')

    def on_dropdown_change(e):
        print(f'dropdown change {dropdown_btn.value}')
        page.update()

    dropdown_btn: ft.Dropdown = ft.Dropdown(
        on_change=on_dropdown_change,
        width=120,
        label='Video download type',
        value=both,
        options=[
            ft.dropdown.Option(both),
            ft.dropdown.Option(video),
            ft.dropdown.Option(audio),
        ],
    )
    download_btn: ElevatedButton = ElevatedButton(
        text="Download", disabled=True)
    image: Image = ft.Image(src="pic.png", width=400, height=350)
    make_dir(destination)

    def show_snack_bar(e: ControlEvent, text: str):
        page.snack_bar = ft.SnackBar(
            ft.Text(f"{text}"))
        page.snack_bar.open = True
        page.update()

    def on_progress(a, byts, ints) -> None:
        print(f"any {a}, btes:, ints: {ints}")

    def download(e: ControlEvent) -> None:
        try:
            if link_txt_box.value:
                video_details = YouTube(
                    link_txt_box.value, on_progress_callback=on_progress)

                show_snack_bar(
                    e=e, text=f'started downloading...\n{str(video_details.title)}')
                progress_ring = ft.ProgressRing()
                page.add(Row(controls=[progress_ring],
                         alignment=ft.MainAxisAlignment.CENTER))
                link_txt_box.disabled = True
                download_btn.disabled = True
                page.update()
                format = str(dropdown_btn.value)
                if (format == both):
                    video_details.streams.get_highest_resolution().download(destination)
                elif (format == video):
                    dest = f'{destination}{video}/'
                    make_dir(dest)
                    video_details.streams.filter(
                        only_video=True).first().download(dest)
                elif (format == audio):
                    dest = f'{destination}{audio}/'
                    make_dir(dest)
                    video_details.streams.get_audio_only().download(dest)
                else:
                    video_details.streams.get_highest_resolution().download(destination)

                print(f"video_details.title {video_details.title}")
                link_txt_box.disabled = False
                # download_btn.disabled = False
                image.visible = False
                page.update()
                link_txt_box.value = ''
                progress_ring.visible = False
                show_snack_bar(
                    e=e, text=f'download completed')
                title.value = ''
                page.update()
        except:
            show_snack_bar(e=e, text=str(link_txt_box.value))
            print("not a valid link")
            page.update()

    def on_text_changed(e: ControlEvent) -> None:
        try:
            print(f"entered text --{e.data}--")
            video_details = YouTube(e.data)
            cc = video_details.streams.get_audio_only()
            # cc = video_details.streams.()
            print(f'audio..... {cc}')
            title.value = str(video_details.title)
            image.src = video_details.thumbnail_url
            image.visible = True
            download_btn.disabled = False
            dropdown_btn.disabled = False
            print(f"video_details.title {video_details.title}, ")
            page.update()

        except:
            print(f"not a valid string Link {e.data}")
            title.value = ''
            page.update()

    def add_widgets(page: ft.Page):
        page.clean
        page.add(Row(controls=[image], alignment=ft.MainAxisAlignment.CENTER))
        image.visible = False
        page.add(Row(
            controls=[Text(value=f"video title:"),],
            alignment=ft.MainAxisAlignment.CENTER))
        page.add(Row(
            controls=[title,],
            alignment=ft.MainAxisAlignment.CENTER))
        page.add(Column(controls=[link_txt_box, Row(alignment='center', controls=[download_btn, dropdown_btn]), ],
                        horizontal_alignment="center"))
    link_txt_box.on_change = on_text_changed
    download_btn.on_click = download

    # add widgets
    add_widgets(page=page)


def make_dir(path: str) -> None:
    try:
        if not os.path.exists(path):
            os.makedirs(path)

    except:
        print("directory not exists")


# if __name__ == "__main__":
# ft.app(target=main)
ft.app(main)
