# Based on the original script from : Scito (https://scito.ch)
# Changes in this script:
# 1. Changed the QR code generation method to SimpleCodeGenerator from  Nir Sofer
# 2. Changed export format to have HTML and Molto-2 compatible import file
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import base64
import glob
import subprocess
from urllib.parse import parse_qs, urlencode, urlparse, quote
from os import name, path, remove
import generated_python.google_auth_pb2
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    '--verbose', '-v', help='verbose output', action='store_true')
arg_parser.add_argument(
    '--saveqr', '-s', help='save QR code(s) as images to the "qr" subfolder', action='store_true')
arg_parser.add_argument(
    '--printqr', '-p', help='print QR code(s) as text to the terminal', action='store_true')
arg_parser.add_argument(
    '--infile', help='file or - for stdin (default: -) with "otpauth-migration://..." URLs separated by newlines, lines starting with # are ignored')
arg_parser.add_argument(
    '--moltofile', help='save exctracted data in file compatible with Molto-2 format. If file does not exist a new file will be created.')
arg_parser.add_argument(
    '--htmlfile', help='save exctracted data in html file with QR codes for enrolling TOTP profiles to other apps or single profile tokens')
arg_parser.add_argument(
    '--fromimg', help='read otpauth-migration strings from a screenshot')
args = arg_parser.parse_args()

verbose = args.verbose

# https://stackoverflow.com/questions/40226049/find-enums-listed-in-python-descriptor-for-protobuf


def get_enum_name_by_number(parent, field_name):
    field_value = getattr(parent, field_name)
    return parent.DESCRIPTOR.fields_by_name[field_name].enum_type.values_by_number.get(field_value).name


def convert_secret_from_bytes_to_base32_str(bytes):
    return str(base64.b32encode(otp.secret), 'utf-8').replace('=', '')


def is_windows():
    return name == 'nt'


# decode from image to text file
if args.fromimg:
    if is_windows():
        qrscan = glob.glob('./qrscan/*/qrscan.exe', recursive=True)
    else:
        qrscan = glob.glob('./qrscan/*/qrscan', recursive=True)

    if not qrscan:
        raise "Couldn't find qrscan, cant decode image"
    elif len(qrscan) > 1:
        raise "Multiple qrscans found, did you add one manually?"

    if args.htmlfile:
        if path.exists(str(args.htmlfile)):
            remove(str(args.htmlfile))
        qrscan.append('--svg')
        qrscan.append(str(args.htmlfile))
    qrscan.append(str(args.fromimg))

    otpauth_list = list()
    for line in subprocess.check_output(qrscan).splitlines():
        otpauth_list.append(line.decode("utf-8"))

    print(type(otpauth_list))
    print(otpauth_list)
    for line in otpauth_list:
        print(f"line: {line}")

    qr_as_image_base64 = base64.b64encode(
        open(str(args.htmlfile), "rb").read())
    qr_as_image_base64 = qr_as_image_base64.decode('utf-8')
    remove(str(args.htmlfile))

elif args.infile:
    otpauth_list = str(args.infile).splitlines()
else:
    raise "Please provide either --infile or --fromimg as source"

i = j = 0
print('Starting the process')
for line in (line.strip() for line in otpauth_list):
    if verbose:
        print(line)
    if not line.startswith('otpauth-migration://'):
        print('\nWARN: line is not a otpauth-migration:// URL\ninput file: {}\nline "{}"\nProbably a wrong file was given'.format(otpauth_list, line))
    parsed_url = urlparse(line)
    params = parse_qs(parsed_url.query)
    if not 'data' in params:
        raise "result of qrscan looks invalid"
    data_encoded = params['data'][0]
    data = base64.b64decode(data_encoded)
    payload = generated_python.google_auth_pb2.MigrationPayload()
    payload.ParseFromString(data)
    i += 1
    if verbose:
        print('\n{}. Payload Line'.format(i), payload, sep='\n')
    line_count = -1
    # Count lines  in Molto2-export.txt
    if args.moltofile:
        if path.exists(args.moltofile):

            file = open(args.moltofile, "r")

            for line in file:
                if line != "\n":
                    line_count += 1
            file.close()

    # pylint: disable=no-member
    for otp in payload.otp_parameters:
        j += 1

        if verbose:
            print('\n{}. Secret Key'.format(j))
        else:
            print()
        print('Name:   {}'.format(otp.name))
        secret = convert_secret_from_bytes_to_base32_str(otp.secret)
        # print('Secret: {}'.format(secret))
        if otp.issuer:
            print('Issuer: {}'.format(otp.issuer))
        print('Type:   {}'.format(get_enum_name_by_number(otp, 'type')))
        url_params = {'secret': secret}
        if otp.type == 1:
            url_params['counter'] = otp.counter
        if otp.issuer:
            url_params['issuer'] = otp.issuer
        otp_url = 'otpauth://{}/{}?'.format('totp' if otp.type ==
                                            2 else 'hotp', quote(otp.name)) + urlencode(url_params)
        if args.moltofile:
            with open(args.moltofile, 'a') as f:
                # Create text file with seed info
                f.write(str(line_count+j)+' '+secret +
                        ' sha1 6 30 yes yes '+otp.issuer+'\n')
        if args.htmlfile:
            with open(args.htmlfile, 'a') as f2:
                # Create html file with seed info in QR format
                keyURI = "otpauth://totp/"+otp.name+"?secret="+secret  # +"?issuer="+otp.issuer
                # Generate QR code image
                f2.write('TOTP Profile '+str(line_count+j)+':'+otp.name +
                         "<br><img width=250 src='data:image/svg+xml;base64;utf-8,"+qr_as_image_base64+"'><pre>"+secret+"</pre><hr><br><br>")

print(' ')
print('Files have been generated:')
if args.htmlfile:
    print(args.htmlfile)
if args.moltofile:
    print(args.moltofile)
