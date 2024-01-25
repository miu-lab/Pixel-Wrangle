from re import match

types = (
    "float",
    "double",
    "int",
    "bool",
    "vec2",
    "vec3",
    "vec4",
    "uvec2",
    "uvec3",
    "uvec4",
    "ivec2",
    "ivec3",
    "ivec4",
    "bvec2",
    "bvec3",
    "bvec4",
    "mat2",
    "mat3",
    "mat4",
)

variantn = op("Variants")
descriptionn = op("Description")


def onTableChange(dat):
    text = dat.text
    start = text.find("/*") + 2
    end = text.find("*/")
    variantn.clear()
    descriptionn.clear()

    if start + end > -1:
        descriptionn.write("/*\n\n" + text[start:end].strip() + "\n\n*/")
        for line in text.split("\n"):
            if line.startswith(types) or match("^[\w]+\s.*", line):
                variantn.write(line.split("{")[0].strip() + "\n\n")

    return
