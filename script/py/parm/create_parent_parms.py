from _stubs import *
from re import sub
from ast import literal_eval
from TDFunctions import getCustomPage
from TDJSON import addParameterFromJSONDict, parameterToJSONPar, pageToJSONDict


# CUSTOM FUNCTIONS


def addParFromJSON(target, src, replace=True, setValues=True, ignoreAttrErrors=True, fixParNames=False, setBuiltIns=False):
    return addParameterFromJSONDict(target, src, replace, setValues,
                                 ignoreAttrErrors, fixParNames, setBuiltIns)

def updateParm(src: dict, pNames, JSONpage):
    updatedPage = JSONpage

    if src["name"] in updatedPage:

        # Delete unused
        if src["name"] not in pNames:
            p = parent.Comp.parGroup[src["name"]]
            p.destroy()
            updatedPage.pop(src["name"])

        else:
            oldp = updatedPage[src["name"]]
            for key in list(oldp.keys()):
                if key not in ['val', 'expr', 'bindExpr', 'style', 'page', 'name']:
                    del oldp[key]
            oldp['defaultExpr'] = ''
            oldp = {**src,**oldp}

            addParFromJSON(parent.Comp, oldp)

    else:
        addParFromJSON(parent.Comp, src)

# OPERATORS
source = op('BUILTIN_PARMS')
target = parent.Comp
page = None

StringTypes = ("SOP", "PanelCOMP", "Python", "TOP", "MAT",
               "COMP", "CHOP", "File", "Folder", "Str", "StrMenu")


def onTableChange(dat: DAT):
    page = None
    pageJSONDict = {}

    # GET TARGET PAGE
    page = getCustomPage(target, 'Controls') or target.appendCustomPage('Controls')
    pageJSONDict = pageToJSONDict(page, extraAttrs='*', forceAttrLists=True)

    # SORT PAGES
    target.sortCustomPages('Controls', 'Code', 'Inputs',
                           'Outputs', 'GLSL', 'Globals')
    # GET ALL DECLARED PARMS
    plist = dat.rows()

    # REMOVE HEADERS
    plist.pop(0)

    pNames = [dat[i+1, "name"].val for i, _ in enumerate(plist)]
    # GET CURRENT UI PARMS
    curPars = page.pars

    # CLEAN OLD
    for curP in curPars:
        if curP.valid and curP.name not in pNames:
            curP.destroy()

    # FOR EACH DECLARED PARMS
    for index, _ in enumerate(plist):

        # STARTING AT ROW 1
        i = index+1

        # IF MIN MAX EXISI CAST IT TO FLOAT
        min = float(dat[i, 'min'].val if dat[i, 'min'].val != "None" else "0")
        max = float(dat[i, 'max'].val if dat[i, 'max'].val != "None" else "1")
        # GET DEFAULT STRING PATTERN
        default = dat[i, 'default'].val

        # IS AN ARRAY
        array = int(dat[i, 'array'].val)

        # BUILD STRING LIST FROM MENU RAW STRING IF EXIST, ELSE SET MENU TO EMPTY STRING
        menu = []

        try:
            # If menu prop exist, parse to list of string
            if dat[i, 'menu'].valid:
                menu = [str(x) for x in literal_eval(dat[i, 'menu'].val)]
            else:
                menu = ""
        except:
            menu = ""

        # Vector default string to list
        if dat[i, 'ptype'].val.find("vec") != -1:
            default = [float(x) for x in literal_eval(default)]
        # IF OP / STRING TYPE, GET CORRESPONFING KEY
        if dat[i, 'style'].val.startswith(StringTypes):
            tarKey = dat[i, 'style'].val.lower()
            if dat[i, tarKey].val == "None":
                default = ""
        pmode = ParMode.CONSTANT

        if dat[i, 'expr'].val != "None":
            pmode = ParMode.EXPRESSION

        if dat[i, 'bindExpr'].val != "None":
            pmode = ParMode.BIND

        # SET PARAMETER SETTINGS

        pSettings = {

            "name": dat[i, 'name'].val,
            "mode" : pmode,
            "label": dat[i, 'label'].val,
            "order": int(dat[i, 'order'].val),
            "startSection": int(dat[i, 'section'].val) if dat[i, 'section'].val != "None" else 0,
            "readOnly": int(dat[i, 'readonly'].val) if dat[i, 'readonly'].val != "None" else 0,
            "help": dat[i, 'help'].val if dat[i, 'help'].val != "None" else "",

            "page": "Controls",
            "style": dat[i, 'style'].val if dat[i, 'style'].val != "None" else "Float",
            "menuNames": [sub(r'\W+|^(?=\d)', '_', x.lower()) for x in menu],
            "menuLabels": menu,

            "type": dat[i, 'ptype'].val,
            "vtype": dat[i, 'vtype'].val,
            "array": array,
            "arraytype": dat[i, 'arraytype'].val.lower() if array == 1 else "",
            "size": int(dat[i, 'typesize'].val),

            "enableExpr": dat[i, 'enableExpr'].val if dat[i, 'enableExpr'].val != "None" else "",
            "expr": f"{dat[i, 'expr'].val}" if dat[i, 'expr'].val != "None" else "",
            "bindExpr": dat[i, 'bindExpr'].val if dat[i, 'bindExpr'].val != "None" else "",

            "min": min,
            "max": max,
            "normMin": min,
            "normMax": max,
            "default": default,
            "val": default,

        }

        # UPDATE PARAMETER UI
        updateParm(pSettings, pNames, pageJSONDict)
        # [TD BUG] Restore Parameter Mode
        parent.Comp.parGroup[pSettings['name']].mode = pmode

    return
