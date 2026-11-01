#!/usr/bin/env python3
"""Static and animated LINE sticker asset preparation (not a LINE upload client)."""
import argparse
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image

STATIC_SIZE = (370, 320)
ANIMATED_SIZE = (320, 270)

def fitted(im, size):
    im = im.convert('RGBA')
    im.thumbnail((size[0]-20, size[1]-20), Image.Resampling.LANCZOS)
    out = Image.new('RGBA', size, (0, 0, 0, 0))
    out.alpha_composite(im, ((size[0]-im.width)//2, (size[1]-im.height)//2))
    return out

def save_static(src, dst):
    with Image.open(src) as im:
        out = fitted(im, STATIC_SIZE)
    dst.parent.mkdir(parents=True, exist_ok=True)
    out.save(dst, format='PNG', optimize=True, dpi=(72,72))

def save_animated(folder, dst, duration_ms):
    paths = sorted(p for p in folder.iterdir() if p.suffix.lower() == '.png')
    if not 5 <= len(paths) <= 20:
        raise ValueError('Animated sticker requires 5–20 PNG frames')
    if duration_ms < 1000 or duration_ms > 4000 or duration_ms % 1000:
        raise ValueError('Choose total duration of 1000, 2000, 3000, or 4000 ms')
    if duration_ms % len(paths):
        raise ValueError('For this simple exporter, total duration must divide evenly by frame count')
    frames = []
    for path in paths:
        with Image.open(path) as im:
            frames.append(fitted(im, ANIMATED_SIZE))
    dst.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(dst, format='PNG', save_all=True, append_images=frames[1:],
                   duration=duration_ms // len(frames), loop=1, disposal=0, blend=0,
                   optimize=False)

def verify(path, kind):
    with Image.open(path) as im:
        frame_count = getattr(im, 'n_frames', 1)
        target = ANIMATED_SIZE if kind == 'animated' else STATIC_SIZE
        problems = []
        if im.format != 'PNG': problems.append('Not a PNG file')
        if im.size != target: problems.append(f'Expected canvas {target}, got {im.size}')
        if kind == 'animated' and not 5 <= frame_count <= 20:
            problems.append('Expected 5–20 frames')
        if kind == 'static' and frame_count != 1: problems.append('Expected one frame')
        if kind == 'animated' and not 1 <= im.info.get('loop',0) <= 4:
            problems.append('Expected 1–4 plays; infinite looping is not an upload asset')
        if kind == 'animated' and not (1000 <= im.info.get('loop',0) * sum(im.seek(i) or im.info.get('duration',0) for i in range(frame_count)) <= 4000):
            problems.append('Animation duration must be 1–4 seconds')
        for i in range(frame_count):
            im.seek(i)
            if im.convert('RGBA').getextrema()[3][0] == 255:
                problems.append(f'Frame {i} has no transparent pixels')
        size_bytes = path.stat().st_size
        if size_bytes >= 1_000_000: problems.append('File >= 1 MB; verify latest platform limit')
        report = {'path':str(path),'type':kind,'size':list(im.size),'frames':frame_count,
                  'bytes':size_bytes,'passed':not problems,'issues':problems,
                  'note':'Technical checks only; official platform rules and visual approval still required.'}
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if problems: raise SystemExit(1)

def package(folder, dst):
    assets = sorted(p for p in folder.glob('*.png') if p.is_file())
    if not assets: raise ValueError('No PNG assets in input directory')
    dst.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(dst, 'w', ZIP_DEFLATED) as z:
        for p in assets: z.write(p, p.name)
    print(f'Packaged {len(assets)} PNG files into {dst}')

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='command',required=True)
    s=sub.add_parser('static');s.add_argument('--input',type=Path,required=True);s.add_argument('--output',type=Path,required=True)
    a=sub.add_parser('animated');a.add_argument('--frames-dir',type=Path,required=True);a.add_argument('--output',type=Path,required=True);a.add_argument('--duration-ms',type=int,default=2000)
    v=sub.add_parser('verify');v.add_argument('--input',type=Path,required=True);v.add_argument('--kind',choices=['static','animated'],required=True)
    p=sub.add_parser('package');p.add_argument('--input-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.command=='static':save_static(args.input,args.output)
    elif args.command=='animated':save_animated(args.frames_dir,args.output,args.duration_ms)
    elif args.command=='verify':verify(args.input,args.kind)
    else:package(args.input_dir,args.output)
if __name__=='__main__':main()
