############################################################################
# BACK END
############################################################################
import zipfile
import os
import tempfile
import re
import html 
import numpy as np

# Structure of enviroment is
# \begin{type}{name} description/content \end{type} 
#  ...other content like images or text... 
# \begin{type2} description/content \end{type2}
# for example type1 defintion, type2 example, then example with be added to corrsponding definition card.

# Used to extract content inside enviroment \begin{definition} ...this... \end{definition}
pattern_satz = r"\\begin\{satz\}(.*?)\\end\{satz\}"
pattern_lemma = r"\\begin\{lemma\}(.*?)\\end\{lemma\}"
pattern_proposition = r"\\begin\{proposition\}(.*?)\\end\{proposition\}"
pattern_folgerung = r"\\begin\{folgerung\}(.*?)\\end\{folgerung\}"
pattern_definition = r"\\begin\{definition\}(.*?)\\end\{definition\}"

# change \{\} into \[\] if you have square brackets, these are used to extract the content of the name field \begin{defitnition}{ this } ...content... \end{definition}
pattern_front =  r"\{(.*?)\}" 
pattern_back = r"\{(?:.*?)\}\s*(.+)"
MATHS = []

#------------ EXTRACTING TEXT FROM INPUT ----------
# Given path to zipfile return temporary folder path containing unzipped files.Uses a temporary directory which is automatically deleted afterwards.

def auto_unzip(user_input):
    print(f"Starting auto unzipping {user_input}...")

    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    print(f"Created temporary directory {temp_dir}...")

    # Extract ZIP contents
    with zipfile.ZipFile(user_input, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    print(f"Unzipped contents into {temp_dir}...")

    return temp_dir  # Return the temporary directory path

# given folder path return list of file paths to LaTeX files
def find_tex_files(folder_path):
    print(f"Searching for LaTeX files in {folder_path}...")
    tex_files = []
    for root, dirs, files in os.walk(folder_path):
        if "__MACOSX" in root:
            continue #skip mac os metadata folder and files 
        for file in files:
            if file.endswith('.tex') and (not file.startswith("._")):
                tex_files.append(os.path.join(root, file))
    return tex_files

# given path to LaTeX file return content of LaTeX file as a text string
def get_content(path):
    print(f"Opening {path}...")
    input = open(path)
    text = input.read()
    input.close()
    return text

#------------PROCESSING----------

def find_defi_beispiel_maths(text):
    # Match: \begin{definition}{optional name}... \end{definition} ... \begin{beispiel}... \end{beispiel}
    pattern = r"\\begin\{definition\}(?:\{(.*?)\})?\s*(.*?)\\end\{definition\}\s*\\begin\{beispiel\}\s*(.*?)\\end\{beispiel\}"

    matches = re.findall(pattern, text, re.DOTALL)
    
    for match in matches:
        name = match[0].strip() if match[0] else None
        definition_content = match[1].strip()
        example = match[2].strip().replace("\n", "")

        if re.search(r'[a-mo-zA-Z]', definition_content):
            print("Text found between definitions and example...")
        else:
            print("Text not between definitions and example...")

        if name:
            for i, maths in enumerate(MATHS):
                if maths.get("name") == name:
                    maths["example"] = example
                    print(example, name)
                    
def find_matches(type,type_str, text):
    matches = re.findall(type, text, re.DOTALL)
    for match in matches:
        maths = {}
        name = re.search(pattern_front, match)
        main = re.search(pattern_back, match, re.DOTALL) 
        if name and main:
            name = name.group(1).strip() 
            main = main.group(1).strip().replace("\n", "") 
            if "todo" in name or "todo" in main:
                print(f"skipping {name} because still todo...")
            else:
                maths["name"] = name
                maths["main"] = main
                maths["example"] ="0"
                maths["proof"] ="0"
                maths["type"] = type_str
                MATHS.append(maths)
        else: 
            print("front not found or main not found\n")

def process(text):
    print("Processing...")
    find_matches(pattern_definition, "definition", text)
    find_matches(pattern_satz, "satz", text)
    find_defi_beispiel_maths(text)

#------------ WRITING ----------
def add_html_section(output, section_name, content):
    output.write(f'<span class="medium"><br><b>{section_name}</b><br>[latex]')
    output.write(content)
    output.write('[/latex]</span>')

def open_html_title(output, title_name, class_name):
    output.write(f'<div class="{class_name}">')# open front
    output.write('<span class="medium"><br><hr>') 
    output.write('<p style="font-size: 18px;"><b>')
    output.write(title_name)
    output.write('</b></p><hr></a></span>')

def write_html_maths(output, maths):
    str_exam = "Example"
    str_proo = "Proof"
    safe_name = html.escape(maths.get("name", ""))
    safe_main = html.escape(maths.get("main", ""))
    safe_exam = html.escape(maths.get("example", ""))
    safe_proo = html.escape(maths.get("proof", ""))
    open_html_title(output, safe_name, 'front') # front
    output.write('</div>') # separate
    output.write('\t')
    output.write('<div class="back">')# open front
    #open_html_title(output, safe_name, 'back') # back
    if safe_main:
        add_html_section(output, maths["type"], safe_main)
    if safe_exam:
        add_html_section(output, str_exam, safe_exam)
    if safe_proo:
        add_html_section(output, str_proo, safe_proo)
    output.write('</div>') 

def write_html_maths_all():
    output = open("output_maths.html","w")
    output.write("#separator:tab\n")
    output.write("#html:true\n")
    output.write("#notetype:super math\n")

    # write maths
    for math in MATHS:
        if math["name"] != "todo":
            write_html_maths(output,math)
            output.write("\n")

    output.close()
    print("Done.")

    output = open("output_maths.txt","w")
    output.write("#separator:tab\n")
    output.write("#html:true\n")
    output.write("#notetype:super math\n")

    # write maths
    for math in MATHS:
        if "todo" not in math["name"] and "todo" not in math["main"]:
            if math["name"] != "0" and math["main"] != "0" and math["main"] != "":
                write_html_maths(output,math)
                output.write("\n")

    output.close()
    print("Done.")


def save_as_array():
    np.save('array_maths.npy', MATHS)
