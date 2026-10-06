import time
from playwright.sync_api import sync_playwright

PSEUDO = "WinterHarass"
SITES = ["SERVEURLISTE", "SERVEUR-MINECRAFT-VOTE"]

def voter(ctx, nom):
    page = ctx.new_page()
    page.goto("https://hyleria.fr/vote", wait_until="networkidle")
    with ctx.expect_page() as nouvelle:
        page.get_by_text(nom, exact=False).first.click()
    site = nouvelle.value
    site.wait_for_load_state("networkidle")
    try:
        champ = site.locator("input[type='text'], input[name*='pseudo'], input[name*='username']").first
        champ.fill(PSEUDO)
        site.locator("button[type='submit'], input[type='submit'], button:has-text('Voter')").first.click()
        site.wait_for_timeout(6000)
        print(nom, "OK")
    except Exception as e:
        print(nom, "ERREUR", e)
        site.screenshot(path=f"erreur_{nom}.png")
    site.close()
    page.close()

with sync_playwright() as p:
    nav = p.chromium.launch(headless=True)
    ctx = nav.new_context()
    for nom in SITES:
        voter(ctx, nom)
        time.sleep(10)
    nav.close()
