#!/usr/bin/env python
'''
Builds compontents for the MPT ECAL
'''

import gegede.builder
from gegede import Quantity as Q

from math import floor, atan, sin, cos, sqrt, pi



class MPTECalTileBuilder(gegede.builder.Builder):
    """Builds a single pad for the MPT Ecal

    The pad is built in the x,y plane with multiple layers.

    Attributes:
    dx,dy: x and y half-dimensions of the pad
    dz: a list specifying the depth of each layer
    lspacing: a list specifying the spacing after each layer
    mat: a list specifying the material of each layer
    filler_mat: the material between and outside of layers
    """
    # set a .defaults which gegede will use to make data members
    # when configure is called

    defaults = dict(dx=Q("15mm"), dy=Q("15mm"),
                    dz=[Q('2mm'), Q('5mm'), Q('1mm')],
                    lspacing=[Q('0.1mm'), Q('0.1mm'), Q('2mm')],
                    mat=['Copper', 'Scintillator', 'FR4'],
                    filler_mat='Air')

#    def configure(self, **kwds):
#        pass

    def depth(self):
        dzm = Q("0mm")
        for dz, lspace in zip(self.dz, self.lspacing):
            dzm += dz+lspace
        return dzm

    def construct(self, geom):
        # first make a mother volume to hold everything else
        dzm = self.depth()
        dzm = dzm/2.0  # Box() requires half dimensions
        print "dzm=", dzm
        name = "MPTECalTile"
        pad_shape = geom.shapes.Box(name, self.dx, self.dy, dzm)
        pad_lv = geom.structure.Volume(name+"_vol", material=self.filler_mat,
                                       shape=pad_shape)
        # now loop to create layers

        skip = Q("0mm")  # no skipped space before the first layer
        cntr = 1
        zloc = Q("0mm")
        for dz, lspace, mat in zip(self.dz, self.lspacing, self.mat):
            lname = (name+"_L%i" % cntr)
            layer_shape = geom.shapes.Box(lname, self.dx, self.dy, dz/2.0)
            zloc = zloc+skip+dz/2.0
            print dz, lspace, mat, zloc
            layer_lv = geom.structure.Volume(lname+"_vol", material=mat,
                                             shape=layer_shape)
            # dzm is the half depth of the mother volume
            # we need to subtract it off to position layers
            # relative to the center of the mother
            layer_pos = geom.structure.Position(lname+"_pos",
                                                x='0mm', y='0mm', z=zloc-dzm)
            layer_pla = geom.structure.Placement(lname+"_pla",
                                                 volume=layer_lv,
                                                 pos=layer_pos)
            pad_lv.placements.append(layer_pla.name)

            skip = dz/2.0+lspace  # set the skipped space before the next layer
            cntr += 1

        self.add_volume(pad_lv)
        return


class MPTECalStripBuilder(gegede.builder.Builder):
    """Builds a strip of ECalTiles

    The strip is built in the x,y plane with its length along x

    Attributes:
    length=the length of the strip,
           will compute the closest number of tiles to fit within this length
    ntiles=the number of tiles
    material=the default material of the strip (will fill in any cracks)
    extra_space=space between tiles
    """
    # set a .defaults which gegede will use to make data members
    # when configure is called

    defaults = dict(length=Q("1m"),
                    ntiles=0,
                    material='Air',
                    extra_space=Q("0.1mm")
                    )

#    def configure(self, **kwds):
#        super(MPTECalStripBuilder, self).configure(**kwds)

    def build_tile(self, geom, mother, lv, xloc, i):
        pos = geom.structure.Position(lv.name+"_%i_pos" % i,
                                      x=xloc, y='0mm', z='0mm')
        pla = geom.structure.Placement(lv.name+"_%i_pla" % i,
                                       volume=lv, pos=pos)

        mother.placements.append(pla.name)
        return

    def construct(self, geom):
        tile_builder = self.get_builder("MPTECalTileBuilder")
        tile_width = tile_builder.dx*2 + self.extra_space
        # has the number of tiles been specified?
        ntiles = 0
        if(self.ntiles > 0):
            ntiles = self.ntiles
        else:
            # need to figure out how many tiles
            ntiles = int(floor(self.length/tile_width))  # round explicitly
        strip_length = ntiles*tile_width

        # make the mother volume
        name = "MPTECalStrip"
        print "In strip builder: strip_length=", strip_length
        strip_shape = geom.shapes.Box(name,
                                      dx=strip_length/2.0,
                                      dy=tile_builder.dy,
                                      dz=tile_builder.depth()/2.0)
        strip_lv = geom.structure.Volume(name+"_vol", shape=strip_shape,
                                         material=self.material)

        tile_lv = tile_builder.get_volume()
        for i, xloc in symmetric_arrangement(ntiles, tile_width):
            self.build_tile(geom, strip_lv, tile_lv, xloc, i)

        self.add_volume(strip_lv)
        return


