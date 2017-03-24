def getShapeDimensions( ggd_shape ):
    shapename = type(ggd_shape).__name__
    ggd_dim = []
    if "Box" in shapename:
        ggd_dim = [ggd_shape.dx, ggd_shape.dy, ggd_shape.dz]
    elif "Tubs" in shapename:
        ggd_dim = [ggd_shape.rmax, ggd_shape.rmax, ggd_shape.dz]
    elif "Sphere" in shapename:
        ggd_dim = [ggd_shape.rmax, ggd_shape.rmax, ggd_shape.rmax]
    return ggd_dim
