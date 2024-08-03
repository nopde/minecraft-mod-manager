import os


class Option:
    def __init__(self, name: str, callback: callable, *args, **kwargs):
        self.name = name
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        self.callback(*self.args, **self.kwargs)


class Options:
    def __init__(self, options: list[Option]):
        self.options = options

    def __str__(self):
        options_str = ""
        counter = 1
        for option in self.options:
            options_str += f"{counter}. {option.name}\r\n"
            counter += 1
        return options_str


class OptionsMenu:
    def __init__(
        self,
        title: str,
        options_title: str,
        options: Options,
        select_title: str = "Select an option:",
        prefix: str = "> ",
    ):
        self.title = title
        self.options_title = options_title
        self.options = options
        self.select_title = select_title
        self.prefix = prefix

    def build(self):
        return f"{self.title}\r\n\r\n{self.options_title}\r\n{str(self.options)}\r\n\r\n{self.select_title}"

    def render(self):
        os.system("cls")
        print(self.build())

        menu_input = input(self.prefix)

        try:
            option_input = int(menu_input)
            selected_option = self.options.options[option_input - 1]
            self.select_option(selected_option)
        except ValueError:
            print("Option must be a number.")
            self.render()
        except IndexError:
            print("Invalid option. Please select an option from the list.")
            self.render()
        except KeyError:
            print("Invalid option. Please select an option from the list.")
            self.render()

    def select_option(self, option: Option):
        option.execute()


class InputMenu:
    def __init__(self, title: str, select_text: str, prefix: str = "> "):
        self.title = title
        self.select_text = select_text
        self.prefix = prefix

    def build(self):
        return f"{self.title}\r\n\r\n{self.select_text}"

    def render(self):
        os.system("cls")
        print(self.build())

        menu_input = input(self.prefix)

        return menu_input


class EmptyMenu:
    def __init__(self, title: str):
        self.title = title

    def build(self):
        return f"{self.title}\r\n"

    def render(self):
        os.system("cls")
        print(self.build())
