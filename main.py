from config import *
import time
import tkinter as tk
from tkinter import filedialog


def gui():
    def browse_files():
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            entry_files.delete(1.0, tk.END)
            for file_path in file_paths:
                entry_files.insert(tk.END, file_path + '\n')

    def perform_action():
        file_paths = entry_files.get(1.0, tk.END).split('\n')
        file_paths = [path.strip() for path in file_paths if path.strip()]
        main(file_paths)

    root = tk.Tk()

    root.title("DepAPP")
    root.configure(bg="#222222")

    label_files = tk.Label(root, text="File paths:", fg="white", bg="#222222")
    label_files.pack()

    entry_files = tk.Text(root, fg="white", bg="#333333", width=50, height=10)
    entry_files.pack()

    button_browse = tk.Button(root, text="Обзор", command=browse_files, bg="#555555", fg="white")
    button_browse.pack()

    button_action = tk.Button(root, text="Depersonalize data", command=perform_action, bg="#555555", fg="white")
    button_action.pack()

    root.mainloop()


def file_explorer(path: str, flag: str, data: list) -> list:
    try:
        start = time_ms()
        if flag == "r":
            with open(path, encoding="utf-8") as f:
                data = [row for row in f]

            end = time_ms()
            logging.info(f"Source file {path} has read in {end - start} ms")

            return data

        elif flag == "w+":
            out = open(path, flag, encoding="utf-8")
            for item in data:
                out.write(str(item))
            out.close()

            end = time_ms()
            logging.info(f"Updated file {path} has wrote in {end - start} ms")

    except FileNotFoundError:
        logging.error(f"No such file: {path}")
        pass


def depersonalization(data: list) -> list:
    start = time_ms()
    logging.info("Hashing of personal data...")
    for line_number in range(len(data)):
        for pattern in pattern_list:
            if hashing(data[line_number], str(pattern)) is not None:
                hash_object = "Depersonal " + hashing(data[line_number], str(pattern))
                data[line_number] = re.sub(pattern=pattern, repl=hash_object, string=data[line_number])
    end = time_ms()
    logging.info(f"Depersonalization has done in {end - start} ms")

    return data


def main(file_paths):
    start_time = time.time()

    for file_path in file_paths:
        source_file_path = Path(file_path)
        output_file_path = os.path.join(Path(file_path).parent, "output_data")
        os.makedirs(output_file_path, exist_ok=True)
        output_file_path = os.path.join(Path(output_file_path), Path(os.path.basename(file_path)))

        source_data = file_explorer(path=source_file_path, flag="r", data=source)
        updated_data = depersonalization(data=source_data)
        file_explorer(path=output_file_path, flag="w+", data=updated_data)
    end_time = time.time()
    logging.debug(f"Depersonalization has done in {end_time - start_time} seconds")
    logging.info("The program is completed.\nPress the space bar for exit.")
    os.system(f"explorer {Path(file_path).parent}")


if __name__ == '__main__':
    gui()
