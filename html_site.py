# -*- coding: utf-8 -*-
"""
Kullanıcı Sitesi CSS ve HTML Template içeriği.
"""

SITE_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

/* &#9472;&#9472; Dark mode (varsayılan) &#9472;&#9472; */
:root {
  --bg:        #0a0a0a;
  --bg2:       #111111;
  --surface:   #161616;
  --surface2:  #1e1e1e;
  --border:    #2a2a2a;
  --border2:   #383838;
  --accent:    #e0e0e0;
  --accent2:   #ffffff;
  --text:      #e0e0e0;
  --text2:     #a0a0a0;
  --muted:     #606060;
  --success:   #22c55e;
  --danger:    #ef4444;
  --warn:      #f59e0b;
  --radius:    4px;
  --radius-sm: 2px;
}

/* &#9472;&#9472; Light mode &#9472;&#9472; */
[data-theme="light"] {
  --bg:        #f4f4f4;
  --bg2:       #ffffff;
  --surface:   #ffffff;
  --surface2:  #ebebeb;
  --border:    #d0d0d0;
  --border2:   #b8b8b8;
  --accent:    #222222;
  --accent2:   #000000;
  --text:      #1a1a1a;
  --text2:     #4a4a4a;
  --muted:     #909090;
}

html, body {
  min-height: 100vh;
  font-family: 'Inter', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  transition: background 0.2s, color 0.2s;
}
body {
  background-image: linear-gradient(var(--border) 1px, transparent 1px), linear-gradient(90deg, var(--border) 1px, transparent 1px);
  background-size: 48px 48px;
  background-position: -1px -1px;
}

/* &#9472;&#9472; NAVBAR &#9472;&#9472; */
.nav {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 32px; height: 60px;
  border-bottom: 1px solid var(--border2);
  background: var(--bg);
  position: sticky; top: 0; z-index: 200;
}
.nav-brand { display: flex; align-items: center; gap: 12px; text-decoration: none; color: var(--text); }
.nav-logo { height: 30px; width: auto; display: block; }
[data-theme="light"] .nav-logo { filter: invert(1); }
.nav-brand-text { font-size: 14px; font-weight: 800; letter-spacing: -0.3px; color: var(--text); display: flex; flex-direction: column; line-height: 1.1; }
.nav-brand-text span { font-size: 10px; font-weight: 400; color: var(--muted); letter-spacing: 1.5px; text-transform: uppercase; }
.nav-links { display: flex; align-items: center; gap: 6px; }
.nav-btn { padding: 6px 16px; border-radius: var(--radius); font-size: 13px; font-weight: 600; cursor: pointer; border: 1px solid transparent; transition: all 0.15s; font-family: 'Inter', sans-serif; }
.nav-btn-ghost { background: transparent; color: var(--text2); border-color: var(--border2); }
.nav-btn-ghost:hover { color: var(--text); border-color: var(--accent); }
.nav-btn-primary { background: var(--accent2); color: var(--bg); border-color: var(--accent2); }
.nav-btn-primary:hover { opacity: 0.85; }

/* Dark/Light toggle */
#theme-toggle {
  display: flex; align-items: center; justify-content: center;
  width: 34px; height: 30px; background: transparent;
  border: 1px solid var(--border2); border-radius: var(--radius);
  cursor: pointer; color: var(--muted); font-size: 15px;
  transition: border-color 0.15s, color 0.15s; flex-shrink: 0;
}
#theme-toggle:hover { border-color: var(--accent); color: var(--text); }

/* &#9472;&#9472; HERO &#9472;&#9472; */
.hero { text-align: center; padding: 72px 24px 56px; }
.hero-badge { display: inline-flex; align-items: center; gap: 6px; background: var(--surface); border: 1px solid var(--border2); color: var(--text2); padding: 4px 14px; border-radius: var(--radius-sm); font-size: 11px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 24px; }
.hero h1 { font-size: clamp(28px, 5vw, 52px); font-weight: 800; line-height: 1.05; margin-bottom: 20px; letter-spacing: -1.5px; color: var(--accent2); }
.hero h1 span { color: var(--muted); font-weight: 300; font-style: italic; }
.hero p { color: var(--text2); font-size: 16px; max-width: 480px; margin: 0 auto 36px; line-height: 1.75; }
.hero-btns { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
.btn-hero { padding: 11px 28px; border-radius: var(--radius); font-size: 14px; font-weight: 700; cursor: pointer; border: 1px solid transparent; font-family: 'Inter', sans-serif; transition: all 0.15s; letter-spacing: 0.2px; }
.btn-hero-primary { background: var(--accent2); color: var(--bg); border-color: var(--accent2); }
.btn-hero-primary:hover { opacity: 0.87; transform: translateY(-1px); }
.btn-hero-ghost { background: transparent; color: var(--text); border-color: var(--border2); }
.btn-hero-ghost:hover { border-color: var(--accent); }

/* &#9472;&#9472; FEATURES &#9472;&#9472; */
.features { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 1px; max-width: 880px; margin: 0 auto 64px; padding: 0 24px; border: 1px solid var(--border); background: var(--border); }
.feature { background: var(--surface); padding: 28px 24px; transition: background 0.15s; }
.feature:hover { background: var(--surface2); }
.feature-icon { font-size: 20px; margin-bottom: 12px; }
.feature h3 { font-size: 14px; font-weight: 700; margin-bottom: 8px; letter-spacing: -0.2px; }
.feature p { font-size: 13px; color: var(--text2); line-height: 1.65; }

/* &#9472;&#9472; PLANS &#9472;&#9472; */
.plans-section { padding: 0 24px 80px; max-width: 880px; margin: 0 auto; }
.section-title { text-align: center; font-size: 26px; font-weight: 800; margin-bottom: 6px; letter-spacing: -0.5px; color: var(--accent2); }
.section-sub { text-align: center; color: var(--muted); font-size: 14px; margin-bottom: 32px; }
.plans { display: grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap: 1px; background: var(--border); border: 1px solid var(--border); }
.plan-card { background: var(--surface); padding: 22px 20px; cursor: pointer; transition: background 0.15s; position: relative; }
.plan-card:hover { background: var(--surface2); }
.plan-card.selected { background: var(--surface2); outline: 2px solid var(--accent2); outline-offset: -2px; }
.plan-card.selected::after { content: '\u2713'; position: absolute; top: 12px; right: 14px; color: var(--accent2); font-weight: 900; font-size: 14px; }
.plan-name { font-size: 14px; font-weight: 700; margin-bottom: 6px; }
.plan-desc { font-size: 12px; color: var(--muted); line-height: 1.55; }

/* &#9472;&#9472; FORMS &#9472;&#9472; */
.form-container { max-width: 420px; margin: 0 auto; padding: 0 24px 80px; }
.form-card { background: var(--surface); border: 1px solid var(--border2); border-radius: var(--radius); padding: 32px; }
.form-title { font-size: 20px; font-weight: 800; margin-bottom: 4px; letter-spacing: -0.4px; }
.form-sub { font-size: 13px; color: var(--muted); margin-bottom: 24px; }
.form-group { margin-bottom: 14px; }
.form-label { display: block; font-size: 11px; font-weight: 600; color: var(--text2); margin-bottom: 6px; letter-spacing: 0.5px; text-transform: uppercase; }
.form-input { width: 100%; background: var(--bg); border: 1px solid var(--border2); border-radius: var(--radius-sm); padding: 10px 12px; color: var(--text); font-size: 14px; font-family: 'Inter', sans-serif; transition: border-color 0.15s; }
.form-input:focus { outline: none; border-color: var(--accent); }
.form-btn { width: 100%; background: var(--accent2); color: var(--bg); border: 1px solid var(--accent2); border-radius: var(--radius); padding: 12px; font-size: 14px; font-weight: 700; cursor: pointer; font-family: 'Inter', sans-serif; transition: opacity 0.15s; margin-top: 6px; letter-spacing: 0.3px; }
.form-btn:hover { opacity: 0.85; }
.form-alt { text-align: center; font-size: 13px; color: var(--muted); margin-top: 14px; }
.form-alt a { color: var(--text); cursor: pointer; font-weight: 600; text-decoration: underline; text-underline-offset: 3px; }
.form-err { background: transparent; border: 1px solid var(--danger); color: #fca5a5; border-radius: var(--radius-sm); padding: 10px 14px; font-size: 13px; margin-bottom: 14px; display: none; }
.form-ok  { background: transparent; border: 1px solid var(--success); color: #86efac; border-radius: var(--radius-sm); padding: 10px 14px; font-size: 13px; margin-bottom: 14px; display: none; }

/* &#9472;&#9472; DASHBOARD &#9472;&#9472; */
.dashboard { max-width: 780px; margin: 0 auto; padding: 32px 24px; }
.dash-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; }
.dash-title { font-size: 20px; font-weight: 800; letter-spacing: -0.4px; }
.dash-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1px; margin-bottom: 1px; background: var(--border); }
.dash-card { background: var(--surface); border: none; padding: 20px; }
.dash-card.full { grid-column: 1 / -1; }
.dash-card h3 { font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; font-weight: 600; }
.dash-val { font-size: 22px; font-weight: 800; color: var(--accent2); letter-spacing: -0.5px; }
.dash-sub { font-size: 12px; color: var(--muted); margin-top: 4px; }
.license-box { background: var(--bg); border: 1px solid var(--border2); border-radius: var(--radius-sm); padding: 18px; text-align: center; }
.license-code { font-family: 'JetBrains Mono', monospace; font-size: 17px; font-weight: 600; color: var(--accent2); letter-spacing: 2.5px; }
.license-sub { font-size: 12px; color: var(--muted); margin-top: 6px; }
.status-badge { display: inline-flex; align-items: center; gap: 6px; padding: 3px 10px; border-radius: var(--radius-sm); font-size: 11px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; }
.status-active  { background: transparent; color: var(--success); border: 1px solid var(--success); }
.status-none    { background: transparent; color: var(--danger);  border: 1px solid var(--danger); }
.status-pending { background: transparent; color: var(--warn);    border: 1px solid var(--warn); }

/* &#9472;&#9472; MESAJ &#9472;&#9472; */
.msg-area { display: flex; flex-direction: column; gap: 10px; max-height: 320px; overflow-y: auto; padding: 4px 0; margin-bottom: 12px; }
.msg-b { max-width: 80%; padding: 10px 14px; border-radius: 0; font-size: 13px; line-height: 1.6; }
.msg-b.benim { background: var(--surface2); color: var(--text); align-self: flex-end; border-left: 2px solid var(--accent2); }
.msg-b.admin { background: var(--bg); color: var(--text2); align-self: flex-start; border: 1px solid var(--border2); }
.msg-wrap { display: flex; flex-direction: column; }
.msg-wrap.right { align-items: flex-end; }
.msg-t { font-size: 10px; color: var(--muted); margin-top: 3px; letter-spacing: 0.3px; }
.msg-input { width: 100%; background: var(--bg); border: 1px solid var(--border2); border-radius: var(--radius-sm); padding: 10px 14px; color: var(--text); font-size: 13px; font-family: 'Inter', sans-serif; resize: vertical; min-height: 72px; }
.msg-input:focus { outline: none; border-color: var(--accent); }

/* &#9472;&#9472; TALEPLER &#9472;&#9472; */
.talep-item { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius-sm); margin-bottom: 6px; }
.badge-sm { padding: 2px 8px; border-radius: 0; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; }
.b-bekl { background: transparent; color: var(--warn);    border: 1px solid var(--warn); }
.b-onay { background: transparent; color: var(--success); border: 1px solid var(--success); }
.b-red  { background: transparent; color: var(--danger);  border: 1px solid var(--danger); }

