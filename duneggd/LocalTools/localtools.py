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

def main_lv( slf, geom, shape ):
    main_shape = geom.shapes.Box( slf.name, dx=slf.halfDimension['dx'], dy=slf.halfDimension['dy'], dz=slf.halfDimension['dz'] )
    return geom.structure.Volume( slf.name+"_lv", material=slf.Material, shape=main_shape )
