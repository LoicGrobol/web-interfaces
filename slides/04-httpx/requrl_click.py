import json

import click
import httpx


@click.command(help="Mate http httpx.")
@click.argument("url")
@click.option(
    "--header",
    "-H",
    help="Headers to add to the request, formatted as JSON.",
    default="{}",
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
    default="GET",
    help="The type of request to send.",
    show_default=True,
    type=click.Choice(["GET", "PUT", "POST"], case_sensitive=False),
)
@click.option(
    "--data",
    "-d",
    default="{}",
    help="Data to pass to a POST request, formatted as JSON.",
)
def main(url, header, output, request, data):
    if request.upper() == "GET":
        response = httpx.get(
            url,
            headers=json.loads(header),
        )
    elif request.upper() == "PUT":
        response = httpx.put(
            url,
            headers=json.loads(header),
        )
    elif request.upper() == "POST":
        response = httpx.post(
            url,
            headers=json.loads(header),
            data=json.loads(data),
        )

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise e

    output.write(response.text)


if __name__ == "__main__":
    main()
