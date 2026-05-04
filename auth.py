# -*- coding: utf-8 -*-
"""
Panel (Admin) kimlik doğrulama ve yetki kontrol mekanizmaları.
"""

from fastapi import HTTPException, Request, Depends
from sqlalchemy.orm import Session

from database import PanelKullanici, db
from helpers import get_ana_admin_creds, sifre_hashle


class PanelUserDto:
    def __init__(self, kadi, is_admin, yetkiler, isim_soyad=None):
        self.kullanici_adi = kadi
        self.is_admin = is_admin
        self.yetkiler = yetkiler
        self.isim_soyad = isim_soyad
        self.tam_isim = f"{isim_soyad or kadi} ({kadi})"


def panel_dogrula(request: Request, s: Session = Depends(db)):
    auth = request.headers.get("authorization") or request.headers.get("Authorization") or ""
    if auth.startswith("Bearer "):
        token = auth[7:]
        parts = token.split(":", 1)
        if len(parts) == 2:
            kadi = parts[0]
            sifre = parts[1]
            kadi_gercek, sifre_hash_gercek = get_ana_admin_creds(s)

            if kadi == kadi_gercek and sifre_hashle(sifre) == sifre_hash_gercek:
                return PanelUserDto(kadi, True, {}, isim_soyad="Ana Admin")

            pk = s.query(PanelKullanici).filter_by(kullanici_adi=kadi, sifre_hash=sifre_hashle(sifre)).first()
            if pk:
                yetkiler = {
                    "lisans_olustur": pk.yetki_lisans_olustur,
                    "lisans_sil": pk.yetki_lisans_sil,
                    "hwid_sifirla": pk.yetki_hwid_sifirla,
                    "sure_uzat": pk.yetki_sure_uzat,
                    "talep_onayla": pk.yetki_talep_onayla,
                    "kullanici_ekle": pk.yetki_kullanici_ekle,
                    "mesaj_yaz": pk.yetki_mesaj_yaz,
                    "ip_ban": pk.yetki_ip_ban,
                    "uyelik_tur": pk.yetki_uyelik_tur,
                    "offline_paket_yonetimi": pk.yetki_offline_paket_yonetimi,
                    "offline_lisans_uret": pk.yetki_offline_lisans_uret,
                }
                return PanelUserDto(kadi, pk.is_admin, yetkiler, isim_soyad=pk.isim_soyad)
    raise HTTPException(status_code=401, detail="Panel kullanici adi veya sifresi yanlis.")


def yetki_kontrol(istenen_yetki: str):
    def checker(user: PanelUserDto = Depends(panel_dogrula)):
        if user.is_admin: return user
        if not user.yetkiler.get(istenen_yetki, False):
            raise HTTPException(status_code=403, detail="Bu işlem için yetkiniz bulunmamaktadır.")
        return user
    return checker
