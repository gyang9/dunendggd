def getShapeDimensions( ggd_vol, geom ):
    ggd_shape = geom.store.shapes.get(ggd_vol.shape)
    shapename = type(ggd_shape).__name__
    ggd_dim = []
    if "Box" in shapename:
        ggd_dim = [ggd_shape.dx, ggd_shape.dy, ggd_shape.dz]
    elif "Tubs" in shapename:
        ggd_dim = [ggd_shape.rmax, ggd_shape.rmax, ggd_shape.dz]
    elif "Sphere" in shapename:
        ggd_dim = [ggd_shape.rmax, ggd_shape.rmax, ggd_shape.rmax]
    return ggd_dim

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
    if "Box" == shape:
        main_shape = geom.shapes.Box( slf.name, dx=slf.halfDimension['dx'], dy=slf.halfDimension['dy'],
                                        dz=slf.halfDimension['dz'] )
        main_hDim = [main_shape.dx, main_shape.dy, main_shape.dz]
    elif "Tubs" == shape:
        main_shape = geom.shape.Tubs( slf.name, rmin=slf.halfDimension['rmin'], rmax=slf.halfDimension['rmax'],
                                        dz=slf.halfDimension['dz'] )
        main_hDim = [main_shape.rmax, main_shape.rmax, main_shape.dz]
    elif "Sphere" == shape:
        main_shape = geom.shapes.Sphere( slf.name, rmin=slf.halfDimension['rmin'], rmax=slf.halfDimension['rmax'] )
        main_hDim = [main_shape.rmax, main_shape.rmax, main_shape.rmax]

    return geom.structure.Volume( slf.name+"_lv", material=slf.Material, shape=main_shape ), main_hDim
