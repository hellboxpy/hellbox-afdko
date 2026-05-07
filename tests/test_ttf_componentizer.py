from fontTools.ttLib import TTFont
from hellbox.jobs.afdko.make_otf import MakeOTF
from hellbox.jobs.afdko.otf2ttf import Otf2Ttf
from hellbox.jobs.afdko.ttf_componentizer import TtfComponentizer


def test_ttfcomponentizer_produces_valid_ttf(ufo_path, tmp_path):
    from hellbox.source_file import SourceFile

    ufo_file = SourceFile(ufo_path, ufo_path, tmp_path)
    otf_file = MakeOTF().process(ufo_file)
    ttf_file = Otf2Ttf().process(otf_file)

    chute = TtfComponentizer()
    result = chute.process(ttf_file)

    assert result.content_path.exists()
    assert result.content_path.suffix == ".ttf"
    font = TTFont(str(result.content_path))
    assert "glyf" in font