/* &#9472;&#9472; ÇEREZ BANNER &#9472;&#9472; */
#cerez-banner { position: fixed; bottom: 0; left: 0; right: 0; z-index: 9999; background: var(--surface); border-top: 1px solid var(--border2); padding: 20px 32px; display: flex; align-items: flex-start; gap: 24px; box-shadow: 0 -4px 24px rgba(0,0,0,0.4); animation: cerezSlideUp 0.35s cubic-bezier(.22,1,.36,1); }
@keyframes cerezSlideUp { from { transform: translateY(100%); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
#cerez-banner.cerez-gizle { animation: cerezSlideDown 0.3s ease forwards; }
@keyframes cerezSlideDown { to { transform: translateY(110%); opacity: 0; } }
.cerez-icerik { flex: 1; }
.cerez-baslik { font-size: 14px; font-weight: 700; color: var(--text); margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }
.cerez-aciklama { font-size: 13px; color: var(--muted); line-height: 1.65; max-width: 640px; }
.cerez-aciklama a { color: var(--text); cursor: pointer; text-decoration: underline; text-underline-offset: 2px; }
.cerez-aksiyonlar { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; flex-shrink: 0; margin-top: 4px; }
.cerez-btn { padding: 8px 18px; border-radius: var(--radius-sm); font-size: 13px; font-weight: 600; cursor: pointer; border: 1px solid var(--border2); font-family: 'Inter', sans-serif; transition: all 0.15s; white-space: nowrap; background: transparent; color: var(--text2); }
.cerez-btn:hover { border-color: var(--accent); color: var(--text); }
.cerez-btn-tum { background: var(--accent2); color: var(--bg); border-color: var(--accent2); }
.cerez-btn-tum:hover { opacity: 0.85; }
.cerez-btn-reddet { color: var(--danger); border-color: var(--danger); }
.cerez-btn-reddet:hover { background: rgba(239,68,68,0.08); }

/* Cerez Modal */
#cerez-modal-overlay { position: fixed; inset: 0; z-index: 10000; background: rgba(0,0,0,0.7); backdrop-filter: blur(4px); display: none; align-items: center; justify-content: center; padding: 16px; }
#cerez-modal-overlay.aktif { display: flex; }
#cerez-modal { background: var(--surface); border: 1px solid var(--border2); border-radius: var(--radius); width: 100%; max-width: 500px; max-height: 90vh; overflow-y: auto; padding: 28px; }
.cerez-modal-baslik { font-size: 17px; font-weight: 800; margin-bottom: 4px; letter-spacing: -0.3px; }
.cerez-modal-sub { font-size: 13px; color: var(--muted); margin-bottom: 20px; line-height: 1.6; }
.cerez-kategori { background: var(--bg); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 14px 16px; margin-bottom: 10px; }
.cerez-kat-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px; }
.cerez-kat-ad { font-size: 13px; font-weight: 700; color: var(--text); }
.cerez-kat-acik { font-size: 12px; color: var(--muted); line-height: 1.55; }
.cerez-toggle { position: relative; width: 40px; height: 22px; flex-shrink: 0; }
.cerez-toggle input { opacity: 0; width: 0; height: 0; }
.cerez-toggle-slider { position: absolute; inset: 0; border-radius: 22px; background: var(--border2); cursor: pointer; transition: background 0.2s; border: 1px solid var(--border2); }
.cerez-toggle-slider::before { content: ''; position: absolute; width: 16px; height: 16px; border-radius: 50%; background: var(--muted); bottom: 2px; left: 2px; transition: all 0.2s; }
.cerez-toggle input:checked + .cerez-toggle-slider { background: var(--accent2); border-color: var(--accent2); }
.cerez-toggle input:checked + .cerez-toggle-slider::before { transform: translateX(18px); background: var(--bg); }
.cerez-toggle input:disabled + .cerez-toggle-slider { opacity: 0.45; cursor: not-allowed; }
.cerez-zorunlu-etiket { font-size: 10px; color: var(--success); background: transparent; border: 1px solid var(--success); padding: 1px 7px; border-radius: var(--radius-sm); font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; }
.cerez-modal-alt { display: flex; gap: 8px; justify-content: flex-end; margin-top: 20px; flex-wrap: wrap; }

/* &#9472;&#9472; RESPONSIVE &#9472;&#9472; */
@media (max-width: 600px) {
  .nav { padding: 0 16px; }
  .hero { padding: 48px 16px 36px; }
  .dash-grid { grid-template-columns: 1fr; }
  .features { grid-template-columns: 1fr; }
  #cerez-banner { flex-direction: column; padding: 16px; gap: 14px; }
  .cerez-aksiyonlar { width: 100%; }
  .cerez-btn { flex: 1; text-align: center; }
}
</style>
""""""

SITE_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="tr" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nautilus Technology | Endüstriyel Gateway ve Otomasyon Çözümleri</title>
<meta name="description" content="Nautilus Technology, endüstriyel tesislerin dijital dönüşümü için güvenilir OPC UA / OPC DA tabanlı Gateway ve otomasyon yazılımları geliştirir.">
<meta name="keywords" content="Nautilus Technology,nautilus, opc, plc, ua,da, gateway, endüstriyel gateway, OPC UA, OPC DA, otomasyon yazılımı, endüstriyel yazılım, scada entegrasyonu">
<meta name="author" content="Nautilus Technology">
<meta name="google-site-verification" content="5PWZlgIA2ix0hNSBohcMBFv76V76GvmZN7-5mLJMF3k" />

{CSS}
</head>
<body>

<!-- ===== ÇEREZ ONAYI BANNER ===== -->
<div id="cerez-banner" style="display:none;">
  <div class="cerez-icerik">
    <div class="cerez-baslik">&#127850; Çerez Politikası</div>
    <div class="cerez-aciklama">
      Bu site yalnızca <strong>zorunlu oturum çerezleri</strong> kullanmaktadır. Oturum çerezi, giriş yaptıktan sonra kimliğinizi doğrulamak için gereklidir; reklam, izleme veya pazarlama amaçlı herhangi bir çerez kullanılmamaktadır.
      <a onclick="cerezAyarlariAc()">Çerez tercihlerini yönet &rarr;</a>
    </div>
  </div>
  <div class="cerez-aksiyonlar">
    <button class="cerez-btn cerez-btn-tum"     onclick="cerezKabulEt('tum')">Tümünü Kabul Et</button>
    <button class="cerez-btn cerez-btn-zorunlu" onclick="cerezKabulEt('zorunlu')">Yalnızca Zorunlu</button>
    <button class="cerez-btn cerez-btn-reddet"  onclick="cerezKabulEt('reddet')">Reddet</button>
    <button class="cerez-btn cerez-btn-ayarlar" onclick="cerezAyarlariAc()">Tercihler</button>
  </div>
</div>

<!-- ===== ÇEREZ TERCİH MODALI ===== -->
<div id="cerez-modal-overlay">
  <div id="cerez-modal">
    <div class="cerez-modal-baslik">&#127850; Çerez Tercihleri</div>
    <div class="cerez-modal-sub">
      Aşağıdaki kategorileri dilediğiniz gibi etkinleştirip devre dışı bırakabilirsiniz.
      Zorunlu çerezler sitenin temel işlevleri için gereklidir ve devre dışı bırakılamaz.
    </div>

    <!-- Zorunlu Çerezler -->
    <div class="cerez-kategori">
      <div class="cerez-kat-header">
        <div>
          <div class="cerez-kat-ad">Zorunlu Çerezler</div>
        </div>
        <div style="display:flex;align-items:center;gap:8px;">
          <span class="cerez-zorunlu-etiket">Her Zaman Aktif</span>
          <label class="cerez-toggle">
            <input type="checkbox" checked disabled>
            <span class="cerez-toggle-slider"></span>
          </label>
        </div>
      </div>
      <div class="cerez-kat-acik">
        <strong>session</strong> &mdash; Giriş yaptıktan sonra kimliğinizi doğrulamak için kullanılır. 7 gün boyunca geçerlidir.
        Oturum kapatıldığında veya süre dolduğunda otomatik olarak silinir. Bu çerez olmadan sisteme giriş yapamazsınız.
      </div>
    </div>

    <!-- Fonksiyonel Çerezler -->
    <div class="cerez-kategori">
      <div class="cerez-kat-header">
        <div>
          <div class="cerez-kat-ad">Fonksiyonel Çerezler</div>
        </div>
        <label class="cerez-toggle">
          <input type="checkbox" id="cerez-toggle-fonk" checked>
          <span class="cerez-toggle-slider"></span>
        </label>
      </div>
      <div class="cerez-kat-acik">
        <strong>cookie_consent</strong> &mdash; Çerez tercihlerinizi hatırlamak için kullanılır (1 yıl geçerli).
        Bu çerezi devre dışı bırakırsanız her ziyarette tekrar onay kutusu görüntülenir.
      </div>
    </div>

    <!-- Analitik -->
    <div class="cerez-kategori" style="opacity:0.6;">
      <div class="cerez-kat-header">
        <div>
          <div class="cerez-kat-ad">Analitik Çerezler</div>
        </div>
        <label class="cerez-toggle">
          <input type="checkbox" id="cerez-toggle-analitik" disabled>
          <span class="cerez-toggle-slider"></span>
        </label>
      </div>
      <div class="cerez-kat-acik">
        Bu site şu an herhangi bir analitik çerez kullanmamaktadır. İleride eklenirse burada listelenecektir.
      </div>
    </div>

    <!-- Pazarlama -->
    <div class="cerez-kategori" style="opacity:0.6;">
      <div class="cerez-kat-header">
        <div>
          <div class="cerez-kat-ad">Pazarlama / Reklam Çerezleri</div>
        </div>
        <label class="cerez-toggle">
          <input type="checkbox" id="cerez-toggle-reklam" disabled>
          <span class="cerez-toggle-slider"></span>
        </label>
      </div>
      <div class="cerez-kat-acik">
        Bu site herhangi bir reklam veya izleme çerezi kullanmamaktadır.
      </div>
    </div>

    <div class="cerez-modal-alt">
      <button class="cerez-btn cerez-btn-zorunlu" onclick="cerezModalKapat()">İptal</button>
      <button class="cerez-btn cerez-btn-reddet"  onclick="cerezKabulEt('reddet')">Reddet</button>
      <button class="cerez-btn cerez-btn-tum"     onclick="cerezAyarlariKaydet()">Seçimlerimi Kaydet</button>
    </div>
  </div>
</div>

<nav class="nav">
  <div class="nav-brand">
    <img src="/static/logo.png" alt="Nautilus Technology" class="nav-logo" onerror="this.style.display='none'">
    <div class="nav-brand-text">
      Nautilus Technology
      <span>OPC Gateway Lisans</span>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:8px;">
    <div id="nav-quick-links" style="display:flex;align-items:center;gap:6px;"></div>
    <div class="nav-links" id="nav-links">
      <button class="nav-btn nav-btn-ghost" onclick="sayfaGoster('giris')">Giriş Yap</button>
      <button class="nav-btn nav-btn-primary" onclick="sayfaGoster('kayit')">Kayıt Ol</button>
    </div>
    <button id="theme-toggle" onclick="temaToggle()" title="Tema Değiştir">
      <span id="theme-icon">&#9790;</span>
    </button>
  </div>
</nav>

<!-- ANASAYFA -->
<div id="sayfa-anasayfa">
  <div class="hero">
    <div class="hero-badge">&#9889; OPC Gateway Lisans Sistemi</div>
    <h1>Endüstriyel Otomasyon<br><span>Lisans Yönetimi</span></h1>
    <p>OPC Gateway yazılımı için güvenli, hızlı ve kolay lisans aktivasyon sistemi.</p>
    <div class="hero-btns">
      <button class="btn-hero btn-hero-primary" onclick="sayfaGoster('kayit')">Hemen Başla &rarr;</button>
      <button class="btn-hero btn-hero-ghost" onclick="sayfaGoster('planlar')">Planları İncele</button>
    </div>
  </div>

  <div class="features">
    <div class="feature">
      <div class="feature-icon">&#128272;</div>
      <h3>Güvenli Aktivasyon</h3>
      <p>HWID tabanlı lisans sistemi ile yazılımınızı yetkisiz kullanıma karşı koruyun.</p>
    </div>
    <div class="feature">
      <div class="feature-icon">&#9889;</div>
      <h3>Anında Aktivasyon</h3>
      <p>Lisans kodunu aldıktan sonra saniyeler içinde programınızı aktive edin.</p>
    </div>
    <div class="feature">
      <div class="feature-icon">&#128172;</div>
      <h3>7/24 Destek</h3>
      <p>Hesabınızdaki destek sistemi üzerinden doğrudan ekibimize ulaşın.</p>
    </div>
    <div class="feature">
      <div class="feature-icon">&#128260;</div>
      <h3>Esnek Planlar</h3>
      <p>Aylık, yıllık veya ömür boyu seçeneklerden ihtiyacınıza uygun planı seçin.</p>
    </div>
  </div>
</div>

<!-- PLANLAR -->
<div id="sayfa-planlar" style="display:none">
  <div style="height:48px;"></div>
  <div class="plans-section">
    <div class="section-title">Lisans Planları</div>
    <div class="section-sub">İhtiyacınıza göre bir plan seçin</div>
    <div class="plans" id="plan-listesi">
      <div style="text-align:center;color:var(--muted);grid-column:1/-1;padding:40px;">Planlar yükleniyor...</div>
    </div>
    <div style="text-align:center;margin-top:32px;">
      <button class="btn-hero btn-hero-primary" onclick="sayfaGoster('kayit')">Kayıt Ol ve Talep Gönder &rarr;</button>
    </div>
  </div>
</div>

<!-- OFFLİNE AKTİVASYON -->
<div id="sayfa-offline" style="display:none">
  <div style="height:48px;"></div>
  <div class="form-container" style="max-width:520px;">
    <div class="form-card">
      <div class="form-title">&#128274; Offline Aktivasyon Talebi</div>
      <div class="form-sub">İnternet bağlantısı olmayan sistemler için lisans talebinde bulunun. Giriş yapmış olmanız gerekir.</div>
      <div class="form-err" id="offline-hata"></div>
      <div class="form-ok" id="offline-ok"></div>
      <div id="offline-giris-uyari" style="display:none;background:#f59e0b15;border:1px solid #f59e0b44;color:#fbbf24;border-radius:8px;padding:12px 16px;font-size:13px;margin-bottom:16px;">
        &#9888; Offline aktivasyon talebi göndermek için önce <a onclick="sayfaGoster('giris')" style="color:#3d6fff;cursor:pointer;font-weight:600;">giriş yapmalısınız</a>.
      </div>
      <div id="offline-form-icerik">
        <div class="form-group">
          <label class="form-label">Lisans Türü</label>
          <select class="form-input" id="off-tur-sec"><option value="">Yükleniyor...</option></select>
        </div>
        <div class="form-group">
          <label class="form-label">Gateway İstek Kodu (REQ-...)</label>
          <input class="form-input" type="text" id="off-req-kod" placeholder="REQ-XXXXXXXXXXXXXXXXXXXX" style="font-family:monospace;letter-spacing:1px;" oninput="offReqKodKontrol()">
          <div id="off-req-durum" style="font-size:12px;margin-top:4px;"></div>
        </div>
        <div style="background:#3d6fff0a;border:1px solid #3d6fff22;border-radius:8px;padding:12px 14px;font-size:12px;color:#8a9bc0;margin-bottom:16px;line-height:1.7;">
          &#128268; İstek kodunu almak için <b>OPC Gateway Pro</b> programını açıp <b>Offline Aktivasyon &rarr; İstek Kodu Oluştur</b> seçeneğini kullanın.
        </div>
        <button class="form-btn" id="off-talep-btn" onclick="offlineTalepGonder()">Offline Lisans Talebi Gönder</button>
      </div>
    </div>
  </div>
</div>

<!-- KAYIT -->
<div id="sayfa-kayit" style="display:none">
  <div style="height:48px;"></div>
  <div class="form-container">
    <div class="form-card">
      <div class="form-title">Hesap Oluştur</div>
      <div class="form-sub">Zaten hesabınız var mı? <a onclick="sayfaGoster('giris')">Giriş yapın</a></div>
      <div class="form-err" id="kayit-hata"></div>
      <div class="form-ok" id="kayit-ok"></div>
      <div class="form-group">
        <label class="form-label">Ad Soyad</label>
        <input class="form-input" type="text" id="r-ad" placeholder="Adınız Soyadınız">
      </div>
      <div class="form-group">
        <label class="form-label">E-posta</label>
        <input class="form-input" type="email" id="r-email" placeholder="ornek@email.com">
      </div>
      <div class="form-group">
        <label class="form-label">Şifre</label>
        <input class="form-input" type="password" id="r-sifre" placeholder="En az 6 karakter">
      </div>
      <button class="form-btn" onclick="kayitOl()">Hesap Oluştur</button>
      <div class="form-alt">Kayıt olarak <a href="#" style="color:var(--accent)">kullanım koşullarını</a> kabul etmiş olursunuz.</div>
    </div>
  </div>
</div>

<!-- GİRİŞ -->
<div id="sayfa-giris" style="display:none">
  <div style="height:48px;"></div>
  <div class="form-container">
    <div class="form-card">
      <div class="form-title">Giriş Yap</div>
      <div class="form-sub">Hesabınız yok mu? <a onclick="sayfaGoster('kayit')">Kayıt olun</a></div>
      <div class="form-err" id="giris-hata"></div>
      <div class="form-ok" id="giris-ok"></div>
      <div class="form-group">
        <label class="form-label">E-posta</label>
        <input class="form-input" type="email" id="g-email" placeholder="ornek@email.com">
      </div>
      <div class="form-group">
        <label class="form-label">Şifre</label>
        <input class="form-input" type="password" id="g-sifre" placeholder="Şifreniz" onkeydown="if(event.key==='Enter')girisYap()">
      </div>
      <button class="form-btn" onclick="girisYap()">Giriş Yap</button>
      <div class="form-alt">Hesabınız yok mu? <a onclick="sayfaGoster('kayit')">Kayıt olun</a></div>
    </div>
  </div>
</div>

<!-- DASHBOARD -->
<div id="sayfa-dashboard" style="display:none">
  <div class="dashboard">
    <div class="dash-header">
      <div class="dash-title" id="dash-hosgeldin">Hoş Geldiniz</div>
      <button class="nav-btn nav-btn-ghost" onclick="cikisYap()" style="font-size:13px;">Çıkış</button>
    </div>

    <div class="dash-grid" id="dash-grid">
      <!-- JS ile doldurulacak -->
    </div>

    <!-- Lisans Talebi -->
    <div class="dash-card full" id="talep-section">
      <h3>Lisans Talebi</h3>
      <div id="talep-icerik"></div>
    </div>

    <!-- Lisans Geçmişi -->
    <div class="dash-card full" id="gecmis-section">
      <h3 style="display:flex;align-items:center;justify-content:space-between;">
        <span>&#128267; Lisans Geçmişi</span>
        <button onclick="lisansGecmisiniYukle()" style="background:transparent;border:1px solid var(--border);color:var(--muted);border-radius:6px;padding:4px 12px;font-size:12px;cursor:pointer;">&#8635; Yenile</button>
      </h3>
      <div id="gecmis-icerik"><div style="color:var(--muted);font-size:13px;">Yükleniyor&hellip;</div></div>
    </div>

    <!-- Mesajlar -->
    <div class="dash-card full">
      <h3>Destek / Mesajlar</h3>
      <div class="msg-area" id="msg-area"></div>
      <textarea class="msg-input" id="msg-yaz" placeholder="Mesajınızı yazın&hellip; (Ctrl+Enter ile gönder)" onkeydown="if(event.ctrlKey&&event.key==='Enter')mesajGonder()"></textarea>
      <button class="form-btn" style="margin-top:8px;padding:10px;" onclick="mesajGonder()">Gönder</button>
    </div>

    <!-- Şifre Değiştirme -->
    <div style="margin-top:32px; padding-top:16px; border-top:1px solid var(--border); text-align:center;">
      <div style="display:flex; justify-content:center; align-items:center; gap:8px;">
        <input type="password" id="k-yeni-sifre" placeholder="Yeni şifreniz (en az 6 karakter)" style="background:transparent; border:1px solid var(--border); border-radius:6px; padding:6px 12px; font-size:12px; color:var(--text); width:200px;">
        <button onclick="kullaniciSifreDegistir()" style="background:transparent; border:1px solid var(--border); color:var(--muted); padding:6px 12px; border-radius:6px; font-size:12px; cursor:pointer; font-weight:600;">Şifremi Değiştir</button>
      </div>
      <div style="font-size:10px; color:var(--muted); margin-top:6px;">Hesabınızın şifresini eski şifrenizi girmeden hızlıca değiştirebilirsiniz.</div>
    </div>
  </div>
</div>

<!-- İPTAL MODALı -->
<div id="iptal-modal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.75);z-index:500;align-items:center;justify-content:center;backdrop-filter:blur(6px);">
  <div style="background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:32px;width:480px;max-width:95vw;">
    <div style="font-size:18px;font-weight:700;color:#f87171;margin-bottom:6px;">&#9888; Lisansı İptal Et</div>
    <div style="font-size:13px;color:var(--muted);margin-bottom:20px;">Bu işlem geri alınamaz. Lisansınız iptal edildikten sonra programı kullanamazsınız.</div>
    <div style="font-size:13px;font-weight:500;margin-bottom:8px;color:#8a9bc0;">Neden iptal ediyorsunuz?</div>
    <select id="iptal-neden-sec" style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:10px 14px;color:var(--text);font-size:13px;font-family:'Sora',sans-serif;margin-bottom:8px;">
      <option value="">-- Neden seçin --</option>
      <option value="Artık kullanmıyorum">Artık kullanmıyorum</option>
      <option value="Fiyatı çok yüksek">Fiyatı çok yüksek</option>
      <option value="Başka bir yazılıma geçtim">Başka bir yazılıma geçtim</option>
      <option value="Teknik sorunlar">Teknik sorunlar</option>
      <option value="Geçici iptal">Geçici iptal</option>
      <option value="Diğer">Diğer</option>
    </select>
    <textarea id="iptal-aciklama" style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:10px 14px;color:var(--text);font-size:13px;font-family:'Sora',sans-serif;min-height:60px;resize:vertical;margin-bottom:16px;" placeholder="Ek açıklama (isteğe bağlı)"></textarea>
    <div id="iptal-hata" style="color:#f87171;font-size:13px;margin-bottom:12px;display:none;"></div>
    <div style="display:flex;gap:10px;">
      <button onclick="lisansImIptalEt()" style="flex:1;background:linear-gradient(135deg,#ef4444,#b91c1c);color:white;border:none;border-radius:8px;padding:12px;font-size:14px;font-weight:700;cursor:pointer;font-family:'Sora',sans-serif;">Evet, İptal Et</button>
      <button onclick="iptalModalKapat()" style="flex:1;background:transparent;color:var(--muted);border:1px solid var(--border);border-radius:8px;padding:12px;font-size:14px;font-weight:600;cursor:pointer;font-family:'Sora',sans-serif;">Vazgeç</button>
    </div>
  </div>
</div>

<script>
let planlar = [];

// ===== SAYFA YÖNETİMİ =====
function sayfaGoster(ad) {
  ["anasayfa","planlar","kayit","giris","dashboard","offline"].forEach(s => {
    document.getElementById("sayfa-" + s).style.display = s === ad ? "" : "none";
  });
  if (ad === "planlar") planlariYukle();
  if (ad === "dashboard") dashboardYukle();
  if (ad === "offline") offlineSayfasiYukle();
}

// ===== PLANLAR =====
async function planlariYukle() {
  const r = await fetch("/api/uyelik-turleri-public");
  planlar = await r.json();
  const el = document.getElementById("plan-listesi");
  if (!planlar.length) { el.innerHTML = '<div style="text-align:center;color:var(--muted);grid-column:1/-1;padding:40px;">Henüz plan eklenmemiş.</div>'; return; }
  el.innerHTML = planlar.map(p => `
    <div class="plan-card" id="plan-${p.kod}" onclick="planSec('${p.kod}')">
      <div class="plan-name">${p.ad} ${p.is_offline ? '&#128274;' : ''}</div>
      <div class="plan-desc">${p.aciklama||""}</div>
    </div>`).join("");
}

var secilenPlan = null;
function planSec(kod) {
  secilenPlan = kod;
  document.querySelectorAll(".plan-card").forEach(c => c.classList.remove("selected"));
  const el = document.getElementById("plan-" + kod);
  if (el) el.classList.add("selected");
}

// ===== KAYIT =====
async function kayitOl() {
  const ad    = document.getElementById("r-ad").value.trim();
  const email = document.getElementById("r-email").value.trim();
  const sifre = document.getElementById("r-sifre").value;
  mesajGizle("kayit-hata"); mesajGizle("kayit-ok");

  if (!ad || !email || !sifre) {
    mesajGoster("kayit-hata", "&#9888; Tüm alanları doldurun.");
    return;
  }

  // Butonu devre dışı bırak
  const btn = document.querySelector("#sayfa-kayit .form-btn");
  if (btn) { btn.disabled = true; btn.textContent = "Kayıt yapılıyor&hellip;"; }

  const r = await fetch("/api/kayit", {method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({ad_soyad: ad, email, sifre})});
  const d = await r.json();

  if (btn) { btn.disabled = false; btn.textContent = "Hesap Oluştur"; }

  if (r.ok) {
    // Geri sayımlı yönlendirme
    let saniye = 3;
    mesajGoster("kayit-ok", `&#9989; Kayıt başarılı! Giriş sayfasına yönlendiriliyorsunuz (${saniye})&hellip;`);
    const sayac = setInterval(() => {
      saniye--;
      if (saniye <= 0) {
        clearInterval(sayac);
        mesajGizle("kayit-ok");
        sayfaGoster("giris");
      } else {
        mesajGoster("kayit-ok", `&#9989; Kayıt başarılı! Giriş sayfasına yönlendiriliyorsunuz (${saniye})&hellip;`);
      }
    }, 1000);
  } else {
    const hata = d.detail || "Bir hata oluştu.";
    mesajGoster("kayit-hata", "&#10060; " + hata);
  }
}

// ===== GİRİŞ =====
async function girisYap() {
  const email = document.getElementById("g-email").value.trim();
  const sifre = document.getElementById("g-sifre").value;
  mesajGizle("giris-hata"); mesajGizle("giris-ok");

  if (!email || !sifre) {
    mesajGoster("giris-hata", "&#9888; Lütfen e-posta ve şifrenizi girin.");
    return;
  }

  const btn = document.querySelector("#sayfa-giris .form-btn");
  if (btn) { btn.disabled = true; btn.textContent = "Giriş yapılıyor&hellip;"; }

  const r = await fetch("/api/giris", {method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({email, sifre})});
  const d = await r.json();

  if (btn) { btn.disabled = false; btn.textContent = "Giriş Yap"; }

  if (r.ok) {
    mesajGoster("giris-ok", "&#9989; Giriş başarılı! Yönlendiriliyorsunuz&hellip;");
    setTimeout(() => {
      mesajGizle("giris-ok");
      sayfaGoster("dashboard");
      baslatSitePoll();
    }, 1200);
  } else {
    // Kullanıcı dostu hata mesajları
    let hata = d.detail || "";
    if (!hata || hata.toLowerCase().includes("e-posta") || hata.toLowerCase().includes("sifre") || hata.toLowerCase().includes("şifre") || r.status === 401) {
      hata = "&#10060; E-posta adresi veya şifre yanlış. Lütfen tekrar deneyin.";
    } else {
      hata = "&#10060; " + hata;
    }
    mesajGoster("giris-hata", hata);
    // Yanlış girişte şifre alanını temizle ve odaklan
    document.getElementById("g-sifre").value = "";
    document.getElementById("g-sifre").focus();
  }
}

// ===== ÇIKIŞ & AYARLAR =====
async function kullaniciSifreDegistir() {
  const ys = document.getElementById("k-yeni-sifre").value.trim();
  if (!ys || ys.length < 6) { alert("Şifre en az 6 karakter olmalıdır."); return; }
  if (!confirm("Şifrenizi değiştirmek istediğinize emin misiniz?")) return;
  try {
    const r = await fetch("/api/sifre-degistir", {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify({yeni_sifre: ys})
    });
    if (r.ok) {
      alert("Şifreniz başarıyla değiştirildi.");
      document.getElementById("k-yeni-sifre").value = "";
    } else {
      const d = await r.json();
      alert("Hata: " + (d.detail || "İşlem başarısız."));
    }
  } catch(e) { alert("Sunucuyla iletişim kurulamadı."); }
}

async function cikisYap() {
  await fetch("/api/cikis", {method:"POST"});
  location.reload();
}

// ===== DASHBOARD =====
function lisansGridRender(p, grid) {
  if (!grid) return;
  const l = p.lisans;
  if (!l) {
    grid.innerHTML = `
      <div class="dash-card full">
        <h3>Lisans Durumu</h3>
        <span class="status-badge status-none">&#9679; Lisans Yok</span>
        <div class="dash-sub" style="margin-top:8px;">Aşağıdan lisans talebinde bulunabilirsiniz.</div>
      </div>`;
    return;
  }
  if (l.durum === "aktif") {
    grid.innerHTML = `
      <div class="dash-card">
        <h3>Lisans Durumu</h3>
        <span class="status-badge status-active">&#9679; Aktif</span>
        <div class="dash-sub" style="margin-top:8px;">${l.tur}</div>
      </div>
      <div class="dash-card">
        <h3>Kalan Süre</h3>
        <div class="dash-val">${l.kalan_gun != null ? l.kalan_gun + " gün" : "Ömür Boyu"}</div>
        <div class="dash-sub">Bitiş: ${l.bitis}</div>
      </div>
      <div class="dash-card full">
        <h3>Lisans Kodunuz</h3>
        <div class="license-box">
          <div class="license-code">${l.kod}</div>
          <div class="license-sub">Bu kodu program aktivasyonunda kullanın</div>
        </div>
      </div>
      ${(p.indirme_linki && p.vt_hash) ? `
      <div class="dash-card full" style="text-align:center;">
        ${(p.yeni_surum_banner && p.son_guncelleme) ? `
        <div style="margin-bottom:14px;">
          <span style="display:inline-block;background:linear-gradient(90deg,#22d3ee,#38bdf8);color:#fff;padding:8px 20px;border-radius:20px;font-size:14px;font-weight:700;box-shadow:0 4px 12px #38bdf844;letter-spacing:0.5px;border:1px solid #ffffff33;">&#128640; YENİ SÜRÜM YAYINDA! (${p.son_guncelleme})</span>
        </div>` : ''}
        <h3>Program İndir</h3>
        <div class="dash-sub" style="margin-bottom:16px;">Lisansınız aktif. Programı indirip lisans kodunuzla aktive edebilirsiniz.</div>
        <a href="${p.indirme_linki}" target="_blank" style="display:inline-flex;align-items:center;gap:10px;background:linear-gradient(135deg,var(--success),#16a34a);color:white;padding:14px 32px;border-radius:10px;font-size:15px;font-weight:700;text-decoration:none;box-shadow:0 0 24px #22c55e33;transition:all 0.2s;">
          &#11015; OPC Gateway'i İndir
        </a>
        <div style="margin-top:18px;">
          <a href="https://www.virustotal.com/gui/file/${p.vt_hash}" target="_blank" style="display:inline-flex;align-items:center;gap:8px;background:linear-gradient(90deg,#22c55e,#16a34a);color:white;padding:10px 22px;border-radius:8px;font-size:14px;font-weight:600;text-decoration:none;box-shadow:0 0 12px #22c55e33;transition:all 0.2s;">
            &#128737; VirusTotal Güvenlik Raporu (0 Virüs)
          </a>
        </div>
      </div>` : ''}
      <div class="dash-card full" style="text-align:center;padding-top:8px;">
        <button onclick="iptalModalAc()" style="background:transparent;border:1px solid #ef444455;color:#f87171;border-radius:8px;padding:9px 20px;font-size:13px;font-weight:600;cursor:pointer;font-family:'Sora',sans-serif;transition:all 0.2s;" onmouseover="this.style.background='#ef444415'" onmouseout="this.style.background='transparent'">
          &#9888; Lisansı İptal Et
        </button>
      </div>`;
  } else if (l.durum === "suresi_dolmus") {
    grid.innerHTML = `
      <div class="dash-card full">
        <h3>Lisans Durumu</h3>
        <span class="status-badge" style="background:#f59e0b15;color:#fbbf24;border:1px solid #f59e0b33;">&#9679; Süresi Dolmuş</span>
        <div class="dash-sub" style="margin-top:8px;">${l.tur} &middot; Bitiş: ${l.bitis}</div>
        <div class="dash-sub" style="margin-top:6px;color:#7eb8ff;">Lisans kodunuz: <strong style="font-family:monospace;">${l.kod}</strong></div>
        <div class="dash-sub" style="margin-top:8px;">Süreniz dolmuş. Yenilemek için aşağıdan yeni bir talep gönderin.</div>
      </div>`;
  } else if (l.durum === "iptal") {
    grid.innerHTML = `
      <div class="dash-card full">
        <h3>Lisans Durumu</h3>
        <span class="status-badge status-none">&#9679; İptal Edildi</span>
        <div class="dash-sub" style="margin-top:8px;">${l.tur} &middot; Lisans kodunuz: <strong style="font-family:monospace;">${l.kod}</strong></div>
        ${l.iptal_nedeni ? `<div class="dash-sub" style="margin-top:6px;">Neden: ${l.iptal_nedeni}</div>` : ''}
        <div class="dash-sub" style="margin-top:8px;">Yeni lisans için aşağıdan talep gönderebilirsiniz.</div>
      </div>`;
  }
}

async function dashboardYukle() {
  const r = await fetch("/api/profil");
  if (!r.ok) { sayfaGoster("giris"); return; }
  const p = await r.json();
  document.getElementById("dash-hosgeldin").textContent = "Merhaba, " + p.ad_soyad + " &#128075;";
  document.getElementById("nav-links").innerHTML = `<span style="font-size:13px;color:var(--muted);margin-right:8px;">${p.email}</span><button class="nav-btn nav-btn-ghost" onclick="cikisYap()">Cıkış</button>`;
  lisansGridRender(p, document.getElementById("dash-grid"));
  taleplerYukle();
  lisansGecmisiniYukle();
  mesajlariYukle();
}

// Dashboard lisans kartını sessizce güncelle
async function lisansKartiGuncelle() {
  const r = await fetch("/api/profil");
  if (!r.ok) return;
  const p = await r.json();
  lisansGridRender(p, document.getElementById("dash-grid"));
}

function iptalModalAc() {
  document.getElementById("iptal-neden-sec").value = "";
  document.getElementById("iptal-aciklama").value = "";
  const hataEl = document.getElementById("iptal-hata");
  if (hataEl) hataEl.style.display = "none";
  document.getElementById("iptal-modal").style.display = "flex";
}

function iptalModalKapat() {
  document.getElementById("iptal-modal").style.display = "none";
}

async function lisansImIptalEt() {
  const sec = document.getElementById("iptal-neden-sec").value;
  const aciklama = document.getElementById("iptal-aciklama").value.trim();
  const hataEl = document.getElementById("iptal-hata");
  if (!sec) {
    hataEl.textContent = "&#9888; Lütfen bir neden seçin.";
    hataEl.style.display = "block";
    return;
  }
  const neden = aciklama ? `${sec} &mdash; ${aciklama}` : sec;
  const r = await fetch("/api/lisansimi-iptal-et", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({neden})
  });
  const d = await r.json();
  if (r.ok) {
    iptalModalKapat();
    lisansKartiGuncelle();
    lisansGecmisiniYukle();
    taleplerYukle();
  } else {
    hataEl.textContent = "&#10060; " + (d.detail || "Bir hata oluştu.");
    hataEl.style.display = "block";
  }
}

