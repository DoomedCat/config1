import os
import sys
import tkinter as tk
from tkinter import scrolledtext
import zipfile
import time

user_name = "Doomedcat"
disk_files = "disk.zip"
current_dir = "disk/"
last_command = ""
start_time = time.time()


def command_ls(path):
    info.insert(tk.END, f"{user_name} - {current_dir}> {last_command}\n")
    if len(path) == 0 or path == "." or path == './':
        with zipfile.ZipFile(disk_files, 'r') as zip:
            result = ""
            directories = set()
            for member in zip.namelist():
                if member.startswith(current_dir) and member != current_dir:
                    file = member[len(current_dir):].split("/")
                    if len(file) == 1:
                        result += file[0] + "\n"
                    elif len(file) > 1:
                        directories.add(file[0])
            for d in directories:
                result += d + "/\n"
            if len(result) == 0:
                info.insert(tk.END, 'Directory is empty\n')
                return 'Directory is empty\n'
            else:
                info.insert(tk.END, result)
                return result
    elif path == "~" or path == '/' or path == '~/':
        with zipfile.ZipFile(disk_files, 'r') as zip:
            result = ""
            directories = set()
            for member in zip.namelist():
                if member.startswith("disk/") and member != "disk/":
                    file = member[len("disk/"):].split("/")
                    if len(file) == 1:
                        result += file[0] + "\n"
                    elif len(file) > 1:
                        directories.add(file[0])
            for d in directories:
                result += d + "/\n"
            if len(result) == 0:
                info.insert(tk.END, 'Directory is empty\n')
                return 'Directory is empty\n'
            else:
                info.insert(tk.END, result)
                return result
    elif path == ".." or path == '../':
        dir = '/'.join(current_dir.split("/")[:-2]) + '/'
        if current_dir == "disk/":
            info.insert(tk.END, 'disk\n')
            return 'disk\n'
        else:
            with zipfile.ZipFile(disk_files, 'r') as zip:
                result = ""
                directories = set()
                for member in zip.namelist():
                    if member.startswith(dir) and member != dir:
                        file = member[len(dir):].split("/")
                        if len(file) == 1:
                            result += file[0] + "\n"
                        elif len(file) > 1:
                            directories.add(file[0])
                for d in directories:
                    result += d + "/\n"
                if len(result) == 0:
                    info.insert(tk.END, 'Directory is empty\n')
                    return 'Directory is empty\n'
                else:
                    info.insert(tk.END, result)
                    return result
    elif path[0] == '.' and path[1] == '.' and path[2] == '/':
        if path[3:].count('.') > 0:
            info.insert(tk.END, 'No such directory: ' + path + '\n')
            return 'No such directory: ' + path + '\n'
        if current_dir != 'disk/':
            path = ('/'.join(current_dir.split('/')[:-2]) + '/' + path[3:])
        else:
            path = current_dir + path[3:]
        with zipfile.ZipFile(disk_files, 'r') as zip:
            result = ""
            directories = set()
            flag = any(path == member and path.count('.') == 0 for member in zip.namelist())
            if not flag:
                info.insert(tk.END, 'No such directory: ' + path + '\n')
                return 'No such directory: ' + path + '\n'
            for member in zip.namelist():
                if member.startswith(path + "/") and member != path + "/":
                    file = member[len(path + "/"):].split("/")
                    if len(file) == 1:
                        result += file[0] + "\n"
                    elif len(file) > 1:
                        directories.add(file[0])
            for d in directories:
                result += d + "/\n"
            if len(result) == 0:
                info.insert(tk.END, 'Directory is empty\n')
                return 'Directory is empty\n'
            else:
                info.insert(tk.END, result)
                return result
    elif path[0] == '/' or (len(path) > 1 and path[0] == "~" and path[1] == '/'):
        if path[0] == "~" and path[1] == '/':
            path = path[2:]
            path = '/disk/' + path
        path = path[1:]
        with zipfile.ZipFile(disk_files, 'r') as zip:
            result = ""
            directories = set()
            flag = any(path == member and path.count('.') == 0 for member in zip.namelist())
            if not flag:
                info.insert(tk.END, 'No such directory: ' + path + '\n')
                return
            for member in zip.namelist():
                if member.startswith(path + "/") and member != path + "/":
                    file = member[len(path + "/"):].split("/")
                    if len(file) == 1:
                        result += file[0] + "\n"
                    elif len(file) > 1:
                        directories.add(file[0])
            for d in directories:
                result += d + "/\n"
            if len(result) == 0:
                info.insert(tk.END, 'Directory is empty\n')
                return 'Directory is empty\n'
            else:
                info.insert(tk.END, result)
                return result
    else:
        if path[0] == "." and path[1] == '/':
            path = path[2:]
        with zipfile.ZipFile(disk_files, 'r') as zip:
            result = ""
            directories = set()
            flag = any((current_dir + path) == member and path.count('.') == 0 for member in zip.namelist())
            if not flag:
                info.insert(tk.END, 'No such directory: ' + path + '\n')
                return 'No such directory: ' + path + '\n'
            for member in zip.namelist():
                if member.startswith(current_dir + path + "/") and member != current_dir + path + "/":
                    file = member[len(current_dir + path + "/"):].split("/")
                    if len(file) == 1:
                        result += file[0] + "\n"
                    elif len(file) > 1:
                        directories.add(file[0])
            for d in directories:
                result += d + "/\n"
            if len(result) == 0:
                info.insert(tk.END, 'Directory is empty\n')
                return 'Directory is empty\n'
            else:
                info.insert(tk.END, result)
                return result


