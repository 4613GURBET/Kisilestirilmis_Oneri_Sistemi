 AI Destekli Akıllı Günlük Aktivite Planlayıcı ve Hobi Öneri Sistemi

## 📋 İçindekiler

- [Proje Hakkında]
- [Özellikler]
- [Mimari]
- [Tasarım Desenleri]
- [Klasör Yapısı]
- [Veritabanı Şeması]
- [Kurulum]
- [Ortam Değişkenleri]
- [Testler]
- [API Dokümantasyonu]
- [Branch Stratejisi]
- [Ekip]
- [Teknoloji Yığını]

---

## 📖 Proje Hakkında

Günümüzde pek çok kişi günlük zamanını verimli planlamakta ve boş zamanlarını değerlendirecek uygun aktiviteler bulmakta zorlanmaktadır. Klasik yapılacaklar listesi uygulamaları yalnızca görev takibi yaparken bu sistem bir adım öteye geçerek kullanıcıyı tanır ve önerir.

Bu proje:

- 🎯 Kullanıcı profilini analiz ederek **kişiselleştirilmiş** günlük plan oluşturur
- 🤖 Yapay zeka API'si ile **akıllı aktivite önerileri** sunar
- 🌱 Kullanıcıların **yeni hobiler keşfetmesine** yardımcı olur
- 📅 Boş zamanları değerlendirerek **zaman yönetimini** kolaylaştırır

---

## ✨ Özellikler

| Özellik | Açıklama | Durum |
|---------|----------|-------|
| 👤 Kullanıcı Kaydı & Girişi | Profil oluşturma, tercih belirleme | 🔄 Geliştiriliyor |
| 📝 Profil Formu | İlgi alanları, boş zaman, hedefler | 🔄 Geliştiriliyor |
| 🤖 AI Öneri Motoru | Kişiselleştirilmiş aktivite & hobi önerileri | 🔄 Geliştiriliyor |
| 📅 Günlük Plan Görünümü | Takvim / timeline arayüzü | 🔄 Geliştiriliyor |
| 🌐 AI API Entegrasyonu | OpenAI / Gemini ile içerik üretimi | 🔄 Geliştiriliyor |
| 📱 Responsive Tasarım | Mobil uyumlu arayüz | 🔄 Geliştiriliyor |

---

## 🏗️ Mimari

Proje **3-Katmanlı Mimari (3-Tier Architecture)** üzerine inşa edilmiştir. Her katman yalnızca bir alt/üst katmanla iletişim kurar; katmanlar arası doğrudan bağımlılık yoktur.

