from colorama import Fore, Style

def info(message):
  """Prints an informational message to the console with blue color."""
  print(f"{Fore.WHITE}║{Fore.BLUE}[INFO] {Style.RESET_ALL}- {message}")

def command(message):
  """Prints a command-related message to the console with light red color."""
  print(f"{Fore.WHITE}║{Fore.LIGHTRED_EX}[COMMANDS] {Style.RESET_ALL}- {message}")

def event(message):
  """Prints an event-related message to the console with yellow color."""
  print(f"{Fore.WHITE}║{Fore.YELLOW}[EVENTS] {Style.RESET_ALL}- {message}")

def join(message):
  """Prints a join-related message to the console with green color."""
  print(f"{Fore.GREEN}[JOIN] {Style.RESET_ALL}- {message}")

def leave(message):
  """Prints a leave-related message to the console with red color."""
  print(f"{Fore.RED}[LEAVE] {Style.RESET_ALL}- {message}")

def system(message):
  """Prints a system-related message to the console with magenta color."""
  print(f"{Fore.WHITE}║{Fore.MAGENTA}[SYSTEM] {Style.RESET_ALL}- {message}")