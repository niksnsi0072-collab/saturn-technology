"""Сборка сайта. Все тексты — дословно со старого сайта saturntechnology.ru (без коррекции)."""
import os, re, sys

# Запуск из папки сайта: python tools/build.py
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
OLD = open(os.path.join(HERE, 'old-site-text.txt'), encoding='utf-8').read()

# Меню — как на старом сайте
NAV = [
    ('develop.html', 'Тренажер оператора'),
    ('supply.html', 'Поставка МТР'),
    ('asutp.html', 'АСУ ТП'),
    ('vacancy.html', 'Вакансии'),
    ('contacts.html', 'Контакты'),
]

LOGO = '<img class="logo" src="assets/logo.png" alt="Сатурн Технолоджи" width="1095" height="188">'
LOGO_LIGHT = '<img class="logo" src="assets/logo-light.png" alt="Сатурн Технолоджи" width="1095" height="188">'
ADDRESS = 'г. Москва, вн.тер.г. муниципальный округ Котловка, ул. Большая Черёмушкинская, д. 13, стр. 1'
EMAIL = 'info@saturn-tek.ru'
PHONE = '+7 (495) 120-88-18'
PHONE_HREF = 'tel:+74951208818'


ICONS = {'home': '<path d="M4 11l8-7 8 7v9h-5v-6H9v6H4z"/>', 'phone': '<path d="M6 3h4l2 5-2.5 1.5a11 11 0 0 0 5 5L16 12l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 4 5a2 2 0 0 1 2-2"/>', 'mail': '<path d="M3 6h18v12H3z M3 7l9 6 9-6"/>', 'pin': '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z M12 12.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5"/>', 'arrow': '<path d="M7 17L17 7 M9 7h8v8"/>'}


def icon(name):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


CIRCLE = f'<span class="circle-arrow" aria-hidden="true">{icon("arrow")}</span>'
MAP_URL = 'https://yandex.ru/maps/?text=Москва%20Большая%20Черёмушкинская%2013%20строение%201'


def page(fname, title, body, extra_class=''):
    nav = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h == fname else ""}>{t}</a>' for h, t in NAV)
    fnav = ''.join(f'<a href="{h}">{t}</a>' for h, t in NAV)
    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#f3f2ef">
<title>{title}</title>
<link rel="icon" type="image/png" href="assets/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<script>
/* Одинаковый вид на всех компьютерных экранах: от 1280px страница масштабируется от эталонной ширины 1440px */
(function () {{
  var r = document.documentElement;
  r.classList.add('js');
  function fit() {{
    var w = window.innerWidth, h = window.innerHeight, z = w >= 1280 ? w / 1440 : 1;
    if (z === 1) {{ r.style.zoom = ''; r.style.removeProperty('--vw'); r.style.removeProperty('--vh'); return; }}
    r.style.zoom = z;
    r.style.setProperty('--vw', (w / z / 100) + 'px');
    r.style.setProperty('--vh', (h / z / 100) + 'px');
  }}
  fit();
  window.addEventListener('resize', fit);
}})();
</script>
<script src="main.js" defer></script>
</head>
<body class="{extra_class}">
<a class="skip" href="#main">К содержанию</a>
<header class="header">
  <a class="pill brand" href="index.html" aria-label="Сатурн Технолоджи — главная">{LOGO}</a>
  <nav id="navigation" class="notch" aria-label="Основная навигация">{nav}</nav>
  <a class="pill head-cta" href="contacts.html">Получить консультацию {icon("arrow")}</a>
  <button class="pill menu" aria-expanded="false" aria-controls="navigation"><span class="menu-label">Меню</span><span class="burger" aria-hidden="true"><i></i><i></i></span></button>
  <span class="progress" aria-hidden="true"></span>
