import re
import math
import time
import os
import sys
import argparse
import requests

from re import RegexFlag

from zipfile import ZipFile
from zipfile import BadZipFile


class InitializationException(Exception):

    """
    Exception raised when there is a error during a script initialization.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = "Initialization error"
        return

    def __str__(self):
        return self.message


class ProcessingException(Exception):

    """
    Exception raised when there is a metric processing error.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = "Processing error"
        return

    def __str__(self):
        return self.message


class Client:
    def __init__(self, api_url, max_byte_length):
        self.api_url = api_url
        self.max_byte_length = max_byte_length

    def upload_file(self, file_path, debug=False):
        file_size = os.path.getsize(file_path)
        headers = {"Filename": os.path.basename(file_path)}
        # headers['Content-type'] = 'application/bianry'

        try:
            with open(file_path, "rb") as file:
                start = 0

                # In python2 12/5 equals to 2 if file_size int. So we are casting to float for compatibility
                chunk_count = math.ceil(float(file_size) / self.max_byte_length)
                print("Total chunk count:", chunk_count)
                retry_timeout = 1
                sent_chunk_count = 0

                while True:
                    end = min(file_size, start + self.max_byte_length)
                    headers["Content-Range"] = "bytes={}-{}/{}".format(
                        start, end - 1, file_size
                    )

                    file.seek(start)
                    data = file.read(self.max_byte_length)
                    start = end

                    upload_endpoint = "%s" % self.api_url

                    try:
                        response = requests.put(
                            upload_endpoint, headers=headers, data=data
                        )
                        print(response.text)
                        if response.ok:
                            if debug:
                                print(
                                    "[Content-Range] => %s" % headers["Content-Range"]
                                )
                                print(
                                    "{}. chunk sent to server for a total of {} kbytes so far....".format(
                                        sent_chunk_count + 1, end / 1024
                                    )
                                )
                            sent_chunk_count += 1

                    except requests.exceptions.RequestException:
                        print(
                            "Error while sending chunk to server. Retrying in {} seconds".format(
                                retry_timeout
                            )
                        )
                        time.sleep(retry_timeout)

                        # Sleep for max 10 seconds
                        if retry_timeout < 10:
                            retry_timeout += 1
                        continue

                    if sent_chunk_count >= chunk_count:
                        return True

                return False

        except IOError:
            raise ProcessingException("Unable to open file '%s'" % file_path)


DESC = (
    "This script uploads an archive containing a geotiff file and an optional csv file to the NAFI database. "
    "The archive prefix until the first underscore, determines which table(s) will be updated"
)
VERSION = "1.0.0"


def is_valid_archive(name):
    try:
        with ZipFile(name, "r") as f:
            ftest = f.testzip()
            if ftest is None:
                return True
            else:
                print("The file '%s' in the archive '%s' is corrupted" % (ftest, name))
                return False

    except BadZipFile:
        return False


def is_valid_url(url):
    regex = re.compile(
        r"^https?://"  # http:// or https://
        # domain...
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        RegexFlag.IGNORECASE,
    )

    return url is not None and regex.search(url)


def main(argv):
    script_name = os.path.basename(argv[0])
    logname = os.path.splitext(script_name)[0]

    parser = argparse.ArgumentParser(prog=script_name, description=DESC)
    mainGroup = parser.add_argument_group(title="Main Parameters")

    mainGroup.add_argument(
        "-u",
        "--url",
        dest="url",
        metavar="UPLOAD URL",
        default="https://test.firenorth.org.au",
        help="Upload server url",
    )
    mainGroup.add_argument(
        "-f",
        "--file",
        dest="file",
        metavar="ZIP ARCHIVE",
        default=None,
        help="The zip file to be uploaded",
    )
    mainGroup.add_argument(
        "-cs",
        "--chunksize",
        dest="chunksize",
        metavar="CHUNK SIZE",
        type=int,
        default=1024,
        help="The max chunk size during upload",
    )

    mainGroup.add_argument(
        "-v",
        "--verbose",
        default=False,
        action="store_true",
        help="verbose, debug mode",
    )

    mainGroup.add_argument(
        "--version",
        dest="version",
        help="Displays script version/revision",
        default=False,
        action="store_true",
    )

    args = parser.parse_args(argv[1:])

    # ====================================================== args.revision ====
    # Print Script version/revision
    if args.version:
        print("\n- Script '%s'; version: %s\n" % (script_name, VERSION))
        exit(0)

    try:
        # ==================================================================  args.url  =======
        if not is_valid_url(args.url):
            raise InitializationException(
                "You need to specify a valid upload ur:l. Found '%s'" % args.url
            )

        # ==================================================================  args.file  =======
        if args.file is None:
            raise InitializationException(
                "You need to specified a zip file (option -f)"
            )

        if not os.path.exists(args.file):
            raise InitializationException(
                "The file to upload '%s' was not found" % args.file
            )

        fname = os.path.basename(args.file)
        if os.path.splitext(fname)[1].lower() == ".zip":
            if not is_valid_archive(args.file):
                raise InitializationException(
                    "The specified archive is not a valid zip file (option -f)"
                )

        # ==================================================================  args.chunksize  =======

    except InitializationException as err:
        print(str(err))
        raise RuntimeError("script terminated due to initialization errors...")

    #  ========  Set call parameters  ========

    url = "%s/upload.php" % args.url
    archive = args.file
    chunksize = args.chunksize
    debug = args.verbose

    print("Uploading archive '%s' to '%s'" % (archive, url))

    try:
        client = Client(url, chunksize)
        if client.upload_file(archive, debug):
            print("\n ===>  %s: upload successful..." % archive)

    except ProcessingException as err:
        raise RuntimeError("script terminated due to processing errors...")

    return


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))

    except RuntimeError as err:
        print(str(err))
        sys.exit(-1)

    except KeyboardInterrupt:
        sys.exit(-1)
