from gegede import Quantity as Q
import math

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def getShapeDimensions( ggd_vol, geom ):
    """
    """
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

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def main_lv( slf, geom, shape ):
    """
    """
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
    return geom.structure.Volume( "vol"+slf.name, material=slf.Material, shape=main_shape ), main_hDim

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def getRotation( slf, geom ):
    """
    Return the Rotation, is not defined return 0deg rotation
    """
    if slf.Rotation == None:
        return geom.structure.Rotation( slf.name+'_rot', '0deg', '0deg', '0deg' )
    else:
        return geom.structure.Rotation( slf.name+'_rot', str(slf.Rotation[0]),
                                            str(slf.Rotation[1]),  str(slf.Rotation[2]) )

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def getInsideGap( slf ):
    """
    Return the InsideGap, is not defined return 0m
    """
    if slf.InsideGap == None:
        return Q('0m')
    else:
        return slf.InsideGap

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def getBeginGap( slf ):
    """
    Return the InsideGap, is not defined return 0m
    """
    if slf.BeginGap == None:
        return Q('0m')
    else:
        return slf.BeginGap

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def getInitialPos( slf, ggd_dim, transpV ):
    """
    Return the initial postion for the builder based on the TranspV
    """
    begingap = getBeginGap( slf )

    if slf.NElements == 0:
        return [0,0,0]
    else:
        return [-t*(d-begingap) for t,d in zip(transpV,ggd_dim)]

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def placeBuilders( slf, geom, main_lv, TranspV ):
    """
    Place sub-builders inside the main_lv
    """
    # definition local rotation
    rotation = getRotation( slf, geom )
    # check InsideGap
    InsideGap = getInsideGap( slf )
    # get the sub-builders and its dimensions
    sb = slf.get_builder()
    sb_lv = sb.get_volume()
    sb_dim = getShapeDimensions( sb_lv, geom )
    # get the main dimensions
    main_hDim = getShapeDimensions( main_lv, geom )
    # get the initial position of the sub-builders
    pos = getInitialPos( slf, main_hDim, TranspV )
    # placement n elements
    if slf.NElements > 0:
        for elem in range(slf.NElements):
            step = [ t*d for t,d in zip(TranspV, sb_dim) ]
            pos = [ p+s for p,s in zip(pos,step) ]
            sb_pos = geom.structure.Position(slf.name+sb_lv.name+str(elem)+'_pos',
                                                pos[0], pos[1], pos[2])
            sb_pla = geom.structure.Placement(slf.name+sb_lv.name+str(elem)+'_pla',
                                                volume=sb_lv, pos=sb_pos, rot =rotation)
            main_lv.placements.append(sb_pla.name)
            pos = [p+s+t*InsideGap for p,s,t in zip(pos,step,TranspV)]
    # placement simple element, component or subdetector
    elif slf.NElements == 0:
        sb_pos = geom.structure.Position(slf.name+sb_lv.name+'_pos',
                                            pos[0], pos[1], pos[2])
        sb_pla = geom.structure.Placement(slf.name+sb_lv.name+'_pla',
                                            volume=sb_lv, pos=sb_pos, rot =rotation)
        main_lv.placements.append(sb_pla.name)

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def placeComplexBuilders( slf, geom, main_lv, TranspV ):
    """
    Place sub-builders inside the main_lv
    """
    # definition local rotation
    rotation = getRotation( slf, geom )
    # check InsideGap
    InsideGap = getInsideGap( slf )
    # get the main dimensions
    main_hDim = getShapeDimensions( main_lv, geom )
    # initial position, based on the dimension projected on transportation vector
    pos = getInitialPos( slf, main_hDim, TranspV )
    # get builders
    builders = slf.get_builders()

    for elem in range(slf.NElements):
        for i,sb in enumerate(builders):
            # get the sub-builders and its dimensions
            sb_lv = sb.get_volume()
            sb_dim = getShapeDimensions( sb_lv, geom )
            step = [ t*d for t,d in zip(TranspV, sb_dim) ]
            pos = [ p+s for p,s in zip(pos,step) ]
            sb_pos = geom.structure.Position(slf.name+sb_lv.name+str(elem)+'_pos',
                                                pos[0], pos[1], pos[2])
            sb_pla = geom.structure.Placement(slf.name+sb_lv.name+str(elem)+'_pla',
                                                volume=sb_lv, pos=sb_pos, rot =rotation)
            main_lv.placements.append(sb_pla.name)
            pos = [p+s+t*InsideGap for p,s,t in zip(pos,step,TranspV)]

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def surroundBuilders( main_lv, sb_cent, sb_surr, gap, geom ):
    """
    """
    sb_cent_lv = sb_cent.get_volume()
    sb_cent_dim = getShapeDimensions( sb_cent_lv, geom )
    sb_surr_lv = sb_surr.get_volume()
    sb_surr_dim = getShapeDimensions( sb_surr_lv, geom )
    rotLeft = geom.structure.Rotation( main_lv.name+'_rotLeft', '0deg', '0deg', '90deg' )
    rotRight = geom.structure.Rotation( main_lv.name+'_rotRight', '0deg', '0deg', '-90deg' )

    sb_cent_pos = geom.structure.Position( sb_cent_lv.name+'_pos', Q("0m"), Q("0m"), Q("0m") )
    sb_cent_pla = geom.structure.Placement( sb_cent_lv.name+'_pla', volume=sb_cent_lv, pos=sb_cent_pos )
    main_lv.placements.append( sb_cent_pla.name )

    # Top
    pos = [ Q('0m'), sb_cent_dim[1] + sb_surr_dim[1] + gap, Q('0m') ]
    sb_surr_pos = geom.structure.Position( sb_surr_lv.name+'_top_pos', pos[0], pos[1], pos[2] )
    sb_surr_pla = geom.structure.Placement( sb_surr_lv.name+'_top_pla', volume=sb_surr_lv, pos=sb_surr_pos )
    main_lv.placements.append( sb_surr_pla.name )

    # Left
    pos = [ sb_cent_dim[0] + sb_surr_dim[1] + gap, Q('0m'), Q('0m') ]
    sb_surr_pos = geom.structure.Position( sb_surr_lv.name+'_left_pos', pos[0], pos[1], pos[2] )
    sb_surr_pla = geom.structure.Placement( sb_surr_lv.name+'_left_pla', volume=sb_surr_lv,
                                                pos=sb_surr_pos, rot=rotLeft )
    main_lv.placements.append( sb_surr_pla.name )

    # Bottom
    pos = [ Q('0m'), -sb_cent_dim[1] - sb_surr_dim[1] - gap, Q('0m') ]
    sb_surr_pos = geom.structure.Position( sb_surr_lv.name+'_bottom_pos', pos[0], pos[1], pos[2] )
    sb_surr_pla = geom.structure.Placement( sb_surr_lv.name+'_bottom_pla', volume=sb_surr_lv, pos=sb_surr_pos )
    main_lv.placements.append( sb_surr_pla.name )

    #Right
    pos = [ -sb_cent_dim[0] - sb_surr_dim[1] - gap, Q('0m'), Q('0m') ]
    sb_surr_pos = geom.structure.Position( sb_surr_lv.name+'_right_pos', pos[0], pos[1], pos[2] )
    sb_surr_pla = geom.structure.Placement( sb_surr_lv.name+'_right_pla', volume=sb_surr_lv,
                                                pos=sb_surr_pos, rot=rotRight )
    main_lv.placements.append( sb_surr_pla.name )

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def crossBuilders( main_lv, sb_cent, sb_top, sb_side, gap, geom ):
    """
    """
    sb_cent_lv = sb_cent.get_volume()
    sb_cent_dim = getShapeDimensions( sb_cent_lv, geom )
    sb_top_lv = sb_top.get_volume()
    sb_top_dim = getShapeDimensions( sb_top_lv, geom )
    sb_side_lv = sb_side.get_volume()
    sb_side_dim = getShapeDimensions( sb_side_lv, geom )
    rotLeft = geom.structure.Rotation( main_lv.name+'_rotLeft', '0deg', '0deg', '90deg' )
    rotRight = geom.structure.Rotation( main_lv.name+'_rotRight', '0deg', '0deg', '-90deg' )

    sb_cent_pos = geom.structure.Position( sb_cent_lv.name+'_pos', Q("0m"), Q("0m"), Q("0m") )
    sb_cent_pla = geom.structure.Placement( sb_cent_lv.name+'_pla', volume=sb_cent_lv, pos=sb_cent_pos )
    main_lv.placements.append( sb_cent_pla.name )

    # Top
    pos = [ Q('0m'), sb_cent_dim[1] + sb_top_dim[1] + gap, Q('0m') ]
    sb_top_pos = geom.structure.Position( sb_top_lv.name+'_top_pos', pos[0], pos[1], pos[2] )
    sb_top_pla = geom.structure.Placement( sb_top_lv.name+'_top_pla', volume=sb_top_lv, pos=sb_top_pos )
    main_lv.placements.append( sb_top_pla.name )

    # Left
    pos = [ sb_cent_dim[0] + sb_side_dim[1] + gap, Q('0m'), Q('0m') ]
    sb_side_pos = geom.structure.Position( sb_side_lv.name+'_left_pos', pos[0], pos[1], pos[2] )
    sb_side_pla = geom.structure.Placement( sb_side_lv.name+'_left_pla', volume=sb_side_lv,
                                                pos=sb_side_pos, rot=rotLeft )
    main_lv.placements.append( sb_side_pla.name )

    # Bottom
    pos = [ Q('0m'), -sb_cent_dim[1] - sb_top_dim[1] - gap, Q('0m') ]
    sb_top_pos = geom.structure.Position( sb_top_lv.name+'_bottom_pos', pos[0], pos[1], pos[2] )
    sb_top_pla = geom.structure.Placement( sb_top_lv.name+'_bottom_pla', volume=sb_top_lv, pos=sb_top_pos )
    main_lv.placements.append( sb_top_pla.name )

    #Right
    pos = [ -sb_cent_dim[0] - sb_side_dim[1] - gap, Q('0m'), Q('0m') ]
    sb_side_pos = geom.structure.Position( sb_side_lv.name+'_right_pos', pos[0], pos[1], pos[2] )
    sb_side_pla = geom.structure.Placement( sb_side_lv.name+'_right_pla', volume=sb_side_lv,
                                                pos=sb_side_pos, rot=rotRight )
    main_lv.placements.append( sb_side_pla.name )


#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def rotation( axis, theta, vec ):
    """
    Return the vector rotated, the rotation matrix is called inside.
    """
    Matrix = rotation_matrix( axis, theta)
    rot_vec = [0,0,0]
    rot_vec[0] = Matrix[0][0]*vec[0] + Matrix[0][1]*vec[1] + Matrix[0][2]*vec[2]
    rot_vec[1] = Matrix[1][0]*vec[0] + Matrix[1][1]*vec[1] + Matrix[1][2]*vec[2]
    rot_vec[2] = Matrix[2][0]*vec[0] + Matrix[2][1]*vec[1] + Matrix[2][2]*vec[2]
    return rot_vec

#^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^
def rotation_matrix( axis, theta ):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta degrees. (https://en.wikipedia.org/wiki/Euler-Rodrigues_formula)
    """
    theta_rad = math.radians(theta)
    a = math.cos(theta_rad/2.0)
    b = -1*math.sin(theta_rad/2.0)*axis[0]
    c = -1*math.sin(theta_rad/2.0)*axis[1]
    d = -1*math.sin(theta_rad/2.0)*axis[2]
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return [[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)], [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]]
