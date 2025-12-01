from pathlib import Path
import shutil

from automation_toolkit.file_organizer import FileOrganizer


def test_file_organizer_creates_target_dirs(tmp_path: Path) -> None:
    # Arrange: create dummy files
    img = tmp_path / "photo.jpg"
    doc = tmp_path / "report.pdf"
    img.write_bytes(b"fake")
    doc.write_bytes(b"fake")

    organizer = FileOrganizer(tmp_path)

    # Act
    organizer.organize()

    # Assert
    assert (tmp_path / "images" / "photo.jpg").exists()
    assert (tmp_path / "documents" / "report.pdf").exists()
