# -*- coding: utf-8 -*-
"""
Panel (Admin) API Route'ları — Lisans, kullanici, talep, mesaj, log, yetkili yönetimi.
"""

import datetime
import hmac
import hashlib
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import (
    Lisans, LisansTalep, Kullanici, Mesaj, IpBan,
    UyelikTuru, PanelKullanici, PanelLog, Ayarlar, Log,
    Session_, db, OFFLINE_SECRET_KEY, PANEL_KULLANICI
)
from helpers import (
    sifre_hashle, lisans_kodu_uret, bitis_tarihi_hesapla,
    log_yaz, panel_log_yaz, get_ana_admin_creds,
    safe_format_datetime, istihbarat_raporu
)
from auth import PanelUserDto, panel_dogrula, yetki_kontrol

router = APIRouter()

class LisansOlusturIstek(BaseModel):
    musteri_adi: str
    musteri_email: Optional[str] = None
    tur: str
    deneme_saat: Optional[int] = 24
    ozel_gun: Optional[int] = None
    notlar: Optional[str] = None

@router.post("/panel/lisans-olustur")
def lisans_olustur(istek: LisansOlusturIstek, request: Request, bg_tasks: BackgroundTasks, user: PanelUserDto = Depends(yetki_kontrol("lisans_olustur")), s: Session = Depends(db)):
    u_tur = s.query(UyelikTuru).filter_by(kod=istek.tur).first()
    prefix = u_tur.prefix if u_tur and hasattr(u_tur, 'prefix') and u_tur.prefix else "STD"
    kod = lisans_kodu_uret(prefix)
    
    if istek.ozel_gun is not None:
        if istek.ozel_gun == 0:
            bitis = None
        else:
            bitis = datetime.datetime.utcnow() + datetime.timedelta(days=istek.ozel_gun)
    else:
        bitis = bitis_tarihi_hesapla(istek.tur, s, istek.deneme_saat)
        
    s.add(Lisans(lisans_kodu=kod, musteri_adi=istek.musteri_adi, musteri_email=istek.musteri_email, tur=istek.tur, bitis_tarihi=bitis, notlar=istek.notlar))
    s.commit()
    istihbarat_raporu(bg_tasks, "Online Lisans Üretildi", user.tam_isim, f"Müşteri: {istek.musteri_adi}\nTür: {istek.tur}\nKod: {kod}", request.client.host)
    return {"lisans_kodu": kod, "bitis_tarihi": bitis.isoformat() if bitis else "Ömür boyu", "mesaj": f"Lisans oluşturuldu: {kod}"}

@router.post("/panel/iptal")
def iptal_et(lisans_kodu: str, request: Request, bg_tasks: BackgroundTasks, user: PanelUserDto = Depends(yetki_kontrol("lisans_sil")), s: Session = Depends(db)):
    lisans = s.query(Lisans).filter_by(lisans_kodu=lisans_kodu.upper()).first()
    lisans.aktif = False
    s.commit()
    istihbarat_raporu(bg_tasks, "Lisans İptal Edildi", user.tam_isim, f"İptal Edilen Kod: {lisans_kodu}", request.client.host)
    return {"mesaj": f"{lisans_kodu} lisansı iptal edildi."}

@router.delete("/panel/lisans-sil/{lisans_kodu}")
def lisans_sil(lisans_kodu: str, request: Request, bg_tasks: BackgroundTasks, user: PanelUserDto = Depends(yetki_kontrol("lisans_sil")), s: Session = Depends(db)):
    lisans = s.query(Lisans).filter_by(lisans_kodu=lisans_kodu.upper()).first()
    s.delete(lisans)
    s.commit()
    istihbarat_raporu(bg_tasks, "Lisans KALICI OLARAK Silindi", user.tam_isim, f"Silinen Kod: {lisans_kodu}", request.client.host)
    return {"mesaj": f"{lisans_kodu} silindi."}

@router.post("/panel/hwid-sifirla")
def hwid_sifirla(lisans_kodu: str, request: Request, bg_tasks: BackgroundTasks, user: PanelUserDto = Depends(yetki_kontrol("hwid_sifirla")), s: Session = Depends(db)):
    lisans = s.query(Lisans).filter_by(lisans_kodu=lisans_kodu.upper()).first()
    lisans.hwid = None
    lisans.aktivasyon_tar = None
    s.commit()
    istihbarat_raporu(bg_tasks, "HWID Sıfırlandı", user.tam_isim, f"İşlem Yapılan Kod: {lisans_kodu}", request.client.host)
    return {"mesaj": f"HWID sıfırlandı."}

