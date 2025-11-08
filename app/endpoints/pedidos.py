from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.database import get_db
from app.models.models import Pedidos, Cliente, Cupon, MetodoEnvio
from app.schemas.pedidos import PedidosCreate, PedidosUpdate, PedidosResponse, PedidosDetail

router = APIRouter()

@router.get("/pedidos", response_model=List[PedidosResponse])
def get_pedidos(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    cliente_id: Optional[int] = Query(None, description="Filtrar por ID de cliente"),
    estado_pedido: Optional[str] = Query(None, description="Filtrar por estado del pedido"),
    estado_pago: Optional[str] = Query(None, description="Filtrar por estado del pago"),
    fecha_envio_desde: Optional[datetime] = Query(None, description="Filtrar por fecha de envío desde (YYYY-MM-DD o YYYY-MM-DD HH:MM:SS)"),
    fecha_envio_hasta: Optional[datetime] = Query(None, description="Filtrar por fecha de envío hasta (YYYY-MM-DD o YYYY-MM-DD HH:MM:SS)"),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de pedidos con filtros opcionales y paginación.
    
    Filtros disponibles:
    - cliente_id: ID del cliente
    - estado_pedido: pendiente, procesando, enviado, entregado, cancelado
    - estado_pago: pendiente, pagado, fallido, reembolsado
    - fecha_envio_desde: Fecha mínima de envío (inclusive)
    - fecha_envio_hasta: Fecha máxima de envío (inclusive)
    
    Ejemplos de uso:
    - /pedidos?fecha_envio_desde=2025-11-01&fecha_envio_hasta=2025-11-30
    - /pedidos?fecha_envio_desde=2025-11-10 10:00:00
    - /pedidos?fecha_envio_hasta=2025-11-15
    """
    query = db.query(Pedidos)
    
    # Aplicar filtros
    if cliente_id:
        query = query.filter(Pedidos.clienteId == cliente_id)
    if estado_pedido:
        query = query.filter(Pedidos.estadoPedido == estado_pedido)
    if estado_pago:
        query = query.filter(Pedidos.estadoPago == estado_pago)
    
    # Filtros de rango de fecha de envío
    if fecha_envio_desde:
        query = query.filter(Pedidos.fechaEnvio >= fecha_envio_desde)
    if fecha_envio_hasta:
        query = query.filter(Pedidos.fechaEnvio <= fecha_envio_hasta)

    # Ordenar por fecha de creación (más recientes primero)
    query = query.order_by(Pedidos.creadoEn.desc())
    
    pedidos = query.offset(skip).limit(limit).all()
    return pedidos


@router.get("/pedidos/{pedido_id}", response_model=PedidosDetail)
def get_pedido(
    pedido_id: int = Path(..., description="ID del pedido"),
    db: Session = Depends(get_db)
):
    """
    Obtener un pedido específico por ID con información detallada
    """
    pedido = db.query(Pedidos).options(
        joinedload(Pedidos.cliente),
        joinedload(Pedidos.cupon),
        joinedload(Pedidos.metodoEnvio)
    ).filter(Pedidos.id == pedido_id).first()
    
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    # Crear respuesta detallada
    pedido_detail = PedidosDetail(
        id=pedido.id,
        clienteId=pedido.clienteId,
        montoTotal=float(pedido.montoTotal),
        estadoPedido=pedido.estadoPedido,
        estadoPago=pedido.estadoPago,
        metodoPago=pedido.metodoPago,
        direccionEnvio=pedido.direccionEnvio,
        cuponId=pedido.cuponId,
        metodoEnvioId=pedido.metodoEnvioId,
        fechaEnvio=pedido.fechaEnvio,
        creadoEn=pedido.creadoEn,
        cliente_nombre=f"{pedido.cliente.nombre} {pedido.cliente.apellido}" if pedido.cliente else None,
        cliente_email=pedido.cliente.email if pedido.cliente else None,
        cupon_codigo=pedido.cupon.codigo if pedido.cupon else None,
        metodo_envio_nombre=pedido.metodoEnvio.nombre if pedido.metodoEnvio else None
    )
    
    return pedido_detail


@router.post("/pedidos", response_model=PedidosResponse, status_code=201)
def create_pedido(pedido: PedidosCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo pedido
    """
    # Validar que el cliente existe
    cliente = db.query(Cliente).filter(Cliente.id == pedido.clienteId).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Validar cupón si se proporciona
    if pedido.cuponId:
        cupon = db.query(Cupon).filter(Cupon.id == pedido.cuponId).first()
        if not cupon:
            raise HTTPException(status_code=404, detail="Cupón no encontrado")
    
    # Validar método de envío si se proporciona
    if pedido.metodoEnvioId:
        metodo_envio = db.query(MetodoEnvio).filter(MetodoEnvio.id == pedido.metodoEnvioId).first()
        if not metodo_envio:
            raise HTTPException(status_code=404, detail="Método de envío no encontrado")
    
    # Crear el pedido
    db_pedido = Pedidos(
        clienteId=pedido.clienteId,
        montoTotal=pedido.montoTotal,
        estadoPedido=pedido.estadoPedido,
        estadoPago=pedido.estadoPago,
        metodoPago=pedido.metodoPago,
        direccionEnvio=pedido.direccionEnvio,
        cuponId=pedido.cuponId,
        metodoEnvioId=pedido.metodoEnvioId,
        fechaEnvio=pedido.fechaEnvio
    )
    
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido


@router.put("/pedidos/{pedido_id}", response_model=PedidosResponse)
def update_pedido(
    pedido_id: int = Path(..., description="ID del pedido"),
    pedido_update: PedidosUpdate = ...,
    db: Session = Depends(get_db)
):
    """
    Actualizar un pedido existente
    """
    # Verificar que el pedido existe
    db_pedido = db.query(Pedidos).filter(Pedidos.id == pedido_id).first()
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    # Validar estados si se proporcionan
    estados_pedido_validos = ['pendiente', 'procesando', 'enviado', 'entregado', 'cancelado']
    estados_pago_validos = ['pendiente', 'pagado', 'fallido', 'reembolsado']
    
    if pedido_update.estadoPedido and pedido_update.estadoPedido not in estados_pedido_validos:
        raise HTTPException(status_code=400, detail=f"Estado de pedido inválido. Valores permitidos: {estados_pedido_validos}")
    
    if pedido_update.estadoPago and pedido_update.estadoPago not in estados_pago_validos:
        raise HTTPException(status_code=400, detail=f"Estado de pago inválido. Valores permitidos: {estados_pago_validos}")
    
    # Validar cupón si se proporciona
    if pedido_update.cuponId:
        cupon = db.query(Cupon).filter(Cupon.id == pedido_update.cuponId).first()
        if not cupon:
            raise HTTPException(status_code=404, detail="Cupón no encontrado")
    
    # Validar método de envío si se proporciona
    if pedido_update.metodoEnvioId:
        metodo_envio = db.query(MetodoEnvio).filter(MetodoEnvio.id == pedido_update.metodoEnvioId).first()
        if not metodo_envio:
            raise HTTPException(status_code=404, detail="Método de envío no encontrado")
    
    # Actualizar campos
    update_data = pedido_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_pedido, field, value)
    
    db.commit()
    db.refresh(db_pedido)
    return db_pedido