// Global state - poll yenilemesinde offline seçimi ve REQ kodu kaybolmasın
// var dashSecilenPlan = null;
let _dashTalepTipi  = "online";
let _dashReqKodu    = "";


async function taleplerYukle() {

  const r = await fetch("/api/benim-taleplerim");
  const talepler = await r.json();
  const durumBadge = {beklemede:"b-bekl",onaylandi:"b-onay",reddedildi:"b-red"};
  const durumYazi = {beklemede:"Beklemede",onaylandi:"Onaylandı",reddedildi:"Reddedildi"};
  let html = "";
  talepler.forEach(t => {
    let aktGosterim = (t.talep_tipi === 'offline' && t.aktivasyon_kodu) ? `<div style="font-size:11px;margin-top:6px;color:#4ade80;font-family:monospace;background:#22c55e15;padding:6px 10px;border-radius:4px;display:inline-block;border:1px solid #22c55e44;">Aktivasyon Kodunuz:<br>${t.aktivasyon_kodu}</div>` : '';
    html += `<div class="talep-item">
      <div>
        <div style="font-size:14px;font-weight:600;">${t.tur} <span style="font-size:10px;padding:2px 6px;border-radius:4px;background:#3d6fff22;color:#3d6fff;margin-left:6px;border:1px solid #3d6fff44;">${(t.talep_tipi || 'online').toUpperCase()}</span></div>
        <div style="font-size:12px;color:var(--muted);">${t.tarih}${t.admin_notu ? " &middot; " + t.admin_notu : ""}</div>
        ${aktGosterim}
      </div>
      <span class="badge-sm ${durumBadge[t.durum]||""}">${durumYazi[t.durum]||t.durum}</span>
    </div>`;
  });

  // Yeni talep formu (lisans yoksa ve bekleyen talep yoksa)
  const bekleyen = talepler.find(t => t.durum === "beklemede");
  if (!bekleyen) {
    const planlarResp = await fetch("/api/uyelik-turleri-public");
    const planlarData = await planlarResp.json();
    html += `<div style="margin-top:16px;">
      <div style="font-size:13px;color:var(--muted);margin-bottom:12px;">Yeni lisans talep edin:</div>

      <div style="display:flex;gap:0;margin-bottom:16px;background:var(--surface);border-radius:8px;border:1px solid var(--border);overflow:hidden;">
        <label style="flex:1;font-size:13px;display:flex;align-items:center;gap:8px;cursor:pointer;padding:10px 16px;" id="lbl-online">
          <input type="radio" name="talep_tipi" value="online" ${_dashTalepTipi !== 'offline' ? 'checked' : ''} onchange="talepTipiDegisti()">
          <span>&#127760;</span> <span>Online Lisans</span>
        </label>
        <div style="width:1px;background:var(--border);"></div>
        <label style="flex:1;font-size:13px;display:flex;align-items:center;gap:8px;cursor:pointer;padding:10px 16px;" id="lbl-offline">
          <input type="radio" name="talep_tipi" value="offline" ${_dashTalepTipi === 'offline' ? 'checked' : ''} onchange="talepTipiDegisti()">
          <span>&#128274;</span> <span>Offline Lisans</span>
        </label>
      </div>

      <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px;">
        ${planlarData.map(p => `<div class="plan-card ${dashSecilenPlan === p.kod ? 'selected' : ''}" id="dp-${p.kod}" onclick="dashPlanSec('${p.kod}')" style="padding:12px 16px;min-width:140px;cursor:pointer;">
          <div style="font-size:13px;font-weight:600;">${p.ad} ${p.is_offline ? '&#128274;' : ''}</div>
          <div style="font-size:11px;color:var(--muted);margin-top:3px;">${p.aciklama||""}</div>
        </div>`).join("")}
      </div>

      <div id="offline-istek-alan" style="display:${_dashTalepTipi === 'offline' ? '' : 'none'};margin-bottom:14px;background:#3d6fff08;border:1px solid #3d6fff22;border-radius:8px;padding:14px;">
        <label style="font-size:12px;color:#8a9bc0;display:block;margin-bottom:6px;font-weight:600;">Gateway İstek Kodu</label>
        <input type="text" id="talep-istek-kodu" placeholder="REQ-XXXXXXXXXXXXXXXXXXXX"
          class="form-input" style="font-family:monospace;letter-spacing:1px;max-width:360px;margin-bottom:4px;"
          value="${_dashReqKodu.replace(/"/g, '&quot;')}"
          oninput="_dashReqKodu=this.value;dashReqKodKontrol()">
        <div id="dash-req-durum" style="font-size:12px;min-height:18px;"></div>
        <div style="font-size:11px;color:var(--muted);margin-top:8px;line-height:1.6;">
          &#128268; İstek kodunu almak için <b>OPC Gateway Pro</b> programını açıp <b>Offline Aktivasyon &rarr; İstek Kodu Oluştur</b> seçeneğini kullanın.
        </div>
      </div>

      <button class="form-btn" id="talep-gonder-btn" style="max-width:220px;padding:10px;" onclick="talepGonder()">${_dashTalepTipi === 'offline' ? '&#128274; Offline Talep Gönder' : '&#127760; Online Talep Gönder'}</button>
      <div class="form-err" id="talep-hata" style="margin-top:10px;"></div>
      <div class="form-ok" id="talep-ok" style="margin-top:10px;"></div>
    </div>`;
  }
  document.getElementById("talep-icerik").innerHTML = html;
  // Re-render sonrası kaydedilen REQ kodunu input'a geri yaz (polling sırasında silinmesin)
  if (_dashTalepTipi === 'offline' && _dashReqKodu) {
    const reqEl = document.getElementById("talep-istek-kodu");
    if (reqEl && reqEl !== document.activeElement) {
      reqEl.value = _dashReqKodu;
    }
    dashReqKodKontrol();
  }
}

