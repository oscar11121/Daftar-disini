<?php
// Include settings file
require_once 'settings.php';
?>
<!DOCTYPE html>
<html lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MENU PENDAFTARAN</title>
	<link rel="canonical" href="https://info-cek-data-mkm.up.railway.app" />
  <!-- Meta SEO -->
  <meta name="description" content="MENU PENDAFTARAN" />
  <meta name="keywords" content="PENDAFTARAN" />
  <meta name="author" content="MENU PENDAFTARAN" />
  <!-- Open Graph (Facebook, Telegram, WhatsApp) -->
  <meta property="og:title" content="MENU PENDAFTARAN - Daftar Sekarang" />
  <meta property="og:description" content="MENU PENDAFTARAN" />
  <meta property="og:image" content="static/image.png" />
  <!-- Ganti dengan URL sebenar gambar jika ada -->
  <meta property="og:type" content="website" />
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="MENU PENDAFTARAN" />
  <meta name="twitter:description" content="MENU PENDAFTARAN" />
  <meta name="twitter:image" content="static/image.png" />
  <link rel="icon" href="static/image.png" type="image/x-icon" />
  <meta name="robots" content="nofollow, noindex" />
  <link rel="stylesheet" href="static/css/font.css" />
  <link rel="stylesheet" href="static/css/bootstrap.min.css" />
  <link rel="stylesheet" href="npm/intl-tel-input-18.2.1/build/css/intlTelInput.min.css" />
  <script src="npm/intl-tel-input-18.2.1/build/js/intlTelInput.min.js"></script>
  <script src="static/java/jQuery.min.js"></script>
  <script type="text/plain" data-savepage-src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js"
    ></script>
  <script src="npm/bootstrap-5.1.3/dist/js/bootstrap.bundle.min.js"
    ></script>
    <style>
    body {
      margin: 0;
      padding: 0;
      height: 100vh;
      font-family: Arial, sans-serif;
      background-color: #f9fafb;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
    }

    h2 {
      color: #16a34a;
      margin-bottom: 10px;
    }

    p {
      color: #334155;
      font-size: 16px;
      margin-bottom: 20px;
    }

    img {
      width: 200px;
      height: auto;
      margin-top: 20px;
    }
    </style>
</head>
<body>
  <div style="width: 100%;padding: 0px 16px;max-width: 600px;margin: auto;">
    <div id="carouselExampleControls" class="carousel slide" data-ride="carousel">
      <div class="carousel-inner">
        <div class="carousel-item active">
          <img class="d-block w-100" src="static/image.png" alt="First slide">
        </div>
      </div>
    </div>
    <h1 style="font-size: 22px!important" class="typewrite mt-3 text-center text-primary" data-period="2000" data-type='[ "MASUKKAN DATA DENGAN TEPAT DAN BENAR" ]'>
    <span class="wrap"></span>
</h1>
<script>
  var TxtType = function(el, toRotate, period) {
    this.toRotate = toRotate;
    this.el = el;
    this.loopNum = 0;
    this.period = parseInt(period, 10) || 2000;
    this.txt = '';
    this.tick();
    this.isDeleting = false;
  };
  TxtType.prototype.tick = function() {
    var i = this.loopNum % this.toRotate.length;
    var fullTxt = this.toRotate[i];
    if (this.isDeleting) {
      this.txt = fullTxt.substring(0, this.txt.length - 1);
    } else {
      this.txt = fullTxt.substring(0, this.txt.length + 1);
    }
    this.el.innerHTML = '<span class="wrap">'+this.txt+'</span>';
    var that = this;
    var delta = 200 - Math.random() * 100;
    if (this.isDeleting) { delta /= 2; }
    if (!this.isDeleting && this.txt === fullTxt) {
      delta = this.period;
      this.isDeleting = true;
    } else if (this.isDeleting && this.txt === '') {
      this.isDeleting = false;
      this.loopNum++;
      delta = 500;
    }
    setTimeout(function() {
      that.tick();
    }, delta);
  };
  window.onload = function() {
    var elements = document.getElementsByClassName('typewrite');
    for (var i=0; i<elements.length; i++) {
      var toRotate = JSON.parse(elements[i].getAttribute('data-type'));
      var period = elements[i].getAttribute('data-period');
      if (toRotate) {
        new TxtType(elements[i], toRotate, period);
      }
    }
    // INJECT CSS
    var css = document.createElement("style");
    css.type = "text/css";
    css.innerHTML = ".typewrite > .wrap { border-right: 0.08em solid #fff}";
    document.body.appendChild(css);
  };
