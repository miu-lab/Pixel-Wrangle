from re import sub
from _stubs import *
from json import dumps
from pprint import pprint
from inspect import cleandoc
from pydoc import locate
from ast import literal_eval
import string

# Corresponding table of declared types vs ParmTypes
validTypePattern = {"//---": "header",
                    "//str:": "str",
                    "//op:": "op",
                    "//chop:": "chop",
                    "//top:": "top",
                    "//mat:": "mat",
                    "//comp:": "comp",
                    "//file:": "file",
                    "//folder:": "folder",
                    "float": "float",
                    "int": "int",
                    "uint": "int",
                    "atomic_uint": "int",
                    "bool": "int",
                    "vec2": "vec2",
                    "vec3": "vec3",
                    "vec4": "vec4",
                    "ivec2": "ivec2",
                    "ivec3": "ivec3",
                    "ivec4": "ivec4",
                    "uvec2": "ivec2",
                    "uvec3": "ivec3",
                    "uvec4": "ivec4",
                    "bvec2": "ivec2",
                    "bvec3": "ivec3",
                    "bvec4": "ivec4",
                    "mat2": "chop",
                    "mat3": "chop",
                    "mat4": "chop",
                    }

# Props and target types
commonProps = {
    "ptype":        {"type": str,  "default": "float"},
    "vtype":        {"type": str,  "default": "float"},
    "gltype":       {"type": str,  "default": "uni"},
    "array":        {"type": int,  "default": 0},
    "arraytype":    {"type": str,  "default": "uniformarray"},
    "arraysamples": {"type": int,  "default": 0},
    "acinittype":   {"type": int,  "default": "0"},
    "acinitval":    {"type": str,  "default": "val"},
    "typesize":     {"type": int,  "default": 1},
    "label":        {"type": str,  "default": "Header"},
    "section":      {"type": int,  "default": 0},
    "order":        {"type": int,  "default": 0},
    "readonly":     {"type": int,  "default": 0},
    "enable":       {"type": int,  "default": 1},
    "enableExpr":   {"type": str,  "default": ""},
    "help":         {"type": str,  "default": ""},
    "style":         {"type": str, "default": "Float"}
}

pythonProps = {
    "expr":         {"type": str, "default": ""},
    "bindExpr":     {"type": str, "default": ""}
}

numberProps = {
    "chop":         {"type": str, "default": ""},
    "min":          {"type": float, "default": 0},
    "max":          {"type": float, "default": 1},
    "default":      {"type": float,  "default": 0}
}

toggleProps = {
    "menu":         {"type": list, "default": ""},
    "toggle":       {"type": int,  "default": 0},
    "pulse":        {"type": int,  "default": 0}
}

matrixProps = {
    "chop":         {"type": str, "default": ""},
}

stringProps = {
    "file":         {"type": str, "default": ""},
    "folder":       {"type": str, "default": ""},
    "str":          {"type": str, "default": ""},
    "strmenu":      {"type": str, "default": ""},
    "python":       {"type": str, "default": ""},
    "comp":         {"type": str, "default": ""},
    "object":       {"type": str, "default": ""},
    "panelcomp":    {"type": str, "default": ""},
    "op":           {"type": str, "default": ""},
    "top":          {"type": str, "default": ""},
    "chop":         {"type": str, "default": ""},
    "dat":          {"type": str, "default": ""},
    "mat":          {"type": str, "default": ""}
}

allProps = {**commonProps, **pythonProps, **numberProps,
            **toggleProps, **matrixProps, **stringProps}


def getParmList(dat: DAT):

    # Init
    rawText = None
    rawLines = []

    # DAT is a scriptDAT type (multi inputs)
    if dat.type == "script":
        rawText = dat.inputs[0].text

    # DAT is standard DAT
    else:
        rawText = dat.text

    # Split lines and write out to result
    rawLines = removeEmpty(rawText.splitlines())
    result = setParmProps(rawLines)

    return result


