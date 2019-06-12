# Binar 2.0: a supercell-generation with optimal atomic configuration in simulation of disordered solid solutions

!!!!!

## Getting Started

For use download the packadge. Use GitHub interface or console command:
```
git clone https://github.com/nikmedoed/pybinar
```
You need next dependences (install it with *pip install*)
- matplotlib
- numpy

### How to use
1. Prepare your Python 3.x interpreter, install all dependences (see links at the end of readme)
2. Prepare experiment files
-- Get correct *.cif* file
-- Prepare .mol files if needed
-- Create your parametres file (use *exampleinput.txt* or this readme). Don't forget to set your *.cif* file there
3. Run experiment with console by command below. You can create *.bat* or *.sh* file for regulary runnig. See examples in packadge directory.
```
python pybinar.py exampleinput.txt /resultfolder #
```
* Parametrs can be in different order. 
* Flag ==#== set the locale. If no, default ==ru==.
* With ==/== your set result folder. Default ==running folder==.
* Else one parametr (without indicators) set the file with experint paramentrs. Default ==example #1==.

#### Input files
##### Experiment parametres
!!!!!!
##### Cell structure (.cif)
[Crystallographic Information File](https://en.wikipedia.org/wiki/Crystallographic_Information_File) generating by many programs for chemistry. You can generate this file using XXXXX. 
Requirements for cell description:
* Atom coordinates in P1
* Non-translational symmetry removed

##### Molecules (.mol)
This is standart *.mol* file. [More details](http://bit.ly/2I2WEd0)

### Examples
!!!!!
## Сomputational result
!!!!!
## Localisation
For make your own localisation see *"src/Local"* directory. In *"local.xlsx"* file create a column with your localisation. Saving *.xlsx* will generate json files with localisation.
Localistion will choose automaticaly as your computer locale, but if your want use custom locale, your should use special flag (==#==) when running programm. Example for ==ru== locale:
```
python pybinar.py exampleinput.txt /resultfolder #ru
```

## Versioning


* 2.2 - multiprocessing
* **now** - fixing bugs, refactoring
* 2.1 - insertion molecules
* 2.0 - Binar 2.0, single proces, only atoms, multi rules insertions
* 1.0 - Old Fortran single rule solution

## Authors

* [**Nikita Muromtsev**](https://vk.com/nikmedoed) - *development, project managing*
* [**Ekaterina Marchenko**](https://vk.com/id37862033) - *testing, assistiveware, publications*
* [**Nikolay Eremin**](https://vk.com/id32014242) - *idea, scientific guidance*

## Acknowledgments

* [ODSS (Ordered-Disordered-Solid-Solution)](http://cryst.geol.msu.ru/odss/)
* [Binar 1.0](http://cryst.geol.msu.ru/odss/binar.pdf)
* [PyCharm Community](https://www.jetbrains.com/pycharm/)
* [Anaconda Python](https://anaconda.org/anaconda/python)