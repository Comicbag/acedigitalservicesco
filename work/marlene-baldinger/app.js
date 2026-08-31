
async function pbPost(col, data, flash){
  try{
    const r = await fetch('pb/api/collections/'+col+'/records',{method:'POST',
      headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
    if(!r.ok) throw new Error(await r.text());
    flash.className='flash ok'; return true;
  }catch(e){ flash.className='flash err'; return false; }
}
function wire(id, col, okMsg){
  const f=document.getElementById(id); if(!f) return;
  f.addEventListener('submit', async ev=>{
    ev.preventDefault();
    const fl=f.querySelector('.flash'); fl.textContent='Sending...'; fl.className='flash ok';
    const data=Object.fromEntries(new FormData(f).entries());
    if(await pbPost(col,data,fl)){ fl.textContent=okMsg; f.reset(); }
    else fl.textContent='Something went wrong sending that. Please try again, or email MarleneforLebanon@gmail.com';
  });
}
wire('askForm','questions','Thank you! Marlene reads every question and answers here on this page.');
wire('signForm','sign_requests','Thank you! Your yard sign request is in.');
wire('joinForm','signups','Thanks for signing up! You are on the list.');
wire('contactForm','messages','Message sent. Marlene will get back to you.');
(async ()=>{
  const box=document.getElementById('answered'); if(!box) return;
  try{
    const r=await fetch('pb/api/collections/questions/records?filter=(answered=true)&sort=-created&perPage=20');
    const j=await r.json();
    if(!j.items||!j.items.length){ box.innerHTML='<p class="note">Questions and answers will appear here as they come in.</p>'; return; }
    box.innerHTML=j.items.map(i=>'<div class="qa"><div class="q">Q: '+esc(i.question)+'</div><div class="a"><strong>Marlene:</strong> '+esc(i.answer)+'</div></div>').join('');
  }catch(e){ box.innerHTML='<p class="note">Questions and answers will appear here as they come in.</p>'; }
})();
document.getElementById('burger')?.addEventListener('click',()=>{
  const m=document.getElementById('menu'); m.classList.toggle('open');
  document.getElementById('burger').setAttribute('aria-expanded', m.classList.contains('open'));
});
(function(){
  const f=document.getElementById('donateForm'); if(!f) return;
  const amt=document.getElementById('damount'), occ=document.getElementById('occBox');
  function sync(){
    const v=parseFloat(amt.value||'0');
    occ.classList.toggle('show', v>300);
    document.querySelectorAll('.amt').forEach(b=>b.classList.toggle('sel', parseFloat(b.dataset.amt)===v));
  }
  document.querySelectorAll('.amt').forEach(b=>b.addEventListener('click',()=>{amt.value=b.dataset.amt;sync();}));
  amt.addEventListener('input', sync);
  f.addEventListener('submit', async ev=>{
    ev.preventDefault();
    const fl=f.querySelector('.flash'); fl.textContent='Sending...'; fl.className='flash ok';
    const d=Object.fromEntries(new FormData(f).entries());
    d.amount=parseFloat(d.amount)||0; d.status='pledged';
    if(d.amount>5500){ fl.className='flash err'; fl.textContent='New Jersey caps an individual contribution at $5,500 per election. Please enter a lower amount.'; return; }
    try{
      const r=await fetch('pb/api/collections/donations/records',{method:'POST',
        headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});
      if(!r.ok) throw new Error(await r.text());
      fl.className='flash ok';
      fl.textContent='Thank you. Marlene will follow up personally about how to send it. No payment has been taken and no card details were collected.';
      f.reset(); sync();
    }catch(e){
      fl.className='flash err';
      fl.textContent='Something went wrong sending that. Please try again, or email MarleneforLebanon@gmail.com';
    }
  });
})();
function esc(s){const d=document.createElement('div');d.textContent=s||'';return d.innerHTML;}
