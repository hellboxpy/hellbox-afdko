# hellbox-afdko

A hellbox job that wraps executables from AFDKO.

## Usage

Import the chutes you need from `hellbox.jobs.afdko`:

```python
from hellbox.jobs.afdko import MakeOTF, Otf2Ttf, TtfComponentizer
```

### Build OTFs from UFO sources

```python
from hellbox import Hellbox
from hellbox.jobs.afdko import MakeOTF

with Hellbox("build") as task:
    task.read("sources/*.ufo") >> MakeOTF() >> task.write("fonts/")
```

`MakeOTF` accepts the following options, all `False` by default:

| Option | AFDKO flag | Description |
|---|---|---|
| `release` | `-r` | Enable release mode |
| `filter_glyphs` | `-gs` | Filter glyphs to those in the GSUB/GPOS tables |
| `omit_mac_names` | `-omitMacNames` | Omit Macintosh name table entries |

### Convert OTFs to TTFs

```python
from hellbox import Hellbox
from hellbox.jobs.afdko import MakeOTF, Otf2Ttf

with Hellbox("build") as task:
    task.read("sources/*.ufo") >> MakeOTF() >> Otf2Ttf() >> task.write("fonts/")
```

### Componentize TTFs

`TtfComponentizer` requires the source UFO to be adjacent to the TTF. hellbox-afdko
handles this automatically by symlinking the UFO into the temporary working directory.

```python
from hellbox import Hellbox
from hellbox.jobs.afdko import MakeOTF, Otf2Ttf, TtfComponentizer

with Hellbox("build") as task:
    task.read("sources/*.ufo") \
        >> MakeOTF() \
        >> Otf2Ttf() \
        >> TtfComponentizer() \
        >> task.write("fonts/")
```

## Installation

```sh
hell add hellbox-afdko
```

## Development

```sh
uv sync
uv run pytest
```
