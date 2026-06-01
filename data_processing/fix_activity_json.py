from pathlib import Path

INPUT_FILE = Path(__file__).resolve().parent / "activity.json"
MARKER = "=======\n["


def fix_json_file() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Dosya bulunamadı: {INPUT_FILE}")

    content = INPUT_FILE.read_text(encoding="utf-8")
    marker_index = content.find(MARKER)
    if marker_index < 0:
        raise ValueError("Dosyada otomatik düzeltme için beklenen çakışma işareti bulunamadı.")

    corrected = content[:marker_index] + "]\n"
    INPUT_FILE.write_text(corrected, encoding="utf-8")
    print(f"Düzeltildi: {INPUT_FILE}")


if __name__ == "__main__":
    fix_json_file()
