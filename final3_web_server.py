import flet as ft
import requests
import os


def main(page: ft.Page):
    # Theme state
    is_dark = True

    def toggle_theme(e):
        nonlocal is_dark
        is_dark = not is_dark
        page.theme_mode = ft.ThemeMode.DARK if is_dark else ft.ThemeMode.LIGHT
        page.update()

    # Set default theme
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "COBRA X9 PANEL"
    page.window_width = 600
    page.window_height = 600
    page.window_centered = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ALWAYS

    # Background image or splash
    splash = ft.Image(src="snake.gif", width=100, height=100)

    # Login section
    key_field = ft.TextField(label="Enter Access Key", password=True, width=300)
    login_status = ft.Text(color=ft.colors.RED_400)

    def login(e):
        user_key = key_field.value.strip()
        try:
            valid_key = requests.get('https://pastebin.com/raw/SyvsVmLG').text.strip()
        except:
            login_status.value = "Failed to connect to server."
            page.update()
            return

        if user_key == valid_key:
            page.clean()
            show_sms_panel()
        else:
            login_status.value = "❌ Invalid key. Try again."
            page.update()

    login_btn = ft.ElevatedButton("Login", on_click=login, width=300)

    login_view = ft.Column([
        splash,
        ft.Text("COBRA X9 PANEL", size=24, weight=ft.FontWeight.BOLD),
        key_field,
        login_btn,
        login_status
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    page.add(login_view)

    def show_sms_panel():
        # Upload List
        file_picker = ft.FilePicker()
        selected_files = ft.Text(value="No file selected", size=12, italic=True)

        def on_file_result(e):
            selected_files.value = "\n".join([f.name for f in e.files]) if e.files else "No file selected"
            page.update()

        file_picker.on_result = on_file_result
        page.overlay.append(file_picker)

        # SMS form fields
        sender_field = ft.TextField(label="Sender", width=400)
        message_field = ft.TextField(label="Message", multiline=True, min_lines=3, max_lines=5, width=400)

        send_button = ft.FilledButton("Send SMS", icon=ft.icons.SEND)
        pick_file_button = ft.OutlinedButton("Choose File", on_click=lambda _: file_picker.pick_files(allow_multiple=True))

        sms_view = ft.Column([
            ft.Row([
                ft.Text("COBRA X9 SMS PANEL", size=20, weight=ft.FontWeight.BOLD),
                ft.IconButton(ft.icons.BRIGHTNESS_6, tooltip="Toggle Theme", on_click=toggle_theme),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            sender_field,
            message_field,
            pick_file_button,
            selected_files,
            send_button
        ], spacing=20, expand=True)

        page.add(sms_view)
        page.update()

ft.app(target=main, view=ft.WEB_BROWSER, port=int(os.environ.get("PORT", 8550)))