```
╔══════════════════════════════════════════════════════════════════╗
║                      KULLANICI (Tarayıcı)                       ║
║                   HTTP İstek / HTML Yanıt                        ║
╚══════════════════════╦═══════════════════════════════════════════╝
                       │
╔══════════════════════▼═══════════════════════════════════════════╗
║           🖥️  SUNUM KATMANI  (Presentation Layer)                ║
║                   — Lizge Maral Çalışkan —                       ║
║                                                                  ║
║   ┌─────────────┐  ┌──────────────┐  ┌──────────────────────┐  ║
║   │  routes.py  │  │  templates/  │  │  static/ (CSS, JS)   │  ║
║   │ Flask Route │  │  Jinja2 HTML │  │  Bootstrap/Tailwind  │  ║
║   └─────────────┘  └──────────────┘  └──────────────────────┘  ║
║                                                                  ║
║  Sorumluluk : HTTP routing, form doğrulama, şablon render       ║
║  Kural      : Sadece Business servislerini çağırır              ║
╚══════════════════════╦═══════════════════════════════════════════╝
                       │  Servis Çağrıları
╔══════════════════════▼═══════════════════════════════════════════╗
║          ⚙️  İŞ MANTIĞI KATMANI  (Business Logic Layer)          ║
║                    — Tayyar Efe İnce —                           ║
║                                                                  ║
║  ┌─────────────────┐  ┌──────────────────┐  ┌───────────────┐  ║
║  │ activity_service│  │recommendation_   │  │  ai_client    │  ║
║  │  İş Kuralları   │  │    engine        │  │ OpenAI/Gemini │  ║
║  └─────────────────┘  └──────────────────┘  └───────────────┘  ║
║                                                                  ║
║  ┌──────────────────────────────────────────────────────────┐   ║
║  │           Strategy Pattern — Öneri Algoritmaları         │   ║
║  │   ┌─────────────┐  ┌─────────────┐  ┌───────────────┐   │   ║
║  │   │ KNNStrategy │  │  CFStrategy │  │ContentStrategy│   │   ║
║  │   └─────────────┘  └─────────────┘  └───────────────┘   │   ║
║  └──────────────────────────────────────────────────────────┘   ║
║                                                                  ║
║  Sorumluluk : İş kuralları, ML modeli, AI API iletişimi         ║
║  Kural      : Sadece Repository'leri kullanır                   ║
╚══════════════════════╦═══════════════════════════════════════════╝
                       │  Repository Çağrıları
╔══════════════════════▼═══════════════════════════════════════════╗
║           🗄️  VERİ ERİŞİM KATMANI  (Data Access Layer)           ║
║                      — Gurbet Fidan —                            ║
║                                                                  ║
║  ┌──────────────────────────────────────────────────────────┐   ║
║  │                   Repository Pattern                      │   ║
║  │  ┌──────────────┐  ┌──────────────────┐  ┌───────────┐  │   ║
║  │  │UserRepository│  │ActivityRepository│  │HobbyRepo. │  │   ║
║  │  └──────┬───────┘  └────────┬─────────┘  └─────┬─────┘  │   ║
║  │         └───────────────────┼──────────────────┘        │   ║
║  │                   BaseRepository (Abstract)              │   ║
║  └─────────────────────────────┬────────────────────────────┘   ║
║                                │  SQLAlchemy ORM (Ham SQL Yok!) ║
║  ┌─────────────────────────────▼────────────────────────────┐   ║
║  │               ORM Modelleri  (models.py)                  │   ║
║  │   User · Activity · Hobby · UserPreference · DailyPlan   │   ║
║  └─────────────────────────────┬────────────────────────────┘   ║
║                                │  Alembic Migrations            ║
╚════════════════════════════════╬═════════════════════════════════╝
                                 │
                       ┌─────────▼──────────┐
                       │   🐘  PostgreSQL    │
                       │     Veritabanı      │
                       └────────────────────┘
```

### 🔄 Veri Akışı — Örnek: Kullanıcı Öneri İstedi

```
1. Kullanıcı "Öneri Al" butonuna tıklar
        │
        ▼
2. [Sunum]   routes.py → POST /recommendations isteğini alır
             Form verisi doğrulanır
        │
        ▼
3. [Business] activity_service.get_recommendations(user_id)
              RecommendationEngine.recommend(user_profile)
              AI API'ye istek gönderilir → açıklama metni üretilir
        │
        ▼
4. [Data]    UserRepository.find_by_id(user_id)
             ActivityRepository.filter_by_preferences(prefs)
             SQLAlchemy ORM sorgusu çalışır
        │
        ▼
5. [DB]      PostgreSQL'den veri döner
        │
        ▼
6. [Sunum]   Öneri listesi HTML'e render edilir → Kullanıcıya gösterilir
```

---

## 🧩 Kullanılan Tasarım Desenleri

### 1. Repository Pattern — Veri Katmanı

```
Business Katmanı
       │
       ▼
IActivityRepository  (Abstract / Arayüz)
       │
  ┌────┴────────────────────┐
  │                         │
ActivityRepository     MockActivityRepository
(PostgreSQL — Prod)    (In-memory — Test)
```

Business katmanı hangi veritabanının kullanıldığını bilmez; Repository arayüzüne bağımlıdır. Bu sayede testlerde gerçek veritabanına ihtiyaç duyulmaz.

### 2. Strategy Pattern — Öneri Algoritmaları

```
RecommendationEngine
       │
       ▼
IRecommendationStrategy   ◄── Çalışma zamanında seçilir
       │
  ┌────┴──────────────────────────┐
  │              │                │
KNNStrategy   CFStrategy    ContentStrategy
(K-En Yakın)  (İşbirlikçi)  (İçerik Filtrele)
```

Yeni bir algoritma eklemek için sadece yeni bir strateji sınıfı yazılır; mevcut kod değişmez.

---

## 📁 Klasör Yapısı

