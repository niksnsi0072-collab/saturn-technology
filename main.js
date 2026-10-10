const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

// Мобильное меню
const menu = document.querySelector('.menu');
const nav = document.querySelector('#navigation');
const setMenu = open => {
  menu.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('open', open);
  menu.querySelector('.menu-label').textContent = open ? 'Закрыть' : 'Меню';
};
menu?.addEventListener('click', () => setMenu(menu.getAttribute('aria-expanded') !== 'true'));
document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') { setMenu(false); menu.focus(); }
});

// Шапка: компактный режим и индикатор прокрутки
const header = document.querySelector('.header');
const parallax = [...document.querySelectorAll('[data-parallax]')];
let ticking = false;
const onScroll = () => {
  const y = scrollY;
  const max = document.documentElement.scrollHeight - innerHeight;
  header.classList.toggle('scrolled', y > 10);
  header.style.setProperty('--p', max > 0 ? (y / max).toFixed(4) : 0);
  if (!reduceMotion) {
    for (const el of parallax) {
      const r = el.getBoundingClientRect();
      if (r.bottom < 0 || r.top > innerHeight) continue;
      const shift = (r.top + r.height / 2 - innerHeight / 2) * -0.08;
      el.style.setProperty('--py', shift.toFixed(1) + 'px');
    }
  }
  ticking = false;
};
addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
onScroll();

// Появление блоков при прокрутке
const io = new IntersectionObserver(entries => {
  for (const entry of entries) {
    if (entry.isIntersecting) { entry.target.classList.add('in'); io.unobserve(entry.target); }
  }
}, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;

// «Магнитные» кнопки слегка тянутся к курсору
if (finePointer && !reduceMotion) {
  document.querySelectorAll('.magnetic').forEach(btn => {
    btn.addEventListener('pointermove', e => {
      const r = btn.getBoundingClientRect();
      const x = (e.clientX - r.left - r.width / 2) * 0.25;
      const y = (e.clientY - r.top - r.height / 2) * 0.35;
      btn.style.transform = `translate(${x}px, ${y}px)`;
    });
    btn.addEventListener('pointerleave', () => { btn.style.transform = ''; });
  });
}

// Линия прогресса вдоль шагов: заполняется по мере прокрутки блока
const progressLists = [...document.querySelectorAll('[data-progress]')];
const updateProgress = () => {
  for (const el of progressLists) {
    const r = el.getBoundingClientRect();
    const k = Math.min(1, Math.max(0, (innerHeight * 0.65 - r.top) / r.height));
    el.style.setProperty('--fill', k.toFixed(3));
  }
};
if (progressLists.length) { addEventListener('scroll', () => requestAnimationFrame(updateProgress), { passive: true }); updateProgress(); }

requestAnimationFrame(() => requestAnimationFrame(() => document.body.classList.add('loaded')));

// Копирование контактов
document.querySelectorAll('[data-copy]').forEach(btn => {
  const label = btn.textContent;
  btn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(btn.dataset.copy);
      btn.textContent = 'Скопировано';
    } catch {
      btn.textContent = 'Не удалось скопировать — выделите вручную';
    }
    btn.classList.add('done');
    setTimeout(() => { btn.textContent = label; btn.classList.remove('done'); }, 2000);
  });
});

// Плавное раскрытие вакансий
document.querySelectorAll('.job').forEach(details => {
  const summary = details.querySelector('summary');
  const content = details.querySelector('.job-content');
  summary.addEventListener('click', e => {
    if (reduceMotion || !content.animate) return;
    e.preventDefault();
    if (details.open) {
      const a = content.animate([{ height: content.offsetHeight + 'px', opacity: 1 }, { height: '0px', opacity: 0 }], { duration: 350, easing: 'cubic-bezier(.2,.7,.2,1)' });
      a.onfinish = () => { details.open = false; };
    } else {
      details.open = true;
      content.animate([{ height: '0px', opacity: 0 }, { height: content.offsetHeight + 'px', opacity: 1 }], { duration: 450, easing: 'cubic-bezier(.2,.7,.2,1)' });
    }
  });
});
