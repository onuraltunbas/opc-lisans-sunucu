# -*- coding: utf-8 -*-
"""
HTML Sayfa Route'ları — Panel ve kullanıcı sitesi HTML endpoint'leri.
"""

import os
import pathlib

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, FileResponse

from html_panel import PANEL_HTML
from html_site import SITE_CSS, SITE_HTML_TEMPLATE

router = APIRouter()


# ===== YARDIMCI FONKSİYON =====

def render_seo(page: str, title: str, desc: str, keys: str) -> HTMLResponse:
    """
    SITE_HTML_TEMPLATE içindeki {CSS}, {{ title }}, {{ description }},
    {{ keywords }} ve {{ current_page }} yer tutucularını .replace() ile
    doldurur ve HTMLResponse döner.
    """
    html = (
        SITE_HTML_TEMPLATE
        .replace("{CSS}", SITE_CSS)
        .replace("{{ title }}", f'<title>{title}</title>')
        .replace("{{ description }}", f'<meta name="description" content="{desc}">')
        .replace("{{ keywords }}", f'<meta name="keywords" content="{keys}">')
        .replace("{{ current_page }}", page)
    )
    return HTMLResponse(content=html)


# ===== PANEL =====

@router.get("/panel", response_class=HTMLResponse)
def panel_html():
    return HTMLResponse(content=PANEL_HTML)


# ===== ANASAYFA =====

@router.get("/", response_class=HTMLResponse)
def anasayfa():
    return render_seo(
        page="anasayfa",
        title="Nautilus Technology | PLC ve Endüstriyel Otomasyon Gateway Sistemleri",
        desc=(
            "Siemens, Delta, Schneider ve tüm PLC markaları ile tam uyumlu OPC Gateway yazılımı. "
            "Güvenli, hızlı ve donanım bağımsız lisans yönetim sistemi."
        ),
        keys=(
            "Nautilus Technology, PLC otomasyon, OPC Gateway, OPC UA, OPC DA, "
            "endüstriyel gateway, SCADA entegrasyonu, Siemens PLC, Delta PLC, "
            "Schneider PLC, lisans yönetimi, endüstriyel yazılım"
        ),
    )


# ===== KAYIT =====

@router.get("/kayit", response_class=HTMLResponse)
def kayit_sayfasi():
    return render_seo(
        page="kayit",
        title="Hesap Oluştur | Nautilus Technology OPC Gateway Lisans Sistemi",
        desc=(
            "Nautilus Technology OPC Gateway lisans sistemine kayıt olun. "
            "PLC otomasyon yazılımınız için hızlı lisans aktivasyonu başlatın."
        ),
        keys=(
            "kayıt ol, hesap oluştur, OPC Gateway lisans, PLC yazılım lisansı, "
            "Nautilus Technology kayıt, otomasyon yazılım kaydı"
        ),
    )


# ===== GİRİŞ =====

@router.get("/giris", response_class=HTMLResponse)
def giris_sayfasi():
    return render_seo(
        page="giris",
        title="Giriş Yap | Nautilus Technology OPC Gateway Lisans Paneli",
        desc=(
            "Nautilus Technology hesabınıza giriş yapın ve OPC Gateway lisanslarınızı, "
            "PLC otomasyon yazılım aktivasyon durumunuzu yönetin."
        ),
        keys=(
            "giriş yap, OPC Gateway lisans girişi, PLC yazılım hesabı, "
            "Nautilus Technology giriş, otomasyon lisans paneli"
        ),
    )


# ===== DASHBOARD =====

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_sayfasi():
    return render_seo(
        page="dashboard",
        title="Dashboard | Nautilus Technology OPC Gateway Lisans Yönetimi",
        desc=(
            "OPC Gateway lisans durumunuzu görüntüleyin, PLC otomasyon yazılımınızı indirin "
            "ve lisans taleplerinizi takip edin."
        ),
        keys=(
            "OPC Gateway dashboard, lisans yönetimi, PLC otomasyon yazılım indirme, "
            "Nautilus Technology panel, lisans durumu, otomasyon lisans takibi"
        ),
    )


