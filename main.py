import colorama
from colorama import Fore, Style
from functools import partial

from helpers import parse_input, display_error_message
from handlers import (
    handle_hello,
    handle_add,
    handle_change,
    handle_phone,
    handle_all,
    handle_exit,
    handle_menu,
)
from instances import AddressBook

ADDRESS_BOOK = AddressBook()  # In-memory contacts database

EXIT_COMMANDS = {'exit', 'close', 'bye', 'q'}


def main_menu() -> str:
    """
    Displays the main menu options to the user.
    Returns:
        str: The main menu string.
    """
    menu_text = (
        f"{Style.BRIGHT}{Fore.BLUE}Please choose an option:{Style.RESET_ALL}\n"
        f"  {Fore.CYAN}* hello{Style.RESET_ALL} - Greet the user\n"
        f"  {Fore.CYAN}* add [name] [phone_number]{Style.RESET_ALL} - Add a new contact (10-digit phone)\n"
        f"  {Fore.CYAN}* change [name] [new_phone_number]{Style.RESET_ALL} - Update an existing contact's primary phone\n"
        f"  {Fore.CYAN}* phone [name]{Style.RESET_ALL} - Retrieve a contact's phone number\n"
        f"  {Fore.CYAN}* all{Style.RESET_ALL} - Display all contacts\n"
        f"  {Fore.CYAN}* exit/close/bye/q{Style.RESET_ALL} - Exit the application\n"
        f"  {Fore.CYAN}* menu{Style.RESET_ALL} - Show this menu again\n"
    )
    return menu_text

"""
Command to handler mapping
"""
COMMAND_HANDLERS = {
    'hello': handle_hello,
    'add': partial(handle_add, address_book=ADDRESS_BOOK),
    'change': partial(handle_change, address_book=ADDRESS_BOOK),
    'phone': partial(handle_phone, address_book=ADDRESS_BOOK),
    'all': partial(handle_all, address_book=ADDRESS_BOOK),
    'menu': partial(handle_menu, menu_provider=main_menu),
}


def _handle_command(command: str, args: list[str]) -> None:
    """
    Handles commands based on user input.
    Args:
        command (str): The command to handle.
        args (list[str]): List of arguments provided with the command.
    Raises:
        SystemExit: If the exit command is invoked.
    """
    if not command:
        return

    if command in EXIT_COMMANDS:
        handle_exit(args)
        return

    handler = COMMAND_HANDLERS.get(command)
    if handler:
        handler(args)
    else:
        display_error_message("Unknown command. Type 'menu' to see available options.")


def main():
    """
    Main function to run the command-line bot application.
    """
    colorama.init(autoreset=True)
    print(main_menu())
    while True:
        user_input = input(f"{Fore.BLUE}Enter command: {Style.RESET_ALL}")
        command, args = parse_input(user_input)
        _handle_command(command, args)


if __name__ == "__main__":
    main()
