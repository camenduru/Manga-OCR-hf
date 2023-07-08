#!/usr/bin/env python

from __future__ import annotations

import functools
import os
import pathlib
import urllib.request

import gradio as gr
import PIL.Image
from manga_ocr import MangaOcr

DESCRIPTION = '# [Manga OCR](https://github.com/kha-white/manga-ocr)'


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
fn = functools.partial(run, mocr=mocr)

image_paths = download_sample_images()
examples = [[path.as_posix()] for path in image_paths]

with gr.Blocks(css='style.css') as demo:
    gr.Markdown(DESCRIPTION)
    with gr.Row():
        with gr.Column():
            image = gr.Image(label='Input', type='pil')
            run_button = gr.Button('Run')
        with gr.Column():
            result = gr.Text(label='Output')
    gr.Examples(examples=examples,
                inputs=image,
                outputs=result,
                fn=fn,
                cache_examples=os.getenv('CACHE_EXAMPLES') == '1')
    run_button.click(fn=fn, inputs=image, outputs=result, api_name='run')
demo.queue().launch()
