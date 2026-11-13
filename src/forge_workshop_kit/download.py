"""Small public teaching artifact, with checksums before any training."""
import hashlib
import json
import shutil
import tarfile
import tempfile
from pathlib import Path
import httpx
from .solar import verify_data

RELEASE='https://github.com/ash0ts/forge-workshop-kit/releases/download/v0.1.0'


def dataset(destination='data/solar-v1', *, base_url=RELEASE):
    destination=Path(destination)
    if (destination/'manifest.json').exists():
        return destination,verify_data(destination)
    with tempfile.TemporaryDirectory() as folder:
        root=Path(folder).resolve()
        metadata=httpx.get(base_url+'/solar-v1.sha256',follow_redirects=True,timeout=30)
        metadata.raise_for_status()
        expected=metadata.text.split()[0]
        archive=root/'solar-v1.tar.gz'
        with httpx.stream('GET',base_url+'/solar-v1.tar.gz',follow_redirects=True,timeout=60) as response:
            response.raise_for_status()
            with archive.open('wb') as output:
                for chunk in response.iter_bytes():
                    output.write(chunk)
        if hashlib.sha256(archive.read_bytes()).hexdigest()!=expected:
            raise ValueError('Download checksum mismatch.')
        with tarfile.open(archive) as bundle:
            for entry in bundle.getmembers():
                if not (root/entry.name).resolve().is_relative_to(root) or entry.issym() or entry.islnk():
                    raise ValueError('Unsafe dataset archive entry')
            bundle.extractall(root,filter='data')
        verify_data(root/'solar-v1')
        destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copytree(root/'solar-v1',destination)
    return destination,verify_data(destination)
