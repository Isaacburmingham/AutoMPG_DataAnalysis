# Isaac Burmingham
# Week 8

import csv
import sys
from collections import namedtuple,defaultdict
import os
import logging
import requests
import argparse
import matplotlib.pyplot as plt


class AutoMPG:

    def __init__(self,make,model,year,mpg):
        self.make = str(make)
        self.model = str(model)
        self.year = int(year)
        self.mpg = float(mpg)

    def __repr__(self):
        return "AutoMPG%s" % str(self)

    def __str__(self):
        return "(%s, %s, %d, %.1f)" % (self.make, self.model, self.year, self.mpg)

    def __eq__(self, other):
        print(f"Debug: {str(self)} == {str(other)}")
        if type(self) == type(other):
            return self.make == other.make and self.model == other.model \
                and self.year == other.year and self.mpg == other.mpg
        else:
            return NotImplemented

    def __lt__(self, other):
        #print(f"Debug: {str(self)} < {str(other)}")
        # assuming this means all attributes
        if type(self) == type(other):
            return (self.make, self.model, self.year, self.mpg) \
                    < (self.make, self.model, other.year, other.mpg)
        else:
            return NotImplemented


    def __hash__(self):
        return hash((self.make, self.model, self.year, self.mpg))


Record = namedtuple('Record', ("mpg","cylinders", "displacement", "horsepower","weight","acceleration",
    "model_year","origin","car_name"))

class AutoMPGData:

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('autompg3.log','w')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    logger.addHandler(sh)


    def __init__(self):
        self.data = []
        self._load_data()

    def __iter__(self):
        self._iter = 0
        return self

    def __next__(self):
        if self._iter == len(self.data):
            raise StopIteration
        datum = self.data[self._iter]
        self._iter += 1
        return datum

    def _clean_data(self):
        if not os.path.exists("auto-mpg.data.txt"):
              logging.debug('File not found, making a request')
              self._get_data()
        else:
            with open("auto-mpg.data.txt", 'r',newline='') as infile:
                with open("auto-mpg.clean.txt", 'w',newline='') as outfile:
                    reader = csv.reader(infile, skipinitialspace=True)
                    writer = csv.writer(outfile,quoting=csv.QUOTE_NONE,quotechar = '')
                    for row in reader:
                        newRow = [w.expandtabs(4) for w in row]
                        writer.writerow(newRow)
                    logging.info('file has been cleaned')
                self._load_data()

    def _load_data(self):
        # if not os.path.exists("auto-mpg.data.txt"):
        #      logging.debug('File not found, making a request')
        #      self._get_data()
        # else:
        if not os.path.exists("auto-mpg.clean.txt"):
            logging.debug('Data not cleaned, going to run _clean_data')
            self._clean_data()
        else:
            logging.info('cleaned file found')
            with open('auto-mpg.clean.txt', 'r',newline='') as infile:
                reader = csv.reader(infile, skipinitialspace=True,delimiter=' ')
                for row in reader:
                    record = Record(*row)
                    make = record.car_name.split()[0]
                    model = ' '.join(record.car_name.split()[1:])
                    if make == 'vw' or make == 'vokswagen':
                        make = 'volkswagen'
                    elif make == 'chevroelt' or make == 'chevy':
                        make = 'chevrolet'
                    elif make == 'maxda':
                        make = 'mazda'
                    elif make == 'mercedes-benz':
                        make = 'mercedes'
                    elif make == 'toyouta':
                        make = 'toyota'
                    dataclean = AutoMPG(make,model,int("19" + record.model_year),float(record.mpg))
                    self.data.append(dataclean)
                logging.info('Finished loading')

    def sort_by_default(self):
            self.data.sort()
            #logging.debug(self.data)

    def sort_by_year(self):
            self.data.sort(key=lambda x: x.year)
            #logging.debug(self.data)

    def sort_by_mpg(self):
            self.data.sort(key=lambda x: x.mpg)
            #logging.debug(self.data)

    def _get_data(self):
        rawdata = requests.get('https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data')
        rawdata.raise_for_status()
        with open('auto-mpg.data.txt','wb') as file:
            file.write(rawdata.content)
        self._load_data()

    def mpg_by_year(self):
        # if not os.path.exists("auto-mpg.clean.txt"):
        #     logging.debug('Data not cleaned, going to run _clean_data')
        #     self._clean_data()
        mpg_year = defaultdict(list)
        with open("auto-mpg.clean.txt",'r') as f:
            reader = csv.reader(f, skipinitialspace=True,delimiter=' ')
            for row in reader:
                record = Record(*row)
                year = int("19" + record.model_year)
                mpg = float(record.mpg)
                mpg_year[year].append(mpg)
            for year in mpg_year:
                mpg_avg = sum(mpg_year[year])/len(mpg_year[year])
                mpg_year[year] = round(mpg_avg,2)

            return mpg_year

            #for k,v in mpg_year.items():
            #    print(k,v)
            #logging.info(mpg_year.items())

    def mpg_by_make(self):
        if not os.path.exists("auto-mpg.clean.txt"):
            logging.debug('Data not cleaned, going to run _clean_data')
            self._clean_data()
        mpg_make = defaultdict(list)
        with open("auto-mpg.clean.txt",'r') as f:
            reader = csv.reader(f, skipinitialspace=True,delimiter=' ')
            for row in reader:
                record = Record(*row)
                make = record.car_name.split()[0]
                mpg = float(record.mpg)
                if make == 'vw' or make == 'vokswagen':
                    make = 'volkswagen'
                elif make == 'chevroelt' or make == 'chevy':
                    make = 'chevrolet'
                elif make == 'maxda':
                    make = 'mazda'
                elif make == 'mercedes-benz':
                    make = 'mercedes'
                elif make == 'toyouta':
                    make = 'toyota'
                mpg_make[make].append(mpg)

            for make in mpg_make:
                mpg_avg = sum(mpg_make[make])/len(mpg_make[make])
                mpg_make[make] = round(mpg_avg,2)

            return mpg_make




