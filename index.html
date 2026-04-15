// fix_index.mjs — Corre con: node fix_index.mjs
// Restaura index.html con Chat Akasha + Voz integrados
// Requiere: node 18+ (fetch nativo)

import { writeFileSync } from 'fs';

const SUPABASE_URL = "https://crfghwtfqaplzsmwylxe.supabase.co";
const ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNyZmdod3RmcWFwbHpzbXd5bHhlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzUzMjc1MjksImV4cCI6MjA5MDkwMzUyOX0.WUNkTqU93H92nohb_Idqhu8nV1JblFvVRk6Lf_PJw64";
const ORIGINAL_URL = "https://agro-sense-f3ls-anenp1qzo-jmpmcr73-3169s-projects.vercel.app";

console.log("📥 Descargando HTML original desde Vercel...");
const res = await fetch(ORIGINAL_URL);
let html = await res.text();
console.log(`✅ Original obtenido: ${html.length} caracteres`);

// ── 1. CSS del chat ──────────────────────────────────────
const chatCSS = `.chat-bbl-u{background:#dcfce7;border-radius:12px 12px 4px 12px;padding:8px 12px;font-size:12px;max-width:82%;color:#15803d;word-break:break-word}
.chat-bbl-a{background:#f8fafc;border-radius:12px 12px 12px 4px;padding:8px 12px;font-size:12px;max-width:85%;border:1px solid var(--border);color:var(--text);word-break:break-word}
.typing-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--green2);animation:pulse 1.2s infinite;margin:0 2px}
.typing-dot:nth-child(2){animation-delay:.2s}.typing-dot:nth-child(3){animation-delay:.4s}
.chat-send-btn{flex-shrink:0;border:none;background:var(--green);color:#fff;padding:7px 13px;border-radius:8px;font-size:13px;font-weight:600;cursor:pointer}
.chat-mic-btn{flex-shrink:0;border:1.5px solid var(--border);background:#fff;padding:7px 10px;border-radius:8px;font-size:13px;cursor:pointer}
.chat-mic-btn.active{background:var(--redl);border-color:var(--redb)}`;

const CSS_MARKER = '.bcs{display:flex;align-items:center;gap:5px;flex-wrap:wrap}';
if (html.includes(CSS_MARKER)) {
  html = html.replace(CSS_MARKER, CSS_MARKER + '\n' + chatCSS);
  console.log("✅ Cambio 1: CSS del chat añadido");
} else { console.warn("⚠️  CSS marker no encontrado"); }

// ── 2. Agent panel con chat ───────────────────────────────
const OLD_PANEL = `  <div style="padding:14px">
    <div style="font-size:12px;font-weight:700;color:var(--green);margin-bottom:10px">Resumen del Sistema</div>
    <div id="ag-st" style="display:flex;flex-direction:column;gap:6px"></div>
    <div style="margin-top:14px;border-top:1px solid var(--border);padding-top:12px">
      <div style="font-size:11px;font-weight:600;color:var(--text2);margin-bottom:8px">Módulos iAGRI</div>
      <div style="display:flex;flex-direction:column;gap:5px">
        <div class="badge bok" style="justify-content:flex-start;padding:6px 10px">✅ AGROSENSe · Activo</div>
        <div class="badge bin" style="justify-content:flex-start;padding:6px 10px">🔄 NOC Local · Sync OK</div>
        <div class="badge bok" style="justify-content:flex-start;padding:6px 10px">✅ Supabase iAGRI · Conectado</div>
        <div class="badge bwn" style="justify-content:flex-start;padding:6px 10px">⏳ WhatsApp · Pendiente</div>
        <div class="badge bwn" style="justify-content:flex-start;padding:6px 10px">⏳ App Stores · Pendiente</div>
      </div>
    </div>
  </div>
</div>`;