</header>
<main id="main">
{body}
</main>
<footer class="footer">
  <div class="footer-main">
    <a class="brand" href="index.html" aria-label="Сатурн Технолоджи — главная">{LOGO_LIGHT}</a>
    <nav aria-label="Разделы">{fnav}</nav>
    <div class="footer-contacts"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{PHONE_HREF}">{PHONE}</a></div>
  </div>
  <div class="footer-bottom"><span>{ADDRESS}</span><span>© САТУРН Технолоджи</span></div>
</footer>
</body>
</html>
'''


def rail():
    items = [('index.html', 'home', 'Главная'), (PHONE_HREF, 'phone', PHONE),
             (f'mailto:{EMAIL}', 'mail', EMAIL), (MAP_URL, 'pin', 'Открыть на Яндекс Картах')]
    links = ''.join(
        f'<a href="{h}" aria-label="{l}" title="{l}"{" target=\"_blank\" rel=\"noopener\"" if h.startswith("https") else ""}>{icon(i)}</a>'
        for h, i, l in items)
    return f'<nav class="rail" aria-label="Быстрые действия">{links}</nav>'


def lines(*parts):
    """Заголовок, который появляется построчно."""
    return ''.join(f'<span class="line"><span>{p}</span></span>' for p in parts)


def inner_hero(kicker, title, lead, photo, lead_cls='lead'):
    if not photo:
        return f'''<section class="page-head">
  <a class="breadcrumb" href="index.html">Главная</a>
  <p class="kicker" data-load>{kicker}</p>
  <h1 class="display">{lines(title)}</h1>
</section>'''
    return f'''<section class="frame inner-frame">
  <div class="frame-bg" data-parallax style="background-image:url('assets/{photo}')"></div>
  {rail()}
  <div class="glass hero-panel" data-load>
    <a class="breadcrumb" href="index.html">Главная</a>
    <p class="kicker">{kicker}</p>
    <h1 class="display">{lines(title)}</h1>
    {f'<p class="{lead_cls}">{lead}</p>' if lead else ''}
  </div>
</section>'''


def open_hero(kicker, title, lead, photo, next_id):
    """Первый экран без плашки: текст прямо на фото, мягкое затемнение снизу."""
    down = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14 M6 13l6 6 6-6"/></svg>'
    return f'''<section class="frame open-frame">
  <div class="frame-bg" data-parallax style="background-image:url('assets/{photo}')"></div>
  {rail()}
  <div class="open-copy">
    <p class="kicker" data-load>{kicker}</p>
    <h1 class="display">{lines(title)}</h1>
    {f'<p class="lead" data-load>{lead}</p>' if lead else ''}
  </div>
  <a class="scroll-down" href="#{next_id}" aria-label="Перейти к содержанию" data-load>{down}</a>
</section>'''


def feature(title, text, cls=''):
    return f'<div class="feature{(" " + cls) if cls else ""}"><h3>{title}</h3>{f"<p>{text}</p>" if text else ""}</div>'


# ---------------- Главная ----------------
INDEX = f'''<section class="frame home-frame">
  <div class="frame-bg" data-parallax style="background-image:url('assets/hero-dusk.jpg')" role="img" aria-label="Нефтегазоперерабатывающая установка на закате"></div>
  {rail()}
  <div class="hero-copy">
    <p class="kicker" data-load>САТУРН ТЕХНОЛОДЖИ</p>
    <h1 class="display mega">{lines('Эффективность', 'вашего производства')}</h1>
    <p class="lead" data-load>Мы используем решения отвечающие всем требованиям клиента по надежности, экономичности, безопасности и цене. При этом предпочтение отдается тем решениям, применение которых позволяет сокращать расходы клиента не только на этапе строительства и в процессе их эксплуатации, но и при последующей модернизации и обслуживании</p>
  </div>
</section>

