from typing import TYPE_CHECKING, Dict, List

from slither.core.declarations.structure import Structure
from slither.core.variables.structure_variable import StructureVariable
from slither.vyper_parsing.variables.structure_variable import StructureVariableVyper
from slither.vyper_parsing.ast.types import StructDef, AnnAssign


class StructVyper:
    def __init__(  # pylint: disable=too-many-arguments
        self,
        st: Structure,
        struct: StructDef,
    ) -> None:

        print(struct)

        self._structure = st
        st.name = struct.name
        # st.canonical_name = canonicalName

        self._elemsNotParsed: List[AnnAssign] = struct.body

    def analyze(self, contract) -> None:
        for elem_to_parse in self._elemsNotParsed:
            elem = StructureVariable()
            elem.set_structure(self._structure)
            elem.set_offset(elem_to_parse.src, self._structure.contract.compilation_unit)

            elem_parser = StructureVariableVyper(elem, elem_to_parse)
            elem_parser.analyze(contract)

            self._structure.elems[elem.name] = elem
            self._structure.add_elem_in_order(elem.name)
        self._elemsNotParsed = []
