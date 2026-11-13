# Teaching data

Run `uv run python scripts/prepare_solar.py` to reproduce acquisition and preparation. This downloads the predeclared source observations; attendees should use the prepared release archive instead.

The release archive contains `solar-v1/manifest.json`, GOES measurements, AIA arrays, source/exclusion manifests and a representative FITS image. Verify the published archive checksum, then every manifest checksum before training.

Raw downloads and generated arrays are ignored by Git. Publish only the reviewed prepared archive and its checksum as release assets.