```
activity-planner/
│
├── app.py                          ← Uygulama giriş noktası
├── config.py                       ← Yapılandırma (.env'den okur)
├── requirements.txt
├── .env.example                    ← Örnek ortam değişkenleri
├── .gitignore
├── README.md
├── CONTRIBUTING.md
│
├── src/
│   ├── presentation/               ← Sunum Katmanı (Lizge)
│   │   ├── __init__.py
│   │   ├── routes.py               ← Flask route tanımları
│   │   ├── templates/
│   │   │   ├── base.html           ← Ana şablon (navbar, footer)
│   │   │   ├── index.html          ← Ana sayfa
│   │   │   ├── profile.html        ← Kullanıcı profil formu
│   │   │   ├── recommendations.html← Öneri listesi
│   │   │   └── daily_plan.html     ← Günlük plan takvimi
│   │   └── static/
│   │       ├── css/style.css
│   │       └── js/main.js
│   │
│   ├── business/                   ← İş Mantığı Katmanı (Efe)
│   │   ├── __init__.py
│   │   ├── activity_service.py     ← Aktivite iş kuralları
│   │   ├── user_service.py         ← Kullanıcı iş kuralları
│   │   ├── recommendation_engine.py← ML öneri motoru
│   │   └── ai_client.py            ← OpenAI/Gemini wrapper
│   │
│   └── data/                       ← Veri Erişim Katmanı (Gurbet)
│       ├── __init__.py
│       ├── models.py               ← SQLAlchemy ORM modelleri
│       ├── base_repository.py      ← Abstract Repository arayüzü
│       ├── user_repository.py
│       ├── activity_repository.py
│       ├── hobby_repository.py
│       └── migrations/             ← Alembic migration dosyaları
│
├── tests/
│   ├── __init__.py
│   ├── test_repositories.py        ← Repository CRUD testleri
│   ├── test_activity_service.py    ← İş kuralı testleri
│   ├── test_recommendation.py      ← Öneri motoru testleri
│   └── test_routes.py              ← Route & form testleri
│
├── data_processing/                ← Veri İşleme (Gurbet)
│   ├── clean_dataset.py            ← Temizleme scripti
│   └── eda.ipynb                   ← Keşifsel veri analizi
│
└── docs/
    ├── architecture.png
    └── er_diagram.png
```

---

## 🗃️ Veritabanı Şeması

```
┌──────────────────┐          ┌─────────────────────────┐
│      users       │          │    user_preferences      │
├──────────────────┤          ├─────────────────────────┤
│ id           PK  │◄──1───N──│ id                  PK  │
│ username         │          │ user_id             FK  │
│ email            │          │ interest_area            │
│ password_hash    │          │ free_time_hours          │
│ created_at       │          │ preferred_time_of_day    │
└────────┬─────────┘          └─────────────────────────┘
         │
         │ 1
         │
         ▼ N
┌──────────────────┐          ┌─────────────────────────┐
│   daily_plans    │          │       activities         │
├──────────────────┤          ├─────────────────────────┤
│ id           PK  │◄──1───N──│ id                  PK  │
│ user_id      FK  │          │ daily_plan_id       FK  │
│ plan_date        │          │ title                    │
│ created_at       │          │ description              │
└──────────────────┘          │ duration_minutes         │
                              │ category                 │
                              │ difficulty_level         │
                              └─────────────────────────┘

┌──────────────────┐          ┌─────────────────────────┐
│     hobbies      │   N:N    │      user_hobbies        │
├──────────────────┤          ├─────────────────────────┤
│ id           PK  │◄─────────│ user_id             FK  │
│ name             │          │ hobby_id            FK  │
│ category         │          │ interest_level (1-5)    │
│ description      │          │ started_at               │
└──────────────────┘          └─────────────────────────┘
```

---

## 🚀 Kurulum

### Gereksinimler

- Python 3.10+
- PostgreSQL 15+
- pip

### 1. Repoyu Klonla

```bash
git clone https://github.com/KULLANICI_ADI/activity-planner.git
cd activity-planner
```

### 2. Sanal Ortam Oluştur

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

### 4. Ortam Değişkenlerini Ayarla

```bash
cp .env.example .env
# .env dosyasını açıp değerleri gir
```

### 5. Veritabanını Hazırla

