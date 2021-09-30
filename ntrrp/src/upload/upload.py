

import re
import os, sys, argparse

from re import RegexFlag

from zipfile import ZipFile
from zipfile import BadZipFile

from client import Client
from exceptions import InitializationException
from exceptions import ProcessingException


DESC = 'This script uploads an archive containing a geotiff file and an optional csv file to the NAFI database. '\
       'The archive prefix until the first underscore, determines which table(s) will be updated' 
VERSION = '1.0.0'



def is_valid_archive(name):

    try:
         with ZipFile(name, 'r') as f:

            ftest = f.testzip()
            if ftest is None:
                return True
            else:
                print('The file \'%s\' in the archive \'%s\' is corrupted' % (ftest, name))
                return False

    except BadZipFile:
        return False


def is_valid_url(url):

    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', RegexFlag.IGNORECASE)

    return url is not None and regex.search(url)


def main(argv):

    script_name = os.path.basename(argv[0])
    logname = os.path.splitext(script_name)[0]

    parser = argparse.ArgumentParser(prog=script_name, description=DESC)
    mainGroup = parser.add_argument_group(title="Main Parameters")

    mainGroup.add_argument('-u', '--url', dest='url', metavar='UPLOAD URL', default = 'https://test.firenorth.org.au', help='Upload server url')
    mainGroup.add_argument('-f', '--file', dest='file', metavar='ZIP ARCHIVE', default = None, help='The zip file to be uploaded')

    mainGroup.add_argument('--version', dest='version', help='Displays script version/revision', default=False, action='store_true')


    args = parser.parse_args(argv[1:])

    # ====================================================== args.revision ====
    # Print Script version/revision
    if args.version:
        print('\n- Script \'%s\'; version: %s\n' % (script_name, VERSION))
        exit(0)

    try:
        # ==================================================================  args.url  =======
        if not is_valid_url(args.url):
            raise InitializationException('You need to specify a valid upload url. Found \'%s\'' % args.url)
        
        # ==================================================================  args.file  =======
        if args.file is None:
            raise InitializationException('You need to specified a zip file (option -f)')

        if not os.path.exists(args.file):
            raise InitializationException('The file to upload \'%s\' was not found' % args.file)

        fname = os.path.basename(args.file)
        if os.path.splitext(fname)[1].lower() != '.zip':
             raise InitializationException('You need to specified a zip archive, found \'%s\' (option -f)' % args.file)

        if not is_valid_archive(args.file):
            raise InitializationException('The specified archive is not a valid zip file (option -f)')

    except InitializationException as err:
        print(str(err))
        raise RuntimeError('script terminated due to initialization errors...')

    filename = args.file
    url = '%s/upload.php' % args.url

    print('Uploading archive \'%s\' to \'%s\'' % (filename, url))

    try:
        client = Client(url, 1024);
        client.upload_file(filename)

    except ProcessingException as err:
        raise RuntimeError('script terminated due to processing errors...')

    return


if __name__ == '__main__':

    try:
        sys.exit(main(sys.argv))
 
    except RuntimeError as err:
        print(str(err))
        sys.exit(-1)
 
    except KeyboardInterrupt:
        sys.exit(-1)
