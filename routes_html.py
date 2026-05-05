# -*- coding: utf-8 -*-
"""
HTML Sayfa Route'ları — Panel ve kullanıcı sitesi HTML endpoint'leri.
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from html_panel import PANEL_HTML
from html_site import SITE_CSS, SITE_HTML_TEMPLATE

router = APIRouter()


@router.get("/panel", response_class=HTMLResponse)
def panel_html():
    return HTMLResponse(content=PANEL_HTML)


@router.get("/", response_class=HTMLResponse)
def anasayfa():
    html = SITE_HTML_TEMPLATE.replace("{CSS}", SITE_CSS)
    return HTMLResponse(content=html)


@router.get("/kayit", response_class=HTMLResponse)
def kayit_sayfasi():
    return HTMLResponse(content=SITE_HTML_TEMPLATE.replace("{CSS}", SITE_CSS) + "<script>sayfaGoster('kayit');</script>")


@router.get("/giris", response_class=HTMLResponse)
def giris_sayfasi():
    return HTMLResponse(content=SITE_HTML_TEMPLATE.replace("{CSS}", SITE_CSS) + "<script>sayfaGoster('giris');</script>")


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_sayfasi():
    return HTMLResponse(content=SITE_HTML_TEMPLATE.replace("{CSS}", SITE_CSS) + "<script>sayfaGoster('dashboard');</script>")


@router.get("/planlar", response_class=HTMLResponse)
def planlar_sayfasi():
    return HTMLResponse(content=SITE_HTML_TEMPLATE.replace("{CSS}", SITE_CSS) + "<script>sayfaGoster('planlar');</script>")


@router.get("/offline-aktivasyon", response_class=HTMLResponse)
def offline_aktivasyon_sayfasi():
    return HTMLResponse(content=SITE_HTML_TEMPLATE.replace("{CSS}", SITE_CSS) + "<script>sayfaGoster('offline');</script>")


@router.get("/hakkimizda", response_class=HTMLResponse)
def hakkimizda_sayfasi():
    return HTMLResponse(content=SITE_HTML_TEMPLATE.replace("{CSS}", SITE_CSS) + "<script>sayfaGoster('hakkimizda');</script>")
