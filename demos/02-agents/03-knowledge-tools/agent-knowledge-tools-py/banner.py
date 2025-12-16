def print_banner(text: str) -> None:
    import shutil
    import textwrap
    try:
        width = shutil.get_terminal_size().columns
    except Exception:
        width = 80
    width = max(40, min(width, 100))
    border = "=" * width
    print(border)
    for line in textwrap.wrap(text, width - 4):
        print(f"| {line.ljust(width - 4)} |")
    print(border)
