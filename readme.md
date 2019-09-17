# MÚSECA Chart Converter

August 2019 Updates:
- Implemented ID support - ID can be specified in the ``#SUBTITLE:123;`` field of the SSC file/SM editor. ID can still be specified as an argument, but it will always defer to the ID in the Subtitle field, if available.
- Automatic folder creation - optimized for drag-n-drop into the data_mods folder of IFS LayeredFS.
- Added jacket support - see jacket info section below.
- Improved preview audio conversion
- Modified general usage of ssc2museca.py - described below

This utility includes a chart converter that can convert a set of charts written in StepMania's .ssc file format and an audio file to a format recognized by MÚSECA. Additionally, it will generate metadata to copy-paste into the music database xml, or optionally update an xml file if provided. Usage is described below:

    python ssc2museca.py [-h (shows help message)] [-id ID] [-d DIRECTORY] [-x NEW_XML] FILE

In the above command, a chart for Novice (Green), Advanced (Yellow), and Exhaust (Red) will be parsed out of ``chart.ssc`` and metadata and a directory suitable for copying into the ``data_mods`` folder of IFS Layered FS will be created. By default, the converter will output the converted metadata, chart and audio files to a `custom_charts` folder in the current directory. To specify the output directory, use ``-d some/directory``. To tell the converter to create a new, isolated xml file containing just the metadata for one song, use ``-x somedir/music-info-b.xml``
If you wish to update the full music database, create the folder ``custom_charts/museca/xml`` and copy-paste the original music-info-b.xml. The converter will append all new entries. Otherwise, the converter will create and update an xml in that directory.
(The IFS xml merging function currently can't handle some japanese characters, so it is best to copy and update the original music-info-b.xml from the game files. IFS LayeredFS will redirect the game to use the xml in ``data_mods/custom_charts/museca/xml``, so long as it is named the same.)

## Installation
* First download python3 for windows. The installer will ask you if you want to add python to your path, say YES!
* Then download this project as a zip file. Extract the ssc2museca folder to a safe location and add it to your path. Google that if you don't know what it means.
* PLEASE read this readme very carefully, especially the bits about handling the XMLs and jackets.
* I also suggest adding Open Command Window Here to the folder right click context menu so you don't have to cd /d to your chart location every time. Tutorial on that here https://www.windowscentral.com/add-open-command-window-here-back-context-menu-windows-10
 

## Recommended Usage:

* Copy the chart folder you wish to convert from the stepmania-museca editor to a new location where all your conversions will be done. Something like Documents\Museca-Customs\to_convert\
* Make sure your audio is OGG format. Don't use WAV and don't use MP3. You can convert with Audacity. You should have an ssc file, an ogg audio file, and (optionally) two jackets in the folder. (see below on jacket requirements)
* Create the folder \custom_charts\museca\xml\ in your Museca-customs directory. Copy the original music-info-b.xml from the game files, and paste it here. 
* Copy the convert.bat file to your Museca-Customs folder and open it in a notepad editor. Update the source to the full path of your to_convert folder. Optionally set the ID, but it's always best to not use this and set the ID in the Subtitle field in the Stempania editor.
* Save and close convert.bat, and double click it to run it. Any chart folders in the to_convert folder should be converted and placed in the custom_charts folder. If you performed all these steps correctly, you should be able to copy the custom_charts folder into your game (it goes in contents\data_mods). If you don't have a data_mods folder, you will need IFS LayeredFS. See the Dependencies section below.


## About This Fork

This fork is designed to be used in conjunction with a fork of StepMania 5.2 that adds a new ``museca-single`` game mode This mode defines a 16-lane single player mode, rather than a 16-lane double play mode like the ones offered by ``bm`` and ``techno``. A noteskin is provided that helps better visualize the spin lanes on top of the normal lanes and should result in quicker and easier chart creation.

Windows binaries for this StepMania 5.2 fork are available as a .zip or .exe installer:
- **.zip**: https://ortlin.de/i/msc/StepMania-5.2-git-edbed30b62-win32.zip
- **.exe installer**: https://ortlin.de/i/msc/StepMania-5.2-git-edbed30b62-win32.exe

## Dependencies

The following external dependencies are required to run this conversion software:
- IFS LayeredFS - Instructions inlcuded in the download. https://mon.im/bemanipatcher/secret/ifs_layeredfs_latest.zip
- ffmpeg - (now included) Used to convert various audio formats to the ADPCM format required by MÚSECA.
- sox - (now included) Used to create preview clips.
- python3 - The script assumes python 3.5 or better to operate.
- MÚSECA cabinet - Obviously you'll need to have access to one of these to test and play songs.

## Jackets

The converter now automates the process of copy-pasting jackets and placing them in the correct folders witht the correct names. The parser will look for ``jacket.png and jacketSmall.png`` at minimum. If they aren't found, an error will be logged to ``jacket_errors.txt``.
Support for individual-difficulty jackets is also available. The converter will look for ``jacket2.png, jacket2small.png, jacket3.png, jacket3small.png``, but it will not show an error if they are not found.

Jackets have the following image size requirements:

    jacket.png - 768x768px
    jacketSmall.png - 202x202px

## Caveats
Note that the game supports time signatures other than 4/4 but the converter doesn't make any attempt to handle this. It also DOES technically support BPM changes, but no verification was done around this feature. The converter will probably let you put down illegal sequences, such as a small/large spinny boi on top of a regular note. The game engine may actually handle this, but there is no guarantee!

# Chart Format

## Header Tags

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
