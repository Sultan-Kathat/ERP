from products.models import Product1
from django.shortcuts import render

# Create your views here.
def index(request):
    if request.method=="POST":
        email = request.POST["email"]
        password = request.POST["pswd"]
        return render(request, "products/index.html",{
            "email": email
        })
    return render(request, "products/index.html")


def upload(request):
    if request.method == "POST":
        txt_file = request.FILES["file"]
        # used 'utf-8-sig' because without it it was showing "\ufeff" in start of first line
        file_data = txt_file.read().decode("utf-8-sig")
        # remove the header line from the data
        lines = file_data.split("\n")
        print(lines)
        lines.pop(0)
        for line in lines:
            data = line.split("\t")
            print(data)
            #print(len(data))
            if len(data) >1:
                if Product1.objects.filter(sku = data[0]).exists():
                    pass
                    #print(f"already have this sku: {data[0]}")
                else:
                    # check id list is not empty as sometime last list might be empty
                    
                    p = Product1(sku = data[0], name = data[2], tax_code = 18)
                    p.save()
            else:
                print("USER Error: there is no data in list, it might be the last empty list")
        #print(lines)
        return render(request, "products/upload.html",{
            "alert_message": "File uploaded Sucessfully"
        })

    return render(request, 'products/upload.html')

def show(request, page_id):
    number_of_record = Product1.objects.all().count()
    print(int(number_of_record/50))

    start = (page_id*50)-50
    end = page_id*50

    return render(request, "products/show.html",{
        "page_id":page_id,
        "products": Product1.objects.all().order_by('id')[start:end],
        "pages": int(number_of_record/50)+1
    })