@router.post("/panel/sure-uzat")
def sure_uzat(lisans_kodu: str, gun: int, request: Request, bg_tasks: BackgroundTasks, user: PanelUserDto = Depends(yetki_kontrol("sure_uzat")), s: Session = Depends(db)):
    lisans = s.query(Lisans).filter_by(lisans_kodu=lisans_kodu.upper()).first()
    if not lisans:
        raise HTTPException(status_code=404, detail="Lisans bulunamadı.")
    if lisans.bitis_tarihi is None:
        raise HTTPException(status_code=400, detail="Ömür boyu lisansların süresi uzatılamaz.")
        
    lisans.bitis_tarihi = max(lisans.bitis_tarihi, datetime.datetime.utcnow()) + datetime.timedelta(days=gun)
    lisans.aktif = True
    s.commit()
    istihbarat_raporu(bg_tasks, "Lisans Süresi Uzatıldı", user.tam_isim, f"Kod: {lisans_kodu}\nEklenen: +{gun} Gün", request.client.host)
    return {"mesaj": f"{gun} gün eklendi."}

@router.post("/panel/talep-guncelle")
async def talep_guncelle(request: Request, bg_tasks: BackgroundTasks, user: PanelUserDto = Depends(yetki_kontrol("talep_onayla")), s: Session = Depends(db)):
    data = await request.json()
    talep = s.query(LisansTalep).filter_by(id=data["talep_id"]).first()
    talep.durum = data["durum"]
    talep.admin_notu = data.get('admin_notu', '')
    
    if data["durum"] == "onaylandi":
        u_tur = s.query(UyelikTuru).filter_by(kod=talep.tur).first()
        prefix = u_tur.prefix if u_tur and hasattr(u_tur, 'prefix') and u_tur.prefix else "STD"
        sure = getattr(u_tur, 'sure_gun', 30) or 30
        
        if talep.talep_tipi == "offline":
            # Çevrimdışı (Offline) aktivasyon kodu üretimi
            mesaj = f"{talep.istek_kodu}|{sure}".encode("utf-8")
            imza = hmac.new(OFFLINE_SECRET_KEY, mesaj, hashlib.sha256).hexdigest()[:16].upper()
            akt_kod = f"ACT-{sure}D-{imza}"
            talep.aktivasyon_kodu = akt_kod
            # Offline lisansı Lisans tablosuna da kaydet — geçmişte görünsün
            bitis_offline = datetime.datetime.utcnow() + datetime.timedelta(days=sure)
            s.add(Lisans(
                lisans_kodu=akt_kod,
                musteri_adi=talep.ad_soyad,
                musteri_email=talep.email,
                tur=talep.tur,
                bitis_tarihi=bitis_offline,
                notlar=f"offline|{talep.istek_kodu}",
                aktif=True
            ))
            s.commit()
            istihbarat_raporu(bg_tasks, "Offline Talep Onaylandı", user.tam_isim, f"Müşteri: {talep.ad_soyad}\nİstek Kodu: {talep.istek_kodu}\nAktivasyon Kodu: {akt_kod}", request.client.host)
        else:
            # Çevrimiçi (Online) lisans kaydı
            kod = lisans_kodu_uret(prefix)
            s.add(Lisans(lisans_kodu=kod, musteri_adi=talep.ad_soyad, musteri_email=talep.email, tur=talep.tur, bitis_tarihi=bitis_tarihi_hesapla(talep.tur, s)))
            s.commit()
            istihbarat_raporu(bg_tasks, "Online Talep Onaylandı", user.tam_isim, f"Müşteri: {talep.ad_soyad} ({talep.email})\nTalep Türü: {talep.tur}\nNot: {talep.admin_notu}", request.client.host)
    else:
        s.commit()
        istihbarat_raporu(bg_tasks, "Talep REDDEDİLDİ", user.tam_isim, f"Müşteri: {talep.ad_soyad} ({talep.email})\nTalep Türü: {talep.tur}\nNot: {talep.admin_notu}", request.client.host)

    return {"basarili": True}

@router.post("/panel/admin-mesaj-gonder")
async def admin_mesaj_gonder(request: Request, bg_tasks: BackgroundTasks, user: PanelUserDto = Depends(yetki_kontrol("mesaj_yaz")), s: Session = Depends(db)):
    data = await request.json()
    s.add(Mesaj(kullanici_id=data["kullanici_id"], gonderen="admin", icerik=data.get("icerik", ""), okundu=False))
    s.commit()
    istihbarat_raporu(bg_tasks, "Kullanıcıya Mesaj Gönderildi", user.tam_isim, f"Alıcı ID: {data['kullanici_id']}\nMesaj: {data.get('icerik')}", request.client.host)
    return {"basarili": True}

