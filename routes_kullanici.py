# -*- coding: utf-8 -*-
"""
Kullanıcı API — Kayıt, giriş, profil, talep, mesaj endpoint'leri.
"""

import datetime
import os
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Request, Response, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session

from database import (
    Kullanici, LisansTalep, Mesaj, Lisans, UyelikTuru, Ayarlar, db
)
from helpers import (
    sifre_hashle, session_olustur, session_sil, session_dogrula,
    get_kullanici_id, safe_format_date, safe_format_datetime,
    safe_days_left, get_exe_hash, get_exe_date, istihbarat_raporu,
    ip_banlimi
)

router = APIRouter()


@router.post("/api/kayit")
async def kayit_ol(request: Request, bg_tasks: BackgroundTasks, s: Session = Depends(db)):
    try:
        data = await request.json()
    except Exception:
        form = await request.form()
        data = dict(form)

    ad_soyad = data.get("ad_soyad", "").strip()
    email = data.get("email", "").strip().lower()
    sifre = data.get("sifre", "")

    if not ad_soyad or not email or not sifre:
        raise HTTPException(status_code=400, detail="Eksik alan.")
    if s.query(Kullanici).filter_by(email=email).first():
        raise HTTPException(status_code=409, detail="Kayıtlı e-posta.")

    k = Kullanici(ad_soyad=ad_soyad, email=email, sifre_hash=sifre_hashle(sifre), email_dogrulandi=True, son_ip=request.client.host)
    s.add(k)
    s.commit()

    istihbarat_raporu(bg_tasks, "Yeni Kullanıcı Kaydı", ad_soyad, f"E-posta: {email}", request.client.host)
    return {"basarili": True, "mesaj": "Kayıt başarılı!"}


@router.post("/api/giris")
async def giris_yap(request: Request, response: Response, bg_tasks: BackgroundTasks, s: Session = Depends(db)):
    try:
        data = await request.json()
    except Exception:
        form = await request.form()
        data = dict(form)

    email = data.get("email", "").strip().lower()
    k = s.query(Kullanici).filter_by(email=email, sifre_hash=sifre_hashle(data.get("sifre", ""))).first()
    if not k:
        raise HTTPException(status_code=401, detail="Yanlış şifre.")

    token = session_olustur(k.id)
    k.son_giris = datetime.datetime.utcnow()
    k.son_ip = request.client.host
    s.commit()

    istihbarat_raporu(bg_tasks, "Müşteri Girişi", k.ad_soyad, f"Müşteri panele giriş yaptı. ({k.email})", request.client.host)

    resp = JSONResponse({"basarili": True, "token": token, "kullanici_id": k.id})
    resp.set_cookie("session", token, httponly=True, max_age=604800, samesite="lax")
    return resp


@router.post("/api/cikis")
def cikis_yap(request: Request, response: Response, bg_tasks: BackgroundTasks):
    token = request.cookies.get("session")
    if token: session_sil(token)
    istihbarat_raporu(bg_tasks, "Müşteri Çıkışı", "Kullanıcı", "Sistemden çıkış yapıldı.", request.client.host)
    resp = JSONResponse({"basarili": True})
    resp.delete_cookie("session")
    return resp


@router.post("/api/talep-olustur")
async def talep_olustur(request: Request, bg_tasks: BackgroundTasks, s: Session = Depends(db)):
    kullanici_id = get_kullanici_id(request)
    if not kullanici_id: raise HTTPException(status_code=401)
    data = await request.json()
    k = s.query(Kullanici).filter_by(id=kullanici_id).first()

    talep_tipi = data.get("talep_tipi", "online")
    istek_kodu = data.get("istek_kodu", "").strip().upper()
    if talep_tipi == "offline":
        if not istek_kodu.startswith("REQ-"):
            raise HTTPException(status_code=400, detail="Geçersiz istek kodu formatı. (REQ- ile başlamalıdır)")
        if s.query(LisansTalep).filter_by(istek_kodu=istek_kodu).first():
            raise HTTPException(status_code=409, detail="Bu istek kodu daha önce kullanılmış.")

    if s.query(LisansTalep).filter_by(kullanici_id=kullanici_id, durum="beklemede").first():
        raise HTTPException(status_code=409, detail="Zaten bekleyen talep var.")

    s.add(LisansTalep(kullanici_id=k.id, ad_soyad=k.ad_soyad, email=k.email, tur=data.get("tur"), ip_adresi=k.son_ip, talep_tipi=talep_tipi, istek_kodu=istek_kodu if talep_tipi=="offline" else None))
    s.commit()
    tip_str = "OFFLINE" if talep_tipi == "offline" else "ONLINE"
    ek_bilgi = f"\nİstek Kodu: {istek_kodu}" if talep_tipi == "offline" else ""
    istihbarat_raporu(bg_tasks, f"YENİ {tip_str} LİSANS TALEBİ", k.ad_soyad, f"Talep Edilen Tür: {data.get('tur')} | E-posta: {k.email}{ek_bilgi}", request.client.host)
    return {"basarili": True}