</script>
<h2>Registrasi Berhasil</h2>
  <p>Terima kasih, pendaftaran Anda telah berhasil diproses.<br>
  Silakan periksa notifikasi atau pesan Telegram Anda untuk langkah selanjutnya.</p>
    <div class="container my-5">
      <div class="card">
        <div class="card-header text-center text-white bg-danger font-weight-bold" style=" font-size: 10px;"> BERGABUNG
          HARI INI </div>
        <div class="card-body">
          <marquee direction="up" height="300">
            <div class="alert alert-primary" role="alert"> ⏏️ Ami Suartini <br> ⏏️ Status: Successfull ✅ </div>
            <div class="alert alert-primary" role="alert"> ⏏️ Uci Mahendra Arsyad <br> ⏏️ Status: Successfull ✅ </div>
            <div class="alert alert-primary" role="alert"> ⏏️ Eki Nuralam <br> ⏏️ Status: Successfull ✅ </div>
            <div class="alert alert-primary" role="alert"> ⏏️ Dian Lukman <br> ⏏️ Status: Successfull ✅ </div>
            <div class="alert alert-primary" role="alert"> ⏏️ Zenudin <br> ⏏️ Status: Successfull ✅ </div>
            <div class="alert alert-primary" role="alert"> ⏏️ Ahmad Luki Pramoto <br> ⏏️ Status: Successfull ✅ </div>
            <div class="alert alert-primary" role="alert"> ⏏️ Cahyadi <br> ⏏️ Status: Successfull ✅ </div>
            <div class="alert alert-primary" role="alert"> ⏏️ Sugi Anrianto <br> ⏏️ Status: Successfull ✅ </div>
            <div class="alert alert-primary" role="alert"> ⏏️ Darmansya <br> ⏏️ Status: Successfull ✅ </div>
            <div class="alert alert-primary" role="alert"> ⏏️ Budi Ilyas Rahmat <br> ⏏️ Status: Successfull ✅ </div>
            <div class="alert alert-primary" role="alert"> ⏏️ Herawati <br> ⏏️ Status: Successfull ✅ </div>
            <div class="alert alert-primary" role="alert"> ⏏️ Devi Pratawi <br> ⏏️ Status: Successfull ✅ </div>
            <div class="alert alert-primary" role="alert"> ⏏️ Wulan Sri Rahayu <br> ⏏️ Status: Successfull ✅ </div>
            <div class="alert alert-primary" role="alert"> ⏏️ Citra Dwi <br> ⏏️ Status: Successfull ✅ </div>
            <div class="alert alert-primary" role="alert"> ⏏️ Ayu wulandri <br> ⏏️ Status: Successfull ✅ </div>
            <div class="alert alert-primary" role="alert"> ⏏️ Retno <br> ⏏️ Status: Successfull ✅ </div>
            <div class="alert alert-primary" role="alert"> ⏏️ Rahmat <br> ⏏️ Status: Successfull ✅ </div>
            <div class="alert alert-primary" role="alert"> ⏏️ Ari Aryanigrat <br> ⏏️ Status: Successfull ✅ </div>
            <div class="alert alert-primary" role="alert"> ⏏️ Fuji astuti <br> ⏏️ Status: Successfull ✅ </div>
            <div class="alert alert-primary" role="alert"> ⏏️ Taufik <br> ⏏️ Status: Successfull ✅ </div>
            <div class="alert alert-primary" role="alert"> ⏏️ Fery Artanto <br> ⏏️ Status: Successfull ✅ </div>
          </marquee>
        </div>
      </div>
    </div>
  </div>
  <style type="text/css">
    .typewrite>.wrap {
      border-right: 0.08em solid #fff
    }
  </style>
  <script>
    setInterval(function () {
      $('.tests:first-child').remove()
    }, 1500)
  </script>
</body>
</html>