from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from app.database import get_db
from app.models.models import ItemsPedido, Pedidos, Producto
from app.schemas.itemspedido import (
    ItemsPedidoCreate,
    ItemsPedidoUpdate,
    ItemsPedidoResponse,
    ItemsPedidoDetail
)

router = APIRouter()


@router.get("/item-pedido/", response_model=List[ItemsPedidoResponse])
def get_items_pedido(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a devolver"),
    pedido_id: Optional[int] = Query(None, description="Filtrar por ID de pedido"),
    producto_id: Optional[int] = Query(None, description="Filtrar por ID de producto"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de items de pedido con filtros opcionales y paginación.
    """
    query = db.query(ItemsPedido)

    # Aplicar filtros
    if pedido_id:
        query = query.filter(ItemsPedido.pedidoId == pedido_id)
    if producto_id:
        query = query.filter(ItemsPedido.productoId == producto_id)

    items = query.offset(skip).limit(limit).all()
    return items


@router.post("/item-pedido/", response_model=ItemsPedidoResponse)
def create_item_pedido(item: ItemsPedidoCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo ítem en un pedido.
    """
    # Verificar que el pedido existe
    pedido = db.query(Pedidos).filter(Pedidos.id == item.pedidoId).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    # Verificar que el producto existe
    producto = db.query(Producto).filter(Producto.id == item.productoId).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Verificar que no exista ya este producto en el pedido
    existing_item = db.query(ItemsPedido).filter(
        and_(ItemsPedido.pedidoId == item.pedidoId, ItemsPedido.productoId == item.productoId)
    ).first()
    if existing_item:
        raise HTTPException(
            status_code=400,
            detail="Este producto ya existe en el pedido. Use PUT para actualizar la cantidad."
        )

    # Crear el nuevo ítem
    db_item = ItemsPedido(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/item-pedido/{item_id}", response_model=ItemsPedidoDetail)
def get_item_pedido(item_id: int, db: Session = Depends(get_db)):
    """
    Obtener un ítem de pedido específico con detalles del pedido y producto.
    """
    item = db.query(ItemsPedido).filter(ItemsPedido.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ítem de pedido no encontrado")

    # Obtener información relacionada
    pedido_info = {
        "id": item.pedido.id,
        "clienteId": item.pedido.clienteId,
        "estadoPedido": item.pedido.estadoPedido,
        "montoTotal": float(item.pedido.montoTotal)
    } if item.pedido else None

    producto_info = {
        "id": item.producto.id,
        "nombre": item.producto.nombre,
        "precio": float(item.producto.precio)
    } if item.producto else None

    return ItemsPedidoDetail(
        id=item.id,
        pedidoId=item.pedidoId,
        productoId=item.productoId,
        cantidad=item.cantidad,
        precioUnitario=float(item.precioUnitario),
        subtotal=float(item.subtotal),
        pedido=pedido_info,
        producto=producto_info
    )


@router.put("/item-pedido/{item_id}", response_model=ItemsPedidoResponse)
def update_item_pedido(
    item_id: int,
    item_update: ItemsPedidoCreate,
    db: Session = Depends(get_db)
):
    """
    Actualizar completamente un ítem de pedido.
    """
    item = db.query(ItemsPedido).filter(ItemsPedido.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ítem de pedido no encontrado")

    # Verificar que el pedido existe
    pedido = db.query(Pedidos).filter(Pedidos.id == item_update.pedidoId).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    # Verificar que el producto existe
    producto = db.query(Producto).filter(Producto.id == item_update.productoId).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Verificar que no exista ya este producto en otro ítem del mismo pedido
    if item_update.pedidoId != item.pedidoId or item_update.productoId != item.productoId:
        existing_item = db.query(ItemsPedido).filter(
            and_(
                ItemsPedido.pedidoId == item_update.pedidoId,
                ItemsPedido.productoId == item_update.productoId,
                ItemsPedido.id != item_id
            )
        ).first()
        if existing_item:
            raise HTTPException(
                status_code=400,
                detail="Este producto ya existe en el pedido"
            )

    # Actualizar el ítem
    for field, value in item_update.model_dump().items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


@router.patch("/item-pedido/{item_id}", response_model=ItemsPedidoResponse)
def patch_item_pedido(
    item_id: int,
    item_update: ItemsPedidoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar parcialmente un ítem de pedido.
    """
    item = db.query(ItemsPedido).filter(ItemsPedido.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ítem de pedido no encontrado")

    # Aplicar solo los campos proporcionados
    update_data = item_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No se proporcionaron campos para actualizar")

    # Si se actualiza cantidad o precioUnitario, recalcular subtotal
    if 'cantidad' in update_data or 'precioUnitario' in update_data:
        cantidad = update_data.get('cantidad', item.cantidad)
        precio_unitario = update_data.get('precioUnitario', item.precioUnitario)
        update_data['subtotal'] = cantidad * precio_unitario

    for field, value in update_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


@router.delete("/item-pedido/{item_id}")
def delete_item_pedido(item_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un ítem de pedido.
    """
    item = db.query(ItemsPedido).filter(ItemsPedido.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ítem de pedido no encontrado")

    # Verificar que el pedido no esté en estado que no permita modificaciones
    if item.pedido and item.pedido.estadoPedido in ['enviado', 'entregado']:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar ítems de pedidos ya enviados o entregados"
        )

    db.delete(item)
    db.commit()
    return {"message": "Ítem de pedido eliminado exitosamente"}


@router.get("/item-pedido/pedido/{pedido_id}", response_model=List[ItemsPedidoDetail])
def get_items_by_pedido(pedido_id: int, db: Session = Depends(get_db)):
    """
    Obtener todos los ítems de un pedido específico.
    """
    # Verificar que el pedido existe
    pedido = db.query(Pedidos).filter(Pedidos.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    items = db.query(ItemsPedido).filter(ItemsPedido.pedidoId == pedido_id).all()

    result = []
    for item in items:
        producto_info = {
            "id": item.producto.id,
            "nombre": item.producto.nombre,
            "precio": float(item.producto.precio)
        } if item.producto else None

        result.append(ItemsPedidoDetail(
            id=item.id,
            pedidoId=item.pedidoId,
            productoId=item.productoId,
            cantidad=item.cantidad,
            precioUnitario=float(item.precioUnitario),
            subtotal=float(item.subtotal),
            pedido=None,  # Ya sabemos el pedido
            producto=producto_info
        ))

    return result


@router.get("/item-pedido/producto/{producto_id}", response_model=List[ItemsPedidoDetail])
def get_items_by_producto(producto_id: int, db: Session = Depends(get_db)):
    """
    Obtener todos los ítems de pedido que contienen un producto específico.
    """
    # Verificar que el producto existe
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    items = db.query(ItemsPedido).filter(ItemsPedido.productoId == producto_id).all()

    result = []
    for item in items:
        pedido_info = {
            "id": item.pedido.id,
            "clienteId": item.pedido.clienteId,
            "estadoPedido": item.pedido.estadoPedido,
            "montoTotal": float(item.pedido.montoTotal)
        } if item.pedido else None

        result.append(ItemsPedidoDetail(
            id=item.id,
            pedidoId=item.pedidoId,
            productoId=item.productoId,
            cantidad=item.cantidad,
            precioUnitario=float(item.precioUnitario),
            subtotal=float(item.subtotal),
            pedido=pedido_info,
            producto=None  # Ya sabemos el producto
        ))

    return result
