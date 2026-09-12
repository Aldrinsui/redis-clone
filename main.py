from dataclasses import make_dataclass
import sys


ARITY = {
    "PING" : (0,1),
    "ECHO" : (1,1),
}

def error_message(message):
    return f"-{message}\r\n"

def handle_command(args):
    """Process a Redis command and return the RESP response."""
    cmd = args[0].upper()
    command_args = args[1:]

    if cmd == "PING":
        if len(args) == 1:
            return "+PONG\r\n"
       
        message = args[1]
        return bulk_string(message)
    
    elif cmd == "ECHO":    
        message = args[1]
        return bulk_string(message)

    elif cmd == "COMMAND" and len(args) > 1 and args[1].upper() == "DOCS":        
        return "+OK\r\n"           
   
    return f"-ERR unknown command '{cmd}'\r\n"

def bulk_string(message):
    return f"${len(message)}\r\n{message}\r\n"

def error_handling(cmd,command_args):
    low,high = ARITY[cmd]

    if not low <= len(command_args) <= high:
        return error_message(
            f"ERR wrong number of arguments for '{cmd.lower()}' command"
        )
    
    return None


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        args = parse_args(line)
        response = handle_command(args)
        sys.stdout.write(response)
        sys.stdout.flush()

def parse_args(line):
    args=[]
    current = ""
    in_quotes = False
    for ch in line:
        if ch == '"' and not in_quotes:
            in_quotes = True
        elif ch == '"' and in_quotes:
            in_quotes = False
        elif ch == ' ' and not in_quotes:
            if current:
                args.append(current)
                current = ""
        else:
            current += ch
    if current:
        args.append(current)
    
    return args

if __name__ == "__main__":
    main()
