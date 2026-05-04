# -*- coding: utf-8 -*-
"""
Veritabanı modelleri, engine, session ve migration.
"""

import os
import uuid
import datetime
import hashlib

from sqlalchemy import (
    create_engine, Column, String, DateTime,
    Boolean, Integer, Text
)
from sqlalchemy.orm import declarative_base, sessionmaker

# =====================================================================
# YAPILANDIRMA
# =====================================================================
SECRET_KEY         = os.getenv("SECRET_KEY", "BURAYA-GIZLI-ANAHTARINIZI-YAZIN")
PANEL_KULLANICI    = os.getenv("PANEL_KULLANICI", "admin")
PANEL_SIFRE        = os.getenv("PANEL_SIFRE", "admin123")
DATABASE_URL       = os.getenv("DATABASE_URL", "sqlite:///./lisanslar.db")
INDIRME_LINKI      = "/api/program-indir"

# TELEGRAM İSTİHBARAT AYARLARI
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID", "")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Offline lisans için gömülü anahtar
_SK_P1 = bytes([0x4f, 0x50, 0x43, 0x5f, 0x47, 0x57, 0x5f, 0x4f])
_SK_P2 = bytes([0x46, 0x46, 0x4c, 0x49, 0x4e, 0x45, 0x5f, 0x4b])
_SK_P3 = hashlib.sha256(b"opcgw_offline_2026_salt_v1").digest()[:16]
OFFLINE_SECRET_KEY = _SK_P1 + _SK_P2 + _SK_P3

# =====================================================================
# VERİTABANI ENGINE
# =====================================================================
_db_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine   = create_engine(DATABASE_URL, connect_args=_db_connect_args)
Session_ = sessionmaker(bind=engine)
Base     = declarative_base()

# =====================================================================
# VERİTABANI MODELLERİ
# =====================================================================
class Lisans(Base):
    __tablename__ = "lisanslar"
    id             = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    lisans_kodu    = Column(String, unique=True, nullable=False, index=True)
    hwid           = Column(String, nullable=True)
    musteri_adi    = Column(String, nullable=False)
    musteri_email  = Column(String, nullable=True)
    tur            = Column(String, nullable=False)
    aktif          = Column(Boolean, default=True)
    olusturma_tar  = Column(DateTime, default=datetime.datetime.utcnow)
    bitis_tarihi   = Column(DateTime, nullable=True)
    notlar         = Column(Text, nullable=True)
    son_checkin    = Column(DateTime, nullable=True)
    aktivasyon_tar = Column(DateTime, nullable=True)
    iptal_nedeni   = Column(Text, nullable=True)
    iptal_tarihi   = Column(DateTime, nullable=True)
    uretilen_tip   = Column(String, default="online")
    istek_kodu_db  = Column(String, nullable=True)
    sure_gun_db    = Column(Integer, nullable=True)

class Log(Base):
    __tablename__ = "loglar"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    tarih       = Column(DateTime, default=datetime.datetime.utcnow)
    islem       = Column(String)
    lisans_kodu = Column(String)
    hwid        = Column(String)
    ip          = Column(String)
    mesaj       = Column(Text)

class Kullanici(Base):
    __tablename__ = "kullanicilar"
    id              = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ad_soyad        = Column(String, nullable=False)
    email           = Column(String, unique=True, nullable=False, index=True)
    sifre_hash      = Column(String, nullable=False)
    email_dogrulandi = Column(Boolean, default=False)
    dogrulama_kodu  = Column(String, nullable=True)
    kayit_tar       = Column(DateTime, default=datetime.datetime.utcnow)
    son_giris       = Column(DateTime, nullable=True)
    son_ip          = Column(String, nullable=True)

