import argparse

import requests


def main(argv=None):
    parser = argparse.ArgumentParser(description="Make http request")
    parser.add_argument("url", help='The url to request')

    args = parser.parse_args(argv)
    response = requests.get(args.url)
    if response:
        print(response.text)
    else:
        print(f"Error (status code {response.status_code})")


if __name__ == "__main__":
    main()