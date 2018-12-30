class Display_Manager:
    def __init__(self, initial_menu):
        self._display(initial_menu)
        self._menu_stack = []

    def open_menu(self, new_menu):
        pass

    def close_menu(self):
        pass


    def display(self, menu):
        pass



class Menu:
    def __init(self, options):
        """
        :param options: list of tuples (title, menu) describing a menu's choices
        """
        self._titles, self._menus = zip(*options)

    def get_menus(self):
        return self._menus
    def get_titles(self):
        return self._titles