class LisansTalep(Base):
    __tablename__ = "lisans_talepler"
    id          = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    kullanici_id = Column(String, nullable=False)
    ad_soyad    = Column(String, nullable=False)
    email       = Column(String, nullable=False)
    tur         = Column(String, nullable=False)
    durum       = Column(String, default="beklemede")
    talep_tar   = Column(DateTime, default=datetime.datetime.utcnow)
    islem_tar   = Column(DateTime, nullable=True)
    ip_adresi   = Column(String, nullable=True)
    admin_notu  = Column(Text, nullable=True)
    talep_tipi  = Column(String, default="online")
    istek_kodu  = Column(String, nullable=True)
    aktivasyon_kodu = Column(String, nullable=True)

class Mesaj(Base):
    __tablename__ = "mesajlar"
    id           = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    kullanici_id = Column(String, nullable=False)
    gonderen     = Column(String, nullable=False)
    icerik       = Column(Text, nullable=False)
    tarih        = Column(DateTime, default=datetime.datetime.utcnow)
    okundu       = Column(Boolean, default=False)

class IpBan(Base):
    __tablename__ = "ip_banlar"
    id        = Column(Integer, primary_key=True, autoincrement=True)
    ip        = Column(String, unique=True, nullable=False, index=True)
    sebep     = Column(Text, nullable=True)
    tarih     = Column(DateTime, default=datetime.datetime.utcnow)
    aktif     = Column(Boolean, default=True)

class UyelikTuru(Base):
    __tablename__ = "uyelik_turleri"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    kod         = Column(String, unique=True, nullable=False)
    ad          = Column(String, nullable=False)
    aciklama    = Column(Text, nullable=True)
    aktif       = Column(Boolean, default=True)
    sira        = Column(Integer, default=0)
    sure_gun    = Column(Integer, default=30)
    prefix      = Column(String, default="STD")
    is_offline  = Column(Boolean, default=False)

class PanelKullanici(Base):
    __tablename__ = "panel_kullanicilari"
    id = Column(Integer, primary_key=True, autoincrement=True)
    kullanici_adi = Column(String, unique=True, nullable=False)
    isim_soyad = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=True)
    sifre_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    yetki_lisans_olustur = Column(Boolean, default=False)
    yetki_lisans_sil = Column(Boolean, default=False)
    yetki_hwid_sifirla = Column(Boolean, default=False)
    yetki_sure_uzat = Column(Boolean, default=False)
    yetki_talep_onayla = Column(Boolean, default=False)
    yetki_kullanici_ekle = Column(Boolean, default=False)
    yetki_mesaj_yaz = Column(Boolean, default=False)
    yetki_ip_ban = Column(Boolean, default=False)
    yetki_uyelik_tur = Column(Boolean, default=False)
    yetki_offline_paket_yonetimi = Column(Boolean, default=False)
    yetki_offline_lisans_uret = Column(Boolean, default=False)
    telegram_chat_id = Column(String, nullable=True)
    telegram_bildirim_alabilir = Column(Boolean, default=False)
    son_giris = Column(DateTime, nullable=True)
    son_cikis = Column(DateTime, nullable=True)

class PanelLog(Base):
    __tablename__ = "panel_loglar"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tarih = Column(DateTime, default=datetime.datetime.utcnow)
    kullanici_adi = Column(String)
    islem = Column(String)
    detay = Column(Text)

class Ayarlar(Base):
    __tablename__ = "ayarlar"
    id = Column(Integer, primary_key=True)
    admin_kullanici = Column(String, nullable=True)
    admin_sifre_hash = Column(String, nullable=True)
    son_exe_hash = Column(String, nullable=True)
    son_surum_tarihi = Column(DateTime, nullable=True)

class OfflineLisansAyarlari(Base):
    __tablename__ = "offline_lisans_ayarlari"
    id = Column(Integer, primary_key=True)
    notlar = Column(Text, nullable=True)

# =====================================================================
# TABLOLARI OLUŞTUR
# =====================================================================
Base.metadata.create_all(engine)

