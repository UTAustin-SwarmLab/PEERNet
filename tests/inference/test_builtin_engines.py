"""Tests for builtin engines."""

from peernet.inference import (
    DummyModel,
    TorchvisionPretrainedClassifier,
    enginize,
)
from peernet.networks import Message
from peernet.metrics import Timer
from peernet.sensors.datasets import FixedImage


def test_dummy():
    """Tests enginize with a dummy model."""
    dummy_message = Message(0, Timer("main"))

    # Get the engineized dummy model
    ie = enginize(DummyModel)(inference_time=0.15)

    out: Message = ie.callback(dummy_message)

    print(out.data)
    print(out.logger)


def test_efficientnet():
    """Tests enginize with an efficientnet model."""
    dataset = FixedImage("resources/test_image_dog.jpeg")

    img = dataset.sample()

    dummy_message = Message(img, Timer("main"))

    ie = enginize(TorchvisionPretrainedClassifier)(
        model_name="efficientnet_v2_s",
        model_weight_name="EfficientNet_V2_S_Weights",
        device="cpu",
    )

    out: Message = ie.callback(dummy_message)

    print(out.data)
    print(out.logger)