@router.get("/api/benim-taleplerim")
def benim_taleplerim(request: Request, s: Session = Depends(db)):
    kid = get_kullanici_id(request)
    if not kid: raise HTTPException(status_code=401)
    talepler = s.query(LisansTalep).filter_by(kullanici_id=kid).order_by(LisansTalep.talep_tar.desc()).all()
    return [{"id": t.id, "tur": t.tur, "durum": t.durum, "tarih": safe_format_datetime(t.talep_tar), "admin_notu": t.admin_notu, "talep_tipi": t.talep_tipi, "istek_kodu": t.istek_kodu, "aktivasyon_kodu": t.aktivasyon_kodu} for t in talepler]


@router.post("/api/mesaj-gonder")
async def mesaj_gonder(request: Request, s: Session = Depends(db)):
    kid = get_kullanici_id(request)
    if not kid: raise HTTPException(status_code=401)
    data = await request.json()
    s.add(Mesaj(kullanici_id=kid, gonderen="kullanici", icerik=data.get("icerik", "")))
    s.commit()
    return {"basarili": True}


@router.get("/api/mesajlarim")
def mesajlarim(request: Request, s: Session = Depends(db)):
    kid = get_kullanici_id(request)
    if not kid: raise HTTPException(status_code=401)
    s.query(Mesaj).filter_by(kullanici_id=kid, gonderen="admin", okundu=False).update({"okundu": True})
    s.commit()
    mesajlar = s.query(Mesaj).filter_by(kullanici_id=kid).order_by(Mesaj.tarih.asc()).all()
    return [{"id": m.id, "gonderen": m.gonderen, "icerik": m.icerik, "tarih": safe_format_datetime(m.tarih)} for m in mesajlar]


@router.get("/api/profil")
def profil(request: Request, s: Session = Depends(db)):
    kid = get_kullanici_id(request)
    if not kid: raise HTTPException(status_code=401)
    k = s.query(Kullanici).filter_by(id=kid).first()
    if not k: raise HTTPException(status_code=401)

    lisans = s.query(Lisans).filter_by(musteri_email=k.email).order_by(Lisans.olusturma_tar.desc()).first()
    l_bilgi = None
    if lisans:
        aktif = lisans.aktif
        kalan = safe_days_left(lisans.bitis_tarihi)
        durum = "aktif" if aktif and (kalan is None or kalan >= 0) else "iptal" if not aktif else "suresi_dolmus"
        if kalan is not None and kalan < 0:
            kalan = 0
        l_bilgi = {
            "kod": lisans.lisans_kodu,
            "tur": lisans.tur,
            "bitis": safe_format_date(lisans.bitis_tarihi) if lisans.bitis_tarihi else "Ömür Boyu",
            "kalan_gun": kalan,
            "aktif": aktif,
            "durum": durum
        }
    try:
        _ayar = s.query(Ayarlar).first()
        import datetime as _dt
        _yeni_surum = bool(
            _ayar and _ayar.son_surum_tarihi and
            (_dt.datetime.utcnow() - _ayar.son_surum_tarihi).total_seconds() < 86400
        )
    except Exception:
        _yeni_surum = False

    return {
        "ad_soyad": k.ad_soyad,
        "email": k.email,
        "kayit_tar": safe_format_date(k.kayit_tar),
        "lisans": l_bilgi,
        "indirme_linki": "/api/program-indir" if (l_bilgi and l_bilgi["durum"]=="aktif") else None,
        "vt_hash": get_exe_hash(),
        "son_guncelleme": get_exe_date(),
        "yeni_surum_banner": _yeni_surum
    }


