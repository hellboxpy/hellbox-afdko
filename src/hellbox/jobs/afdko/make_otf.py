import tempfile
from pathlib import Path

from hellbox import Hellbox
from hellbox.chutes.chute import Chute
from hellbox.source_file import SourceFile


class MakeOTF(Chute):
    def __init__(
        self,
        release: bool = False,
        filter_glyphs: bool = False,
        omit_mac_names: bool = False,
    ) -> None:
        self.release = release
        self.filter_glyphs = filter_glyphs
        self.omit_mac_names = omit_mac_names

    def process(self, file: SourceFile) -> SourceFile:
        from afdko import makeotf

        Hellbox.info(f"Building OTF: {file.name}")
        # Pass a pre-created directory as -o so makeotf names the output file
        # after the font's PostScript name (e.g. SourceSans3-Regular.otf).
        # When given an existing directory, makeotf uses the PS name; when
        # given a non-existent path, it treats it as the literal output filename.
        tmp_dir = Path(tempfile.mkdtemp(dir=file.tmp_root))
        args = ["-f", str(file.content_path), "-o", str(tmp_dir)]
        if self.release:
            args += ["-r"]
        if self.filter_glyphs:
            args += ["-gs"]
        if self.omit_mac_names:
            args += ["-omitMacNames"]
        result = makeotf.main(args)
        if result is not None:
            raise RuntimeError(f"makeotf failed with exit code {result}")
        otf_files = list(tmp_dir.glob("*.otf"))
        if not otf_files:
            raise RuntimeError(f"makeotf produced no .otf file in {tmp_dir}")
        return SourceFile(file.original_path, otf_files[0], file.tmp_root)
