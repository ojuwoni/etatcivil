import re

with open('test_dep.csv', encoding = "ISO-8859-1") as f:
    for line in f:
        if not line.isspace():
            #line = line.strip()
            line = line.split()
            if len(line) > 1:
                if re.match(r"DEPT", line[0]):
                    word = line[1:]
                    print("",*word)
                elif re.match(r"COMMUNE", line[0]):
                    word = line[1:]
                    print("\t",*word)
                elif re.match(r"ARROND", line[0]):
                    word = line[1:]
                    print("\t\t",*word)
                else:
                    print("\t\t\t",*line)
            else:
                print("\t\t\t",*line)