# =====================================================================
# MİGRASYON
# =====================================================================
def _db_migrate():
    """
    PostgreSQL'de tek bir connection içinde bir DDL başarısız olursa
    transaction bozuk kalır; sonraki commit'ler çalışmaz.
    Çözüm: Her ALTER TABLE için bağımsız bir connection kullan.
    PostgreSQL destekliyorsa 'IF NOT EXISTS' sözdizimi kullanılır.
    """
    _is_pg = not DATABASE_URL.startswith("sqlite")
    _ifne  = "IF NOT EXISTS " if _is_pg else ""

    _migrations = [
        f"ALTER TABLE panel_kullanicilari ADD COLUMN {_ifne}yetki_offline_paket_yonetimi BOOLEAN DEFAULT false",
        f"ALTER TABLE panel_kullanicilari ADD COLUMN {_ifne}yetki_offline_lisans_uret BOOLEAN DEFAULT false",
        f"ALTER TABLE uyelik_turleri ADD COLUMN {_ifne}sure_gun INTEGER DEFAULT 30",
        f"ALTER TABLE uyelik_turleri ADD COLUMN {_ifne}prefix VARCHAR(10) DEFAULT 'STD'",
        f"ALTER TABLE uyelik_turleri ADD COLUMN {_ifne}is_offline BOOLEAN DEFAULT false",
        f"ALTER TABLE ayarlar ADD COLUMN {_ifne}son_exe_hash VARCHAR(100)",
        f"ALTER TABLE ayarlar ADD COLUMN {_ifne}son_surum_tarihi TIMESTAMP",
        f"ALTER TABLE lisans_talepler ADD COLUMN {_ifne}talep_tipi VARCHAR(20) DEFAULT 'online'",
        f"ALTER TABLE lisans_talepler ADD COLUMN {_ifne}istek_kodu VARCHAR(100)",
        f"ALTER TABLE lisans_talepler ADD COLUMN {_ifne}aktivasyon_kodu VARCHAR(100)",
        f"ALTER TABLE panel_kullanicilari ADD COLUMN {_ifne}telegram_chat_id VARCHAR(100)",
        f"ALTER TABLE panel_kullanicilari ADD COLUMN {_ifne}telegram_bildirim_alabilir BOOLEAN DEFAULT false",
        f"ALTER TABLE lisanslar ADD COLUMN {_ifne}uretilen_tip VARCHAR(20) DEFAULT 'online'",
        f"ALTER TABLE lisanslar ADD COLUMN {_ifne}istek_kodu_db VARCHAR(100)",
        f"ALTER TABLE lisanslar ADD COLUMN {_ifne}sure_gun_db INTEGER",
    ]

    for sql in _migrations:
        try:
            with engine.connect() as conn:
                conn.execute(__import__("sqlalchemy").text(sql))
                conn.commit()
        except Exception:
            pass  # Kolon zaten varsa (IF NOT EXISTS olmayan DB) devam et

_db_migrate()

# =====================================================================
# VARSAYILAN TÜRLERİ EKLE
# =====================================================================
def varsayilan_turleri_ekle():
    s = Session_()
    try:
        if s.query(UyelikTuru).count() == 0:
            turler = [
                UyelikTuru(kod="aylik", ad="Aylık Lisans", aciklama="30 gün geçerli", sira=1, sure_gun=30, prefix="AYL"),
                UyelikTuru(kod="yillik", ad="Yıllık Lisans", aciklama="365 gün geçerli", sira=2, sure_gun=365, prefix="YIL"),
                UyelikTuru(kod="omur_boyu", ad="Ömür Boyu Lisans", aciklama="Süresiz geçerli", sira=3, sure_gun=0, prefix="OBY"),
                UyelikTuru(kod="deneme", ad="Deneme Sürümü", aciklama="24 saat ücretsiz deneme", sira=4, sure_gun=1, prefix="DEN"),
            ]
            for t in turler: s.add(t)
            s.commit()
    finally: s.close()

varsayilan_turleri_ekle()

# =====================================================================
# DB SESSION DEPENDENCY
# =====================================================================
def db():
    s = Session_()
    try: yield s
    finally: s.close()
