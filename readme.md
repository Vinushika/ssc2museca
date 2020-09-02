# MÚSECA Chart Converter

September 2020 Updates:
- Added two programs to fully automate the process of transferring your chart updates to your cab! No need to f*ck around with thumb drives or ftp anymore.
- Fixed some more bugs in the converter scripts.
- Converter can now recognize a manually entered ``RELEASEDATE`` tag in the ssc file. See the Chart Format section for details. 

June 2020 Updates:
- Local caching
    - When you run the converter for the first time, it will build a src\cache.json file to keep track of any changes that occur in src\custom_charts.
    - If a song folder is removed from src\custom_charts, the converter will remove the respective assets from your converted custom_charts folder.
    - A change to any file in a folder in src\custom_charts will cause that song and all of it's assets to be re-converted.
- Introduced a progress bar
- Moved most of the batch file contents over to ssc2museca.py
- More verification checks (jacket sizes, music files, etc)

April 2020 Updates:  
- Overhauled the converter, added better logging, ssc2museca executable, ssc verification.
- Two batch files provided to build all charts or add one to the current build.
- Omnimix songs included in ``defaults``
- If you want to use a separate preview audio file, name it in the Preview field of the sm editor. Otherwise, the main audio file will be used.

August 2019 Updates:
- Implemented ID support - ID can be specified in the ``#SUBTITLE:123;`` field of the SSC file/SM editor. ID can still be specified as an argument, but it will always defer to the ID in the Subtitle field, if available.
- Automatic folder creation - optimized for drag-n-drop into the data_mods folder of IFS LayeredFS.
- Added jacket support - see jacket info section below.
- Improved preview audio conversion
- Modified general usage of ssc2museca.py - described below

This utility includes a chart converter that can convert a set of charts written in StepMania's .ssc file format and an audio file to a format recognized by MÚSECA. Additionally, it will generate metadata to copy-paste into the music database xml, or optionally update an xml file if provided. Usage is described below:

    usage: ssc2museca.exe [-h] [-f FILE] [-id ID] [-d DIRECTORY] [-x NEW_XML] [-v] [--build-all] [-y]

    A utility to convert 16-lane StepMania charts (.ssc format) to Museca format.

    optional arguments:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  .ssc file to convert to Museca format.
      -id ID                ID to assign this song.
      -d DIRECTORY, --directory DIRECTORY
                            Directory to place files in. Defaults to current
                            directory.
      -x NEW_XML, --new-xml NEW_XML
                            Location of an isolated music-info-b.xml to create. If
                            not specified, a new one will be created or updated
                            automatically in the xml directory.
      -v, --verify          Checks the ssc files for errors without converting or
                            writing files.
      --build-all           Builds the modpack.
      -y, --yes             Supress prompts.

## Installation
This fork is designed to be used in conjunction with a fork of StepMania 5.2 that adds a new ``museca-single`` game mode This mode defines a 16-lane single player mode, rather than a 16-lane double play mode like the ones offered by ``bm`` and ``techno``. A noteskin is provided that helps better visualize the spin lanes on top of the normal lanes and should result in quicker and easier chart creation.  
A compiled Windows release is available here:
- **.exe installer**: https://github.com/camprevail/ssc2museca/releases/download/V1.1/StepMania-5.2-git-d2b5a9a1b1-win32_INSTALLER.exe
* VisualC++2019 Redist, which may already be installed on your pc. You should also install the x64 version on your cab if you want to use the personal updater programs.
* PLEASE read this readme very carefully, especially the bits about handling the XMLs and jackets.

## Recommended Usage:

* Copy the chart folders you wish to convert from the stepmania-museca editor to ``src\custom_charts``
* You should have an ssc file, an audio file, and two jackets in the folder. (see below on jacket requirements)
* Run the ``build_all.bat`` batch file to start the conversion process. Once complete, you may copy ``custom_charts`` to the ``contents\data_mods`` folder in your game, OR...
* Use the updater programs to transfer the charts to your cab: (64bit VC++2019 Redist must be installed on your cab):
    - Start the ``updater_pc_server`` program, Take note of the IP address and Port it prints out. This can run in the background and doesn't 
    need to be restarted when you run the ``build_all.bat`` script to update your charts.

    - Copy the ``updater_cab_client`` program to the ``contents`` folder on your cab. Edit your gamestart/spicestart.bat: on a newline
    above ``launcher`` or ``spice``, add ``call updater_cab_client 192.168.xxx.xxx:8000``. Use the ip and port from the updater_pc_server.
    
    - Restart your cab and enjoy automatic updates from your personal server! Note that updates can only take effect by restarting the game. 
    This is a limitation of Museca, not the updater program. 
  
