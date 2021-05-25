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

## lucy owns dart
drop_inplace(df, (df['name'].isin(["lucy"])) & ~(df['everyday'].isin(['dart']) ))
drop_inplace(df, ~(df['name'].isin(["lucy"])) & (df['everyday'].isin(['dart']) ))
drop_inplace(df, ~(df['name'].isin(["lucy"])) & (df['classic'].isin(['ferrari']) ))
drop_inplace(df, ~(df['name'].isin(["nicole"])) & (df['classic'].isin(['corvair']) ))
drop_inplace(df, ~(df['name'].isin(["natalie"])) & (df['classic'].isin(['corniche']) ))
drop_inplace(df, (df['house'].isin([6])) & ~(df['classic'].isin(['spider']) ))
drop_inplace(df, ~(df['house'].isin([6])) & (df['classic'].isin(['spider']) ))
drop_inplace(df, (df['classic'].isin(['porsche'])) & (df['eyear'].isin([2001]) )) # everyday with porsche is same year as yugo, yugo is 2002 - 2006
# >>> x = pc('classic', 'house')
# [('corniche', [1]),
#  ('corvair', [3, 4, 5]),
#  ('countach', [2, 4]),
#  ('el dorado', [3, 4, 5]),
#  ('ferrari', [7]),
#  ('porsche', [3, 4, 5]),
#  ('spider', [6])]
drop_inplace(df, (df['classic'].isin(['countach'])) & (df['house'].isin([4]) )) # countach can't be in 4
# if regina sees el dorado and corvair, then they cannot be next to each other => corvair / el dorado are 3 or 5 => porsche is in 4 and regina is in 4
drop_inplace(df, (df['classic'].isin(['porsche'])) & ~(df['house'].isin([4]) ))
drop_inplace(df, ~(df['classic'].isin(['porsche'])) & (df['house'].isin([4]) ))
drop_inplace(df, (df['name'].isin(['regina'])) & ~(df['house'].isin([4]) ))
drop_inplace(df, ~(df['name'].isin(['regina'])) & (df['house'].isin([4]) ))
# [('elizabeth', [3, 5, 6]),
#  ('lucy', [7]),
#  ('natalie', [1]),
#  ('nicole', [3, 5]),
#  ('oliver', [2, 6]),
#  ('regina', [4]),
#  ('william', [2, 6])]
# => elizabeth cannot be in 6
drop_inplace(df, (df['name'].isin(['elizabeth'])) & (df['house'].isin([6]) ))
# [('elizabeth', ['accord', 'taurus']),
#  ('lucy', ['dart']),
#  ('natalie', ['escort']),
#  ('nicole', ['accord', 'taurus']),
#  ('oliver', ['impala', 'opel', 'taurus', 'yugo']),
#  ('regina', ['impala', 'taurus']),
#  ('william', ['impala', 'opel', 'taurus', 'yugo'])]
# => accord/taurus is elizabeth/nicole => regina is impala, and william/oliver are opel/yugo
drop_inplace(df, ~(df['name'].isin(['elizabeth','nicole'])) & (df['everyday'].isin(['accord', 'taurus']) ))
drop_inplace(df, ~(df['name'].isin(['regina'])) & (df['everyday'].isin(['impala']) ))
drop_inplace(df, (df['name'].isin(['regina'])) & ~(df['everyday'].isin(['impala']) ))
#16. The owner of the 2006 car lives in a house whose number is exactly 2 less than the Taurus’s owner.
# [(1, ['escort']),
#  (2, ['opel', 'yugo']),
#  (3, ['accord', 'taurus']),
#  (4, ['impala']),
#  (5, ['accord', 'taurus']),
#  (6, ['opel', 'yugo']),
#  (7, ['dart'])]
# => 2006 is in 1 or in 3,
# [(1, [2003, 2005]),
 # (2, [2001, 2003, 2004, 2005, 2006]),
 # (3, [2001, 2002, 2004, 2005, 2006]),
 # (4, [2004]),
 # (5, [2001, 2002, 2003, 2004, 2006]),
 # (6, [2001, 2002, 2003, 2004, 2005, 2006]),
 # (7, [2007])]
 # => 2006 is not in 1 => 2006 in 3 => taurus is in 5
