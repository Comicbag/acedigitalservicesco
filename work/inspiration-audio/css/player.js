/* IA playlist player. One <audio>, a track list, keyboard + seek + prev/next.
   Files are served from the RMC PocketBase pb_public folder (same box, CORS + Range on). */
(function(){
  var root=document.getElementById('player'); if(!root) return;
  var tracks=[].slice.call(root.querySelectorAll('.track'));
  var audio=new Audio(); audio.preload='none';
  var base=root.getAttribute('data-base')||'';
  var cur=-1, seeking=false;
  var $=function(s){return root.querySelector(s)};
  var btnPlay=$('.np-play'), btnPrev=$('.np-prev'), btnNext=$('.np-next'),
      seek=$('.np-seek'), tCur=$('.np-cur'), tDur=$('.np-dur'), npT=$('.np-title'), npA=$('.np-artist'), np=$('.np');
  function fmt(s){ if(!isFinite(s)) return '0:00'; s=Math.floor(s); return Math.floor(s/60)+':'+('0'+s%60).slice(-2); }
  function load(i,play){
    if(i<0||i>=tracks.length) return;
    if(i!==cur){
      cur=i; var t=tracks[i];
      audio.src=base+t.getAttribute('data-file');
      npT.textContent=t.querySelector('.tt').textContent;
      npA.textContent=t.querySelector('.ta').textContent;
      tDur.textContent=t.querySelector('.td').textContent;
      tracks.forEach(function(x,k){ x.classList.toggle('on',k===i); x.querySelector('button').setAttribute('aria-pressed',k===i?'true':'false'); });
      seek.value=0; tCur.textContent='0:00';
    }
    if(play){ audio.play().catch(function(){}); }
  }
  function toggle(){ if(cur<0){ load(0,true); return; } audio.paused?audio.play():audio.pause(); }
  tracks.forEach(function(t,i){ t.querySelector('button').addEventListener('click',function(){ (i===cur)?toggle():load(i,true); }); });
  btnPlay.addEventListener('click',toggle);
  btnPrev.addEventListener('click',function(){ if(audio.currentTime>3){audio.currentTime=0;return;} load((cur-1+tracks.length)%tracks.length,true); });
  btnNext.addEventListener('click',function(){ load((cur+1)%tracks.length,true); });
  audio.addEventListener('play',function(){ root.classList.add('playing'); btnPlay.setAttribute('aria-label','Pause'); });
  audio.addEventListener('pause',function(){ root.classList.remove('playing'); btnPlay.setAttribute('aria-label','Play'); });
  audio.addEventListener('ended',function(){ load((cur+1)%tracks.length, cur<tracks.length-1); });
  audio.addEventListener('loadedmetadata',function(){ tDur.textContent=fmt(audio.duration); });
  audio.addEventListener('timeupdate',function(){ if(seeking||!audio.duration) return; seek.value=Math.round(audio.currentTime/audio.duration*1000); tCur.textContent=fmt(audio.currentTime); });
  audio.addEventListener('error',function(){ npA.textContent='This track could not be loaded.'; });
  seek.addEventListener('input',function(){ seeking=true; tCur.textContent=fmt(seek.value/1000*(audio.duration||0)); });
  seek.addEventListener('change',function(){ if(audio.duration) audio.currentTime=seek.value/1000*audio.duration; seeking=false; });
  document.addEventListener('keydown',function(e){
    if(e.target.matches('input,textarea,select,[contenteditable]')) return;
    if(e.code==='Space'&&cur>=0){ e.preventDefault(); toggle(); }
  });
  if('mediaSession' in navigator){
    navigator.mediaSession.setActionHandler('previoustrack',function(){btnPrev.click()});
    navigator.mediaSession.setActionHandler('nexttrack',function(){btnNext.click()});
  }
})();
