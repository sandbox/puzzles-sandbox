names = ["william","oliver","elizabeth","lucy","natalie","nicole","regina"]
houses = [x for x in range(1, 8)]
everyday = ["accord", "dart", "escort", "impala", "opel", "taurus", "yugo"]
everyday_year = [2001, 2002, 2003, 2004, 2005, 2006, 2007]
classic = ["corniche", "corvair", "countach", "el dorado", "ferrari", "porsche", "spider"]
classic_year = [1965, 1966, 1968, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990]

import itertools

possibilities = itertools.product(names, houses, everyday, everyday_year, classic, classic_year)


import csv

with open("possibilities.csv", "w") as blah:
  csv_writer = csv.writer(blah)
  csv_writer.writerow(("name", "house", "everyday", "eyear", "classic", "cyear"))
  for x in possibilities:
    csv_writer.writerow(x)

import pandas
df = pandas.read_csv("possibilities.csv")
from pprint import pprint

def pc(a, b):
  ret = [(name, sorted(df[(df[a]==name)][b].unique())) for name in sorted(df[a].unique())]
  pprint(ret)
  return ret

def pc2(df, a, b):
  pprint([(name, sorted(df[(df[a]==name)][b].unique())) for name in sorted(df[a].unique())])

def show(df, condition):
  print(df[condition])

def drop_inplace(df, condition):
  print(len(df))
  df.drop(df[condition].index, inplace=True)
  print(len(df))

df['dyear'] = df['eyear'] - df['cyear']
df['hmatch'] = df['eyear'] - df['house'] == 2000

# 1. William and Oliver live in even house numbers.
drop_inplace(df, (df['name'] == 'william') & ~(df['house'].isin([2,4,6])))
drop_inplace(df, (df['name'] == 'oliver') & ~(df['house'].isin([2,4,6])))

# 2. Neither the Corvair or El Dorado were manufactured in the 1970s.
drop_inplace(df, (df['classic'] == 'el dorado') & (df['cyear'].isin(range(1970, 1980))))
drop_inplace(df, (df['classic'] == 'corvair') & (df['cyear'].isin(range(1970, 1980))))

# Two everyday cars (the Yugo and the car owned by the person who also owned the Porsche)
#   have the same year
#    => yugo and porsche not the same person
drop_inplace(df, (df['everyday'] == 'yugo') & (df['classic'] == 'porsche'))
# Two classic cars (the Countach and Lucy’s classic car) were manufactured in the same year
#    => lucy does not have countach
drop_inplace(df, (df['name'] == 'lucy') & (df['classic'] == 'countach'))

# lucy classic and countach have same year
# yugo and everyday of porsche have same year

# drop_inplace(df, (df['name'] == 'regina') & ~(df['house'].isin([2,3,4,5,6])))

# Regina often starts the day by checking out her neighbor’s Corvair and her other neighbor’s El Dorado.
#   None of the three own either the Opel or the Yugo.
#  regina does not own corvair or eldorado
drop_inplace(df, (df['name'] == 'regina') & (df['classic'].isin(["el dorado", "corvair"])))
#  regina does not own opel or yugo
drop_inplace(df, (df['name'] == 'regina') & (df['everyday'].isin(["yugo", "opel"])))
#  owner of el dorado/corvair does not own yugo or opel
drop_inplace(df, (df['classic'].isin(["el dorado", "corvair"])) & (df['everyday'].isin(["yugo", "opel"])))

# 7. The owner of the Dart is a woman.
drop_inplace(df, (df['everyday'].isin(["dart"])) & (df['name'].isin(["william", "oliver"])))
# The owner of the Countach is a man.
drop_inplace(df, (df['classic'].isin(["countach"])) & ~(df['name'].isin(["william", "oliver"])))

# the Impala, whose owner lives in an even house number
drop_inplace(df, (df['everyday'].isin(["impala"])) & (df['house'].isin([1, 3, 5, 7])))