# ===== PLANLAR =====

@router.get("/planlar", response_class=HTMLResponse)
def planlar_sayfasi():
    return render_seo(
        page="planlar",
        title="Lisans Planları | Nautilus Technology OPC Gateway",
        desc=(
            "OPC Gateway yazılımı için aylık, yıllık ve ömür boyu lisans planlarını inceleyin. "
            "PLC otomasyon çözümleri için en uygun planı seçin."
        ),
        keys=(
            "OPC Gateway lisans planları, PLC yazılım fiyatları, otomasyon lisans aylık yıllık, "
            "Nautilus Technology planlar, Gateway yazılım fiyatlandırma"
        ),
    )


# ===== OFFLİNE AKTİVASYON =====

@router.get("/offline-aktivasyon", response_class=HTMLResponse)
def offline_aktivasyon_sayfasi():
    return render_seo(
        page="offline",
        title="Offline Aktivasyon | Nautilus Technology OPC Gateway",
        desc=(
            "İnternet bağlantısı olmayan PLC ve SCADA sistemleri için OPC Gateway offline lisans "
            "aktivasyon talebi oluşturun."
        ),
        keys=(
            "offline lisans aktivasyon, OPC Gateway offline, PLC offline aktivasyon, "
            "internetsiz lisans, SCADA offline aktivasyon, Nautilus Technology offline"
        ),
    )


# ===== HAKKIMIZDA =====

@router.get("/hakkimizda", response_class=HTMLResponse)
def hakkimizda_sayfasi():
    return render_seo(
        page="hakkimizda",
        title="Hakkımızda | Nautilus Technology — PLC Otomasyon ve Gateway Çözümleri",
        desc=(
            "Nautilus Technology; PLC otomasyon, OPC UA/DA Gateway ve endüstriyel haberleşme "
            "alanında yenilikçi yazılım çözümleri geliştiren Türk teknoloji firmasıdır."
        ),
        keys=(
            "Nautilus Technology hakkında, PLC otomasyon firması, OPC Gateway geliştirici, "
            "endüstriyel yazılım şirketi, SCADA çözümleri, otomasyon teknoloji"
        ),
    )


# ===== BLOG =====

@router.get("/blog", response_class=HTMLResponse)
def blog_sayfasi():
    return render_seo(
        page="blog",
        title="Teknik Blog | Nautilus Technology — PLC Otomasyon Makaleleri",
        desc=(
            "PLC otomasyon, OPC UA/DA protokolleri, SCADA entegrasyonu ve endüstriyel "
            "haberleşme konularında teknik makaleler ve rehberler."
        ),
        keys=(
            "PLC otomasyon blog, OPC UA makaleler, SCADA rehber, endüstriyel otomasyon teknik, "
            "Siemens PLC programlama, Delta PLC, Schneider otomasyon, Gateway kurulum"
        ),
    )


# ===== EFE SAYFASI (FOTOĞRAF / VİDEO) =====

_STATIC_DIR = pathlib.Path(__file__).parent / "static"
_EFE_DIR = _STATIC_DIR / "dolandiriciefe"

# Desteklenen uzantılar
_IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif"}
_VIDEO_EXT = {".mp4", ".webm", ".mov", ".mkv"}


def _efe_dosya_bul():
    """static/efe/ klasöründeki ilk fotoğraf veya videoyu döner."""
    if not _EFE_DIR.exists():
        return None, None
    for f in _EFE_DIR.iterdir():
        ext = f.suffix.lower()
        if ext in _IMAGE_EXT:
            return f, "image"
        if ext in _VIDEO_EXT:
            return f, "video"
    return None, None


