"""
Flet Mobile App - Cross-platform file processing application
Works on Android (via Flet build apk) and Linux Desktop (XFCE, etc.)
"""

import flet as ft
import json
import os
from pathlib import Path


class FileProcessorApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "File Processor"
        self.page.theme_mode = ft.ThemeMode.SYSTEM
        self.page.window_width = 400
        self.page.window_height = 600
        self.page.padding = 20

        # State
        self.selected_file_path = None
        self.file_content = ""

        # UI Components
        self.file_picker = ft.FilePicker(on_result=self.on_file_picked)
        self.page.overlay.append(self.file_picker)

        self.status_text = ft.Text("Ready", size=14, color=ft.Colors.GREY_600)
        self.file_info = ft.Text("No file selected", size=12, color=ft.Colors.GREY_500)
        self.content_display = ft.TextField(
            multiline=True,
            read_only=True,
            min_lines=15,
            max_lines=20,
            text_size=12,
            border_color=ft.Colors.OUTLINE,
            expand=True,
        )
        self.stats_text = ft.Text("", size=12, color=ft.Colors.BLUE_700)

        self.build_ui()

    def build_ui(self):
        """Build the user interface"""
        # Header
        header = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.FOLDER_OPEN, size=48, color=ft.Colors.BLUE_600),
                    ft.Text("File Processor", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        "Load and analyze text files", size=14, color=ft.Colors.GREY_600
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            padding=ft.padding.only(bottom=20),
        )

        # File selection button
        select_btn = ft.ElevatedButton(
            "Select File",
            icon=ft.Icons.UPLOAD_FILE,
            on_click=lambda _: self.file_picker.pick_files(
                allowed_extensions=["txt", "json", "csv", "md", "py", "log"],
                dialog_title="Select a text file to process",
            ),
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(horizontal=30, vertical=15),
                text_style=ft.TextStyle(size=16),
            ),
        )

        # Process button
        self.process_btn = ft.ElevatedButton(
            "Process File",
            icon=ft.Icons.PLAY_ARROW,
            on_click=self.process_file,
            disabled=True,
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(horizontal=30, vertical=15),
                text_style=ft.TextStyle(size=16),
                bgcolor=ft.Colors.GREEN_600,
                color=ft.Colors.WHITE,
            ),
        )

        # Clear button
        clear_btn = ft.OutlinedButton(
            "Clear",
            icon=ft.Icons.CLEAR,
            on_click=self.clear_all,
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(horizontal=30, vertical=15),
                text_style=ft.TextStyle(size=16),
            ),
        )

        # Button row
        button_row = ft.Row(
            [
                select_btn,
                self.process_btn,
                clear_btn,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            wrap=True,
        )

        # File info
        file_info_container = ft.Container(
            content=self.file_info, padding=ft.padding.symmetric(vertical=10)
        )

        # Content display area
        content_container = ft.Container(
            content=ft.Column(
                [
                    ft.Text("File Content:", size=14, weight=ft.FontWeight.BOLD),
                    self.content_display,
                ],
                spacing=8,
            ),
            border=ft.border.all(1, ft.Colors.OUTLINE),
            border_radius=8,
            padding=10,
            expand=True,
        )

        # Stats
        stats_container = ft.Container(
            content=self.stats_text, padding=ft.padding.symmetric(vertical=10)
        )

        # Status bar
        status_bar = ft.Container(
            content=self.status_text,
            padding=ft.padding.symmetric(vertical=10),
            alignment=ft.alignment.center,
        )

        # Main layout
        main_column = ft.Column(
            [
                header,
                button_row,
                file_info_container,
                content_container,
                stats_container,
                status_bar,
            ],
            spacing=0,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        self.page.add(main_column)

    def on_file_picked(self, e: ft.FilePickerResultEvent):
        """Handle file selection"""
        if e.files:
            self.selected_file_path = e.files[0].path
            self.file_info.value = (
                f"Selected: {e.files[0].name} ({e.files[0].size} bytes)"
            )
            self.process_btn.disabled = False
            self.status_text.value = "File selected. Click 'Process File' to analyze."
        else:
            self.selected_file_path = None
            self.file_info.value = "No file selected"
            self.process_btn.disabled = True
            self.status_text.value = "File selection cancelled"
        self.page.update()

    def process_file(self, e):
        """Process the selected file"""
        if not self.selected_file_path:
            return

        self.status_text.value = "Processing file..."
        self.process_btn.disabled = True
        self.page.update()

        try:
            # Read file content
            with open(self.selected_file_path, "r", encoding="utf-8") as f:
                self.file_content = f.read()

            # Display content (first 10000 chars)
            display_content = self.file_content[:10000]
            if len(self.file_content) > 10000:
                display_content += (
                    "\n\n... [content truncated, showing first 10000 characters]"
                )
            self.content_display.value = display_content

            # Calculate statistics
            lines = self.file_content.count("\n") + 1
            chars = len(self.file_content)
            words = len(self.file_content.split())

            # Try to detect file type and do specific processing
            file_ext = Path(self.selected_file_path).suffix.lower()
            extra_info = ""

            if file_ext == ".json":
                try:
                    data = json.loads(self.file_content)
                    if isinstance(data, dict):
                        extra_info = f" | JSON object with {len(data)} keys"
                    elif isinstance(data, list):
                        extra_info = f" | JSON array with {len(data)} items"
                except json.JSONDecodeError:
                    extra_info = " | Invalid JSON format"
            elif file_ext == ".csv":
                csv_lines = self.file_content.strip().split("\n")
                if csv_lines:
                    headers = csv_lines[0].split(",")
                    extra_info = f" | CSV with {len(headers)} columns, {len(csv_lines)-1} data rows"
            elif file_ext in [".py", ".js", ".ts", ".java", ".cpp", ".c", ".h"]:
                extra_info = f" | Source code file ({file_ext[1:].upper()})"

            self.stats_text.value = (
                f"Lines: {lines} | Words: {words} | Characters: {chars}{extra_info}"
            )
            self.status_text.value = "File processed successfully!"

        except UnicodeDecodeError:
            self.content_display.value = "[Error: File is not a valid UTF-8 text file]"
            self.stats_text.value = ""
            self.status_text.value = (
                "Error: Cannot read file (binary or invalid encoding)"
            )
        except Exception as ex:
            self.content_display.value = f"[Error: {str(ex)}]"
            self.stats_text.value = ""
            self.status_text.value = f"Error: {str(ex)}"
        finally:
            self.process_btn.disabled = False
            self.page.update()

    def clear_all(self, e):
        """Clear all content"""
        self.selected_file_path = None
        self.file_content = ""
        self.file_info.value = "No file selected"
        self.content_display.value = ""
        self.stats_text.value = ""
        self.status_text.value = "Ready"
        self.process_btn.disabled = True
        self.page.update()


def main(page: ft.Page):
    app = FileProcessorApp(page)


if __name__ == "__main__":
    if hasattr(ft, "app"):
        ft.app(target=main)
    else:
        # Prawidłowa obsługa środowiska Flet Mobile / Serious Python
        main(ft.Page())
