# Teaching data

Participants use the prepared teaching bundles offered by their notebook's Download control. They do not need to run acquisition scripts. The package includes the smaller office, transit, and airline fixtures directly.

## Reproduce the Solar bundle

From the repository root, install the maintainer acquisition dependencies and fetch the predeclared observations:

```sh
uv run --frozen --group data-prep python scripts/prepare_solar.py
```

This command downloads real source observations and writes `data/solar-v1/`. It can take much longer than opening the prepared teaching bundle. Use `--part goes` or `--part aia` to acquire one part; a partial bundle is not a complete workshop dataset.

The archive contains `manifest.json`, GOES measurements, AIA arrays, source and exclusion records, and a representative FITS file. Verify the archive checksum and each manifest checksum before training. The [Solar data contract](../docs/solar-contract.md#data) defines dates, units, partitions, and quality exclusions; the [evidence review](../docs/solar-evidence.md) records what was acquired.

For the other downloaded datasets, start with the [Routing](../docs/routing-workshop.md#dataset-and-fixed-worked-example) or [Inspection](../docs/inspection-workshop.md#data-and-prediction-task) preparation record. Their acquisition scripts and licenses differ from Solar's.

Raw downloads and generated arrays are ignored by Git. Publish only reviewed prepared archives and checksums as release assets. Keep source attribution, licenses, exclusions, and split assignments with every bundle.
