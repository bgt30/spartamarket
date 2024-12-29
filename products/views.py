from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Hashtag
from .forms import ProductForm
from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def product_list(request):
    sort = request.GET.get('sort', '-created_at')
    query = request.GET.get('q', '')
    
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) |  # 제목 검색
            Q(description__icontains=query) |  # 설명 검색
            Q(owner__username__icontains=query) |  # 작성자 검색
            Q(hashtags__name__icontains=query)  # 해시태그 검색
        ).distinct()
    else:
        products = Product.objects.all()
    
    if sort == 'popular':
        products = products.annotate(
            like_count=models.Count('likes')
        ).order_by('-like_count', '-created_at')
    else:
        products = products.order_by('-created_at')
    
    context = {
        'products': products,
        'current_sort': sort,
        'query': query,
    }
    return render(request, 'products/product_list.html', context)

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.view_count += 1  # 조회수 증가
    product.save()
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            
            # 해시태그 처리
            hashtag_text = form.cleaned_data.get('hashtags', '')
            if hashtag_text:
                hashtags = [tag.strip() for tag in hashtag_text.split(',') if tag.strip()]
                for tag_name in hashtags:
                    tag, created = Hashtag.objects.get_or_create(name=tag_name)
                    product.hashtags.add(tag)
            
            return redirect('products:product_detail', product_id=product.id)
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

@login_required
def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id, owner=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            
            # 기존 해시태그 제거
            product.hashtags.clear()
            
            # 새 해시태그 추가
            hashtag_text = form.cleaned_data.get('hashtags', '')
            if hashtag_text:
                hashtags = [tag.strip() for tag in hashtag_text.split(',') if tag.strip()]
                for tag_name in hashtags:
                    tag, created = Hashtag.objects.get_or_create(name=tag_name)
                    product.hashtags.add(tag)
            
            return redirect('products:product_detail', product_id=product.id)
    else:
        initial_hashtags = ','.join([tag.name for tag in product.hashtags.all()])
        form = ProductForm(instance=product, initial={'hashtags': initial_hashtags})
    return render(request, 'products/product_form.html', {'form': form})

@login_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id, owner=request.user)
    if request.method == 'POST':
        product.delete()
        return redirect('products:product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})

@login_required
def product_like(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user in product.likes.all():
        product.likes.remove(request.user)
    else:
        product.likes.add(request.user)
    return redirect('products:product_detail', product_id=product.id)

