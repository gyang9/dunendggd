# Dune-ND-GGD

This is a tool to build proposal geometries for DUNE near detector.

dunendggd is based on the sophisticated package called [GeGeDe](https://github.com/brettviren/gegede)

# Setup
```bash
python setup.sh develop
```
# Example
```bash
cd ndggd
gegede-cli Config/PRIMggd_test.cfg Config/COMMONggd_test.cfg -w World -o ID.gdml
```

* **dunendggd:**
  * Guang Yang `guang.yang.1@stonybrook.edu`
  * Jose Palomino`jose.palominogallo@stonybrook.edu`
* **GeGeDe:**
  * Brett Viren `bviren@bnl.gov`
