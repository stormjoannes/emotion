#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tqdm import tqdm
from torchvision.datasets import ImageFolder
from torchvision.transforms import Compose, Grayscale, Resize
from facenet_pytorch import MTCNN
from model import FaceFinder


def crop_and_save(dataset, out_dir):
    """Crop each image from the dataset and store in the output directory

    Parameters
    ----------
    dataset: Dataset
        The pytorch Dataset class for generating the images
    out_dir: str
        The path to the output directory
    """
    labels = dataset.classes
    for i, (img, label_idx) in enumerate(tqdm(dataset)):
        emotion = labels[label_idx]
        output_dir = os.path.join(out_dir, emotion)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        img.save(os.path.join(output_dir, f'{emotion}_{i}.png'), 'PNG')


if __name__ == '__main__':
    # process the raw images, detect the faces, crop them, make them grayscale, and save them
    root_dir = '/home/mchobanyan/data/emotion/images/'
    raw_dir = os.path.join(root_dir, 'raw')
    output_dir = os.path.join(root_dir, 'gray')

    face_model = FaceFinder(MTCNN(keep_all=True))
    transforms = Compose([face_model, Resize((224, 224)), Grayscale(1)])
    base_dataset = ImageFolder(raw_dir, transform=transforms)
    crop_and_save(base_dataset, output_dir)