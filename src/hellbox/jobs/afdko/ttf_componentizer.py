from pathlib import Path
from hellbox import Hellbox
from hellbox.chutes.chute import Chute
from hellbox.source_file import SourceFile


class TtfComponentizer(Chute):
    def process(self, file: SourceFile) -> SourceFile:
        from afdko import ttfcomponentizer

        Hellbox.info(f"Componentizing: {file.name}")
        copy = file.copy()

        # ttfcomponentizer looks for a UFO in the same directory as the TTF
        # Create a symlink to the original UFO in the same directory as the copy
        ufo_link = copy.content_path.parent / file.original_path.name
        if not ufo_link.exists():
            ufo_link.symlink_to(file.original_path.resolve())

        result = ttfcomponentizer.main([str(copy.content_path)])
        if result is not None:
            raise RuntimeError(f"ttfcomponentizer failed with exit code {result}")
        return copy
