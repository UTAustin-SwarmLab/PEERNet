"""Includes FixedImage dataset, which returns a single image sampled over and over."""

from PIL import Image
import numpy as np
from typing import Union


class FixedImage:
    """Implements a valid sensor class that samples a single image."""

    def __init__(self, image_path: str) -> None:
        """Constructor.

        Args:
            image_path (str): path to the image to be sampled.
        """
        self.image_path = image_path

    def sample(
        self, is_rgb: bool = False, numpy: bool = False
    ) -> Union[np.ndarray, Image.Image]:
        """Returns a sample from the dataset (returns the image).

        Args:
            is_rgb (bool): return as rgb?
            numpy (bool): return as np array or PIL Image.
        """
        image = Image.open(self.image_path)

        if not numpy:
            return image

        rgb_image = np.asarray(image)

        if is_rgb:
            return rgb_image
        else:
            return rgb_image[:, :, ::-1]
