"""Pinned ResNet-18 feature encoder for the VisA teaching cache.

The layer layout follows torchvision's BSD-3-Clause ResNet implementation.
ImageNet weights are fixed. No training or download occurs on import.
"""
from pathlib import Path
import hashlib
import numpy as np

WEIGHTS_URL = 'https://download.pytorch.org/models/resnet18-f37072fd.pth'
WEIGHTS_SHA256 = 'f37072fd47e89c5e827621c5baffa7500819f7896bbacec160b1a16c560e07ec'
ENCODER_ID = 'resnet18-imagenet1k-v1-layer2-layer3-rp64-v1'
TRANSFORM = {'resize': [224, 224], 'interpolation': 'PIL.BILINEAR',
             'mean': [.485, .456, .406], 'std': [.229, .224, .225],
             'patch_grid': [14, 14], 'projection_seed': 20261114,
             'projection_channels': 64, 'global_channels': 512}


def model(weights_path):
    import torch
    from torch import nn

    class Block(nn.Module):
        def __init__(self, incoming, outgoing, stride=1):
            super().__init__()
            self.conv1 = nn.Conv2d(incoming, outgoing, 3, stride, 1, bias=False)
            self.bn1 = nn.BatchNorm2d(outgoing)
            self.relu = nn.ReLU(inplace=True)
            self.conv2 = nn.Conv2d(outgoing, outgoing, 3, 1, 1, bias=False)
            self.bn2 = nn.BatchNorm2d(outgoing)
            self.downsample = (nn.Sequential(nn.Conv2d(incoming, outgoing, 1, stride, bias=False),
                                            nn.BatchNorm2d(outgoing))
                               if stride != 1 or incoming != outgoing else None)
        def forward(self, x):
            residual = x if self.downsample is None else self.downsample(x)
            return self.relu(self.bn2(self.conv2(self.relu(self.bn1(self.conv1(x))))) + residual)

    class Encoder(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = nn.Conv2d(3, 64, 7, 2, 3, bias=False)
            self.bn1 = nn.BatchNorm2d(64)
            self.relu = nn.ReLU(inplace=True)
            self.maxpool = nn.MaxPool2d(3, 2, 1)
            self.layer1 = nn.Sequential(Block(64, 64), Block(64, 64))
            self.layer2 = nn.Sequential(Block(64, 128, 2), Block(128, 128))
            self.layer3 = nn.Sequential(Block(128, 256, 2), Block(256, 256))
            self.layer4 = nn.Sequential(Block(256, 512, 2), Block(512, 512))
            self.avgpool = nn.AdaptiveAvgPool2d(1)
            self.fc = nn.Linear(512, 1000)
        def forward(self, x):
            x = self.layer1(self.maxpool(self.relu(self.bn1(self.conv1(x)))))
            l2 = self.layer2(x)
            l3 = self.layer3(l2)
            global_features = self.avgpool(self.layer4(l3)).flatten(1)
            patch_features = torch.cat([nn.functional.avg_pool2d(l2, 2), l3], dim=1)
            return global_features, patch_features

    path = Path(weights_path)
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != WEIGHTS_SHA256:
        raise ValueError('The ResNet-18 weight checksum does not match the pinned checkpoint.')
    encoder = Encoder()
    encoder.load_state_dict(torch.load(path, map_location='cpu', weights_only=True), strict=True)
    return encoder.eval()


def encode(paths, weights_path, *, batch_size=16, progress=None):
    import torch
    from PIL import Image
    torch.set_num_threads(2)
    encoder = model(weights_path)
    rng = np.random.default_rng(TRANSFORM['projection_seed'])
    projection = torch.from_numpy((rng.standard_normal((384, 64)) / np.sqrt(64)).astype('float32'))
    globals_, patches = [], []
    mean = torch.tensor(TRANSFORM['mean'])[:, None, None]
    std = torch.tensor(TRANSFORM['std'])[:, None, None]
    with torch.inference_mode():
        for offset in range(0, len(paths), batch_size):
            images = []
            for path in paths[offset:offset + batch_size]:
                with Image.open(path) as image:
                    arr = np.array(image.convert('RGB').resize((224, 224), Image.Resampling.BILINEAR), dtype=np.float32) / 255
                images.append((torch.from_numpy(arr).permute(2, 0, 1) - mean) / std)
            whole, patch = encoder(torch.stack(images))
            projected = patch.permute(0, 2, 3, 1) @ projection
            globals_.append(whole.numpy().astype('float16'))
            patches.append(projected.numpy().astype('float16'))
            if progress:
                progress(min(offset + batch_size, len(paths)), len(paths))
    return np.concatenate(globals_), np.concatenate(patches)