def main():
    parser = argparse.ArgumentParser(description="Analyze Auto MPG data")
    parser.add_argument("command", metavar='<command>', help='command to execute')
    parser.add_argument("-s",'--sort', metavar='<sort order>',
    help='sort the data by different values',choices=['year','mpg','default'])
    parser.add_argument("-o","--ofile",metavar='<outfile>', help='file to write to, default is standard output')
    parser.add_argument("-p","--plot",action='store_true',help="Plot the output")
    args = parser.parse_args()

    myData = AutoMPGData()

    if args.ofile:
        with open(args.ofile, 'w',newline='') as outfile:
            writer = csv.writer(outfile, dialect='excel')

            if args.command == 'print':

                if args.plot:
                    logging.debug('sorry you cannot plot, too many dimensions')

                if args.sort == 'year':
                    myData.sort_by_year()
                    logging.info('Finished')

                elif args.sort == 'mpg':
                    myData.sort_by_mpg()
                    logging.info('Finished')

                else:
                    myData.sort_by_default() #sort by default if not specified
                    logging.info('Finished')

                for data in myData:
                    make,model,year,mpg = data.make,data.model,str(data.year),str(data.mpg)
                    rows = [make,model,year,mpg]
                    writer.writerow(rows)
                    print(repr(data))

            elif args.command == 'mpg_by_year':
                d = myData.mpg_by_year()

                if args.plot:
                    plt.figure(figsize=(10,6))
                    plt.plot(list(d.keys()),list(d.values()),'bo')
                    plt.title('MPG by Year')
                    plt.xlabel('Year')
                    plt.ylabel('MPG')
                    plt.show()

                for k,v in d.items():
                    rows = [k,v]
                    writer.writerow(rows)

            elif args.command == 'mpg_by_make':
                d = myData.mpg_by_make()

                if args.plot:
                    plt.figure(figsize=(10,6))
                    plt.plot(list(d.keys()),list(d.values()),'ro')
                    plt.title('MPG by Make')
                    plt.xlabel('Make')
                    plt.ylabel('MPG')
                    plt.xticks(rotation=45)
                    plt.show()

                for k,v in d.items():
                    rows = [k,v]
                    writer.writerow(rows)



    else:
        if args.command == 'print':

            if args.plot:
                logging.debug('sorry you cannot plot, too many dimensions')

            if args.sort == 'year':
                myData.sort_by_year()
                logging.info('Finished')

            elif args.sort == 'mpg':
                myData.sort_by_mpg()
                logging.info('Finished')

            else:
                myData.sort_by_default()
                logging.info('Finished')

            for data in myData:
                sys.stdout.write(repr(data) + '\n') # write to standard output

        elif args.command == 'mpg_by_year':
            d = myData.mpg_by_year()

            if args.plot:
                plt.figure(figsize=(10,6))
                plt.plot(list(d.keys()),list(d.values()),'bo')
                plt.title('MPG by Year')
                plt.xlabel('Year')
                plt.ylabel('MPG')
                plt.show()

            for k,v in d.items():
                rows = str((k,v))
                sys.stdout.write(rows + '\n')

        elif args.command == 'mpg_by_make':
            d = myData.mpg_by_make()

            if args.plot:
                plt.figure(figsize=(10,6))
                plt.plot(list(d.keys()),list(d.values()),'ro')
                plt.title('MPG by Make')
                plt.xlabel('Make')
                plt.ylabel('MPG')
                plt.xticks(rotation=45)
                plt.show()

            for k,v in d.items():
                rows = str((k,v))
                sys.stdout.write(rows + '\n')

if __name__ == "__main__":
    main()
