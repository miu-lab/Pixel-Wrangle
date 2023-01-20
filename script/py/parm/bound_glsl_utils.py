from _stubs import *
from re import findall

## CUSTOM FUNCTIONS ##


def getUntouched(refTable, offset):
    result = []
    for row in refTable.rows():
        val = row[0].val
        digit = int(findall(r'\d+', val)[0])
        if digit < offset:
            result.append(val)
    return result


def resetParms(refTable, targetGLSL, offset):
    untouched = getUntouched(refTable, offset)
    for row in refTable.rows():
        if row[0].val not in untouched:
            p = targetGLSL.par[row[0].val]
            p.bindExpr = ''
            p.expr = ''
            p.mode = ParMode.CONSTANT
            if p.style in ["SOP", "PanelCOMP", "Python", "TOP", "MAT", "COMP", "CHOP", "File", "Folder", "Str", "StrMenu"]:
                p.val = ""
            else:
                p.val = 0


def getCellValue(dat, row, search, refRow=0):
    return row[dat.findCell(search, rows=[refRow]).col].val


def getParGroups(parmList, namesRow, selectedColName='pargroup'):
    if type(selectedColName) == int:
        rmDouble = dict((k[selectedColName].val, v)
                        for v, k in enumerate(reversed(parmList)))
    elif type(selectedColName) == str:
        index = [name.val for name in namesRow].index(selectedColName)
        selectedColName = index
        rmDouble = dict((k[selectedColName].val, v)
                        for v, k in enumerate(reversed(parmList)))
    sortedKeys = sorted(rmDouble, key=rmDouble.get, reverse=True)
    result = []
    for pGroupName in sortedKeys:
        parGroup = []
        for p in parmList:
            if p[selectedColName].val == pGroupName:
                parGroup.append(p)
        result.append(parGroup)
    return result
