from argparse import ArgumentParser
from pathlib import Path
from tqdm import tqdm
import UnityPy
def __main__():
    parser = ArgumentParser(description="METAL GEAR SOLID MASTER COLLECTION VOL. 1 - MGS2/3 Screenplay Compilation Tool")
    parser.add_argument("input", help="Game directory")
    parser.add_argument("--head", default="head.html", help="Head HTML file")
    parser.add_argument("output", help="Output directory")
    args = parser.parse_args()
    paths = Path(args.input)
    paths = list(paths.glob('**/output_*.bundle')) + list(paths.glob('**/speaker*.bundle'))
    env = UnityPy.Environment()
    for path in tqdm(paths,desc="Loading"):
        env.load_file(path.as_posix())
    objects = [(o.peek_name(), o) for o in env.objects]
    objects = sorted(objects, key=lambda x: x[1].byte_size) 
    objects = {name: obj for name, obj in objects}     
    speakers = objects['SpeakerAsset'].read()
    speakers = {x.speakerId : x for x in speakers.speakerItemList}
    output_EN = objects['output_EN'].read()
    output_JP = objects["output_JP"].read()    
    def write_one(items, path : Path, lang : str):
        with open(path, 'w', encoding='utf-8') as f:
            f.write('<!DOCTYPE html>\n')
            f.write('<meta charset="UTF-8">\n')
            with open(args.head, 'r', encoding='utf-8') as head:
                f.write(head.read())
            for index, item in tqdm(list(enumerate(items)), "Writing"):
                speaker = f'<p class="speaker">{speakers[item.speakerId].__dict__[lang]}</p>\n\t' if item.speakerId else ''
                text : str = item.text
                for _ in range(text.count('<b>') - text.count('</b>')):
                    text += '</b>'
                f.write(f'''<div id="{index}" class="show{item.showType}">
    {speaker}<a href="#{index}" class="link text">{text}</a>
</div>
''')
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    write_one(output_EN.data[1:-1], output / "english.html", "speakerName_EN")
    write_one(output_JP.data[1:-1], output / "japanese.html", "speakerName_JP")

if __name__ == "__main__":
    __main__()