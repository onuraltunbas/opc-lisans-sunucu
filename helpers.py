# -*- coding: utf-8 -*-
"""
Yardımcı fonksiyonlar: hash, lisans kodu, tarih hesaplama,
session yönetimi, log yazma, Telegram bildirimi.
"""

import os
import datetime
import hashlib
import secrets
import urllib.request
import urllib.parse
import json
from typing import Optional

from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from database import (
    Session_, Log, PanelLog, Ayarlar, UyelikTuru,
    PanelKullanici, PANEL_KULLANICI, PANEL_SIFRE,
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
)


# =====================================================================
# EXE YARDIMCI FONKSİYONLARI
# =====================================================================
def get_exe_path() -> Optional[str]:
    """dosyalar/ klasöründeki ilk .exe dosyasının tam yolunu döner.
    Dosya adından bağımsız çalışır; klasöre yeni exe atılsa bile otomatik bulur."""
    folder = "dosyalar"
    try:
        for f in os.listdir(folder):
            if f.lower().endswith(".exe"):
                return os.path.join(folder, f)
    except Exception:
        pass
    return None

def get_exe_hash() -> str:
    exe_path = get_exe_path()
    if not exe_path:
        return ""
    try:
        with open(exe_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return ""

def get_exe_date() -> str:
    exe_path = get_exe_path()
    if not exe_path:
        return ""
    try:
        ts = os.path.getmtime(exe_path)
        return datetime.datetime.fromtimestamp(ts).strftime("%d.%m.%Y")
    except Exception:
        return ""

def is_exe_new() -> bool:
    """EXE dosyası son 24 saat içinde mi güncellendi?"""
    exe_path = get_exe_path()
    if not exe_path:
        return False
    try:
        ts = os.path.getmtime(exe_path)
        diff = datetime.datetime.now() - datetime.datetime.fromtimestamp(ts)
        return diff.total_seconds() < 86400  # 24 saat
    except Exception:
        return False


# =====================================================================
# TELEGRAM
# =====================================================================
def telegram_bildirim_gonder(mesaj: str):
    """Genel sistem bildirimleri için Telegram fonksiyonu"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID: return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = urllib.parse.urlencode({"chat_id": TELEGRAM_CHAT_ID, "text": mesaj, "parse_mode": "HTML"}).encode("utf-8")
        req = urllib.request.Request(url, data=data)
        urllib.request.urlopen(req, timeout=4)
    except Exception:
        pass

def get_ip_konum(ip: str) -> str:
    if ip in ("127.0.0.1", "localhost", "0.0.0.0", "") or ip.startswith("192.168.") or ip.startswith("10."):
        return "Yerel Ağ (LAN/Localhost)"
    try:
        url = f"http://ip-api.com/json/{ip}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=2) as response:
            data = json.loads(response.read().decode())
            if data.get("status") == "success":
                return f"{data.get('city', '?')}, {data.get('country', '?')}"
    except Exception:
        pass
    return "Bilinmeyen Konum"

def istihbarat_raporu(bg_tasks, islem_turu: str, actor: str, detay: str, ip: str):
    """Telegrama asenkron olarak log fırlatır."""
    def gorev():
        if not TELEGRAM_BOT_TOKEN: return
        konum = get_ip_konum(ip)
        zaman = (datetime.datetime.utcnow() + datetime.timedelta(hours=3)).strftime("%d.%m.%Y - %H:%M:%S")

        mesaj = (
            f"🚨 <b>YENİ SİSTEM İŞLEMİ</b> 🚨\n\n"
            f"👤 <b>İşlemi Yapan:</b> {actor}\n"
            f"⚙️ <b>İşlem:</b> {islem_turu}\n"
            f"📄 <b>Detay:</b> {detay}\n\n"
            f"🌐 <b>IP & Konum:</b> {ip} ({konum})\n"
            f"🕒 <b>Tarih:</b> {zaman}"
        )

        chat_ids = []
        if TELEGRAM_CHAT_ID:
            chat_ids.append(TELEGRAM_CHAT_ID)

        s = Session_()
        try:
            users = s.query(PanelKullanici).filter_by(telegram_bildirim_alabilir=True).all()
            for u in users:
                if u.telegram_chat_id and u.telegram_chat_id not in chat_ids:
                    chat_ids.append(u.telegram_chat_id)
        except Exception:
            pass
        finally:
            s.close()

        for cid in chat_ids:
            try:
                url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                data = urllib.parse.urlencode({"chat_id": cid, "text": mesaj, "parse_mode": "HTML"}).encode("utf-8")
                req = urllib.request.Request(url, data=data)
                urllib.request.urlopen(req, timeout=4)
            except Exception:
                pass

    if bg_tasks:
        bg_tasks.add_task(gorev)


# =====================================================================
# YARDIMCI FONKSİYONLAR
# =====================================================================
def sifre_hashle(sifre: str) -> str:
    return hashlib.sha256(sifre.encode()).hexdigest()

def lisans_kodu_uret(tur_prefix="STD"):
    parca = secrets.token_hex(6).upper()
    return f"{tur_prefix}-{parca[:4]}-{parca[4:8]}-{parca[8:12]}"

def bitis_tarihi_hesapla(tur: str, s: Session, saat: Optional[int] = None) -> Optional[datetime.datetime]:
    simdi = datetime.datetime.utcnow()

    if tur == "deneme" and saat:
        return simdi + datetime.timedelta(hours=saat)

    u_tur = s.query(UyelikTuru).filter_by(kod=tur).first()

    if not u_tur:
        if tur == "omur_boyu":
            return None
        if tur == "deneme":
            return simdi + datetime.timedelta(hours=24)
        return simdi + datetime.timedelta(days=30)

    sure = getattr(u_tur, 'sure_gun', 0)

    if sure is None or sure == 0:
        if tur == "deneme":
            return simdi + datetime.timedelta(hours=24)
        return None

    return simdi + datetime.timedelta(days=sure)

def log_yaz(s: Session, islem, lisans_kodu, hwid, ip, mesaj):
    s.add(Log(islem=islem, lisans_kodu=lisans_kodu, hwid=hwid, ip=ip, mesaj=mesaj))
    s.commit()

def panel_log_yaz(s: Session, kullanici_adi: str, islem: str, detay: str = ""):
    s.add(PanelLog(kullanici_adi=kullanici_adi, islem=islem, detay=detay))
    s.commit()

def get_ana_admin_creds(s: Session):
    ayar = s.query(Ayarlar).first()
    if ayar and ayar.admin_kullanici and ayar.admin_sifre_hash:
        return ayar.admin_kullanici, ayar.admin_sifre_hash
    return PANEL_KULLANICI, sifre_hashle(PANEL_SIFRE)

def ip_banlimi(s: Session, ip: str) -> bool:
    from database import IpBan
    ban = s.query(IpBan).filter_by(ip=ip, aktif=True).first()
    return ban is not None


# =====================================================================
# SESSION YÖNETİMİ
# =====================================================================
_sessions = {}

def session_olustur(kullanici_id: str) -> str:
    token = secrets.token_urlsafe(32)
    _sessions[token] = {"kullanici_id": kullanici_id, "tarih": datetime.datetime.utcnow()}
    return token

def session_dogrula(token: str) -> Optional[str]:
    if not token: return None
    s = _sessions.get(token)
    if not s: return None
    if (datetime.datetime.utcnow() - s["tarih"]).days > 7:
        del _sessions[token]
        return None
    return s["kullanici_id"]

def session_sil(token: str):
    _sessions.pop(token, None)

def safe_format_date(dt) -> str:
    if not dt: return "-"
    if isinstance(dt, str): return dt.split(" ")[0].replace("-", ".")
    try: return dt.strftime("%d.%m.%Y")
    except: return str(dt)

def safe_format_datetime(dt) -> str:
    if not dt: return "-"
    if isinstance(dt, str): return dt
    try: return dt.strftime("%d.%m.%Y %H:%M")
    except: return str(dt)

def safe_days_left(dt) -> Optional[int]:
    if not dt: return None
    if isinstance(dt, str):
        try:
            d_obj = datetime.datetime.strptime(dt[:10], "%Y-%m-%d")
            return (d_obj - datetime.datetime.utcnow()).days
        except: return 0
    try:
        return (dt - datetime.datetime.utcnow()).days
    except: return 0

def get_kullanici_id(request: Request) -> Optional[str]:
    token = request.cookies.get("session")
    return session_dogrula(token) if token else None
