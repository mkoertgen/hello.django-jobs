# Dependencies

Dependencies are managed using Python standard [pip](https://docs.python.org/3/installing/index.html), i.e.

- runtime dependencies are managed in [requirements.txt]
- development dependencies are managed in [requirements-dev.txt]

Upgrading dependencies can be achieved using [pur](https://pypi.org/project/pur/), i.e.

```console
pur
pur -r requirements-dev.txt
```

Remove all dependencies

```console
pip freeze > all.txt
pip uninstall -y -r all.txt
```

## Vendoring

**Update:** Vendoring is usually not necessary. Still documented here for documentation reasons.

Download packages to `./packages`. **NOTE** that this may download platform-specific packages, e.g. [PyYAML](https://pypi.org/project/PyYAML/).
There is ab open GitHub issue for platform specific wheel downloads, cf.: [pypa/pip/issues/5453: Add `--platform`...](https://github.com/pypa/pip/issues/5453)

```console
pip wheel -r requirements.txt -w ./packages
```

Then install offline using

```console
pip install -r requirements.txt --no-index -f ./packages
```
