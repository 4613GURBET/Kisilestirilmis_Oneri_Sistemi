import json
from pathlib import Path

INPUT_FILE = Path(__file__).with_name("activity.json")
OUTPUT_FILE = Path(__file__).with_name("activity_cleaned.json")


def normalize_record(record: dict) -> dict:
    cleaned = {
        "activity": str(record.get("activity", "")),
        "type": str(record.get("type", "")),
        "participants": int(record.get("participants", 0)),
    }

    return cleaned


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Veri dosyası bulunamadı: {INPUT_FILE}")

    with INPUT_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Beklenen veri formatı bir liste olmalıdır.")

    cleaned_data = [normalize_record(item) for item in data]

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

    print(f"Temizlenmiş veriler kaydedildi: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