<section class="directions" id="directions">
  <article class="dir-card reveal" style="--img:url('assets/trainer-dusk.jpg')">
    <div class="glass dir-panel">
      <h2>Тренажер оператора</h2>
      <div class="dir-body"><div>
      <ul class="dir-points">
        <li>Тренажер оператора для технологических объектов с блоками I и II категории взрывоопасности согласно приказу №533 Ростехнадзора</li>
        <li>Обучение и проверка знаний персонала перед началом работ, без риска повреждения оборудования</li>
        <li>Повышение квалификации операторов, отработка нештатных ситуаций</li>
      </ul>
      </div></div>
      <a class="more" href="develop.html">Узнать больше {CIRCLE}</a>
    </div>
  </article>
  <article class="dir-card reveal" style="--img:url('assets/asutp-dusk.jpg')">
    <div class="glass dir-panel">
      <h2>АСУ ТП и средства автоматизации</h2>
      <div class="dir-body"><div>
      <p>Разработка и реализация автоматизированных систем управления технологическими процессами, а также продажа измерительных приборов и средств автоматики</p>
      </div></div>
      <a class="more" href="asutp.html">Узнать больше {CIRCLE}</a>
    </div>
  </article>
  <article class="dir-card reveal" style="--img:url('assets/supply-hero.jpg')">
    <div class="glass dir-panel">
      <h2>Компетенции в поставке МТР</h2>
      <div class="dir-body"><div>
      <p>Комплексная поставка оборудования и материально-технических ресурсов при выполнении технического обслуживания, ремонта, строительства и реконструкции, а также по прямым договорам поставки</p>
      </div></div>
      <a class="more" href="supply.html">Узнать больше {CIRCLE}</a>
    </div>
  </article>
</section>'''

# ---------------- Тренажер оператора (старая страница «Разработка») ----------------
DEV_ICONS = {
    'model': '<path d="M9 3h6 M10 3v6l-5 9a2 2 0 0 0 1.7 3h10.6a2 2 0 0 0 1.7-3l-5-9V3 M7.5 14h9"/>',
    'learn': '<path d="M2 9l10-5 10 5-10 5z M6 11v5c3 2 9 2 12 0v-5 M22 9v6"/>',
    'alarm': '<path d="M12 3l10 18H2z M12 10v5 M12 18h.01"/>',
    'check': '<path d="M9 3h6v3H9z M7 4.5H5V21h14V4.5h-2 M9 14l2 2 4-4"/>',
    'cycle': '<path d="M20 11a8 8 0 1 0-2.3 5.7 M20 4v7h-7"/>',
    'shield': '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z M9 12l2 2 4-4"/>',
    'link': '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1 M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    'server': '<path d="M4 4h16v6H4z M4 14h16v6H4z M8 7h.01 M8 17h.01 M12 7h4 M12 17h4"/>',
    'code': '<path d="M8 8l-4 4 4 4 M16 8l4 4-4 4 M14 5l-4 14"/>',
    'wave': '<path d="M3 12h4l3-8 4 16 3-8h4"/>',
    'team': '<path d="M16 20v-1a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v1 M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8 M22 20v-1a4 4 0 0 0-3-3.9 M16 3.1a4 4 0 0 1 0 7.8"/>',
    'chip': '<path d="M7 7h10v10H7z M10 10h4v4h-4z M9 3v4 M15 3v4 M9 17v4 M15 17v4 M3 9h4 M3 15h4 M17 9h4 M17 15h4"/>',
    'layers': '<path d="M12 3l9 5-9 5-9-5z M3 13l9 5 9-5"/>',
    'key': '<path d="M15 9a4 4 0 1 0-3.9 4.9L9 16H7v2H5v2H3v-3l6.1-6.1 M15 7h.01"/>',
}


def dicon(name):
    return f'<span class="ico" aria-hidden="true"><svg viewBox="0 0 24 24">{DEV_ICONS[name]}</svg></span>'


def bento(icon_name, title, text, cls=''):
    return f'<div class="bento-card{(" " + cls) if cls else ""} reveal">{dicon(icon_name)}<h3>{title}</h3><p>{text}</p></div>'


DEVELOP = open_hero('Сатурн Технолоджи', 'Тренажер оператора АСУ ТП', 'Ваши сотрудники готовы к любым ситуациям', 'trainer-dusk.jpg', 'features') + f'''
<section class="block" id="features">
  <div class="bento">
    <div class="bento-title reveal" style="--img:url('assets/trainer-features.jpg')"><h2 class="display-2">Основные возможности тренажера</h2></div>
    {bento('model', 'Моделирование', 'Имитация технологических процессов, работу АСУ ТП и СПАЗ, а также интерфейс АСУ ТП ( в случае наличия такой потребности)')}
    {bento('learn', 'Обучение', 'Проводить как самостоятельное обучение по заданным сценариям, так и обучение под руководством инструктора')}
    {bento('alarm', 'Нештатные ситуации', 'Имитация неисправности оборудования, каналов управления и блоков АСУ ТП. Возможность задания ситуаций согласно ПЛАС.', 'warm')}
    {bento('check', 'Система обучения', 'Проводить плановые и внеплановые проверки знаний (отработку сценариев и прохождение тестов)')}
    {bento('cycle', 'Навыки всегда актуальны', 'Восстанавливать навыки управления после длительного перерыва (отпуск, вахта, болезнь)')}
    {bento('shield', 'Минимизация рисков', 'Организовывать проверки режимов работы комплекса, без риска повреждения оборудования')}
  </div>
