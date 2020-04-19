import logging
import argparse
import datetime
import os
import sys
import subprocess
import shutil
import io

logging.basicConfig(filename='error_log.txt', filemode='a', level=logging.DEBUG, format="[%(asctime)s] %(message)s", datefmt='%H:%M:%S')
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logging.getLogger('').addHandler(console)
logger = logging.getLogger(__name__)

from typing import Dict, Any, List, Tuple, Optional
from xml.dom import minidom  # type: ignore

from chartv2 import Chartv2, XMLv2
from audio import TwoDX, ADPCM
from exception_handler import exception_handler


def main() -> int:
    parser = argparse.ArgumentParser(
        description="A utility to convert 16-lane StepMania charts (.ssc format) to Museca format.")
    parser.add_argument(
        "file",
        metavar="FILE",
        help=".ssc file to convert to Museca format.",
        type=str,
    )
    parser.add_argument(
        "-id",
        metavar="ID",
        help="ID to assign this song.",
        type=int,
        default=None,
    )
    parser.add_argument(
        "-d",
        "--directory",
        help="Directory to place files in. Defaults to current directory.",
        default='.',
    )
    parser.add_argument(
        "-x",
        "--new-xml",
        help="Location of an isolated music-info-b.xml to create. If not specified, "
             "a new one will be created or updated automatically in the xml directory.",
        default=None,
    )
    parser.add_argument(
        "-v",
        "--verify",
        help="Checks the ssc files for errors without converting or writing files.",
        action='store_true'
    )

    args = parser.parse_args()
    root = args.directory
    if root[-1] != '/':
        root = root + '/'
    root = os.path.realpath(root)

    # First, parse out the chart and get the XML writer ready.
    fp = open(args.file, 'rb')
    data = fp.read()
    fp.close()

    if args.verify:
        err = 0
        try:
            print("Verifying - " + args.file)
            chart = Chartv2(data)
            if args.id is None and chart.metadata.get('subtitle') is None:
                raise Exception("No ID found in SSC file! Please specify an id in the #SUBTITLE:x; field.")
            xml = XMLv2(chart, args.id)
            if chart.metadata.get('samplestart') is None:
                raise Exception('Music file present but no sample start specified for preview!')
            if not os.path.exists(os.path.split(args.file)[0] + '\\' + 'jacket.png'):
                logger.critical(os.path.splitext(os.path.basename(args.file))[0] + " - Missing jacket.png")
                # err = 1
            if not os.path.exists(os.path.split(args.file)[0] + '\\' + 'jacketSmall.png'):
                logger.critical(os.path.splitext(os.path.basename(args.file))[0] + " - Missing jacketSmall.png")
                # err = 1

        except Exception as msg:
            exception_handler(msg, args.file)
        if err:
            sys.exit(1)
        else:
            sys.exit(0)


    try:
        chart = Chartv2(data)
    except Exception as msg:
        exception_handler(msg, args.file)

    if args.id is None and chart.metadata.get('subtitle') is None:
        exception_handler("No ID found in SSC file! Please specify an id in the #SUBTITLE:x; field.", args.file)
    elif args.id is None and chart.metadata.get('subtitle') is not None:
        args.id = int(chart.metadata.get('subtitle'))
    elif args.id is not None and chart.metadata.get('subtitle') is not None:
        args.id = int(chart.metadata.get('subtitle'))
    else:
        if args.id is not None and chart.metadata.get('subtitle') is None:
            args.id = args.id
    try:
        xml = XMLv2(chart, args.id)
    except Exception as msg:
        exception_handler(msg, args.file)

    output_dir = 'custom_charts'
    jacket_b_dir = os.path.join(root, output_dir, 'graphics', 'jacket_b')
    jacket_s_dir = os.path.join(root, output_dir, 'graphics', 'afp', 'museca1_5', 'pix_jk_s_2_ifs')
    music_dir = os.path.join(root, output_dir, 'museca', 'sound', 'music', '01_{num:04d}'.format(num=args.id))
    xml_dir = os.path.join(root, output_dir, 'museca', 'xml')
    os.makedirs(root, exist_ok=True)
    os.makedirs(music_dir, exist_ok=True)
    os.makedirs(xml_dir, exist_ok=True)
    os.makedirs(jacket_b_dir, exist_ok=True)
    os.makedirs(jacket_s_dir, exist_ok=True)

    print("%d %s" % (args.id, chart.metadata.get('title')))
    print('Parsing chart data...')

    # Changing default XML handling to update if an xml is present in the xml_dir.
    # Argument will now be used to specify location of a new, isolated XML file.

    def xstr(s):
        if s is None:
            return ''
        return str(s)

    empty_xml_arg = xstr(args.new_xml)
    new_xml_path = xstr(os.path.join(empty_xml_arg, 'music-info-b.xml'))

    if new_xml_path == os.path.join(xml_dir, 'music-info-b.xml'):
        exception_handler('This XML directory is reserved for the converter!', args.file)
    elif os.path.exists(os.path.join(xml_dir, 'music-info-b.xml')) is False and args.new_xml is not None:
        print("Isolating XML...")
        # First, write out a metadata file, that can be copied into music-info.xml
        fp = open(args.new_xml, "wb")
        fp.write(xml.get_metadata())
        fp.close()
    elif os.path.exists(os.path.join(xml_dir, 'music-info-b.xml')) is True and args.new_xml is None:
        print("Updating XML...")
        # First, update the metadata file with the info from this chart.
        fp = open(os.path.join(xml_dir, 'music-info-b.xml'), "rb")
        data = fp.read()
        fp.close()
        fp = open(os.path.join(xml_dir, 'music-info-b.xml'), "wb")
        fp.write(xml.update_metadata(data))
        fp.close()
    else:
        print("Creating new XML...")
        # First, write out a metadata file, that can be copied into music-info.xml
        fp = open(os.path.join(xml_dir, 'music-info-b.xml'), 'wb')
        fp.write(xml.get_metadata())
        fp.close()

    # Now, write out the chart data - nov/green
    fp = open(os.path.join(music_dir, '01_{num:04d}_nov.xml'.format(num=args.id)), 'wb')
    fp.write(xml.get_notes('easy'))
    fp.close()

    # Now, write out the chart data - adv/yellow
    fp = open(os.path.join(music_dir, '01_{num:04d}_adv.xml'.format(num=args.id)), 'wb')
    fp.write(xml.get_notes('medium'))
    fp.close()

    # Now, write out the chart data - exh/red
    fp = open(os.path.join(music_dir, '01_{num:04d}_exh.xml'.format(num=args.id)), 'wb')
    fp.write(xml.get_notes('hard'))
    fp.close()

    # Should we even attempt inf?
    # fp = open(os.path.join(root, '01_{num:04d}_inf.xml'.format(num=args.id)), 'wb')
    # fp.write(xml.get_notes('infinite'))
    # fp.close()

    # Write out miscelaneous files
    fp = open(os.path.join(music_dir, '01_{num:04d}.def'.format(num=args.id)), 'wb')
    fp.write('#define 01_{num:04d}   0\n'.format(num=args.id).encode('ascii'))
    fp.close()
    fp = open(os.path.join(music_dir, '01_{num:04d}_prv.def'.format(num=args.id)), 'wb')
    fp.write('#define 01_{num:04d}_prv   0\n'.format(num=args.id).encode('ascii'))
    fp.close()

    # Now, if we have a jacket file, copy that

    jacket_b = "jacket.png"
    jacket_s = "jacketSmall.png"
    jacketvar = os.path.split(args.file)[0]
    if jacket_b is not None:
        print('Copying BIG jacket...')
        try:
            shutil.copyfile(jacketvar + '\\' + jacket_b,
                            jacket_b_dir + '\\' + 'jk_01_{num:04d}_1_b.png'.format(num=args.id))
        except IOError as e:
            logger.critical(f'{os.path.splitext(os.path.basename(args.file))[0]} - {e.strerror}: {jacket_b}')

    if jacket_s is not None:
        print('Copying SMALL jacket...')
        try:
            shutil.copyfile(jacketvar + '\\' + jacket_s,
                            jacket_s_dir + '\\' + 'jk_01_{num:04d}_1_s.png'.format(num=args.id))
        except IOError as e:
            logger.critical(f'{os.path.splitext(os.path.basename(args.file))[0]} - {e.strerror}: {jacket_s}')

    if os.path.exists(jacketvar + '\\' + 'jacket2.png'):
        print("jacket2 found")
        try:
            shutil.copyfile(jacketvar + '\\' + 'jacket2.png',
                            jacket_b_dir + '\\' + 'jk_01_{num:04d}_2_b.png'.format(num=args.id))
        except IOError as e:
            print('%s' % e.strerror + ': ' + 'jacket2.png')
        else:
            print("Copy OK")

    if os.path.exists(jacketvar + '\\' + 'jacket2small.png'):
        print("jacket2small found")
        try:
            shutil.copyfile(jacketvar + '\\' + 'jacket2small.png',
                            jacket_s_dir + '\\' + 'jk_01_{num:04d}_2_s.png'.format(num=args.id))
        except IOError as e:
            print('%s' % e.strerror + ': ' + 'jacket2small.png')
        else:
            print("Copy OK")

    if os.path.exists(jacketvar + '\\' + 'jacket3.png'):
        print("jacket3 found")
        try:
            shutil.copyfile(jacketvar + '\\' + 'jacket3.png',
                            jacket_b_dir + '\\' + 'jk_01_{num:04d}_3_b.png'.format(num=args.id))
        except IOError as e:
            print('%s' % e.strerror + ': ' + 'jacket3.png')
        else:
            print("Copy OK")

    if os.path.exists(jacketvar + '\\' + 'jacket3Small.png'):
        print("jacket3small found")
        try:
            shutil.copyfile(jacketvar + '\\' + 'jacket3small.png',
                            jacket_s_dir + '\\' + 'jk_01_{num:04d}_3_s.png'.format(num=args.id))
        except IOError as e:
            print('%s' % e.strerror + ': ' + 'jacket3small.png')
        else:
            print("Copy OK")

    # Now, if we have an audio file, convert that too

    musicvar = (os.path.split(args.file)[0])
    musicfile = (os.path.join(musicvar, chart.metadata.get('music')))
    # print(musicvar)
    # print(musicfile)
    if musicfile is not None:
        # Make sure we also provided a sample start/offset
        preview_start = chart.metadata.get('samplestart')

        if preview_start is None:
            exception_handler('Music file present but no sample start specified for preview!', args.file)
        sample_start = float(preview_start)
        sample_length = 10.0

        print('Converting audio...')
        adpcm = ADPCM(musicfile, sample_start, sample_length)
        twodx = TwoDX()
        twodx.set_name('01_{num:04d}'.format(num=args.id))
        twodx.write_file('01_{num:04d}_1.wav'.format(num=args.id), adpcm.get_full_data())

        fp = open(os.path.join(music_dir, '01_{num:04d}.2dx'.format(num=args.id)), 'wb')
        fp.write(twodx.get_new_data())
        fp.close()

        print('Converting preview...')

        twodx = TwoDX()
        twodx.set_name('01_{num:04d}_prv'.format(num=args.id))
        twodx.write_file('01_{num:04d}_prv_1.wav'.format(num=args.id), adpcm.get_preview_data())

        fp = open(os.path.join(music_dir, '01_{num:04d}_prv.2dx'.format(num=args.id)), 'wb')
        fp.write(twodx.get_new_data())
        fp.close()

    print('Done!\r\n')

    return 0


if __name__ == '__main__':
    sys.exit(main())