from django.shortcuts import render
from django.http import FileResponse, HttpResponseRedirect
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code39, code128, code93, createBarcodeDrawing
from products.models import Product1
from django.urls import reverse


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

        if Product1.objects.filter(sku = sku).exists():
            product = Product1.objects.get(sku = sku)
            
        else:
            return render(request, "reports/skulabel-25x50.html",{
                'message': "SKU does not exists in database"
            })

        # Create a file-like buffer to receive PDF data.
        font_size = 20 # fro big SKU print
        font_size_barcode_caption = 9 # for caption printing belwo the barcode
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer)
        p.setPageSize((100*mm, 25*mm))
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        
        # p.rect(0*mm, 0*mm, 50*mm, 25*mm, fill=0)
        # p.rect(50*mm, 0*mm, 50*mm, 25*mm, fill=0)
        
        #point to inch to mm conversion
        # 1 pt = 1/72 inch = 0.3528 mm

        #relation between barcodewidth(total length including quiet white space) and barwidth
        #
        #barcodewidth = ((11*number of char in data + 35) * barWidth) +lquiet + rquiet
        #quiet space maximum of 0.25 inch(6.35 mm) and 10xbarwidth on one side total space is 2 times of the value

        #canvas.setFont('DarkGardenMK', 32)
        

        barcode_length = 50
        bar_width = (barcode_length-12.70)/(11*len(sku)+35)
        print(f"bar Width: -> {bar_width}")
        
        for x in range(quantity):

            #text_len = p.stringWidth(sku, "Helvetica", font_size)*0.3528
            p.setFont('Helvetica', font_size)
            text_to_print= sku
            x_coordinate = 10
            
            if p.stringWidth(text_to_print, "Helvetica", font_size)*0.3528 > 40:
                
                for i in range(len(text_to_print)):
                    if p.stringWidth(text_to_print[:i], "Helvetica", font_size)*0.3528 >= 40:
                        # save the remaining text in 2nd variable
                        text_to_print_2 = text_to_print[i:len(text_to_print)]
                        #update the first variable with text till i character
                        text_to_print = text_to_print[:i]
                        
                        print(f"Final SKU text to print: {text_to_print}")
                        break
                # print lower text first, 2nd part of the long SKU
                margin = (50 - p.stringWidth(text_to_print_2, "Helvetica", font_size)*0.3528)/2
                p.drawString(margin*mm, 6*mm, text_to_print_2)
                # change x coordinate for upper text
                x_coordinate = 14

            #print upper FIRST part of SKU now
            margin = (50 - p.stringWidth(text_to_print, "Helvetica", font_size)*0.3528)/2
                    
            p.drawString(margin*mm, x_coordinate*mm, text_to_print)

            

            
            barcode128 = code128.Code128(value=sku,barWidth = bar_width*mm , barHeight = 12*mm) # barWidth = bar_width*mm barWidth = 0.3*mm
            print(f"barcode total width : {barcode128.width*0.352778}")
            barcode128.drawOn(p, 50*mm, 11.5*mm)
            print(f"lquiet: {barcode128.lquiet*0.352778}")
            print(f"rquiet: {barcode128.rquiet*0.352778}")
            print (f"Print Area:{(barcode128.width - (barcode128.lquiet + barcode128.rquiet))*0.352778}")
            
            text_len = p.stringWidth(sku, "Helvetica", font_size_barcode_caption)*0.3528
            margin = (50-text_len)/2+ 50
            if margin <= 5:
                margin=5
            p.setFont('Helvetica', font_size_barcode_caption)
            p.drawString(margin*mm, 7.5*mm, sku)
            text_to_print = product.name
            #text_to_print = text_to_print[:25]
            for i in range(len(text_to_print)):
                if p.stringWidth(text_to_print[:i], "Helvetica", font_size_barcode_caption)*0.3528 >= 44:
                    text_to_print = text_to_print[:i]
                    print(f"Final text: {text_to_print}")
                    break
            p.drawString(52*mm, 4*mm, f"{text_to_print}..")

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