drop_inplace(df, ~(df['house'].isin([5])) & (df['everyday'].isin(['taurus']) ))
drop_inplace(df, (df['house'].isin([5])) & ~(df['everyday'].isin(['taurus']) ))
drop_inplace(df, (df['house'].isin([3])) & ~(df['eyear'].isin([2006]) ))
# [(1, ['corniche']),
#  (2, ['countach']),
#  (3, ['el dorado']),
#  (4, ['porsche']),
#  (5, ['corvair', 'el dorado']),
#  (6, ['spider']),
#  (7, ['ferrari'])]
# => corvair is in 5
drop_inplace(df, (df['house'].isin([5])) & ~(df['classic'].isin(['corvair']) ))
drop_inplace(df, ~(df['house'].isin([5])) & (df['classic'].isin(['corvair']) ))
# [(1, [21]),
#  (2, [22, 24, 25, 26, 27]),
#  (3, [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]),
#  (4, [14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36]),
#  (5, [33, 34, 35, 36]),
#  (6, [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]),
#  (7, [28])]
# biggest difference in age between an owner’s two cars is 36 years. This owner lives next to Oliver
#   oliver lives in 2 or 6
#   only 4, 5, have 36 age difference => 5 must have 36 year age difference and oliver lives in 6
drop_inplace(df, (df['house'].isin([5])) & ~(df['dyear'].isin([36]) ))
drop_inplace(df, ~(df['house'].isin([6])) & (df['name'].isin(['oliver']) ))
drop_inplace(df, (df['house'].isin([6])) & ~(df['name'].isin(['oliver']) ))
# >>> x = pc('house', 'eyear'); print(len(x))
# [(1, [2003, 2005]),
#  (2, [2001, 2003, 2004, 2005, 2006]),
#  (3, [2006]),
#  (4, [2004]),
#  (5, [2001, 2002, 2004]),
#  (6, [2001, 2002, 2003, 2004, 2005, 2006]),
#  (7, [2007])]
# 7
# >>> x = pc('house', 'name'); print(len(x))
# [(1, ['natalie']),
#  (2, ['william']),
#  (3, ['elizabeth']),
#  (4, ['regina']),
#  (5, ['nicole']),
#  (6, ['oliver']),
#  (7, ['lucy'])]
# 7
# william does not live next to owner of a 2003 vehicle and william in 2 => house in 1 is not 2003
#
drop_inplace(df, (df['house'].isin([1, 3])) & (df['eyear'].isin([2003]) ))
# [(1, [21]),
#  (2, [22, 24, 25, 26, 27]),
#  (3, [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]),
# william in 2 and does not live to owner whose car is 26 years apart => 3 does not have year difference of 26
drop_inplace(df, (df['house'].isin([1, 3])) & (df['dyear'].isin([26]) ))
# >>> x = pc('everyday', 'eyear'); print(len(x))
# [('accord', [2006]),
#  ('dart', [2007]),
#  ('escort', [2005]),
#  ('impala', [2004]),
#  ('opel', [2001, 2002, 2003, 2004, 2005, 2006]),
#  ('taurus', [2001, 2002, 2004]),
#  ('yugo', [2002, 2003, 2004, 2005, 2006])]
# 7
# >>> x = pc('everyday', 'classic'); print(len(x))
# [('accord', ['el dorado']),
#  ('dart', ['ferrari']),
#  ('escort', ['corniche']),
#  ('impala', ['porsche']),
#  ('opel', ['countach', 'spider']),
#  ('taurus', ['corvair']),
#  ('yugo', ['countach', 'spider'])]
# 7
# the Yugo and the car owned by the person who also owned the Porsche are same year
# impala in 2004 => yugo in 2004
# no other everyday cars have same year => only impala and yugo are in 2004
drop_inplace(df, ~(df['eyear'].isin([2004])) & (df['everyday'].isin(['yugo', 'impala']) ))
drop_inplace(df, (df['eyear'].isin([2004])) & ~(df['everyday'].isin(['yugo', 'impala']) ))
# [('accord', [2006]),
# ('dart', [2007]),
# ('escort', [2005]),
# ('impala', [2004]),
# ('opel', [2001, 2002, 2003, 2005, 2006]),
# ('taurus', [2001, 2002]),
# ('yugo', [2004])]
# no other cars have same year and escort 2005, accord 2006  => no others are in 2005/2006
drop_inplace(df, (df['eyear'].isin([2005, 2006])) & ~(df['everyday'].isin(['escort', 'accord']) ))
# [('corniche', [1984]),
#  ('corvair', [1965, 1966]),
#  ('countach', [1979]),
# corniche in 1984 means no one else can be 1984 since countach 1979 and ferrari is 1979
drop_inplace(df, (df['cyear'].isin([1984])) & ~(df['classic'].isin(['corniche']) ))
#  ('oliver',
#   [11,
#    12,
#    13,
#    14,
#    15,
#    16,
#    17,
#    18,
#    19,
#    20,
#    21,
#    22,
#    23,
#    24,
#    25,
#    26,
#    27,
#    29,
#    30,
#    31,
#    32,
#    33,
#    34,
#    35,
#    36]),
#  ('regina',
#   [14,
#    15,
#    16,
#    17,
#    18,
#    19,
#    21,
#    22,
#    23,
#    24,
#    26,
#    27,
#    28,
#    29,
#    30,
#    31,
#    32,
#    33,
#    34,
#    36]),
#  ('william', [22, 24, 25])]
# William and Oliver live in even house numbers. One owns two cars that are 35 years apart in age.
# oliver must 35 years apart since william not possible
drop_inplace(df, (df['name'].isin(['oliver'])) & ~(df['dyear'].isin([35]) ))
# [('elizabeth', ['accord']),
#  ('lucy', ['dart']),
#  ('natalie', ['escort']),
#  ('nicole', ['taurus']),
#  ('oliver', ['opel']),
#  ('regina', ['impala']),
#  ('william', ['opel', 'yugo'])]
# 7
# oliver is opel => william is yugo
drop_inplace(df, (df['name'].isin(['oliver'])) & ~(df['everyday'].isin(['opel']) ))
drop_inplace(df, ~(df['name'].isin(['oliver'])) & (df['everyday'].isin(['opel']) ))
# three houses in the middle (... and the owner of a car manufactured in 2001
# [(1, [2005]),
#  (2, [2004]),
#  (3, [2006]),
#  (4, [2004]),
#  (5, [2001, 2002]),
#  (6, [2001, 2003]),
#  (7, [2007])]
# => house 5 is eyear in 2001
drop_inplace(df, (df['house'].isin([5])) & ~(df['eyear'].isin([2001]) ))
# 5. there exists a owner with 24 year difference
# 3. there exists an owner whose two cars were 26 years apart in age.
drop_inplace(df, (df['house'].isin([5])) & ~(df['eyear'].isin([2001]) ))
# [(1, [21]),
#  (2, [25]),
#  (3, [16, 17, 18, 19, 20, 21, 23, 24, 25]),
#  (4,
#   [14,
#    15,
#    16,
#    17,
#    18,
#    19,
#    21,
#    22,
#    23,
#    24,
#    26,
#    27,
#    28,
#    29,
#    30,
#    31,
#    32,
#    33,
#    34,
#    36]),
#  (5, [36]),
#  (6, [35]),
#  (7, [28])]
#
# => 24 year apart in house 3 and 26 year apart in house 4
drop_inplace(df, (df['house'].isin([3])) & ~(df['dyear'].isin([24]) ))
drop_inplace(df, (df['house'].isin([4])) & ~(df['dyear'].isin([26]) ))

