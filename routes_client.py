# -*- coding: utf-8 -*-
"""
İstemci API — EXE tarafından kullanılan endpoint'ler.
/api/aktive-et ve /api/kontrol
"""

import datetime
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import Lisans, db
from helpers import log_yaz, ip_banlimi
from database import SECRET_KEY

router = APIRouter()


def app_sirri_dogrula(request: Request):
    gelen = request.headers.get("x-app-secret") or request.headers.get("x_app_secret") or ""
    if gelen != SECRET_KEY:
        raise HTTPException(status_code=403, detail="Yetkisiz erisim.")


class AktivasoyonIstek(BaseModel):
    hwid: str
    lisans_kodu: str

class KontrolIstek(BaseModel):
    hwid: str
    lisans_kodu: str


@router.post("/api/aktive-et", dependencies=[Depends(app_sirri_dogrula)])
def aktive_et(istek: AktivasoyonIstek, request: Request, s: Session = Depends(db)):
    ip = request.client.host
    if ip_banlimi(s, ip): raise HTTPException(status_code=403, detail="Bu IP adresi yasaklanmıştır.")
    kod = istek.lisans_kodu.strip().upper()
    hwid = istek.hwid.strip()

    lisans = s.query(Lisans).filter_by(lisans_kodu=kod).first()
    if not lisans: raise HTTPException(status_code=404, detail="Lisans kodu bulunamadı.")
    if not lisans.aktif: raise HTTPException(status_code=403, detail="Bu lisans iptal edilmiştir.")
    if lisans.bitis_tarihi and datetime.datetime.utcnow() > lisans.bitis_tarihi: raise HTTPException(status_code=403, detail="Lisans süresi dolmuştur.")
    if lisans.hwid and lisans.hwid != hwid: raise HTTPException(status_code=403, detail="Bu lisans başka bilgisayara kayıtlı.")

    if not lisans.hwid:
        lisans.hwid = hwid
        lisans.aktivasyon_tar = datetime.datetime.utcnow()
    lisans.son_checkin = datetime.datetime.utcnow()
    s.commit()
    log_yaz(s, "aktivasyon", kod, hwid, ip, "Basarili aktivasyon")
    return {"basarili": True, "mesaj": f"Hoş geldiniz, {lisans.musteri_adi}!", "tur": lisans.tur, "bitis_tarihi": lisans.bitis_tarihi.isoformat() if lisans.bitis_tarihi else None, "musteri_adi": lisans.musteri_adi}


@router.post("/api/kontrol", dependencies=[Depends(app_sirri_dogrula)])
def kontrol(istek: KontrolIstek, request: Request, s: Session = Depends(db)):
    ip = request.client.host
    if ip_banlimi(s, ip): return {"gecerli": False, "mesaj": "Yasaklı IP."}
    kod = istek.lisans_kodu.strip().upper()
    hwid = istek.hwid.strip()
    lisans = s.query(Lisans).filter_by(lisans_kodu=kod).first()
    if not lisans or not lisans.aktif: return {"gecerli": False, "mesaj": "Lisans geçersiz."}
    if lisans.hwid != hwid: return {"gecerli": False, "mesaj": "HWID uyuşmazlığı."}
    if lisans.bitis_tarihi and datetime.datetime.utcnow() > lisans.bitis_tarihi: return {"gecerli": False, "mesaj": "Süre dolmuştur."}
    lisans.son_checkin = datetime.datetime.utcnow()
    s.commit()
    return {"gecerli": True, "tur": lisans.tur, "bitis_tarihi": lisans.bitis_tarihi.isoformat() if lisans.bitis_tarihi else None, "musteri_adi": lisans.musteri_adi}
