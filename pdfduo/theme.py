"""Thème moderne : clair ou sombre, couleur d'accent au choix."""
from PySide6.QtGui import QColor, QPalette

THEMES = {
    "clair": {"bg": "#f3f4f6", "panel": "#ffffff", "text": "#1f2328", "muted": "#6b7280",
              "border": "#d9dce1", "hover": "#e9ebef", "input": "#ffffff", "work": "#6b7280"},
    "sombre": {"bg": "#1d1f23", "panel": "#26292e", "text": "#e6e8eb", "muted": "#9aa0a8",
               "border": "#3a3e45", "hover": "#32363c", "input": "#1f2226", "work": "#141518"},
    "bleu nuit": {"bg": "#172033", "panel": "#1e2a42", "text": "#e3e9f5", "muted": "#94a3c2",
                  "border": "#2f3d5c", "hover": "#27365a", "input": "#152036", "work": "#0e1626"},
    "sable": {"bg": "#f4efe6", "panel": "#fbf8f2", "text": "#2b2620", "muted": "#7d7264",
              "border": "#ddd3c2", "hover": "#ece4d6", "input": "#fffdf8", "work": "#8b8172"},
}
ACCENTS = {"Rouge": "#e53935", "Bleu": "#1e88e5", "Vert": "#2e9b5a", "Violet": "#7e57c2",
           "Orange": "#f57c00", "Turquoise": "#00897b", "Rose": "#d81b60"}


def palette(t, accent):
    c = THEMES[t]
    p = QPalette()
    for role, key in ((QPalette.Window, "bg"), (QPalette.Base, "input"), (QPalette.AlternateBase, "hover"),
                      (QPalette.Button, "panel"), (QPalette.ToolTipBase, "panel")):
        p.setColor(role, QColor(c[key]))
    for role in (QPalette.WindowText, QPalette.Text, QPalette.ButtonText, QPalette.ToolTipText):
        p.setColor(role, QColor(c["text"]))
    p.setColor(QPalette.PlaceholderText, QColor(c["muted"]))
    p.setColor(QPalette.Highlight, QColor(accent))
    p.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    p.setColor(QPalette.Disabled, QPalette.Text, QColor(c["muted"]))
    p.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(c["muted"]))
    return p


def stylesheet(t, accent):
    c = dict(THEMES[t])
    a = QColor(accent)
    soft = f"rgba({a.red()},{a.green()},{a.blue()},0.16)"
    c.update(acc=accent, soft=soft)
    return """
QMainWindow, QDialog {{ background: {bg}; }}
QWidget {{ font-size: 10pt; }}
QMenuBar {{ background: {panel}; border-bottom: 1px solid {border}; padding: 2px; }}
QMenuBar::item {{ padding: 5px 10px; border-radius: 6px; }}
QMenuBar::item:selected {{ background: {soft}; }}
QMenu {{ background: {panel}; border: 1px solid {border}; border-radius: 8px; padding: 5px; }}
QMenu::item {{ padding: 6px 22px 6px 14px; border-radius: 5px; }}
QMenu::item:selected {{ background: {soft}; color: {text}; }}
QMenu::separator {{ height: 1px; background: {border}; margin: 4px 8px; }}
QToolBar {{ background: {panel}; border: none; border-bottom: 1px solid {border}; padding: 4px; spacing: 4px; }}
QToolBar#outils {{ border-bottom: none; border-right: 1px solid {border}; }}
QToolBar QLabel {{ color: {muted}; padding: 0 2px 0 6px; }}
QToolButton {{ border: 1px solid transparent; border-radius: 8px; padding: 4px 6px; color: {text}; }}
QToolButton:hover {{ background: {hover}; }}
QToolButton:checked {{ background: {soft}; border: 1px solid {acc}; color: {text}; }}
QToolBar#outils QToolButton {{ min-width: 62px; font-size: 8pt; padding: 2px 2px; }}
QDockWidget {{ titlebar-close-icon: none; }}
QDockWidget::title {{ background: {panel}; padding: 7px 10px; border-bottom: 1px solid {border};
                      font-weight: 600; text-align: left; }}
QDockWidget > QWidget {{ background: {panel}; }}
QListWidget, QTableWidget, QScrollArea, QPlainTextEdit {{ background: {panel}; border: 1px solid {border};
                      border-radius: 8px; }}
QListWidget::item {{ border-radius: 6px; padding: 2px; }}
QListWidget::item:hover {{ background: {hover}; }}
QListWidget::item:selected {{ background: {soft}; color: {text}; }}
QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox, QFontComboBox {{ background: {input}; border: 1px solid {border};
                      border-radius: 6px; padding: 3px 6px; min-height: 20px; }}
QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus, QSpinBox:focus {{ border: 1px solid {acc}; }}
QPushButton {{ background: {panel}; border: 1px solid {border}; border-radius: 7px; padding: 5px 12px; }}
QPushButton:hover {{ background: {hover}; }}
QPushButton:checked, QPushButton:default {{ background: {acc}; color: white; border: 1px solid {acc}; }}
QCheckBox::indicator {{ width: 15px; height: 15px; border-radius: 4px; border: 1px solid {border}; background: {input}; }}
QCheckBox::indicator:checked {{ background: {acc}; border: 1px solid {acc}; }}
QTabBar::tab {{ background: {bg}; padding: 6px 12px; border-top-left-radius: 7px; border-top-right-radius: 7px; }}
QTabBar::tab:selected {{ background: {panel}; color: {acc}; font-weight: 600; }}
QStatusBar {{ background: {panel}; border-top: 1px solid {border}; color: {muted}; }}
QHeaderView::section {{ background: {bg}; border: none; padding: 4px; }}
QScrollBar:vertical {{ background: transparent; width: 11px; margin: 2px; }}
QScrollBar::handle:vertical {{ background: {border}; border-radius: 4px; min-height: 30px; }}
QScrollBar:horizontal {{ background: transparent; height: 11px; margin: 2px; }}
QScrollBar::handle:horizontal {{ background: {border}; border-radius: 4px; min-width: 30px; }}
QScrollBar::add-line, QScrollBar::sub-line {{ width: 0; height: 0; }}
QToolTip {{ background: {panel}; color: {text}; border: 1px solid {border}; border-radius: 6px; padding: 5px; }}
""".format(**c)
