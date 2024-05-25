"""Implements an inference object for pytorch image classifiers."""

import torch  # type: ignore
import torchvision  # type: ignore
from torchvision.models import get_weight  # type: ignore
import PIL.Image

import logging
from peernet.utils import ch

from typing import Literal, Tuple


class TorchvisionPretrainedClassifier:
    """An inference class for any cv classifier we can pull from torchvision."""

    def __init__(
        self,
        model_name: str,
        model_weight_name: str,
        device: torch.device,
        verbose: Literal[0, 1, 2] = 1,
    ):
        """Constructor for TorchvisionPretrainedClassifier.

        Args:
            model_name: str - Name of pytorch model
            model_weight_name: str - Name of weights to use
            device: torch.device - CPU, cuda core, etc.
            verbose: Literal[0, 1, 2] - Verbosity of output. 0 enables all messages,
                1 enables warnings and above, and 2 enables only critical errors.
        """
        # logger setup
        self.logger = logging.getLogger("TorchvisionPretrained")
        if verbose == 0:
            self.logger.setLevel(logging.DEBUG)
        elif verbose == 1:
            self.logger.setLevel(logging.WARN)
        else:
            self.logger.setLevel(logging.CRITICAL)
        self.logger.addHandler(ch)

        self.device = device

        # Make sure the model name passed in is valid
        if model_name not in torchvision.models.list_models():
            self.logger.error(
                f"model_name {model_name} not found in torchvision models list"
            )

        # I don't know how to make sure the weights actually exist right now

        # Pull the model and the weights class
        self.logger.debug(f"model_name is {model_name}")
        self.logger.debug(f"model weight name is {model_weight_name}")
        self.weights = get_weight(f"{model_weight_name}.DEFAULT")
        self.model = torch.hub.load("pytorch/vision", model_name, weights=self.weights)

        self.model.to(self.device)
        self.model.eval()

        # Step 2: Initialize the inference transforms
        self.preprocessor = self.weights.transforms(antialias=None)

    def preprocess(self, img: PIL.Image) -> torch.tensor:
        """Apply required transfomrations pulled from torchhub itself.
        
        Args:
            img: PIL.Image - input image
        """
        self.batch = self.preprocessor(img).unsqueeze(0).to(self.device)
        return self.batch

    def infer(self, x: torch.tensor) -> torch.tensor:
        """Get the actual  output tensor."""
        return self.model(self.batch)

    def postprocess(self, x: torch.tensor) -> Tuple[str, float]:
        """Processes output tensor into classification + score."""
        prediction = x.squeeze(0).softmax(0)
        class_id = prediction.argmax().item()
        score = prediction[class_id].item()
        category_name = self.weights.meta["categories"][class_id]

        return (category_name, score)
