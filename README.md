# TravelManagement 🧳🚌

یک سیستم مدیریت سفر ساده با امکانات ثبت، مشاهده و رزرو سفر برای کاربران و مدیریت کامل برای ادمین‌ها.

## 📦 امکانات

- ثبت‌نام و ورود کاربران و مدیران
- اضافه‌کردن سفر با انواع وسایل نقلیه (اتوبوس، قطار و غیره)
- رزرو صندلی توسط کاربر
- نمایش لیست سفرها و رزروها
- مدیریت صندلی‌ها و اطلاعات هر سفر
- ذخیره داده‌ها در پایگاه‌داده PostgreSQL


## 💻 پیش نیاز ها

- Python3.1x
- PostgreSQL

## 🛠️ تکنولوژی‌ها

- Python 3.1x
- PostgreSQL
- Psycopg2
- cmd module
- ساختار ماژولار و خوانا

## 🚀 اجرا

### راه‌اندازی محیط مجازی:

```bash
python -m venv .venv
source .venv/bin/activate  # on Linux/macOS
.venv\Scripts\activate.bat     # on Windows
```
### اجرای برنامه:

```bash
cd TravelManagement
pip install -r requirements.txt
vi example.env
mv example.env .env
```
### دستورات اصلی:
```bash
python -m travel register_user
python -m travel login_admin
python -m travel login_admin
```
