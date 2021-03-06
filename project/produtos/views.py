from django.shortcuts import render, redirect
from .models import Produto, Esqueleto
from .forms import ProductForm
import requests
from bs4 import BeautifulSoup

# Create your views here.

def list_products(request):
    form = ProductForm(request.POST or None)

    if form.is_valid():
        data = request.POST.copy()
        titulo = data.get('titulo')
        return redirect('find_products/'+ titulo)


    return render(request, 'produtos.html', {'form': form})


def find_products(request, nome):
    headerss = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    url = 'https://busca.magazineluiza.com.br/busca?q=' + nome


    response = requests.get(url, headers=headerss)

    print(response.text)

    soup = BeautifulSoup(response.content, features="lxml")

    l = soup.find_all('li', class_="nm-product-item")

    lista = []

    for list in l:
        
        

        titulo = list.a.get('title')
        if titulo == '':
            titulo = list.span.get_text()


        url = list.a.get('href')
        if url == '':
            url = list.span.get_text()

        produto1 = Esqueleto(titulo, url, "")
        lista.append(produto1)



    ##img = l[0].a.div.div

    ##nm-product-img-link

    print("---------------------")
    for produto in lista:
        print(produto.titulo)
        print(produto.link)
        print("\n")  
    print("---------------------")


    return render(request, 'produtosFiltrados.html', {'lista': lista})