function talepTipiDegisti() {
  const tip = document.querySelector('input[name="talep_tipi"]:checked');
  if (!tip) return;
  _dashTalepTipi = tip.value; // Global state'i güncelle
  const alan = document.getElementById("offline-istek-alan");
  const btn  = document.getElementById("talep-gonder-btn");
  if (alan) alan.style.display = tip.value === "offline" ? "" : "none";
  if (btn)  btn.textContent   = tip.value === "offline" ? "&#128274; Offline Talep Gönder" : "&#127760; Online Talep Gönder";
}

function dashReqKodKontrol() {
  const val = (document.getElementById("talep-istek-kodu").value || "").trim().toUpperCase();
  const el  = document.getElementById("dash-req-durum");
  if (!el) return;
  if (!val) { el.textContent = ""; return; }
  if (!val.startsWith("REQ-") || val.length < 10) {
    el.style.color = "#f87171";
    el.textContent = "&#9888; Geçersiz format &mdash; REQ- ile başlamalı ve yeterince uzun olmalıdır.";
  } else {
    el.style.color = "#4ade80";
    el.textContent = "&#10003; Format geçerli.";
  }
}

var dashSecilenPlan = null;
function dashPlanSec(kod) {
  dashSecilenPlan = kod;
  document.querySelectorAll("[id^='dp-']").forEach(c => c.classList.remove("selected"));
  const el = document.getElementById("dp-" + kod);
  if (el) el.classList.add("selected");
}

