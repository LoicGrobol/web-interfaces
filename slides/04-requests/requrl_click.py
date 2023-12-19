import argparse

import click
import requests


@click.command("Download a text resource and print it")
@click.argument("url")
def main(url):
    response = requests.get(url)
    if response:
        print(response.text)
    else:
        print(f"Error (status code {response.status_code})")


if __name__ == "__main__":
    main()