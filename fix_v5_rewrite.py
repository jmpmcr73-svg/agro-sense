#!/usr/bin/env python3
# fix_v5_rewrite.py — Reescritura completa del JS de index.html
# Uso: python3 fix_v5_rewrite.py

import re, sys

with open('index.html','r',encoding='utf-8') as f:
    h = f.read()
print(f'Original: {len(h)} chars')

# ── PASO 1: Eliminar el bloque Akasha roto ──
markers = ['// ── AKASHA CHAT & VOICE','// ── AKASHA v4','// ── AKASHA v3','async function greetVoice']
start = -1
for m in markers:
    idx = h.find(m)
    if idx > -1:
        start = idx
        print(f'✅ Bloque Akasha encontrado en char {idx}')
        break

script_end = h.rfind('</script>')
if start > -1 and script_end > -1:
    h = h[:start] + h[script_end:]
    print(f'✅ Bloque roto eliminado')
else:
    print('ℹ️  No se encontró bloque Akasha o </script>')

# ── PASO 2: Fix doLogin — siempre limpio ──
# Remove any existing broken doLogin patches
h = h.replace(
    'if(ok){curUserName=uRole==="admin"?"Juan Pablo":"Carlos";document.getElementById("s-login").classList.remove("active");document.getElementById("s-app").classList.add("active");aAudit(curUserName,"login","Sistema","AGROSENSe Pro");initApp();setTimeout(function(){greetVoice(curUserName);},900);loadQuickPrompts();loadSystemStatus();}',
    'if(ok){curUserName=uRole==="admin"?"Juan Pablo":"Carlos";document.getElementById("s-login").classList.remove("active");document.getElementById("s-app").classList.add("active");aAudit(curUserName,"login","Sistema","AGROSENSe Pro");initApp();setTimeout(function(){if(typeof greetVoice==="function")greetVoice(curUserName);},900);}'
)
# Also patch original doLogin if not yet patched
if 'curUserName=uRole' not in h:
    h = h.replace(
        'if(ok){document.getElementById("s-login").classList.remove("active");document.getElementById("s-app").classList.add("active");aAudit(uRole==="admin"?"Juan Pablo":"Carlos","login","Sistema","AGROSENSe Pro");initApp();}',
        'if(ok){curUserName=uRole==="admin"?"Juan Pablo":"Carlos";document.getElementById("s-login").classList.remove("active");document.getElementById("s-app").classList.add("active");aAudit(curUserName,"login","Sistema","AGROSENSe Pro");initApp();}'
    )
print('✅ doLogin actualizado')

# ── PASO 3: Agregar CFG si no existe ──
SUPA  = 'https://crfghwtfqaplzsmwylxe.supabase.co'
AKEY  = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNyZmdod3RmcWFwbHpzbXd5bHhlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzUzMjc1MjksImV4cCI6MjA5MDkwMzUyOX0.WUNkTqU93H92nohb_Idqhu8nV1JblFvVRk6Lf_PJw64'
if 'var CFG=' not in h:
    cfg = (
        "var CFG={supa:'" + SUPA + "',anonKey:'" + AKEY + "',"
        "voiceId:'21m00Tcm4TlvDq8ikWAM',"
        "actionsUrl:'" + SUPA + "/functions/v1/akasha-actions',"
        "chatUrl:'" + SUPA + "/functions/v1/akasha-chat',"
        "voiceUrl:'" + SUPA + "/functions/v1/akasha-voice'};\n"
        "var chatHist=[];var curUserName='';var _sessionId='sess_'+Math.random().toString(36).substr(2,9)+'_'+Date.now();\n"
    )
    h = h.replace('var VRS={', cfg + 'var VRS={', 1)
    print('✅ CFG agregado')
else:
    print('ℹ️  CFG ya existe')
    if 'var chatHist' not in h:
        h = h.replace('var VRS={', "var chatHist=[];var curUserName='';var _sessionId='sess_'+Math.random().toString(36).substr(2,9)+'_'+Date.now();\nvar VRS={", 1)

