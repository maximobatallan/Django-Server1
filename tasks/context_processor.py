def total_carrito(request):
    total = 0
    cantidad = 0
    if request.user.is_authenticated:
        if "carrito" in request.session.keys():
            
            for key, value in request.session["carrito"].items():
                carrito = len(request.session["carrito"].items())
               
                total += int(value["acumulado"])
                cantidad += int(value["cantidad"])
                
    return {"total_carrito": total,"cantidad": cantidad}