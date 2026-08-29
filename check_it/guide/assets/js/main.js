/* Shiksha Radar — Project Guide JS */
(function () {
  // Mobile sidebar toggle
  const burger = document.getElementById('burger');
  const sidebar = document.getElementById('sidebar');
  const backdrop = document.getElementById('backdrop');
  if (burger && sidebar && backdrop) {
    burger.addEventListener('click', () => {
      sidebar.classList.toggle('open');
      backdrop.classList.toggle('open');
    });
    backdrop.addEventListener('click', () => {
      sidebar.classList.remove('open');
      backdrop.classList.remove('open');
    });
  }

  // Highlight active nav link based on current page
  const current = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.sidebar nav a').forEach(a => {
    const href = a.getAttribute('href');
    if (href === current || (current === '' && href === 'index.html')) {
      a.classList.add('active');
    }
  });

  // Set topbar title from active link
  const tTitle = document.getElementById('tTitle');
  if (tTitle) {
    const active = document.querySelector('.sidebar nav a.active');
    if (active) tTitle.textContent = active.textContent.trim();
  }

  // Reveal-on-scroll animation (respects prefers-reduced-motion)
  const reveal = document.querySelectorAll('.reveal');
  if (reveal.length && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
      });
    }, { threshold: 0.08 });
    reveal.forEach(el => io.observe(el));
  }
})();