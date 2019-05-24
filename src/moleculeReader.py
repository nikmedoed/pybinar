from atom import atom
from cells import cell
from localisation import localisation
from graph2 import buildCell, buildCells
from addons import *

def readMol(link):
    with open(link) as f:
        local = localisation()
        text = f.read().split('\n')
        n = int (text[3].split()[0])
        text = list(map(lambda x: x.split()[:4], text[4:4+n]))
        atoms = list(map(lambda x: atom(x[3], x[:3], local), text))
        return cell(atoms, file=link)


if __name__ == "__main__":
    mol = readMol('..\Methylammonium.mol')
    new = dc(mol)
    print(mol)
    # buildCell(mol)
    # mol.rotate([45, 0, 0])
    # print(mol)
    # buildCell(mol)
    import rand
    ran = rand.rand("0", "TIME")
    mol.randRotate(ran)
    print(mol)
    buildCells([mol, new])
