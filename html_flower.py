# -*- coding: utf-8 -*-
"""
Flower Control — 3 Sayfa HTML Modülü

Sayfalar:
  FLOWER_HTML   → /flower   (Site entegre, navbar/footer dahil)
  FLOWER1_HTML  → /flower1  (Premium tam ekran)
  FLOWER2_HTML  → /flower2  (Minimal/sade)
"""

# ── Paylaşılan bileşenler ──

_MEDIAPIPE_CDN = """
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js" crossorigin="anonymous"></script>
"""

_HEAD_COMMON = """
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="theme-color" content="#0a0a1a">
<link rel="stylesheet" href="/static/flower/flower_app.css?v=4">
"""

_LOADING_SECTION = """
<div id="flower-loading" class="flower-loading">
  <div class="flower-loading-spinner"></div>
  <div id="flower-loading-text" class="flower-loading-text">Görseller yükleniyor...</div>
  <div class="flower-loading-bar">
    <div id="flower-loading-bar-fill" class="flower-loading-bar-fill"></div>
  </div>
</div>
"""

_STATUS_PANEL = """
<div id="flower-status" class="flower-status-panel">
  <div id="flower-steps" class="flower-steps">
    <div class="flower-step"></div>
    <div class="flower-step"></div>
    <div class="flower-step"></div>
    <div class="flower-step"></div>
  </div>
  <div id="flower-status-title" class="flower-status-title">Hazırlanıyor...</div>
  <div id="flower-countdown" class="flower-countdown" style="display:none;">3</div>
  <div id="flower-status-desc" class="flower-status-desc">Görseller yüklendikten sonra başlayabilirsiniz.</div>
</div>
"""

_CANVAS_AREA = """
<div class="flower-canvas-wrap">
  <canvas id="flower-canvas"></canvas>
  <video id="flower-video" playsinline muted></video>
</div>
"""

_START_BUTTON = """
<div class="flower-btn-group">
  <button id="flower-start-camera" class="flower-btn flower-btn-primary">
    📷 Kamerayı Başlat
  </button>
</div>
"""

_FALLBACK_SECTION = """
<div id="flower-fallback" class="flower-fallback" style="display:none;">
  <div id="flower-fallback-info" class="flower-fallback-info">
    Kamera kullanılamıyor. Slider ile çiçeği kontrol edebilirsiniz.
  </div>
  <div class="flower-display">
    <img id="flower-display-img" src="/static/flower/frames/kare_001.webp?v=2" alt="Çiçek">
  </div>
  <div class="flower-slider-wrap">
    <input type="range" id="flower-slider" class="flower-slider" min="0" max="149" value="0">
    <div class="flower-slider-label">Çiçeği büyütmek için kaydırın →</div>
  </div>
</div>
"""

_DEV_TOOLS = """
<div id="flower-dev-panel" class="flower-dev-panel"></div>
<button id="flower-dev-toggle" class="flower-dev-toggle" title="Geliştirici Modu">🔧</button>
"""

_SCRIPTS = f"""
{_MEDIAPIPE_CDN}
<script src="/static/flower/flower_app.js?v=5"></script>
"""


# ═══════════════════════════════════════════════════════
# SAYFA 1: /flower — Site Entegre
# ═══════════════════════════════════════════════════════

FLOWER_HTML = f"""<!DOCTYPE html>
<html lang="tr">
<head>
  {_HEAD_COMMON}
  <title>Çiçek Kontrolü | Nautilus Technology</title>
  <meta name="description" content="El hareketleriyle çiçeği büyütün — MediaPipe el takibi ile interaktif web deneyimi.">
  <meta name="keywords" content="çiçek kontrol, el takibi, MediaPipe, interaktif, Nautilus Technology">
  <style>
    body {{
      margin: 0;
      padding: 0;
      background: #0a0a1a;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
  </style>
</head>
<body>
  <div class="flower-page flower-integrated">
    <div class="flower-header">
      <h1 class="flower-title">🌸 Çiçek Kontrolü</h1>
      <p class="flower-subtitle">
        Kameranızı açın, ellerinizi hizalayın ve parmak hareketlerinizle çiçeği büyütün.
        Tüm işlemler tarayıcınızda gerçekleşir — hiçbir görüntü sunucuya gönderilmez.
      </p>
    </div>

    {_LOADING_SECTION}

    <div id="flower-main" style="display:none; width:100%; flex-direction:column; align-items:center; gap:16px;">
      {_CANVAS_AREA}
      {_STATUS_PANEL}
      {_START_BUTTON}
    </div>

    {_FALLBACK_SECTION}
    {_DEV_TOOLS}
  </div>

  {_SCRIPTS}
</body>
</html>
"""


# ═══════════════════════════════════════════════════════
# SAYFA 2: /flower1 — Premium Tam Ekran
# ═══════════════════════════════════════════════════════

FLOWER1_HTML = f"""<!DOCTYPE html>
<html lang="tr">
<head>
  {_HEAD_COMMON}
  <title>Çiçek Deneyimi — Premium | Nautilus Technology</title>
  <meta name="description" content="Premium tam ekran çiçek kontrol deneyimi — el takibi ile interaktif animasyon.">
  <style>
    body {{
      margin: 0;
      padding: 0;
      background: #0a0a1a;
      overflow-x: hidden;
    }}
  </style>
</head>
<body>
  <div class="flower-page flower-premium">
    <div class="flower-header">
      <h1 class="flower-title">Çiçek Deneyimi</h1>
      <p class="flower-subtitle">Ellerinizle doğayı kontrol edin</p>
    </div>

    {_LOADING_SECTION}

    <div id="flower-main" class="flower-container" style="display:none;">
      {_CANVAS_AREA}
      {_STATUS_PANEL}
      {_START_BUTTON}
    </div>

    {_FALLBACK_SECTION}
    {_DEV_TOOLS}
  </div>

  {_SCRIPTS}
</body>
</html>
"""


# ═══════════════════════════════════════════════════════
# SAYFA 3: /flower2 — Minimal/Sade
# ═══════════════════════════════════════════════════════

FLOWER2_HTML = f"""<!DOCTYPE html>
<html lang="tr">
<head>
  {_HEAD_COMMON}
  <title>Çiçek</title>
  <meta name="description" content="Minimal çiçek kontrol deneyimi.">
  <style>
    body {{
      margin: 0;
      padding: 0;
      background: #000;
      overflow: hidden;
    }}
  </style>
</head>
<body>
  <div class="flower-page flower-minimal">
    <div class="flower-hint">Kamerayı başlatın ve parmak hareketleriyle kontrol edin</div>

    {_LOADING_SECTION}

    <div id="flower-main" class="flower-container" style="display:none;">
      {_CANVAS_AREA}
      {_STATUS_PANEL}
      {_START_BUTTON}
    </div>

    {_FALLBACK_SECTION}
    {_DEV_TOOLS}
  </div>

  {_SCRIPTS}
</body>
</html>
"""
