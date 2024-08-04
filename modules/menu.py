import os
import keyboard
import time

# class Action:
#     def __init__(self, action: callable, *action_args, **action_kwargs):
#         self.action = action
#         self.action_args = action_args
#         self.action_kwargs = action_kwargs

#     def execute(self):
#         self.action(*self.action_args, **self.action_kwargs)


# class Option:
#     def __init__(self, name: str, action: Action, callback: callable = None):
#         self.name = name
#         self.action = action
#         self.callback = callback

#     def execute(self):
#         self.action.execute()
#         if self.callback:
#             self.callback()


# class Options:
#     def __init__(self, options: list[Option]):
#         self.options = options

#     def __str__(self):
#         options_str = ""
#         counter = 1
#         for option in self.options:
#             options_str += f"{counter}. {option.name}\r\n"
#             counter += 1
#         return options_str


# class OptionsMenu:
#     def __init__(
#         self,
#         title: str,
#         options_title: str,
#         options: Options,
#         select_title: str = "Select an option:",
#         prefix: str = "> ",
#     ):
#         self.title = title
#         self.options_title = options_title
#         self.options = options
#         self.select_title = select_title
#         self.prefix = prefix

#     def build(self):
#         return f"{self.title}\r\n\r\n{self.options_title}\r\n{str(self.options)}\r\n\r\n{self.select_title}"

#     def render(self):
#         os.system("cls")
#         print(self.build())

#         menu_input = input(self.prefix)

#         try:
#             option_input = int(menu_input)
#             selected_option = self.options.options[option_input - 1]
#             self.select_option(selected_option)
#         except ValueError:
#             print("Option must be a number.")
#             self.render()
#         except IndexError:
#             print("Invalid option. Please select an option from the list.")
#             self.render()
#         except KeyError:
#             print("Invalid option. Please select an option from the list.")
#             self.render()

#     def select_option(self, option: Option):
#         option.execute()


# class InputMenu:
#     def __init__(self, title: str, select_text: str, prefix: str = "> "):
#         self.title = title
#         self.select_text = select_text
#         self.prefix = prefix

#     def build(self):
#         return f"{self.title}\r\n\r\n{self.select_text}"

#     def render(self):
#         os.system("cls")
#         print(self.build())

#         menu_input = input(self.prefix)

#         return menu_input


# class EmptyMenu:
#     def __init__(self, title: str):
#         self.title = title

#     def build(self):
#         return f"{self.title}\r\n"

#     def render(self):
#         os.system("cls")
#         print(self.build())


class Action:
    def __init__(self, action: callable, *args, **kwargs):
        self.action = action
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        self.action(*self.args, **self.kwargs)


class Option:
    def __init__(self, name: str, action: Action, callback: callable = None):
        self.name = name
        self.action = action
        self.callback = callback

    def __call__(self):
        self.action()
        if self.callback:
            self.callback()


class Options:
    def __init__(self, options: list[Option]):
        self.options = options


class OptionMenu:
    def __init__(self, title: str, subtitle: str, options: Options):
        self.title = title
        self.subtitle = subtitle
        self.options = options
        self.selected_option = 0
        self.key_pressed = True

    def render(self):
        os.system("cls")
        print(self.title, "\r\n")
        print(self.subtitle, "\r\n")
        for i, option in enumerate(self.options.options):
            if i == self.selected_option:
                print(f"{i + 1}. \033[4m\033[1m{option.name}\033[0m")
            else:
                print(f"{i + 1}. {option.name}")

    def __call__(self):
        self.render()
        while True:
            if keyboard.is_pressed("up") and not self.key_pressed:
                self.selected_option -= 1
                if self.selected_option < 0:
                    self.selected_option = len(self.options.options) - 1
                self.key_pressed = True
                self.render()
            elif keyboard.is_pressed("down") and not self.key_pressed:
                self.selected_option += 1
                if self.selected_option >= len(self.options.options):
                    self.selected_option = 0
                self.key_pressed = True
                self.render()
            elif keyboard.is_pressed("enter") and not self.key_pressed:
                self.options.options[self.selected_option]()
                self.key_pressed = True
            else:
                self.key_pressed = False
            time.sleep(0.1)


class InputMenu:
    def __init__(self, title: str, select_text: str):
        self.title = title
        self.select_text = select_text

    def get_input(self):
        print("", end="", flush=True)
        input_text = ""
        
        while True:
            event = keyboard.read_event()
            
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == "enter":
                    break
                elif event.name == "backspace":
                    input_text = input_text[:-1]
                    print("\b \b", end="", flush=True)
                elif len(event.name) == 1 and event.name.isprintable():
                    input_text += event.name
                    print(event.name, end="", flush=True)
        
        print()
        return input_text

    def build(self):
        return f"{self.title}\r\n\r\n{self.select_text}"

    def __call__(self):
        os.system("cls")
        print(self.build())

        menu_input = self.get_input()

        return menu_input


class EmptyMenu:
    def __init__(self, title: str):
        self.title = title

    def build(self):
        return f"{self.title}\r\n"

    def __call__(self):
        os.system("cls")
        print(self.build())
