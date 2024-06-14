#! /usr/bin/env python

import argparse
import os
import requests

def addUserArgument(parser):
    parser.add_argument(
        "--user", "-u", 
        help="set the user to use for this command"
    )

def main():

    parser = argparse.ArgumentParser(description="Barcode drop CLI")

    # MARK: - Sub Commands -

    subparsers = parser.add_subparsers(
        help="sub commands for barcode drop",
        dest="command"
    )

    # MARK: Get Scans

    get_scans_parser = subparsers.add_parser(
        "scans",
        help="Get scans"
    )

    addUserArgument(get_scans_parser)

    get_scans_parser.add_argument(
        "--latest", "-l",
        help="only get the latest scan for the user",
        action="store_true",
        default=False
    )

    get_scans_parser.add_argument(
        "--format", "-f",
        help="The format of the output",
        choices=["json", "csv", "barcodes-only"],
        default="barcodes-only"
    )

    # MARK: Post Scan

    post_scan_parser = subparsers.add_parser(
        "scan",
        help="Post a new scan"
    )

    addUserArgument(post_scan_parser)

    post_scan_parser.add_argument(
        "barcode",
        help="Barcode to post"
    )

    # MARK: Delete Scans

    delete_scans_parser = subparsers.add_parser(
        "delete",
        help="Delete scans for the user"
    )

    addUserArgument(delete_scans_parser)

    delete_scans_parser.add_argument(
        "--except-last", "-e",
        help="Delete all scans except the last N scans (if omitted, all scans will be deleted)",
    )

    delete_scans_parser.add_argument(
        "--ids", "-i",
        nargs="*",
        help="Delete scans by ids",
    )


    # MARK: Set User

    setUserParser = subparsers.add_parser(
        "set-user",
        help="Set the default user for subsequent commands"
    )

    setUserParser.add_argument(
        "user", 
        help="The user to set as the default"
    )

    
    # MARK: - Finished Processing Arguments

    args = parser.parse_args()

    print(f"args: {args}")

if __name__ == "__main__":
    main()


class API:

    def __init__(self):
        self.user = None
        self.backend_url = os.getenv("BACKEND_URL", "http://localhost:8080")

    def set_user(self, user):
        self.user = user

    def get_scans(self, latest=False, format=None, user=None):
        f = format or "barcodes-only"
        u = user or self.user

        if not u:
            print(
                "No user set; please use the --user flag or set-user command"
            )
            return

        url = f"{self.backend_url}/scans/{u}"
        if latest:
            url += "/latest"
        url += "?latest={latest}&format={f}"
            
        print(f"Getting scans for user: {u} (url: {url})")


    def post_scan(self, barcode, user=None):
        u = user or self.user
        if not u:
            print(
                "No user set; please use the --user flag or set-user command"
            )
            return
        
        if not barcode:
            print("No barcode provided")
            return

        url = f"{self.backend_url}/scan/{u}?barcode={barcode}"

        print(f"Posting scan for user: {u}, barcode: {barcode}")

    def delete_scans(self, ids=None, user=None):
        u = user or self.user
        if not u:
            print(
                "No user set; please use the --user flag or set-user command"
            )
            return
        

        if not ids:
            print(f"will delete all scans for user {u}")
            url = f"{self.backend_url}/scans/{u}"
        else:
            print(
                f"Deleting scans with ids: {ids}"
            )
            idsQueryValue = ",".join(ids)
            url = f"{self.backend_url}/scans?ids={idsQueryValue}"