# two houses on the left (Natalie and the owner of either the Opel or Yugo
drop_inplace(df, (df['name'].isin(["natalie"])) & ~(df['house'].isin([1, 2])))

# three houses in the middle (the owner of the Porsche, the owner of the Accord
#   * and the owner of a car manufactured in 2001
drop_inplace(df, (df['classic'].isin(["porsche"])) & ~(df['house'].isin([3,4,5])))
drop_inplace(df, (df['everyday'].isin(["accord"])) & ~(df['house'].isin([3,4,5])))
# => owner of porsche cannot be same as owner of accord
drop_inplace(df, (df['classic'].isin(["porsche"])) & (df['everyday'].isin(["accord"])))

# two houses on the right (the owner of the Spider and the owner of the Dart)
drop_inplace(df, (df['classic'].isin(["spider"])) & ~(df['house'].isin([6,7])))
drop_inplace(df, (df['everyday'].isin(["dart"])) & ~(df['house'].isin([6,7])))


# spider and dart not together
drop_inplace(df, (df['classic'].isin(["spider"])) & (df['everyday'].isin(['dart'])))
# porsche in 3,4,5 => cannot have dart and porsche
drop_inplace(df, (df['classic'].isin(["porsche"])) & (df['everyday'].isin(['dart'])))
# accord in 3,4,5 => spider cannot be with accord
drop_inplace(df, (df['classic'].isin(["spider"])) & (df['everyday'].isin(['accord'])))

# biggest difference in age between an owner’s two cars is 36 years.
drop_inplace(df, df['dyear'] > 36)

# the Corniche, which was manufactured in an even-numbered year, is 21 years older than its owner’s
# everyday car.`
drop_inplace(df, (df['classic'].isin(["corniche"])) & (df['dyear'] != 21))
drop_inplace(df, (df['classic'].isin(["corniche"])) & (df['cyear'].isin(range(1965, 2000, 2))))

# The owners on the ends of the street are Lucy and the owner of both the Escort and Corniche
drop_inplace(df, (df['classic'].isin(["corniche"])) & ~(df['everyday'].isin(['escort']) ))
drop_inplace(df, ~(df['classic'].isin(["corniche"])) & (df['everyday'].isin(['escort']) ))

# The owners on the ends of the street are Lucy and the owner of both the Escort and Corniche
drop_inplace(df, (df['classic'].isin(["corniche"])) & ~(df['house'].isin([1, 7]) ))
drop_inplace(df, (df['everyday'].isin(["escort"])) & ~(df['house'].isin([1, 7]) ))
drop_inplace(df, (df['name'].isin(["lucy"])) & ~(df['house'].isin([1, 7]) ))

# consistent

# 8. Two everyday cars have years that match their house number: the one that’s exactly 28 years younger
#    than its owner’s classic car and the Impala, whose owner lives in an even house number.
#
# 8 : if house matches car number, then must be 28 years apart or impala
drop_inplace(df, (df['eyear'] - df['house'] == 2000) & (~(df['everyday']=='impala') & ~(df['eyear'] - df['cyear'] == 28)))
#   impala year matches house number
drop_inplace(df, (df['eyear'] - df['house'] != 2000) & (df['everyday']=='impala'))


# 16, house is 2 less than taurus
drop_inplace(df, (df['everyday'].isin(["taurus"])) & (df['house'].isin([1, 2]) ))

# Nicole owns the oldest car, which is either the Ferrari or Corvai
# nicole owns either ferrari or corvair
drop_inplace(df, (df['name'].isin(["nicole"])) & ~(df['classic'].isin(["ferrari", "corvair"]) ))

# Nicole owns the oldest car, which is either the Ferrari or Corvair.
#   if there is a 1965 it can only be a ferrari or corvair
#   if there is a 1965 it can only be nicole
drop_inplace(df, (df['cyear'].isin([1965])) & ~(df['classic'].isin(['ferrari', 'corvair']) ))
drop_inplace(df, (df['cyear'].isin([1965])) & ~(df['name'].isin(['nicole']) ))