</section>

<section class="frame order-frame reveal">
  <div class="frame-bg" data-parallax style="background-image:url('assets/trainer-order.jpg')"></div>
  <div class="glass order-panel">
    <h2>Соответсвие приказу Ростехнадзора №533 от 15 декабря 2020 года</h2>
    <p>Согласно приказу Ростехнадзора на технологических объектах с блоками I и II категории взрывоопасности все сотрудники, непосредственно ведущие технологический процесс, должны проходить обучение на тренажерах, содержащих максимально приближенные к реальным динамические модели процессов.</p>
    <p>Внедрение тренажерного комплекса позволит вашему предприятию соответствовать данным требованиям</p>
  </div>
  <figure class="order-doc"><img src="assets/rtn-order-533.jpg" alt="Приказ Ростехнадзора №533 от 15 декабря 2020 года" loading="lazy" width="1321" height="760"></figure>
</section>

<section class="block models">
  <div class="models-media reveal"><div class="models-img" data-parallax style="background-image:url('assets/trainer-models.jpg')"></div><span class="models-badge">{dicon('wave')}</span></div>
  <div class="models-text">
    <h2 class="display-2 reveal">Динамические модели процессов</h2>
    <ul class="models-steps" data-progress>
      <li class="reveal">В составе тренажера используются динамические модели технологических процессов. Эти модели основаны на физико-химических моделях процессов происходящих в технологическом оборудовании.</li>
      <li class="reveal">Базовые модели актуализируются на этапе проектирования, в соответствии с особенностями конкретного технологического объекта заказчика.</li>
      <li class="reveal">Тонкая настройка моделей может производится путем автоматического сбора данных и подстройке параметров моделей на основе данных реальной АСУ ТП.</li>
      <li class="reveal">Тренажер подготовит Ваш персонал к управлению технологическим комплексом в штатных и пусковых режимах работы, принятию необходимых мер при возникновении нештатных и аварийных ситуаций.</li>
    </ul>
  </div>
</section>

<section class="block">
  <div class="block-head reveal">
    <h2 class="display-2">Интеграция с любой системой АСУ ТП</h2>
    <p>Тренажер может использоватсья в двух режимах:</p>
  </div>
  <div class="mode-grid">
    <div class="mode-card reveal">{dicon('link')}<p>в режиме интеграции с существующей АСУ ТП, когда она выступает в качестве интерфейса, а тренажер моделирует только работу оборудования.</p></div>
    <div class="mode-card reveal">{dicon('server')}<p>в независимом режиме - когда тренажер также эмулирует и АСУ ТП, что особенно важно в случае когда невозможна полноценная работа с ушедшим с российского рынка вендором.</p></div>
  </div>
  <div class="import-card reveal">
    {dicon('code')}
    <div><h2>Импортозамещение</h2><p>Тренажер полностью российская разработка, базирующиеся на компонентах и продуктах с открытым исходным кодом. Это позволяет ей быть устойчивой и независимой при любой ситуации на рынке.</p></div>
  </div>
