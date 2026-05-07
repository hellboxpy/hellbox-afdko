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
        import tempfile
        from pathlib import Path
        from afdko import makeotf

        Hellbox.info(f"Building OTF: {file.name}")
        # Create a temp directory and specify the output file path within it.
        # We must NOT pre-create the output path as a directory: makeotf treats
        # an existing directory as an output folder and names the file after the
        # font's PostScript name instead of using the path as a file name.
        tmp_dir = Path(tempfile.mkdtemp(dir=file.tmp_root))
        output_path = tmp_dir / (file.stem + ".otf")
        args = ["-f", str(file.content_path), "-o", str(output_path)]
        if self.release:
            args += ["-r"]
        if self.filter_glyphs:
            args += ["-gs"]
        if self.omit_mac_names:
            args += ["-omitMacNames"]
        result = makeotf.main(args)
        if result and result != 0:
            raise RuntimeError(f"makeotf failed with exit code {result}")
        return SourceFile(file.original_path, output_path, file.tmp_root)