@router.post("/panel/ip-ban-ekle")
async def ip_ban_ekle(request: Request, bg_tasks: BackgroundTasks, user: PanelUserDto = Depends(yetki_kontrol("ip_ban")), s: Session = Depends(db)):
    data = await request.json()
    s.add(IpBan(ip=data["ip"], sebep=data.get("sebep", "")))
    s.commit()
    istihbarat_raporu(bg_tasks, "IP Banlandı", user.tam_isim, f"Banlanan IP: {data['ip']}\nSebep: {data.get('sebep')}", request.client.host)
    return {"mesaj": f"IP banlandı."}

@router.post("/panel/ip-ban-kaldir")
async def ip_ban_kaldir(request: Request, bg_tasks: BackgroundTasks, user: PanelUserDto = Depends(yetki_kontrol("ip_ban")), s: Session = Depends(db)):
    data = await request.json()
    ban = s.query(IpBan).filter_by(ip=data["ip"]).first()
    ban.aktif = False
    s.commit()
    istihbarat_raporu(bg_tasks, "IP Banı Kaldırıldı", user.tam_isim, f"Kaldırılan IP: {data['ip']}", request.client.host)
    return {"mesaj": f"IP banı kaldırıldı."}

# Diğer get metotları (loglar, istatistikler, listeler) aynı kalıyor...
@router.get("/panel/lisanslar")
def lisanslar_listele(filtre: str = "hepsi", user: PanelUserDto = Depends(panel_dogrula), s: Session = Depends(db)):
    simdi = datetime.datetime.utcnow()
    liste = s.query(Lisans).order_by(Lisans.olusturma_tar.desc()).all()
    sonuc = []
    for l in liste:
        durum = "aktif" if l.aktif and (not l.bitis_tarihi or simdi <= l.bitis_tarihi) else "iptal" if not l.aktif else "suresi_dolmus"
        if filtre != "hepsi" and filtre != durum: continue
        sonuc.append({
            "lisans_kodu": l.lisans_kodu, "musteri_adi": l.musteri_adi, "musteri_email": l.musteri_email,
            "tur": l.tur, "aktif": l.aktif, "durum": durum, "hwid": l.hwid or "Yok",
            "bitis_tarihi": l.bitis_tarihi.strftime("%d.%m.%Y") if l.bitis_tarihi else "Ömür boyu",
            "son_checkin": l.son_checkin.strftime("%d.%m.%Y") if l.son_checkin else "Hiç",
            "aktivasyon": l.aktivasyon_tar.strftime("%d.%m.%Y") if l.aktivasyon_tar else "Yok",
            "notlar": l.notlar or "", "iptal_nedeni": l.iptal_nedeni or "",
            "uretilen_tip": getattr(l, "uretilen_tip", "online") or "online",
            "istek_kodu": getattr(l, "istek_kodu_db", "") or "",
            "sure_gun": getattr(l, "sure_gun_db", "") or "",
            "yetki": getattr(l, "yetki_seviyesi", "") or ""
        })
    return sonuc

@router.get("/panel/talepler")
def panel_talepler(user: PanelUserDto = Depends(panel_dogrula), s: Session = Depends(db)):
    return [{"id": t.id, "kullanici_id": t.kullanici_id, "ad_soyad": t.ad_soyad, "email": t.email, "tur": t.tur, "durum": t.durum, "tarih": t.talep_tar.strftime("%d.%m.%Y %H:%M"), "ip": t.ip_adresi, "admin_notu": t.admin_notu or "", "talep_tipi": t.talep_tipi, "istek_kodu": t.istek_kodu, "aktivasyon_kodu": t.aktivasyon_kodu} for t in s.query(LisansTalep).order_by(LisansTalep.talep_tar.desc()).all()]

@router.get("/panel/iptal-istatistikleri")
def iptal_istatistikleri(user: PanelUserDto = Depends(panel_dogrula), s: Session = Depends(db)):
    return {"ozet": {"toplam": s.query(Lisans).count(), "aktif": 0, "biten": 0, "iptal": 0}, "nedenler": []}

