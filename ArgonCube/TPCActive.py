
TPCActiveCenter = {
        '00':[-487.949,-218.236,-335.],
        '01':[-182.051,-218.236,-335.],
        '10':[182.051,-218.236,-335.],
        '11':[487.949,-218.236,-335.],
        '20':[-487.949,-218.236,335.],
        '21':[-182.051,-218.236,335.],
        '30':[182.051,-218.236,335.],
        '31':[487.949,-218.236,335.],
        }

TPCActiveID = {
        '00':0,
        '01':1,
        '10':2,
        '11':3,
        '20':4,
        '21':5,
        '30':6,
        '31':7
        }

def GetTPCActiveCenter(module_copynumber,halfDetector_copynumber):
    return TPCActiveCenter[str(module_copynumber)+str(halfDetector_copynumber)]

def GetTPCActiveID(module_copynumber,halfDetector_copynumber):
    return TPCActiveID[str(module_copynumber)+str(halfDetector_copynumber)]

