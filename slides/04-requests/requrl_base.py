import sys

import requests


def main(argv):
    response = requests.get(argv[1])
    if response:
        print(response.text)
    else:
        print(f"Error (status code {response.status_code})")


if __name__ == "__main__":
    main(sys.argv)