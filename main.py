import flet as ft
import io
import contextlib
import datetime
import subprocess
import sys
import webbrowser

def main(page: ft.Page):
    # titre nle fenetre
    page.title = "CodePy - IDE"
    page.theme_mode = ft.ThemeMode.LIGHT

    # function manova theme
    def theme_changed(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        page.update()

    # Switch ho manova ny theme mainty na fotsy
    theme_switch = ft.Switch(on_change=theme_changed)

    # Faritra fanoratana code
    code_input = ft.TextField(
        multiline=True,
        min_lines=15,
        expand=True,
    )

    # Console ilay resultat le code mivaka amin ty
    output_display = ft.TextField(
        multiline=True,
        read_only=True,
        min_lines=5,
        expand=True,
    )

    # textfield ho an'ny module Python
    installation_input = ft.TextField(label="Module à installer")

    # chargement miseho rehefa manao telechargement
    loading_indicator = ft.ProgressRing(visible=False)

    # function manao installation module
    def install_module(module_name):
        loading_indicator.visible = True
        page.update()
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
            output_display.value = f"Module '{module_name}' napetraka soa aman-tsara."
        except Exception as e:
            output_display.value = f"Hadisoana tamin'ny fametrahana: {str(e)}"
        loading_indicator.visible = False
        page.update()

    # button rehefa manao installation module
    install_button = ft.ElevatedButton(
        "Installer", on_click=lambda e: install_module(installation_input.value)
    )

    # Fonction mandefa/run ilay code avy any amin'ny ilay textfield
    def run_code(e):
        code = code_input.value
        buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
                exec(code, {})
        except Exception as ex:
            buffer.write(f"Erreur: {ex}")
        output_display.value = buffer.getvalue()
        page.update()

    # Fonction mi savegarder ilay code
    def save_code(e):
        code = code_input.value
        now = datetime.datetime.now()
        filename = f'code_{now.strftime("%Y-%m-%d_%H-%M-%S")}.py'
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(code)
            output_display.value = "Sauvegarde effectuée"
        except Exception as err:
            output_display.value = f"Erreur lors de la sauvegarde : {err}"
        page.update()
       
    # Fonction manokatra ny documentation python NB: online 
    def open_documentation():
        webbrowser.open("https://docs.python.org/3/")

    # Fonction "À propos" just a propos ny appliction
    def show_about(e=None):
        output_display.value = """
        CodePy 
        Version 1.0.0
        Cette application est un environnement de développement intégré (IDE)
        simple et léger conçu avec Flet pour exécuter du code Python en toute simplicité.

        Elle permet d'écrire, d'exécuter et de sauvegarder du code Python,
        d’installer des modules, et d’accéder à la documentation officielle de Python.

        Développée par Manitra & Tendry
        """
        page.update()

    # Bouton milance ilay code, misavegarder, documentation, momba ilay application
    run_button = ft.ElevatedButton(" ", on_click=run_code, icon=ft.icons.PLAY_ARROW)
    save_button = ft.ElevatedButton(" ", on_click=save_code, icon=ft.icons.SAVE)
    doc_button = ft.ElevatedButton("Documentation", on_click=lambda e: open_documentation())
    about_button = ft.ElevatedButton(" ", on_click=show_about, icon=ft.icons.INFO)

    # Affichage ny variable rehetra ao amin flet
    page.add(
        ft.Row([about_button, doc_button, theme_switch]),
        ft.Row([installation_input, install_button, loading_indicator]),
        code_input,
        ft.Row([run_button, save_button]),
        output_display,
    )

ft.app(target=main)