@router.get("/panel/kullanicilar")
def panel_kullanicilar(user: PanelUserDto = Depends(panel_dogrula), s: Session = Depends(db)):
    kullanicilar = s.query(Kullanici).order_by(Kullanici.kayit_tar.desc()).all()
    sonuc = []
    for k in kullanicilar:
        l = s.query(Lisans).filter_by(musteri_email=k.email, aktif=True).first()
        sonuc.append({"id": k.id, "ad_soyad": k.ad_soyad, "email": k.email, "email_dogrulandi": k.email_dogrulandi, "kayit_tar": k.kayit_tar.strftime("%d.%m.%Y"), "son_giris": k.son_giris.strftime("%d.%m.%Y") if k.son_giris else "Hiç", "son_ip": k.son_ip or "-", "lisans_kodu": l.lisans_kodu if l else None, "lisans_tur": l.tur if l else None})
    return sonuc

@router.delete("/panel/kullanici-sil/{kullanici_id}")
def kullanici_sil(kullanici_id: str, request: Request, bg_tasks: BackgroundTasks, user: PanelUserDto = Depends(panel_dogrula), s: Session = Depends(db)):
    k = s.query(Kullanici).filter_by(id=kullanici_id).first()
    s.query(Lisans).filter_by(musteri_email=k.email).update({"aktif": False})
    s.delete(k)
    s.commit()
    istihbarat_raporu(bg_tasks, "Müşteri Silindi", user.tam_isim, f"Silinen: {k.ad_soyad} ({k.email})", request.client.host)
    return {"mesaj": f"Kullanıcı silindi."}

@router.put("/panel/kullanici-duzenle/{kullanici_id}")
async def kullanici_duzenle(
    kullanici_id: str,
    request: Request,
    bg_tasks: BackgroundTasks,
    user: PanelUserDto = Depends(panel_dogrula),
    s: Session = Depends(db)
):
    """Ana Admin'in müşteri kullanıcıların şifresini sıfırlayabilmesi ve not ekleyebilmesi için."""
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Yalnızca admin düzenleyebilir.")
    data = await request.json()
    k = s.query(Kullanici).filter_by(id=kullanici_id).first()
    if not k:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
    degisiklik = []
    if data.get("sifre"):
        if len(data["sifre"]) < 6:
            raise HTTPException(status_code=400, detail="Şifre en az 6 karakter olmalıdır.")
        k.sifre_hash = sifre_hashle(data["sifre"])
        degisiklik.append("Şifre sıfırlandı")
    if "not" in data:
        # Notları lisans kaydına ekle (mevcut aktif lisans varsa)
        lisans = s.query(Lisans).filter_by(musteri_email=k.email, aktif=True).order_by(Lisans.olusturma_tar.desc()).first()
        if lisans:
            lisans.notlar = data["not"]
            degisiklik.append("Lisans notu güncellendi")
    s.commit()
    panel_log_yaz(s, user.kullanici_adi, "Müşteri Düzenlendi", f"ID: {kullanici_id} | {', '.join(degisiklik)}")
    istihbarat_raporu(bg_tasks, "Müşteri Bilgisi Düzenlendi", user.tam_isim, f"Kullanıcı: {k.ad_soyad} ({k.email})\n{', '.join(degisiklik)}", request.client.host)
    return {"basarili": True, "mesaj": "Değişiklikler kaydedildi."}

@router.post("/panel/uyelik-tur-ekle")
async def uyelik_tur_ekle(request: Request, bg_tasks: BackgroundTasks, user: PanelUserDto = Depends(yetki_kontrol("uyelik_tur")), s: Session = Depends(db)):
    data = await request.json()
    s.add(UyelikTuru(kod=data["kod"], ad=data["ad"], aciklama=data.get("aciklama", ""), sira=data.get("sira", 99), sure_gun=data.get("sure_gun", 30), prefix=data.get("prefix", "STD").upper()[:10], is_offline=data.get("is_offline", False)))
    s.commit()
    istihbarat_raporu(bg_tasks, "Yeni Paket/Tür Eklendi", user.tam_isim, f"Tür: {data['ad']} ({data['kod']}) | Offline: {'Evet' if data.get('is_offline') else 'Hayır'}", request.client.host)
    return {"basarili": True}

class GirisIstek(BaseModel):
    kullanici: str
    sifre: str

