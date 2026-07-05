# -*- coding: utf-8 -*-
"""
404 - Sayfa Bulunamadı şablonu.
html_site.py içindeki SITE_CSS kullanılarak, sitenin navbar/footer/renk
paletiyle birebir uyumlu, bağımsız (SPA'ya bağlı olmayan) bir hata sayfası
üretir. Bu sayede sitede TANIMLI OLMAYAN her adrese gidildiğinde
(ör. /herhangibirsayfa) düzgün görünen bir 404 sayfası döner.
"""

import html as _html

from html_site import SITE_CSS

# Sadece bu sayfaya özel, ek stiller (SITE_CSS zaten navbar/footer/buton
# sınıflarını tanımlıyor; burada sadece 404'e özgü birkaç sınıf ekleniyor)
_NOT_FOUND_EXTRA_CSS = """
<style>
.nf-wrap {
  flex: 1 1 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: clamp(40px, 8vh, 90px) clamp(16px, 4vw, 24px);
  text-align: center;
}
.nf-code {
  font-family: 'JetBrains Mono', monospace;
  font-size: clamp(64px, 14vw, 140px);
  font-weight: 700;
  line-height: 1;
  letter-spacing: -2px;
  color: var(--accent2);
  opacity: 0.92;
}
.nf-code span { color: var(--muted); }
.nf-title {
  font-size: clamp(18px, 3vw, 26px);
  font-weight: 800;
  margin: clamp(12px, 2vw, 18px) 0 clamp(8px, 1.5vw, 12px);
  letter-spacing: -0.4px;
}
.nf-desc {
  color: var(--text2);
  font-size: clamp(13px, 1.6vw, 15px);
  max-width: clamp(280px, 90vw, 460px);
  margin: 0 auto clamp(24px, 4vw, 34px);
  line-height: 1.75;
}
.nf-path {
  font-family: 'JetBrains Mono', monospace;
  background: var(--surface);
  border: 1px solid var(--border2);
  color: var(--text2);
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-size: 0.85em;
  word-break: break-all;
  display: inline-block;
}
</style>
"""


