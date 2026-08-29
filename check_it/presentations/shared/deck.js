// Shared slide-deck navigation for Shiksha Radar presentations
(function () {
  const slides = Array.from(document.querySelectorAll('.slide'));
  if (!slides.length) return;
  const counter = document.getElementById('counter');
  const progress = document.getElementById('progress');
  const menu = document.getElementById('menu');
  const menuLinks = document.getElementById('menuLinks');
  let current = 0;

  // Build menu links from slides
  slides.forEach((s, i) => {
    const kick = s.querySelector('.kicker');
    const h = s.querySelector('h1, h2');
    const label = (kick ? kick.textContent + ' — ' : '') + (h ? h.textContent.trim() : ('Slide ' + (i + 1)));
    const a = document.createElement('a');
    a.href = '#';
    a.textContent = (i + 1) + '. ' + label;
    a.addEventListener('click', e => { e.preventDefault(); show(i); closeMenu(); });
    menuLinks.appendChild(a);
  });

  function show(i) {
    current = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach((s, idx) => s.classList.toggle('active', idx === current));
    counter.textContent = (current + 1) + ' / ' + slides.length;
    progress.style.width = ((current + 1) / slides.length * 100) + '%';
    slides[current].scrollTop = 0;
  }
  function next() { show(current + 1); }
  function prev() { show(current - 1); }
  function openMenu() { menu.classList.add('open'); }
  function closeMenu() { menu.classList.remove('open'); }

  document.getElementById('nextBtn').addEventListener('click', next);
  document.getElementById('prevBtn').addEventListener('click', prev);
  document.getElementById('menuBtn').addEventListener('click', openMenu);
  document.getElementById('closeBtn').addEventListener('click', closeMenu);
  menu.addEventListener('click', e => { if (e.target === menu) closeMenu(); });

  document.addEventListener('keydown', e => {
    if (menu.classList.contains('open')) { if (e.key === 'Escape') closeMenu(); return; }
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { e.preventDefault(); next(); }
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); prev(); }
    else if (e.key === 'Home') { show(0); }
    else if (e.key === 'End') { show(slides.length - 1); }
  });

  let touchX = 0;
  document.addEventListener('touchstart', e => { touchX = e.touches[0].clientX; });
  document.addEventListener('touchend', e => {
    const dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 60) { dx < 0 ? next() : prev(); }
  });

  show(0);
})();