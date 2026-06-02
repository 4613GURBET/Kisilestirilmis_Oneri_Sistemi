import json
from src.data.database import SessionLocal, create_tables
from src.data.models import Activity, ActivityCategory, DifficultyLevel

create_tables()
db = SessionLocal()

type_map = {
    'relaxation': ActivityCategory.WELLNESS,
    'education': ActivityCategory.EDUCATIONAL,
    'social': ActivityCategory.SOCIAL,
    'music': ActivityCategory.MUSIC,
    'outdoor': ActivityCategory.OUTDOOR,
    'sports': ActivityCategory.SPORTS,
    'art': ActivityCategory.ART,
    'cooking': ActivityCategory.INDOOR,
}

data = json.load(open('data_processing/activity.json', encoding='utf-8'))

for item in data[:50]:
    category = type_map.get(item['type'].lower(), ActivityCategory.SOCIAL)
    activity = Activity(
        name=item['activity'][:100],
        category=category,
        difficulty=DifficultyLevel.MEDIUM,
        duration=60,
        is_indoor=True,
        min_budget=float(item.get('price', 0)),
    )
    db.add(activity)

db.commit()
db.close()
print('Aktiviteler yuklendi!')