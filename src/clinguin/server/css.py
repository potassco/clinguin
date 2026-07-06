"""Generates Tailwind CSS dynamically from the UI encoding files."""

import logging
import os
import subprocess
import sys

log = logging.getLogger(__name__)

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
APP_CSS_PATH = os.path.normpath(os.path.join(_THIS_DIR, "..", "client", "svelte", "src", "app.css"))

STATIC_DIR = os.path.join(os.getcwd(), "static")
GENERATED_CSS_PATH = os.path.join(STATIC_DIR, "generated.css")
TEMP_CSS_FILE = os.path.join(STATIC_DIR, "_temp_build.css")


def _create_temp_css_file(ui_files: list[str]) -> str:
    """Wrapper file: imports the real theme, then points Tailwind's
    scanner at each UI encoding file via @source so classes used
    dynamically in `attr/3` facts get included."""
    os.makedirs(STATIC_DIR, exist_ok=True)

    lines = [f'@import "{APP_CSS_PATH}";']
    lines += [f'@source "{os.path.abspath(f)}";' for f in ui_files]

    with open(TEMP_CSS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return TEMP_CSS_FILE


def _remove_temp_css_file(temp_css_file: str) -> None:
    if os.path.exists(temp_css_file):
        os.remove(temp_css_file)


def generate_tailwind_css(ui_files: list[str]) -> None:
    """Runs the Tailwind CLI (via pytailwindcss) once, at startup."""
    temp_css_file = _create_temp_css_file(ui_files)
    log.info("Compiling Tailwind CSS for: %s", ", ".join(ui_files))
    try:
        subprocess.run(["tailwindcss", "-i", temp_css_file, "-o", GENERATED_CSS_PATH], check=True)
        log.info("CSS compiled successfully -> %s", GENERATED_CSS_PATH)
    except subprocess.CalledProcessError as e:
        log.error("CSS compilation failed: %s", e)
        sys.exit(1)
    finally:
        _remove_temp_css_file(temp_css_file)
