## Goals 

Toward implementing effective fuzzing for the serialization functions of the IPDL
compiler, we plan to take the following development approach. 
- .ipdl and .ipdlh Generator
- Run IPDL compiler in isolation against the generated files
  - Frozen at changeset [648192:80e567cf7ef7].
- Automatically test that the generated C++ serialization functions 