const NEW_PANEL = `  <div style="padding:10px 14px">
    <div style="font-size:12px;font-weight:700;color:var(--green);margin-bottom:8px">Resumen del Sistema</div>
    <div id="ag-st" style="display:flex;flex-direction:column;gap:5px"></div>
    <div style="margin-top:10px;border-top:1px solid var(--border);padding-top:8px">
      <div style="display:flex;flex-wrap:wrap;gap:4px">
        <div class="badge bok" style="padding:4px 8px">✅ AGROSENSe</div>
        <div class="badge bin" style="padding:4px 8px">🔄 NOC OK</div>
        <div class="badge bok" style="padding:4px 8px">✅ Supabase</div>
        <div class="badge bok" style="padding:4px 8px">✅ WhatsApp</div>
      </div>
    </div>
  </div>
  <div style="border-top:1.5px solid var(--border);display:flex;flex-direction:column">
    <div style="padding:10px 14px 6px;display:flex;align-items:center;justify-content:space-between">
      <div style="font-size:12px;font-weight:700;color:var(--green)">💬 Chat con Akasha</div>
      <div style="display:flex;align-items:center;gap:5px">
        <span style="font-size:10px;color:var(--text2)">🔊 Voz</span>
        <input type="checkbox" id="voz-toggle" style="width:auto;padding:0" title="Respuesta por voz"/>
      </div>
    </div>
    <div id="chat-msgs" style="overflow-y:auto;padding:0 10px 8px;display:flex;flex-direction:column;gap:8px;min-height:180px;max-height:320px">
      <div style="display:flex"><div class="chat-bbl-a">👋 ¡Hola! Soy Akasha. Analizo datos IoT en tiempo real, correlaciones, alertas y consultas agronómicas. ¿En qué te ayudo?</div></div>
    </div>
    <div style="padding:8px 10px;border-top:1px solid var(--border);background:#fafcfa">
      <div style="display:flex;gap:6px">
        <input id="chat-input" type="text" placeholder="Pregunta a Akasha..." style="flex:1;font-size:12px;padding:7px 10px" onkeydown="if(event.key==='Enter')sendChat()"/>
        <button class="chat-send-btn" onclick="sendChat()">→</button>
        <button class="chat-mic-btn" id="voz-mic" onclick="toggleVoiceInput()" title="Voz">🎤</button>
      </div>
      <div style="display:flex;gap:5px;margin-top:6px;flex-wrap:wrap">
        <button onclick="quickAsk('¿Qué alertas activas hay ahora?')" style="font-size:9px;padding:3px 7px;border-radius:5px;border:1px solid var(--border);background:#fff;cursor:pointer;color:var(--text2)">⚠️ Alertas</button>
        <button onclick="quickAsk('Analiza correlación entre temperatura y etileno')" style="font-size:9px;padding:3px 7px;border-radius:5px;border:1px solid var(--border);background:#fff;cursor:pointer;color:var(--text2)">📊 Temp-Etileno</button>
        <button onclick="quickAsk('¿Cómo están los KPIs hoy?')" style="font-size:9px;padding:3px 7px;border-radius:5px;border:1px solid var(--border);background:#fff;cursor:pointer;color:var(--text2)">📈 KPIs</button>
        <button onclick="quickAsk('Analiza correlación entre temperatura humedad co2 metano etileno')" style="font-size:9px;padding:3px 7px;border-radius:5px;border:1px solid var(--border);background:#fff;cursor:pointer;color:var(--text2)">🧪 Multi-corr</button>
      </div>
    </div>
  </div>
</div>`;

if (html.includes(OLD_PANEL)) {
  html = html.replace(OLD_PANEL, NEW_PANEL);
  console.log("✅ Cambio 2: Panel de chat añadido");
} else { console.warn("⚠️  Panel marker no encontrado — verifica el HTML original"); }

// ── 3. Config vars ────────────────────────────────────────
const CFG = `var CFG={supa:'${SUPABASE_URL}',anonKey:'${ANON_KEY}',voiceId:'21m00Tcm4TlvDq8ikWAM'};
var chatHist=[];var curUserName='';
`;
if (html.includes('var VRS={')) {
  html = html.replace('var VRS={', CFG + 'var VRS={');
  console.log("✅ Cambio 3: Config añadida");
} else { console.warn("⚠️  var VRS no encontrado"); }

// ── 4. doLogin con voz ────────────────────────────────────
const OLD_LOGIN = 'if(ok){document.getElementById("s-login").classList.remove("active");document.getElementById("s-app").classList.add("active");aAudit(uRole==="admin"?"Juan Pablo":"Carlos","login","Sistema","AGROSENSe Pro");initApp();}';
const NEW_LOGIN = 'if(ok){curUserName=uRole==="admin"?"Juan Pablo":"Carlos";document.getElementById("s-login").classList.remove("active");document.getElementById("s-app").classList.add("active");aAudit(curUserName,"login","Sistema","AGROSENSe Pro");initApp();setTimeout(function(){greetVoice(curUserName);},900);}';
if (html.includes(OLD_LOGIN)) {
  html = html.replace(OLD_LOGIN, NEW_LOGIN);
  console.log("✅ Cambio 4: doLogin modificado con voz");
} else { console.warn("⚠️  doLogin pattern no encontrado"); }

