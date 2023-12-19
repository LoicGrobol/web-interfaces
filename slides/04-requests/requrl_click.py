import json

import click
import requests


@click.command(help="Download a text resource and print it")
@click.argument("url")
@click.option(
    "--header", "-H", help="Headers to add to the request, formatted as JSON."
)
@click.option(
    "--output",
    "-o",
    type=click.File("w"),
    default="-",
    help="A file to write the output to. Defaults to stdin.",
)
@click.option(
    "--request",
    "-X",
    type=click.Choice(["GET", "PUT", "POST"], case_sensitive=False),
    default="GET",
    show_default=True,
    help="The type of request to send.",
)
@click.option("--data", "-d", help="Data to pass to a POST request, formatted as JSON.")
def main(url, header, output, request, data):
    if request.lower() == "GET":
        response = requests.get(
            url,
            header=json.loads(header),
        )
    elif request.lower() == "PUT":
        response = requests.put(
            url,
            header=json.loads(header),
        )
    elif request.lower() == "POST":
        response = requests.post(
            url,
            header=json.loads(header),
            data=json.loads(data),
        )
    if response:
        output.write(response.text)
    else:
        print(f"Error (status code {response.status_code})")


if __name__ == "__main__":
    main()
