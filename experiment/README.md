# Discussion problem: date parsing

This program used to read notebook.md files, extract date information from them and write to yaml files.
It also has the ability to check whether there is a missing section and whether a student has missed any 
residential class.

# How to run the program

```
1. Run "cms sys command generate date_parsing" to generate a command ("date_parsing" is our command name).

2. Make sure all notebook*.md files are in "cloudmesh.date_parsing" directory which has just generated 
by the above command.

3. After replace the "date_parsing.py" with our script, run "pip install ." to install this command.

4. Run "cms" to enter the cloudmesh panel.

5. Run "date_parsing -g" or "date_parsing generate" command to get the results and yaml files.

For detail install steps see: https://cloudmesh.github.io/classes/lesson/prg/python-cmd5.html.
```

# Main functions usage description

```
convert_data(str): Processing the raw data read from notebook.md file.

extract_data(str): Get the data from each section (Assume data is between two "\n").

split_str(row, content): splite date and content information from a line of data.

check_sections(name, sections): check for missing sections.

check_attend(name, meetings): check for absence in meetings.

output_data(data, file): write data into yaml files with typical format.

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

The data in each yaml file has the following format. Take data_parsing_notebook2.md.yaml as an example.

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
