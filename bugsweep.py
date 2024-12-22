#!/usr/bin/python3

from argparse import ArgumentParser

def main():
    parser = ArgumentParser(description="A script to handle domain argument input.")
    parser.add_argument("-d", "--domain", help="Specify the domain (e.g., example.com)", required=True, type=str)
    args = parser.parse_args()
    print(f"The provided domain is: {args.domain}")

if __name__ == "__main__":
    main()
