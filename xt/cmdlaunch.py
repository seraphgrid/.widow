import sys
import subprocess
import tkinter as tk
import os
import glob

def run_command(command, use_xterm=True):
    if use_xterm:
        shell_keep = f"xterm -hold -e {command}"
        subprocess.Popen(shell_keep, shell=True)
    else:
        subprocess.Popen(command, shell=True)

def autocomplete(entry):
    # Get the current input from the entry
    current_input = entry.get()
    # Get the current working directory
    current_dir = os.getcwd()
    # Use glob to find matching files/directories
    matches = glob.glob(os.path.join(current_dir, current_input + '*'))
    
    if matches:
        # If there's a match, complete the entry with the first match
        entry.delete(0, tk.END)  # Clear the entry
        entry.insert(0, matches[0])  # Insert the first match

def show_input_box(full_command, use_xterm, append_arg=None):
    root = tk.Tk()
    root.configure(bg='black')

    label = tk.Label(root, text=full_command, fg='green', bg='black', font=('Liberation Mono', 9))
    label.pack(padx=0, pady=0)

    if append_arg:
        entry1 = tk.Entry(root, width=30, fg='green', bg='black', font=('Liberation Mono', 9))
        entry1.pack(side=tk.LEFT, padx=0, pady=0)

        entry2 = tk.Entry(root, width=30, fg='green', bg='black', font=('Liberation Mono', 9))
        entry2.pack(side=tk.RIGHT, padx=0, pady=0)

        entry1.focus_set()

        def on_submit(event=None):
            main_input = entry1.get()
            additional_input = entry2.get()
            full_command_with_args = f"{full_command} {main_input} {append_arg}{additional_input}"
            run_command(full_command_with_args, use_xterm)
            root.destroy()

        entry1.bind("<Return>", on_submit)
        entry2.bind("<Return>", on_submit)
        entry1.bind("<Tab>", lambda event: (autocomplete(entry1), "break"))
        entry2.bind("<Tab>", lambda event: (autocomplete(entry2), "break"))

    else:
        entry = tk.Entry(root, width=30, fg='green', bg='black', font=('Liberation Mono', 9))
        entry.pack(padx=0, pady=0)
        entry.focus_set()

        def on_submit(event=None):
            args = entry.get()
            full_command_with_args = f"{full_command} {args}"
            run_command(full_command_with_args, use_xterm)
            root.destroy()

        entry.bind("<Return>", on_submit)
        entry.bind("<Tab>", lambda event: (autocomplete(entry), "break"))

    root.attributes('-topmost', True)
    root.resizable(False, False)
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        use_xterm = True
        if '-n' in sys.argv:
            use_xterm = False
            sys.argv.remove('-n')

        append_arg = None
        if '-a' in sys.argv:
            a_index = sys.argv.index('-a')
            if a_index + 1 < len(sys.argv):
                append_arg = sys.argv[a_index + 1]
                sys.argv.pop(a_index)
                sys.argv.pop(a_index)

        directory = None
        if '-d' in sys.argv:
            d_index = sys.argv.index('-d')
            if d_index + 1 < len(sys.argv):
                directory = sys.argv[d_index + 1]
                sys.argv.pop(d_index)
                sys.argv.pop(d_index)

        if directory and os.path.isdir(directory):
            os.chdir(directory)
            print(f"Changed working directory to: {directory}")
        elif directory:
            print(f"Directory not found: {directory}")

        full_command = " ".join(sys.argv[1:])
        show_input_box(full_command, use_xterm, append_arg)
    else:
        print("No command provided.")
