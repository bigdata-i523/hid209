# Discussion problem: date parsing

This program used to read notebook.md files, extract date information from them and write to yaml files.
It also has the ability to check whether there is a missing section and whether a student has missed any residential class.

# How to run the program

```
Make sure that all notebook.md files are in the same directory with this script, 
then run "python date_parsing.py" command to generate yaml files and get some useful information.
```

# Main functions usage description

```
convert_data(str): Processing the raw data read from notebook.md file in order to extract information easily.

extract_data(str): Get the data from each section (Assume data is between two "\n").

split_str(row, content): splite date and content information from a line of data.

check_sections(name, sections): check for missing sections.

check_attend(name, meetings): check for absence.

output_data: write data into yaml files.

```

# Test results

```
Test files: notebook1.md, notebook2.md.

Output results:
notebook1.md

['170825', '170901', '170908']
notebook1.md misses following sections:
Writing
notebook1.md misses following meetings:
170915
170922

notebook2.md

['170825', '170901', '170908', '170915', '170922']
notebook2.md does not miss any section.
notebook2.md does not miss any meeting.

Explanation: this script shows the input file name, output date from a sample section (use "Meetings"), 
check sections and attendance. In this sample, we could find that notebook1.md has missed the "Writing" 
section and absence meetings at "09/15/17" and "09/22/17".
```

# Data in yaml files

The data in each yaml file has the following format. Take notebook2.md as an example.

```
Logistic:
  Content: [Read the entire class overview section2222, Read the entire class overview
      section]
  Date: ['170821', '170821']
Meetings:
  Content: [Attended class meeting for residential students, Attended class meeting
      for residential students, Attended class meeting for residential students, Attended
      class meeting for residential students, Attended class meeting for residential
      students]
  Date: ['170825', '170901', '170908', '170915', '170922']
Practice:
  Content: [Bought Raspberry PI, Enabled Python 2 and 3 via pyenv on OSX]
  Date: ['170824', '170825']
Theory:
  Content: [Read and watched all videos in the Theory Introduction section, Read and
      watched all videos in the Theory Introduction section]
  Date: ['170822170823', '170824170826']
Writing:
  Content: [Installed and Learned aquamacs, Installed and Learned jabref]
  Date: ['170826', '000117']

We have splited a whole event into two parts: event date and detail content.
```
