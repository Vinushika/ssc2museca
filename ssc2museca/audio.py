from exception_handler import exception_handler
import os, glob
import struct
import subprocess
import tempfile
from typing import Dict, List, Tuple, Optional


sox_location = [f for f in glob.glob("**/sox.exe", recursive=True)]
if not sox_location:
    exception_handler('Could not locate SOX.exe')

ffmpeg_location = [f for f in glob.glob("**/ffmpeg.exe", recursive=True)]
if not ffmpeg_location:
    exception_handler('Could not locate ffmpeg.exe')

class TwoDX:
    def __init__(self, data: Optional[bytes] = None) -> None:
        self.__name = None  # type: Optional[str]
        self.__files = {}  # type: Dict[str, bytes]
        if data is not None:
            self.__parse_file(data)

    def __parse_file(self, data: bytes) -> None:
        # Parse file header
        (name, headerSize, numfiles) = struct.unpack('<16sII', data[0:24])
        self.__name = name.split(b'\x00')[0].decode('ascii')

        if headerSize != (72 + (4 * numfiles)):
            exception_handler('Unrecognized 2dx file header!')

        fileoffsets = struct.unpack('<' + ''.join(['I' for _ in range(numfiles)]), data[72:(72 + (4 * numfiles))])
        fileno = 1

        for offset in fileoffsets:
            (magic, headerSize, wavSize, _, track, _, attenuation, loop) = struct.unpack(
                '<4sIIhhhhi',
                data[offset:(offset+24)],
            )

            if magic != b'2DX9':
                exception_handler('Unrecognized entry in file!')
            if headerSize != 24:
                exception_handler('Unrecognized subheader in file!')

            wavOffset = offset + headerSize
            wavData = data[wavOffset:(wavOffset + wavSize)]

            self.__files['{}_{}.wav'.format(self.__name, fileno)] = wavData
            fileno = fileno + 1

    @property
    def name(self) -> str:
        return self.__name

    def set_name(self, name: str) -> None:
        if len(name) <= 16:
            self.__name = name
        else:
            exception_handler('Name of archive too long!')

    @property
    def filenames(self) -> List[str]:
        return [f for f in self.__files]

    def read_file(self, filename: str) -> bytes:
        return self.__files[filename]

    def write_file(self, filename: str, data: bytes) -> None:
        self.__files[filename] = data

    def get_new_data(self) -> bytes:
        if not self.__files:
            exception_handler('No files to write!')
        if not self.__name:
            exception_handler('2dx archive name not set!')

        name = self.__name.encode('ascii')
        while len(name) < 16:
            name = name + b'\x00'
        filedata = [self.__files[x] for x in self.__files]

        # Header length is also the base offset for the first file
        baseoffset = 72 + (4 * len(filedata))
        data = [struct.pack('<16sII', name, baseoffset, len(filedata)) + (b'\x00' * 48)]

        # Calculate offset this will go to
        for bytedata in filedata:
            # Add where this file will go, then calculate the length
            data.append(struct.pack('<I', baseoffset))
            baseoffset = baseoffset + 24 + len(bytedata)

        # Now output the headers and files
        for bytedata in filedata:
            data.append(struct.pack(
                '<4sIIhhhhi',
                b'2DX9',
                24,
                len(bytedata),
                0x3231,
                -1,
                64,
                1,
                0,
            ))
            data.append(bytedata)

        return b''.join(data)


class ADPCM:

    FADE_LENGTH = 1

    def __init__(self, filename: str, preview: str, preview_offset: float, preview_length: float) -> None:
        self.__filename = filename
        self.__preview_offset = preview_offset
        self.__preview_length = preview_length
        self.__full_data = None
        self.__preview_data = None
        if preview:
            self.__preview = preview
        else:
            self.__preview = filename

    def __check_file(self) -> None:
        if not os.path.exists(self.__filename):
            exception_handler('File \'{}\' does not exist!'.format(self.__filename))

    def __conv_file(self) -> None:
        self.__check_file()
        if self.__full_data is not None:
            exception_handler('Logic error, re-converting audio file!')

        # We must create a temporary file, use ffmpeg to convert the file
        # to MS-ADPCM and then load those bytes in.
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp:
            subprocess.call([
                ffmpeg_location[0],
                '-y',
                '-hide_banner',
                '-nostats',
                '-loglevel',
                'error',
                '-i',
                self.__filename,
                '-acodec',
                'adpcm_ms',
                '-ar',
                '44100',
                temp.name,
            ])

            temp.seek(0)
            self.__full_data = temp.read()
        os.remove(temp.name)

    def __conv_preview(self) -> None:
        self.__check_file()
        if self.__preview_data is not None:
            exception_handler('Logic error, re-converting audio file!')

        # We have to convert to .wav because SOX sometimes doesn't have
        # codecs for other formats, so we support everything ffmpeg does.
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as intemp:
            subprocess.call([
                ffmpeg_location[0],
                '-y',
                '-hide_banner',
                '-nostats',
                '-loglevel',
                'error',
                '-i',
                self.__preview,
                intemp.name,
            ])

            # Now, get sox to cut this up into a new file.
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as cuttemp:
                subprocess.call([
                    sox_location[0],
                    '-V1',
                    intemp.name,
                    cuttemp.name,
                    'trim',
                    str(self.__preview_offset),
                    '10.0',
                    'fade',
                    't',
                    '0.0',
                    '10.0',
                    str(self.FADE_LENGTH),
                ])

                # Now, do the final conversion to ADPCM and load the data.
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as outtemp:
                    subprocess.call([
                        ffmpeg_location[0],
                        '-y',
                        '-hide_banner',
                        '-nostats',
                        '-loglevel',
                        'error',
                        '-i',
                        cuttemp.name,
                        '-acodec',
                        'adpcm_ms',
                        '-ar',
                        '44100',
                        outtemp.name,
                    ])

                    outtemp.seek(0)
                    self.__preview_data = outtemp.read()
                os.remove(outtemp.name)
            os.remove(cuttemp.name)
        os.remove(intemp.name)

    def get_full_data(self) -> bytes:
        if self.__full_data is None:
            self.__conv_file()

        return self.__full_data

    def get_preview_data(self) -> bytes:
        if self.__preview_data is None:
            self.__conv_preview()

        return self.__preview_data
