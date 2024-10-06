from fasthtml.common import *

icons = "assets/icons"
gap2 = "flex gap-2"
col = "flex flex-col"
center = "flex items-center"
between = "flex justify-between"
inset = "shadow-[0_2px_2px_rgba(255,255,255,0.5),0_3px_3px_rgba(0,0,0,0.2)]"
bnset = "shadow-[inset_0_2px_4px_rgba(255,255,255,0.1),0_4px_8px_rgba(0,0,0,0.5)]"
section_base1 = "pt-8 px-4 pb-24 gap-8 lg:gap-16 lg:pt-16 lg:px-16"
section_base = f"{col} {section_base1}"


def maxpx(px):
    return f"w-full max-w-[{px}px]"


def maxrem(rem):
    return f"w-full max-w-[{rem}rem]"


def section_wrapper(content, bg_color, xtra="", flex=True):
    return Section(
        content,
        cls=f"bg-{bg_color} {section_base1} {col if flex else ''} -mt-8 lg:-mt-16 items-center rounded-t-3xl lg:rounded-t-[2.5rem] relative {xtra}",
    )


def section_header(mono_text, heading, subheading, max_width=32, center=True):
    pos = "items-center text-center" if center else "items-start text-start"
    return Div(
        P(mono_text, cls="mono-body text-opacity-60"),
        H2(heading, cls=f"text-black heading-2 {maxrem(max_width)}"),
        P(subheading, cls=f"l-body {maxrem(max_width)}"),
        cls=f"{maxrem(50)} mx-auto {col} {pos} gap-6",
    )


def accordion(id, question, answer, question_cls="", answer_cls="", container_cls=""):
    return Div(
        Input(
            id=f"collapsible-{id}",
            type="checkbox",
            cls=f"collapsible-checkbox peer/collapsible hidden",
        ),
        Label(
            P(question, cls=f"flex-grow {question_cls}"),
            Img(src=f"{icons}/plus-icon.svg", alt="Expand", cls=f"plus-icon w-6 h-6"),
            Img(
                src=f"{icons}/minus-icon.svg", alt="Collapse", cls=f"minus-icon w-6 h-6"
            ),
            _for=f"collapsible-{id}",
            cls="flex items-center cursor-pointer py-4 lg:py-6 pl-6 lg:pl-8 pr-4 lg:pr-6",
        ),
        P(
            answer,
            cls=f"overflow-hidden max-h-0 pl-6 lg:pl-8 pr-4 lg:pr-6 peer-checked/collapsible:max-h-[30rem] peer-checked/collapsible:pb-4 peer-checked/collapsible:lg:pb-6 transition-all duration-300 ease-in-out {answer_cls}",
        ),
        cls=container_cls,
    )