@router.patch("/pedidos/{pedido_id}/estado", response_model=PedidosResponse)
def update_pedido_estado(
    pedido_id: int = Path(..., description="ID del pedido"),
    estado_pedido: Optional[str] = Query(None, description="Nuevo estado del pedido"),
    estado_pago: Optional[str] = Query(None, description="Nuevo estado del pago"),
    db: Session = Depends(get_db)
):
    """
    Actualizar solo los estados de un pedido (endpoint especializado)
    """
    # Verificar que el pedido existe
    db_pedido = db.query(Pedidos).filter(Pedidos.id == pedido_id).first()
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    # Validar que al menos un estado se proporciona
    if not estado_pedido and not estado_pago:
        raise HTTPException(status_code=400, detail="Debe proporcionar al menos un estado para actualizar")
    
    # Validar estados
    if estado_pedido:
        estados_pedido_validos = ['pendiente', 'procesando', 'enviado', 'entregado', 'cancelado']
        if estado_pedido not in estados_pedido_validos:
            raise HTTPException(status_code=400, detail=f"Estado de pedido inválido. Valores permitidos: {estados_pedido_validos}")
        db_pedido.estadoPedido = estado_pedido
    
    if estado_pago:
        estados_pago_validos = ['pendiente', 'pagado', 'fallido', 'reembolsado']
        if estado_pago not in estados_pago_validos:
            raise HTTPException(status_code=400, detail=f"Estado de pago inválido. Valores permitidos: {estados_pago_validos}")
        db_pedido.estadoPago = estado_pago
    
    db.commit()
    db.refresh(db_pedido)
    return db_pedido


