from os.path import dirname, realpath, join


def load_styles() -> str:
    dir_here = dirname(realpath(__file__))
    file_url = join(dir_here, "../styles/main.css")
    style: str | None = None

    with open(file_url, "r") as css:
        style = css.read()
    return style


def load_off_icon() -> str:
    return join(dirname(realpath(__file__)), "../images/off.png")


def load_on_icon() -> str:
    return join(dirname(realpath(__file__)), "../images/on.png")


def load_morning_icon() -> str:
    return join(dirname(realpath(__file__)), "../images/dia.png")


def load_afternoon_icon() -> str:
    return join(dirname(realpath(__file__)), "../images/tarde.png")


def load_evening_icon() -> str:
    return join(dirname(realpath(__file__)), "../images/luna.png")


def load_cold_icon() -> str:
    return join(dirname(realpath(__file__)), "../images/frio.png")


def load_warm_icon() -> str:
    return join(dirname(realpath(__file__)), "../images/tibio.png")


def load_hot_icon() -> str:
    return join(dirname(realpath(__file__)), "../images/caliente.png")


def load_offline_icon() -> str:
    return join(dirname(realpath(__file__)), "../images/desenchufado.png")


def load_logo_icon() -> str:
    return join(dirname(realpath(__file__)), "../images/logo.png")
