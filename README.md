# Binar 2.0: a supercell-generation with optimal atomic configuration in simulation of disordered solid solutions

**!!!!!**

- [How to use](#howtouse)
	- [Input files](#input)
	- [Used file formats](#ff)
- [Examples](#examples)
- [Сomputational result](#result)
- [Localisation](#localisation)
- [Versioning](#versioning)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)

## Getting Started

For use download the packadge. Use GitHub interface or console command:
```
git clone https://github.com/nikmedoed/pybinar
```
You need next dependences (install it with *pip install*)
- matplotlib
- numpy

### How to use
<a name="howtouse"></a>

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

#### Input files <a name="input"></a> 
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
* `10.0` - χ² ground in percents (%) for printing GULP results. TWO numbers (`10.0 15.6`) for your grounds or ONE for interval to 0 or 100 (depending on the direction χ²)
* `1`  - n, чтобы выводить каждую n-ую попадающую в границы хи-квадрат модификацию. Оставьте пустым, чтобы не выводить. Для каждого вывода будет создан свой набор файлов.
* `0` - печать координат атомов из входного файла
* `0`  - печать координат всех размноженных атомов (0 - нет, 1 - да)
* `1`  - печать координат катионов, попавших в 2-ю координационную сферу катиона
* `0` - печать координат катионов, попавших в 1-ю координационную сферу аниона
* `0`  - печать анионов  ( в строчку), попавших в 1-ю координационную сферу основного катиона
* `0`  - печать катионов ( в строчку), попавших в 1-ю координационную сферу аниона
* `1` - печать минимальных значений хи-квадрат    
* `1` - печать распределения вероятности          
* `1` - печать координат конфигурации катионов    
* `1`  - печать координат итоговой конфигурации    
* `1`  - печать данных для GULP 
* `1`  - график вероятностей для лучшего распределения и теоретического 

```
Output:
10		// χ² ground in %	
100		// counter for printing good interations
0		// печать координат атомов из входного файла
1 		// печать координат всех размноженных атомов (0 - нет, 1 - да)
1		// печать координат катионов, попавших в 2-ю координационную сферу катиона
1		// печать координат катионов, попавших в 1-ю координационную сферу аниона
1		// печать анионов  (в строчку), попавших в 1-ю координационную сферу основного катиона
1		// печать катионов (в строчку), попавших в 1-ю координационную сферу аниона
1		// печать минимальных значений хи-квадрат    
1		// печать распределения вероятности          
1		// печать координат конфигурации катионов    
1		// печать координат итоговой конфигурации    
1		// печать данных для GULP        
1		// график вероятностей для лучшего распределения и теоретического         
```

##### Cell structure (.cif)
<a name="ff"></a> 

[Crystallographic Information File](https://en.wikipedia.org/wiki/Crystallographic_Information_File) generating by many programs for chemistry. You can generate this file using **XXXXX**. 
Requirements for cell description:
* Atom coordinates in P1
* Non-translational symmetry removed

##### Molecules (.mol)
This is standart `.mol` file. [More details](http://bit.ly/2I2WEd0)


### Examples
<a name="examples"></a> 

**`coming soon`**

## Сomputational result
<a name="result"></a> 

**`coming soon`**

## Localisation


For make your own localisation see `src/Local` directory. In `local.xlsx` file create a column with your localisation. Saving `.xlsx` will generate json files with localisation.
Localistion will choose automaticaly as your computer locale, but if your want use custom locale, your should use special flag (`#`) when running programm. Example for `ru` locale:
```
python pybinar.py exampleinput.txt /resultfolder #ru
```

## Versioning
<a name="localisation"></a> 

* `2.2` - multiprocessing
* **now** - fixing bugs, refactoring and some features
* `2.1` - insertion molecules
* `2.0` - Binar 2.0, single proces, only atoms, multi rules insertions
* `1.0` - Old Fortran single rule solution

## Authors <a name="authors"></a> 

* [**Nikita Muromtsev**](https://vk.com/nikmedoed) - *development, project managing*
* [**Ekaterina Marchenko**](https://vk.com/id37862033) - *testing, assistiveware, publications*
* [**Nikolay Eremin**](https://vk.com/id32014242) - *idea, scientific guidance*

## Acknowledgments
<a name="acknowledgments"></a> 

* [ODSS (Ordered-Disordered-Solid-Solution)](http://cryst.geol.msu.ru/odss/)
* [Binar 1.0](http://cryst.geol.msu.ru/odss/binar.pdf)
* [PyCharm Community](https://www.jetbrains.com/pycharm/)
* [Anaconda Python](https://anaconda.org/anaconda/python)