# no other cars manufactured in same year and nicole/taurus in 2001 => oliver is 2003
drop_inplace(df, (df['name'].isin(['oliver'])) & (df['eyear'].isin([2001]) ))


#
#              name  house everyday  eyear    classic  cyear  dyear  hmatch
# 15851     william      2     yugo   2004   countach   1979     25   False
# 103969     oliver      6     opel   2003     spider   1968     35   False
# 132638  elizabeth      3   accord   2006  el dorado   1982     24   False
# 224555       lucy      7     dart   2007    ferrari   1979     28    True
# 233536    natalie      1   escort   2005   corniche   1984     21   False
# 326951     nicole      5   taurus   2001    corvair   1965     36   False
# 374602     regina      4   impala   2004    porsche   1978     26    True
#
# ANSWER:
# house        name  everyday  eyear    classic  cyear
#     1     natalie    escort   2005   corniche   1984
#     2     william      yugo   2004   countach   1979
#     3   elizabeth    accord   2006  el dorado   1982
#     4      regina    impala   2004    porsche   1978
#     5      nicole    taurus   2001    corvair   1965
#     6      oliver      opel   2003     spider   1968
#     7        lucy      dart   2007    ferrari   1979
print(df)

### single owner

# years apart
# -36
# -35
# -28
# 26 *
# 24 *
# -21
#
# -25
