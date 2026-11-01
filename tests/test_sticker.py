import importlib.util,tempfile,unittest
from pathlib import Path
from PIL import Image,ImageDraw
spec=importlib.util.spec_from_file_location('sticker',Path(__file__).parents[1]/'scripts/sticker.py');s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
class StickerTest(unittest.TestCase):
 def test_animated_export_and_infinite_rejection(self):
  with tempfile.TemporaryDirectory() as d:
   d=Path(d);f=d/'frames';f.mkdir()
   for i in range(8):
    im=Image.new('RGBA',(320,270));ImageDraw.Draw(im).rectangle((20+i*5,40,80+i*5,100),fill='red');im.save(f/f'{i:02}.png')
   p=d/'out.png';s.save_animated(f,p,2000);s.verify(p,'animated')
   with Image.open(p) as im:
    self.assertEqual(im.n_frames,8);self.assertEqual(im.info['loop'],1);imgs=[]
    for i in range(im.n_frames):im.seek(i);imgs.append(im.convert('RGBA').copy())
   imgs[0].save(p,save_all=True,append_images=imgs[1:],duration=250,loop=0)
   with self.assertRaises(SystemExit):s.verify(p,'animated')
 def test_static(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'out.png';s.save_static(Path(__file__).parents[1]/'examples/rest-break/static.png',p);s.verify(p,'static')
   with Image.open(p) as im:self.assertGreaterEqual(im.info['dpi'][0],71.99);self.assertEqual(im.getpixel((0,0))[3],0)
