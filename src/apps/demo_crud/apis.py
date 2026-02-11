from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from django_starter_core.http.response import responses

from .models import Item
from .schemas import ItemIn, ItemOut

router = Router(tags=['demo_crud'])


@router.post('/', response=ItemOut, summary="创建商品")
def create_item(request, payload: ItemIn):
    item = Item.objects.create(**payload.dict())
    return item


@router.get('/{item_id}', response=ItemOut, summary="获取商品详情")
def get_item(request, item_id: int):
    item = get_object_or_404(Item, id=item_id)
    return item


@router.get('/', response=List[ItemOut], summary="获取商品列表")
@paginate
def list_items(request, keyword: str = Query(None, description="搜索关键词")):
    qs = Item.objects.all()
    if keyword:
        qs = qs.filter(name__icontains=keyword)
    return qs


@router.put('/{item_id}', response=ItemOut, summary="更新商品")
def update_item(request, item_id: int, payload: ItemIn):
    item = get_object_or_404(Item, id=item_id)
    for attr, value in payload.dict().items():
        setattr(item, attr, value)
    item.save()
    return item


@router.delete('/{item_id}', summary="删除商品")
def delete_item(request, item_id: int):
    item = get_object_or_404(Item, id=item_id)
    item.delete()  # ModelExt 会执行软删除
    return responses.ok('已删除')