@router.post("/api/lisansimi-iptal-et")
async def lisansimi_iptal_et(request: Request, bg_tasks: BackgroundTasks, s: Session = Depends(db)):
    kid = get_kullanici_id(request)
    if not kid: raise HTTPException(status_code=401, detail="Giriş yapmalısınız.")
    k = s.query(Kullanici).filter_by(id=kid).first()
    if not k: raise HTTPException(status_code=401, detail="Geçersiz kullanıcı.")

    data = await request.json()
    neden = data.get("neden", "Belirtilmedi")

    lisans = s.query(Lisans).filter_by(musteri_email=k.email, aktif=True).order_by(Lisans.olusturma_tar.desc()).first()
    if not lisans:
        raise HTTPException(status_code=404, detail="İptal edilecek aktif lisans bulunamadı.")

    lisans.aktif = False
    lisans.iptal_nedeni = neden
    lisans.iptal_tarihi = datetime.datetime.utcnow()
    s.commit()

    istihbarat_raporu(bg_tasks, "KULLANICI LİSANS İPTALİ", k.ad_soyad, f"Kod: {lisans.lisans_kodu} | Neden: {neden}", request.client.host)

    return {"basarili": True, "mesaj": "Lisansınız iptal edildi."}


@router.get("/api/lisans-gecmisim")
def lisans_gecmisim(request: Request, s: Session = Depends(db)):
    kid = get_kullanici_id(request)
    if not kid: raise HTTPException(status_code=401)
    k = s.query(Kullanici).filter_by(id=kid).first()
    if not k: raise HTTPException(status_code=401)

    lisanslar = s.query(Lisans).filter_by(musteri_email=k.email).order_by(Lisans.olusturma_tar.desc()).all()
    sonuc = []
    for l in lisanslar:
        aktif = l.aktif
        kalan = safe_days_left(l.bitis_tarihi)
        durum = "aktif" if aktif and (kalan is None or kalan >= 0) else "iptal" if not aktif else "suresi_dolmus"
        notlar = l.notlar or ""
        is_offline = notlar == "offline" or notlar.startswith("offline|")
        istek_kodu = notlar.split("|", 1)[1] if "|" in notlar else None
        sonuc.append({
            "kod": l.lisans_kodu,
            "tur": l.tur,
            "durum": durum,
            "olusturma": safe_format_date(l.olusturma_tar),
            "bitis": safe_format_date(l.bitis_tarihi) if l.bitis_tarihi else "Ömür Boyu",
            "aktivasyon": safe_format_date(l.aktivasyon_tar) if l.aktivasyon_tar else None,
            "kalan_gun": kalan,
            "tip": "offline" if is_offline else "online",
            "istek_kodu": istek_kodu
        })
    return sonuc


@router.get("/api/uyelik-turleri-public")
def uyelik_turleri_public(s: Session = Depends(db)):
    return [{"kod": t.kod, "ad": t.ad, "aciklama": t.aciklama, "is_offline": getattr(t, 'is_offline', False)} for t in s.query(UyelikTuru).filter_by(aktif=True).order_by(UyelikTuru.sira).all()]


@router.get("/api/program-indir")
def program_indir(request: Request):
    kid = get_kullanici_id(request)
    if not kid: raise HTTPException(status_code=401, detail="Lütfen önce giriş yapın.")

    exe_path = os.path.join("dosyalar", "OPC_Gateway_Pro.exe")
    if not os.path.exists(exe_path):
        raise HTTPException(status_code=404, detail="Program dosyası sunucuda bulunamadı.")
    return FileResponse(exe_path, media_type="application/vnd.microsoft.portable-executable", filename="OPC_Gateway_Pro.exe")


@router.get("/api/public-info")
def public_info(request: Request):
    kid = get_kullanici_id(request)
    if not kid: raise HTTPException(status_code=401)

    exe_path = os.path.join("dosyalar", "OPC_Gateway_Pro.exe")
    return {
        "indirme_linki": "/api/program-indir" if os.path.exists(exe_path) else None,
        "vt_hash": get_exe_hash(),
        "son_guncelleme": get_exe_date()
    }


@router.post("/api/sifre-degistir")
async def sifre_degistir(request: Request, s: Session = Depends(db)):
    kid = get_kullanici_id(request)
    if not kid: raise HTTPException(status_code=401, detail="Giriş yapmalısınız.")
    data = await request.json()
    yeni_sifre = data.get("yeni_sifre", "").strip()
    if not yeni_sifre or len(yeni_sifre) < 6:
        raise HTTPException(status_code=400, detail="Şifre en az 6 karakter olmalıdır.")
    k = s.query(Kullanici).filter_by(id=kid).first()
    if not k: raise HTTPException(status_code=401)
    k.sifre_hash = sifre_hashle(yeni_sifre)
    s.commit()
    return {"basarili": True, "mesaj": "Şifre başarıyla güncellendi."}
