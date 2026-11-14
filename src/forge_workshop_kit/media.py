"""Portable image receipts and typed values for saved evaluation rows."""

import hashlib
from pathlib import Path


def image_value(path, caption='', *, root=None):
    from PIL import Image
    path = Path(path).resolve()
    with Image.open(path) as image:
        width, height = image.size
        format = image.format.lower()
    content = path.read_bytes()
    saved_path = path.relative_to(Path(root).resolve()).as_posix() if root is not None else str(path)
    return {'_workshop_type': 'image', 'path': saved_path, 'sha256': hashlib.sha256(content).hexdigest(),
            'size': len(content), 'format': format, 'width': width, 'height': height, 'caption': caption}


def is_image(value):
    return isinstance(value, dict) and value.get('_workshop_type') == 'image'


def checked_image(value):
    path = Path(value['path'])
    if hashlib.sha256(path.read_bytes()).hexdigest() != value['sha256']:
        raise ValueError('An image changed after evaluation. Restore the saved image before publishing.')
    return path


def map_values(value, image_mapper):
    if is_image(value):
        return image_mapper(value)
    if isinstance(value, dict):
        return {k: map_values(v, image_mapper) for k, v in value.items()}
    if isinstance(value, list):
        return [map_values(v, image_mapper) for v in value]
    return value


def bind_root(value, root):
    """Resolve workspace-relative receipts only for transport, keeping saved IDs portable."""
    def bind(image):
        path = Path(image['path'])
        if path.is_absolute():
            return image
        full = (Path(root) / path).resolve()
        if not full.is_relative_to(Path(root).resolve()):
            raise ValueError('Image receipt escapes the saved workspace.')
        return {**image, 'path': str(full)}
    return map_values(value, bind)


def wandb_value(value):
    import wandb
    return map_values(value, lambda image: wandb.Image(str(checked_image(image)), caption=image['caption']))


def wandb_table_data(rows):
    """Give nested images optional media columns; missing masks remain missing."""
    from copy import deepcopy
    columns = ['case_id', 'input', 'prediction', 'target', 'error', 'scores', 'evidence']
    paths = set()
    def collect(value, path):
        if is_image(value):
            if len(path) > 1:
                paths.add(path)
        elif isinstance(value, dict):
            for key, child in value.items():
                collect(child, (*path, key))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                collect(child, (*path, index))
    for row in rows:
        for field in columns:
            collect(row.get(field), (field,))
    paths = sorted(paths, key=lambda path: '.'.join(map(str, path)))
    data = []
    for row in rows:
        value, images = deepcopy(row), []
        for path in paths:
            parent = value
            try:
                for key in path[:-1]:
                    parent = parent[key]
                child = parent[path[-1]]
                images.append(wandb_value(child) if is_image(child) else None)
                if isinstance(parent, dict):
                    parent.pop(path[-1], None)
                else:
                    parent[path[-1]] = None
            except (KeyError, IndexError, TypeError):
                images.append(None)
        data.append([wandb_value(value.get(column, {} if column in ('scores', 'evidence') else None))
                     for column in columns] + images)
    return columns + ['.'.join(map(str, path)) for path in paths], data


def weave_value(value):
    from PIL import Image
    def read(image):
        with Image.open(checked_image(image)) as source:
            return source.copy()
    return map_values(value, read)


def matches_saved(output, saved):
    if is_image(saved):
        from PIL import Image
        with Image.open(checked_image(saved)) as image:
            return isinstance(output, Image.Image) and output.mode == image.mode and output.size == image.size and output.tobytes() == image.tobytes()
    if isinstance(saved, dict):
        return isinstance(output, dict) and output.keys() == saved.keys() and all(matches_saved(output[k], v) for k, v in saved.items())
    if isinstance(saved, list):
        return isinstance(output, list) and len(output) == len(saved) and all(matches_saved(a, b) for a, b in zip(output, saved))
    return output == saved
