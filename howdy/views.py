from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
import requests,datetime,json, time



# from .forms import MyForm
from .forms import HomeForm

# Create your views here.
class HomePageView(TemplateView):
    template_name = "index.html"

    def get(self, request):
        form = HomeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.method == 'POST':   
            form = HomeForm(request.POST) 
            if form.is_valid():
                    symbol = form.cleaned_data['symbol']
                    symbol = symbol.upper();
                    result = ""
                    r = time.strftime("%a %b %d %T PDT %Y")
                    date = r

                    result += (r+"\n")
                    intrinio_url = "https://api.intrinio.com/companies?ticker="+symbol

                    response =requests.get(intrinio_url, auth=('af9176a39d74076b7c50c47bee130a1f', '06f61fcdae6705ce48b8d3c9e27edbae'))
                    if(response.status_code == 200):
                            result += (response.json().get('name')+" ({})\n").format(symbol)
                            company_name = (response.json().get('name')+" ({})\n").format(symbol)


                    else:
                            print("Symbol is not valid or API - %s does not identify this symbol !!!"%(intrinio_url))
                    # except Exception as e:
                    #     print("Could not retrieve company name as server is not responding, try again late !!! \n\n ")
                    #     result += (" ({})\n").format(symbol)

                    url_alpha = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey=8UWFH5V3AXJ1P5OX".format(symbol)

                    stock_response =requests.get(url_alpha)
                    if(stock_response.status_code == 200):
                            data = stock_response.json()
                            stock_keys = list(data.keys())
                            stock_data = data.get(stock_keys[1])
                            stock_price_keys = list(stock_data.keys())
                            stock_price_var_keys = list(stock_data.get(stock_price_keys[0]).keys())
                            current_price = float(stock_data.get(stock_price_keys[0]).get(stock_price_var_keys[3]))
                            previous_price = float(stock_data.get(stock_price_keys[1]).get(stock_price_var_keys[3]))
                            price_str = "%.2f "%(current_price)

                            price_diff = current_price - previous_price
                            if(price_diff < 0):
                                    price_str += " %.2f (-"%(price_diff);
                            else:
                                    price_str += " +%.2f (+"%(price_diff);
                            percentage = (abs(price_diff)/current_price)*100
                            price_str += "%.2f%s)"%(percentage,"%");
                            price_string = price_str
                            result +=price_str
                            args = {'date': date, 'company_name': company_name, 'price_string': price_string}

                    return render(request, "result.html", args)