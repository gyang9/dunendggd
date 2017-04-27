from gegede import Quantity as Q
import math

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
    return geom.structure.Volume( slf.name+"_lv", material=slf.Material, shape=main_shape ), main_hDim

def getInitialPos( slf, ggd_dim ):
    """
    Return the initial postion for the builder based on the TranspV
    """
    if slf.BeginGap == None:
        begingap = Q('0m')
    else:
        begingap = slf.BeginGap
    return [-t*(d-begingap) for t,d in zip(slf.TranspV,ggd_dim)]

def surroundBuilders( main_lv, sb_cent, sb_surr, axis, initial_vec, gap, angles, geom ):
    """
    """
    sb_cent_lv = sb_cent.get_volume()
    sb_cent_dim = getShapeDimensions( sb_cent_lv, geom )
    sb_surr_lv = sb_surr.get_volume()
    sb_surr_dim = getShapeDimensions( sb_surr_lv, geom )

    Pos = [Q("0m"),Q("0m"),Q("0m")]
    sb_cent_pos = geom.structure.Position( sb_cent_lv.name+'_pos', Pos[0], Pos[1], Pos[2] )
    sb_cent_pla = geom.structure.Placement( sb_cent_lv.name+'_pla', volume=sb_cent_lv, pos=sb_cent_pos )
    main_lv.placements.append( sb_cent_pla.name )

    for i, angle in enumerate(angles):
        f_vec = rotation(axis, angle, initial_vec)
        pos = [a*(b+c+gap) for a,b,c in zip(f_vec,sb_cent_dim,sb_surr_dim)]
        sb_surr_pos = geom.structure.Position( sb_surr_lv.name+str(angle)+'_pos', pos[0], pos[1], pos[2] )
        sb_surr_pla = geom.structure.Placement( sb_surr_lv.name+str(angle)+'_pla', volume=sb_surr_lv, pos=sb_surr_pos )
        main_lv.placements.append( sb_surr_pla.name )

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
