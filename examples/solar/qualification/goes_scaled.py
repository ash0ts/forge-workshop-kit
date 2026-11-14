"""Predict log-flux on a consistent scale, optionally correcting persistence.

The caller supplies normalization fitted on training observations only. Validation
and final targets never enter build_model or fit.
"""
import torch
from torch import nn


def build_model(input_shape, config):
    width = config.get("width", 16)

    class FluxPredictor(nn.Module):
        def __init__(self):
            super().__init__()
            if config["architecture"] == "mlp":
                self.net = nn.Sequential(
                    nn.Flatten(), nn.Linear(input_shape[0] * input_shape[1], width),
                    nn.ReLU(), nn.Linear(width, 1),
                )
            else:
                self.net = nn.Sequential(
                    nn.Conv1d(input_shape[0], width, 5, padding=2), nn.ReLU(),
                    nn.AdaptiveAvgPool1d(1), nn.Flatten(), nn.Linear(width, 1),
                )
            self.residual = config["residual"]
            self.register_buffer("center", torch.tensor(float(config["target_center"])))
            self.register_buffer("scale", torch.tensor(float(config["target_scale"])))
            if self.residual:
                nn.init.zeros_(self.net[-1].weight)
                nn.init.zeros_(self.net[-1].bias)

        def forward(self, x):
            value = self.net(x)
            if self.residual:
                value = value + x[:, 1, -1:]
            return value * self.scale + self.center

    return FluxPredictor()


def training_loss(prediction, target, mask):
    return ((prediction - target).abs() * mask).sum() / mask.sum()


def fit(model, x, y, mask, config):
    optimizer = torch.optim.Adam(model.parameters(), lr=config["learning_rate"])
    generator = torch.Generator().manual_seed(config["seed"])
    losses = []
    model.train()
    for _ in range(config["steps"]):
        indices = torch.randint(len(x), (min(config["batch_size"], len(x)),), generator=generator)
        # Both prediction and target use the same training-fitted flux scale.
        loss = training_loss(model(x[indices]), y[indices], mask[indices]) / model.scale
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach()))
    return losses
