"""Enthält die visuellen Aspekte der App.
# nicht up-to-date

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

# REFACTOR: Nach dem MVC Model müssten zumindest die Button-commands in ein
# eigenes Modul kommen, da sie die Daten am ehesten verändern.

import tkinter as tk
import typing
import logic


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
    Wird als Singleton verwendet. Window()() kann als shorthand für
    get_instance() verwendet werden.

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

    def __call__(self, *args, **kwargs):
        return self.get_instance()

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
                ControlPage.update_pages(name, self)
            self.widgetName = name
            self.master = master


class ControlPage(Window.Page):
    """Dient als controller für die restlichen Pages (äq. zu Frames).
    Wird als Singleton verwendet. ControlPage(...)() kann als shorthand für
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
        wird stattdessen das Dictionary als Fallback zurückgegeben.

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

    def __init__(self, master: ControlPage, name='main', *args,
                 **kwargs) -> None:
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

    def __init__(self, master: ControlPage, name='game', *args,
                 **kwargs) -> None:
        super().__init__(master, name=name, *args, **kwargs)
        self.configure(bg='#d0f4de')
        self.place(relheight=1.0, relwidth=1.0)

        # initialisiert ein neues Spiel.
        self.game = logic.Game()
        print(f'{self.game.number}')    # debug

        # IDEA: trace_add() sollte eigentlich besser funktionieren können,
        # um das Label dynamisch updaten zu können.

        # output-Label setup
        self.dialog = tk.Label(self, bg='#d0f4de')
        start_text = self.game.get_next_dialog(self.game.gen_start)

        self.dialog_text_var = tk.StringVar(self.dialog)
        self.dialog_text_var.initialize(start_text)

        self.dialog.configure(textvariable=self.dialog_text_var)
        self.dialog.pack()

        # input-Entry setup
        self.entry = tk.Entry(self,
                              bg='#e4c1f9',
                              validate='focusout',
                              validatecommand=self.forward)

        self.entry_text_var = tk.StringVar(self.entry)

        self.entry.configure(textvariable=self.entry_text_var)
        self.entry.focus()
        self.entry.pack()

        # button setup
        b_names = ['Weiter', 'Zurück']
        b_dict: typing.Dict[str, tk.Button] = {}

        for i in b_names:
            b_dict |= {i: tk.Button(self, text=i, bg='#e4c1f9')}
            b_dict[i].pack()

        b_dict['Weiter'].configure(command=self.toggle_entry_state)
        b_dict['Zurück'].configure(command=self.back)

    def toggle_entry_state(self) -> None:
        """Wechselt den Zustand des Entry-widgets 'normal' <=> 'disabled'.
        Ändert auch den Fokus vom Entry, um dessen command zu triggern.

        """
        state: str = self.entry.cget('state')
        match state:
            case 'disabled':
                self.entry.configure(state='normal')
                self.entry.focus()

            case 'normal':
                self.entry.configure(state='disabled')
                self.dialog.focus()

            case _:
                pass

    def forward(self) -> bool:
        """Bringt den game-state voran, indem die Eingabe weitergegeben wird.

        """
        if self.check_and_notify():
            val = int(self.entry_text_var.get())
            res = self.game.get_dialog_text(val)
            # TODO: Hier gehört ein Debug-schalter hin und sowieso ein Logger.
            if self.game.is_win:
                res = f'{res} Punkte: {self.game.score_total}'
            self.dialog_text_var.set(res)
            return True
        return False

    def check_and_notify(self) -> bool:
        """Validiert den Entry-text und ändert das Dialog-Label.

        True:
            Input ist korrekt und kann weiter verarbeitet werden.
        False:
            Input ist fehlerhaft und Benachrichtigung ist erfolgt.

        """
        def is_valid_input() -> bool:
            """Validiert den Entry-text.

            """
            text_in = self.entry_text_var.get()
            if text_in.startswith('-') or not text_in.isdecimal():
                return False
            return True

        def notify() -> bool:
            """Ändert das Dialog-Label.

            """
            self.dialog_text_var.set(
                'Bitte gebe eine positive, ganze Zahl ein. ')
            # Penalty für falsche Eingaben.
            self.game.turn += 1
            return True

        res = not is_valid_input() and notify()
        return not res

    def update_dialog(self, gen: typing.Generator = None,
                      is_skip=False,
                      skip_count=1) -> None:
        """Updated das Dialog-Label mit neuem Dialog-Inhalt. Ohne Angabe wird
        gen_start als Generator verwendet.

        """
        gen_ = gen or self.game.gen_start
        sv: tk.StringVar() = self.dialog.cget('textvariable')
        sv.set(self.game.get_next_dialog(gen_, is_skip, skip_count))

    @staticmethod
    def back() -> None:
        """Wechselt zur Hauptseite.

        """
        ControlPage.get_page('main').tkraise()


class ScorePage(Window.Page):
    """Stellt die Leaderboard-seite der Anwendung dar.

    """

    def __init__(self, master: ControlPage, name='score', *args,
                 **kwargs) -> None:
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
    def back() -> None:
        """Wechselt zur Hauptseite.

        """
        ControlPage.get_page('main').tkraise()


class ConfigPage(Window.Page):
    """Stellt die Config-seite der Anwendung dar.

    """

    def __init__(self, master: ControlPage, name='config', *args,
                 **kwargs) -> None:
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
    def back() -> None:
        """Wechselt zur Hauptseite.

        """
        ControlPage.get_page('main').tkraise()

# COLORS:
# pink ff99c8 score
# yellow fcf6bd main
# lime d0f4de game
# blue a9def9 config
# purple e4c1f9 button

# IDEA: alternierende Funktionsaufrufe für Button-command-lambdas..
# def foo(i: int, *args, **kwargs):
#     i_ = i
#     print(f'foo args: {i_}')
#
#
# def bar(k: str, *args, **kwargs):
#     k_ = k
#     print(f'bar args: {k_}')
#
#
# def foobar() -> typing.Generator:
#     list_: list[typing.Callable] = [foo, bar]
#     while True:
#         for i in list_:
#             yield i
#
#
# gen = foobar()
# gen.__next__()(i=45, k='dasd')
# gen.__next__()(i=77, k='dasasdasd')
