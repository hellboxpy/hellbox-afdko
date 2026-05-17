from fontTools.ttLib import TTFont
from hellbox.jobs.afdko.make_otf import MakeOTF


def test_make_otf_produces_valid_otf(ufo_path, tmp_path):
    from hellbox.source_file import SourceFile

    file = SourceFile(ufo_path, ufo_path, tmp_path)

    chute = MakeOTF()
    result = chute.process(file)

    assert result.content_path.exists()
    assert result.content_path.suffix == ".otf"
    font = TTFont(str(result.content_path))
    assert "CFF " in font


def test_make_otf_release_mode(ufo_path, tmp_path):
    from hellbox.source_file import SourceFile

    file = SourceFile(ufo_path, ufo_path, tmp_path)

    chute = MakeOTF(release=True, omit_mac_names=True)
    result = chute.process(file)

    assert result.content_path.exists()
    font = TTFont(str(result.content_path))
    assert "CFF " in font