// ===== OFFLİNE AKTİVASYON SAYFASI =====
async function offlineSayfasiYukle() {
  // Oturum kontrolü
  const r = await fetch("/api/profil");
  const uyariEl = document.getElementById("offline-giris-uyari");
  const formEl  = document.getElementById("offline-form-icerik");
  if (!r.ok) {
    if (uyariEl) uyariEl.style.display = "";
    if (formEl)  formEl.style.display  = "none";
    return;
  }
  if (uyariEl) uyariEl.style.display = "none";
  if (formEl)  formEl.style.display  = "";
  // Plan listesini doldur
  const pr = await fetch("/api/uyelik-turleri-public");
  const planlarData = await pr.json();
  const sel = document.getElementById("off-tur-sec");
  if (sel) sel.innerHTML = planlarData.map(p => `<option value="${p.kod}">${p.ad} &mdash; ${p.aciklama||""}</option>`).join("");
}

function offReqKodKontrol() {
  const val = (document.getElementById("off-req-kod").value || "").trim().toUpperCase();
  const durumEl = document.getElementById("off-req-durum");
  if (!val) { durumEl.textContent = ""; return; }
  if (!val.startsWith("REQ-")) {
    durumEl.style.color = "#f87171";
    durumEl.textContent = "&#9888; Geçersiz format. REQ- ile başlamalıdır.";
  } else {
    durumEl.style.color = "#4ade80";
    durumEl.textContent = "&#10003; Format geçerli görünüyor.";
  }
}