</section>

<section class="block architecture">
  <div class="block-head reveal">
    <h2 class="display-2">Архитектура решения</h2>
    <p>Архитектура решения постоянно развивается и эволюционирует, для максимально полного удовлетворения требований раших заказчиков</p>
  </div>
  <figure class="diagram reveal">
    <a href="assets/trainer-architecture.png" target="_blank" rel="noopener"><img src="assets/trainer-architecture.png" alt="Архитектура решения: клиенты экзаменатора и обучаемых, сервер моделирования, сервер БД и бизнес логики, опциональный SCADA сервер, клиент настройки и конфигурирования, технологический сегмент с серверами АСУ ТП. Технологии: Astra Linux, .Net, Postgre SQL и использование SCADA систем в качестве интерфейса для обучения" loading="lazy" width="1680" height="1096"></a>
  </figure>
</section>'''

# ---------------- АСУ ТП ----------------
ASUTP = open_hero('САТУРН Технолоджи', 'Создание АСУ ТП и продажа измерительных приборов, средств автоматики', '', 'asutp-hero.jpg', 'intro') + f'''
<section class="block split" id="intro">
  <div class="split-media reveal"><div class="split-img" data-parallax style="background-image:url('assets/asutp-instruments.jpg')"></div></div>
  <div class="split-text reveal">
    <p class="big-text">Как независимый интегратор автоматизированных систем, мы устанавливаем на объектах продукцию тех производителей, чье оборудование отвечает всем требованиям клиента по надежности, экономичности, безопасности и цене. При этом предпочтение отдается тем инновационным автоматизированным системам, применение которых позволяет сокращать расходы клиента не только на этапе строительства и в процессе их эксплуатации, но и при последующей модернизации и обслуживании</p>
  </div>
</section>

<section class="block split reverse">
  <div class="split-media reveal"><div class="split-img" data-parallax style="background-image:url('assets/asutp-team.jpg')"></div><span class="models-badge">{dicon('team')}</span></div>
  <div class="split-text reveal">
    <h2 class="display-2">Сильная команда</h2>
    <p class="big-text">Высококлассные, опытные специалисты с широким практическим опытом в сфере автоматизации технологических процессов.</p>
    <p>За свою относительно недолгую историю компания «Сатурн — Технолоджи» накопила достаточно обширный опыт успешной реализации проектов, в которых участвовало несколько компаний подрядчиков. Этому в значительной степени помогли методики планирования, реализации, координации и<br>контроля, разработанные внутри компании.</p>
  </div>
</section>

<section class="block">
  <div class="bento">
    <div class="bento-title tall reveal" style="--img:url('assets/asutp-partners.jpg')">
      <div><h2 class="display-2">Наш приоритет - партнерские отношения</h2><p>Основной целью нашей компании является установление долгосрочных партнерских отношений со своими клиентами, поэтому в своей работе мы не стремимся к сиюминутной максимизации прибыли</p></div>
    </div>
    {bento('team', 'Команда', 'Имеем в своей команде высококлассных, опытных инженеров с высшим образованием в сфере автоматизации технологических процессов')}
    {bento('chip', 'Технологии', 'Мы сами являемся носителями технологий и ни у кого их не заимствуем')}
    {bento('layers', 'Решения', 'Предлагаем как индивидуальные, так и типовые решения, которые могут быть более экономичными')}
    {bento('link', 'Сотрудничество', 'Являемся представителями ведущих производителей инженерного оборудования, что позволяет быть гибкими в выборе конкретного оборудования при реализации конкретного проекта')}
    {bento('key', 'Под-ключ', 'Всегда готовы предложить решение “под ключ”, начиная с разработки проекта и заканчивая пуско-наладкой', 'warm wide')}
  </div>
