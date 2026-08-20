import shutil
from pathlib import Path

from pydantic import TypeAdapter
from jinja2 import Environment, FileSystemLoader, select_autoescape

from models import Information

current_dir = Path(__file__).parent.absolute()
build_folder = current_dir / 'build'

# TODO: This is not generic enough, we should fix it later if the
# need to accommodate more pyrole pages arives.
jinja_env = Environment(
    loader=FileSystemLoader(current_dir / 'pybr26'),
    autoescape=select_autoescape(['html'])
)


def _create_build_folder():
    if build_folder.exists() and build_folder.is_dir():
        shutil.rmtree(build_folder)

    build_folder.mkdir()


def render_pybr26():
    _create_build_folder()

    with open(current_dir / 'pybr26' / 'data.json') as f:
        information = TypeAdapter(Information).validate_json(f.read())

    html = jinja_env.get_template('index.html').render(information=information)
    build_folder.joinpath('index.html').write_text(html)


if __name__ == "__main__":
    render_pybr26()
