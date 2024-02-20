import os.path
from config import *
import keyboard


def file_explorer(path: str, flag: str, data: list) -> list | None:
    try:
        start = time_ms()
        if flag == "r":
            logging.info(f"Trying to open \"{os.path.basename(path)}\" file...")
            logging.info(f"Reading from source file...")

            with open(path) as f:
                data = [row for row in f]

            end = time_ms()
            logging.info(f"Source file \"{os.path.basename(path)}\" has read in {end - start} ms")

            return data

        elif flag == "w+":
            logging.info(f"Trying to open or create \"{os.path.basename(path)}\" file in \"output_data\" folder...")
            out = open(path, flag)
            logging.info(f"Writing in \"{os.path.basename(path)}\" file...")

            for item in data:
                out.write(str(item))
            out.close()

            end = time_ms()
            logging.info(f"Updated file \"{os.path.basename(path)}\" has wrote in {end - start} ms")

    except FileNotFoundError:
        logging.error(f"No such file: {path}")
        pass


def depersonalization(data: list) -> list:
    start = time_ms()
    logging.info("Hashing of personal data...")
    for line_number in range(len(data)):
        for pattern in pattern_list:
            if hashing(data[line_number], str(pattern)) is not None:
                hash_object = hashing(data[line_number], str(pattern))
                data[line_number] = re.sub(pattern=str(pattern), repl=hash_object, string=data[line_number])
    end = time_ms()
    logging.info(f"Depersonalization has done in {end - start} ms")

    return data


def main():
    start_time = time.time()
    logging.debug("Starting depersonalization of data...")
    for filename in listdir:
        source_file_path = os.path.join(ROOT_PATH, "input_data", filename)
        output_file_path = os.path.join(ROOT_PATH, "output_data", filename)

        source_data = file_explorer(path=source_file_path, flag="r", data=source)
        updated_data = depersonalization(data=source_data)
        file_explorer(path=output_file_path, flag="w+", data=updated_data)

    end_time = time.time()
    logging.debug(f"The program is completed in {end_time - start_time} seconds.")
    print("Press the space bar for exit.")
    while True:
        if keyboard.is_pressed(" "):
            sys.exit()


if __name__ == '__main__':
    main()
