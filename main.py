from Classes.Chemistry.Atom import Atom
from Classes.Chemistry.Molecule import Molecule
from Classes.Speciation import Speciation


def main(**argv):
    someSpeciation = Speciation.fromStr("4 {HNO3: 16, H2O: 76, H3NO4: 4}")
    print(type(str(someSpeciation.species)), str(someSpeciation.species))

    nitrogen = Atom("N")
    hydrogen = Atom("H")
    oxygen = Atom("O")
    listAtoms = [hydrogen, nitrogen, oxygen, oxygen, oxygen]
    
    
    someMol = Molecule("HNO3")
    print(someMol)

    someOtherMol = Molecule(listAtoms)
    print(someOtherMol)

if __name__ == "__main__":
    main()