
import io_parserExt as parse
from pprint import pprint

def onTableChange(dat):
	code = dat.text
	analyzer = parse.GLSLCodeAnalyzer(code)
	variables = analyzer.Run()
	# [print(x) for x in variables]
	return
