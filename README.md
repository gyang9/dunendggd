# Dune-ND-GGD

This is a tool to build proposal geometries for DUNE near detector.

dunendggd is based on the sophisticated package called [GeGeDe](https://github.com/brettviren/gegede)

# Setup
This package could be installed as user, on unix environment:

```bash
python setup.py develop --user
```
Don't forget to check your variable `PATH`
```bash
export PATH=~/.local/bin/:${PATH}
```
As root privileges:
```bash
python setup.py develop
```


# Example
To run an example containing basic detectors, you could process like:
```bash
gegede-cli duneggd/Config/PRIMggd_example.cfg duneggd/Config/DETENCLOSURE-prim-only.cfg duneggd/Config/WORLDggd.cfg -w World -o example.gdml
```

To run a full example containing surrounded magnet
```bash
gegede-cli duneggd/Config/PRIMggd_example.cfg duneggd/Config/SECggd_example.cfg duneggd/Config/DETENCLOSURE.cfg duneggd/Config/WORLDggd.cfg -w World -o full_example.gdml
```

# Quick Visualization
To do a quick check or your geometry file you can use ROOT-CERN:
```bash
root -l 'geoDisplay.C("example.gdml")'
```

# Contact
* **dunendggd:**
  * Guang Yang `guang.yang.1@stonybrook.edu`
  * Jose Palomino`jose.palominogallo@stonybrook.edu`
* **GeGeDe:**
  * Brett Viren `bviren@bnl.gov`
