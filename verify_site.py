"""Kiểm tra trình duyệt cục bộ: python verify_site.py (cần playwright và Chrome)."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
OUT = ROOT / '.qa'
OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch(channel='chrome', headless=True)
    page = browser.new_page()
    errors = []
    missing = []
    status_api = 'https://api.mcstatus.io/v2/status/java/*'
    page.route(status_api, lambda route: route.fulfill(json={'online': True, 'players': {'online': 2}}))
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('response', lambda response: missing.append(response.url) if response.status == 404 and response.url.startswith('http://localhost:8080') else None)
    for width in [360, 390, 768, 1024, 1440]:
        page.set_viewport_size({'width': width, 'height': 900})
        page.goto('http://localhost:8080', wait_until='networkidle')
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), width
        assert page.locator('#hero-title img').get_attribute('alt') == 'WildRest.vn — Server Minecraft sinh tồn Việt Nam'
        assert page.locator('#launch-status').text_content() == 'Đang mở thử nghiệm'
        assert page.locator('#hero-ip').get_attribute('href') == '#cach-vao'
        assert page.locator('#countdown').is_hidden()
        assert page.locator('[data-copy]:visible').count() == 3
        assert page.locator('[data-ip="java"]').inner_text() == 'play.wildrest.vn'
        assert page.locator('[data-ip="bedrock"]').inner_text() == 'play.wildrest.vn'
        assert page.locator('#bedrock-port').inner_text() == '19132'
        assert page.locator('.edition [data-version="java"]').inner_text() == '1.21.4–26.3'
        assert page.locator('#cach-vao [data-version="bedrock"]').inner_text() == '26.40 đến 26.60'
        if width < 880:
            page.locator('.menu-toggle').click()
            assert page.locator('#menu').is_visible()
            page.keyboard.press('Escape')
            assert page.locator('#menu').is_hidden()
        page.locator('summary').first.click()
        assert page.locator('details').first.get_attribute('open') is not None
        page.locator('summary').first.click()
        page.screenshot(path=str(OUT / f'{width}.png'))
    source = (ROOT / 'script.js').read_text(encoding='utf-8')
    page.set_viewport_size({'width': 390, 'height': 844})
    page.context.grant_permissions(['clipboard-read', 'clipboard-write'])
    for edition, value in [('java', 'play.wildrest.vn'), ('bedrock', 'play.wildrest.vn'), ('port', '19132')]:
        page.locator(f'[data-copy="{edition}"]').click()
        assert page.evaluate('navigator.clipboard.readText()') == value
    for mode, date in [('future', '2099-12-20T19:00:00+07:00'), ('past', '2020-12-20T19:00:00+07:00'), ('invalid', 'invalid')]:
        changed = source.replace('NGAY_MO: null', f'NGAY_MO: "{date}"')
        page.route('**/script.js', lambda route: route.fulfill(body=changed, content_type='text/javascript'))
        page.goto('http://localhost:8080', wait_until='networkidle')
        assert page.locator('[data-ip="java"]').inner_text() == 'play.wildrest.vn'
        assert page.locator('[data-copy]:visible').count() == 3
        if mode == 'future':
            assert page.locator('#countdown').is_visible()
            page.locator('#hero-ip').click()
            assert page.evaluate('navigator.clipboard.readText()') == 'play.wildrest.vn'
            assert page.locator('#toast').inner_text().startswith('✦\nĐã copy!')
            page.evaluate("Object.defineProperty(navigator,'clipboard',{value:undefined,configurable:true})")
            page.locator('[data-copy="port"]').click()
            assert page.locator('#toast strong').inner_text() == 'Đã copy!'
        elif mode == 'past':
            assert page.locator('#launch-status').text_content() == 'Đã mở cửa! Vào chơi ngay'
            assert page.locator('#hero-title img').count() == 1
        else:
            assert page.locator('#countdown').is_hidden()
        page.unroute('**/script.js')
    page.emulate_media(reduced_motion='reduce')
    page.goto('http://localhost:8080', wait_until='networkidle')
    assert page.locator('.hero-logo').evaluate('(e) => getComputedStyle(e).animationName') == 'none'
    page.set_viewport_size({'width': 1440, 'height': 1000})
    page.screenshot(path=str(OUT / 'desktop.png'), full_page=True)
    size = page.evaluate('performance.getEntriesByType("resource").reduce((n,r)=>n+r.encodedBodySize,0)')
    print('Initial resources:', size, 'bytes')
    assert size < 1500000
    page.set_viewport_size({'width': 390, 'height': 844})
    page.screenshot(path=str(OUT / 'mobile.png'), full_page=True)
    for width in [390, 1440]:
        page.set_viewport_size({'width': width, 'height': 1000})
        for selector, name in [('#anh', 'gallery'), ('#cap-nhat', 'updates')]:
            page.locator(selector).screenshot(path=str(OUT / f'v3-{width}-{name}.png'), style='.header,.skip-link{visibility:hidden!important}')
    import json
    schema = json.loads(page.locator('script[type="application/ld+json"]').text_content())
    assert len(schema['@graph']) == 5
    assert next(item for item in schema['@graph'] if item['@type'] == 'Person')['name'] == 'LouisHieuuu'
    assert page.locator('#owner-title').inner_text() == 'LouisHieuuu'
    assert page.locator('#menu a[href="#owner"]').count() == 1
    assert page.locator('#owner').evaluate('(e) => e.previousElementSibling.id') == 'cach-vao'
    assert page.locator('#owner').evaluate('(e) => e.nextElementSibling.id') == 'hoi-dap'
    assert page.locator('.owner-character').evaluate('(e) => getComputedStyle(e).animationName') == 'none'
    assert len(schema['@graph'][-1]['mainEntity']) == page.locator('details').count()
    for index, detail in enumerate(page.locator('details').all()):
        question = schema['@graph'][-1]['mainEntity'][index]
        assert question['name'] == detail.locator('summary').inner_text()
        answer = ' '.join(detail.locator('p').text_content().split())
        assert question['acceptedAnswer']['text'] == answer, (question, answer)
    assert page.locator('meta[property="og:image"]').get_attribute('content').endswith('/og-v2.jpg')
    assert page.locator('img.feature-icon').count() == 13
    for icon in page.locator('img.feature-icon').all():
        assert (ROOT / icon.get_attribute('src')).is_file()
    photos = page.evaluate('ANH_MAY_CHU')
    assert len(photos) == page.locator('#gallery-grid img').count()
    for photo in photos:
        original = ROOT / photo['src']
        assert photo['alt'].strip()
        assert original.is_file()
        assert original.with_name(original.stem + '-640.webp').is_file()
    assert page.locator('#update-list article').count() == len(page.evaluate('CAP_NHAT'))
    assert page.locator('#server-status').is_visible()
    assert page.locator('#server-status strong').inner_text() == '2'
    assert page.locator('a[data-vote]').count() == 2
    for link in page.locator('a[data-vote]').all():
        assert link.get_attribute('href') == 'https://minecraft-mp.com/server/366670/vote/'
    no_js = browser.new_page(java_script_enabled=False)
    no_js.goto('http://localhost:8080')
    assert no_js.locator('[data-ip]').all_text_contents() == ['play.wildrest.vn'] * 2
    assert no_js.locator('#bedrock-port').inner_text() == '19132'
    assert no_js.locator('#update-list time').evaluate_all('(dates) => dates.map(date => date.dateTime)') == ['2026-11-12', '2026-11-11', '2026-11-10']
    no_js.close()
    page.set_viewport_size({'width': 390, 'height': 844})
    first_photo = page.locator('#gallery-grid button').first
    first_photo.press('Enter')
    lightbox = page.locator('#gallery-lightbox')
    assert lightbox.is_visible()
    assert lightbox.locator('img').get_attribute('src') == photos[0]['src']
    page.keyboard.press('ArrowRight')
    assert lightbox.locator('img').get_attribute('src') == photos[1]['src']
    page.keyboard.press('ArrowLeft')
    assert lightbox.locator('img').get_attribute('src') == photos[0]['src']
    page.keyboard.press('Escape')
    assert lightbox.is_hidden()
    assert first_photo.evaluate('(button) => button === document.activeElement')
    assert page.locator('[data-social]:visible').count() == 0
    page.route('https://mc-heads.net/**', lambda route: route.abort())
    page.unroute(status_api)
    page.route(status_api, lambda route: route.fulfill(json={'online': False}))
    hidden_ip = source.replace('HIEN_IP: true', 'HIEN_IP: false')
    page.route('**/script.js', lambda route: route.fulfill(body=hidden_ip, content_type='text/javascript'))
    page.goto('http://localhost:8080', wait_until='networkidle')
    assert page.locator('#server-status').is_hidden()
    assert page.locator('[data-ip]').all_text_contents() == ['Sẽ công bố khi mở cửa'] * 2
    assert page.locator('#bedrock-port').inner_text() == 'Sẽ công bố khi mở cửa'
    assert page.locator('[data-copy]:visible').count() == 0
    page.locator('#owner').scroll_into_view_if_needed()
    page.wait_for_function('document.querySelector(".owner-avatar").hidden')
    assert page.request.get('http://localhost:8080/.well-known/discord').body() == b'dh=dd86fffe4e37f78146784d67dde8d157b343b378\n'
    for resource in ['robots.txt', 'sitemap.xml']:
        assert page.request.get('http://localhost:8080/' + resource).status == 200
    page.goto('http://localhost:8080/404.html')
    assert page.locator('a').get_attribute('href') == '/'
    assert not errors, errors
    assert not missing, missing
    browser.close()
print('PASS: 5 viewports, menu, FAQ, IP, clipboard + fallback, countdown, reduced motion, 404; no page errors.')
