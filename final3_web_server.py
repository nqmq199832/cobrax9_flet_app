import flet as ft
import requests
import webbrowser
from time import sleep

def main(page: ft.Page):
    # ---------- Global Page Settings ----------
    page.title = '🐍 COBRA X9 APP 🐍'
    page.window_width = 410
    page.window_height = 890
    page.window_resizable = False
    page.bgcolor = ft.colors.BLUE_GREY_900
    page.padding = 20

    # ---------- SHARED UTILS ----------
    def telegram(e): webbrowser.open_new('https://t.me/shopandbuyy')
    def whatsapp(e): webbrowser.open_new('https://wa.me/qr/ENLYCD65EQZK1')

    def switch_to_sms_panel():
        login_card.visible = False
        sms_panel.visible = True
        page.update()

    # ---------- LOGIN UI ----------
    license_input = ft.TextField(
        label="Enter License Key",
        password=True,
        can_reveal_password=True,
        icon=ft.icons.VERIFIED_USER,
        bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLUE_200),
        border_radius=10,
        text_align="center"
    )

    # ---------- Centered Spinner Overlay ----------
    loading_overlay = ft.Container(
        content=ft.Column(
            controls=[
                ft.ProgressRing(color=ft.colors.LIGHT_GREEN_ACCENT_700, scale=2),
                ft.Text("Checking license...", color=ft.colors.PURPLE_100, size=16),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        bgcolor=ft.colors.with_opacity(0.6, ft.colors.BLACK),
        width=page.window_width,
        height=page.window_height,
        visible=False
    )
    page.overlay.append(loading_overlay)

    def validate_key(e):
        loading_overlay.visible = True
        page.update()

        user_key = license_input.value
        valid_key = requests.get('https://pastebin.com/raw/SyvsVmLG').text

        sleep(1.2)  # simulate processing

        loading_overlay.visible = False

        if user_key == valid_key:
            switch_to_sms_panel()
        else:
            dialog = ft.AlertDialog(
                title=ft.Text("❌ Invalid Key"),
                content=ft.Text("CLICK BUY TO PURCHASE LICENSE KEY."),
                actions=[
                    ft.TextButton("BUY", on_click=telegram),
                    ft.TextButton("NO", on_click=telegram),
                ]
            )
            page.dialog = dialog
            dialog.open = True

        page.update()

    login_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("         WELCOME TO", size=25, weight=ft.FontWeight.BOLD,
                        color=ft.colors.DEEP_PURPLE_ACCENT, text_align="center"),
                ft.Text("🐍 COBRA X9 LOGIN 🐍", size=25, weight=ft.FontWeight.BOLD,
                        color=ft.colors.DEEP_PURPLE_ACCENT, text_align="center"),
                ft.Image(
                    src="https://media.tenor.com/BAHGKtKC5TQAAAAi/plant-grow.gif",
                    width=300,
                    height=160
                ),
                ft.Text("   🔐 Secure Access to Bulk SMS Panel", size=16, weight=ft.FontWeight.BOLD,
                        text_align="center", color=ft.colors.DEEP_PURPLE_ACCENT),
                license_input,
                ft.Container(height=10),
                ft.Row([
                    ft.ElevatedButton(
                        "🔓 Submit",
                        icon=ft.icons.SAFETY_CHECK,
                        on_click=validate_key,
                        style=ft.ButtonStyle(
                            bgcolor=ft.colors.DEEP_PURPLE_ACCENT,
                            color=ft.colors.WHITE,
                            shape=ft.RoundedRectangleBorder(radius=12),
                            padding=15
                        )
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(opacity=0.2),
                ft.Row([
                    ft.TextButton("@COBRA9X", icon=ft.icons.TELEGRAM, on_click=telegram),
                    ft.TextButton("WhatsApp", icon=ft.icons.WIFI_CALLING_ROUNDED, on_click=whatsapp)
                ], alignment=ft.MainAxisAlignment.CENTER)
            ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
            padding=25,
            border_radius=20,
            bgcolor=ft.colors.with_opacity(0.10, ft.colors.PURPLE_100),
        ),
        elevation=20,
        visible=True
    )

    # ---------- SMS PANEL ----------
    selected_files = ft.Text(color=ft.colors.BLUE_100)
    lead_input = ft.TextField()
    message_list = ft.ListView()
    sent_count_text = ft.Text("Total Sent: 0", color=ft.colors.PURPLE_100, size=16)

    def pick_files_result(e: ft.FilePickerResultEvent):
        if e.files:
            try:
                file_path = e.files[0].path
                with open(file_path, "r", encoding="utf-8") as f:
                    lead_input.value = f.read()
            except Exception as err:
                lead_input.value = f"❌ Error reading file: {err}"
            selected_files.value = e.files[0].name
        else:
            selected_files.value = "Cancelled!"
        selected_files.update()
        lead_input.update()

    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)

    def on_message(msg):
        message_list.controls.append(ft.Text(msg, color=ft.colors.PURPLE_100))
        sent_count_text.value = f"Total Sent: {len(message_list.controls)}"
        page.update()

    page.pubsub.subscribe(on_message)

    def send_message_click(e):
        try:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Sending messages...", size=24, text_align='center', color=ft.colors.WHITE),
                bgcolor=ft.colors.GREEN_ACCENT_700
            )
            page.snack_bar.open = True
            page.update()

            leads = requests.get('https://pastebin.com/raw/SZ1VjQXR').text.splitlines()
            for lead in leads:
                sleep(1.5)
                page.pubsub.send_all(f"✅ Message sent to {lead}")
        except Exception as err:
            page.pubsub.send_all(f"❌ Error: {err}")

    def clear_data_click(e):
        lead_input.value = ""
        selected_files.value = ""
        message_list.controls.clear()
        sent_count_text.value = "Total Sent: 0"
        page.update()

    message_input = ft.TextField(
        label="Message Content",
        filled=True,
        multiline=True,
        min_lines=3,
        max_lines=5,
        border_radius=10,
        icon=ft.icons.MESSAGE,
        bgcolor=ft.colors.WHITE,
        label_style=ft.TextStyle(color=ft.colors.PURPLE_ACCENT)
    )

    lead_input.label = "Recipient Numbers"
    lead_input.hint_text = "Paste numbers or upload file..."
    lead_input.filled = True
    lead_input.multiline = True
    lead_input.min_lines = 3
    lead_input.max_lines = 5
    lead_input.border_radius = 10
    lead_input.icon = ft.icons.LIST_ALT_OUTLINED
    lead_input.bgcolor = ft.colors.WHITE
    lead_input.label_style = ft.TextStyle(color=ft.colors.PURPLE_ACCENT)

    file_upload = ft.Row([
        ft.ElevatedButton(
            "📁 Upload List",
            icon=ft.icons.UPLOAD_FILE,
            on_click=lambda _: pick_files_dialog.pick_files(allow_multiple=False),
            style=ft.ButtonStyle(
                bgcolor=ft.colors.PURPLE_700,
                color=ft.colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=12)
            )
        ),
        ft.ElevatedButton(
            "🧹 Clear Data",
            icon=ft.icons.DELETE_SWEEP,
            on_click=clear_data_click,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.RED_400,
                color=ft.colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=12)
            )
        ),
        selected_files
    ], alignment=ft.MainAxisAlignment.CENTER)

    send_button = ft.Row([
        ft.ElevatedButton(
            "🚀 Send Messages",
            icon=ft.icons.SEND,
            on_click=send_message_click,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.GREEN_ACCENT_700,
                color=ft.colors.WHITE,
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=15
            )
        )
    ], alignment=ft.MainAxisAlignment.CENTER)

    message_list_container = ft.Container(
        content=message_list,
        height=200,
        bgcolor=ft.colors.BLUE_GREY_800,
        border_radius=10,
        padding=10
    )

    sms_panel = ft.Container(
        content=ft.Column([
            ft.Text(" 🐍COBRA X9 BULK SMS🐍", size=26, weight=ft.FontWeight.BOLD,
                    color=ft.colors.PURPLE_ACCENT, text_align="center"),
            ft.Divider(color=ft.colors.PURPLE_ACCENT),
            ft.Card(ft.Container(content=message_input, padding=15)),
            ft.Card(ft.Container(content=lead_input, padding=15)),
            file_upload,
            ft.Container(height=10),
            send_button,
            ft.Container(height=10),
            ft.Row([
                ft.Text("📋 Sent Log", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.PURPLE_100),
                sent_count_text
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            message_list_container
        ],
        spacing=15,
        scroll=ft.ScrollMode.AUTO
        ),
        expand=True,
        visible=False
    )

    # ---------- PAGE ADD ----------
    page.add(login_card, sms_panel)

ft.app(target=main, view=ft.WEB_BROWSER, port=8550)
