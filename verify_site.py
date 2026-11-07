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
    page.on('pageerror', lambda error: errors.append(str(error)))
    for width in [360, 390, 768, 1024, 1440]:
        page.set_viewport_size({'width': width, 'height': 900})
        page.goto('http://localhost:8080', wait_until='networkidle')
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), width
        assert page.locator('#hero-title').inner_text() == 'Sắp ra mắt'
        assert page.locator('#countdown').is_hidden()
        assert page.locator('[data-copy]:visible').count() == 0
        assert page.locator('[data-ip="java"]').inner_text() == 'Sẽ công bố khi mở cửa'
        if width < 640:
            page.locator('.menu-toggle').click()
            assert page.locator('#menu').is_visible()
            page.keyboard.press('Escape')
            assert page.locator('#menu').is_hidden()
        page.locator('summary').first.click()
        assert page.locator('details').first.get_attribute('open') is not None
        page.locator('summary').first.click()
        page.screenshot(path=str(OUT / f'{width}.png'))
    source = (ROOT / 'script.js').read_text(encoding='utf-8')
    for mode, date in [('future', '2099-12-20T19:00:00+07:00'), ('past', '2020-12-20T19:00:00+07:00'), ('invalid', 'invalid')]:
        changed = source.replace('HIEN_IP: false', 'HIEN_IP: true').replace('NGAY_MO: null', f'NGAY_MO: "{date}"')
        page.route('**/script.js', lambda route: route.fulfill(body=changed, content_type='text/javascript'))
        page.goto('http://localhost:8080', wait_until='networkidle')
        assert page.locator('[data-ip="java"]').inner_text() == 'play.wildrest.vn'
        assert page.locator('[data-copy]:visible').count() == 3
        if mode == 'future':
            assert page.locator('#countdown').is_visible()
            page.context.grant_permissions(['clipboard-read', 'clipboard-write'])
            page.locator('#hero-ip').click()
            assert page.evaluate('navigator.clipboard.readText()') == 'play.wildrest.vn'
            assert page.locator('#toast').inner_text().startswith('✦\nĐã copy!')
            page.evaluate("Object.defineProperty(navigator,'clipboard',{value:undefined,configurable:true})")
            page.locator('[data-copy="port"]').click()
            assert page.locator('#toast strong').inner_text() == 'Đã copy!'
        elif mode == 'past':
            assert page.locator('#hero-title').inner_text() == 'Đã mở cửa! Vào chơi ngay'
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
    page.goto('http://localhost:8080/404.html')
    assert page.locator('a').get_attribute('href') == '/'
    assert not errors, errors
    browser.close()
print('PASS: 5 viewports, menu, FAQ, IP, clipboard + fallback, countdown, reduced motion, 404; no page errors.')