@router.post("/panel/giris")
def panel_giris_yap(istek: GirisIstek, request: Request, bg_tasks: BackgroundTasks, s: Session = Depends(db)):
    kadi_gercek, sifre_hash_gercek = get_ana_admin_creds(s)
    if istek.kullanici == kadi_gercek and sifre_hashle(istek.sifre) == sifre_hash_gercek:
        istihbarat_raporu(bg_tasks, "Admin Panel Girişi", "Ana Admin", "Sisteme giriş yapıldı.", request.client.host)
        return {"basarili": True, "is_admin": True, "kullanici_adi": kadi_gercek, "isim_soyad": "Ana Admin", "yetkiler": {}}
        
    pk = s.query(PanelKullanici).filter_by(kullanici_adi=istek.kullanici, sifre_hash=sifre_hashle(istek.sifre)).first()
    if pk:
        istihbarat_raporu(bg_tasks, "Yetkili Panel Girişi", f"{pk.isim_soyad} ({pk.kullanici_adi})", "Sisteme giriş yapıldı.", request.client.host)
        pk.son_giris = datetime.datetime.utcnow()
        s.commit()
        return {"basarili": True, "is_admin": pk.is_admin, "kullanici_adi": pk.kullanici_adi, "isim_soyad": pk.isim_soyad, "yetkiler": {}}
    raise HTTPException(status_code=401, detail="Panel kullanici adi veya sifresi yanlis.")

class YetkiliEkleIstek(BaseModel):
    kullanici_adi: str
    isim_soyad: str
    email: str
    sifre: str
    yetkiler: dict

@router.post("/panel/yetkili-ekle")
def panel_yetkili_ekle(istek: YetkiliEkleIstek, request: Request, bg_tasks: BackgroundTasks, user: PanelUserDto = Depends(yetki_kontrol("kullanici_ekle")), s: Session = Depends(db)):
    y = PanelKullanici(kullanici_adi=istek.kullanici_adi, isim_soyad=istek.isim_soyad, email=istek.email, sifre_hash=sifre_hashle(istek.sifre))
    yetki_map = {
        "lisans_olustur": "yetki_lisans_olustur", "lisans_sil": "yetki_lisans_sil",
        "hwid_sifirla": "yetki_hwid_sifirla", "sure_uzat": "yetki_sure_uzat",
        "talep_onayla": "yetki_talep_onayla", "kullanici_ekle": "yetki_kullanici_ekle",
        "mesaj_yaz": "yetki_mesaj_yaz", "ip_ban": "yetki_ip_ban", "uyelik_tur": "yetki_uyelik_tur",
        "offline_paket_yonetimi": "yetki_offline_paket_yonetimi", "offline_lisans_uret": "yetki_offline_lisans_uret"
    }
    for key, col in yetki_map.items():
        if key in istek.yetkiler:
            setattr(y, col, bool(istek.yetkiler[key]))
    s.add(y)
    s.commit()
    istihbarat_raporu(bg_tasks, "Yeni Alt Yetkili Eklendi", user.tam_isim, f"Eklenen Yetkili: {istek.isim_soyad} ({istek.kullanici_adi})", request.client.host)
    return {"basarili": True}

@router.delete("/panel/yetkili-sil/{yetkili_id}")
def panel_yetkili_sil(yetkili_id: int, request: Request, bg_tasks: BackgroundTasks, user: PanelUserDto = Depends(panel_dogrula), s: Session = Depends(db)):
    y = s.query(PanelKullanici).filter_by(id=yetkili_id).first()
    istihbarat_raporu(bg_tasks, "Alt Yetkili Silindi", user.tam_isim, f"Silinen Yetkili: {y.kullanici_adi}", request.client.host)
    s.delete(y)
    s.commit()
    return {"basarili": True}

class OfflineLisansIstek(BaseModel):
    istek_kodu: str
    sure_gun: int
    kime_uretildi: str
    musteri_email: str = ""

@router.post("/panel/offline-lisans-uret")
def offline_lisans_uret(istek: OfflineLisansIstek, request: Request, bg_tasks: BackgroundTasks, user: PanelUserDto = Depends(yetki_kontrol("offline_lisans_uret")), s: Session = Depends(db)):
    mesaj = f"{istek.istek_kodu}|{istek.sure_gun}".encode("utf-8")
    imza = hmac.new(OFFLINE_SECRET_KEY, mesaj, hashlib.sha256).hexdigest()[:16].upper()
    akt_kod = f"ACT-{istek.sure_gun}D-{imza}"
    
    bitis = datetime.datetime.utcnow() + datetime.timedelta(days=istek.sure_gun) if istek.sure_gun > 0 else None
    
    l = Lisans(
        lisans_kodu=akt_kod,
        musteri_adi=istek.kime_uretildi,
        musteri_email=istek.musteri_email,
        tur="Offline",
        bitis_tarihi=bitis,
        notlar=f"offline|{istek.istek_kodu}",
        aktif=True,
        uretilen_tip="offline",
        istek_kodu_db=istek.istek_kodu,
        sure_gun_db=istek.sure_gun
    )
    s.add(l)
    s.commit()
    
    detay = f"İstek Kodu: {istek.istek_kodu}\nMüşteri: {istek.kime_uretildi}\nSüre: {istek.sure_gun} Gün\n\nÜretilen Kod: {akt_kod}"
    istihbarat_raporu(bg_tasks, "Çevrimdışı (Offline) Lisans Üretildi", user.tam_isim, detay, request.client.host)
    return {"basarili": True, "aktivasyon_kodu": akt_kod, "istek_kodu": istek.istek_kodu, "sure_gun": istek.sure_gun}

