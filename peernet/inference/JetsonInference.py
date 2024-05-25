"""Inference object for jetson inference object detectors.

A note on installation: Jetson Inference is not installed through PyPI, so
it is not installed when PEERNet is installed through pip. Jetson Inference
should be installed from source or built on machine.
"""

import cv2  # type: ignore
import jetson.utils  # type: ignore
import jetson.inference  # type: ignore
import numpy as np


class JetsonInferenceObjectDetector:
    """Inference class that uses Jetson Inference Detect Nets for object detection."""

    def __init__(self, model_name: str, threshold: float = 0.5) -> None:
        """Constructor.

        Args:
            model_name: str - Name of model to use
            threshold: float - Detection threshold. Default = 0.5
        """
        self.model_name = model_name
        self.threshold = threshold
        self.net = jetson.inference.detectNet(model_name)

    def read_cv(self, image_path: str) -> np.ndarray:
        """Reads an image from image_path and returns the opencv representation."""
        return cv2.imread(image_path)

    def preprocess(self, cv_image: np.ndarray) -> jetson.utils.cudaImage:
        """Preprocesses the image.

        Allocated cuda memory for the image, and returns a jetson.utils.cudaImage
        object with allocated GPU memory.

        Args:
            cv_image: np.ndarray - opencv image in bgr format.

        Returns:
            jetson.utils.cudaImage
        """
        # Convert from cv to cuda
        bgr_frame = jetson.utils.cudaFromNumpy(cv_image, isBGR=True)
        rgb_cuda_frame = jetson.utils.cudaAllocMapped(
            width=bgr_frame.width, height=bgr_frame.height, format="rgb8"
        )
        jetson.utils.cudaConvertColor(bgr_frame, rgb_cuda_frame)
        return rgb_cuda_frame

    def infer(self, cuda_frame: jetson.utils.cudaImage) -> jetson.utils.cudaImage:
        """Runs the detectnet on the cuda frame.

        Args:
            cuda_frame: jetson.utils.cudaImage - GPU mapped memory of an image.

        Returns:
            jetson.utils.cudaImage - mapped memory with detections
        """
        self.net.Detect(cuda_frame)
        return cuda_frame

    def postprocess(self, cuda_frame: jetson.utils.cudaImage) -> np.ndarray:
        """Converts a cuda frame back to an opencv image.

        Args:
            cuda_frame: jetson.utils.cudaImage - CUDA memory of an image + detections.

        Returns:
            np.ndarray - opencv image in bgr8 format with detections
        """
        # Convert from cuda back to cv
        bgr_cv_frame = jetson.utils.cudaAllocMapped(
            width=cuda_frame.width, height=cuda_frame.height, format="bgr8"
        )
        jetson.utils.cudaConvertColor(cuda_frame, bgr_cv_frame)
        jetson.utils.cudaDeviceSynchronize()
        cv_frame = jetson.utils.cudaToNumpy(bgr_cv_frame)
        return cv_frame
