# AutoMPG Data Analysis
Object oriented approach in Python to data analysis utilizing modules such as argparse and logging, using data from the UCI Machine Learning Repository.

This program focuses on pulling data using the requests module from the UCI database if the file is not present. The file is then cleaned, and then loaded, in which you can print the data, sort the data by mpg or year, as well as have some plot options. This was for a graduate class assigment.

Attributes of the dataset:
1. mpg: continuous
2. cylinders: multi-valued discrete
3. displacement: continuous
4. horsepower: continuous
5. weight: continuous
6. acceleration: continuous
7. model year: multi-valued discrete
8. origin: multi-valued discrete
9. car name: string (unique for each instance)


Here is the argparse help option:
usage: autompg3.py [-h] [-s <sort order>] [-o <outfile>] [-p] <command>

Analyze Auto MPG data

positional arguments:
  <command>             command to execute

optional arguments:
  -h, --help            show this help message and exit
  -s <sort order>, --sort <sort order>
                        sort the data by different values
  -o <outfile>, --ofile <outfile>
                        file to write to, default is standard output
  -p, --plot            Plot the output


Citation:
Dua, D. and Graff, C. (2019). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, School of Information and Computer Science.
