from fasthtml.common import *
from home_components import *
from content import *

_blank = dict(target="_blank", rel="noopener noreferrer")
description = "benvenuti..."


def footer_link(text, href, **kw):
    return Li(
        A(
            Span(text, cls="border-b border-b-transparent border-b-white/50"),
            Img(
                src=f"{icons}/arrow-up-right-white.svg",
                alt="Arrow right icon",
                width="16",
                height="16",
                cls="w-4 h-4",
            ),
            href=href,
            cls=f"{gap2} items-center hover:text-white border-b border-b-transparent hover:border-b-white",
            **kw,
        )
    )


def hero_section():
    return (
        Header(
            Nav(
                A(
                    Img(
                        src="/assets/logo.svg",
                        alt="FastHTML",
                        width="105",
                        height="24",
                    ),
                    href="#",
                ),
                A(
                    "LinkedIn",
                    href="https://sg.linkedin.com/in/nouman-memon-0aab3310",
                    **_blank,
                    cls=f"bg-black text-white py-2 px-4 s-body rounded-[62.5rem] hover:bg-black/80 transition-colors duration-300 px-4 py-1 h-10 {center} justify-center",
                ),
                cls=f"py-2 px-4 {between} items-center rounded-full w-full max-w-[400px] bg-white/50 backdrop-blur-lg border border-white/20",
            ),
            cls=f"fixed top-0 w-full left-0 p-4 {center} justify-center z-50",
        ),
        Section(
            Div(
                File("assets/hero-shapes.svg"),
                cls="absolute z-0 lg:-top-[15%] top-0 left-1/2 -translate-x-1/2 grid grid-cols-1 grid-rows-1 w-[120%] aspect-square max-w-[2048px] min-w-[900px]",
            ),
            Div(
                Div(cls="lg:flex-1 max-lg:basis-[152px]"),
                Div(
                    H1(description, cls="heading-1 max-w-3xl"),
                    Img(
                        src="/assets/hero_new.png",
                        alt="FastHTML",
                        width="400",
                        height="200",
                    ),
                    cls=f"flex-1 {col} items-center justify-center text-center w-full text-black",
                ),
                Div(
                    A(
                        "Lets Connect",
                        href="https://sg.linkedin.com/in/nouman-memon-0aab3310",
                        **_blank,
                        cls=f"{bnset} m-body px-4 py-1 rounded-full bg-black hover:bg-black/80 transition-colors duration-300 text-white h-[76px] w-full max-w-[350px] flex items-center justify-center",
                    ),
                    cls=f"flex-1 {center} justify-center content-center flex-wrap lg:gap-6 gap-4 m-body",
                ),
                cls=f"{col} flex-1 relative px-4 lg:px-16",
            ),
            cls=f"{col} relative w-full h-screen max-h-[1024px] min-h-[720px] overflow-hidden bg-white",
        ),
    )


def faq_item(question, answer, id):
    return accordion(
        id=id,
        question=question,
        answer=answer,
        question_cls="text-black s-body",
        answer_cls="s-body text-black/80 col-span-full",
        container_cls=f"{col} justify-between bg-soft-blue rounded-[1.25rem] {bnset}",
    )


def about_me():
    msg = "Nouman is my name and this is an example. Why do I care because I am just trying to fill in the space for styling. This is a placeholder."
    return section_wrapper(
        (
            Div(
                section_header(
                    "SOME INFORMATION ABOUT ME", "Nouman Memon [n03an]", msg
                ),
                cls="max-w-3xl w-full mx-auto flex-col items-center text-center gap-6 mb-8 lg:mb-8",
            ),
            Div(
                *[
                    faq_item(question, answer, i + 3)
                    for i, (question, answer) in enumerate(aboutme)
                ],
                cls=f"{col} w-full lg:flex-row gap-4 items-center lg:gap-8 max-w-7xl mx-auto justify-center",
            ),
        ),
        bg_color="yellow",
        flex=False,
    )


def footer():
    return Section(
        Div(
            Div(
                P("© 2024 onwards n03an.me. All rights reserved.", cls="mr-auto"),
                Nav(
                    Ul(
                        footer_link(
                            "Github",
                            "https://github.com/N0-man",
                            **_blank,
                        ),
                        footer_link(
                            "ML Notes",
                            "https://n0-man.github.io/MIT-MachineLearning-MicroMasters/INTRO.html",
                            **_blank,
                        ),
                        footer_link(
                            "Math for ML",
                            "https://n0-man.github.io/math-for-machine-learning/intro.html",
                            **_blank,
                        ),
                        cls="flex max-lg:flex-col max-lg:items-start gap-4 lg:gap-6 flex-wrap",
                    )
                ),
                cls="relative z-[1] mono-s flex max-lg:flex-col gap-6 text-white/80 px-4 lg:px-16 pb-16",
            ),
            Div(
                File("assets/footer-path.svg"),
                cls=f"relative z-0 w-full px-4 lg:px-16 pb-1 {col} flex-1 justify-end",
            ),
            cls=f"relative w-full h-[420px] lg:h-[600px] {col} pt-8 lg:pt-12 rounded-t-3xl lg:rounded-t-[2.5rem] bg-black overflow-hidden -mt-8 lg:-mt-10",
        )
    )


hdrs = [
    Meta(charset="UTF-8"),
    Meta(
        name="viewport",
        content="width=device-width, initial-scale=1.0, maximum-scale=1.0",
    ),
    Meta(name="description", content=description),
    *Favicon("favicon.ico", "favicon-dark.ico"),
    *Socials(
        title="n03an",
        description=description,
        site_name="fastht.ml",
        twitter_site="@answerdotai",
        image=f"/assets/og-sq.png",
        url="",
    ),
    # surrsrc,
    Script(src="https://cdn.jsdelivr.net/gh/gnat/surreal@main/surreal.js"),
    scopesrc,
    Link(href="css/main.css", rel="stylesheet"),
    Link(href="css/tailwind.css", rel="stylesheet"),
    Link(href="css/stack.css", rel="stylesheet"),
    Link(href="css/preview-stack.css", rel="stylesheet"),
    Link(href="css/highlighter-theme.css", rel="stylesheet"),
]

bodykw = {"class": "relative bg-black font-geist text-black/80 font-details-off"}
app, rt = fast_app(hdrs=hdrs, default_hdrs=False, bodykw=bodykw, on_startup=[startup])

scripts = (
    Script(
        src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"
    ),
    Script(
        src="https://cdnjs.cloudflare.com/ajax/libs/highlightjs-line-numbers.js/2.8.0/highlightjs-line-numbers.min.js"
    ),
)

from fastcore.xtras import timed_cache


@timed_cache(seconds=60)
async def home():
    return (
        Title(f"n03an 👋🏼 {description}"),
        Main(
            hero_section(),
            about_me(),
            footer(),
        ),
        *scripts,
    )


@rt("/")
async def get():
    return await home()


serve()
