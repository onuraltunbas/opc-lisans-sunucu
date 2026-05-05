# -*- coding: utf-8 -*-
"""
Admin Panel HTML içeriği.
"""

PANEL_HTML = r"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>OPC Gateway — Lisans Paneli</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: system-ui, sans-serif; background: #0f1117; color: #e0e0e0; min-height: 100vh; }
a { color: inherit; text-decoration: none; }

/* Login overlay */
#login-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.85); display: flex; align-items: center; justify-content: center; z-index: 999; backdrop-filter: blur(6px); }
#login-box { background: #1a1d2e; border: 1px solid #2a2d3e; border-radius: 12px; padding: 36px; width: 340px; text-align: center; }
#login-box h2 { color: #5b8cff; margin-bottom: 24px; font-size: 20px; }
#login-box input { width: 100%; background: #0f1117; border: 1px solid #2a2d3e; border-radius: 6px; padding: 10px 12px; color: #e0e0e0; font-size: 14px; margin-bottom: 12px; }
#login-box input:focus { outline: none; border-color: #5b8cff; }
#login-box button { width: 100%; background: #5b8cff; color: white; border: none; border-radius: 6px; padding: 11px; font-size: 14px; font-weight: 600; cursor: pointer; }
#login-box button:hover { background: #4a7aff; }
#login-hata { color: #ff6b6b; font-size: 13px; margin-top: 8px; min-height: 20px; }