```bash
createdb activity_planner
alembic upgrade head
```

### 6. Uygulamayı Başlat

```bash
python app.py
```

Uygulama `http://localhost:5000` adresinde çalışacaktır.

---

## ⚙️ Ortam Değişkenleri

`.env.example` dosyasını kopyalayıp `.env` olarak düzenle:

```env
# Veritabanı
DATABASE_URL=postgresql://kullanici:sifre@localhost:5432/activity_planner

# AI API (birini kullan)
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...

# Flask
FLASK_SECRET_KEY=guclu-ve-rastgele-bir-anahtar
FLASK_ENV=development
```

> ⚠️ `.env` dosyası `.gitignore`'a eklenmiştir. Asla commit etme!

---

## 🧪 Testleri Çalıştırma

```bash
# Tüm testleri çalıştır
pytest tests/ -v

# Tek modül
pytest tests/test_repositories.py -v

# Kapsam raporu
pytest tests/ --cov=src --cov-report=term-missing
```

---

## 🌐 API Dokümantasyonu

| Metot | Endpoint | Açıklama |
|-------|----------|----------|
| GET | `/` | Ana sayfa |
| GET / POST | `/register` | Kullanıcı kaydı |
| GET / POST | `/login` | Giriş |
| GET | `/logout` | Çıkış |
| GET / POST | `/profile` | Profil görüntüleme / güncelleme |
| GET | `/recommendations` | Kişiselleştirilmiş öneriler |
| POST | `/recommendations/generate` | Yeni öneri üret (AI) |
| GET | `/plan` | Günlük plan görüntüle |
| POST | `/plan/add` | Plana aktivite ekle |

---

## 🌿 Branch Stratejisi

```
main ──────────────────────────────────────────────► (her zaman yayına hazır)
  │
  ├── feature/data-cleaning          (Gurbet)
  ├── feature/orm-models             (Gurbet)
  ├── feature/repositories           (Gurbet)
  │
  ├── feature/ml-model               (Efe)
  ├── feature/recommendation-engine  (Efe)
  ├── feature/ai-api-integration     (Efe)
  │
  ├── feature/ui-home                (Lizge)
  ├── feature/ui-user-form           (Lizge)
  ├── feature/ui-recommendations     (Lizge)
  └── feature/ui-daily-plan          (Lizge)
```

- `main` → Doğrudan push yasak, her zaman PR üzerinden merge
- Her özellik `main`'den dallanır
- PR için en az 1 takım üyesi onayı zorunludur

Detaylar için → [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 👥 Ekip

| İsim | Rol | Sorumluluklar | Branch'ler |
|------|-----|---------------|------------|
| **Gurbet Fidan** | Veri & Backend | Veri temizleme, ORM, Repository Pattern, Migration | `feature/data-cleaning` `feature/orm-models` `feature/repositories` |
| **Tayyar Efe İnce** | ML & İş Mantığı | Model eğitimi, Öneri motoru, AI API, Strategy Pattern | `feature/ml-model` `feature/recommendation-engine` `feature/ai-api-integration` |
| **Lizge Maral Çalışkan** | Frontend | Sunum katmanı, Arayüz, Responsive tasarım, Route testleri | `feature/ui-home` `feature/ui-user-form` `feature/ui-recommendations` |

---

## 📦 Teknoloji Yığını

| Katman | Teknoloji | Sürüm | Amaç |
|--------|-----------|-------|------|
| Web Framework | Flask | 3.x | HTTP routing, şablon render |
| ORM | SQLAlchemy | 2.x | Veritabanı soyutlama |
| Migration | Alembic | 1.13+ | Şema versiyonlama |
| Veritabanı | PostgreSQL | 15+ | Ana veri deposu |
| ML | Scikit-learn | 1.4+ | Öneri modeli eğitimi |
| Veri İşleme | Pandas / NumPy | 2.x | Temizleme & analiz |
| AI API | OpenAI / Gemini | latest | İçerik üretimi |
| Test | pytest | 8.x | Unit testler |
| Mock | unittest.mock | stdlib | Test izolasyonu |
| Proje Yönetimi | Jira Kanban | — | Görev takibi |
| Versiyon Kontrolü | Git + GitHub | — | Kod yönetimi |

---
