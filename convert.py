import os, subprocess, glob

# Usage- Set the source_dir, ssc2museca path, optionally set the ID for batch conversion. 
# ID specified in the .ssc file will always take precedence.
# Converter creates a custom_charts folder in the directory the script was run, and
#  automatically creates and updates a music-info-b.xml. If you wish to create an isolated
#  xml, uncomment the new_xml_dir variable and switch the comment in the for loop below.


id = 227

SOURCE_DIR = "D:\\Museca\\to_convert\\"
SSC2MUSECA_PATH = "C:/Users/Me/AppData/Local/Programs/Python/Python37-32/Scripts/ssc2museca.py"
# NEW_XML_DIR="-x D:/Museca/music-info-b.xml"



def run(cmd):
    subprocess.run(cmd, shell=True)

if os.path.exists("jacket_errors.txt"):
  os.remove("jacket_errors.txt")


files = [f for f in glob.glob(SOURCE_DIR + "**/*.ssc", recursive=True)]


for f in files:
    print(f"==== CONVERTING {f} ===============")

    ### Uncomment this for isolated xml
    # run(f"python {SSC2MUSECA_PATH} \"{f}\" {NEW_XML_DIR} {id}")

    ### Use this for normal operation.
    run(f"python {SSC2MUSECA_PATH} \"{f}\" -id {id}")

    id += 1
