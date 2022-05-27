#!/usr/bin/env python

from __future__ import annotations

import argparse
import functools
import pathlib
import urllib.request

import gradio as gr
import PIL.Image
from manga_ocr import MangaOcr

TITLE = 'kha-white/manga-ocr'
DESCRIPTION = 'This is a demo for https://github.com/kha-white/manga-ocr.'
ARTICLE = '<center><img src="https://visitor-badge.glitch.me/badge?page_id=hysts.manga-ocr" alt="visitor badge"/></center>'


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--theme', type=str)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--share', action='store_true')
    parser.add_argument('--port', type=int)
    parser.add_argument('--disable-queue',
                        dest='enable_queue',
                        action='store_false')
    parser.add_argument('--allow-flagging', type=str, default='never')
    return parser.parse_args()


def download_sample_images() -> list[pathlib.Path]:
    image_dir = pathlib.Path('images')
    if not image_dir.exists():
        image_dir.mkdir()
        for index in range(12):
            url = f'https://raw.githubusercontent.com/kha-white/manga-ocr/master/assets/examples/{index:02d}.jpg'
            urllib.request.urlretrieve(url, image_dir / f'{index:02d}.jpg')
    return sorted(image_dir.rglob('*.jpg'))


def run(image: PIL.Image.Image, mocr: MangaOcr) -> str:
    return mocr(image)


def main():
    args = parse_args()

    mocr = MangaOcr()

    func = functools.partial(run, mocr=mocr)
    func = functools.update_wrapper(func, run)

    image_paths = download_sample_images()
    examples = [[path.as_posix()] for path in image_paths]

    gr.Interface(
        func,
        gr.inputs.Image(type='pil', label='Input'),
        gr.outputs.Textbox(type='str', label='Output'),
        examples=examples,
        title=TITLE,
        description=DESCRIPTION,
        article=ARTICLE,
        theme=args.theme,
        allow_flagging=args.allow_flagging,
        live=args.live,
    ).launch(
        enable_queue=args.enable_queue,
        server_port=args.port,
        share=args.share,
    )


if __name__ == '__main__':
    main()
