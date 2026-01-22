from flask_menu import current_menu


def customize_menus(app):
    """Customize menus."""
    current_menu.submenu("main.communities").hide()
