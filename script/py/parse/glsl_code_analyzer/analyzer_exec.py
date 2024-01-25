jsonOP = parent.Analyzer.op("Analyzer_Result")


def run():
    print("Analyzer: Started")
    result = parent.Analyzer.Send_to_textDAT(jsonOP)
    print("Analyzer: Finished")
    return result