def symmetric_arrangement(ntiles, tile_width):
    """Arrange ntiles of tile_width symmetrically around zero.

    Returns a tuple (int: itile,real: location)
    where itile ranges from -ntiles/2 to +ntiles/2 for even ntiles
    and -(ntiles-1)/2 to +(ntiles-1)/2 for odd ntiles
    """
    def feven(w, i):
        return w*(i-0.5)

    def fodd(w, i): return w*i
    xloc = feven
    istart = 1
    iend = ntiles/2
    if ntiles % 2 != 0:
        xloc = fodd
        istart = 0
        iend = (ntiles-1)/2
    rval = []
    for i in range(istart, iend+1):
        rval.append((i, xloc(tile_width, i)))
        if(i != 0):
            rval.append((-i, -xloc(tile_width, i)))
    return rval


class MPTECalLayerBuilder(gegede.builder.Builder):
    """Builds a layer of ECalStrips

    Attributes:
    geometry=
      cylinder: build on a cylinder of radius r with angular coverage over
                phi_range=[start,end]. cylinder axis along z. phi is the
                usual angle in the x,y plane.
      xyplane: build out a rectangular plane of width x, height y
      cplane: build out a circular plane of radius r
    r, phi_range= used by the cylinder and cplane (just r) geometries
    x, y= used by the xyplane geometry
    material= material filling the mother volume (fills in any cracks)
    extra_space = space between strips
    """
    # set a .defaults which gegede will use to make data members
    # when configure is called

    defaults = dict(geometry='cylinder',
                    r=Q("2.5m"), phi_range=[Q("0deg"), Q("360deg")],
                    material='Air',
                    extra_space=Q("0.1mm")
                    )

#    def configure(self, **kwds):
#        super(MPTECalStripBuilder, self).configure(**kwds)

    def construct(self, geom):
        if self.geometry == 'cylinder':
            self.construct_cylinder(geom)
        return

    def construct_cylinder(self, geom):
        strip_builder = self.get_builder("MPTECalStripBuilder")
        strip_lv = strip_builder.get_volume()
        ggd_shape = geom.store.shapes.get(strip_lv.shape)
        y_strip = (ggd_shape.dy+self.extra_space)*2
        z_strip = ggd_shape.dz*2
        strip_length = ggd_shape.dx*2

        # start by building the mother volume
        wanted_phi_coverage = self.phi_range[1]-self.phi_range[0]
        # dphi=angle covered by one strip with inside face at radius r
        dphi = 2*atan(y_strip/(2*self.r))
        n_strips = int(floor(wanted_phi_coverage/dphi))
        actual_phi_coverage = n_strips*dphi
        phi_coverage_diff = wanted_phi_coverage-actual_phi_coverage
        # adjust phi start and end points
        # checked that phi_end-phi_start=phi actual
        phi_start = self.phi_range[0]+phi_coverage_diff/2.0
        phi_end = self.phi_range[1]-phi_coverage_diff/2.0
        rmin = self.r
        print z_strip, rmin, y_strip,strip_length
        rmax2 = ((z_strip+rmin)**2 + (y_strip/2.0)**2)/Q("1mm**2")
        print rmax2
        rmax=sqrt(rmax2)*Q("1mm")
        lname = "MPTECalCylindricalLayer"
        # start with the Tubs symmetric about phi=zero
        # this works better with symmetric_arrangement()
        # we will rotate it later
        temp_phi_start = -actual_phi_coverage/2
        layer_shape = geom.shapes.Tubs(lname, rmin=rmin, rmax=rmax,
                                       sphi=temp_phi_start,
                                       dphi=actual_phi_coverage,
                                       dz=strip_length/2.0)

        layer_lv = geom.structure.Volume(lname+"_vol", shape=layer_shape,
                                         material=self.material)

        # now fill the mother volume with strips
        # the approach will be similar to what we did to make strips
        # we first will center strips on phi=0 and then rotate to get
        # the correct phi_start and phi_end
        for i, dloc in symmetric_arrangement(n_strips, dphi):
            # instead of formally rotating, just modify dloc here?
            xloc = (self.r+z_strip/2.0)*cos(dloc)
            yloc = (self.r+z_strip/2.0)*sin(dloc)
            zloc = Q("0mm")
#            print dloc
            pos = geom.structure.Position(strip_lv.name+"_%i_pos" % i,
                                          x=xloc, y=yloc, z=zloc)
            rot = geom.structure.Rotation(strip_lv.name+"_%i_rot" % i,
                                          x='90deg',y=(dloc-pi/2.0),
                                          z='90deg')
            pla = geom.structure.Placement(strip_lv.name+"_%i_pla" % i,
                                           volume=strip_lv, pos=pos, rot=rot)

            layer_lv.placements.append(pla.name)
        self.add_volume(layer_lv)
        return
