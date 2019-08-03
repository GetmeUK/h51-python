# H51 Python Library

The H51 Python library provides a pythonic interface to the H51 API. It includes an API client class, a set of resource classes and classes for configuring core analyzers and transforms.


## Installation

```
pip install h51
```

## Requirements

- Python 3.7+


# Usage

```Python

import h51


client = h51.Client('your_api_key...')

# Create an asset
with open('image.bmp') as f:
    asset = h51.Asset.create(client, f)

# Analyze the image asset to find its dominant colours and focal point
asset.analyze([
    h51.transforms.images.DominantColours(),
    h51.analyzers.images.FocalPoint()
])

# Create web optimized variations of the image
h51.resources.Variation.create(
    asset,
    {
        'x1': [
            h51.transforms.images.AutoOrient(),
            h51.transforms.images.FocalPointCrop(aspect_ratio=0.5),
            h51.transforms.images.Fit(640, 640),
            h51.transforms.images.Output('WEBP')
        ],
        'x2': [
            h51.transforms.images.AutoOrient(),
            h51.transforms.images.FocalPointCrop(aspect_ratio=0.5),
            h51.transforms.images.Fit(1280, 1280),
            h51.transforms.images.Output('WEBP')
        ]
    }
])

```
