#!/usr/bin/env python

from __future__ import annotations

import functools
import pathlib
import urllib.request

import gradio as gr
import PIL.Image
from manga_ocr import MangaOcr

TITLE = 'Manga OCR'
DESCRIPTION = 'This is an unofficial demo for https://github.com/kha-white/manga-ocr.'


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


mocr = MangaOcr()
func = functools.partial(run, mocr=mocr)

image_paths = download_sample_images()
examples = [[path.as_posix()] for path in image_paths]

gr.Interface(
    fn=func,
    inputs=gr.Image(label='Input', type='pil'),
    outputs=gr.Text(label='Output'),
    examples=examples,
    title=TITLE,
    description=DESCRIPTION,
).launch(show_api=False)
