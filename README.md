# Binar 2.0: a supercell-generation with optimal atomic configuration in simulation of disordered solid solutions

The program allows to generate disordered configuration of solid solutions, as well as organic-inorganic compounds with molecules in the random orientation with an infinite size approximation. In order to run the program, it is necessary to create two files: the INPUT file containing the input information of calculation parameters (supercell size, atom insertion rules, the rules for χ² criterion, etc.) and the CIF file with structural information in space group P1. 
After calculations, the program creates two files: the OUTPUT file containing the output information of the problem and the structural information data with the atomic coordinates of the best chosen configurations. The criterion for the degree of disordering of the configuration is represented by the squares of deviations of the numbers of pairs of dissimilar atoms in the second coordination sphere for the random configuration from the theoretical statistical histogram (the Pearson goodness-of-fit criterion). A set of random configurations is analyzed for the deviation from the ideal statistical histogram of the frequency of occurrence of dissimilar second neighbors for each composition (the χ² criterion). The ideal disordered configuration is determined by combinatorial methods with the correction for the relative concentration of each component. The program can be recommended for ab-initio calculations and simulation with semi-empirical methods.

- [How to use](#howtouse)
	- [* Input files](#input)
	- [Used file formats](#ff)
- [* Examples](#examples)
- [* Сomputational result](#result)
- [Localisation](#localisation)
- [Versioning](#versioning)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)

## Getting Started

For use download the packadge. Use GitHub interface or console command:
```
git clone https://github.com/nikmedoed/pybinar
```
You need next dependences (install with `pip install`)
- matplotlib
- numpy

<a name="howtouse"></a>
### How to use

1. Prepare your Python 3.x interpreter, install all dependences (see links at the end of readme)
2. Prepare experiment files
	- Get correct `.cif` file
	- Prepare `.mol` files if needed
	- Create your parametres file (use *exampleinput.txt* or this readme). Don't forget to set your *.cif* file there
3. Run experiment with console by command below. You can create `.bat` or `.sh` file for regulary runnig. See examples in packadge directory.
```
python pybinar.py exampleinput.txt /resultfolder #
```
* Parametrs can be in different order.
* Flag `#` set the locale. If no, default `ru` (russian).
* With `/` your set result folder. Default **running folder**.
* Else one parametr (without indicators) set the file with experint paramentrs. Default **example #1**.

<a name="input"></a>
#### Input files
##### Experiment parametres

For inputing experiment parametrs use text file. Rules for input file:
* `//` Double slash for comments. Ingnors all symbols to the end of line
*  Useless spaces and lines ingrnores
*  Parameters are divided into several blocks
*  Blocks can be placed in random order
*  Inside block, the fields must follow the specified order

###### Name:
Contains path (name) to file with cell description (.cif)
```
Name:
NaCl.cif
```
###### Сonditions:
* `2 2 2` - how make translation fpr supercell
* `0` - code for random generator (0 - default, 1 and etc. - `in feature`)
*  `_` - random paramentr / any  symbol combination or `TIME` for use actual time
* `X > X1(p) 1`	- insertion rule (any numbers of lines). 
	- `interchangeable atom` `>` `insertable atom` `(insertable atom energy)` `number of implementations`
	- `X > Methylammonium.mol 1` - use for inserting molecules (see about `.mol` below)

```
Сonditions:
4 4 4
0
TIME
Na > K1(1.5) 96
Na > Methylammonium.mol 10
```
###### Сonstraints:
* `20` - time limit in minutes (uses for interations only). Also you van use `hhhh:mm:ss` (ex. `12:31:23`) or `hhhh:mm`
* `3.0` - the radius of neighbors sphere in Å (coordination sphere)
* `0` - χ² direction: 1 - select iteration where χ² is maximum, 0 - if χ² is minimal
* `0.1` - χ² ground (iterations stop if got) 

```
Сonstraints:
30
4.2
0
0.1
```
###### Output:
* `10.0` - χ² ground in percents (%) for printing GULP results.
	- TWO numbers (`10.0 15.6`) for your grounds 
	- ONE for interval to 0 or 100% (depending on the direction χ²)
* `1` - n, for printing every n-th iteration with χ² in grounds
	- will create pack of files
	- ` ` (nothing) for cancel printing
* `0` or `1` - printin cell atoms coordinates in result file
* `0` or `1` - printin sulercell atoms coordinates in result file
* **`other` in progress**

```
Output:
10		// χ² ground in %
100		// counter for printing good interations
0		// printing cell coordinates
1 		// printing supercell coordinates
```

<a name="ff"></a>
##### Cell structure (.cif)

[Crystallographic Information File](https://en.wikipedia.org/wiki/Crystallographic_Information_File) generating by many programs for chemistry.
Atom **coordinates in P1** are required.

##### Molecules (.mol)
This is standart `.mol` file. [More details](http://bit.ly/2I2WEd0)

<a name="examples"></a>
### Examples

**`coming soon`**

<a name="result"></a>
## Сomputational result

**`coming soon`**

## Localisation


For make your own localisation see `src/Local` directory. In `local.xlsx` file create a column with your localisation. Saving `.xlsx` will generate json files with localisation.
Localistion will choose automaticaly as your computer locale, but if your want use custom locale, your should use special flag (`#`) when running programm. Example for `ru` locale:
```
python pybinar.py exampleinput.txt /resultfolder #ru
```

<a name="localisation"></a>
## Versioning

* `2.2` - multiprocessing
* **now** - fixing bugs, refactoring and some features
* `2.1` - insertion molecules
* `2.0` - Binar 2.0, single proces, only atoms, multi rules insertions
* `1.0` - Old Fortran single rule solution

<a name="authors"></a>
## Authors

* [**Nikita Muromtsev**](https://vk.com/nikmedoed) - *development, project managing*
* [**Nikolay Eremin**](https://vk.com/id32014242) - *idea, scientific guidance*
* [**Ekaterina Marchenko**](https://vk.com/id37862033) - *testing, assistiveware, publications*

<a name="acknowledgments"></a>
## Acknowledgments


* [ODSS (Ordered-Disordered-Solid-Solution)](http://cryst.geol.msu.ru/odss/)
* [Binar 1.0](http://cryst.geol.msu.ru/odss/binar.pdf)
* [PyCharm Community](https://www.jetbrains.com/pycharm/)
* [Anaconda Python](https://anaconda.org/anaconda/python)