from urllib.request import urlretrieve
import os


def main():
    output = input('Output path (Include file name ex: path/to/file/file_name.py): ')
    url = input('URL: ')

    # Ensure the directory exists
    directory = os.path.dirname(output)
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        urlretrieve(url, output)
        print(f"File downloaded and saved as {output}")
    except Exception as e:
        print(f"An error occurred: {e}")


main()