@router.get("/panel/loglar")
def loglar(son: int = 100, user: PanelUserDto = Depends(panel_dogrula), s: Session = Depends(db)):
    logs = s.query(Log).order_by(Log.tarih.desc()).limit(son).all()
    return [{"tarih": l.tarih.strftime("%d.%m.%Y %H:%M:%S"), "islem": l.islem, "lisans_kodu": l.lisans_kodu, "hwid": l.hwid, "ip": l.ip, "mesaj": l.mesaj} for l in logs]

@router.get("/panel/mesajlar-ozet")
def panel_mesajlar_ozet(user: PanelUserDto = Depends(panel_dogrula), s: Session = Depends(db)):
    """Her kullanıcı için son mesaj ve okunmamış sayısı"""
    kullanicilar = s.query(Kullanici).all()
    sonuc = []
    for k in kullanicilar:
        toplam = s.query(Mesaj).filter_by(kullanici_id=k.id).count()
        if toplam == 0:
            continue
        okunmamis = s.query(Mesaj).filter_by(kullanici_id=k.id, gonderen="kullanici", okundu=False).count()
        son_mesaj = s.query(Mesaj).filter_by(kullanici_id=k.id).order_by(Mesaj.tarih.desc()).first()
        lisans = s.query(Lisans).filter_by(musteri_email=k.email, aktif=True).order_by(Lisans.olusturma_tar.desc()).first()
        kalan = None
        if lisans and lisans.bitis_tarihi:
            kalan = max(0, (lisans.bitis_tarihi - datetime.datetime.utcnow()).days)
        sonuc.append({
            "kullanici_id": k.id,
            "ad_soyad": k.ad_soyad,
            "email": k.email,
            "son_ip": k.son_ip,
            "okunmamis": okunmamis,
            "son_mesaj": son_mesaj.icerik[:60] if son_mesaj else "",
            "son_mesaj_tar": son_mesaj.tarih.strftime("%d.%m.%Y %H:%M") if son_mesaj else "",
            "lisans_kodu": lisans.lisans_kodu if lisans else None,
            "lisans_tur": lisans.tur if lisans else None,
            "lisans_bitis": lisans.bitis_tarihi.strftime("%d.%m.%Y") if (lisans and lisans.bitis_tarihi) else ("Ömür Boyu" if lisans else None),
            "kalan_gun": kalan,
        })
    sonuc.sort(key=lambda x: x["okunmamis"], reverse=True)
    return sonuc

@router.get("/panel/kullanici-mesajlar/{kullanici_id}")
def kullanici_mesajlari(kullanici_id: str, user: PanelUserDto = Depends(panel_dogrula), s: Session = Depends(db)):
    s.query(Mesaj).filter_by(kullanici_id=kullanici_id, gonderen="kullanici", okundu=False).update({"okundu": True})
    s.commit()
    mesajlar = s.query(Mesaj).filter_by(kullanici_id=kullanici_id).order_by(Mesaj.tarih.asc()).all()
    k = s.query(Kullanici).filter_by(id=kullanici_id).first()
    lisans = s.query(Lisans).filter_by(musteri_email=k.email if k else "", aktif=True).order_by(Lisans.olusturma_tar.desc()).first()
    kalan = None
    if lisans and lisans.bitis_tarihi:
        kalan = max(0, (lisans.bitis_tarihi - datetime.datetime.utcnow()).days)
    return {
        "kullanici": {
            "id": k.id if k else kullanici_id,
            "ad_soyad": k.ad_soyad if k else "?",
            "email": k.email if k else "?",
            "son_ip": k.son_ip if k else "?",
            "kayit_tar": k.kayit_tar.strftime("%d.%m.%Y") if k else "?",
        },
        "lisans": {
            "kod": lisans.lisans_kodu if lisans else None,
            "tur": lisans.tur if lisans else None,
            "bitis": lisans.bitis_tarihi.strftime("%d.%m.%Y") if (lisans and lisans.bitis_tarihi) else ("Ömür Boyu" if lisans else None),
            "kalan_gun": kalan,
            "aktif": lisans.aktif if lisans else False,
        } if lisans else None,
        "mesajlar": [{"id": m.id, "gonderen": m.gonderen, "icerik": m.icerik, "tarih": m.tarih.strftime("%d.%m.%Y %H:%M")} for m in mesajlar],
    }