# ── PASO 4: Insertar funciones Akasha LIMPIAS ──
# Written as Python string concatenation — NO template literal issues possible
AKASHA = '\n'.join([
'// ── AKASHA v5 LIMPIO ──',
'async function greetVoice(name){',
"  var vc=document.getElementById('voz-toggle');",
"  if(vc&&!vc.checked)return;",
"  var txt='\\u00a1Hola '+name+'! Soy Akasha, tu asistente de iAGRI.';",
'  try{',
"    var r=await fetch(CFG.voiceUrl,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:txt,voice_id:CFG.voiceId})});",
"    if(r.ok){var blob=await r.blob();new Audio(URL.createObjectURL(blob)).play();}",
"  }catch(e){console.log('Voice:',e);}",
'}',
'async function loadSystemStatus(){',
'  try{',
"    var r=await fetch(CFG.actionsUrl,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:'get_system_status',tenant_id:'hidroexpo'})});",
'    var d=await r.json();',
"    var dot=document.getElementById('sem-dot');",
"    var lbl=document.getElementById('sem-lbl');",
"    if(!dot||!lbl)return;",
"    var sem=d.semaforo||'verde';",
"    dot.className='semaforo sem-'+sem;",
"    lbl.textContent=(sem==='verde'?'\\u2705':sem==='amarillo'?'\\u26a0\\ufe0f':'\\ud83d\\udd34')+' '+(d.alertas_activas||0)+' alertas';",
"  }catch(e){}",
'}',
'async function loadQuickPrompts(){',
'  try{',
"    var r=await fetch(CFG.actionsUrl+'?action=get_quick_prompts&org_id=hidroexpo');",
'    var d=await r.json();',
"    if(!d.prompts||!d.prompts.length)return;",
"    var panel=document.getElementById('qpanel');",
"    if(!panel)return;",
"    panel.innerHTML=d.prompts.slice(0,6).map(function(p){return '<button class=\"qbtn\" onclick=\"quickAsk('+JSON.stringify(p.prompt)+')\">'+(p.emoji||'\\ud83d\\udcac')+' '+p.label+'</button>';}).join('');",
"  }catch(e){}",
'}',
'function getStatsCtx(){',
'  try{',
"    var ms=gM(curSlot,'1.2');",
'    function ga(vk){return avg(ms.map(function(m){return m[vk]||0;})).toFixed(2);}',
"    var alts=ALERTS_D.filter(function(a){return!a.ok;}).map(function(a){return a.msg;}).slice(0,3).join('; ');",
"    return 'Temp='+ga('temp_aire')+'C Hum='+ga('hum_aire')+'% CO2='+ga('co2_ppm')+'ppm'+(alts?' Alertas:'+alts:'');",
"  }catch(e){return '';}",
'}',
'async function sendChat(){',
"  var inp=document.getElementById('chat-input');",
"  var btn=document.getElementById('chat-send-btn');",
"  var msg=inp.value.trim();if(!msg)return;",
"  inp.value='';if(btn)btn.disabled=true;",
"  addChatMsg(msg,'user');showTyping();",
'  var t0=Date.now();',
'  try{',
"    var r=await fetch(CFG.chatUrl,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg,user_name:curUserName,user_role:uRole,stats_context:getStatsCtx(),history:chatHist.slice(-8),tenant_id:'hidroexpo',session_id:_sessionId})});",
'    var d=await r.json();',
'    hideTyping();',
"    var reply=d.reply||'Sin respuesta.';",
'    if(d.correlData&&d.correlData.pares&&d.correlData.pares.length>0){',
"      var ct='\\n\\n\\ud83d\\udcca Correlaciones:\\n';",
"      d.correlData.pares.slice(0,4).forEach(function(p){if(p.correlacion!=null)ct+='\\u2022 '+p.variable_x+' \\u2192 '+p.variable_y+': r='+p.correlacion+' ('+p.fuerza+')\\n';});",
'      reply+=ct;',
'    }',
'    var elapsed=Date.now()-t0;',
"    addChatMsg(reply,'akasha',elapsed,d.model);",
"    chatHist.push({role:'user',content:msg});",
"    chatHist.push({role:'assistant',content:reply});",
"    aAudit(curUserName,'chat_akasha','\\ud83d\\udcac Chat',msg.substring(0,40));",
"    var vt=document.getElementById('voz-toggle');",
'    if(vt&&vt.checked){',
'      try{',
"        var cleanReply=reply.split('').filter(function(c){var cc=c.charCodeAt(0);return cc<55296||cc>57343;}).join('').replace(/[\\r\\n]+/g,' ').substring(0,300);",
"        var vr=await fetch(CFG.voiceUrl,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:cleanReply,voice_id:CFG.voiceId})});",
"        if(vr.ok){var vb=await vr.blob();new Audio(URL.createObjectURL(vb)).play();}",
"      }catch(ve){}",
'    }',
"    if(typeof loadSystemStatus==='function')loadSystemStatus();",
"  }catch(e){hideTyping();addChatMsg('\\u26a0\\ufe0f Error: '+e.message,'akasha');}",
"  finally{if(btn)btn.disabled=false;inp.focus();}",
'}',
'function quickAsk(msg){',
"  document.getElementById('chat-input').value=msg;sendChat();",
"  var p=document.getElementById('agent-panel');",
"  if(p&&!p.classList.contains('open'))togglePanel('agent-panel');",
'}',
'function addChatMsg(txt,who,ms,model){',
"  var area=document.getElementById('chat-msgs');if(!area)return;",
"  var wrap=document.createElement('div');",
"  wrap.style.cssText='display:flex;flex-direction:column;'+(who==='user'?'align-items:flex-end':'');",
"  var d=document.createElement('div');",
"  d.className=who==='user'?'chat-bbl-u':'chat-bbl-a';",
"  var esc=txt.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');",
"  var lines=esc.split('\\n');d.innerHTML=lines.join('<br/>');",
'  wrap.appendChild(d);',
"  if(who==='akasha'&&ms){",
"    var meta=document.createElement('div');meta.className='chat-meta';",
"    meta.textContent=(model||'akasha')+' \\u00b7 '+ms+'ms';",
'    wrap.appendChild(meta);',
'  }',
'  area.appendChild(wrap);area.scrollTop=area.scrollHeight;',
'}',
'function showTyping(){',
"  var area=document.getElementById('chat-msgs');if(!area)return;",
"  var d=document.createElement('div');d.id='typing-ind';",
'  d.innerHTML=\'<div style="display:flex;align-items:center;gap:3px;padding:8px 12px;background:#f8fafc;border-radius:12px;border:1px solid var(--border)"><span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span></div>\';',
'  area.appendChild(d);area.scrollTop=area.scrollHeight;',
'}',
"function hideTyping(){var t=document.getElementById('typing-ind');if(t)t.remove();}",
'function toggleVoiceInput(){',
"  var btn=document.getElementById('voz-mic');",
"  var lbl=document.getElementById('stt-lbl');",
'  var SR=window.SpeechRecognition||window.webkitSpeechRecognition;',
"  if(!SR){alert('Requiere Chrome o Edge.');return;}",
"  if(btn.classList.contains('active')){",
'    if(window._aRec)window._aRec.stop();',
"    btn.classList.remove('active');btn.textContent='\\ud83c\\udfa4';",
"    if(lbl)lbl.classList.remove('vis');return;",
'  }',
'  window._aRec=new SR();',
"  window._aRec.lang='es-ES';",
'  window._aRec.continuous=false;',
'  window._aRec.interimResults=false;',
'  window._aRec.onresult=function(e){',
'    var t=e.results[0][0].transcript;',
"    document.getElementById('chat-input').value=t;",
"    btn.classList.remove('active');btn.textContent='\\ud83c\\udfa4';",
"    if(lbl)lbl.classList.remove('vis');sendChat();",
'  };',
"  window._aRec.onend=function(){btn.classList.remove('active');btn.textContent='\\ud83c\\udfa4';if(lbl)lbl.classList.remove('vis');};",
"  window._aRec.onerror=function(){btn.classList.remove('active');btn.textContent='\\ud83c\\udfa4';if(lbl)lbl.classList.remove('vis');};",
"  window._aRec.start();btn.classList.add('active');btn.textContent='\\u23f9';if(lbl)lbl.classList.add('vis');",
'}',
])

# Insert before last </script>
last_script = h.rfind('</script>')
if last_script > -1:
    h = h[:last_script] + '\n' + AKASHA + '\n' + h[last_script:]
    print('✅ Funciones Akasha v5 insertadas')
else:
    print('❌ No se encontró </script>')

with open('index.html','w',encoding='utf-8') as f:
    f.write(h)
print(f'\n🎉 ¡Listo! index.html: {len(h)} chars')
print('📌 git add index.html && git commit -m "v5: JS reescrito limpio" && git push')
