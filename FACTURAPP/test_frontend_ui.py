from playwright.sync_api import Page, expect


def test_login_muestra_campos_y_boton(page: Page):
    page.goto("http://127.0.0.1:5000/login")

    # Comprueba que el formulario aparece
    expect(page.locator("form")).to_be_visible()

    # Comprueba los campos de correo y contraseña
    expect(page.locator('input[name="email"]')).to_be_visible()
    expect(page.locator('input[name="password"]')).to_be_visible()

    
    expect(
        page.locator("form button, form input[type='submit']")
    ).to_be_visible()

def test_login_no_envia_formulario_vacio(page: Page):
    page.goto("http://127.0.0.1:5000/login")

    boton = page.locator(
        "form button, form input[type='submit']"
    ).first

    boton.click()

    
    assert page.url.rstrip("/").endswith("/login")

    
    expect(
        page.locator('input[name="email"]')
    ).to_be_visible()



def test_login_correcto(page: Page):
    page.goto("http://127.0.0.1:5000/login")

    page.locator('input[name="email"]').fill("octa@facturapp.com")
    page.locator('input[name="password"]').fill("12345678")

    page.locator("form button, form input[type='submit']").first.click()

    page.wait_for_load_state("networkidle")

    assert "/login" not in page.url



def test_clientes_redirige_sin_sesion(page: Page):
    page.goto("http://127.0.0.1:5000/logout")
    page.goto("http://127.0.0.1:5000/clientes/")

    expect(page).to_have_url(
        "http://127.0.0.1:5000/login"
    )


def test_clientes_carga_con_sesion(page: Page):
    page.goto("http://127.0.0.1:5000/login")

    page.locator('input[name="email"]').fill("octa@facturapp.com")
    page.locator('input[name="password"]').fill("12345678")
    page.locator("form button, form input[type='submit']").first.click()

    page.wait_for_load_state("networkidle")
    page.goto("http://127.0.0.1:5000/clientes/")

    expect(page).to_have_url(
        "http://127.0.0.1:5000/clientes/"
    )