@router.get("/dolandiriciefe", response_class=HTMLResponse)
def efe_sayfasi():
    dosya, tur = _efe_dosya_bul()

    if dosya is None:
        return HTMLResponse(content="""<!DOCTYPE html>
<html lang='tr'><head><meta charset='UTF-8'>
<title>Efe</title>
<style>
  body{background:#0a0a0a;color:#fff;font-family:sans-serif;
       display:flex;align-items:center;justify-content:center;height:100vh;margin:0;}
  p{opacity:.5;font-size:1.2rem;}
</style></head>
<body><p>Henüz bir dosya yüklenmedi.</p></body></html>""", status_code=404)

    # URL yolu: /static/efeyicokseviyorum/<dosya_adı>
    url = f"/static/{_EFE_DIR.name}/{dosya.name}"

    if tur == "image":
        medya_html = f"""<img src="{url}" alt="Efe"
            style="max-width:100%;max-height:100%;object-fit:contain;border-radius:12px;
                   box-shadow:0 8px 48px rgba(0,0,0,.7);">"""
    else:
        medya_html = f"""<video src="{url}" controls autoplay loop muted
            style="max-width:100%;max-height:100%;object-fit:contain;border-radius:12px;
                   box-shadow:0 8px 48px rgba(0,0,0,.7);">
        </video>"""

    html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Efe</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      height: 100%;
      background: #0a0a0a;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }}
    .container {{
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100vw;
      height: 100vh;
      padding: 24px;
    }}
  </style>
</head>
<body>
  <div class="container">
    {medya_html}
  </div>
</body>
</html>"""
    return HTMLResponse(content=html)


# ===== 121222 SAYFASI (FOTOĞRAF / VİDEO) =====
# 👇 Yeni sayfa eklemek için bu 3 parçayı kopyalayıp özelleştirin:
#    1) _XXX_DIR  →  klasör adı
#    2) _xxx_dosya_bul()  →  fonksiyon adı
#    3) @router.get("/xxx")  →  URL adresi

_121222_DIR = _STATIC_DIR / "121222"   # ← klasör adı (static/ altında)


def _121222_dosya_bul():
    """static/121222/ klasöründeki ilk fotoğraf veya videoyu döner."""
    if not _121222_DIR.exists():
        return None, None
    for f in _121222_DIR.iterdir():
        ext = f.suffix.lower()
        if ext in _IMAGE_EXT:
            return f, "image"
        if ext in _VIDEO_EXT:
            return f, "video"
    return None, None


@router.get("/121222", response_class=HTMLResponse)   # ← URL adresi
def sayfa_121222():
    dosya, tur = _121222_dosya_bul()

    if dosya is None:
        return HTMLResponse(content="""<!DOCTYPE html>
<html lang='tr'><head><meta charset='UTF-8'>
<title>121222</title>
<style>
  body{background:#0a0a0a;color:#fff;font-family:sans-serif;
       display:flex;align-items:center;justify-content:center;height:100vh;margin:0;}
  p{opacity:.5;font-size:1.2rem;}
</style></head>
<body><p>Henüz bir dosya yüklenmedi.</p></body></html>""", status_code=404)

    url = f"/static/121222/{dosya.name}"

    if tur == "image":
        medya_html = f"""<img src="{url}" alt="121222"
            style="max-width:100%;max-height:100%;object-fit:contain;border-radius:12px;
                   box-shadow:0 8px 48px rgba(0,0,0,.7);">"""
    else:
        medya_html = f"""<video src="{url}" controls autoplay loop muted
            style="max-width:100%;max-height:100%;object-fit:contain;border-radius:12px;
                   box-shadow:0 8px 48px rgba(0,0,0,.7);">
        </video>"""

    html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>121222</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{
      height: 100%;
      background: #0a0a0a;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
    }}
    .container {{
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100vw;
      height: 100vh;
      padding: 24px;
    }}
  </style>
</head>
<body>
  <div class="container">
    {medya_html}
  </div>
</body>
</html>"""
    return HTMLResponse(content=html)
