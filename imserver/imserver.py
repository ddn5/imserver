import bottle
from os.path import *
import markdown
import codecs
from . import py2html

app = bottle.Bottle()

template = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html><title>Directory listing for {{path}}</title><style>
img{width:100%;}a{font-family: serif;}
div {display: inline-block;width:475px;padding:0 -8 px;border:1px gray solid}
h3{    position: fixed;    top: -4px;}
h3 a {
    text-decoration: initial;
    color: black;
    margin: 0 -7px 0 0;
    font-family: sans-serif;
    box-shadow: 0px 0px 4px 0px #9E9E9E;
    padding: 2px 14px;
    border-radius: 0 16px 0px 0;
    background-color: #f2ff72;
}
h3 a:nth-child(3n+2) {
    background-color: #ffef65;
}
h3 a:nth-child(3n+1) {
    background-color: #cbefff;
}
</style>
<body><h3>
<a href="/">ROOT</a>
<% p='/'
 for i in path.split("/"):
 if i:
 p+=i+'/' 
 %>
<a href="{{p}}">{{i}}</a>
% end 
% end
</h3>
<br><br>
% I = 0
% for f in sorted(list,reverse=True):
% n,ext = splitext(f)
% bn = basename(n)
% fp = join(path,f)
% if isdir(fp):
<pre>[DIR] <a href="/{{fp}}">{{bn}}/</a></b></pre>
% continue
% end
% if ext and ext.lower() in '.png,.bmp,.jpg,.jpeg,.bmp':
<div>[IMG]<a href="/{{fp}}">{{bn}}</a>
% I += 1
% if I<200:
<img src="/{{fp}}">
% end
</div>
% else:
<pre><a href="/{{fp}}">{{bn}}{{ext}}</a></pre>
% end
% end
</body>
</html>
'''


@app.route('/<path:path>')
@app.route('/')
def image_serv(path=''):
    if isdir(path) or path == '':
        return bottle.template(template, path=path, list=sorted(bottle.os.listdir('./' + path)), **globals())
    elif path.lower().endswith('.md'):
        with codecs.open(path, mode="r", encoding="utf-8") as f:
            return markdown.markdown(f.read())
    elif path.lower().endswith('.py'):
        return py2html.py2html(path)
    else:
        return bottle.static_file(path, root='./')


def main(_, port=8100):
    bottle.run(app=app, server='paste', host='0.0.0.0', port=port)


if __name__ == '__main__':
    main(*bottle.sys.argv)
