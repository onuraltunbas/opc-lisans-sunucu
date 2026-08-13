/* ═══════════════════════════════════════════════════════════════════════
   Flower Control — Ana JavaScript (MediaPipe Hands + Animasyon)
   main.py'nin web versiyonu — tarayıcıda kamera + el takibi + çiçek
   ═══════════════════════════════════════════════════════════════════════ */

(function () {
  "use strict";

  // ── AYARLAR ──
  const TOPLAM_KARE = 150;
  const FRAMES_PATH = "/static/flower/frames/";
  const HIZALAMA_SURESI = 3; // saniye
  const KALIB1_SURESI = 5;
  const KALIB2_SURESI = 5;

  // ── DURUM DEĞİŞKENLERİ ──
  let durum = "YUKLENIYOR"; // YUKLENIYOR, BEKLEME, KALIB_1, KALIB_2, OYUN
  let hizalamaZamanlayici = 0;
  let zamanlayiciBaslangic = 0;
  let referansElBoyutu = 0;
  let elBoyutlari = [];
  let minMesafeOrani = Infinity;
  let maxMesafeOrani = 0;
  let mevcutKareIndeksi = 0;
  let gelistiriciModu = false;

  // ── DOM ÖĞELERİ ──
  let canvas, ctx;
  let videoElement;
  let statusPanel, statusTitle, statusDesc;
  let countdownEl;
  let stepsContainer;
  let loadingSection, mainSection, fallbackSection;
  let loadingBarFill, loadingText;
  let devPanel;
  let flowerDisplayImg;

  // ── KARE GÖRSELLERİ ──
  let kareler = [];
  let yuklenmisSayisi = 0;

  // ── MediaPipe ──
  let handsInstance = null;
  let kameraAktif = false;

  // ═══════════════════════════════════════
  // BAŞLATMA
  // ═══════════════════════════════════════

  function init() {
    // DOM'u bul
    canvas = document.getElementById("flower-canvas");
    ctx = canvas ? canvas.getContext("2d") : null;
    videoElement = document.getElementById("flower-video");
    statusPanel = document.getElementById("flower-status");
    statusTitle = document.getElementById("flower-status-title");
    statusDesc = document.getElementById("flower-status-desc");
    countdownEl = document.getElementById("flower-countdown");
    stepsContainer = document.getElementById("flower-steps");
    loadingSection = document.getElementById("flower-loading");
    mainSection = document.getElementById("flower-main");
    fallbackSection = document.getElementById("flower-fallback");
    loadingBarFill = document.getElementById("flower-loading-bar-fill");
    loadingText = document.getElementById("flower-loading-text");
    devPanel = document.getElementById("flower-dev-panel");
    flowerDisplayImg = document.getElementById("flower-display-img");

    // Dev toggle butonu
    const devToggle = document.getElementById("flower-dev-toggle");
    if (devToggle) {
      devToggle.addEventListener("click", function () {
        gelistiriciModu = !gelistiriciModu;
        if (devPanel) devPanel.classList.toggle("show", gelistiriciModu);
      });
    }

    // Kamera başlat butonu
    const startBtn = document.getElementById("flower-start-camera");
    if (startBtn) {
      startBtn.addEventListener("click", kameraBaslat);
    }

    // Fallback slider
    const slider = document.getElementById("flower-slider");
    if (slider) {
      slider.addEventListener("input", function () {
        mevcutKareIndeksi = parseInt(this.value);
        fallbackKareGoster(mevcutKareIndeksi);
      });
    }

    // Kareleri yükle
    kareleriYukle();
  }

  // ═══════════════════════════════════════
  // KARE YÜKLEME
  // ═══════════════════════════════════════

  function kareleriYukle() {
    durum = "YUKLENIYOR";
    gosterGizle(loadingSection, true);
    gosterGizle(mainSection, false);
    gosterGizle(fallbackSection, false);

    for (let i = 1; i <= TOPLAM_KARE; i++) {
      const img = new Image();
      const dosyaAdi = "kare_" + String(i).padStart(3, "0") + ".webp";
      img.src = FRAMES_PATH + dosyaAdi + "?v=2";

      img.onload = function () {
        yuklenmisSayisi++;
        yuklemeDurumuGuncelle();
      };

      img.onerror = function () {
        // WebP yüklenemezse PNG dene
        const pngAdi = "kare_" + String(i).padStart(3, "0") + ".png";
        this.src = FRAMES_PATH + pngAdi + "?v=2";
        // Hala hata varsa boş bırak
        this.onerror = function () {
          yuklenmisSayisi++;
          yuklemeDurumuGuncelle();
        };
      };

      kareler[i - 1] = img;
    }
  }

  function yuklemeDurumuGuncelle() {
    const yuzde = Math.round((yuklenmisSayisi / TOPLAM_KARE) * 100);
    if (loadingBarFill) loadingBarFill.style.width = yuzde + "%";
    if (loadingText) loadingText.textContent = "Görseller yükleniyor... " + yuzde + "%";

    if (yuklenmisSayisi >= TOPLAM_KARE) {
      // Yükleme tamamlandı
      setTimeout(function () {
        gosterGizle(loadingSection, false);
        gosterGizle(mainSection, true, "flex");
        durum = "BEKLEME";
        durumGuncelle();
      }, 300);
    }
  }

  // ═══════════════════════════════════════
  // KAMERA BAŞLATMA
  // ═══════════════════════════════════════

  function kameraBaslat() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      fallbackModuAc("Tarayıcınız kamera erişimini desteklemiyor.");
      return;
    }

    // Kamera izni iste
    navigator.mediaDevices
      .getUserMedia({
        video: {
          facingMode: "user",
          width: { ideal: 640 },
          height: { ideal: 360 },
        },
      })
      .then(function (stream) {
        if (!videoElement) return;
        videoElement.srcObject = stream;
        videoElement.play();
        kameraAktif = true;

        // Canvas boyutlarını ayarla
        videoElement.addEventListener("loadedmetadata", function () {
          if (canvas) {
            canvas.width = videoElement.videoWidth;
            canvas.height = videoElement.videoHeight;
          }
          // MediaPipe'ı başlat
          mediaPipeBaslat();
        });
      })
      .catch(function (err) {
        console.warn("Kamera erişim hatası:", err);
        fallbackModuAc("Kamera erişimi reddedildi. Slider ile kontrol edebilirsiniz.");
      });
  }

  // ═══════════════════════════════════════
  // MEDIAPIPE HANDS
  // ═══════════════════════════════════════

  function mediaPipeBaslat() {
    if (typeof Hands === "undefined") {
      // CDN'den yüklenmediyse fallback
      fallbackModuAc("MediaPipe yüklenemedi. Slider ile devam edebilirsiniz.");
      return;
    }

    handsInstance = new Hands({
      locateFile: function (file) {
        return "https://cdn.jsdelivr.net/npm/@mediapipe/hands/" + file;
      },
    });

    handsInstance.setOptions({
      maxNumHands: 2,
      modelComplexity: 1,
      minDetectionConfidence: 0.7,
      minTrackingConfidence: 0.5,
    });

    handsInstance.onResults(elSonuclariIsle);

    // Kamera döngüsünü başlat
    kameraDongusu();
  }

  function kameraDongusu() {
    if (!kameraAktif || !videoElement || videoElement.paused || videoElement.ended) return;

    handsInstance
      .send({ image: videoElement })
      .then(function () {
        requestAnimationFrame(kameraDongusu);
      })
      .catch(function () {
        requestAnimationFrame(kameraDongusu);
      });
  }

  // ═══════════════════════════════════════
  // EL SONUÇLARINI İŞLEME
  // ═══════════════════════════════════════

  function elSonuclariIsle(results) {
    if (!ctx || !canvas) return;

    const w = canvas.width;
    const h = canvas.height;

    // Kamera görüntüsünü çiz (ayna)
    ctx.save();
    ctx.translate(w, 0);
    ctx.scale(-1, 1);
    ctx.drawImage(results.image, 0, 0, w, h);
    ctx.restore();

    // Elleri ayır (sol/sağ — ayna görüntüsü nedeniyle ters)
    let solElLms = null;
    let sagElLms = null;

    if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
      for (let i = 0; i < results.multiHandLandmarks.length; i++) {
        const lms = results.multiHandLandmarks[i];
        const x9 = lms[9].x;
        // Ayna görüntüsünde sol-sağ ters
        if (x9 > 0.5) {
          solElLms = lms;
        } else {
          sagElLms = lms;
        }
      }
    }

    // Durum makinesi
    durumMakinesi(solElLms, sagElLms, w, h);

    // Çiçeği çiz
    cicekCiz(w, h);

    // Geliştirici modu
    if (gelistiriciModu) {
      gelistiriciBilgileriCiz(solElLms, w, h);
    }
  }

  // ═══════════════════════════════════════
  // DURUM MAKİNESİ
  // ═══════════════════════════════════════

  function durumMakinesi(solElLms, sagElLms, w, h) {
    const simdi = Date.now() / 1000;

    if (durum === "BEKLEME") {
      // Kutular
      const solKutu = {
        x1: Math.round(w * 0.1),
        y1: Math.round(h * 0.2),
        x2: Math.round(w * 0.4),
        y2: Math.round(h * 0.8),
      };
      const sagKutu = {
        x1: Math.round(w * 0.6),
        y1: Math.round(h * 0.2),
        x2: Math.round(w * 0.9),
        y2: Math.round(h * 0.8),
      };

      const solOk = elKutudaMi(solElLms, solKutu, w, h);
      const sagOk = elKutudaMi(sagElLms, sagKutu, w, h);

      // Kutuları çiz
      kutuCiz(solKutu, solOk, "Sol El");
      kutuCiz(sagKutu, sagOk, "Sağ El");

      durumPaneliGuncelle(
        "Başlamak İçin Hazırlanın",
        "Ellerinizi ekrandaki kutulara hizalayın ve 3 saniye sabit tutun.",
        0
      );

      if (solOk && sagOk) {
        if (hizalamaZamanlayici === 0) {
          hizalamaZamanlayici = simdi;
        } else {
          const gecen = simdi - hizalamaZamanlayici;
          const kalan = HIZALAMA_SURESI - Math.floor(gecen);
          geriSayimGoster(kalan);

          if (gecen > HIZALAMA_SURESI) {
            durum = "KALIB_1";
            zamanlayiciBaslangic = simdi;
            elBoyutlari = [];
            durumGuncelle();
          }
        }
      } else {
        hizalamaZamanlayici = 0;
        geriSayimGizle();
      }
    } else if (durum === "KALIB_1") {
      const gecen = simdi - zamanlayiciBaslangic;
      const kalan = KALIB1_SURESI - Math.floor(gecen);

      durumPaneliGuncelle(
        "Adım 1: Kalibrasyon",
        "Ellerinizi sabit tutun — referans boyut ölçülüyor.",
        1
      );
      geriSayimGoster(kalan);

      if (gecen > KALIB1_SURESI) {
        if (elBoyutlari.length > 0) {
          referansElBoyutu =
            elBoyutlari.reduce(function (a, b) {
              return a + b;
            }, 0) / elBoyutlari.length;
        } else {
          referansElBoyutu = 100;
        }
        durum = "KALIB_2";
        zamanlayiciBaslangic = simdi;
        durumGuncelle();
      } else if (solElLms) {
        const x0 = solElLms[0].x * w;
        const y0 = solElLms[0].y * h;
        const x9 = solElLms[9].x * w;
        const y9 = solElLms[9].y * h;
        elBoyutlari.push(Math.hypot(x9 - x0, y9 - y0));
      }
    } else if (durum === "KALIB_2") {
      const gecen = simdi - zamanlayiciBaslangic;
      const kalan = KALIB2_SURESI - Math.floor(gecen);

      durumPaneliGuncelle(
        "Adım 2: Parmak Aralığı",
        "Sol elinizin baş ve işaret parmağını açıp kapatın.",
        2
      );
      geriSayimGoster(kalan);

      if (gecen > KALIB2_SURESI) {
        durum = "OYUN";
        durumGuncelle();
        geriSayimGizle();
      } else if (solElLms) {
        const x4 = solElLms[4].x * w;
        const y4 = solElLms[4].y * h;
        const x8 = solElLms[8].x * w;
        const y8 = solElLms[8].y * h;
        const mesafe = Math.hypot(x8 - x4, y8 - y4) / referansElBoyutu;
        if (mesafe < minMesafeOrani) minMesafeOrani = mesafe;
        if (mesafe > maxMesafeOrani) maxMesafeOrani = mesafe;
      }
    } else if (durum === "OYUN") {
      durumPaneliGuncelle(
        "🌸 Çiçek Aktif!",
        "Sol elinizin parmakları ile çiçeği büyütün.",
        3
      );

      mevcutKareIndeksi = 0;

      if (solElLms) {
        const x4 = solElLms[4].x * w;
        const y4 = solElLms[4].y * h;
        const x8 = solElLms[8].x * w;
        const y8 = solElLms[8].y * h;

        const anlikMesafeOrani = Math.hypot(x8 - x4, y8 - y4) / referansElBoyutu;

        let fark = maxMesafeOrani - minMesafeOrani;
        if (fark < 0.01) fark = 0.01;

        let oran =
          Math.max(
            0,
            Math.min(anlikMesafeOrani - minMesafeOrani, maxMesafeOrani - minMesafeOrani)
          ) / fark;
        mevcutKareIndeksi = Math.round(oran * (TOPLAM_KARE - 1));
      }
    }
  }

  // ═══════════════════════════════════════
  // ÇİZİM FONKSİYONLARI
  // ═══════════════════════════════════════

  function cicekCiz(w, h) {
    if (durum !== "OYUN" || kareler.length === 0) return;

    const kare = kareler[mevcutKareIndeksi];
    if (!kare || !kare.complete || kare.naturalWidth === 0) return;

    // Çiçeği sol alt köşeye çiz (orijinal main.py gibi)
    const cicekW = Math.round(w * 0.5);
    const cicekH = Math.round((kare.naturalHeight / kare.naturalWidth) * cicekW);
    const x = 0;
    const y = h - cicekH;

    ctx.drawImage(kare, x, y, cicekW, cicekH);
  }

  function kutuCiz(kutu, ok, etiket) {
    if (!ctx) return;

    ctx.strokeStyle = ok ? "#22c55e" : "#ef4444";
    ctx.lineWidth = 2;
    ctx.strokeRect(kutu.x1, kutu.y1, kutu.x2 - kutu.x1, kutu.y2 - kutu.y1);

    ctx.fillStyle = ok ? "rgba(34,197,94,0.1)" : "rgba(239,68,68,0.05)";
    ctx.fillRect(kutu.x1, kutu.y1, kutu.x2 - kutu.x1, kutu.y2 - kutu.y1);

    ctx.fillStyle = ok ? "#22c55e" : "#ef4444";
    ctx.font = "bold 14px Inter, sans-serif";
    ctx.fillText(etiket, kutu.x1 + 8, kutu.y1 + 22);
  }

  function gelistiriciBilgileriCiz(solElLms, w, h) {
    if (!devPanel) return;

    if (solElLms) {
      const x4 = solElLms[4].x * w;
      const y4 = solElLms[4].y * h;
      const x8 = solElLms[8].x * w;
      const y8 = solElLms[8].y * h;
      const mesafePx = Math.hypot(x8 - x4, y8 - y4);

      let devHTML = '<div class="dev-title">─── GELİŞTİRİCİ MODU ───</div>';
      devHTML +=
        '<div class="dev-row"><span class="dev-label">Durum:</span><span>' +
        durum +
        "</span></div>";
      devHTML +=
        '<div class="dev-row"><span class="dev-label">Mesafe (px):</span><span>' +
        mesafePx.toFixed(1) +
        "</span></div>";
      devHTML +=
        '<div class="dev-row"><span class="dev-label">Kare:</span><span>' +
        mevcutKareIndeksi +
        "/" +
        TOPLAM_KARE +
        "</span></div>";

      if (referansElBoyutu > 0) {
        const anlikOran = mesafePx / referansElBoyutu;
        devHTML +=
          '<div class="dev-row"><span class="dev-label">Oran:</span><span>' +
          anlikOran.toFixed(3) +
          "</span></div>";
        devHTML +=
          '<div class="dev-row"><span class="dev-label">Min/Max:</span><span>' +
          (minMesafeOrani === Infinity ? "0" : minMesafeOrani.toFixed(3)) +
          " / " +
          maxMesafeOrani.toFixed(3) +
          "</span></div>";
      }

      devPanel.innerHTML = devHTML;

      // Canvas üzerine de çizgi çiz
      if (ctx) {
        // Ayna yansıması uygula
        const mx4 = w - x4;
        const mx8 = w - x8;
        ctx.strokeStyle = "#0ff";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(mx4, y4, 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(mx8, y8, 6, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.moveTo(mx4, y4);
        ctx.lineTo(mx8, y8);
        ctx.stroke();
      }
    }
  }

  // ═══════════════════════════════════════
  // UI YARDIMCI FONKSİYONLARI
  // ═══════════════════════════════════════

  function elKutudaMi(elLms, kutu, w, h) {
    if (!elLms) return false;
    // Ayna görüntüsü (mirroring) uygulandığı için x koordinatını ters çeviriyoruz
    const x9 = w - (elLms[9].x * w);
    const y9 = elLms[9].y * h;
    return x9 > kutu.x1 && x9 < kutu.x2 && y9 > kutu.y1 && y9 < kutu.y2;
  }

  function durumPaneliGuncelle(baslik, aciklama, adim) {
    if (statusTitle) statusTitle.textContent = baslik;
    if (statusDesc) statusDesc.textContent = aciklama;

    // Adım göstergesini güncelle
    if (stepsContainer) {
      const steps = stepsContainer.querySelectorAll(".flower-step");
      steps.forEach(function (el, idx) {
        el.classList.remove("active", "done");
        if (idx < adim) el.classList.add("done");
        else if (idx === adim) el.classList.add("active");
      });
    }
  }

  function durumGuncelle() {
    // Durum değiştiğinde UI'ı güncelle
    if (durum === "OYUN") {
      // Status paneli gizle (OYUN modunda çiçek tam görünsün)
      if (statusPanel) {
        statusPanel.style.opacity = "0.6";
        setTimeout(function () {
          if (durum === "OYUN" && statusPanel) {
            statusPanel.style.display = "none";
          }
        }, 3000);
      }
    } else if (statusPanel) {
      statusPanel.style.display = "";
      statusPanel.style.opacity = "1";
    }
  }

  function geriSayimGoster(kalan) {
    if (!countdownEl) return;
    countdownEl.style.display = "inline-flex";
    countdownEl.textContent = Math.max(0, kalan);
  }

  function geriSayimGizle() {
    if (countdownEl) countdownEl.style.display = "none";
  }

  function gosterGizle(el, goster, displayType) {
    if (el) el.style.display = goster ? (displayType || "") : "none";
  }

  // ═══════════════════════════════════════
  // FALLBACK MODU (Kamera yokken)
  // ═══════════════════════════════════════

  function fallbackModuAc(mesaj) {
    gosterGizle(mainSection, false);
    gosterGizle(fallbackSection, true);

    const infoEl = document.getElementById("flower-fallback-info");
    if (infoEl) infoEl.textContent = mesaj;

    // İlk kareyi göster
    fallbackKareGoster(0);
  }

  function fallbackKareGoster(indeks) {
    if (!flowerDisplayImg) return;
    if (indeks < 0) indeks = 0;
    if (indeks >= kareler.length) indeks = kareler.length - 1;
    if (kareler[indeks] && kareler[indeks].src) {
      flowerDisplayImg.src = kareler[indeks].src;
    }
  }

  // ═══════════════════════════════════════
  // SAYFA HAZIR OLUNCA BAŞLAT
  // ═══════════════════════════════════════

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