# nicole owns oldest + only 2 classic have same date => nicole must own car older than 1984
# 85 86 87 88 89 90
# biggest difference in age between an owner’s two cars is 36 years
#  => nicole must have car older than 1971 (otherwise can't fit a difference in age of 36)
drop_inplace(df, (df['name'].isin(["nicole"])) & (df['cyear'] > 1971))

# 15 : lucy has most recently manufactured car, at least 2006 since 2006 exists
drop_inplace(df, (df['name']=='lucy') & (df['eyear'] < 2006))

# lucy. Two classic cars (the Countach and Lucy’s classic car) were manufactured in the same year.
# lucy only has following possible years
drop_inplace(df, (df['classic'].isin(["countach"])) & ~(df['cyear'].isin([1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990]) ))

# 14. The owners on the ends of the street are Lucy and the owner of both the Escort and Corniche.
#  => lucy cannot own escort or corniche
drop_inplace(df, (df['name'].isin(["lucy"])) & (df['classic'].isin(["corniche"]) ))
drop_inplace(df, (df['name'].isin(["lucy"])) & (df['everyday'].isin(["escort"]) ))


## filtered-12-51
## df = pandas.read_csv("~/Downloads/filtered-possibilities-12-51.csv", index_col=0)


# the Yugo and the car owned by the person who also owned the Porsche
#   one of ('porsche', ['impala', 'opel', 'taurus']), has same year as yugo
#
# Two classic cars (the Countach and Lucy’s classic car) were manufactured in the same year.
#   one of ('lucy', ['corvair', 'el dorado', 'ferrari', 'spider']) has same year as Countach
#
#

# 11.The biggest difference in age between an owner’s two cars is 36 years. This owner lives next to Oliver.
# => 36 year difference cannot be in a spot not next to oliver
#   oliver is 2, 4, 6


### Regina often starts the day by checking out her neighbor’s Corvair and her other neighbor’s El Dorado.
# => regina is 2 through 6 (has 2 neighbors)
drop_inplace(df, (df['name'].isin(["regina"])) & (df['house'].isin([1, 7]) ))

# if 28 year apart match house year
# Two everyday cars have years that match their house number: the one that’s exactly 28 years younger
#   than its owner’s classic car and the Impala, whose owner lives in an even house number.
drop_inplace(df, (df['dyear']==28) & ~(df['hmatch']))

# yugo is not made in 2001
#
# otherwise, yugo 2001 and everday of porsche in 2001 and owner in middle 3 house non-porsche also 2001. Too many in 2001
# 4. Two everyday cars (the Yugo and the car owned by the person who also owned the Porsche) were manufactured in the same year
drop_inplace(df, (df['everyday'].isin(["yugo"])) & (df['eyear'].isin([2001]) ))

# Two everyday cars (the Yugo and the car owned by the person who also owned the Porsche) were
# manufactured in the same year. Two classic cars (the Countach and Lucy’s classic car) were
# manufactured in the same year. No other cars were manufactured in the same year as another car.

# lucy cannot own porsche => lucy's everyday car year is unique
# if lucy is 2007, no one else can be 2007, if lucy is 2006, no one else can be 2007. Only lucy can be 2007
drop_inplace(df, ~(df['name'].isin(["lucy"])) & (df['eyear'].isin([2007]) ))

# saved = df.copy(deep=True)

# guess: lucy is 2006 yields contradiction

