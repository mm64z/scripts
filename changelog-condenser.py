#!/usr/bin/python

def printHelp():
    print """
A helper to condense different Unreleased sections
If outputfile is not provided, will write to screen
Usage: changelog-condenser.py <changelog> <outputfile?>
changelog - filename of the README.md to read in
outputfile - (optional) write all changelog entries to this file
"""


# takes changelog filename
# returns dict of keys to lines as well as rest of file
def condenser(filename):
    changelog = {}
    unreleased = True
    restOfFile = []
    key = ''
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip('\n')
            if unreleased:
                if line == '':
                    continue
                if line[:3] == '###':
                    # change keys
                    key = line[3:].strip()
                elif line[:2] == '##':
                    # check if not unreleased
                    if 'unreleased' not in line.lower():
                        unreleased = False
                        restOfFile.append(line)
                    else:
                        key = 'Uncategorized'
                else:
                    if key in changelog:
                        changelog[key].append(line)
                    else:
                        changelog[key] = [line]
            else:
                restOfFile.append(line)
    return (changelog, restOfFile)

def printNewChangelog(changelog, restOfFile, fileHandle):

    
    output('## Unreleased', fileHandle)
    setOrder = ['Added', 'Changed', 'Fixed', 'Removed']

    # output some of the categories in a set order
    for key in setOrder:
        if key in changelog:
            output('### ' + key, fileHandle)
            for entry in changelog[key]:
                output(entry, fileHandle)
            output('', fileHandle)

    # output the rest of the categories
    for key in changelog:
        if key not in setOrder:
            output('### ' + key, fileHandle)
            for entry in changelog[key]:
                output(entry, fileHandle)
            output('', fileHandle)

    # output the rest of the file
    for line in restOfFile:
        output(line, fileHandle)

def output(line, fileHandle):
    if fileHandle is None:
        print(line)
    else:
        fileHandle.write(line + '\n')

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        printHelp()
        exit()
    (changelog, restOfFile) = condenser(sys.argv[1])
    if len(sys.argv) > 2:
        outputFile = sys.argv[2]
        with open(outputFile, 'w') as outputFileHandle:
            printNewChangelog(changelog, restOfFile, outputFileHandle)
    else:
        printNewChangelog(changelog, restOfFile, None)

                