* IFS LayeredFS is now built directly into spicetools, and loads the data_mods folder automatically.

## Jackets

The converter automates the process of copy-pasting jackets and placing them in the correct folders witht the correct names. The parser will look for ``jacket.png and jacketSmall.png`` at minimum. 
If they aren't found, an error will be thrown and the converter will not convert the charts.  
Support for individual-difficulty jackets is also available. The converter will look for ``jacket2.png, jacket2small.png, jacket3.png, jacket3small.png``, but it will not show an error if they are not found.

Jackets have the following image size requirements:

    jacket.png - 768x768px
    jacketSmall.png - 202x202px

## Caveats
Note that the game supports time signatures other than 4/4 but the converter doesn't make any attempt to handle this. It also DOES technically support BPM changes, but no verification was done around this feature. The converter will probably let you put down illegal sequences, such as a small/large spinny boi on top of a regular note. The game engine may actually handle this, but there is no guarantee!

# Chart Format

## Header Tags

* ``RELEASEDATE`` - You can optionally add this header to the ssc file manually, only recognized by the ssc2museca converter.
* ``TITLE`` - The title of the song as it shows in-game. This can include all sorts of characters, including english, kana or kanji. Various accented latin characters may not render correctly due to particulars about how the game handles certain character sets, though.
* ``SUBTITLE`` - The chart ID that will be read by the converter. Museca's final music database update ended at 226, so you should use 227 or higher.
* ``TITLETRANSLIT`` - The title of the song as sounded out, written in half-width katakana (dakuten allowed). This is used for title sort. There are converters which take any english and give you the katakana, and converters that go from full-width to half-width katakana. Use them!
* ``ARTIST`` - The artist of the song as it shows in-game. This can include all sorts of characters, including english, kana or kanji. Various accented latin characters may not render correctly due to particulars about how the game handles certain character sets, though.
* ``ARTISTTRANSLIT`` - The artist of the song as sounded out, written in half-width katakana (dakuten allowed). This is used for artist sort. There are converters which take any english and give you the katakana, and converters that go from full-width to half-width katakana. Use them!
* ``SUBTITLETRANSLIT`` - Can (and should) be omitted. This maps to the ``ascii`` element in music-info.xml, and defaults to "``dummy``" if no value is provided.
* ``MUSIC`` - Path to an audio file to be converted. Use any format supported by ffmpeg.
* ``SAMPLESTART`` - Number of seconds into the above music to start the preview. The converter will auto-fade in and convert to a preview song.
* ``SAMPLELENGTH`` - Number of seconds after the start to continue playing the preview before cutting off. The game tends to use 10-second previews, so it's wise to stick with that.
* ``OFFSET`` - Number of seconds to offset the chart relative to the start of the music. Use this to sync the game to the chart.
* ``BPMS`` - What BPM the chart is at. For help on this field, please refer to [the .ssc format documentation](https://github.com/stepmania/stepmania/wiki/ssc). It is not a simple number, but instead a comma-separated list of beat numbers paired to a BPM that the song uses at that point.
* ``LABELS`` - These are used for declaring the beginnings and ends of Grafica sections. Similar to ``BPMS``, this is a comma-separated list of values ``beat_num=LABELTEXT``. The converter expects/requires 6 labels in this order:
    * ``GRAFICA_1_START``
    * ``GRAFICA_1_END``
    * ``GRAFICA_2_START``
    * ``GRAFICA_2_END``
    * ``GRAFICA_3_START``
    * ``GRAFICA_3_END``
* ``LICENSE`` - The license owner of the song. Can be left blank.
* ``CREDIT`` - The illustration artist. Can be left blank.

### Chart Tags
Each chart begins with a `#NOTEDATA:;` line. The following tags after `#NOTEDATA:;` are used by the converter:
- ``#STEPSTYPE`` - The only supported type is ``museca-single``.
- ``#CREDIT`` - The author of the chart, AKA your handle. Not to be confused with the ``#CREDIT`` one level up in ``#NOTESDATA:;``. Note that this doesn't actually get displayed anywhere, and usually tends to be "``dummy``".
- ``#DIFFICULTY`` - One of the following three supported difficulties: ``Easy``, ``Medium``, or ``Hard``.
- ``#METER`` - The difficulty rating, as a value from 1-15 inclusive.
- ``#NOTES`` - The actual note data, which will continue to be parsed until a line with only a  ``;`` on it is encountered.


## Lane Layout, Charting, and Design Notes

There is 1 pedal lane, and then 3 channels of 5 lanes each.

    CH0 @ sm[0]:      pedal (note that in museca, this lane is actually on the far right at ``msc[5]``)
    CH1 @ sm[1..5]:   taps and holds
    CH2 @ sm[6..10]:  left spins
    CH3 @ sm[11..15]: right spins

### Mapping Examples
- **Tap** in CH1, ``sm[1]``
    - **Tap** in ``msc[1]``
- **Hold** in CH1, ``sm[1]``
    - **Hold** in ``msc[1]``
- **Tap** in CH2, ``sm[6]``
    - **Left spin** in ``msc[1]``
- **Tap** in CH3, ``sm[11]``
    - **Right spin** in ``msc[1]``
- **Tap** in CH2 and CH3, ``sm[6] and sm[11]`` 
    - **Non-directional spin** in ``msc[1]``
- **Hold *start*** in CH2 or CH3, ``sm[6] or sm[11]``
    - **Start storm object event** in ``msc[1]``
- **Mine** in CH1 or CH2 or CH3, ``sm[1] or sm[6] or sm[11]``
    - **End storm object event** in ``msc[1]``

### Why 3 Channels?
- Hold ends in StepMania don't have multiple end types, so we can't overlap a spinner of any kind onto a hold release.
- More taps means more claps, which is always nice.
    - An original 6-lane draft made use of all 4 note types: Tap, Mine (left spin), Fake (right spin), Lift (non-dir spin)
    - But there were still hold ends and storm objects to worry about, thus...

### Storm Objects: Why Hold Start, Why Mines?
- Storm objects are "like" holds in that they have a start and end...
    - ...but they do not claim exclusive control of the lane in MÚSECA.
    - While a storm object is out, that lane could have taps and spins going on!
- To still retain the assist tick sound while distinguishing these from normal spins, we make a hold, rather than a lift/fake.
    - The timing of the hold end does not matter, the converter should ignore hold end events in CH2 or CH3.
- The mine will indicate the storm is over, but it can go in any 5-lane channel, even CH1.
    - This way, a storm object can end at the same time a spin of any kind occurs in that lane. (mine goes in CH1, taps go in CH2+CH3)
- There's still one imperfect situation...

### Case(s) Not Covered
- Storm end event in ``msc[1]`` at the same time as a non-directional spin acting as the "tail" of a hold in ``msc[1]``. (or acting as the "head", but that's evil)
    - Where does the mine go? CH1 is occupied by a hold, CH2 and CH3 are occupied by taps that will become a non-directional spin.
    - Either shift something (preferably the mine/stormend) by 1/192nd...
    - ...or maybe add a Label that starts with  "``STORM_END_LANE_n_``" at this point, which will tell the converter to create a storm end event in lane ``n``. (more text is accepted after the trailing ``_`` to allow for multiples of these events to exist, since label names cannot be repeated)

### TODO
- Chart-specific ``#BPMS`` and ``#LABELS``.
    - This can be accomplished by using Step Timing mode instead of Song Timing mode in SM5.
    - Right now, using Step Timing at all will break the converter.
    - The parser will need to ignore many more sections while within ``#NOTEDATA``:
        - #TIMESIGNATURESEGMENT
        - #TICKCOUNTS
        - #COMBOS
        - #SPEEDS
        - #SCROLLS
    - Additionally, the parser will need to account for how multi-value lines are handled in ``#NOTEDATA`` .
        - In ``#NOTEDATA``, each (potentially) multi-value tag gets a linebreak after each value.
        - This means subsequent values start with ``\n,`` instead of ``,\n`` as it is elsewhere
        - This also means the tag-ending ``;`` always appears on its own line, which differs from how the main song header keeps the final semi-colon on the same line for multi-value tags.
    - Basically, this means reworking the parser quite a fair bit.
- Allow storm end events to also be pulled in from ``#LABELS``, which will remove a limitation in this chart format
- Adjust output file locations to put chart/audio data in one folder, and music-info.xml in another folder?

## Example chart

Below is an example chart, which includes a few measures showcasing a handful of events:

    #VERSION:0.83;
    #TITLE:Test Song;
    #SUBTITLE: 123; (CHART ID GOES HERE)
    #ARTIST:Test;
    #TITLETRANSLIT:ﾃｽﾄｿﾝｸﾞｸ;
    #ARTISTTRANSLIT:ﾃｽﾄ;
    #CREDIT:ILLUSTRATOR;
    #BANNER:banner.jpg;
    #BACKGROUND:bg.jpg;
    #DISCIMAGE:;
    #MUSIC:test.wav;
    #OFFSET:0.000000;
    #SAMPLESTART:72.680000;
    #SAMPLELENGTH:10.000000;
    #SELECTABLE:YES;
    #BPMS:0.000=170.000;
    #TIMESIGNATURES:0.000=4=4;
    #TICKCOUNTS:0.000=4;
    #COMBOS:0.000=1;
    #SPEEDS:0.000=1.000=0.000=0;
    #SCROLLS:0.000=1.000;
    #LABELS:0.000=Song Start,
    72.000=GRAFICA_1_START,
    104.000=GRAFICA_1_END,
    208.000=GRAFICA_2_START,
    271.000=GRAFICA_2_END,
    272.000=GRAFICA_3_START,
    316.000=GRAFICA_3_END;
    #BGCHANGES:0.000=-songbackground-=1.000=0=0=0=StretchNoLoop====,
    99999=-nosongbg-=1.000=0=0=0 // don't automatically add -songbackground-
    ;


    //---------------museca-single - ----------------
    #NOTEDATA:;
    #STEPSTYPE:museca-single;
    #DIFFICULTY:Hard;
    #METER:15;
    #RADARVALUES:0.424903,1.104567,0.186425,0.194899,0.419456,351.000000,319.000000,22.000000,23.000000,6.000000,12.000000,0.000000,0.000000,0.000000,0.424903,1.104567,0.186425,0.194899,0.419456,351.000000,319.000000,22.000000,23.000000,6.000000,12.000000,0.000000,0.000000,0.000000;
    #CREDIT:K;
    #NOTES:
    // measure 0
    0000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    ,  // measure 1
    2000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    0000000010000200
    0000000000000300
    0000000000000000
    0000000000000000
    0000000100000010
    0000000000000000
    0000000000000000
    0000000000000000
    ,  // measure 2
    3100000000000M00
    0001000000000000
    0000010000000000
    0000100000000000
    0010000000000000
    0000100000000000
    0000010000000000
    0001000000000000
    0100000000000000
    0010000000000000
    0000100000000000
    0010000000000000
    0100000000000000
    0001000000000000
    0000010000000000
    0000100000000000
    ,  // measure 3
    0010000000000000
    0100000000000000
    0001000000000000
    0000010000000000
    0000100000000000
    0010000000000000
    0000100000000000
    0000010000000000
    0001000000000000
    0100000000000000
    0010000000000000
    0000100000000000
    0010000000000000
    0100000000000000
    0001000000000000
    0000010000000000
    ,  // measure 4
    0001000000000000
    0010000000000000
    0000100000000000
    0100000000000000
    0000010000000000
    0100000000000000
    0000100000000000
    0010000000000000
    0001000000000000
    0000010000000000
    0100000000000000
    0010000000000000
    0000100000000000
    0000010000000000
    0001000000000000
    0010000000000000
    ,  // measure 5
    0100000000000000
    0010000000000000
    0001000000000000
    0000100000000000
    0000010000000000
    0010000000000000
    0000100000000000
    0100000000000000
    0001000000000000
    0000100000000000
    0000010000000000
    0000100000000000
    0001000000000000
    0010000000000000
    0000010000000000
    0001000000000000

    [--snip--]

    ,  // measure 77 (this is 2 storm objects layered on top of 2 hold starts, don't do this!)
    2200022000110002
    3000003000000003
    0000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    ,  // measure 78
    0000000000000000
    2000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    0000000000000000
    ,  // measure 79
    3300031000MM0001
    0000000000000000
    0000000000000000
    0000000000000000
    ;