async function offlineTalepGonder() {
  mesajGizle("offline-hata"); mesajGizle("offline-ok");
  const tur        = document.getElementById("off-tur-sec")  ? document.getElementById("off-tur-sec").value.trim()  : "";
  const istek_kodu = (document.getElementById("off-req-kod").value || "").trim().toUpperCase();
  if (!tur)        { mesajGoster("offline-hata", "&#9888; Lütfen bir lisans türü seçin."); return; }
  if (!istek_kodu) { mesajGoster("offline-hata", "&#9888; İstek kodu zorunludur."); return; }
  if (!istek_kodu.startsWith("REQ-")) { mesajGoster("offline-hata", "&#10060; Geçersiz istek kodu. REQ- ile başlamalıdır."); return; }
  const btn = document.getElementById("off-talep-btn");
  if (btn) { btn.disabled = true; btn.textContent = "Gönderiliyor&hellip;"; }
  const r = await fetch("/api/talep-olustur", {
    method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({tur, talep_tipi:"offline", istek_kodu})
  });
  const d = await r.json();
  if (btn) { btn.disabled = false; btn.textContent = "Offline Lisans Talebi Gönder"; }
  if (r.ok) {
    mesajGoster("offline-ok", "&#9989; Talebiniz alındı! Onaylandığında aktivasyon kodunuz lisans geçmişinizde görünecektir.");
    document.getElementById("off-req-kod").value = "";
    document.getElementById("off-req-durum").textContent = "";
  } else {
    mesajGoster("offline-hata", "&#10060; " + (d.detail || "Bir hata oluştu."));
  }
}