def setParmProps(stringList: str):
    result = []
    # For each line
    for line in stringList:

        # Get orignal line number
        id = line["id"]
        # Get original text line
        text = line["text"]
        # Get Parameter type
        parmTypeItem = checkParmType(text)

        parmVTypeName = parmTypeItem[0]
        parmTypeName = parmTypeItem[1]
        # Is a constant parameter ?
        parmIsConst = text.startswith("const")
        # Props of corresponding type
        parmTypeAvailableProps = getAvailablePropsOfParmType(parmTypeName)
        parmFullName = ""
        parmName = parmFullName

        # IF HEADER PARM
        if parmTypeName == "header":
            parmGLtypeName = "None"
            # Set default Header Name
            parmFullName = f"UntitledHeader{id}"
            parmName = cleanName(parmFullName)
            # Get individual key/value pair ["key=value"]
            specifiedProps = cleanStrProps(text, True)

        # IF CONST PARM
        elif parmIsConst:

            # Get name
            parmFullName = text.split(";")[0].split(" ")[2].split("=")[0]
            parmName = cleanName(parmFullName).rstrip(string.digits)
            parmGLtypeName = "const"
            # Get property list as string
            propList = text.split(";", 1)
            # Remove spaces
            specifiedProps = propList[1]
            # Get individual key/value pair ["key=value"] if specified props
            if "//" in specifiedProps:
                specifiedProps = cleanStrProps(specifiedProps)
            else:
                specifiedProps = []

        # IF ARRAY
        elif text.split(";")[0].split(" ")[1].endswith("]"):

            # Get name
            parmFullName = text.split(";")[0].split(" ")[1]
            parmName = cleanName(parmFullName.split("[")[0])
            parmGLtypeName = "chop"
            # Get property list as string
            propList = text.split(";", 1)
            # Remove spaces
            specifiedProps = propList[1]
            # Get individual key/value pair ["key=value"] if specified props
            if "//" in specifiedProps:
                specifiedProps = cleanStrProps(specifiedProps)

            else:
                specifiedProps = []

        # IF NORMAL PARM
        else:

            # Get name
            parmFullName = text.split(";")[0].split(" ")[1]
            parmName = cleanName(parmFullName)
            parmGLtypeName = "None"
            if parmVTypeName.startswith("atomic"):
                parmGLtypeName = "ac"
            if parmVTypeName.startswith("mat"):
                parmGLtypeName = "mat"

            # Get property list as string
            propList = text.split(";", 1)
            # Remove spaces
            specifiedProps = propList[1]
            # Get individual key/value pair ["key=value"] if specified props
            if "//" in specifiedProps:
                specifiedProps = cleanStrProps(specifiedProps)
            else:
                specifiedProps = []

        parmProps = setProps(id, parmFullName, parmName, parmTypeName, parmVTypeName, parmGLtypeName,
                             specifiedProps, parmTypeAvailableProps, allProps)
        result.append(parmProps)

    return result


def cleanName(strName):
    # Replace non compatible chars by _, make lowercase and capitalize first letter
    return sub(r'\W+|^(?=\d)', '', strName).lower().capitalize()


def cleanStrProps(strProp, ISCOMMENTLINEPARM=False):

    # Leave spaces in str properties
    preservedSpaceProps = ("help", "label", "expr", "bindExpr", "enableExpr")

    # GLSL compatible parm
    if not ISCOMMENTLINEPARM:
        prop = [x.strip() for x in strProp.split("//")[1].split(";")]

    # other parm types
    else:
        prop = [x.strip() for x in strProp.split("//---")[1].split(";")]

    # Conditionnal remove space
    prop = [x.translate(
        str.maketrans('', '', string.whitespace)) if not x.startswith(preservedSpaceProps) else x for x in prop]

    return prop


def checkParmType(line: str):
    # Remove All spaces
    currentLine = line.translate(
        str.maketrans('', '', string.whitespace))

    # Remove Start and split each specified prop
    specifiedProps = currentLine.split(";")

    # If const offset string check after const keyword and check type
    if specifiedProps[0].startswith("const"):
        for key, value in validTypePattern.items():
            if specifiedProps[0].startswith(key, len("const"), len(key) + len("const")):
                return [key, value]

    # Else check type
    else:
        for key, value in validTypePattern.items():
            if specifiedProps[0].startswith(key, 0, len(key)):
                return [key, value]


def getAvailablePropsOfParmType(parmType):

    # Set common properties
    parmTypeAvailableProps = {**commonProps}

    # Simple integers, menu, toggle parm types
    if parmType in ["int"]:
        return {
            **commonProps,
            **numberProps,
            **toggleProps,
            **pythonProps
        }

    # Float and vectors parm types
    elif parmType in [
        "float",
        "vec2", "vec3", "vec4",
        "ivec2", "ivec3", "ivec4",
        "uvec2", "uvec3", "uvec4",
        "bvec2", "bvec3", "bvec4",
    ]:
        return {
            **commonProps,
            **numberProps,
            **pythonProps
        }

    # OP, files and strings parm types
    elif parmType in ["chop"]:
        return {
            **commonProps,
            **matrixProps,
            **pythonProps
        }

    else:
        return parmTypeAvailableProps


def removeEmpty(stringList: str):

    # Init
    result = []

    for i, line in enumerate(stringList):

        # String is empty
        if len(line) < 1:
            continue

        # String is comment
        elif line.strip().startswith(("//", "/*")) and not line.strip().startswith("//---"):
            continue

        # String is valid
        else:
            result.append({"text": line, "id": i+1})

    return result