@router.get("/panel/ip-banlar")
def ip_banlar(user: PanelUserDto = Depends(yetki_kontrol("ip_ban")), s: Session = Depends(db)):
    banlar = s.query(IpBan).order_by(IpBan.tarih.desc()).all()
    return [{"id": b.id, "ip": b.ip, "sebep": b.sebep or "", "tarih": b.tarih.strftime("%d.%m.%Y %H:%M"), "aktif": b.aktif} for b in banlar]

@router.get("/panel/uyelik-turleri")
def panel_uyelik_turleri(user: PanelUserDto = Depends(yetki_kontrol("uyelik_tur")), s: Session = Depends(db)):
    turler = s.query(UyelikTuru).order_by(UyelikTuru.sira).all()
    return [{"id": t.id, "kod": t.kod, "ad": t.ad, "aciklama": t.aciklama, "aktif": t.aktif, "sira": t.sira, "sure_gun": getattr(t, 'sure_gun', 30), "prefix": getattr(t, 'prefix', 'STD'), "is_offline": getattr(t, 'is_offline', False)} for t in turler]

@router.post("/panel/uyelik-tur-guncelle")
async def uyelik_tur_guncelle(request: Request, user: PanelUserDto = Depends(yetki_kontrol("uyelik_tur")), s: Session = Depends(db)):
    data = await request.json()
    t = s.query(UyelikTuru).filter_by(id=data["id"]).first()
    if not t:
        raise HTTPException(status_code=404, detail="Tür bulunamadı.")
    if "aktif" in data:
        t.aktif = data["aktif"]
    if "sure_gun" in data:
        t.sure_gun = int(data["sure_gun"])
    if "prefix" in data:
        t.prefix = str(data["prefix"]).upper()[:10]
    if "is_offline" in data:
        t.is_offline = bool(data["is_offline"])
    s.commit()
    panel_log_yaz(s, user.kullanici_adi, "Üyelik Türü Güncellendi", f"ID: {data['id']}")
    return {"basarili": True}

