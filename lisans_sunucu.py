# -*- coding: utf-8 -*-

"""
OPC Gateway Lisans Doğrulama Sunucusu v5.0 (İstihbarat Entegreli)
FastAPI + SQLite | Railway deploy

GİRİŞ NOKTASI — sadece app tanımı ve router kayıtları burada.
İş mantığı ayrı modüllerde:
  database.py       — DB modelleri, engine, migration
  helpers.py        — Yardımcı fonksiyonlar, session, Telegram
  auth.py           — Panel kimlik doğrulama, yetki kontrolü
  routes_client.py  — EXE API (aktive-et, kontrol)
  routes_kullanici.py — Kullanıcı API (kayıt, giriş, profil ...)
  routes_panel.py   — Panel API (lisans, talep, mesaj, yetkili ...)
  routes_html.py    — HTML sayfa endpoint'leri
  html_panel.py     — Admin panel HTML
  html_site.py      — Kullanıcı sitesi CSS + HTML Template
"""

import os
import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

# ── Modüller ──────────────────────────────────────────────────────────
from database import Session_, Ayarlar
from helpers import telegram_bildirim_gonder, get_exe_hash, get_exe_date

import routes_client
import routes_kullanici
import routes_panel
import routes_html

# =====================================================================
# FASTAPI UYGULAMASI
# =====================================================================
app = FastAPI(title="OPC Gateway", docs_url=None, redoc_url=None)

# CORS
_cors_origins = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000")
_cors_list = [o.strip() for o in _cors_origins.split(",") if o.strip()]
if len(_cors_list) == 1 and _cors_list[0] == "*":
    _allow_credentials = False
else:
    _allow_credentials = True

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_list,
    allow_credentials=_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================================
# GODOT 4 WEB EXPORT GÜVENLİK BAŞLIKLARI (MIDDLEWARE)
# =====================================================================
@app.middleware("http")
async def add_godot_headers(request: Request, call_next):
    response = await call_next(request)
    # Eğer istek FlappyElectronics oyununa geliyorsa, SharedArrayBuffer izinlerini ver:
    if request.url.path.startswith("/flappyelectronics"):
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    return response

# =====================================================================
# GLOBAL EXCEPTION HANDLER
# =====================================================================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_msg = f"❌ <b>SUNUCU HATASI (CRASH)</b>\n\n<b>Endpoint:</b> {request.url}\n<b>Hata:</b> {str(exc)}"
    telegram_bildirim_gonder(error_msg)
    return JSONResponse(status_code=500, content={"detail": "Sunucu hatası oluştu, yöneticiye bildirildi."})

# =====================================================================
# STARTUP / SHUTDOWN
# =====================================================================
@app.on_event("startup")
async def startup_event():
    telegram_bildirim_gonder("🚀 <b>Deploy Başarılı!</b>\nSunucu ayağa kalktı ve aktif durumda.")

    s = Session_()
    try:
        current_hash = get_exe_hash()
        if current_hash:
            try:
                ayar = s.query(Ayarlar).first()
                if not ayar:
                    ayar = Ayarlar(son_exe_hash=current_hash, son_surum_tarihi=datetime.datetime.utcnow())
                    s.add(ayar)
                    s.commit()
                elif ayar.son_exe_hash != current_hash:
                    ayar.son_exe_hash = current_hash
                    ayar.son_surum_tarihi = datetime.datetime.utcnow()
                    s.commit()
                    telegram_bildirim_gonder(f"🆕 <b>Yeni Program Sürümü Yayınlandı!</b>\n\nOPC Gateway Pro programı güncellendi.\n<b>Tarih:</b> {get_exe_date()}\n<b>Hash:</b> {current_hash[:16]}...")
            except Exception as e:
                s.rollback()
                telegram_bildirim_gonder(f"⚠️ <b>Startup DB Uyarısı</b>\nAyarlar sorgusu başarısız: {str(e)[:200]}")
    finally:
        s.close()


@app.on_event("shutdown")
def shutdown_event():
    telegram_bildirim_gonder("🚧 <b>Sistem Kapanıyor</b>\nSunucu kapatılıyor — yeni deploy başlıyor olabilir.")

# =====================================================================
# STATIC DOSYALAR (/static/logo.png vb.)
# =====================================================================
import pathlib
_static_dir = pathlib.Path(__file__).parent / "static"
_static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")

# =====================================================================
# FLAPPYELECTRONICS OYUN DOSYALARI
# =====================================================================
_flappy_dir = pathlib.Path(__file__).parent / "flappyelectronics"
_flappy_dir.mkdir(exist_ok=True)
# html=True parametresi sayesinde /flappyelectronics yazılınca otomatik index.html açılır
app.mount("/flappyelectronics", StaticFiles(directory=str(_flappy_dir), html=True), name="flappyelectronics")

# =====================================================================
# ROUTER KAYITLARI
# =====================================================================
app.include_router(routes_client.router)
app.include_router(routes_kullanici.router)
app.include_router(routes_panel.router)
app.include_router(routes_html.router)