async function talepGonder() {
  if (!dashSecilenPlan) { mesajGoster("talep-hata", "&#9888; Lütfen bir plan seçin."); return; }
  mesajGizle("talep-hata"); mesajGizle("talep-ok");

  const tipEl      = document.querySelector('input[name="talep_tipi"]:checked');
  const talep_tipi = tipEl ? tipEl.value : "online";
  const istekEl    = document.getElementById("talep-istek-kodu");
  const istek_kodu = istekEl ? istekEl.value.trim().toUpperCase() : _dashReqKodu.trim().toUpperCase();

  if (talep_tipi === "offline") {
    if (!istek_kodu) {
      mesajGoster("talep-hata", "&#9888; Offline lisans için Gateway İstek Kodu zorunludur.");
      return;
    }
    if (!istek_kodu.startsWith("REQ-") || istek_kodu.length < 10) {
      mesajGoster("talep-hata", "&#10060; Geçersiz istek kodu formatı. REQ- ile başlamalıdır.");
      return;
    }
  }

  const btn = document.getElementById("talep-gonder-btn");
  if (btn) { btn.disabled = true; btn.textContent = "Gönderiliyor&hellip;"; }

  const r = await fetch("/api/talep-olustur", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({tur: dashSecilenPlan, talep_tipi, istek_kodu})
  });
  const d = await r.json();

  if (btn) { btn.disabled = false; btn.textContent = talep_tipi === "offline" ? "&#128274; Offline Talep Gönder" : "&#127760; Online Talep Gönder"; }

  if (r.ok) {
    mesajGoster("talep-ok", talep_tipi === "offline"
      ? "&#9989; Offline lisans talebiniz alındı! Onaylandığında lisans geçmişinizde görünecektir."
      : "&#9989; Talebiniz başarıyla gönderildi!"
    );
    taleplerYukle();
  } else {
    mesajGoster("talep-hata", "&#10060; " + (d.detail || "Hata oluştu."));
  }
}

