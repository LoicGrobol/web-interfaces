import sys

import httpx


def main(argv):
    response = httpx.get(argv[1])
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise e
    
    print(response.text)



if __name__ == "__main__":
    main(sys.argv)