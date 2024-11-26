import json

import argparse

import httpx


def main(argv=None):
    parser = argparse.ArgumentParser(description="Make http httpx")
    parser.add_argument("url", help="The url to request")
    parser.add_argument(
        "--header",
        help="Headers to add to the request, formatted as JSON.",
        default=dict(),
        type=json.loads,
    )
    parser.add_argument(
        "-X",
        "--request",
        help="The type of request to send.",
        choices=["GET", "PUT", "POST"],
        default="GET",
    )
    parser.add_argument("-o", "--output", help="A file to write the output to. Defaults to stdin.")
    parser.add_argument(
        "-d",
        "--data",
        help="Data to pass to a POST request, formatted as JSON.",
        default=dict(),
        type=json.loads,
    )

    args = parser.parse_args(argv)
    if args.request == "GET":
        response = httpx.get(
            args.url,
            headers=args.header,
        )
    elif args.request == "PUT":
        response = httpx.put(
            args.url,
            headers=args.header,
        )
    elif args.request == "POST":
        response = httpx.post(
            args.url,
            headers=args.header,
            data=args.data,
        )
    response = httpx.get(args.url)

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise e

    if args.output is None:
        print(response.text)
    else:
        with open(args.output, "w") as out_stream:
            out_stream.write(response.text)


if __name__ == "__main__":
    main()
