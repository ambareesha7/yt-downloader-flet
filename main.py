import flet as ft


# def main(page: ft.Page):
#     page.add(ft.SafeArea(ft.Text("Hello, Flet!")))


# ft.app(main)
from pytube import YouTube
import os
import flet as ft
from flet import Text, TextField, ElevatedButton, Row, Column, Image
from flet_core.control_event import ControlEvent

# replace destination with the path where you want to save the downloaded file
destination = "downloads/"


def main(page: ft.Page):
    page.title = "YouTube downloder"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    # page.window_width = 400
    # page.window_height = 400
    title: Text = Text(value="")
    link_txt_box: TextField = TextField(
        hint_text='click here to enter youtube link')

    download_btn: ElevatedButton = ElevatedButton(
        text="Download")
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
                title.value = video_details.title
                show_snack_bar(
                    e=e, text=f'started downloading...\n{str(video_details.title)}')
                progress_ring = ft.ProgressRing()
                page.add(Row(controls=[progress_ring],
                         alignment=ft.MainAxisAlignment.CENTER))
                link_txt_box.disabled = True
                download_btn.disabled = True
                page.update()
                video_details.streams.get_highest_resolution().download(destination)
                print(f"video_details.title {video_details.title}")
                link_txt_box.disabled = False
                download_btn.disabled = False
                page.update()
                link_txt_box.value = ''
                progress_ring.visible = False
                show_snack_bar(
                    e=e, text=f'{str(video_details.title)} download completed')
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
            title.value = str(video_details.title)
            image.src = video_details.thumbnail_url
            print(f"video_details.title {video_details.title}, ")
            page.update()

        except:
            print(f"not a valid string Link {e.data}")
            title.value = ''
            page.update()

    def add_widgets(page: ft.Page):
        page.clean
        page.add(Row(controls=[image], alignment=ft.MainAxisAlignment.CENTER))
        page.add(Row(
            controls=[Text(value=f"video title:"),],
            alignment=ft.MainAxisAlignment.CENTER))
        page.add(Row(
            controls=[title,],
            alignment=ft.MainAxisAlignment.CENTER))
        page.add(Column(controls=[link_txt_box, download_btn],
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