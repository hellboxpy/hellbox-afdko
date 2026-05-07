from hellbox import Hellbox
from hellbox.chutes.chute import Chute
from hellbox.source_file import SourceFile


class Otf2Ttf(Chute):
    def process(self, file: SourceFile) -> SourceFile:
        from afdko import otf2ttf

        Hellbox.info(f"Converting to TTF: {file.name}")
        copy = file.copy(name=file.stem + ".ttf")
        result = otf2ttf.main([str(file.content_path), "-o", str(copy.content_path)])
        if result is not None:
            raise RuntimeError(f"otf2ttf failed with exit code {result}")
        return copy
