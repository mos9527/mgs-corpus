from argparse import ArgumentParser
from pathlib import Path
from io import StringIO
import json

'''
<size=0>
<voffset=31.72px>
<br>
</voffset>
</size>

<size=0>
<voffset=31.72px>
<br>
</voffset>
</size>
<space=102px>
KENNETH
<br>
That... that exoskeleton...!
<br>
<br>
<size=0>
<voffset=47.58px>
<br>
</voffset>
</size>
<space=102px>
NINJA
<br>Ggggyyyaaaaaaahhh!!!<br><br><size=0><voffset=47.58px><br></voffset></size><size=0><voffset=47.58px><br></voffset></size><size=0><voffset=31.72px><br></voffset></size><size=0><voffset=31.72px><br></voffset></size><space=102px>SNAKE<br>Who the hell...?<br><br>
'''
def lexer(line : str):
    tokens = []
    tok = ""    
    for c in line:
        if c == "<":
            if tok:
                tokens.append(("TEXT", tok))
                tok = ""            
            tok += c
        elif c == ">":
            tok += c
            tokens.append(("TAG", tok))
            tok = ""            
        else:
            tok += c
    if tok:
        tokens.append(("TEXT", tok))
    return tokens

t_index = 0
def format(line : str):
    global t_index
    res = StringIO()
    tokens = lexer(line)
    stack = []
    istack = [] 
    for type, token in tokens:
        match type:
            case 'TAG':
                token = token[1:-1]
                match token:
                    case 'space=102px':
                        stack.append(f'<div class="show0"><a class="speaker link">')
                        istack.append('</a></div>')
                    case 'size=24':
                        stack.append(f'<div class="show1"><a class="link">')
                        istack.append('</a></div>')
                    case 'width=613':
                        stack.append(f'<div class="show3">')
                        istack.append('</div>')
                    case 'br':
                        res.write('<br/>\n')
            case 'TEXT':
                if token == '―':
                    continue
                for tag in stack:
                    res.write(f'{tag}\n')
                stack = []
                res.write(f'<a href="#{t_index}" id="{t_index}" class="link text">{token}</a>\n')
                for itag in istack:
                    res.write(f'{itag}\n')
                istack = []
                t_index += 1              
    return res.getvalue()
def __main__():
    parser = ArgumentParser(description="METAL GEAR SOLID MASTER COLLECTION VOL. 1 - MGS1 (JP) Screenplay Compilation Tool")
    parser.add_argument("input", help="output_TextData.. JSON file")
    parser.add_argument("--head", default="head.html", help="Head HTML file")
    parser.add_argument("output", help="Output file")
    args = parser.parse_args()
    data = json.load(open(args.input, 'r', encoding='utf-8'))
    data = data['data']    
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n')
        f.write('<meta charset="UTF-8">\n')
        with open(args.head, 'r', encoding='utf-8') as head:
            f.write(head.read())        
        keysL = ['TextAreaA0','TextAreaA1','TextAreaA2','TextAreaA3']
        keysR = ['TextAreaB0','TextAreaB1','TextAreaB2','TextAreaB3']
        for item in data:
            for i in range(len(keysL)):
                f.write('<table>\n')    
                f.write('<tr>\n')
                key = keysL[i]
                f.write(f'<td class="left {key}">\n')                
                f.write(format(item[key]))
                f.write('\n')
                f.write('</td>\n')
                key = keysR[i]
                f.write(f'<td class="right {key}">\n')                
                f.write(format(item[key]))
                f.write('\n')
                f.write('</td>\n')
                f.write('</tr>\n')
                f.write('</table>\n')

if __name__ == "__main__":
    __main__()