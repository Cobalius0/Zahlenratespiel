"""Enthält die visuellen Aspekte der App.

Classes / Methods:
    Window(tk.Tk)
        get_instance() -> Window
    ControlPage(Window.Page)
        get_instance() -> ConfigPage
    MainPage(Window.Page)
        close()
        to_game()
        to_score()
        to_config()
    GamePage(Window.Page)
        back()
    ScorePage(Window.Page)
        back()
    ConfigPage(Window.Page)
        back()

"""

import tkinter as tk
import typing

# IDEA: Singleton per metaclass hook verwendbar machen.
# Sollte aber vlt abgelehnt werden wegen der Simplicity Regel.
# class Singleton(type):
#     """Implementiert das Singleton-Pattern als Metaclass."""
#
#     # Eine metaclass wird als eine Art Wrapper verwendet
#     # und ist damit verwandt mit decorators.
#     # Anscheinend wird als default eine standard metaclass(type) verwendet,
#     # wobei es in python.org keine Dokumentation zu C('metaclass=') gibt.
#
#     # Auch hier ein dunder, um es privat zu bekommen.
#     __instances = {}
#
#     def __new__(mcs, *args, **kwargs):
#         # Anscheinend wird hier mcs verwendet, um zu
#         # signalisieren, dass hier mit der metaclass gearbeitet wird.
#
#         # Im Folgenden würde der Konstruktor für type(),
#         # resp. type(mcs, name, bases, **kwargs) geändert werden.
#         pass
#
#     def __call__(cls, *args, **kwargs):
#         # Anscheinend kann die Funktion aus dem instanziierten obj
#         # ein callable machen.
#         if cls not in cls.__instances:
#             instance = super().__call__(*args, **kwargs)
#             # hier ebenfalls =| als shorthand für non-muted iterable-updates.
#             cls.__instances |= {cls: instance}
#             # Nachteil: Kann mitunter teure dict-lookups verursachen.
#             # Nicht geeignet für Overhead efficiency projects.
#         return cls.__instances[cls]


class Window(tk.Tk):
    """Stellt das root Window der App dar.
    Wird als Singleton verwendet.

    """
    __instance = None

    # True Singleton, weil die Anwendung nur mit einem Window arbeiten soll.
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self, *args, **kwargs) -> None:
        if self.__initialized:
            return

        super().__init__(*args, **kwargs)

        self.title('Zahlenratespiel')
        self.geometry('600x400')

        # BROCKEN: Wirft Errors wenn destroy() auf root.children
        #          angewendet wird. Dabei wird die Instanz von ControlPage
        #          nicht mehr zerstört und sys.exit() muss angewendet werden.
        # # Initialisiert die ControlPage mit.
        # ControlPage(self)

        self.__initialized = True

    @staticmethod
    def get_instance():
        """Gibt das Singleton-object zurück.

        """
        # Pfeilnotation kann nicht verwendet werden,
        # daher die explizite res variable.
        res: Window = Window.__instance
        return res

    # Als inner class, weil das Window zwangsweise eine Page hat,
    # diese aber nie ohne das Window verwendet werden kann.
    class Page(tk.Frame):
        """Vorkonfiguriert hiervon erbende tk.Frame-like Klassen.

        """
        def __init__(self, master, name, *args, **kwargs) -> None:
            __config = {
                      }

            super().__init__(master, __config, *args, **kwargs)
            if not isinstance(self, ControlPage):
                print('with ', name, self)
                res = ControlPage.update_pages(name, self)
                print('updated', res)
            self.widgetName = name
            self.master = master


class ControlPage(Window.Page):
    """Dient als controller für die restlichen Pages (äq. zu Frames).
    Wird als Singleton verwendet. ControlPage()() kann als shorthand für
    get_instance() verwendet werden.

    """
    _pages = {}

    __instance = None

    # True Singleton, weil die Anwendung mit einer ControlPage arbeiten soll.
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self, master: tk.Tk, name='control', *args, **kwargs) -> None:
        if self.__initialized:
            return

        super().__init__(master, name, *args, **kwargs)

        self.place(relheight=1.0, relwidth=1.0)

        self.__initialized = True

    def __call__(self, *args, **kwargs):
        return self.get_instance()

    @staticmethod
    def update_pages(key: str, val: Window.Page) -> bool:
        """Updated das Seiten-Dictionary und zeigt den Erfolg mittels
        bool Übergabe an.

        """
        try:
            ControlPage._pages |= {key: val}
            return True
        except ValueError:
            return False

    @staticmethod
    def get_page(key: str = None) -> Window.Page | dict:
        """Falls die gesuchte Seite nicht zurückgegeben werden konnte,
        wird stattdessen das Dictionary als Ganzes zurückgegeben.

        """
        try:
            return ControlPage._pages.get(key)
        except KeyError:
            return ControlPage._pages

    @staticmethod
    def get_instance():
        """Gibt das Singleton-object zurück.

        """
        res: ControlPage = ControlPage.__instance
        return res