@router.delete("/panel/uyelik-tur-sil/{tur_id}")
def uyelik_tur_sil(tur_id: int, user: PanelUserDto = Depends(yetki_kontrol("uyelik_tur")), s: Session = Depends(db)):
    t = s.query(UyelikTuru).filter_by(id=tur_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Tür bulunamadı.")
    panel_log_yaz(s, user.kullanici_adi, "Üyelik Türü Silindi", f"Kod: {t.kod}")
    s.delete(t)
    s.commit()
    return {"basarili": True}

@router.get("/panel/yetkililer")
def panel_yetkililer_getir(user: PanelUserDto = Depends(panel_dogrula), s: Session = Depends(db)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Yalnızca admin görebilir.")
    pk = s.query(PanelKullanici).all()
    return [{
        "id": p.id,
        "kullanici_adi": p.kullanici_adi,
        "isim_soyad": p.isim_soyad,
        "email": p.email,
        "is_admin": p.is_admin,
        "telegram_chat_id": p.telegram_chat_id or "",
        "telegram_bildirim_alabilir": p.telegram_bildirim_alabilir,
        "son_giris": p.son_giris.strftime("%d.%m.%Y %H:%M") if p.son_giris else "-",
        "son_cikis": p.son_cikis.strftime("%d.%m.%Y %H:%M") if p.son_cikis else "-",
        "yetkiler": {
            "lisans_olustur": p.yetki_lisans_olustur,
            "lisans_sil": p.yetki_lisans_sil,
            "hwid_sifirla": p.yetki_hwid_sifirla,
            "sure_uzat": p.yetki_sure_uzat,
            "talep_onayla": p.yetki_talep_onayla,
            "kullanici_ekle": p.yetki_kullanici_ekle,
            "mesaj_yaz": p.yetki_mesaj_yaz,
            "ip_ban": p.yetki_ip_ban,
            "uyelik_tur": p.yetki_uyelik_tur,
            "offline_paket_yonetimi": p.yetki_offline_paket_yonetimi,
            "offline_lisans_uret": p.yetki_offline_lisans_uret,
        }
    } for p in pk]

@router.get("/panel/panel-loglari")
def panel_loglari_getir(user: PanelUserDto = Depends(panel_dogrula), s: Session = Depends(db)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Yalnızca admin görebilir.")
    plogs = s.query(PanelLog).order_by(PanelLog.tarih.desc()).limit(200).all()
    return [{
        "tarih": pl.tarih.strftime("%d.%m.%Y %H:%M:%S"),
        "kullanici_adi": pl.kullanici_adi,
        "islem": pl.islem,
        "detay": pl.detay or ""
    } for pl in plogs]

@router.post("/panel/cikis")
def panel_cikis_yap(user: PanelUserDto = Depends(panel_dogrula), s: Session = Depends(db)):
    if not user.is_admin and user.kullanici_adi != PANEL_KULLANICI:
        pk = s.query(PanelKullanici).filter_by(kullanici_adi=user.kullanici_adi).first()
        if pk:
            pk.son_cikis = datetime.datetime.utcnow()
            s.commit()
    panel_log_yaz(s, user.kullanici_adi, "Çıkış Yaptı")
    return {"basarili": True}

@router.put("/panel/yetkili-guncelle/{yetkili_id}")
async def panel_yetkili_guncelle(
    yetkili_id: int,
    request: Request,
    bg_tasks: BackgroundTasks,
    user: PanelUserDto = Depends(panel_dogrula),
    s: Session = Depends(db)
):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Yalnızca admin güncelleyebilir.")
    data = await request.json()
    y = s.query(PanelKullanici).filter_by(id=yetkili_id).first()
    if not y:
        raise HTTPException(status_code=404, detail="Yetkili bulunamadı.")
    yetki_map = {
        "lisans_olustur": "yetki_lisans_olustur",
        "lisans_sil":     "yetki_lisans_sil",
        "hwid_sifirla":   "yetki_hwid_sifirla",
        "sure_uzat":      "yetki_sure_uzat",
        "talep_onayla":   "yetki_talep_onayla",
        "kullanici_ekle": "yetki_kullanici_ekle",
        "mesaj_yaz":      "yetki_mesaj_yaz",
        "ip_ban":         "yetki_ip_ban",
        "uyelik_tur":     "yetki_uyelik_tur",
        "offline_paket_yonetimi": "yetki_offline_paket_yonetimi",
        "offline_lisans_uret": "yetki_offline_lisans_uret",
    }
    yetkiler = data.get("yetkiler", {})
    for key, col in yetki_map.items():
        if key in yetkiler:
            setattr(y, col, bool(yetkiler[key]))
            
    if "telegram_chat_id" in data:
        y.telegram_chat_id = data["telegram_chat_id"]
    if "telegram_bildirim_alabilir" in data:
        y.telegram_bildirim_alabilir = data["telegram_bildirim_alabilir"]
    if data.get("sifre"):
        y.sifre_hash = sifre_hashle(data["sifre"])
        
    s.commit()
    panel_log_yaz(s, user.kullanici_adi, "Yetkili Güncelledi", f"ID: {yetkili_id}")
    
    degisenler = [f"{k}: {'Açık' if yetkiler[k] else 'Kapalı'}" for k in yetkiler] if yetkiler else []
    detay = f"Düzenlenen Yetkili: {y.isim_soyad or y.kullanici_adi}\nŞifre Değişti: {'Evet' if data.get('sifre') else 'Hayır'}"
    if degisenler:
        detay += f"\nYetkiler:\n" + "\n".join(degisenler)
    
    istihbarat_raporu(bg_tasks, "Alt Yetkili İzinleri Güncellendi", user.tam_isim, detay, request.client.host)
    return {"basarili": True}

class AdminGuncelleIstek(BaseModel):
    yeni_kullanici: str
    yeni_sifre: str

@router.post("/panel/admin-guncelle")
def admin_guncelle(istek: AdminGuncelleIstek, user: PanelUserDto = Depends(panel_dogrula), s: Session = Depends(db)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Yalnızca ana admin değiştirebilir.")

    ayar = s.query(Ayarlar).first()
    if not ayar:
        ayar = Ayarlar()
        s.add(ayar)

    ayar.admin_kullanici = istek.yeni_kullanici
    ayar.admin_sifre_hash = sifre_hashle(istek.yeni_sifre)
    s.commit()
    panel_log_yaz(s, user.kullanici_adi, "Admin Bilgilerini Değiştirdi")
    return {"basarili": True, "mesaj": "Admin bilgileri güncellendi. Lütfen tekrar giriş yapın."}


