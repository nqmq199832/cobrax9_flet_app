import os
import flet as ft
import requests
import webbrowser
from time import sleep

def main(page: ft.Page):
    def toggle_theme(e):
        page.theme_mode = ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        page.update()

    page.title = "COBRA X9 SMS PANEL"
    page.window_width = 720
    page.window_height = 720
    page.window_centered = True
    page.theme_mode = ft.ThemeMode.DARK

    def login_dialog():
        def check_key(e):
            user_key = key_field.value.strip()
            try:
                valid_key = requests.get("https://pastebin.com/raw/SyvsVmLG").text.strip()
            except:
                dlg.content.value = "\n[ERROR] Connection Failed. Try Again Later."
                page.dialog = dlg
                dlg.open = True
                page.update()
                return

            if user_key == valid_key:
                dlg.open = False
                page.update()
                main_ui()
            else:
                dlg.content.value = "\n[ERROR] Invalid Access Key."
                page.dialog = dlg
                dlg.open = True
                page.update()

        key_field = ft.TextField(label="Enter Access Key", password=True, width=300)
        submit_btn = ft.ElevatedButton("Login", on_click=check_key)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Login Required"),
            content=ft.Text(""),
            actions=[submit_btn],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.add(key_field)
        page.dialog = dlg
        dlg.open = True
        page.update()

    def main_ui():
        upload_list = ft.Text(value="No files uploaded.", size=12)

        def pick_files_result(e):
            if e.files:
                upload_list.value = "\n".join([f.name for f in e.files])
                page.update()

        file_picker = ft.FilePicker(on_result=pick_files_result)
        page.overlay.append(file_picker)

        pick_btn = ft.ElevatedButton("Choose File", on_click=lambda _: file_picker.pick_files(allow_multiple=True))
        toggle_btn = ft.IconButton(ft.icons.BRIGHTNESS_6, on_click=toggle_theme)

        layout = ft.Column([
            ft.Row([
                ft.Text("🐍 COBRA X9 PANEL", size=22, weight=ft.FontWeight.BOLD),
                toggle_btn
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            pick_btn,
            upload_list,
        ], spacing=20)

        page.add(layout)
        page.update()

    login_dialog()

ft.app(target=main, view=ft.WEB_BROWSER, port=int(os.environ.get("PORT", 8550)))
