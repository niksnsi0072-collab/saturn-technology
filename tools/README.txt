Сборка страниц сайта

Все шесть HTML-страниц (index, develop, asutp, supply, vacancy, contacts)
генерируются скриптом build.py. Править тексты и разметку нужно в build.py,
а не в HTML-файлах напрямую — иначе изменения пропадут при следующей сборке.

Запуск (из папки saturn-technology):
    python tools/build.py

old-site-text.txt — тексты со старого сайта saturntechnology.ru,
из него берутся полные описания вакансий.

Стили — style.css, скрипты — main.js (их правят напрямую).