# guess: lucy is 2007 and lucy is in 7
drop_inplace(df, (df['name'].isin(["lucy"])) & (df['eyear'].isin([2006]) ))
drop_inplace(df, (df['name'].isin(["lucy"])) & ~(df['house'].isin([7]) ))
drop_inplace(df, ~(df['name'].isin(["lucy"])) & (df['house'].isin([7]) ))
drop_inplace(df, (df['classic'].isin(['countach'])) & ~(df['cyear'].isin([1979]))) # countach same year as lucy classic
drop_inplace(df, (df['classic'].isin(["corniche"])) & ~(df['house'].isin([1]) ))
drop_inplace(df, ~(df['classic'].isin(["corniche"])) & (df['house'].isin([1]) ))
drop_inplace(df, (df['classic'].isin(['porsche'])) & (df['cyear'].isin([1979]))) # porsche cannot be 1979, lucy classic not porsche/countach are 1979
# two houses on the left (Natalie and the owner of either the Opel or Yugo),
#   escort in 1 => natalie is in 1, since opel/yugo cannot be in 1
drop_inplace(df, (df['name'].isin(['natalie'])) & ~(df['house'].isin([1])))
drop_inplace(df, ~(df['name'].isin(['natalie'])) & (df['house'].isin([1])))
drop_inplace(df, (df['house'].isin([2])) & ~(df['everyday'].isin(['opel', 'yugo'])))
## second guess: lucy owns dart or lucy owns spider
saved2 = df.copy(deep=True)

## lucy owns spider
drop_inplace(df, (df['name'].isin(["lucy"])) & ~(df['classic'].isin(['spider']) ))
drop_inplace(df, ~(df['name'].isin(["lucy"])) & (df['classic'].isin(['spider']) ))
drop_inplace(df, (df['house'].isin([6])) & ~(df['everyday'].isin(['dart']) ))
drop_inplace(df, ~(df['house'].isin([6])) & (df['everyday'].isin(['dart']) ))
drop_inplace(df, (df['house'].isin([6])) & (df['name'].isin(['william', 'oliver']) ))

drop_inplace(df, (df['house'].isin([3, 5, 6])) & ~(df['name'].isin(['elizabeth', 'regina', 'nicole']) ))
drop_inplace(df, ~(df['house'].isin([3, 5, 6])) & (df['name'].isin(['elizabeth', 'regina', 'nicole']) ))
# >>> x = pc('house', 'classic'); print(len(x))
# [(1, ['corniche']),
#  (2, ['countach', 'ferrari']),
#  (3, ['corvair', 'el dorado', 'ferrari', 'porsche']),
#  (4, ['corvair', 'countach', 'el dorado', 'ferrari', 'porsche']),
#  (5, ['corvair', 'el dorado', 'ferrari', 'porsche']),
#  (6, ['corvair', 'el dorado', 'ferrari']),
#  (7, ['spider'])]
# 7
# regina next to corvair and el dorado => regina cannot be in 3, and must be 4/5 => regina in 5
drop_inplace(df, ~(df['house'].isin([4, 5])) & (df['name'].isin(['regina']) ))
drop_inplace(df, ~(df['house'].isin([5])) & (df['name'].isin(['regina']) ))
drop_inplace(df, (df['house'].isin([5])) & ~(df['name'].isin(['regina']) ))

drop_inplace(df, ~(df['house'].isin([4, 6])) & (df['classic'].isin(['el dorado', 'corvair']) ))
drop_inplace(df, (df['house'].isin([4, 6])) & ~(df['classic'].isin(['el dorado', 'corvair']) ))
drop_inplace(df, (df['house'].isin([2])) & ~(df['classic'].isin(['countach']) ))

drop_inplace(df, (df['everyday'].isin(['accord'])) & ~(df['classic'].isin(['ferrari']) ))
drop_inplace(df, ~(df['everyday'].isin(['accord'])) & (df['classic'].isin(['ferrari']) ))
drop_inplace(df, (df['everyday'].isin(['taurus'])) & ~(df['classic'].isin(['porsche', 'spider']) ))
drop_inplace(df, ~(df['everyday'].isin(['impala'])) & (df['eyear'].isin([2004]) ))
drop_inplace(df, (df['everyday'].isin(['taurus'])) & (df['house'].isin([3]) ))
drop_inplace(df, (df['eyear'].isin([2006])) & ~(df['house'].isin([3, 5]) ))
drop_inplace(df, (df['eyear'].isin([2001])) & (df['classic'].isin(['porsche']) ))
# contradiction because william or oliver need a 35 year difference, and not possible