def render_404(path: str = "") -> str:
    """
    İstenen (bulunamayan) path'i alır, sitenin tasarımına uygun tam bir
    404 HTML sayfası döner. `path` kullanıcıdan geldiği için mutlaka
    HTML-escape edilir (XSS önlemi).
    """
    guvenli_path = _html.escape(path or "/")

    return f"""<!DOCTYPE html>
<html lang="tr" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>404 - Sayfa Bulunamadı | Nautilus Technology</title>
<meta name="robots" content="noindex, nofollow">
<meta name="description" content="Aradığınız sayfa bulunamadı. Nautilus Technology OPC Gateway lisans sistemi ana sayfasına dönün.">
{SITE_CSS}
{_NOT_FOUND_EXTRA_CSS}
</head>
<body>

<nav class="nav">
  <a class="nav-brand" href="/" style="text-decoration:none;">
    <img src="/static/logo.png" alt="Nautilus Technology" class="nav-logo" onerror="this.style.display='none'">
  </a>
  <div style="display:flex;flex-wrap:wrap;flex:1 1 auto;align-items:center;justify-content:flex-end;gap:clamp(6px,0.8vw,10px);">
    <div class="nav-links">
      <button class="nav-btn nav-btn-ghost" onclick="window.location.href='/giris'">Giriş Yap</button>
      <button class="nav-btn nav-btn-primary" onclick="window.location.href='/kayit'">Kayıt Ol</button>
    </div>
    <button id="theme-toggle" onclick="temaToggle()" title="Tema Değiştir">
      <span id="theme-icon">&#9790;</span>
    </button>
  </div>
</nav>

<div class="nf-wrap">
  <div>
    <div class="nf-code">4<span>0</span>4</div>
    <div class="nf-title">Aradığınız Sayfa Bulunamadı</div>
    <div class="nf-desc">
      Erişmeye çalıştığınız <span class="nf-path">{guvenli_path}</span> adresi
      sitemizde mevcut değil, kaldırılmış ya da taşınmış olabilir.
    </div>
    <div class="hero-btns" style="justify-content:center;">
      <button class="btn-hero btn-hero-primary" onclick="window.location.href='/'">&larr; Ana Sayfaya Dön</button>
      <button class="btn-hero btn-hero-ghost" onclick="window.location.href='/planlar'">Planları İncele</button>
    </div>
  </div>
</div>

<footer id="site-footer" style="border-top:1px solid var(--border);margin-top:auto;padding:clamp(36px,4.8vw,58px) clamp(18px,2.4vw,29px) clamp(24px,3.2vw,39px);">
  <div style="width:100%;max-width:clamp(300px,95vw,1100px);margin:0 auto;">
    <div style="display:grid;grid-template-columns:2fr 1fr 1fr;gap:clamp(30px,4.0vw,48px);margin-bottom:clamp(30px,4.0vh,48px);">
      <div>
        <div style="display:flex;flex-wrap:wrap;flex:1 1 auto;align-items:center;gap:clamp(7px,1.0vw,12px);margin-bottom:clamp(10px,1.4vh,17px);">
          <img src="/static/logo.png" alt="Nautilus" class="footer-logo" style="height:clamp(21px,2.8vh,34px);" onerror="this.style.display='none'">
          <span style="font-size:clamp(12px,1.6vw,20px);font-weight:800;">Nautilus Technology</span>
        </div>
        <p style="font-size:clamp(9px,1.3vw,16px);color:var(--text);line-height:1.7;width:100%;max-width:clamp(300px,95vw,280px);margin:0;">Endüstriyel otomasyon ve veri haberleşmesi alanında yenilikçi, yüksek verimli yazılım çözümleri.</p>
      </div>
      <div>
        <div style="font-size:clamp(9px,1.2vw,15px);font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted);margin-bottom:clamp(10px,1.4vh,17px);">Hızlı Erişim</div>
        <div style="display:flex;flex-wrap:wrap;flex:1 1 auto;flex-direction:column;gap:clamp(7px,1.0vw,12px);">
          <a href="/" style="font-size:clamp(10px,1.4vw,17px);color:var(--text);text-decoration:none;transition:color .15s;" onmouseover="this.style.color='var(--accent)'" onmouseout="this.style.color='var(--text)'">Ana Sayfa</a>
          <a href="/hakkimizda" style="font-size:clamp(10px,1.4vw,17px);color:var(--text);text-decoration:none;transition:color .15s;" onmouseover="this.style.color='var(--accent)'" onmouseout="this.style.color='var(--text)'">Hakkımızda</a>
          <a href="/blog" style="font-size:clamp(10px,1.4vw,17px);color:var(--text);text-decoration:none;transition:color .15s;" onmouseover="this.style.color='var(--accent)'" onmouseout="this.style.color='var(--text)'">Teknik Blog</a>
        </div>
      </div>
      <div>
        <div style="font-size:clamp(9px,1.2vw,15px);font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted);margin-bottom:clamp(10px,1.4vh,17px);">Hesap</div>
        <div style="display:flex;flex-wrap:wrap;flex:1 1 auto;flex-direction:column;gap:clamp(7px,1.0vw,12px);">
          <a href="/giris" style="font-size:clamp(10px,1.4vw,17px);color:var(--text);text-decoration:none;transition:color .15s;" onmouseover="this.style.color='var(--accent)'" onmouseout="this.style.color='var(--text)'">Giriş Yap</a>
          <a href="/kayit" style="font-size:clamp(10px,1.4vw,17px);color:var(--text);text-decoration:none;transition:color .15s;" onmouseover="this.style.color='var(--accent)'" onmouseout="this.style.color='var(--text)'">Kayıt Ol</a>
          <a href="/offline-aktivasyon" style="font-size:clamp(10px,1.4vw,17px);color:var(--text);text-decoration:none;transition:color .15s;" onmouseover="this.style.color='var(--accent)'" onmouseout="this.style.color='var(--text)'">Offline Aktivasyon</a>
        </div>
      </div>
    </div>
    <div style="border-top:1px solid var(--border);padding-top:clamp(18px,2.4vh,29px);display:flex;flex-wrap:wrap;flex:1 1 auto;align-items:center;justify-content:space-between;gap:clamp(9px,1.2vw,15px);">
      <div style="font-size:clamp(9px,1.3vw,16px);color:var(--text);">&copy; 2025 Nautilus Technology. Tüm hakları saklıdır.</div>
    </div>
  </div>
</footer>

<script>
// ===== TEMA YÖNETİMİ (dark/light) — anasayfa ile aynı mantık =====
(function() {{
  var kayitli = localStorage.getItem('nt_tema') || 'dark';
  document.documentElement.setAttribute('data-theme', kayitli);
  var ikon = document.getElementById('theme-icon');
  if (ikon) ikon.innerHTML = kayitli === 'light' ? '&#9728;' : '&#9790;';
}})();

function temaToggle() {{
  var mevcut = document.documentElement.getAttribute('data-theme') || 'dark';
  var yeni   = mevcut === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', yeni);
  localStorage.setItem('nt_tema', yeni);
  var ikon = document.getElementById('theme-icon');
  if (ikon) ikon.innerHTML = yeni === 'light' ? '&#9728;' : '&#9790;';
}}
</script>
</body>
</html>"""