@router.delete("/pedidos/{pedido_id}", status_code=204)
def delete_pedido(
    pedido_id: int = Path(..., description="ID del pedido"),
    db: Session = Depends(get_db)
):
    """
    Eliminar un pedido (soft delete recomendado, pero aquí implementamos hard delete)
    """
    db_pedido = db.query(Pedidos).filter(Pedidos.id == pedido_id).first()
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    # Verificar que el pedido puede ser eliminado (ej: no debe estar en estado 'enviado' o 'entregado')
    estados_no_eliminables = ['enviado', 'entregado']
    if db_pedido.estadoPedido in estados_no_eliminables:
        raise HTTPException(
            status_code=400, 
            detail=f"No se puede eliminar un pedido en estado '{db_pedido.estadoPedido}'"
        )
    
    db.delete(db_pedido)
    db.commit()
    return None


@router.get("/pedidos/cliente/{cliente_id}", response_model=List[PedidosResponse])
def get_pedidos_by_cliente(
    cliente_id: int = Path(..., description="ID del cliente"),
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    db: Session = Depends(get_db)
):
    """
    Obtener todos los pedidos de un cliente específico
    """
    # Verificar que el cliente existe
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    pedidos = db.query(Pedidos).filter(
        Pedidos.clienteId == cliente_id
    ).order_by(Pedidos.creadoEn.desc()).offset(skip).limit(limit).all()
    
    return pedidos


@router.get("/pedidos/stats/resumen")
def get_pedidos_stats(db: Session = Depends(get_db)):
    """
    Obtener estadísticas resumidas de pedidos
    """
    total_pedidos = db.query(Pedidos).count()
    pedidos_pendientes = db.query(Pedidos).filter(Pedidos.estadoPedido == 'pendiente').count()
    pedidos_procesando = db.query(Pedidos).filter(Pedidos.estadoPedido == 'procesando').count()
    pedidos_enviados = db.query(Pedidos).filter(Pedidos.estadoPedido == 'enviado').count()
    pedidos_entregados = db.query(Pedidos).filter(Pedidos.estadoPedido == 'entregado').count()
    pedidos_cancelados = db.query(Pedidos).filter(Pedidos.estadoPedido == 'cancelado').count()
    
    # Estadísticas de pagos
    pagos_pendientes = db.query(Pedidos).filter(Pedidos.estadoPago == 'pendiente').count()
    pagos_completados = db.query(Pedidos).filter(Pedidos.estadoPago == 'pagado').count()
    pagos_fallidos = db.query(Pedidos).filter(Pedidos.estadoPago == 'fallido').count()
    
    # Monto total de pedidos pagados
    from sqlalchemy import func
    monto_total = db.query(func.sum(Pedidos.montoTotal)).filter(Pedidos.estadoPago == 'pagado').scalar() or 0
    
    return {
        "total_pedidos": total_pedidos,
        "estados_pedido": {
            "pendientes": pedidos_pendientes,
            "procesando": pedidos_procesando,
            "enviados": pedidos_enviados,
            "entregados": pedidos_entregados,
            "cancelados": pedidos_cancelados
        },
        "estados_pago": {
            "pendientes": pagos_pendientes,
            "completados": pagos_completados,
            "fallidos": pagos_fallidos
        },
        "monto_total_pagado": float(monto_total)
    }