</section>'''

# ---------------- Поставка МТР ----------------
RU = ['ООО «Электронстандартприбор»', 'ООО «Рэко-Век»', 'ООО «ВНИИГАЗ»', 'ООО НПП «Эталон»', 'ЗАО «ПГ Метран»', 'ЗАО «Виброприбор»', 'ЗАО «Манометр»', 'ЗАО «Система Газ»', 'ЗАО НПФ «Система-Сервис»', 'ЗАО «Атлантиктрансгазсистема»', 'ЗАО «ДС Контролз»', 'ОАО «Манотомь»', 'ОАО НПФ «Вымпел»', 'ОАО «Промприбор»', 'ОАО «Автоматика»', 'ОАО «МЗТА»']
ALSO = 'Compressor Control Corp., General Electric, Klinkmann, Invensys Process Systems, Schneider Electric Systems (Ранее - Invensys Process Systems), WIKA, Cisco, D-Link, Phoenix Contact, Endress+Hauser, ABB, SIEMENS, GE IP, Rockwell Automation, Phase Dynamics, iFix компании Intellution, PI System компании OSIsoft, Yokogawa, НПП «ЭлеМер», НПФ «ОВЕН-К», Emerson, MTL, JUMO, Dresser, Zyxel, APC by Schneider Electric, APC, Ritall и др'
SUPPLY = open_hero('САТУРН Технолоджи', 'Компетенции в поставке МТР', 'Комплексная поставка оборудования и материально-технических ресурсов при выполнении технического обслуживания, ремонта, строительства и реконструкции, а также по прямым договорам поставки', 'supply-hero.jpg', 'channels') + f'''
<section class="block channels" id="channels">
  <article class="channel reveal" style="--img:url('assets/supply-import.jpg')"><div class="glass dir-panel"><h2>Прямые контракты с иностраными заводами</h2></div></article>
  <article class="channel reveal" style="--img:url('assets/supply-domestic.jpg')"><div class="glass dir-panel"><h2>Поставка МТР отечественных производителей</h2></div></article>
  <article class="channel reveal" style="--img:url('assets/supply-official.jpg')"><div class="glass dir-panel"><h2>Поставка МТР иностранного производства через оф. представителей в РФ</h2></div></article>
</section>

<section class="block split">
  <div class="split-media reveal"><div class="split-img" data-parallax style="background-image:url('assets/supply-partners.jpg')"></div></div>
  <div class="split-text reveal">
    <h2 class="display-2">Ключевые партнеры:</h2>
    <ul class="partner-list">{''.join(f'<li>✓ {n}</li>' for n in RU)}</ul>
  </div>
</section>

<section class="block reveal">
  <div class="also-card">
    <h2 class="display-3">А также:</h2>
    <p class="also-text">{ALSO}</p>
  </div>
