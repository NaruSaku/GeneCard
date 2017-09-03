import xlwt

book = xlwt.Workbook(encoding="utf-8", style_compression=0)
sheet = book.add_sheet('1a', )
sheet.write(0,1,'shit')
book.save("e:/shit.xls")