class MainPage(Window.Page):
    """Stellt die Hauptseite der Anwendung dar.

    """
    def __init__(self, master: ControlPage, name='main', *args, **kwargs) -> None:
        super().__init__(master, name=name, *args, **kwargs)
        self.configure(bg='#fcf6bd')
        self.place(relheight=1.0, relwidth=1.0)

        b_names = ['Neues Spiel', 'Leaderboard', 'Optionen', 'Beenden']
        b_dict: typing.Dict[str, tk.Button] = {}

        for i in b_names:
            b_dict |= {i: tk.Button(self, text=i, bg='#e4c1f9')}
            b_dict[i].pack()

        b_dict['Neues Spiel'].configure(command=self.to_game)
        b_dict['Leaderboard'].configure(command=self.to_score)
        b_dict['Optionen'].configure(command=self.to_config)
        b_dict['Beenden'].configure(command=self.close)

    @staticmethod
    def close():
        """Beendet die Anwendung.

        """
        ControlPage.get_instance().master.quit()

    @staticmethod
    def to_game():
        """Wechselt zur Spielseite.

        """
        ControlPage.get_page('game').tkraise()

    @staticmethod
    def to_score():
        """Wechselt zur Leaderboard-seite.

        """
        ControlPage.get_page('score').tkraise()

    @staticmethod
    def to_config():
        """Wechselt zur Config-seite.

        """
        ControlPage.get_page('config').tkraise()
            

class GamePage(Window.Page):
    """Stellt die Spielseite der Anwendung dar.

    """
    def __init__(self, master: ControlPage, name='game', *args, **kwargs) -> None:
        super().__init__(master, name=name, *args, **kwargs)
        self.configure(bg='#d0f4de')
        self.place(relheight=1.0, relwidth=1.0)

        label = tk.Label(self, text='"Wie wär\'s mit einem Spiel?"', bg='#d0f4de')
        label.pack()
        entry = tk.Entry(self, bg='#e4c1f9')
        entry.pack()

        b_names = ['Zurück']
        b_dict: typing.Dict[str, tk.Button] = {}

        for i in b_names:
            b_dict |= {i: tk.Button(self, text=i, bg='#e4c1f9')}
            b_dict[i].pack()

        b_dict['Zurück'].configure(command=self.back)

    @staticmethod
    def back():
        """Wechselt zur Hauptseite.

        """
        ControlPage.get_page('main').tkraise()


class ScorePage(Window.Page):
    """Stellt die Leaderboard-seite der Anwendung dar.

    """
    def __init__(self, master: ControlPage, name='score', *args, **kwargs) -> None:
        super().__init__(master, name=name, *args, **kwargs)
        self.configure(bg='#ff99c8')
        self.place(relheight=1.0, relwidth=1.0)

        b_names = ['Zurück']
        b_dict: typing.Dict[str, tk.Button] = {}

        for i in b_names:
            b_dict |= {i: tk.Button(self, text=i, bg='#e4c1f9')}
            b_dict[i].pack()

        b_dict['Zurück'].configure(command=self.back)

    @staticmethod
    def back():
        """Wechselt zur Hauptseite.

        """
        ControlPage.get_page('main').tkraise()


class ConfigPage(Window.Page):
    """Stellt die Config-seite der Anwendung dar.

    """
    def __init__(self, master: ControlPage, name='config', *args, **kwargs) -> None:
        super().__init__(master, name=name, *args, **kwargs)
        self.configure(bg='#a9def9')
        self.place(relheight=1.0, relwidth=1.0)

        b_names = ['Zurück']
        b_dict: typing.Dict[str, tk.Button] = {}

        for i in b_names:
            b_dict |= {i: tk.Button(self, text=i, bg='#e4c1f9')}
            b_dict[i].pack()

        b_dict['Zurück'].configure(command=self.back)

    @staticmethod
    def back():
        """Wechselt zur Hauptseite.

        """
        ControlPage.get_page('main').tkraise()

# colors:
# pink ff99c8 score
# yellow fcf6bd main
# lime d0f4de game
# blue a9def9 config
# purple e4c1f9 button