</section>'''

# ---------------- Вакансии ----------------
SUMMARY = {
    'Разработчик .Net': 'Разработка микросервисного ядра приложений, с применением RabbitMQ, Postgres, микросервисов и оптимизация его для работы под нагрузкой',
    'Разработчик Frontend (React)': 'Разработка пользовательского интерфейса с использованием лучших практики по UX\\UI и создание сложных элементов для визуализации технологических процессов',
    'Системный аналитик': 'Проработка и детализация требований к системе. Проектирование ключевых алгоритмов и структур данных совместно с командой',
    'Тестировщик': 'Организация тестирования продукта и постепенная автоматизация данного процесса',
}


def parse_jobs():
    """Полные тексты вакансий из выгрузки старого сайта: абзацы + списки «Требования» и «Мы предлагаем»."""
    vac = OLD[OLD.index('========== vacancy.html'):]
    blocks = re.split(r'---- rec\d+ 232\n---- recorddiv\d+ \n', vac)[1:]
    jobs = []
    for b in blocks:
        b = re.split(r'\n---- rec', b)[0]
        rows = [r.strip() for r in b.split('\n')]
        title, rest = rows[0], rows[1:]
        intro, req, offer, cur = [], [], [], 'intro'
        for r in rest:
            if not r:
                continue
            if r == 'Требования к кандидату':
                cur = 'req'; continue
            if r == 'Мы предлагаем':
                cur = 'offer'; continue
            {'intro': intro, 'req': req, 'offer': offer}[cur].append(r)
        jobs.append((title, intro, req, offer))
    return jobs


def job_html(i, title, intro, req, offer):
    ul = lambda items: '<ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'
    return f'''<details class="job">
    <summary><span class="job-number">{i:02d}</span><div class="job-head"><h2>{title}</h2><p class="job-summary">{SUMMARY[title]}</p></div><span class="job-more">подробнее</span><span class="plus" aria-hidden="true"></span></summary>
    <div class="job-content">
      {''.join(f'<p>{p}</p>' for p in intro)}
      <h3>Требования к кандидату</h3>{ul(req)}
      <h3>Мы предлагаем</h3>{ul(offer)}
    </div>
  </details>'''


JOBS = parse_jobs()
assert [j[0] for j in JOBS] == list(SUMMARY), [j[0] for j in JOBS]
VACANCY = open_hero('САТУРН Технолоджи', 'Вакансии', '', 'vacancy-hero.jpg', 'jobs') + f'''
<section class="jobs reveal" id="jobs">
  {''.join(job_html(i + 1, *j) for i, j in enumerate(JOBS))}
</section>
<section class="resume reveal">
  <a class="button primary magnetic" href="mailto:saturnrutech@gmail.com">Отправить резюме {CIRCLE}</a>
  <a class="resume-mail" href="mailto:saturnrutech@gmail.com">saturnrutech@gmail.com</a>
</section>'''

# ---------------- Контакты ----------------
CONTACTS = open_hero('САТУРН Технолоджи', 'Контакты', '', 'contacts-hero.jpg', 'contacts') + f'''
<section class="contacts-grid reveal" id="contacts">
  <div class="contact-card">
    <p class="contact-label">Электронная почта</p>
    <a class="large-contact" href="mailto:{EMAIL}">{EMAIL}</a>
    <button class="copy" type="button" data-copy="{EMAIL}">Скопировать адрес</button>
  </div>
  <div class="contact-card">
    <p class="contact-label">Телефон</p>
    <a class="large-contact" href="{PHONE_HREF}">{PHONE}</a>
    <button class="copy" type="button" data-copy="{PHONE}">Скопировать номер</button>
  </div>
  <div class="contact-card address">
    <p class="contact-label">Адрес</p>
    <h2>САТУРН Технолоджи</h2>
    <p>{ADDRESS}</p>
    <a class="text-link" href="{MAP_URL}" target="_blank" rel="noopener">Открыть на Яндекс Картах</a>
  </div>
</section>'''

pages = {
    'index.html': ('Главная — Сатурн Технолоджи', INDEX, 'home'),
    'develop.html': ('Тренажер оператора — Сатурн Технолоджи', DEVELOP, ''),
    'asutp.html': ('АСУ ТП — Сатурн Технолоджи', ASUTP, ''),
    'supply.html': ('МТР — Сатурн Технолоджи', SUPPLY, ''),
    'vacancy.html': ('Вакансии — Сатурн Технолоджи', VACANCY, ''),
    'contacts.html': ('Контакты — Сатурн Технолоджи', CONTACTS, ''),
}
for f, (t, b, c) in pages.items():
    with open(os.path.join(OUT, f), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(page(f, t, b, c))
    print('wrote', f)
