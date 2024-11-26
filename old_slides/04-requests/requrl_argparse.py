import json

import argparse

import requests


def main(argv=None):
    parser = argparse.ArgumentParser(description="Make http requests")
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
    parser.add_argument(
        "-o", "--output", help="A file to write the output to. Defaults to stdin."
    )
    parser.add_argument(
        "-d",
        "--data",
        help="Data to pass to a POST request, formatted as JSON.",
        default=dict(),
        type=json.loads,
    )

    args = parser.parse_args(argv)
    if args.request == "GET":
        response = requests.get(
            args.url,
            headers=args.header,
        )
    elif args.request == "PUT":
        response = requests.put(
            args.url,
            headers=args.header,
        )
    elif args.request == "POST":
        response = requests.post(
            args.url,
            headers=args.header,
            data=args.data,
        )
    response = requests.get(args.url)
    if response:
        if args.output is None:
            print(response.text)
        else:
            with open(args.output, "w") as out_stream:
                out_stream.write(response.text)
    else:
        print(f"Error (status code {response.status_code})")


if __name__ == "__main__":
    main()
