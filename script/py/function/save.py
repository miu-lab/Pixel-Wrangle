import contextlib

from pathlib import Path, PurePosixPath


def onSelect(info):
    if info["button"] != "Save":
        return
    name = str(PurePosixPath(info["enteredText"]).name)
    path = parent.Comp.par.Codeuserfunctionpath
    relpath = ""

    with contextlib.suppress(Exception):
        relpath = op("SAVE_TO_PATH")[1, "relpath"].val
        path = f"{path}/{relpath}"
    if "/" in str(PurePosixPath(info["enteredText"])):
        folder = PurePosixPath(f"{path}/{PurePosixPath(info['enteredText'])}").parent
        Path(str(folder)).mkdir(parents=True, exist_ok=True)
        path = folder

    with open(f"{path}/{name}.glsl", "w") as f:
        f.write(op("FUNCTION_OUT").text)
