<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Awizacje DPH</title>

<!-- jsPDF -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>

<!-- QRCode -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>

<style>
:root{
  --bg:#0b0e14;
  --bg-soft:#11151f;
  --card:#151a26;
  --border:rgba(255,255,255,.08);
  --text:#ffffff;
  --muted:#a0a6b8;
  --accent:#4f7cff;
  --ok:#2ecc71;
  --err:#ff5c5c;
  --shadow:0 10px 30px rgba(0,0,0,.45);
}
*{box-sizing:border-box}
body{
  margin:0;
  min-height:100vh;
  background:var(--bg);
  display:flex;
  align-items:center;
  justify-content:center;
  padding:40px;
  font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
  color:var(--text);
}
.wrapper{
  width:100%;
  max-width:1600px;
  display:grid;
  grid-template-columns:0.9fr 2fr;
  gap:32px;
}
.card{
  background:var(--card);
  border:1px solid var(--border);
  border-radius:18px;
  padding:36px;
  box-shadow:var(--shadow);
}
.field{margin-bottom:22px}
label{display:block;color:var(--muted);margin-bottom:8px}
input,select{
  width:100%;
  background:var(--bg-soft);
  border:1px solid var(--border);
  border-radius:14px;
  padding:18px 20px;
  color:var(--text);
}
button{
  width:100%;
  padding:18px;
  background:transparent;
  color:var(--text);
  border:1px solid var(--accent);
  border-radius:16px;
  cursor:pointer;
}
.status{margin-top:24px;padding:18px;border-radius:14px;display:none}
.status.ok{display:block;background:rgba(46,204,113,.15);color:var(--ok)}
.status.err{display:block;background:rgba(255,92,92,.15);color:var(--err)}
</style>
</head>

<body>

<div class="wrapper">
  <div class="card">
    <div id="infoTitle"></div>
    <ul id="infoList"></ul>
    <img src="image.png" alt="EPAL pallet" style="width:100%">
  </div>

  <div class="card">
    <button onclick="toggleLang()">EN</button>

    <h1 data-i18n="title"></h1>
    <p data-i18n="subtitle"></p>

    <div class="field">
      <label data-i18n="supplier"></label>
      <input id="supplier">
    </div>

    <div class="field">
      <label data-i18n="date"></label>
      <input type="date" id="date">
    </div>

    <div class="field">
      <label data-i18n="hour"></label>
      <select id="hour">
        <option value="">—</option>
        <option>08:00</option>
        <option>08:15</option>
        <option>08:30</option>
      </select>
    </div>

    <div class="field">
      <label data-i18n="pallets"></label>
      <input id="pallets" value="-">
    </div>

    <div class="field">
      <label data-i18n="info"></label>
      <input id="info">
    </div>

    <button onclick="generate()" data-i18n="generate"></button>
    <div class="status" id="status"></div>
  </div>
</div>

<div id="qr" style="display:none"></div>

<script>
let lang="pl";
const statusBox=document.getElementById("status");

const EMAIL_TO="cyprian.m.latka@delpharm.com";
const EMAIL_SUBJECT="Witam uprzejmie, Panie Piotrze. Proszę o zatwierdzenie awizacji.";
const EMAIL_BODY="W załączniku przesyłam awizację dostawy.\n\nPozdrawiam";

const I18N={
  pl:{title:"Awizacje DPH",subtitle:"Stwórz awizację",supplier:"Dostawca",date:"Data",hour:"Godzina",pallets:"Palety",info:"Informacja",generate:"Potwierdź"},
  en:{title:"DPH Notifications",subtitle:"Create notification",supplier:"Supplier",date:"Date",hour:"Time",pallets:"Pallets",info:"Info",generate:"Generate"}
};

function applyLang(){
  document.querySelectorAll("[data-i18n]").forEach(el=>{
    el.textContent=I18N[lang][el.dataset.i18n];
  });
}
function toggleLang(){lang=lang==="pl"?"en":"pl";applyLang();}
applyLang();

function show(type,msg){
  statusBox.className="status "+type;
  statusBox.textContent=msg;
}

function sanitizeSupplier(v){
  return v.toUpperCase().replace(/\s+/g,"_").replace(/[^A-Z0-9_]/g,"");
}

async function generate(){
  const qr=document.getElementById("qr");
  qr.innerHTML="";
  new QRCode(qr,{text:"TEST",width:200,height:200});
  await new Promise(requestAnimationFrame);
  const canvas=qr.querySelector("canvas");
  const qrImg=canvas.toDataURL("image/png");

  const {jsPDF}=window.jspdf;
  const pdf=new jsPDF();
  pdf.text("AWIZACJA DOSTAWY",20,20);
  pdf.addImage(qrImg,"PNG",60,60,90,90);

  const safeSupplier=sanitizeSupplier(supplier.value);
  pdf.save(`awizacja_delpharm_${safeSupplier}.pdf`);

  const mailto=
    "mailto:"+encodeURIComponent(EMAIL_TO)+
    "?subject="+encodeURIComponent(EMAIL_SUBJECT)+
    "&body="+encodeURIComponent(EMAIL_BODY);

  window.location.href=mailto;
  show("ok","✓ PDF pobrany i otwarto e‑mail");
}
</script>

</body>
</html>