// ── 5. Nuevas funciones ───────────────────────────────────
const NEW_FUNS = `
async function greetVoice(name){var txt='¡Hola '+name+'! Bienvenido a iAgri AGROSENSe Pro. Soy Akasha, tu asistente agrícola inteligente. ¿En qué puedo ayudarte hoy?';try{var r=await fetch(CFG.supa+'/functions/v1/akasha-voice',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:txt,voice_id:CFG.voiceId})});if(r.ok){var blob=await r.blob();new Audio(URL.createObjectURL(blob)).play();}}catch(e){console.log('Voice:',e);}}
function getStatsCtx(){try{var ms=gM(curSlot,'1.2');function ga(vk){return avg(ms.map(function(m){return m[vk]||0;})).toFixed(2);}var alts=ALERTS_D.filter(function(a){return!a.ok;}).map(function(a){return a.msg;}).slice(0,3).join('; ');return 'Estructura:'+curSt.n+' Cultivo:'+curSt.cult+' Sem:'+curSt.sem+' Temp='+ga('temp_aire')+'C Hum='+ga('hum_aire')+'% CO2='+ga('co2_ppm')+'ppm CH4='+ga('ch4_ppm')+'ppm Etileno='+ga('etileno_ppm')+'ppm HumSust='+ga('hum_sustrato')+'% CE='+ga('ce_sustrato')+'mS/cm'+(alts?' Alertas:'+alts:'');}catch(e){return '';}}
async function sendChat(){var inp=document.getElementById('chat-input');var msg=inp.value.trim();if(!msg)return;inp.value='';addChatMsg(msg,'user');showTyping();try{var r=await fetch(CFG.supa+'/functions/v1/akasha-chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg,user_name:curUserName,user_role:uRole,stats_context:getStatsCtx(),history:chatHist.slice(-8)})});var d=await r.json();hideTyping();var reply=d.reply||'Sin respuesta.';if(d.correlData&&d.correlData.pares&&d.correlData.pares.length>0){var ct='\\n\\n📊 Correlaciones:\\n';d.correlData.pares.slice(0,4).forEach(function(p){if(p.correlacion!=null)ct+='• '+p.variable_x+' ↔ '+p.variable_y+': r='+p.correlacion+' ('+p.fuerza+')\\n';});reply+=ct;}addChatMsg(reply,'akasha');chatHist.push({role:'user',content:msg});chatHist.push({role:'assistant',content:reply});aAudit(curUserName,'chat_akasha','💬 Chat',msg.substring(0,40));var vt=document.getElementById('voz-toggle');if(vt&&vt.checked){try{var vr=await fetch(CFG.supa+'/functions/v1/akasha-voice',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:reply.replace(/[\\n📊🌱🌿⚠️✅🧪💬👋]/g,' ').substring(0,200),voice_id:CFG.voiceId})});if(vr.ok){var vb=await vr.blob();new Audio(URL.createObjectURL(vb)).play();}}catch(ve){}}}catch(e){hideTyping();addChatMsg('⚠️ Error: '+e.message,'akasha');}}
function quickAsk(msg){document.getElementById('chat-input').value=msg;sendChat();var p=document.getElementById('agent-panel');if(!p.classList.contains('open'))togglePanel('agent-panel');}
function addChatMsg(txt,who){var area=document.getElementById('chat-msgs');if(!area)return;var d=document.createElement('div');d.style.cssText='display:flex;'+(who==='user'?'justify-content:flex-end':'');var esc=txt.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\\n/g,'<br/>');d.innerHTML='<div class="'+(who==='user'?'chat-bbl-u':'chat-bbl-a')+'">'+esc+'</div>';area.appendChild(d);area.scrollTop=area.scrollHeight;}
function showTyping(){var area=document.getElementById('chat-msgs');if(!area)return;var d=document.createElement('div');d.id='typing-ind';d.innerHTML='<div style="display:flex;align-items:center;gap:3px;padding:8px 12px;background:#f8fafc;border-radius:12px 12px 12px 4px;border:1px solid var(--border)"><span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span></div>';area.appendChild(d);area.scrollTop=area.scrollHeight;}
function hideTyping(){var t=document.getElementById('typing-ind');if(t)t.remove();}
function toggleVoiceInput(){var btn=document.getElementById('voz-mic');if(!window.SpeechRecognition&&!window.webkitSpeechRecognition){alert('Requiere Chrome o Edge.');return;}if(btn.classList.contains('active')){if(window._aRec)window._aRec.stop();btn.classList.remove('active');btn.textContent='🎤';return;}var SR=window.SpeechRecognition||window.webkitSpeechRecognition;window._aRec=new SR();window._aRec.lang='es-ES';window._aRec.continuous=false;window._aRec.interimResults=false;window._aRec.onresult=function(e){document.getElementById('chat-input').value=e.results[0][0].transcript;btn.classList.remove('active');btn.textContent='🎤';sendChat();};window._aRec.onend=function(){btn.classList.remove('active');btn.textContent='🎤';};window._aRec.start();btn.classList.add('active');btn.textContent='⏹';}
`;

// Insert before the last </script>
const lastScript = html.lastIndexOf('</script>');
if (lastScript !== -1) {
  html = html.slice(0, lastScript) + NEW_FUNS + html.slice(lastScript);
  console.log("✅ Cambio 5: Funciones de chat y voz añadidas");
} else { console.warn("⚠️  </script> no encontrado"); }

// ── Guardar resultado ─────────────────────────────────────
writeFileSync('index.html', html, 'utf-8');
console.log(`\n🎉 ¡Listo! index.html generado: ${html.length} caracteres`);
console.log("📤 Próximo paso: git add index.html && git commit -m 'Add Akasha chat + voice' && git push");
