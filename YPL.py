import os, random, time, pyautogui

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show(txt):
    print(txt)

def rand(a, b):
    return random.randint(a, b)

def sleep(seconds):
    time.sleep(seconds)

def ypl_input(txt=""):
    return input(txt)

def randl(list):
    return random.choice(list)

def move(x, y):
    pyautogui.moveTo(x, y)

def click():
    pyautogui.click()

def write(text):
    pyautogui.write(text)

# --- Start interpreter ---
ideMode = True
clear()

commands = []
variables = {
    "show": show,
    "rand": rand,
    "wait": sleep,
    "input": ypl_input,
    "randlist": randl,
    "move": move,
    "click": click,
    "write": write
}

collecting_if = False
collecting_else = False
if_block = []
else_block = []
if_condition = ""

print("Type your code here and type /run to execute the code.")

while ideMode:
    line = input(">> ")

    # RUN command
    if line.lower() == "/run":
        print("-----")
        try:
            for cmd in commands:
                if cmd.startswith("IFBLOCK:"):
                    condition = cmd.split(":", 1)[1].strip()
                    if eval(condition, {}, variables):
                        for sub in if_block:
                            exec(sub, {}, variables)
                    elif else_block:
                        for sub in else_block:
                            exec(sub, {}, variables)

                elif ":" in cmd and "show" not in cmd:
                    name, value = cmd.split(":", 1)
                    variables[name.strip()] = eval(value.strip(), {}, variables)

                else:
                    exec(cmd, {}, variables)

        except Exception as e:
            print(f"Error: {e}")
        print("-----")

        # Reset
        if_block, else_block = [], []
        collecting_if = collecting_else = False
        if_condition = ""

    # IF (...) start
    elif line.strip().startswith("if ") and line.strip().endswith("("):
        collecting_if = True
        if_condition = line.strip()[3:-1].strip()
        if_block = []

    # ELSE (...) start
    elif line.strip().startswith("else") and line.strip().endswith("("):
        collecting_else = True
        else_block = []

    # End of IF or ELSE block
    elif line.strip() == ")":
        if collecting_if:
            collecting_if = False
            commands.append(f"IFBLOCK: {if_condition}")
        elif collecting_else:
            collecting_else = False

    # Normal assignment
    elif ":" in line and "show" not in line and not collecting_if and not collecting_else:
        commands.append(line)

    # Inside IF or ELSE
    else:
        if collecting_if:
            if_block.append(line)
        elif collecting_else:
            else_block.append(line)
        else:
            commands.append(line)
