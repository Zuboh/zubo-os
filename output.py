RESET = "\033[0m"
CYAN  = "\033[36m"
RED   = "\033[31m"
WHITE = "\033[37m"
GRAY  = "\033[90m"

def tool_line(name: str, **kwargs: str) -> str:
    params = " ".join(f"{k}={v}" for k, v in kwargs.items())
    return f"{CYAN}[TOOL]{RESET} {name} {GRAY}{params}{RESET}"

def error_line(msg: str) -> str:
    return f"{RED}[ERROR]{RESET} {msg}"

def response_line(text: str) -> str:
    return f"{WHITE}{text}{RESET}"

def info_line(msg: str) -> str:
    return f"{GRAY}[INFO]{RESET} {msg}"
