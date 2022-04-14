"""Watermark.

Adds a watermark to the given files.
"""
from PIL import Image
from pathlib import Path
from argparse import ArgumentParser
from tqdm import tqdm
import sys


PADDING_PROPORTION = 0.2


def parse_args():
    p = ArgumentParser(description="Add watermarks to given images.")
    p.add_argument('--dir', '-d', type=Path,
                   help='Path to the folder of images to watermark.')
    p.add_argument('--ext', '-e', type=str,
                   help='The file extension of images to be watermarked. '
                        'Case insensitive.')
    p.add_argument('--out', '-o', type=Path,
                   help='Path to the output folder. Will be created if it '
                        'doesn\'t exist.')
    p.add_argument('--watermark', '-w', type=Path,
                   help='Path to the watermark file.')
    g = p.add_mutually_exclusive_group()
    g.add_argument('--br', action='store_true',
                   help='Places the watermark in the bottom right corner.')
    g.add_argument('--bl', action='store_true',
                   help='Places the watermark in the bottom left corner.')
    g.add_argument('--tr', action='store_true',
                   help='Places the watermark in the top right corner.')
    g.add_argument('--tl', action='store_true',
                   help='Places the watermark in the top left corner.')

    p.add_argument('--scale', '-s', type=float, default=0.16,
                   help='Scaling factor of the watermark as a proportion of '
                        'the original image.')

    if len(sys.argv) == 1:
        p.print_help(sys.stdout)
        print("\nRunning in interactive mode. Note that it is possible to "
              "run this script with arguments\n")

    return p.parse_args()


def do_watermark(in_path: Path, extension: str, out_path: Path,
                 watermark_path: Path, position: str, scale: float):
    """Actually places the watermark.

    Args:
        in_path: Path to the folder of images to watermark.
        extension: Extension of images to watermark in the folder
        out_path: Path to the output folder. Will be created if it does not
            exist.
        watermark_path: Path to the watermark file.
        position: One of (br, bl, tr, tl) (Bottom right, bottom left, top right,
            top left)
        scale: Scaling factor of the watermark as a proportion of the original
            image
    """
    imgs_to_watermark = []
    for f in in_path.iterdir():
        if f.suffix.lower() == extension.lower():
            imgs_to_watermark.append(f)

    watermark = Image.open(watermark_path)

    for f in tqdm(imgs_to_watermark):
        image = Image.open(f)

        temp_watermak = watermark.copy()
        width = image.size[0]
        height = image.size[1]

        # Adjust to size of the watermark relatively to the current image
        watermark_size = (int(width * scale), int(height * scale))
        min_size = watermark_size[0] if watermark_size[0] < watermark_size[
            1] else watermark_size[1]
        temp_watermak.thumbnail(watermark_size)

        # Locate the watermark at a specific distance from the selected corner
        if position[0] == 'b':
            y_loc = int(height - (PADDING_PROPORTION + 1) * min_size)
        else:
            y_loc = int(PADDING_PROPORTION * min_size)

        if position[1] == 'r':
            x_loc = int(width - (PADDING_PROPORTION + 1) * min_size)
        else:
            x_loc = int(PADDING_PROPORTION * min_size)

        # Ensures transparency
        image.paste(temp_watermak, (x_loc, y_loc), temp_watermak)

        # Save image with a number to the according folder
        out_path.mkdir(parents=True, exist_ok=True)
        image.save(out_path / Path(str(f.stem) + '.jpg'), 'JPEG')


if __name__ == '__main__':
    args = parse_args()

    in_path = args.dir if args.dir is not None \
        else Path(input("Input dir? >> "))
    extension = args.ext if args.ext is not None \
        else input("Image extension? >> ")
    out_path = args.out if args.out is not None \
        else Path(input("Output dir? >> "))
    watermark_path = args.watermark if args.watermark is not None \
        else Path(input("Watermark path? >> "))

    scale = args.scale if args.scale is not None \
        else float(input("Scaling? [0.16] >> ") or '0.16')

    # Checks
    assert in_path.exists(), f'Given input dir {in_path} does not exist'
    assert watermark_path.exists(), f'Given watermark file {watermark_path} ' \
                                    f'does not exist'
    assert watermark_path.is_file(), f'Given watermark file {watermark_path} ' \
                                     f'is not a file.'

    if args.br:
        pos = 'br'
    elif args.bl:
        pos = 'bl'
    elif args.tr:
        pos = 'tr'
    elif args.tl:
        pos = 'tl'
    else:
        pos_given = False
        while not pos_given:
            pos = input("Watermark position? br/bl/tr/tl")
            pos_given = pos in ('br', 'bl', 'tr', 'tl')

    do_watermark(in_path, extension, out_path, watermark_path, pos, scale)