def setProps(id, parmFullName: str, parmName: str, parmTypeName: str, parmVTypeName: str, parmGLTypeName: str, specifiedProps, parmTypeAvailableProps, parmAllProps):

    # INITIAL PARAMETER SETTINGS
    parmFinalName = parmName

    parmAllKeysDefault = {x[0]: x[1]["default"] for x in parmAllProps.items()}

    parmKeysVals = {}

    parmKeysVals["ptype"] = parmTypeName
    parmKeysVals["vtype"] = parmVTypeName
    parmKeysVals["gltype"] = parmGLTypeName
    parmKeysVals["order"] = id
    parmKeysVals["label"] = parmFullName
    parmKeysVals["style"] = "Float"
    parmKeysVals['typesize'] = 1

    # Array Type
    if parmFullName.endswith("]"):
        parmKeysVals["ptype"] = "chop"
        parmKeysVals["label"] = parmFinalName
        parmKeysVals["array"] = 1
        arraySamples = int(parmFullName.split('[')[1].split("]")[0])
        parmKeysVals["arraysamples"] = arraySamples
        parmKeysVals["style"] = "CHOP"

    else:
        parmKeysVals["array"] = 0
        parmKeysVals["arraysamples"] = None
        parmKeysVals["arraytype"] = None

    # Vector Types
    if "vec" in parmTypeName:
        parmKeysVals["typesize"] = int(parmTypeName[-1])
        parmKeysVals["default"] = [
            float(parmAllKeysDefault["default"])] * parmKeysVals["typesize"]
        if parmKeysVals["typesize"] == 3:
            parmKeysVals["style"] = "RGB"
        elif parmKeysVals["typesize"] == 4:
            parmKeysVals["style"] = "RGBA"

    # Int types
    if parmTypeName.startswith(("int", "ivec", "bvec", "uvec")):
        parmKeysVals["style"] = "Int"

    # Matrix types
    if parmVTypeName.startswith("mat"):
        parmKeysVals["style"] = "CHOP"

    # Atomic types
    if parmGLTypeName != "ac":
        parmKeysVals["acinitval"] = None
        parmKeysVals["acinittype"] = None

    # OVERRIDE PROPERTIES
    # FOR EACH SPECIFIED PROPS
    for currentProp in specifiedProps:
        # Try splitting property name and property value
        try:
            propRaw = currentProp.split("=")
            propName = propRaw[0]
            propVal = propRaw[1]
            isValidPropName = None

        # Break if list is empty
        except:
            continue

        ## CHECK PROPERTY NAME ##
        # Try access current property from available properties dict
        try:
            isValidPropName = True
            targetProp = parmTypeAvailableProps[propName]

        # Else display detailed error
        except:
            isValidPropName = False
            error = cleandoc(
                f"""

                =================================
                LINE {id} -> Property Error on "{parmFullName}" 
                =================================
                The '{propName}' property does not exist on {parmTypeName.capitalize()} ParmType
                This property will be ignore
                """)

            print(error)
            continue

        ## CHECK PROPERTY VALUE ##
        # If specified property has a valid name
        if isValidPropName:
            targetPropTypeName = targetProp["type"].__name__

            if propName == 'menu':
                propVal = [str(x) for x in literal_eval(propVal)]
                parmKeysVals[propName] = propVal
                parmKeysVals["style"] = "Menu"

            elif parmTypeName == "header" and propName == "label":
                parmFinalName = cleanName(f"h{propVal}").lower().capitalize()
                parmKeysVals[propName] = propVal
                parmKeysVals["style"] = "Header"

            elif propName == 'default':
                if parmKeysVals['typesize'] > 1:
                    try:
                        propVal = [float(x) for x in literal_eval(propVal)]
                        parmKeysVals[propName] = propVal
                    except:
                        try:
                            propVal = [float(propVal)] * \
                                parmKeysVals["typesize"]
                            parmKeysVals[propName] = propVal
                        except:
                            propVal = [
                                float(parmAllKeysDefault["default"])] * parmKeysVals["typesize"]
                            parmKeysVals[propName] = propVal
                else:
                    try:
                        parmKeysVals[propName] = propVal
                    except:
                        parmKeysVals[propName] = float(
                            parmAllKeysDefault["default"])

            elif parmKeysVals["array"] == 1 and propName == 'arraytype':
                parmKeysVals["arraytype"] = cleanName(propVal).lower()

            elif propName in ["op", "top", "file", "folder", "dat", "mat", "chop", "comp"] and parmKeysVals['style'].startswith(("SOP", "PanelCOMP", "Python", "TOP", "MAT", "COMP", "CHOP", "File", "Folder", "Str", "StrMenu")):
                    key = parmKeysVals['style'].lower()
                    parmKeysVals[key] = propVal
                    parmKeysVals['default'] = propVal

                

            elif propName == 'acinitval' and propVal == 'chop':
                parmKeysVals["style"] = "CHOP"
                parmKeysVals[propName] = propVal

            else:
                try:
                    c = locate(targetPropTypeName)
                    propVal = c(propVal)
                    parmKeysVals[propName] = propVal

                # Else display detailed error
                except:
                    error = cleandoc(
                        f"""

                        =================================
                        LINE {id} -> Value Error on "{parmFullName}"
                        =================================
                        The '{propVal}' value on '{propName}' property is wrong type
                        Expected type is {targetProp['type'].__name__}
                        This value will be reset to default : {targetProp['default']}
                        """)

                    print(error)
                    continue

    return {parmFinalName: {**parmAllKeysDefault, **parmKeysVals}}
