from django.shortcuts import render
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code39, code128, code93, createBarcodeDrawing


import io

# Create your views here.
def index(request):
    return render(request, "reports/index.html")


def sku_label_25x50(request):
    if request.method == "POST":
        from reportlab.lib.units import mm
        from reportlab.lib.colors import pink, black, red, blue, green
        # Get Data from post request
        sku = request.POST['sku']
        quantity = int(request.POST['quantity'])

        # Create a file-like buffer to receive PDF data.
        font_size = 17
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer)
        p.setPageSize((100*mm, 25*mm))
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.setFont('Helvetica', font_size)
        
        #point to inch to mm conversion
        # 1 pt = 1/72 inch = 0.03528 mm

        #relation between barcodewidth(total length including quiet white space) and barwidth
        #
        #barcodewidth = ((11*number of char in data + 35) * barWidth) +lquiet + rquiet
        #quiet space maximum of 0.25 inch(6.35 mm) and 10xbarwidth on one side total space is 2 times of the value

        #canvas.setFont('DarkGardenMK', 32)
        text_len = p.stringWidth(sku, "Helvetica", font_size)*0.352778
        print(text_len)
        #text_len=text_len*0.352778
        margin = (50-text_len)/2
        if margin <= 5:
            margin=5

        barcode_length = 50
        #bar_width = len(sku)*0.015 
        #bar_width = ((-0.03818)*(len(sku))-1)+0.18
        #bar_width = ((-0.03818)*len(sku)) + 0.698
        #bar_width = 0.29*mm
        bar_width = (barcode_length-12.70)/(11*len(sku)+35)
        print(f"bar Width: -> {bar_width}")
        
        for x in range(quantity):
            p.drawString(margin*mm, 12.5*mm, sku)
            
            barcode128 = code128.Code128(value=sku,barWidth = bar_width*mm , barHeight = 12*mm) # barWidth = bar_width*mm barWidth = 0.3*mm
            print(f"barcode total width : {barcode128.width*0.352778}")
            barcode128.drawOn(p, 45*mm, 3*mm)
            print(f"lquiet: {barcode128.lquiet*0.352778}")
            print(f"rquiet: {barcode128.rquiet*0.352778}")
            print (f"Print Area:{(barcode128.width - (barcode128.lquiet + barcode128.rquiet))*0.352778}")
            

            p.showPage()
            
        # p.setStrokeColor(red)
        #p.grid([10*mm,20*mm, 30*mm, 40*mm], [145*mm,150*mm, 165*mm, 290*mm])
        # Close the PDF object cleanly, and we're done.
        
        #canvas.rect(x, y, width, height, stroke=1, fill=0) 
        # p.setFont("Times-Roman", 20)
        # p.drawString(105*mm, 148*mm,"TEXT  CHECK" )
        # p.rect(50,50,20,70)
        # p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f"{sku}.pdf")


    return render(request, 'reports/skulabel-25x50.html')