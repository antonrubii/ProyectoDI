def load_stylesheet():
    with open("styles.qss", "r", encoding="utf-8") as f:
        return f.read()