def command_cd(path):
    global current_dir, last_command
    info.insert(tk.END, f"{user_name}@{current_dir}> {last_command}\n")
    if len(path) == 0 or path == '.' or path == './':
        info.insert(tk.END, current_dir + '\n')
        return current_dir + '\n'
    elif path == "~" or path == '/' or path == '~/':
        current_dir = "disk/"
    elif path[0] == '/' or (path[0] == "~" and path[1] == '/'):
        if path[0] == "~" and path[1] == '/':
            path = path[2:]
            path = '/disk/' + path
        new_dir = path[1:]
        with zipfile.ZipFile(disk_files, 'r') as zip:
            flag = any(new_dir + '/' == member and path.count('.') == 0 for member in zip.namelist())
            if flag:
                current_dir = new_dir + '/'
            else:
                info.insert(tk.END, 'No such directory: ' + path + '\n')
                return 'No such directory: ' + path + '\n'
    elif path == ".." or path == '../':
        if current_dir == "disk/":
            return 'already in disk'
        current_dir = '/'.join(current_dir.split("/")[:-2]) + '/'
    elif path[0] == '.' and path[1] == '.' and path[2] == '/':
        if path[3:].count('.') > 0:
            info.insert(tk.END, 'No such directory: ' + path + '\n')
            return 'No such directory: ' + path + '\n'
        if current_dir != 'disk/':
            dir = ('/'.join(current_dir.split('/')[:-2]) + '/' + path[3:])
        else:
            dir = current_dir + path[3:]
        with zipfile.ZipFile(disk_files, 'r') as zip:
            flag = any((dir + '/' == member and dir.count('.') == 0 for member in zip.namelist()))
            if not flag:
                info.insert(tk.END, 'No such directory: ' + dir + '\n')
                return 'No such directory: ' + dir + '\n'
            else:
                current_dir = dir + '/'
    else:
        if path[0] == "." and path[1] == '/':
            path = path[2:]
        with zipfile.ZipFile(disk_files, 'r') as zip:
            flag = any((current_dir + path + '/' == member and path.count('.') == 0 for member in zip.namelist()))
            if not flag:
                info.insert(tk.END, 'No such directory: ' + path + '\n')
                return 'No such directory: ' + path + '\n'
            else:
                current_dir += path + '/'
    return current_dir


def command_uptime():
    uptime = time.time() - start_time
    info.insert(tk.END, f"{user_name}@{current_dir}> {last_command}\nUptime: {int(uptime)} seconds\n")
    return f'Uptime: {uptime} seconds\n'


def command_wc(files):
    info.insert(tk.END, f"{user_name}@{current_dir}> {last_command}\n")
    if len(files) == 0:
        info.insert(tk.END, 'Empty\n')
        return 'Empty\n'
    result = ""
    for file in files:
        path = resolve_path(file)
        with zipfile.ZipFile(disk_files, 'r') as zip:
            if path in zip.namelist():
                with zip.open(path) as f:
                    content = f.read().decode('utf-8')
                    lines = content.splitlines()
                    words = content.split()
                    chars = len(content)
                    result += f"{len(lines)} {len(words)} {chars} {file}\n"
            else:
                result += f'No such file: {path}\n'
    info.insert(tk.END, result)
    return result


def resolve_path(file):
    if file[0] == '/':
        path = file[1:]
    elif file[0] == '~' and file[1] == '/':
        path = 'disk/' + file[2:]
    elif len(file) > 1 and file[0] == '.' and file[1] == '/':
        path = current_dir + file[2:]
    elif len(file) > 2 and file[0] == '.' and file[1] == '.' and file[2] == '/':
        if current_dir != 'disk/':
            path = ('/'.join(current_dir.split('/')[:-2]) + '/' + file[3:])
        else:
            path = current_dir + file[3:]
    else:
        path = current_dir + file
    return path


def command_analyzer():
    global last_command
    commandline = entry.get()
    entry.delete(0, tk.END)
    command = commandline.split()
    last_command = commandline
    info.config(state=tk.NORMAL)
    if len(command) == 0:
        pass
    elif command[0] == 'ls':
        command_ls(command[1] if len(command) > 1 else "")
    elif command[0] == 'cd':
        command_cd(command[1] if len(command) > 1 else "")
    elif command[0] == 'exit':
        sys.exit(0)
    elif command[0] == 'uptime':
        command_uptime()
    elif command[0] == 'wc':
        command_wc(command[1:])
    else:
        info.insert(tk.END, f"{user_name}@{current_dir}> {last_command} - Unknown command\n")
    directory.config(text=f"{current_dir}>")
    info.config(state=tk.DISABLED)
    info.see(tk.END)


def GUI():
    global root, info, input_frame, directory, entry, button
    root = tk.Tk()
    root.title("Virtual Shell")
    root.geometry("1200x600")
    info = scrolledtext.ScrolledText(root, width=40, height=10, wrap=tk.WORD, font=("Kristen ITC", 14), bg="white")
    info.insert(tk.END, f"Welcome to vShell, {user_name}\n")
    info.pack(expand=True, fill='both')
    info.config(state=tk.DISABLED)
    input_frame = tk.Frame(root, bg='white')
    input_frame.pack(expand=True, fill='both')
    directory = tk.Label(input_frame, font=("Kristen ITC", 14), text=f"{current_dir}>", bg="white")
    directory.pack(side=tk.LEFT, padx=30)
    entry = tk.Entry(input_frame, width=50, font=("Kristen ITC", 14))
    entry.pack(side=tk.LEFT, padx=30)
    entry.bind('<Return>', lambda event: command_analyzer())
    button = tk.Button(input_frame, text="Confirm", command=command_analyzer, font=("Kristen ITC", 14))
    button.pack(side=tk.LEFT, padx=30)
    root.resizable(False, False)
    return root


root = GUI()
root.mainloop()
