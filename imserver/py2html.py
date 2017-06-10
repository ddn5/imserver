#!/usr/bin/env python

# This is a trimmed down version of Marc-Andre Lemburg's py2html.py.
# The original code can be found at http://starship.python.net/~lemburg/.
#
# Borrow (or steal?) PyFontify.py from reportlab.lib.

import sys

from . import PyFontify

pattern="""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN">
<html>
<head>
<title>%(source)s</title>
<style>



cc{font-style: italic;font-family: "Times";color:gray}
ii,kk,ss{font-family: serif;}
ii{color:red}
kk{color:black;font-weight: bold;}
ss{color:green}
</style>
</head>
<body bgcolor=white>
<pre>
%(target)s
</pre>
</body>
</html>
"""

formats = { 'comment': "<cc>%s</cc>",
            'identifier': "<ii>%s</ii>",
            'keyword': "<kk>%s</kk>",
            'string': "<ss>%s</ss>" }
            
            
def escape_html(text):
        t = (('&','&amp;'), ('<','&lt;'), ('>','&gt;'))
        for x,y in t:
            text = y.join(text.split(x))
        return text

def py2html(source):
    f = open(source)
    text = f.read()
    f.close()
    tags = PyFontify.fontify(text)
    done = 0
    chunks = []
    for tag, start, end, sublist in tags:
        chunks.append(escape_html(text[done:start]))
        chunks.append(formats[tag] % escape_html(text[start:end]))
        done = end
    chunks.append(escape_html(text[done:]))

    dict = { 'source' : source, 'target' : ''.join(chunks) }
    return pattern % dict


if __name__ == '__main__':

    if len(sys.argv) == 1:
        print ("Usage: ./py2html.py files")
        print ("\tfiles is a list of Python source files.")
        sys.exit(1)

    for ff in sys.argv[1:]:
        html=py2html(ff)
        with open(ff + '.html', 'w') as f:
            f.write(html)
            f.close()
