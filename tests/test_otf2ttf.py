from fontTools.ttLib import TTFont
from hellbox.jobs.afdko.make_otf import MakeOTF
from hellbox.jobs.afdko.otf2ttf import Otf2Ttf


def test_otf2ttf_produces_valid_ttf(ufo_path, tmp_path):
    from hellbox.source_file import SourceFile

    # Build OTF first, then convert
    ufo_file = SourceFile(ufo_path, ufo_path, tmp_path)
    otf_file = MakeOTF().process(ufo_file)

    chute = Otf2Ttf()
    result = chute.process(otf_file)

    assert result.content_path.exists()
    assert result.content_path.suffix == ".ttf"
    font = TTFont(str(result.content_path))
    assert "glyf" in font
    assert "CFF " not in font
