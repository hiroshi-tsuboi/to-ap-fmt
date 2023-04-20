import codecs
import sys
import json
import re

def aformat(line, rubyState, rubyChar, reProgram):
    mode = 0
    a = ""
    w = ""
    r = ""
    for c in line:
        if c in rubyState:
            n = rubyState[c]
            if n == 3:
                if mode == 2:
                    a += rubyChar[1]
                    a += w
                    a += rubyChar[2]
                    a += r
                    a += rubyChar[3]
                elif 0 < mode:
                    print("error in %s" % line)
                    return line
                else:
                    a += c
                w = ""
                r = ""
                mode = 0
                continue
            elif mode == 0:
                if 1 < n and len(w) == 0:
                    pass
                elif n == 1:
                    a += w
                    w = ""
            mode = n
        elif mode == 0:
            if reProgram.match(str(c)):
                a += w
                a += c
                w = ""
            else:
                w += c
        elif mode == 1:
            w += c
        elif mode == 2:
            r += c

    if 0 < len(r):
        print("error in %s" % line)
        return line

    result = a + w

    if result != line:
        #print("replace %s -> %s" % (line, result))
        pass

    return result


config = None

try:
    f = codecs.open("config.json", 'r', 'utf-8')
    config = json.load(f)
    f.close()
    #print(config)
except:
    print("failed to open config.json")
    sys.exit()

key = None
if "key" in config:
    key = config["key"][0]
else:
    sys.exit()

title = None
if "title" in config:
    title = config["title"][0]
else:
    sys.exit()

article = None
if "article" in config:
    article = config["article"][0]
else:
    sys.exit()

rubyState = {}
rubyChar = {}
if "ruby-char" in config:
    items = config["ruby-char"]
    index = 1
    for item in items:
        rubyState[item[0]] = index
        rubyChar[index] = item[1]
        index += 1

reProgram = None
if "re-pattern" in config:
    reProgram = re.compile(config["re-pattern"][0])

#

if len(sys.argv) < 2:
    sys.exit()

filename = sys.argv[1]

lines = []

try:
    f = codecs.open(filename, 'r', 'utf-8')
    mode = 0
    for line in f:
        if mode < 4:
            if 0 < mode and mode < 3:
                lines.append(line)
                mode += 1
            elif line[0] == key:
                if title in line:
                    mode = 1
                elif article in line:
                    mode = 4
        else:
            lines.append(aformat(line, rubyState, rubyChar, reProgram))

    f.close()

    #print(lines)
except:
    print("failed to open %s" % filename)
    sys.exit()

#

if len(sys.argv) < 3:
    sys.exit()

filename = sys.argv[2]

try:
    f = codecs.open(filename, 'w', 'utf-8')

    for line in lines:
        f.write(line)

    f.close()
except:
    print("failed to create %s" % filename)
    sys.exit()