async function lisansGecmisiniYukle() {
  const r = await fetch("/api/lisans-gecmisim");
  if (!r.ok) return;
  const liste = await r.json();
  const el = document.getElementById("gecmis-icerik");
  if (!liste.length) {
    el.innerHTML = '<div style="color:var(--muted);font-size:13px;">Henüz lisans kaydı yok.</div>';
    return;
  }
  const durumBilgi = {
    aktif:          { cls: 'b-onay',  yazi: '&#10003; Aktif' },
    suresi_dolmus:  { cls: 'b-red',   yazi: '✗ Süresi Doldu' },
    iptal:          { cls: 'b-red',   yazi: '✗ İptal Edildi' },
  };
  const turIkon = { aylik: '&#128467;', yillik: '&#128197;', omur_boyu: '&#9854;', deneme: '&#128300;' };
  el.innerHTML = `<div style="overflow-x:auto;">
    <table style="width:100%;border-collapse:collapse;font-size:13px;">
      <thead>
        <tr style="color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:0.5px;">
          <th style="padding:8px 12px;text-align:left;">Lisans / ACT Kodu</th>
          <th style="padding:8px 12px;text-align:left;">Tür</th>
          <th style="padding:8px 12px;text-align:left;">Tip</th>
          <th style="padding:8px 12px;text-align:left;">İstek Kodu (REQ)</th>
          <th style="padding:8px 12px;text-align:left;">Durum</th>
          <th style="padding:8px 12px;text-align:left;">Oluşturulma</th>
          <th style="padding:8px 12px;text-align:left;">Bitiş</th>
        </tr>
      </thead>
      <tbody>
        ${liste.map(l => {
          const d = durumBilgi[l.durum] || { cls: '', yazi: l.durum };
          const ikon = l.tip === 'offline' ? '&#128274;' : (turIkon[l.tur] || '&#128273;');
          const kalanTxt = l.kalan_gun != null ? ` &middot; ${l.kalan_gun} gün kaldı` : '';
          const kodRenk = l.tip === 'offline' ? '#4ade80' : '#7eb8ff';
          const tipBadge = l.tip === 'offline'
            ? `<span style="font-size:10px;padding:2px 6px;border-radius:4px;background:#22c55e15;color:#4ade80;border:1px solid #22c55e44;">&#128274; OFFLİNE</span>`
            : `<span style="font-size:10px;padding:2px 6px;border-radius:4px;background:#3d6fff15;color:#7eb8ff;border:1px solid #3d6fff44;">&#127760; ONLİNE</span>`;
          const istekKoduCell = l.tip === 'offline' && l.istek_kodu
            ? `<code style="font-family:monospace;font-size:11px;background:var(--bg);padding:2px 6px;border-radius:4px;color:#a78bfa;">${l.istek_kodu}</code>`
            : `<span style="color:var(--muted);">&mdash;</span>`;
          return `<tr style="border-top:1px solid var(--border);">
            <td style="padding:10px 12px;"><code style="font-family:monospace;font-size:12px;background:var(--bg);padding:3px 8px;border-radius:4px;color:${kodRenk};">${l.kod}</code></td>
            <td style="padding:10px 12px;">${ikon} ${l.tur.replace('_',' ')}</td>
            <td style="padding:10px 12px;">${tipBadge}</td>
            <td style="padding:10px 12px;">${istekKoduCell}</td>
            <td style="padding:10px 12px;"><span class="badge-sm ${d.cls}" style="white-space:nowrap;">${d.yazi}${kalanTxt}</span></td>
            <td style="padding:10px 12px;color:var(--muted);">${l.olusturma}</td>
            <td style="padding:10px 12px;color:${l.durum==='suresi_dolmus'?'#f87171':'var(--muted)'};">${l.bitis}</td>
          </tr>`;
        }).join('')}
      </tbody>
    </table>
  </div>`;
}

async function mesajlariYukle() {
  const r = await fetch("/api/mesajlarim");
  if (!r.ok) return;
  const mesajlar = await r.json();
  const el = document.getElementById("msg-area");
  if (!el) return;
  // Kullanıcı en alttaysa otomatik kaydır; yazarken konumunu koruma
  const altaYakin = (el.scrollHeight - el.scrollTop) <= (el.clientHeight + 60);
  el.innerHTML = mesajlar.map(m => `
    <div class="msg-wrap ${m.gonderen==='kullanici'?'right':''}">
      <div class="msg-b ${m.gonderen==='kullanici'?'benim':'admin'}">${m.icerik}</div>
      <div class="msg-t">${m.gonderen==='kullanici'?'Siz':'Destek'} &middot; ${m.tarih}</div>
    </div>`).join("");
  if (altaYakin) el.scrollTop = el.scrollHeight;
}

async function mesajGonder() {
  const icerik = document.getElementById("msg-yaz").value.trim();
  if (!icerik) return;
  const r = await fetch("/api/mesaj-gonder", {method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({icerik})});
  if (r.ok) {
    document.getElementById("msg-yaz").value = "";
    mesajlariYukle();
  }
}

// ===== YARDIMCI =====
function mesajGoster(id, txt) {
  const el = document.getElementById(id);
  if (el) { el.textContent = txt; el.style.display = "block"; }
}
function mesajGizle(id) {
  const el = document.getElementById(id);
  if (el) el.style.display = "none";
}

function baslatSitePoll() {
  if (_sitePollTimer) return;
  _sitePollTimer = setInterval(async () => {
    const isDash = document.getElementById("sayfa-dashboard") &&
                   document.getElementById("sayfa-dashboard").style.display !== "none";
    if (!isDash) return;
    lisansKartiGuncelle();
    // taleplerYukle() polling'den ÇIKARILDI &mdash; form her 2 sn'de yeniden render edilince
    // kullanıcının girdiği REQ kodu siliniyor. Talepler sadece dashboard açılışında
    // ve talep gönderildiğinde yüklenir. Kullanıcı manuel "&#8635; Yenile" butonu kullanabilir.
    lisansGecmisiniYukle();
    mesajlariYukle();
  }, 2000);
}

// Sayfa yüklenince oturum kontrolü
let _sitePollTimer = null;
(async function() {
  const r = await fetch("/api/profil");
  if (r.ok) {
    sayfaGoster("dashboard");
    const p = await r.json();
    document.getElementById("nav-links").innerHTML = `<span style="font-size:13px;color:var(--muted);margin-right:8px;">${p.email}</span><button class="nav-btn nav-btn-ghost" onclick="sayfaGoster('offline')" style="border-color:#3d6fff44;color:#7eb8ff;">&#128274; Offline</button><button class="nav-btn nav-btn-ghost" onclick="cikisYap()">Cıkış</button>`;
    baslatSitePoll();
  }
})();

// ===== ÇEREZ YÖNETİMİ =====
(function() {
  const CEREZ_ANAHTAR = 'cookie_consent';
  const CEREZ_SURE    = 365; // gün

  function cerezOku(ad) {
    const esles = document.cookie.match('(?:^|; )' + ad.replace(/([.$?*|{}()[\]\\/+^])/g, '\\\\$1') + '=([^;]*)');
    return esles ? decodeURIComponent(esles[1]) : null;
  }

  function cerezYaz(ad, deger, gun) {
    const exp = new Date(Date.now() + gun * 864e5).toUTCString();
    document.cookie = `${ad}=${encodeURIComponent(deger)}; expires=${exp}; path=/; SameSite=Lax`;
  }

  function bannerGizle() {
    const b = document.getElementById('cerez-banner');
    b.classList.add('cerez-gizle');
    setTimeout(() => { b.style.display = 'none'; }, 320);
  }

  window.cerezKabulEt = function(tip) {
    // 'reddet': sadece zorunlu çerezler aktif, fonksiyonel kaydedilmez
    // 'zorunlu': zorunlu kabul, fonksiyonel hayır
    // 'tum': hepsi kabul
    const tercih = { zorunlu: true, fonksiyonel: tip === 'tum', verilen: tip, tarih: new Date().toISOString() };
    if (tip !== 'reddet') {
      cerezYaz(CEREZ_ANAHTAR, JSON.stringify(tercih), CEREZ_SURE);
    } else {
      // Reddet: tercih çerezini kaydetme ama banner'ı kapat (session boyunca hatırla)
      sessionStorage.setItem(CEREZ_ANAHTAR, 'reddet');
    }
    bannerGizle();
    cerezModalKapat();
  };

  window.cerezAyarlariAc = function() {
    const mevcut = cerezOku(CEREZ_ANAHTAR);
    if (mevcut) {
      try {
        const t = JSON.parse(mevcut);
        const fonkEl = document.getElementById('cerez-toggle-fonk');
        if (fonkEl) fonkEl.checked = !!t.fonksiyonel;
      } catch(e) {}
    }
    document.getElementById('cerez-modal-overlay').classList.add('aktif');
  };

  window.cerezModalKapat = function() {
    document.getElementById('cerez-modal-overlay').classList.remove('aktif');
  };

  window.cerezAyarlariKaydet = function() {
    const fonk = document.getElementById('cerez-toggle-fonk').checked;
    const tip  = fonk ? 'tum' : 'zorunlu';
    cerezKabulEt(tip);
  };

  // Modal dışına tıklayınca kapat
  document.getElementById('cerez-modal-overlay').addEventListener('click', function(e) {
    if (e.target === this) cerezModalKapat();
  });

  // Banner göster/gizle kontrolü
  const kayitli = cerezOku(CEREZ_ANAHTAR);
  const sessionRed = sessionStorage.getItem(CEREZ_ANAHTAR);
  if (!kayitli && !sessionRed) {
    const banner = document.getElementById('cerez-banner');
    banner.style.display = 'flex';
  }
})();
</script>

<script>
(async function(){
  try {
    const r = await fetch("/api/public-info");
    if (!r.ok) return;
    const d = await r.json();
    const q = document.getElementById("nav-quick-links");
    if (!q) return;
    q.innerHTML = "";
    if (d.indirme_linki) {
      q.innerHTML += `<a href="${d.indirme_linki}" style="display:inline-flex;align-items:center;gap:6px;background:linear-gradient(90deg,#06b6d4,#3b82f6);color:#fff;padding:6px 10px;border-radius:8px;font-size:13px;font-weight:700;text-decoration:none;">&#11015; İndir</a>`;
    } else {
      q.innerHTML += `<a href="#" onclick="alert('Program sunucuda mevcut değil.')" style="display:inline-flex;align-items:center;gap:6px;background:#ef44447a;color:#fff;padding:6px 10px;border-radius:8px;font-size:13px;font-weight:700;text-decoration:none;">&#11015; İndir</a>`;
    }
    if (d.vt_hash) {
      q.innerHTML += `<a href="https://www.virustotal.com/gui/file/${d.vt_hash}" target="_blank" style="display:inline-flex;align-items:center;gap:6px;background:#111;color:#fff;padding:6px 10px;border-radius:8px;font-size:13px;font-weight:700;text-decoration:none;margin-left:6px;">&#128737; VT</a>`;
    }
  } catch(e) {}
})();
</script>
<script>
// ===== TEMA YÖNETİMİ (dark/light) =====
(function() {
  var kayitli = localStorage.getItem('nt_tema') || 'dark';
  document.documentElement.setAttribute('data-theme', kayitli);
  var ikon = document.getElementById('theme-icon');
  if (ikon) ikon.innerHTML = kayitli === 'light' ? '&#9728;' : '&#9790;';
})();

function temaToggle() {
  var mevcut = document.documentElement.getAttribute('data-theme') || 'dark';
  var yeni   = mevcut === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', yeni);
  localStorage.setItem('nt_tema', yeni);
  var ikon = document.getElementById('theme-icon');
  if (ikon) ikon.innerHTML = yeni === 'light' ? '&#9728;' : '&#9790;';
}
</script>
</body>
</html>"""
