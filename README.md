# Photo Watermark

Adds a watermark to photos

## Usage

It is possible to use arguments as follows:
```text
$ python3 watermark.py --help
usage: watermark.py [-h] [--dir DIR] [--ext EXT] [--out OUT]
                    [--watermark WATERMARK] [--br | --bl | --tr | --tl]
                    [--scale SCALE]

Add watermarks to given images.

options:
  -h, --help            show this help message and exit
  --dir DIR, -d DIR     Path to the folder of images to watermark.
  --ext EXT, -e EXT     The file extension of images to be watermarked. Case
                        insensitive.
  --out OUT, -o OUT     Path to the output folder. Will be created if it
                        doesn't exist.
  --watermark WATERMARK, -w WATERMARK
                        Path to the watermark file.
  --br                  Places the watermark in the bottom right corner.
  --bl                  Places the watermark in the bottom left corner.
  --tr                  Places the watermark in the top right corner.
  --tl                  Places the watermark in the top left corner.
  --scale SCALE, -s SCALE
                        Scaling factor of the watermark as a proportion of the
                        original image.
```

Otherwise, running the script without arguments, as below, starts an interactive mode 

```text
$ python3 watermark.py
```