/* Layout */
.sidebar { position: fixed; left: 0; top: 0; bottom: 0; width: 220px; background: #1a1d2e; border-right: 1px solid #2a2d3e; padding: 20px 0; display: flex; flex-direction: column; overflow-y: auto; }
.sidebar-logo { padding: 0 20px 20px; border-bottom: 1px solid #2a2d3e; margin-bottom: 12px; }
.sidebar-logo h1 { font-size: 15px; font-weight: 700; color: #5b8cff; }
.sidebar-logo p { font-size: 11px; color: #666; margin-top: 2px; }
.nav-item { display: flex; align-items: center; gap: 10px; padding: 10px 20px; font-size: 13px; color: #aaa; cursor: pointer; transition: all 0.15s; position: relative; }
.nav-item:hover { background: #222540; color: #e0e0e0; }
.nav-item.active { background: #222540; color: #5b8cff; border-right: 3px solid #5b8cff; }
.nav-item .badge { background: #ff4757; color: white; border-radius: 10px; padding: 1px 7px; font-size: 11px; font-weight: 700; margin-left: auto; }
.nav-icon { font-size: 16px; width: 20px; text-align: center; }

/* Accordion Sidebar */
.acc-header { display: flex; align-items: center; gap: 10px; padding: 10px 20px; font-size: 13px; color: #aaa; cursor: pointer; transition: all 0.15s; user-select: none; }
.acc-header:hover { background: #222540; color: #e0e0e0; }
.acc-header.active { background: #222540; color: #5b8cff; border-right: 3px solid #5b8cff; }
.acc-content { display: none; background: #121420; padding: 4px 0; }
.acc-content.show { display: block; }
.acc-item { padding: 8px 20px 8px 46px; font-size: 12px; color: #888; cursor: pointer; transition: all 0.15s; display: block; position: relative; }
.acc-item:hover { color: #e0e0e0; background: #1a1d2e; }
.acc-item.active { color: #5b8cff; background: #1a1d2e; }
.acc-item.active::before { content: ''; position: absolute; left: 24px; top: 50%; transform: translateY(-50%); width: 4px; height: 4px; border-radius: 50%; background: #5b8cff; }
.acc-chevron { margin-left: auto; font-size: 10px; transition: transform 0.2s; }
.acc-header.open .acc-chevron { transform: rotate(90deg); }

/* Sub Tabs for Yeni Lisans */
.sub-tabs { display: flex; gap: 2px; background: #0f1117; padding: 4px; border-radius: 8px; margin-bottom: 16px; border: 1px solid #2a2d3e; }
.sub-tab { flex: 1; text-align: center; padding: 8px 12px; font-size: 12px; font-weight: 600; color: #888; cursor: pointer; border-radius: 6px; transition: all 0.2s; }
.sub-tab:hover { color: #e0e0e0; }
.sub-tab.active { background: #222540; color: #5b8cff; }
.sub-pane { display: none; }
.sub-pane.active { display: block; }

.main { margin-left: 220px; padding: 24px; position: relative; }
.page { display: none; }
.page.active { display: block; }
.page-title { font-size: 20px; font-weight: 700; color: #e0e0e0; margin-bottom: 20px; }

/* Greeting */
#panel-greeting { position: absolute; right: 24px; top: 24px; font-size: 14px; font-weight: 600; color: #8a9bc0; z-index: 10; }


/* Cards */
.card { background: #1a1d2e; border: 1px solid #2a2d3e; border-radius: 10px; padding: 20px; margin-bottom: 16px; }
.card h3 { font-size: 14px; font-weight: 600; color: #5b8cff; margin-bottom: 14px; }

/* Form elements */
input[type=text], input[type=email], input[type=number], input[type=password], select, textarea {
  background: #0f1117; border: 1px solid #2a2d3e; border-radius: 6px; padding: 9px 12px; color: #e0e0e0; font-size: 13px; width: 100%; margin-bottom: 8px;
}
input:focus, select:focus, textarea:focus { outline: none; border-color: #5b8cff; }
textarea { min-height: 80px; resize: vertical; }

/* Buttons */
.btn { border: none; border-radius: 6px; padding: 8px 18px; font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.15s; display: inline-flex; align-items: center; gap: 6px; }
.btn-primary { background: #5b8cff; color: white; }
.btn-primary:hover { background: #4a7aff; }
.btn-danger { background: #c62828; color: white; }
.btn-danger:hover { background: #b71c1c; }
.btn-success { background: #2e7d32; color: white; }
.btn-success:hover { background: #1b5e20; }
.btn-warning { background: #e65100; color: white; }
.btn-warning:hover { background: #bf360c; }
.btn-ghost { background: transparent; border: 1px solid #2a2d3e; color: #aaa; }
.btn-ghost:hover { border-color: #5b8cff; color: #5b8cff; }
.btn-sm { padding: 5px 12px; font-size: 12px; }
.row-btns { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 4px; }

/* Tables */
.tbl-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: 12px; }
th { background: #222540; color: #888; text-transform: uppercase; font-size: 11px; letter-spacing: 0.5px; padding: 10px 12px; text-align: left; }
td { padding: 10px 12px; border-bottom: 1px solid #1e2033; vertical-align: middle; color: #ccc; }
tr:hover td { background: #1e2033; }
code { font-family: monospace; font-size: 12px; background: #222540; padding: 2px 6px; border-radius: 4px; color: #7eb8ff; }

/* Badges */
.badge { display: inline-block; padding: 2px 9px; border-radius: 10px; font-size: 11px; font-weight: 600; }
.b-aktif { background: #1b5e2033; color: #4caf50; border: 1px solid #2e7d3255; }
.b-pasif { background: #b71c1c22; color: #ef9a9a; border: 1px solid #c6282833; }
.b-beklemede { background: #e65100; color: white; }
.b-onaylandi { background: #2e7d32; color: white; }
.b-reddedildi { background: #c62828; color: white; }
.b-aylik { background: #1565c033; color: #90caf9; border: 1px solid #1565c055; }
.b-yillik { background: #4a148c33; color: #ce93d8; border: 1px solid #4a148c55; }
.b-omur { background: #1b5e2033; color: #a5d6a7; border: 1px solid #2e7d3255; }
.b-deneme { background: #e6510033; color: #ffcc80; border: 1px solid #e6510055; }

/* Terminal / log */
#log-output { background: #0a0c14; color: #00e676; font-family: monospace; font-size: 11px; padding: 14px; border-radius: 6px; min-height: 120px; max-height: 360px; overflow-y: auto; white-space: pre-wrap; border: 1px solid #1e2033; }

/* Stat cards */
.stats { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; margin-bottom: 20px; }
.stat-card { background: #1a1d2e; border: 1px solid #2a2d3e; border-radius: 10px; padding: 16px; }
.stat-card .val { font-size: 28px; font-weight: 700; color: #5b8cff; }
.stat-card .lbl { font-size: 12px; color: #666; margin-top: 4px; }

/* Messages */
.msg-list { display: flex; flex-direction: column; gap: 8px; max-height: 420px; overflow-y: auto; padding-right: 4px; }
.msg-bubble { max-width: 80%; padding: 10px 14px; border-radius: 10px; font-size: 13px; line-height: 1.6; }
.msg-bubble.kullanici { background: #222540; color: #ccc; align-self: flex-start; border-bottom-left-radius: 2px; }
.msg-bubble.admin { background: #5b8cff22; color: #90caf9; align-self: flex-end; border-bottom-right-radius: 2px; border: 1px solid #5b8cff33; }
.msg-time { font-size: 10px; color: #555; margin-top: 4px; }
.msg-sender { display: flex; flex-direction: column; }
.msg-sender.right { align-items: flex-end; }

/* User detail card */
.user-detail { background: #0f1117; border: 1px solid #2a2d3e; border-radius: 8px; padding: 14px; margin-bottom: 14px; font-size: 13px; }
.user-detail .row { display: flex; gap: 24px; flex-wrap: wrap; }
.user-detail .field { display: flex; flex-direction: column; gap: 3px; }
.user-detail .field label { font-size: 11px; color: #555; text-transform: uppercase; letter-spacing: 0.5px; }
.user-detail .field span { color: #ccc; font-weight: 500; }

/* Konuşma listesi */
.conv-list { display: flex; flex-direction: column; gap: 2px; }
.conv-item { display: flex; align-items: center; gap: 12px; padding: 12px 14px; border-radius: 8px; cursor: pointer; transition: background 0.15s; border: 1px solid transparent; }
.conv-item:hover { background: #222540; }
.conv-item.active { background: #222540; border-color: #5b8cff33; }
.conv-avatar { width: 38px; height: 38px; border-radius: 50%; background: #5b8cff33; color: #5b8cff; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 15px; flex-shrink: 0; }
.conv-info { flex: 1; min-width: 0; }
.conv-name { font-size: 13px; font-weight: 600; color: #e0e0e0; }
.conv-preview { font-size: 12px; color: #666; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-top: 2px; }
.conv-meta { display: flex; flex-direction: column; align-items: flex-end; gap: 4px; flex-shrink: 0; }
.unread-dot { background: #ff4757; color: white; border-radius: 10px; padding: 1px 7px; font-size: 11px; font-weight: 700; }

/* Split layout for messages */
.msg-split { display: grid; grid-template-columns: 280px 1fr; gap: 16px; height: calc(100vh - 140px); }
.msg-left { background: #1a1d2e; border: 1px solid #2a2d3e; border-radius: 10px; overflow-y: auto; padding: 12px; }
.msg-right { background: #1a1d2e; border: 1px solid #2a2d3e; border-radius: 10px; display: flex; flex-direction: column; }
.msg-right-header { padding: 14px 16px; border-bottom: 1px solid #2a2d3e; }
.msg-right-body { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 10px; }
.msg-right-footer { padding: 12px 16px; border-top: 1px solid #2a2d3e; display: flex; gap: 8px; }
.msg-right-footer textarea { margin: 0; flex: 1; min-height: 44px; max-height: 120px; }

/* Notification */
.notif { position: fixed; bottom: 24px; right: 24px; background: #2e7d32; color: white; padding: 12px 20px; border-radius: 8px; font-size: 13px; font-weight: 600; z-index: 9999; transform: translateY(80px); opacity: 0; transition: all 0.3s; }
.notif.show { transform: translateY(0); opacity: 1; }
.notif.error { background: #c62828; }

/* Üyelik türleri */
.tur-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 12px; }
.tur-card { background: #0f1117; border: 1px solid #2a2d3e; border-radius: 8px; padding: 14px; }
.tur-card h4 { font-size: 14px; color: #e0e0e0; margin-bottom: 4px; }
.tur-card .tur-kod { font-size: 11px; color: #5b8cff; font-family: monospace; }
.tur-card .tur-aciklama { font-size: 12px; color: #666; margin: 8px 0; }

/* Filtre butonları */
.filtre-bar { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }
.filtre-btn { border: 1px solid #2a2d3e; background: transparent; color: #888; border-radius: 20px; padding: 5px 16px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.15s; display: inline-flex; align-items: center; gap: 6px; }
.filtre-btn:hover { border-color: #5b8cff; color: #e0e0e0; }
.filtre-btn.aktif { background: #5b8cff22; border-color: #5b8cff; color: #5b8cff; }
.filtre-btn.aktif-f { background: #22c55e22; border-color: #22c55e; color: #4ade80; }
.filtre-btn.biten-f { background: #f59e0b22; border-color: #f59e0b; color: #fbbf24; }
.filtre-btn.iptal-f { background: #ef444422; border-color: #ef4444; color: #f87171; }
.cnt-badge { font-size: 11px; font-weight: 700; background: rgba(255,255,255,0.08); border-radius: 10px; padding: 1px 7px; }

/* İstatistik kartı */
.istat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 16px; }
.istat-card { background: #0f1117; border: 1px solid #2a2d3e; border-radius: 8px; padding: 14px 16px; text-align: center; }
.istat-card .i-val { font-size: 26px; font-weight: 700; }
.istat-card .i-lbl { font-size: 11px; color: #555; margin-top: 3px; text-transform: uppercase; letter-spacing: 0.5px; }
.istat-card.i-green .i-val { color: #4ade80; }
.istat-card.i-yellow .i-val { color: #fbbf24; }
.istat-card.i-red .i-val { color: #f87171; }
.istat-card.i-blue .i-val { color: #7eb8ff; }
</style>
</head>
<body>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js"></script>

<!-- Login -->
<div id="login-overlay">
  <div id="login-box">
    <h2>🔐 Panel Girişi</h2>
    <input type="text" id="inp-kullanici" placeholder="Kullanıcı adı" autocomplete="username">
    <input type="password" id="inp-sifre" placeholder="Şifre" autocomplete="current-password" onkeydown="if(event.key==='Enter')panelGiris()">
    <button onclick="panelGiris()">Giriş Yap</button>
    <div id="login-hata"></div>
  </div>
</div>

<!-- Sidebar -->
<div class="sidebar">
  <div class="sidebar-logo">
    <h1>OPC Gateway</h1>
    <p>Lisans Yönetim Paneli</p>
  </div>
  
  <div class="acc-header open" onclick="toggleAccordion(this)">
    <span class="nav-icon">🔑</span> Lisanslar <span class="acc-chevron">▶</span>
  </div>
  <div class="acc-content show">
    <div class="acc-item active" onclick="sayfaAc('yeni-lisans')" id="nav-yeni-lisans">Yeni Lisans Oluştur</div>
    <div class="acc-item" onclick="sayfaAc('tum-lisanslar')" id="nav-tum-lisanslar">Tüm Lisanslar</div>
    <div class="acc-item" onclick="sayfaAc('lisans-islemleri')" id="nav-lisans-islemleri">Lisans İşlemleri</div>
    <div class="acc-item" onclick="sayfaAc('lisans-istatistikleri')" id="nav-lisans-istatistikleri">Lisans İstatistikleri</div>
    <div class="acc-item yetki-uyelik-tur" onclick="sayfaAc('uyelik-turleri')" id="nav-uyelik-turleri" style="display:none">Lisans Türleri</div>
  </div>

  <div class="nav-item" onclick="sayfaAc('talepler')" id="nav-talepler">
    <span class="nav-icon">📋</span> Talepler
    <span class="badge" id="talep-badge" style="display:none">0</span>
  </div>
  <div class="nav-item" onclick="sayfaAc('mesajlar')" id="nav-mesajlar">
    <span class="nav-icon">💬</span> Mesajlar
    <span class="badge" id="mesaj-badge" style="display:none">0</span>
  </div>
  <div class="nav-item" onclick="sayfaAc('kullanicilar')" id="nav-kullanicilar">
    <span class="nav-icon">👥</span> Kullanıcılar
  </div>
  <div class="nav-item yetki-ip-ban" onclick="sayfaAc('ip-banlar')" id="nav-ip-banlar" style="display:none">
    <span class="nav-icon">🚫</span> IP Ban
  </div>
  <div class="nav-item" onclick="sayfaAc('loglar')" id="nav-loglar">
    <span class="nav-icon">📜</span> Loglar
  </div>
  <div class="nav-item yetki-admin-only" onclick="sayfaAc('yetkililer')" id="nav-yetkililer" style="display:none">
    <span class="nav-icon">🛡️</span> Yetkililer
  </div>
  <div class="nav-item yetki-admin-only" onclick="sayfaAc('panel-loglari')" id="nav-panel-loglari" style="display:none">
    <span class="nav-icon">📑</span> Kayıtlar
  </div>
  
  <div class="nav-item" onclick="panelCikis()" style="margin-top:auto;color:#ef4444;border-top:1px solid #2a2d3e;padding-top:14px;">
    <span class="nav-icon">🚪</span> Çıkış Yap
  </div>
</div>

<!-- Main -->
<div class="main">
  <div id="panel-greeting"></div>

  <!-- Yeni Lisans -->
  <div class="page active" id="page-yeni-lisans">
    <div class="page-title">➕ Yeni Lisans Oluştur</div>
    <div class="card" style="max-width:600px;">
      <div class="sub-tabs">
        <div class="sub-tab active" onclick="switchYeniLisansTab('online')" id="tab-yeni-online">Online Lisans</div>
        <div class="sub-tab" onclick="switchYeniLisansTab('offline')" id="tab-yeni-offline">Offline Lisans</div>
      </div>
      
      <div class="sub-pane active" id="pane-yeni-online">
        <input type="text" id="l-adi" placeholder="Müşteri adı soyadı *">
        <input type="email" id="l-email" placeholder="E-posta (teşekkür maili için)">
        <select id="l-tur">
          <option value="aylik">Aylık (30 gün)</option>
        </select>
        <div style="display:flex;gap:8px;">
          <input type="number" id="l-ozel-gun" placeholder="Özel gün sayısı (Opsiyonel)" min="0" style="flex:1;">
          <input type="number" id="l-saat" placeholder="Deneme (saat)" value="24" min="1" max="8760" style="flex:1;">
        </div>
        <textarea id="l-not" placeholder="Not"></textarea>
        <button class="btn btn-primary yetki-lisans-olustur" onclick="lisansOlustur()">✚ Oluştur</button>
        <div id="l-sonuc" style="margin-top:10px;font-size:13px;color:#4caf50;font-weight:bold;font-family:monospace;"></div>
      </div>
      
      <div class="sub-pane" id="pane-yeni-offline">
        <input type="text" id="off-kime" placeholder="Kime Üretildi (Müşteri Adı) *">
        <input type="email" id="off-email" placeholder="Müşteri E-posta (Panelde görünmesi için)">
        <input type="text" id="off-istek" placeholder="İstek Kodu (REQ-...) *">
        <input type="number" id="off-sure" placeholder="Süre (Gün) *" value="30">
        <button class="btn btn-warning yetki-offline-lisans" onclick="offlineLisansUretBtn()">🔒 Offline Lisans Üret</button>
        <div id="off-sonuc" style="margin-top:10px;font-size:13px;color:#ffb74d;font-weight:bold;font-family:monospace;"></div>
      </div>
    </div>
  </div>

  <!-- Tüm Lisanslar -->
  <div class="page" id="page-tum-lisanslar">
    <div class="page-title">📄 Tüm Lisanslar</div>
    
    <div class="card">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
        <h3 style="margin:0;color:#4ade80;">Aktif Online Lisanslar</h3>
        <button class="btn btn-ghost btn-sm" onclick="lisanslariYukle()">↻ Yenile</button>
      </div>
      <div class="filtre-bar">
        <button class="filtre-btn aktif" id="fb-hepsi" onclick="filtreAyarla('hepsi')">Tümü <span class="cnt-badge" id="fb-hepsi-cnt">—</span></button>
        <button class="filtre-btn aktif-f" id="fb-aktif" onclick="filtreAyarla('aktif')">✓ Aktif <span class="cnt-badge" id="fb-aktif-cnt">—</span></button>
        <button class="filtre-btn biten-f" id="fb-biten" onclick="filtreAyarla('biten')">⏱ Süresi Dolmuş <span class="cnt-badge" id="fb-biten-cnt">—</span></button>
        <button class="filtre-btn iptal-f" id="fb-iptal" onclick="filtreAyarla('iptal')">✗ İptal <span class="cnt-badge" id="fb-iptal-cnt">—</span></button>
      </div>
      <div class="tbl-wrap">
        <table>
          <thead><tr><th>Kod</th><th>Müşteri</th><th>Tür</th><th>Durum</th><th>HWID</th><th>Bitiş</th><th>Son Checkin</th><th>Not / İptal</th><th>İşlem</th></tr></thead>
          <tbody id="l-tablo-online"></tbody>
        </table>
      </div>
    </div>

    <div class="card">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
        <h3 style="margin:0;color:#fbbf24;">Üretilen Offline Lisanslar</h3>
      </div>
      <div class="tbl-wrap">
        <table>
          <thead><tr><th>Kod</th><th>Müşteri</th><th>Yetki</th><th>Süre</th><th>İstek Kodu</th><th>Durum</th><th>Not / İptal</th><th>İşlem</th></tr></thead>
          <tbody id="l-tablo-offline"></tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Lisans İşlemleri -->
  <div class="page" id="page-lisans-islemleri">
    <div class="page-title">⚙️ Lisans İşlemleri</div>
    <div class="card" style="max-width:500px;">
      <h3>Lisans İşlemleri</h3>
      <input type="text" id="l-islem-kod" placeholder="Lisans kodu (AYL-XXXX-XXXX-XXXX)">
      <input type="number" id="l-uzat-gun" placeholder="Uzatma (gün)" value="30" min="1">
      <div class="row-btns">
        <button class="btn btn-danger btn-sm yetki-lisans-sil" onclick="iptalEt()">✖ İptal Et</button>
        <button class="btn btn-warning btn-sm yetki-hwid-sifirla" onclick="hwIdSifirla()">↺ HWID Sıfırla</button>
        <button class="btn btn-success btn-sm yetki-sure-uzat" onclick="sureUzat()">+ Süre Uzat</button>
      </div>
      <div id="l-islem-sonuc" style="margin-top:10px;font-size:13px;"></div>
    </div>
  </div>

  <!-- Lisans İstatistikleri -->
  <div class="page" id="page-lisans-istatistikleri">
    <div class="page-title">📊 Lisans İstatistikleri</div>
    <div class="card" id="istat-card">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
        <h3 style="margin:0">İstatistikler</h3>
        <button class="btn btn-ghost btn-sm" onclick="istatistikYukle()">↻ Yenile</button>
      </div>
      <div class="istat-grid" id="istat-grid">
        <div class="istat-card i-blue"><div class="i-val" id="is-toplam">—</div><div class="i-lbl">Toplam</div></div>
        <div class="istat-card i-green"><div class="i-val" id="is-aktif">—</div><div class="i-lbl">Aktif</div></div>
        <div class="istat-card i-yellow"><div class="i-val" id="is-biten">—</div><div class="i-lbl">Süresi Dolmuş</div></div>
        <div class="istat-card i-red"><div class="i-val" id="is-iptal">—</div><div class="i-lbl">İptal</div></div>
      </div>
      <div id="neden-bolum" style="display:none;margin-top:16px;">
        <div style="font-size:12px;color:#555;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:12px;">İptal Nedenleri</div>
        <div style="display:grid;grid-template-columns:1fr auto;gap:16px;align-items:start;">
          <div id="neden-bars"></div>
          <div style="width:160px;height:160px;"><canvas id="neden-chart"></canvas></div>
        </div>
      </div>
    </div>
  </div>

  <!-- Talepler -->
  <div class="page" id="page-talepler">
    <div class="page-title">📋 Lisans Talepleri</div>
    <div class="card">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;flex-wrap:wrap;gap:8px;">
        <h3 style="margin:0">Gelen Talepler</h3>
        <div style="display:flex;gap:8px;flex-wrap:wrap;">
          <button class="btn btn-ghost btn-sm" onclick="taleplerYukle()">↻ Yenile</button>
          <button class="btn btn-sm" id="talep-toplu-sil-btn" onclick="talepTopluSil()" style="background:#7f1d1d;color:#fca5a5;border:1px solid #991b1b;display:none;">🗑 Seçilenleri Kalıcı Sil</button>
        </div>
      </div>
      <div class="tbl-wrap">
        <table>
          <thead><tr><th style="width:36px;"><input type="checkbox" id="talep-hepsi-cb" onchange="talepTumunuSec(this.checked)" title="Tümünü Seç"></th><th>Tarih</th><th>Ad Soyad</th><th>E-posta</th><th>Tür</th><th>IP</th><th>Durum</th><th>İşlem</th></tr></thead>
          <tbody id="talep-tablo"></tbody>
        </table>
      </div>
    </div>
    <!-- Talep işlem modalı -->
    <div id="talep-modal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:500;align-items:center;justify-content:center;">
      <div style="background:#1a1d2e;border:1px solid #2a2d3e;border-radius:12px;padding:28px;width:480px;max-width:95vw;">
        <h3 style="color:#5b8cff;margin-bottom:16px;">Talep İşlemi</h3>
        <div id="talep-bilgi" style="background:#0f1117;border-radius:8px;padding:12px;margin-bottom:14px;font-size:13px;color:#ccc;"></div>
        <textarea id="talep-not" placeholder="Kullanıcıya mesaj (reddedilirse destek mesajı olarak iletilir, onaylanırsa lisans notuna eklenir)" style="margin-bottom:12px;"></textarea>
        <div style="display:flex;gap:10px;">
          <button class="btn btn-success" onclick="talepIsle('onaylandi')">✔ Onayla</button>
          <button class="btn btn-danger" onclick="talepIsle('reddedildi')">✖ Reddet</button>
          <button class="btn btn-ghost" onclick="talepModalKapat()">İptal</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Mesajlar -->
  <div class="page" id="page-mesajlar">
    <div class="page-title">💬 Mesajlar</div>
    <div class="msg-split">
      <div class="msg-left">
        <div style="font-size:12px;color:#555;margin-bottom:10px;text-transform:uppercase;letter-spacing:0.5px;">Konuşmalar</div>
        <div class="conv-list" id="conv-list"></div>
      </div>
      <div class="msg-right" id="msg-right">
        <div style="flex:1;display:flex;align-items:center;justify-content:center;color:#444;font-size:14px;">
          Soldan bir konuşma seçin
        </div>
      </div>
    </div>
  </div>

  <!-- Kullanıcılar -->
  <div class="page" id="page-kullanicilar">
    <div class="page-title">👥 Kullanıcılar</div>
    <div class="card">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
        <h3 style="margin:0">Kayıtlı Kullanıcılar</h3>
        <button class="btn btn-ghost btn-sm" onclick="kullanicilariYukle()">↻ Yenile</button>
      </div>
      <div class="tbl-wrap">
        <table>
          <thead><tr><th>Ad Soyad</th><th>E-posta</th><th>Doğrulandı</th><th>Kayıt</th><th>Son Giriş</th><th>Son IP</th><th>Lisans</th><th>İşlem</th></tr></thead>
          <tbody id="kullanici-tablo"></tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Kullanıcı Düzenle Modal -->
  <div id="kullanici-duzenle-modal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.75);z-index:600;align-items:center;justify-content:center;backdrop-filter:blur(4px);">
    <div style="background:#1a1d2e;border:1px solid #2a2d3e;border-radius:14px;padding:28px;width:520px;max-width:95vw;max-height:90vh;overflow-y:auto;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;">
        <h3 style="color:#5b8cff;font-size:16px;">✏️ Kullanıcı Düzenle</h3>
        <button class="btn btn-ghost btn-sm" onclick="kullaniciDuzenleModalKapat()">✕</button>
      </div>
      <div id="kd-bilgi" style="background:#0f1117;border-radius:8px;padding:12px;margin-bottom:18px;font-size:13px;color:#aaa;"></div>

      <div style="margin-bottom:14px;">
        <label style="font-size:11px;color:#666;display:block;margin-bottom:5px;text-transform:uppercase;letter-spacing:0.5px;">Yeni Şifre (boş bırakılırsa değişmez)</label>
        <input type="password" id="kd-sifre" placeholder="Yeni şifre (min. 6 karakter)" style="margin:0;">
      </div>

      <div style="border-top:1px solid #2a2d3e;padding-top:16px;margin-bottom:14px;">
        <label style="font-size:11px;color:#666;display:block;margin-bottom:10px;text-transform:uppercase;letter-spacing:0.5px;">📋 Kullanıcı Notları / Admin Notu</label>
        <textarea id="kd-not" placeholder="Bu kullanıcı hakkında not..." style="min-height:60px;margin:0;"></textarea>
      </div>

      <div style="display:flex;gap:12px;margin-top:18px;">
        <button class="btn btn-primary" style="flex:1;" onclick="kullaniciDuzenleKaydet()">💾 Kaydet</button>
        <button class="btn btn-ghost" onclick="kullaniciDuzenleModalKapat()">İptal</button>
      </div>
      <div id="kd-sonuc" style="margin-top:10px;font-size:13px;display:none;"></div>
    </div>
  </div>

  <!-- IP Ban -->
  <div class="page" id="page-ip-banlar">
    <div class="page-title">🚫 IP Ban Yönetimi</div>
    <div style="display:grid;grid-template-columns:340px 1fr;gap:16px;">
      <div class="card">
        <h3>IP Ban Ekle</h3>
        <input type="text" id="ban-ip" placeholder="IP adresi (örn: 1.2.3.4)">
        <textarea id="ban-sebep" placeholder="Ban sebebi (opsiyonel)"></textarea>
        <button class="btn btn-danger" onclick="ipBanEkle()">🚫 Banla</button>
      </div>
      <div class="card">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
          <h3 style="margin:0">Banlı IP'ler</h3>
          <button class="btn btn-ghost btn-sm" onclick="ipBanlariYukle()">↻ Yenile</button>
        </div>
        <div class="tbl-wrap">
          <table>
            <thead><tr><th>IP</th><th>Sebep</th><th>Tarih</th><th>Durum</th><th>İşlem</th></tr></thead>
            <tbody id="ban-tablo"></tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- Üyelik Türleri -->
  <div class="page" id="page-uyelik-turleri">
    <div class="page-title">⚙️ Üyelik Türleri</div>
    <div style="display:grid;grid-template-columns:320px 1fr;gap:16px;">
      <div class="card">
        <h3>Yeni Tür Ekle</h3>
        <input type="text" id="tur-kod" placeholder="Kod (örn: haftalik) *">
        <input type="text" id="tur-ad" placeholder="Görünen ad (örn: Haftalık Lisans) *">
        <textarea id="tur-aciklama" placeholder="Açıklama (opsiyonel)"></textarea>
        <label style="display:flex;align-items:center;gap:8px;margin-bottom:10px;font-size:13px;cursor:pointer;">
          <input type="checkbox" id="tur-is-offline"> <b>Bu bir Çevrimdışı (Offline) Pakettir 🔒</b>
        </label>
        <select id="tur-sure-select" onchange="document.getElementById('tur-sure-custom').style.display = this.value === 'custom' ? 'block' : 'none';" style="margin-bottom:8px;">
          <option value="30">1 Ay (30 Gün)</option>
          <option value="90">3 Ay (90 Gün)</option>
          <option value="180">6 Ay (180 Gün)</option>
          <option value="365">1 Yıl (365 Gün)</option>
          <option value="0">Ömür Boyu (0 Gün)</option>
          <option value="custom">Özel Süreli (Manuel)</option>
        </select>
        <input type="number" id="tur-sure-custom" placeholder="Özel Süre (Gün) *" style="display:none;" value="30">
        <input type="text" id="tur-prefix" placeholder="Lisans Ön Eki (örn: VIP) *" value="STD">
        <input type="number" id="tur-sira" placeholder="Sıra (küçük = önce)" value="99">
        <button class="btn btn-primary" onclick="turEkle()">✚ Ekle</button>
      </div>
      <div class="card">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
          <h3 style="margin:0">Mevcut Türler</h3>
          <button class="btn btn-ghost btn-sm" onclick="turleriYukle()">↻ Yenile</button>
        </div>
        <div class="tur-grid" id="tur-grid"></div>
      </div>
    </div>
  </div>

  <!-- Loglar -->
  <div class="page" id="page-loglar">
    <div class="page-title">📜 İşlem Logları</div>
    <div class="card">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
        <button class="btn btn-ghost btn-sm" onclick="logYukle()">↻ Yenile</button>
        <select id="log-adet" style="width:auto;margin:0;" onchange="logYukle()">
          <option value="50">Son 50</option>
          <option value="100" selected>Son 100</option>
          <option value="250">Son 250</option>
        </select>
      </div>
      <div id="log-output">Loglar yükleniyor...</div>
    </div>
  </div>

  <!-- Yetkililer -->
  <div class="page" id="page-yetkililer">
    <div class="page-title">🛡️ Panel Yetkilileri</div>
    
    <div class="card yetki-admin-only" style="margin-bottom:24px;border-color:#5b8cff44;background:#131828;">
      <h3 style="color:#5b8cff">🛠️ Ana Admin Bilgilerini Güncelle</h3>
      <p style="font-size:12px;color:#aaa;margin-bottom:12px;">Sistemin ana yöneticisi (Kurucu) için giriş bilgilerini değiştirin.</p>
      <div style="display:flex;gap:12px;max-width:500px;">
        <input type="text" id="a-yeni-kadi" placeholder="Yeni Kullanıcı Adı">
        <input type="password" id="a-yeni-sifre" placeholder="Yeni Şifre">
        <button class="btn btn-warning" onclick="adminGuncelle()" style="white-space:nowrap;">Değiştir</button>
      </div>
    </div>
    
    <div style="display:grid;grid-template-columns:320px 1fr;gap:16px;">
      <div class="card">
        <h3>Yeni Yetkili Ekle</h3>
        <input type="text" id="y-kadi" placeholder="Kullanıcı Adı *">
        <input type="text" id="y-isim" placeholder="İsim Soyisim *">
        <input type="email" id="y-email" placeholder="E-posta *">
        <input type="password" id="y-sifre" placeholder="Şifre *">
        <div style="margin:14px 0;font-size:12px;color:#ccc;display:flex;flex-direction:column;gap:6px;">
          <label><input type="checkbox" id="cb-lisans_olustur"> Lisans Oluşturabilme</label>
          <label><input type="checkbox" id="cb-lisans_sil"> Lisans Silebilme / İptal</label>
          <label><input type="checkbox" id="cb-hwid_sifirla"> HWID Sıfırlama</label>
          <label><input type="checkbox" id="cb-sure_uzat"> Lisans Süre Uzatma</label>
          <label><input type="checkbox" id="cb-talep_onayla"> Lisans Taleplerini Onaylama</label>
          <label><input type="checkbox" id="cb-kullanici_ekle"> Panel Kullanıcısı (Yetkili) Ekleme</label>
          <label><input type="checkbox" id="cb-mesaj_yaz"> Mesaj Yazabilme</label>
          <label><input type="checkbox" id="cb-ip_ban"> IP Banlama & Kaldırma</label>
          <label><input type="checkbox" id="cb-uyelik_tur"> Üyelik Türleri Yönetimi</label>
          <label><input type="checkbox" id="cb-offline_paket_yonetimi"> 🔒 Çevrimdışı Paket/Tür Yönetimi</label>
          <label><input type="checkbox" id="cb-offline_lisans_uret"> 🔒 Çevrimdışı Lisans Üretme</label>
        </div>
        <button class="btn btn-primary" onclick="yetkiliEkle()">✚ Ekle</button>
      </div>
      <div class="card">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
          <h3 style="margin:0">Mevcut Yetkililer</h3>
          <button class="btn btn-ghost btn-sm" onclick="yetkilileriYukle()">↻ Yenile</button>
        </div>
        <div class="tbl-wrap">
          <table>
            <thead><tr><th>Kullanıcı Adı</th><th>İsim Soyisim</th><th>Rol</th><th>Yetkiler</th><th>Son Giriş</th><th>Son Çıkış</th><th>İşlem</th></tr></thead>
            <tbody id="yetkili-tablo"></tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- Kayıtlar (Panel Logları) -->
  <div class="page" id="page-panel-loglari">
    <div class="page-title">📑 Panel Kayıtları</div>
    <div class="card">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
        <h3 style="margin:0">Yetkili İşlem Geçmişi</h3>
        <button class="btn btn-ghost btn-sm" onclick="panelLoglariYukle()">↻ Yenile</button>
      </div>
      <div class="tbl-wrap">
        <table>
          <thead><tr><th>Tarih</th><th>Yetkili</th><th>İşlem</th><th>Detay</th></tr></thead>
          <tbody id="panel-log-tablo"></tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Offline Lisans Üretici -->
  <div class="page" id="page-offline-lisans">
    <div class="page-title">🔒 Çevrimdışı Lisans Üretici</div>
    <div style="display:grid;grid-template-columns:380px 1fr;gap:16px;">
      <!-- Form -->
      <div class="card">
        <h3 style="margin-bottom:14px;">Aktivasyon Kodu Üret</h3>
        <label style="font-size:11px;color:#666;display:block;margin-bottom:4px;">İstek Kodu (Müşteriden alınan REQ-...):</label>
        <input type="text" id="ol-istek-kodu" placeholder="REQ-XXXXXXXXXXXXXXXXXXXX" style="font-family:Consolas;letter-spacing:1px;">
        <label style="font-size:11px;color:#666;display:block;margin:10px 0 4px;">Kime Üretildi (Müşteri/Kurum Adı):</label>
        <input type="text" id="ol-kime" placeholder="Örn: ABC Firması">
        <label style="font-size:11px;color:#666;display:block;margin:10px 0 4px;">Müşteri E-posta (Panelde görünmesi için):</label>
        <input type="email" id="ol-email" placeholder="Örn: musteri@mail.com">
        <label style="font-size:11px;color:#666;display:block;margin:10px 0 4px;">Süre (Gün):</label>
        <input type="number" id="ol-sure" value="30" min="1" max="365">
        <button class="btn btn-primary" style="margin-top:14px;width:100%;" onclick="offlineLisansUret()">⚡ Aktivasyon Kodu Üret</button>
        <div id="ol-hata" style="color:#f87171;font-size:12px;margin-top:8px;display:none;"></div>
      </div>
      <!-- Sonuç -->
      <div class="card" id="ol-sonuc-kart" style="display:none;">
        <h3 style="color:#4caf50;margin-bottom:12px;">✅ Aktivasyon Kodu Üretildi</h3>
        <div style="background:#1b5e2022;border:1px solid #4caf5044;border-radius:8px;padding:18px;margin-bottom:14px;">
          <div style="font-size:10px;color:#666;margin-bottom:6px;">Aktivasyon Kodu (Müşteriye Gönder):</div>
          <div id="ol-akt-kod" style="font-family:Consolas;font-size:15px;font-weight:bold;color:#00e676;letter-spacing:1px;word-break:break-all;"></div>
        </div>
        <div style="display:flex;gap:8px;margin-bottom:14px;">
          <button class="btn btn-success" onclick="olKopyala()" id="ol-kopyala-btn">📋 Kopyala</button>
          <span id="ol-kopyala-ok" style="font-size:12px;color:#4caf50;align-self:center;display:none;">✓ Kopyalandı!</span>
        </div>
        <div style="font-size:12px;color:#888;line-height:1.8;">
          <div>İstek Kodu: <code id="ol-det-istek" style="color:#7eb8ff;"></code></div>
          <div>Süre: <b id="ol-det-sure" style="color:#e0e0e0;"></b> Gün</div>
        </div>
      </div>
    </div>
  </div>

</div><!-- /main -->

<!-- Yetkili Düzenle Modal -->
<div id="yetkili-duzenle-modal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.75);z-index:600;align-items:center;justify-content:center;backdrop-filter:blur(4px);">
  <div style="background:#1a1d2e;border:1px solid #2a2d3e;border-radius:14px;padding:28px;width:540px;max-width:95vw;max-height:92vh;overflow-y:auto;">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;">
      <h3 style="color:#5b8cff;font-size:16px;">✏️ Yetkili Düzenle</h3>
      <button class="btn btn-ghost btn-sm" onclick="yetkiliDuzenleModalKapat()">✕</button>
    </div>
    <div id="yd-bilgi" style="background:#0f1117;border-radius:8px;padding:10px 14px;margin-bottom:16px;font-size:13px;color:#aaa;"></div>

    <div style="margin-bottom:14px;">
      <label style="font-size:11px;color:#666;display:block;margin-bottom:5px;text-transform:uppercase;letter-spacing:0.5px;">Yeni Şifre (boş bırakılırsa değişmez)</label>
      <input type="password" id="yd-sifre" placeholder="Yeni şifre..." style="margin:0;">
    </div>

    <div style="margin-bottom:16px;">
      <label style="font-size:11px;color:#666;display:block;margin-bottom:5px;text-transform:uppercase;letter-spacing:0.5px;">📱 Telegram Chat ID</label>
      <input type="text" id="yd-telegram-id" placeholder="Örn: 123456789" style="margin:0;">
      <label style="display:flex;align-items:center;gap:8px;margin-top:8px;font-size:13px;color:#aaa;cursor:pointer;">
        <input type="checkbox" id="yd-telegram-bildirim"> Telegram bildirimleri alsın
      </label>
    </div>

    <div style="border-top:1px solid #2a2d3e;padding-top:16px;margin-bottom:16px;">
      <div style="font-size:11px;color:#666;margin-bottom:10px;text-transform:uppercase;letter-spacing:0.5px;">🛡️ Yetkiler</div>
      <div style="display:flex;flex-direction:column;gap:7px;font-size:13px;color:#ccc;">
        <label style="display:flex;align-items:center;gap:8px;cursor:pointer;"><input type="checkbox" id="yd-cb-lisans_olustur"> Lisans Oluşturabilme</label>
        <label style="display:flex;align-items:center;gap:8px;cursor:pointer;"><input type="checkbox" id="yd-cb-lisans_sil"> Lisans Silebilme / İptal</label>
        <label style="display:flex;align-items:center;gap:8px;cursor:pointer;"><input type="checkbox" id="yd-cb-hwid_sifirla"> HWID Sıfırlama</label>
        <label style="display:flex;align-items:center;gap:8px;cursor:pointer;"><input type="checkbox" id="yd-cb-sure_uzat"> Lisans Süre Uzatma</label>
        <label style="display:flex;align-items:center;gap:8px;cursor:pointer;"><input type="checkbox" id="yd-cb-talep_onayla"> Lisans Taleplerini Onaylama</label>
        <label style="display:flex;align-items:center;gap:8px;cursor:pointer;"><input type="checkbox" id="yd-cb-kullanici_ekle"> Panel Kullanıcısı (Yetkili) Ekleme</label>
        <label style="display:flex;align-items:center;gap:8px;cursor:pointer;"><input type="checkbox" id="yd-cb-mesaj_yaz"> Mesaj Yazabilme</label>
        <label style="display:flex;align-items:center;gap:8px;cursor:pointer;"><input type="checkbox" id="yd-cb-ip_ban"> IP Banlama &amp; Kaldırma</label>
        <label style="display:flex;align-items:center;gap:8px;cursor:pointer;"><input type="checkbox" id="yd-cb-uyelik_tur"> Üyelik Türleri Yönetimi</label>
        <label style="display:flex;align-items:center;gap:8px;cursor:pointer;"><input type="checkbox" id="yd-cb-offline_paket_yonetimi"> 🔒 Çevrimdışı Paket/Tür Yönetimi</label>
        <label style="display:flex;align-items:center;gap:8px;cursor:pointer;"><input type="checkbox" id="yd-cb-offline_lisans_uret"> 🔒 Çevrimdışı Lisans Üretme</label>
      </div>
    </div>

    <div style="display:flex;gap:12px;margin-top:18px;">
      <button class="btn btn-primary" style="flex:1;" onclick="yetkiliDuzenleKaydet()">💾 Değişiklikleri Kaydet</button>
      <button class="btn btn-ghost" onclick="yetkiliDuzenleModalKapat()">İptal</button>
    </div>
    <div id="yd-sonuc" style="margin-top:10px;font-size:13px;display:none;"></div>
  </div>
</div>
<div class="notif" id="notif"></div>

<script>
let TOKEN = "";
let secilenTalepId = null;
let secilenKullaniciId = null;

function auth() {
  return {"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"};
}

function notif(msg, hata = false) {
  const el = document.getElementById("notif");
  el.textContent = msg;
  el.className = "notif" + (hata ? " error" : "") + " show";
  setTimeout(() => el.className = "notif" + (hata ? " error" : ""), 2800);
}

let _panelPollTimer = null;
let _aktifSayfa = "lisanslar";

function arayuzuYetkilendir() {
  if (window.IS_ADMIN) {
    document.querySelectorAll(".yetki-admin-only").forEach(el => el.style.display = "");
  }
  // Buton yetkileri
  const y = window.YETKILER || {};
  const goster = (cls, yetki) => {
    document.querySelectorAll("." + cls).forEach(el => {
      if (window.IS_ADMIN || y[yetki]) el.style.display = "";
      else el.style.display = "none";
    });
  };
  goster("yetki-lisans-olustur", "lisans_olustur");
  goster("yetki-lisans-sil", "lisans_sil");
  goster("yetki-hwid-sifirla", "hwid_sifirla");
  goster("yetki-sure-uzat", "sure_uzat");
  goster("yetki-ip-ban", "ip_ban");
  goster("yetki-uyelik-tur", "uyelik_tur");
  goster("yetki-offline-lisans", "offline_lisans");
  // Talep onayla butonu ve JS içi render kısımlarını ayrıca idare edeceğiz.
}

function updateGreeting() {
  const hr = new Date().getHours();
  let msj = "İyi geceler";
  if (hr >= 6 && hr < 12) msj = "Günaydın";
  else if (hr >= 12 && hr < 18) msj = "İyi günler";
  else if (hr >= 18 && hr < 24) msj = "İyi akşamlar";
  
  const el = document.getElementById("panel-greeting");
  if (!el) return;
  if (window.IS_ADMIN) {
    el.innerHTML = `<span style="color:#5b8cff">🛡️ Ana Admin Paneli</span>`;
  } else {
    el.innerHTML = `${msj}, <span style="color:#e0e0e0">${window.ISIM_SOYAD || window.KULLANICI_ADI}</span>`;
  }
}

function panelGiris() {
  const k = document.getElementById("inp-kullanici").value;
  const s = document.getElementById("inp-sifre").value;
  fetch("/panel/giris", {
    method:"POST", 
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({kullanici: k, sifre: s})
  })
    .then(r => r.json())
    .then(d => {
      if (d.basarili) {
        TOKEN = k + ":" + s;
        window.IS_ADMIN = d.is_admin;
        window.YETKILER = d.yetkiler;
        window.ISIM_SOYAD = d.isim_soyad;
        window.KULLANICI_ADI = d.kullanici_adi;
        arayuzuYetkilendir();
        updateGreeting();
        
        document.getElementById("login-overlay").style.display = "none";
        turleriYukle();
        lisanslariYukle();
        badgeGuncelle();
        // Aktif sayfayı 15 saniyede bir otomatik yenile
        _panelPollTimer = setInterval(() => {
          panelOtoPoll();
          badgeGuncelle();
        }, 15000);
        istatistikYukle();
      } else {
        document.getElementById("login-hata").textContent = d.detail || "Giriş başarısız.";
      }
    }).catch(e => {
       document.getElementById("login-hata").textContent = "Giriş yapılamadı.";
    });
}

function panelCikis() {
  fetch("/panel/cikis", {method:"POST", headers:auth()}).then(()=>{
    location.reload();
  });
}

function panelOtoPoll() {
  const yukle = {
    lisanslar:       lisanslariYukle,
    "tum-lisanslar": lisanslariYukle,
    "yeni-lisans":   turleriYukle,
    "lisans-islemleri": () => {},
    "lisans-istatistikleri": istatistikYukle,
    "uyelik-turleri": turleriYukle,
    talepler:        taleplerYukle,
    mesajlar:        mesajlariYukle,
    kullanicilar:    kullanicilariYukle,
    "ip-banlar":     ipBanlariYukle,
    loglar:          logYukle,
    yetkililer:      yetkilileriYukle,
    "panel-loglari": panelLoglariYukle,
    "offline-lisans": () => {
       const el1 = document.getElementById("ol-istek-kodu");
       const el2 = document.getElementById("ol-sonuc-kart");
       const el3 = document.getElementById("ol-hata");
       if (el1) el1.value = "";
       if (el2) el2.style.display = "none";
       if (el3) el3.style.display = "none";
    },
  };
  if (yukle[_aktifSayfa]) yukle[_aktifSayfa]();
}

function sayfaAc(sayfa) {
  document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
  document.querySelectorAll(".nav-item, .acc-item").forEach(n => n.classList.remove("active"));
  const pageEl = document.getElementById("page-" + sayfa);
  if (pageEl) pageEl.classList.add("active");
  const navEl = document.getElementById("nav-" + sayfa);
  if (navEl) navEl.classList.add("active");
  _aktifSayfa = sayfa;

  const yukle = {
    lisanslar:           lisanslariYukle,
    "tum-lisanslar":     lisanslariYukle,
    "yeni-lisans":       turleriYukle,
    "lisans-islemleri":  () => {},
    "lisans-istatistikleri": istatistikYukle,
    "uyelik-turleri":    turleriYukle,
    talepler:            taleplerYukle,
    mesajlar:            mesajlariYukle,
    kullanicilar:        kullanicilariYukle,
    "ip-banlar":         ipBanlariYukle,
    loglar:              logYukle,
    yetkililer:          yetkilileriYukle,
    "panel-loglari":     panelLoglariYukle,
  };
  if (yukle[sayfa]) yukle[sayfa]();
}

async function badgeGuncelle() {
  // Talepler
  const tr = await fetch("/panel/talepler", {headers: auth()}).then(r => r.json()).catch(() => []);
  const bekleyen = tr.filter ? tr.filter(t => t.durum === "beklemede").length : 0;
  const tb = document.getElementById("talep-badge");
  tb.textContent = bekleyen;
  tb.style.display = bekleyen > 0 ? "" : "none";

  // Mesajlar
  const mr = await fetch("/panel/mesajlar-ozet", {headers: auth()}).then(r => r.json()).catch(() => []);
  const okunmamis = mr.reduce ? mr.reduce((s, m) => s + m.okunmamis, 0) : 0;
  const mb = document.getElementById("mesaj-badge");
  mb.textContent = okunmamis;
  mb.style.display = okunmamis > 0 ? "" : "none";
}

// ===== LİSANSLAR =====
function lisansOlustur() {
  const ozel_val = document.getElementById("l-ozel-gun").value;
  const b = {
    musteri_adi: document.getElementById("l-adi").value,
    musteri_email: document.getElementById("l-email").value,
    tur: document.getElementById("l-tur").value,
    deneme_saat: parseInt(document.getElementById("l-saat").value) || 24,
    ozel_gun: ozel_val !== "" ? parseInt(ozel_val) : null,
    notlar: document.getElementById("l-not").value,
  };
  if (!b.musteri_adi) { notif("Müşteri adı zorunlu!", true); return; }
  fetch("/panel/lisans-olustur", {method:"POST", headers:auth(), body:JSON.stringify(b)})
    .then(r => r.json())
    .then(d => {
      if (d.lisans_kodu) {
        document.getElementById("l-sonuc").textContent = "✅ " + d.lisans_kodu + " | " + d.bitis_tarihi;
        notif("Lisans oluşturuldu: " + d.lisans_kodu);
        lisanslariYukle();
      } else {
        notif(d.detail || "Hata", true);
      }
    });
}

function iptalEt() {
  const k = document.getElementById("l-islem-kod").value;
  if (!k) { notif("Lisans kodu girin!", true); return; }
  if (!confirm(k + " iptal edilsin mi?")) return;
  fetch("/panel/iptal?lisans_kodu=" + encodeURIComponent(k), {method:"POST", headers:auth()})
    .then(r => r.json()).then(d => { notif(d.mesaj || d.detail, !!d.detail); lisanslariYukle(); });
}

function hwIdSifirla() {
  const k = document.getElementById("l-islem-kod").value;
  if (!k) { notif("Lisans kodu girin!", true); return; }
  fetch("/panel/hwid-sifirla?lisans_kodu=" + encodeURIComponent(k), {method:"POST", headers:auth()})
    .then(r => r.json()).then(d => { notif(d.mesaj || d.detail, !!d.detail); lisanslariYukle(); });
}

function sureUzat() {
  const k = document.getElementById("l-islem-kod").value;
  const g = document.getElementById("l-uzat-gun").value;
  if (!k) { notif("Lisans kodu girin!", true); return; }
  fetch("/panel/sure-uzat?lisans_kodu=" + encodeURIComponent(k) + "&gun=" + g, {method:"POST", headers:auth()})
    .then(r => r.json()).then(d => { notif(d.mesaj || d.detail, !!d.detail); lisanslariYukle(); });
}

function lisansSil(lisansKodu) {
  if (!confirm(lisansKodu + " lisansı kalıcı olarak silinecek. Bu işlem geri alınamaz. Emin misiniz?")) return;
  fetch("/panel/lisans-sil/" + encodeURIComponent(lisansKodu), {method: "DELETE", headers: auth()})
    .then(r => r.json())
    .then(d => { notif(d.mesaj || d.detail, !!d.detail); lisanslariYukle(); istatistikYukle(); });
}

let _aktifFiltre = "hepsi";
let _nedenChart = null;

function filtreAyarla(f) {
  _aktifFiltre = f;
  // Buton aktif/pasif güncelle
  ["hepsi","aktif","biten","iptal"].forEach(x => {
    const el = document.getElementById("fb-" + x);
    if (!el) return;
    const baseClass = x === "hepsi" ? "aktif" : x + "-f";
    if (x === f) el.className = "filtre-btn " + baseClass;
    else el.className = "filtre-btn";
  });
  lisanslariYukle();
}

function istatistikYukle() {
  fetch("/panel/iptal-istatistikleri", {headers: auth()}).then(r => r.json()).then(d => {
    const o = d.ozet;
    document.getElementById("is-toplam").textContent = o.toplam;
    document.getElementById("is-aktif").textContent  = o.aktif;
    document.getElementById("is-biten").textContent  = o.biten;
    document.getElementById("is-iptal").textContent  = o.iptal;
    // Filtre sayı badge'ları
    document.getElementById("fb-hepsi-cnt").textContent = o.toplam;
    document.getElementById("fb-aktif-cnt").textContent = o.aktif;
    document.getElementById("fb-biten-cnt").textContent = o.biten;
    document.getElementById("fb-iptal-cnt").textContent = o.iptal;
    // İptal nedenleri
    const nedenler = d.nedenler || [];
    const bolum = document.getElementById("neden-bolum");
    if (!nedenler.length) { bolum.style.display = "none"; return; }
    bolum.style.display = "";
    const toplam_iptal = nedenler.reduce((s, n) => s + n.sayi, 0);
    document.getElementById("neden-bars").innerHTML = nedenler.map(n => {
      const yuzde = Math.round((n.sayi / toplam_iptal) * 100);
      return `<div style="margin-bottom:10px;">
        <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px;">
          <span style="color:#ccc;">${n.neden}</span>
          <span style="color:#888;">${n.sayi} (${yuzde}%)</span>
        </div>
        <div style="background:#1e2033;border-radius:4px;height:6px;">
          <div style="background:#ef4444;width:${yuzde}%;height:6px;border-radius:4px;transition:width 0.4s;"></div>
        </div>
      </div>`;
    }).join("");
    // Donut grafik
    const canvas = document.getElementById("neden-chart");
    if (_nedenChart) { _nedenChart.destroy(); _nedenChart = null; }
    _nedenChart = new Chart(canvas, {
      type: "doughnut",
      data: {
        labels: nedenler.map(n => n.neden),
        datasets: [{ data: nedenler.map(n => n.sayi),
          backgroundColor: ["#ef4444","#f59e0b","#3b82f6","#8b5cf6","#10b981","#ec4899","#06b6d4"],
          borderColor: "#0f1117", borderWidth: 2 }]
      },
      options: { responsive: true, maintainAspectRatio: false, plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (c) => ` ${c.label}: ${c.raw}` } }
      }}
    });
  }).catch(() => {});
}

function lisanslariYukle() {
  fetch("/panel/lisanslar?filtre=" + _aktifFiltre, {headers: auth()}).then(r => r.json()).then(liste => {
    const turBadge = {aylik:"b-aylik",yillik:"b-yillik",omur_boyu:"b-omur",deneme:"b-deneme"};
    const durumBadge = {
      aktif:         '<span class="badge b-aktif">✓ Aktif</span>',
      suresi_dolmus: '<span class="badge" style="background:#f59e0b22;color:#fbbf24;border:1px solid #f59e0b55;">⏱ Süresi Doldu</span>',
      iptal:         '<span class="badge b-pasif">✗ İptal</span>',
    };

    // Online ve Offline lisansları ayır
    const online = liste.filter(l => {
      const tip = (l.uretilen_tip || "").toLowerCase();
      const notlar = (l.notlar || "").toLowerCase();
      return tip !== "offline" && !notlar.startsWith("offline");
    });
    const offline = liste.filter(l => {
      const tip = (l.uretilen_tip || "").toLowerCase();
      const notlar = (l.notlar || "").toLowerCase();
      return tip === "offline" || notlar.startsWith("offline");
    });

    // Online tablo
    const onlineTablo = document.getElementById("l-tablo-online");
    if (onlineTablo) {
      onlineTablo.innerHTML = online.map(l => `
        <tr>
          <td><code>${l.lisans_kodu}</code></td>
          <td>${l.musteri_adi}<br><span style="color:#555;font-size:11px;">${l.musteri_email||""}</span></td>
          <td><span class="badge ${turBadge[l.tur]||""}"> ${l.tur}</span></td>
          <td>${durumBadge[l.durum] || l.durum}</td>
          <td style="font-family:monospace;font-size:11px;color:#555;">${(l.hwid||"—").substring(0,18)}</td>
          <td>${l.bitis_tarihi}</td>
          <td>${l.son_checkin}</td>
          <td style="color:#666;font-size:11px;">${l.notlar||""}${l.iptal_nedeni ? `<br><span style="color:#f87171;">İptal: ${l.iptal_nedeni}</span>` : ""}</td>
          <td><button class="btn btn-danger btn-sm" onclick="lisansSil('${l.lisans_kodu}')">🗑 Sil</button></td>
        </tr>`).join("") || '<tr><td colspan="9" style="color:#555;text-align:center;padding:20px;">Kayıt yok</td></tr>';
    }

    // Offline tablo
    const offlineTablo = document.getElementById("l-tablo-offline");
    if (offlineTablo) {
      offlineTablo.innerHTML = offline.map(l => {
        // istek kodunu notlar'dan veya istek_kodu alanından çek
        let istekKodu = l.istek_kodu || "";
        if (!istekKodu && (l.notlar||"").includes("|")) istekKodu = l.notlar.split("|")[1] || "";
        const yetki = l.yetki || "FULL";
        const sureGun = l.sure_gun || "—";
        return `<tr>
          <td><code style="color:#a78bfa;">${l.lisans_kodu}</code></td>
          <td>${l.musteri_adi}<br><span style="color:#555;font-size:11px;">${l.musteri_email||""}</span></td>
          <td><span class="badge" style="background:#a78bfa22;color:#a78bfa;border:1px solid #a78bfa44;">${yetki}</span></td>
          <td>${sureGun !== "—" ? sureGun + " Gün" : "—"}</td>
          <td>${istekKodu ? `<code style="color:#7eb8ff;font-size:11px;">${istekKodu}</code>` : '<span style="color:#555;">—</span>'}</td>
          <td>${durumBadge[l.durum] || l.durum}</td>
          <td style="color:#666;font-size:11px;">${l.iptal_nedeni ? `<span style="color:#f87171;">İptal: ${l.iptal_nedeni}</span>` : "—"}</td>
          <td><button class="btn btn-danger btn-sm" onclick="lisansSil('${l.lisans_kodu}')">🗑 Sil</button></td>
        </tr>`;
      }).join("") || '<tr><td colspan="8" style="color:#555;text-align:center;padding:20px;">Henüz offline lisans üretilmemiş</td></tr>';
    }

    // Geriye dönük uyumluluk - eski l-tablo varsa onu da doldur
    const eskiTablo = document.getElementById("l-tablo");
    if (eskiTablo) {
      eskiTablo.innerHTML = liste.map(l => `
        <tr>
          <td><code>${l.lisans_kodu}</code></td>
          <td>${l.musteri_adi}<br><span style="color:#555;font-size:11px;">${l.musteri_email||""}</span></td>
          <td><span class="badge ${turBadge[l.tur]||""}"> ${l.tur}</span></td>
          <td>${durumBadge[l.durum] || l.durum}</td>
          <td style="font-family:monospace;font-size:11px;color:#555;">${(l.hwid||"").substring(0,18)}</td>
          <td>${l.bitis_tarihi}</td>
          <td>${l.son_checkin}</td>
          <td>${l.aktivasyon}</td>
          <td style="color:#666;font-size:11px;">${l.notlar||""}${l.iptal_nedeni ? `<br><span style="color:#f87171;">İptal: ${l.iptal_nedeni}</span>` : ""}</td>
          <td><button class="btn btn-danger btn-sm" onclick="lisansSil('${l.lisans_kodu}')">🗑 Sil</button></td>
        </tr>`).join("");
    }
  });
}

// ===== TALEPLER =====
function taleplerYukle() {
  fetch("/panel/talepler", {headers: auth()}).then(r => r.json()).then(liste => {
    const durumBadge = {beklemede:"b-beklemede",onaylandi:"b-onaylandi",reddedildi:"b-reddedildi"};
    document.getElementById("talep-tablo").innerHTML = liste.map(t => `
      <tr>
        <td><input type="checkbox" class="talep-cb" value="${t.id}" onchange="talepSecimGuncelle()"></td>
        <td>${t.tarih}</td>
        <td>${t.ad_soyad}</td>
        <td>${t.email}</td>
        <td>${t.tur} ${t.talep_tipi === "offline" ? `<br><span style="font-size:10px;padding:2px 6px;border-radius:4px;background:#3d6fff22;color:#3d6fff;border:1px solid #3d6fff44;">OFFLINE</span>` : ""}</td>
        <td><code>${t.ip||"-"}</code></td>
        <td><span class="badge ${durumBadge[t.durum]||""}">` + t.durum + `</span></td>
        <td style="white-space:nowrap;">
          ${t.durum==="beklemede" ? `<button class="btn btn-primary btn-sm" onclick="talepModalAc('${t.id}','${t.ad_soyad}','${t.email}','${t.tur}','${t.ip||''}','${t.talep_tipi||'online'}','${t.istek_kodu||''}')">İşlem</button>` : (t.admin_notu ? `<span style="color:#666;font-size:11px;">${t.admin_notu.substring(0,30)}</span>` : "—")}
          <button class="btn btn-sm" style="background:#7f1d1d;color:#fca5a5;border:1px solid #991b1b;margin-left:4px;" onclick="talepKaliciSil('${t.id}','${t.ad_soyad}')" title="Kalıcı Olarak Sil">🗑</button>
        </td>
      </tr>`).join("");
    document.getElementById("talep-hepsi-cb").checked = false;
    document.getElementById("talep-toplu-sil-btn").style.display = "none";
    badgeGuncelle();
  });
}

function talepSecimGuncelle() {
  const secilen = document.querySelectorAll(".talep-cb:checked").length;
  const btn = document.getElementById("talep-toplu-sil-btn");
  btn.style.display = secilen > 0 ? "" : "none";
  btn.textContent = `🗑 ${secilen} Talebi Kalıcı Sil`;
}

function talepTumunuSec(durum) {
  document.querySelectorAll(".talep-cb").forEach(cb => cb.checked = durum);
  talepSecimGuncelle();
}

function talepKaliciSil(id, ad) {
  if (!confirm(`"${ad}" adlı kullanıcının bu talebi VERİTABANINDAN KALICI OLARAK silinecek.\n\nBu işlem GERİ ALINAMAZ. Emin misiniz?`)) return;
  fetch(`/panel/talep-sil/${id}`, {method:"DELETE", headers:auth()})
    .then(r => r.json())
    .then(d => { notif(d.basarili ? "Talep kalıcı olarak silindi" : (d.detail || "Hata"), !d.basarili); taleplerYukle(); });
}

function talepTopluSil() {
  const ids = [...document.querySelectorAll(".talep-cb:checked")].map(cb => cb.value);
  if (!ids.length) return;
  if (!confirm(`${ids.length} talep VERİTABANINDAN KALICI OLARAK silinecek.\n\nBu işlem GERİ ALINAMAZ. Emin misiniz?`)) return;
  fetch("/panel/talep-toplu-sil", {method:"POST", headers:auth(), body:JSON.stringify({ids})})
    .then(r => r.json())
    .then(d => { notif(`${d.silinen || ids.length} talep kalıcı silindi`); taleplerYukle(); });
}

function talepModalAc(id, ad, email, tur, ip, tip, istekKodu) {
  secilenTalepId = id;
  let ekOfflineBilgi = tip === "offline" ? `<div style="background:#3d6fff11;border:1px solid #3d6fff33;padding:8px;border-radius:6px;margin-top:8px;font-size:13px;"><b style="color:#3d6fff;">OFFLINE TALEP</b><br>İstek Kodu: <code style="color:#fff;">${istekKodu}</code><br><span style="color:#888;font-size:11px;">Onaylandığında otomatik aktivasyon kodu üretilecektir.</span></div>` : "";
  document.getElementById("talep-bilgi").innerHTML = `<b>${ad}</b> &lt;${email}&gt;<br>Tür: <b>${tur}</b> | IP: <code>${ip}</code>${ekOfflineBilgi}`;
  document.getElementById("talep-not").value = "";
  const m = document.getElementById("talep-modal");
  m.style.display = "flex";
}

function talepModalKapat() {
  document.getElementById("talep-modal").style.display = "none";
  secilenTalepId = null;
}

function talepIsle(durum) {
  if (!secilenTalepId) return;
  fetch("/panel/talep-guncelle", {method:"POST", headers:auth(), body:JSON.stringify({
    talep_id: secilenTalepId,
    durum: durum,
    admin_notu: document.getElementById("talep-not").value,
  })}).then(r => r.json()).then(d => {
    notif(durum === "onaylandi" ? "Talep onaylandı" : "Talep reddedildi");
    talepModalKapat();
    taleplerYukle();
  });
}

// ===== MESAJLAR =====
function mesajlariYukle() {
  fetch("/panel/mesajlar-ozet", {headers: auth()}).then(r => r.json()).then(liste => {
    const convList = document.getElementById("conv-list");
    convList.innerHTML = liste.map(m => `
      <div class="conv-item ${m.kullanici_id === secilenKullaniciId ? 'active' : ''}"
           onclick="konusmaSec('${m.kullanici_id}')">
        <div class="conv-avatar">${m.ad_soyad[0]}</div>
        <div class="conv-info">
          <div class="conv-name">${m.ad_soyad}</div>
          <div class="conv-preview">${m.son_mesaj || "…"}</div>
        </div>
        <div class="conv-meta">
          <span style="font-size:10px;color:#555;">${m.son_mesaj_tar}</span>
          ${m.okunmamis > 0 ? `<span class="unread-dot">${m.okunmamis}</span>` : ""}
        </div>
      </div>`).join("");
    badgeGuncelle();
  });
}

let _konusmaPollTimer = null;

function konusmaSec(kullaniciId) {
  secilenKullaniciId = kullaniciId;
  mesajlariYukle();
  // Önceki konuşma poll'unu temizle
  if (_konusmaPollTimer) { clearInterval(_konusmaPollTimer); _konusmaPollTimer = null; }
  _konusmaMesajYukle(kullaniciId);
  // Açık konuşmayı 5 saniyede bir canlı güncelle
  _konusmaPollTimer = setInterval(() => {
    if (secilenKullaniciId === kullaniciId) _konusmaMesajYukle(kullaniciId);
    else { clearInterval(_konusmaPollTimer); _konusmaPollTimer = null; }
  }, 5000);
}

function _konusmaMesajYukle(kullaniciId) {
  fetch("/panel/kullanici-mesajlar/" + kullaniciId, {headers: auth()}).then(r => r.json()).then(d => {
    const right = document.getElementById("msg-right");
    // Eğer kullanıcı mesaj kutusuna yazıyorsa sadece mesaj listesini güncelle
    const inputMevcut = document.getElementById("admin-msg-inp");
    const inputDeger = inputMevcut ? inputMevcut.value : null;

    const k = d.kullanici;
    const l = d.lisans;
    const lisansBilgi = l ?
      `<span class="badge b-aktif" style="margin-right:4px;">${l.tur}</span> ${l.kod} — ${l.bitis||"Ömür Boyu"}${l.kalan_gun != null ? ` (${l.kalan_gun} gün)` : ""}` :
      `<span class="badge b-pasif">Lisans Yok</span>`;

    const mesajlerHtml = d.mesajlar.map(m => `
      <div class="msg-sender ${m.gonderen==='admin'?'right':''}">
        <div class="msg-bubble ${m.gonderen}">${m.icerik}</div>
        <div class="msg-time">${m.gonderen==='admin'?'Siz':'Kullanıcı'} · ${m.tarih}</div>
      </div>`).join("");

    if (inputMevcut) {
      // Sadece mesaj listesini güncelle, input ve header dokunma
      const mesajEl = document.getElementById("aktif-mesajlar");
      if (mesajEl) {
        const eskiScroll = mesajEl.scrollHeight - mesajEl.scrollTop;
        mesajEl.innerHTML = mesajlerHtml;
        // Kullanıcı en alttaysa otomatik kaydır
        if (eskiScroll <= mesajEl.clientHeight + 40) mesajEl.scrollTop = mesajEl.scrollHeight;
      }
      // Input değerini koru
      const inp = document.getElementById("admin-msg-inp");
      if (inp && inputDeger !== null) inp.value = inputDeger;
    } else {
    right.innerHTML = `
        <div class="msg-right-header">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
            <div style="font-size:15px;font-weight:700;color:#e0e0e0;">${k.ad_soyad}</div>
            <button class="btn btn-sm" style="background:#7f1d1d;color:#fca5a5;border:1px solid #991b1b;" onclick="mesajKonusmaSil('${kullaniciId}','${k.ad_soyad}')" title="Tüm konuşmayı kalıcı sil">🗑 Konuşmayı Sil</button>
          </div>
          <div class="user-detail">
            <div class="row">
              <div class="field"><label>E-posta</label><span>${k.email}</span></div>
              <div class="field"><label>Son IP</label><span><code>${k.son_ip||"?"}</code></span></div>
              <div class="field"><label>Kayıt Tarihi</label><span>${k.kayit_tar}</span></div>
              <div class="field"><label>Lisans</label><span>${lisansBilgi}</span></div>
            </div>
          </div>
        </div>
        <div class="msg-right-body" id="aktif-mesajlar">
          ${mesajlerHtml}
        </div>
        <div class="msg-right-footer">
          <textarea id="admin-msg-inp" placeholder="Mesajınızı yazın…" onkeydown="if(event.ctrlKey&&event.key==='Enter')adminMesajGonder()"></textarea>
          <div style="display:flex;flex-direction:column;gap:6px;">
            <button class="btn btn-primary btn-sm" onclick="adminMesajGonder()">Gönder</button>
          </div>
        </div>`;
      setTimeout(() => {
        const el = document.getElementById("aktif-mesajlar");
        if (el) el.scrollTop = el.scrollHeight;
      }, 50);
    }
  });
}

function adminMesajGonder() {
  if (!secilenKullaniciId) return;
  const icerik = document.getElementById("admin-msg-inp").value.trim();
  if (!icerik) return;
  document.getElementById("admin-msg-inp").value = "";
  fetch("/panel/admin-mesaj-gonder", {method:"POST", headers:auth(), body:JSON.stringify({
    kullanici_id: secilenKullaniciId,
    icerik: icerik,
  })}).then(r => r.json()).then(() => {
    notif("Mesaj gönderildi");
    _konusmaMesajYukle(secilenKullaniciId);
    mesajlariYukle();
  });
}

function mesajKonusmaSil(kullaniciId, ad) {
  if (!confirm(`"${ad}" kullanıcısına ait TÜM MESAJLAR VERİTABANINDAN KALICI OLARAK silinecek.\n\nBu işlem GERİ ALINAMAZ. Emin misiniz?`)) return;
  fetch(`/panel/mesaj-konusma-sil/${kullaniciId}`, {method:"DELETE", headers:auth()})
    .then(r => r.json())
    .then(d => {
      notif(`${d.silinen || 0} mesaj kalıcı silindi`);
      secilenKullaniciId = null;
      document.getElementById("msg-right").innerHTML = '<div style="flex:1;display:flex;align-items:center;justify-content:center;color:#444;font-size:14px;">Konuşma silindi</div>';
      mesajlariYukle();
    });
}

// ===== KULLANICILAR =====
let _duzenleKullanici = null;

function kullanicilariYukle() {
  fetch("/panel/kullanicilar", {headers: auth()}).then(r => r.json()).then(liste => {
    document.getElementById("kullanici-tablo").innerHTML = liste.map(k => `
      <tr>
        <td>${k.ad_soyad}</td>
        <td>${k.email}</td>
        <td><span class="badge ${k.email_dogrulandi?'b-aktif':'b-pasif'}">${k.email_dogrulandi?'✔':'✗'}</span></td>
        <td>${k.kayit_tar}</td>
        <td>${k.son_giris}</td>
        <td><code>${k.son_ip||"-"}</code></td>
        <td>${k.lisans_kodu ? `<code>${k.lisans_kodu}</code> <span class="badge">${k.lisans_tur||""}</span>` : '<span style="color:#555">Yok</span>'}</td>
        <td>
          <div style="display:flex;gap:4px;">
            <button class="btn btn-primary btn-sm" onclick="kullaniciDuzenleModalAc('${k.id}','${(k.ad_soyad||'').replace(/'/g,'&#39;')}','${k.email}')">✏️ Düzenle</button>
            <button class="btn btn-danger btn-sm" onclick="kullaniciSil('${k.id}','${(k.ad_soyad||'').replace(/'/g,'&#39;')}')">Sil</button>
          </div>
        </td>
      </tr>`).join("");
  });
}

function kullaniciDuzenleModalAc(id, ad, email) {
  _duzenleKullanici = {id, ad, email};
  document.getElementById("kd-bilgi").innerHTML = `<b style="color:#e0e0e0;">${ad}</b> &lt;${email}&gt;`;
  document.getElementById("kd-sifre").value = "";
  document.getElementById("kd-not").value = "";
  document.getElementById("kd-sonuc").style.display = "none";
  const m = document.getElementById("kullanici-duzenle-modal");
  m.style.display = "flex";
}

function kullaniciDuzenleModalKapat() {
  document.getElementById("kullanici-duzenle-modal").style.display = "none";
  _duzenleKullanici = null;
}

function kullaniciDuzenleKaydet() {
  if (!_duzenleKullanici) return;
  const sifre = document.getElementById("kd-sifre").value.trim();
  const not = document.getElementById("kd-not").value.trim();
  const sonucEl = document.getElementById("kd-sonuc");

  if (sifre && sifre.length < 6) {
    sonucEl.textContent = "❌ Şifre en az 6 karakter olmalıdır.";
    sonucEl.style.color = "#f87171";
    sonucEl.style.display = "block";
    return;
  }

  const payload = {};
  if (sifre) payload.sifre = sifre;
  if (not) payload.not = not;

  fetch("/panel/kullanici-duzenle/" + _duzenleKullanici.id, {
    method: "PUT",
    headers: auth(),
    body: JSON.stringify(payload)
  }).then(r => r.json()).then(d => {
    if (d.basarili) {
      sonucEl.textContent = "✅ Değişiklikler kaydedildi.";
      sonucEl.style.color = "#4caf50";
      sonucEl.style.display = "block";
      setTimeout(() => kullaniciDuzenleModalKapat(), 1200);
      kullanicilariYukle();
    } else {
      sonucEl.textContent = "❌ " + (d.detail || "Hata oluştu.");
      sonucEl.style.color = "#f87171";
      sonucEl.style.display = "block";
    }
  }).catch(() => {
    sonucEl.textContent = "❌ Sunucu ile iletişim kurulamadı.";
    sonucEl.style.color = "#f87171";
    sonucEl.style.display = "block";
  });
}

function kullaniciSil(id, ad) {
  if (!confirm(ad + " adlı kullanıcı ve tüm verileri (talepler, mesajlar) silinecek. Aktif lisansı varsa iptal edilecek. Emin misiniz?")) return;
  fetch("/panel/kullanici-sil/" + id, {method: "DELETE", headers: auth()})
    .then(r => r.json())
    .then(d => { notif(d.mesaj || d.detail, !!d.detail); kullanicilariYukle(); });
}

// ===== IP BAN =====
function ipBanEkle() {
  const ip = document.getElementById("ban-ip").value.trim();
  const sebep = document.getElementById("ban-sebep").value.trim();
  if (!ip) { notif("IP adresi girin!", true); return; }
  fetch("/panel/ip-ban-ekle", {method:"POST", headers:auth(), body:JSON.stringify({ip, sebep})})
    .then(r => r.json()).then(d => { notif(d.mesaj || d.detail, !!d.detail); ipBanlariYukle(); });
}

function ipBanKaldir(ip) {
  fetch("/panel/ip-ban-kaldir", {method:"POST", headers:auth(), body:JSON.stringify({ip})})
    .then(r => r.json()).then(d => { notif(d.mesaj || d.detail, !!d.detail); ipBanlariYukle(); });
}

function ipBanlariYukle() {
  fetch("/panel/ip-banlar", {headers: auth()}).then(r => r.json()).then(liste => {
    document.getElementById("ban-tablo").innerHTML = liste.map(b => `
      <tr>
        <td><code>${b.ip}</code></td>
        <td style="color:#888;">${b.sebep||"—"}</td>
        <td>${b.tarih}</td>
        <td><span class="badge ${b.aktif?'b-pasif':'b-aktif'}">${b.aktif?'Aktif Ban':'Kaldırıldı'}</span></td>
        <td>${b.aktif ? `<button class="btn btn-success btn-sm" onclick="ipBanKaldir('${b.ip}')">Kaldır</button>` : "—"}</td>
      </tr>`).join("");
  });
}

// ===== ÜYELİK TÜRLERİ =====
function turEkle() {
  const kod = document.getElementById("tur-kod").value.trim();
  const ad  = document.getElementById("tur-ad").value.trim();
  const aciklama = document.getElementById("tur-aciklama").value.trim();
  const sure_sel = document.getElementById("tur-sure-select").value;
  let sure_gun = 30;
  if (sure_sel === "custom") {
    const sure_val = document.getElementById("tur-sure-custom").value;
    if (sure_val === "") { notif("Özel Süre (Gün) zorunludur! Sınırsız için 0 girin.", true); return; }
    sure_gun = parseInt(sure_val) || 0;
  } else {
    sure_gun = parseInt(sure_sel) || 0;
  }
  const prefix = document.getElementById("tur-prefix").value.trim() || "STD";
  const sira = parseInt(document.getElementById("tur-sira").value) || 99;
  const is_offline = document.getElementById("tur-is-offline").checked;
  if (!kod || !ad) { notif("Kod ve ad zorunlu!", true); return; }
  fetch("/panel/uyelik-tur-ekle", {method:"POST", headers:auth(), body:JSON.stringify({kod, ad, aciklama, sira, sure_gun, prefix, is_offline})})
    .then(r => r.json()).then(d => { notif(d.basarili ? "Tür eklendi" : d.detail, !d.basarili); turleriYukle(); });
}

function turSil(id) {
  if (!confirm("Bu türü silmek istediğinizden emin misiniz?")) return;
  fetch("/panel/uyelik-tur-sil/" + id, {method:"DELETE", headers:auth()})
    .then(r => r.json()).then(d => { notif(d.basarili ? "Tür silindi" : d.detail, !d.basarili); turleriYukle(); });
}

function turToggle(id, aktif) {
  fetch("/panel/uyelik-tur-guncelle", {method:"POST", headers:auth(), body:JSON.stringify({id, aktif: !aktif})})
    .then(() => turleriYukle());
}

function turleriYukle() {
  fetch("/panel/uyelik-turleri", {headers: auth()}).then(r => r.json()).then(liste => {
    document.getElementById("tur-grid").innerHTML = liste.map(t => `
      <div class="tur-card" style="opacity:${t.aktif?1:0.5}">
        <div class="tur-kod">${t.kod}</div>
        <h4>${t.ad}</h4>
        <div class="tur-aciklama">${t.aciklama||"—"}</div>
        <div style="font-size:11px;color:#888;margin-top:6px;">Süre: ${t.sure_gun===0 ? 'Ömür Boyu' : t.sure_gun + ' Gün'} | Ön Ek: ${t.prefix}</div>
        <div class="row-btns" style="margin-top:8px;">
          <button class="btn btn-ghost btn-sm" onclick="turToggle(${t.id},${t.aktif})">${t.aktif?"Pasif Et":"Aktif Et"}</button>
          <button class="btn btn-danger btn-sm" onclick="turSil(${t.id})">Sil</button>
        </div>
      </div>`).join("");
      
    const ltur = document.getElementById("l-tur");
    if (ltur) {
      ltur.innerHTML = liste.filter(t => t.aktif).map(t => `<option value="${t.kod}">${t.ad} (${t.sure_gun === 0 ? 'Ömür Boyu' : t.sure_gun + ' Gün'})</option>`).join("");
    }
  });
}

// ===== LOGLAR =====
function logYukle() {
  const son = document.getElementById("log-adet").value;
  fetch("/panel/loglar?son=" + son, {headers: auth()}).then(r => r.json()).then(logs => {
    const renkler = {aktivasyon:"#00e676", kontrol:"#40c4ff", red:"#ff5252"};
    document.getElementById("log-output").innerHTML = logs.map(l =>
      `<span style="color:#555">[${l.tarih}]</span> <span style="color:${renkler[l.islem]||'#aaa'}">${l.islem.toUpperCase().padEnd(12)}</span> <span style="color:#7eb8ff">${l.lisans_kodu}</span> <span style="color:#888">IP:${l.ip}</span> ${l.mesaj}`
    ).join("\n");
  });
}

// ===== YETKİLİLER (RBAC) =====
function adminGuncelle() {
  const kadi = document.getElementById("a-yeni-kadi").value.trim();
  const sifre = document.getElementById("a-yeni-sifre").value.trim();
  if (!kadi || !sifre) { notif("Kullanıcı adı ve şifre boş olamaz!", true); return; }
  
  if (!confirm("Ana admin giriş bilgilerini değiştirmek üzeresiniz. Onaylıyor musunuz?")) return;
  
  fetch("/panel/admin-guncelle", {
    method: "POST", headers: auth(), body: JSON.stringify({yeni_kullanici: kadi, yeni_sifre: sifre})
  }).then(r => r.json()).then(d => {
    notif(d.mesaj || d.detail, !d.basarili);
    if(d.basarili) {
       setTimeout(() => panelCikis(), 1500);
    }
  });
}

function yetkilileriYukle() {
  fetch("/panel/yetkililer", {headers: auth()}).then(r => r.json()).then(liste => {
    if(liste.detail) {
        document.getElementById("yetkili-tablo").innerHTML = `<tr><td colspan="7" style="color:#f87171">${liste.detail}</td></tr>`;
        return;
    }
    const yStr = (y) => Object.entries(y).filter(([k,v]) => v).map(([k,v]) => `<span class="badge b-aktif" style="margin:2px">${k.split('_').join(' ')}</span>`).join("") || '<span style="color:#555">Yok</span>';
    document.getElementById("yetkili-tablo").innerHTML = liste.map(y => `
      <tr>
        <td>${y.kullanici_adi}</td>
        <td>${y.isim_soyad || "-"}</td>
        <td><span class="badge ${y.is_admin ? 'b-onay' : 'b-bekl'}">${y.is_admin ? 'Süper Admin' : 'Yetkili'}</span></td>
        <td style="max-width:200px;line-height:1.8">${y.is_admin ? '<span class="badge b-onay">TÜM YETKİLER</span>' : yStr(y.yetkiler)}</td>
        <td>${y.son_giris}</td>
        <td>${y.son_cikis}</td>
        <td>${!y.is_admin ? `<div style="display:flex;gap:4px;"><button class="btn btn-primary btn-sm" onclick="yetkiliDuzenleModalAc(${y.id},'${y.kullanici_adi}','${y.isim_soyad||''}','${y.telegram_chat_id||''}',${y.telegram_bildirim_alabilir},${JSON.stringify(y.yetkiler).replace(/"/g,'&quot;')})">✏️ Düzenle</button><button class="btn btn-danger btn-sm" onclick="yetkiliSil(${y.id}, '${y.kullanici_adi}')">Sil</button></div>` : "-"}</td>
      </tr>`).join("");
  }).catch(e => {
      document.getElementById("yetkili-tablo").innerHTML = `<tr><td colspan="7" style="color:#f87171">Yetkiniz yok veya yüklenemedi.</td></tr>`;
  });
}

function yetkiliEkle() {
  const kullanici_adi = document.getElementById("y-kadi").value.trim();
  const isim_soyad = document.getElementById("y-isim").value.trim();
  const email = document.getElementById("y-email").value.trim();
  const sifre = document.getElementById("y-sifre").value.trim();
  const yetkiler = {
      lisans_olustur: document.getElementById("cb-lisans_olustur").checked,
      lisans_sil: document.getElementById("cb-lisans_sil").checked,
      hwid_sifirla: document.getElementById("cb-hwid_sifirla").checked,
      sure_uzat: document.getElementById("cb-sure_uzat").checked,
      talep_onayla: document.getElementById("cb-talep_onayla").checked,
      kullanici_ekle: document.getElementById("cb-kullanici_ekle").checked,
      mesaj_yaz: document.getElementById("cb-mesaj_yaz").checked,
      ip_ban: document.getElementById("cb-ip_ban").checked,
      uyelik_tur: document.getElementById("cb-uyelik_tur").checked,
      offline_paket_yonetimi: document.getElementById("cb-offline_paket_yonetimi").checked,
      offline_lisans_uret: document.getElementById("cb-offline_lisans_uret").checked,
  };
  
  if (!kullanici_adi || !email || !sifre || !isim_soyad) { notif("Tüm alanları doldurun!", true); return; }
  
  fetch("/panel/yetkili-ekle", {
      method:"POST", 
      headers:auth(), 
      body:JSON.stringify({kullanici_adi, isim_soyad, email, sifre, yetkiler})
  }).then(r => r.json()).then(d => {
      if(d.basarili) {
          notif("Yetkili başarıyla eklendi");
          document.getElementById("y-kadi").value = "";
          document.getElementById("y-isim").value = "";
          document.getElementById("y-email").value = "";
          document.getElementById("y-sifre").value = "";
          yetkilileriYukle();
      } else {
          notif(d.detail || "Eklenemedi", true);
      }
  });
}

function offlineLisansUret() {
  const req_kodu = document.getElementById("ol-istek-kodu").value.trim();
  const sure     = document.getElementById("ol-sure").value;
  const kime     = document.getElementById("ol-kime").value.trim() || "Bilinmeyen Offline Müşteri";
  const email    = document.getElementById("ol-email").value.trim();
  const hataEl   = document.getElementById("ol-hata");

  hataEl.style.display = "none";
  if(!req_kodu) {
     hataEl.textContent = "İstek Kodu girmeniz gerekiyor.";
     hataEl.style.display = "block";
     return;
  }
  
  fetch("/panel/offline-lisans-uret", {
      method:"POST", 
      headers:auth(),
      body: JSON.stringify({ istek_kodu: req_kodu, sure_gun: parseInt(sure), kime_uretildi: kime, musteri_email: email })
  }).then(r => r.json()).then(d => {
      if(d.basarili) {
          document.getElementById("ol-akt-kod").textContent = d.aktivasyon_kodu;
          document.getElementById("ol-det-istek").textContent = d.istek_kodu;
          document.getElementById("ol-det-sure").textContent = d.sure_gun;
          
          document.getElementById("ol-sonuc-kart").style.display = "block";
          document.getElementById("ol-kopyala-ok").style.display = "none";
          document.getElementById("ol-kopyala-btn").textContent = "📋 Kopyala";
          document.getElementById("ol-istek-kodu").value = "";
          document.getElementById("ol-kime").value = "";
          document.getElementById("ol-email").value = "";
          notif("Aktivasyon kodu üretildi.");
      } else {
          hataEl.textContent = d.detail || "Hata oluştu.";
          hataEl.style.display = "block";
          document.getElementById("ol-sonuc-kart").style.display = "none";
      }
  }).catch(e => {
      hataEl.textContent = "Sunucu ile iletişim kurulamadı.";
      hataEl.style.display = "block";
  });
}

function olKopyala() {
  const txt = document.getElementById("ol-akt-kod").textContent;
  if(!txt) return;
  navigator.clipboard.writeText(txt).then(() => {
      document.getElementById("ol-kopyala-btn").textContent = "✓ Kopyalandı";
      document.getElementById("ol-kopyala-ok").style.display = "inline";
      setTimeout(() => {
          document.getElementById("ol-kopyala-btn").textContent = "📋 Kopyala";
          document.getElementById("ol-kopyala-ok").style.display = "none";
      }, 2000);
  });
}

let _duzenleYetkili = null;

function yetkiliDuzenleModalAc(id, kadi, isim, telegramId, telegramBildirim, yetkillerJson) {
  _duzenleYetkili = id;
  let yetkiler = {};
  try { yetkiler = typeof yetkillerJson === 'string' ? JSON.parse(yetkillerJson) : yetkillerJson; } catch(e) {}
  document.getElementById("yd-bilgi").innerHTML = `<b style="color:#e0e0e0;">${isim||kadi}</b> <span style="color:#666;">(@${kadi})</span>`;
  document.getElementById("yd-sifre").value = "";
  document.getElementById("yd-telegram-id").value = telegramId || "";
  document.getElementById("yd-telegram-bildirim").checked = !!telegramBildirim;
  const cbMap = ["lisans_olustur","lisans_sil","hwid_sifirla","sure_uzat","talep_onayla","kullanici_ekle","mesaj_yaz","ip_ban","uyelik_tur","offline_paket_yonetimi","offline_lisans_uret"];
  cbMap.forEach(k => {
    const el = document.getElementById("yd-cb-" + k);
    if (el) el.checked = !!(yetkiler[k]);
  });
  document.getElementById("yd-sonuc").style.display = "none";
  document.getElementById("yetkili-duzenle-modal").style.display = "flex";
}

function yetkiliDuzenleModalKapat() {
  document.getElementById("yetkili-duzenle-modal").style.display = "none";
  _duzenleYetkili = null;
}

function yetkiliDuzenleKaydet() {
  if (!_duzenleYetkili) return;
  const sonucEl = document.getElementById("yd-sonuc");
  const sifre = document.getElementById("yd-sifre").value.trim();
  const telegramId = document.getElementById("yd-telegram-id").value.trim();
  const telegramBildirim = document.getElementById("yd-telegram-bildirim").checked;

  const cbMap = ["lisans_olustur","lisans_sil","hwid_sifirla","sure_uzat","talep_onayla","kullanici_ekle","mesaj_yaz","ip_ban","uyelik_tur","offline_paket_yonetimi","offline_lisans_uret"];
  const yetkiler = {};
  cbMap.forEach(k => {
    const el = document.getElementById("yd-cb-" + k);
    yetkiler[k] = el ? el.checked : false;
  });

  const payload = { yetkiler, telegram_chat_id: telegramId, telegram_bildirim_alabilir: telegramBildirim };
  if (sifre) payload.sifre = sifre;

  fetch("/panel/yetkili-guncelle/" + _duzenleYetkili, {
    method: "PUT",
    headers: auth(),
    body: JSON.stringify(payload)
  }).then(r => r.json()).then(d => {
    if (d.basarili) {
      sonucEl.textContent = "✅ Değişiklikler kaydedildi.";
      sonucEl.style.color = "#4caf50";
      sonucEl.style.display = "block";
      setTimeout(() => { yetkiliDuzenleModalKapat(); yetkilileriYukle(); }, 1200);
    } else {
      sonucEl.textContent = "❌ " + (d.detail || "Hata oluştu.");
      sonucEl.style.color = "#f87171";
      sonucEl.style.display = "block";
    }
  }).catch(() => {
    sonucEl.textContent = "❌ Sunucu ile iletişim kurulamadı.";
    sonucEl.style.color = "#f87171";
    sonucEl.style.display = "block";
  });
}

function yetkiliSil(id, kadi) {
  if (!confirm(`${kadi} adlı yetkiliyi silmek istediğinize emin misiniz?`)) return;
  fetch("/panel/yetkili-sil/" + id, {method:"DELETE", headers:auth()})
    .then(r => r.json()).then(d => {
        notif(d.mesaj || d.detail, !d.basarili);
        yetkilileriYukle();
    });
}

// ===== PANEL LOGLARI =====
function panelLoglariYukle() {
  fetch("/panel/panel-loglari", {headers: auth()}).then(r => r.json()).then(liste => {
    if(liste.detail) {
        document.getElementById("panel-log-tablo").innerHTML = `<tr><td colspan="4" style="color:#f87171">${liste.detail}</td></tr>`;
        return;
    }
    document.getElementById("panel-log-tablo").innerHTML = liste.map(l => `
      <tr>
        <td style="color:#888">${l.tarih}</td>
        <td style="font-weight:600;color:#5b8cff">${l.kullanici_adi}</td>
        <td><span class="badge b-bekl" style="background:#222540;color:#e0e0e0;border-color:#2a2d3e">${l.islem}</span></td>
        <td style="color:#aaa">${l.detay}</td>
      </tr>`).join("");
  }).catch(e => {
      document.getElementById("panel-log-tablo").innerHTML = `<tr><td colspan="4" style="color:#f87171">Yetkiniz yok veya yüklenemedi.</td></tr>`;
  });
}

// ===== ACCORDION =====
function toggleAccordion(header) {
  const content = header.nextElementSibling;
  const isOpen = content.classList.contains("show");
  if (isOpen) {
    content.classList.remove("show");
    header.classList.remove("open");
  } else {
    content.classList.add("show");
    header.classList.add("open");
  }
}

// ===== YENİ LİSANS ALT SEKMELER =====
function switchYeniLisansTab(tip) {
  document.getElementById("tab-yeni-online").classList.toggle("active", tip === "online");
  document.getElementById("tab-yeni-offline").classList.toggle("active", tip === "offline");
  document.getElementById("pane-yeni-online").classList.toggle("active", tip === "online");
  document.getElementById("pane-yeni-offline").classList.toggle("active", tip === "offline");
}

// ===== YENİ LİSANS SAYFASI - OFFLINE FORM =====
function offlineLisansUretBtn() {
  const kime = document.getElementById("off-kime").value.trim();
  const email = document.getElementById("off-email").value.trim();
  const istek = document.getElementById("off-istek").value.trim().toUpperCase();
  const sure = document.getElementById("off-sure").value;
  const sonucEl = document.getElementById("off-sonuc");

  if (!kime) { sonucEl.textContent = "\u274c Kime \u00fcretildi\u011fini girin!"; sonucEl.style.color="#f87171"; return; }
  if (!istek) { sonucEl.textContent = "\u274c \u0130stek kodunu girin!"; sonucEl.style.color="#f87171"; return; }

  fetch("/panel/offline-lisans-uret", {
    method: "POST",
    headers: auth(),
    body: JSON.stringify({
        istek_kodu: istek,
        sure_gun: parseInt(sure),
        kime_uretildi: kime,
        musteri_email: email
      })
  }).then(r => r.json()).then(d => {
    if (d.basarili) {
      sonucEl.style.color = "#4ade80";
      const kod = d.aktivasyon_kodu || "";
      sonucEl.innerHTML = "\u2705 Aktivasyon Kodu: <b style=\"font-family:Consolas;letter-spacing:1px;\">" + kod + "</b> <button class=\"btn btn-ghost btn-sm\" style=\"margin-left:8px;\" onclick=\"navigator.clipboard.writeText('" + kod + "').then(()=>notif('Kopyaland\u0131!'))\">&#128203; Kopyala</button>";
      document.getElementById("off-istek").value = "";
      document.getElementById("off-kime").value = "";
      document.getElementById("off-email").value = "";
      notif("Offline lisans \u00fcretildi.");
    } else {
      sonucEl.textContent = "\u274c " + (d.detail || "Hata olu\u015ftu.");
      sonucEl.style.color = "#f87171";
    }
  }).catch(() => {
    sonucEl.textContent = "\u274c Sunucu ile ileti\u015fim kurulamad\u0131.";
    sonucEl.style.color = "#f87171";
  });
}

// Startup
document.getElementById("inp-kullanici").focus();
document.addEventListener("keydown", e => {
  if (e.key === "Escape") {
    talepModalKapat();
    yetkiliDuzenleModalKapat();
    kullaniciDuzenleModalKapat();
  }
});
</script>
</body>
</html>"""
