temp = list()

for(year in c(1996, 1997, 1998, 1999, 2000)){
  fg = teams %>% filter(yearID == year) %>% select(salary, W)
  fg$salary = fg$salary/1000000
  
  tempLm = lm(W ~ salary, data = fg)
  
  temp = append(temp, summary(tempLm)$adj.r.squared)
}

temp = as.numeric(temp)
mean(temp)

temp2 = list()

for(year in c(2001, 2002, 2003, 2004, 2005)){
  fg = teams %>% filter(yearID == year) %>% select(salary, W)
  fg$salary = fg$salary/1000000
  
  tempLm = lm(W ~ salary, data = fg)
  
  temp2 = append(temp2, summary(tempLm)$adj.r.squared)
}

temp2 = as.numeric(temp2)
mean(temp2)

mean(temp) - mean(temp2)

temp3 = list()

for(year in c(2009, 2010, 2011, 2012, 2013)){
  fg = teams %>% filter(yearID == year) %>% select(salary, W)
  fg$salary = fg$salary/1000000
  
  tempLm = lm(W ~ salary, data = fg)
  
  temp3 = append(temp3, summary(tempLm)$adj.r.squared)
}

temp3 = as.numeric(temp3)
mean(temp3)
mean(temp) - mean(temp3)