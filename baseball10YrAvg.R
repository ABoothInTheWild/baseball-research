setwd("C:/Users/Alexander/Documents/baseball/baseballdatabank-master/core")
library(lubridate)
library(forecast)
library(devtools)
library(ggplot2)
library(dplyr)
options(scipen=999)

teams <- read.csv("Teams.csv", stringsAsFactors=FALSE)
teams <- filter(teams, yearID >= 1985)
teams <- select(teams, yearID, teamID, Rank, R, RA, G, W, H, BB, HBP, AB, SF, HR, X2B, X3B)

View(teams)

filter(teams, yearID == 2001, teamID == "OAK")["W"]

salaries <- read.csv("Salaries.csv", stringsAsFactors=FALSE)
salaries <- filter(salaries, yearID >= 1985)

salaries_by_yearID_teamID= salaries %>% 
  group_by(yearID, teamID) %>%
  summarise(sum(salary)) 

teams = full_join(teams, salaries_by_yearID_teamID)
teams$salary = teams$`sum(salary)`
teams$`sum(salary)` = NULL

filter(teams, yearID == 2001, teamID == "OAK")["salary"]

fg = teams %>% filter(yearID >= 2000, yearID <= 2005) %>% 
  group_by(teamID) %>% summarise(mean(salary), mean(W))
fg$salary = fg$`mean(salary)`/1000000
fg$salary = (fg$salary - median(fg$salary))/mad(fg$salary)
fg$W = fg$`mean(W)`

fg2 = fg %>% filter(teamID == "OAK") %>% select(salary, W)
fg2$salary = (fg2$salary - median(fg$salary))/mad(fg$salary)

fg3 = fg %>% filter(teamID == "NYA") %>% select(salary, W)
fg3$salary = (fg3$salary - median(fg$salary))/mad(fg$salary)

fg$salary <- (fg$salary - median(fg$salary))/mad(fg$salary)

windowsFonts(Helvetica=windowsFont("Helvetica"))

gg<-ggplot(fg, aes(y=W, x=salary)) + ylab("Average Wins") + xlab("Normalized Salary")
gg<- gg + geom_point(size = 5, color = "#5D5D81") + geom_smooth(fill = NA, colour= "#000505", size= rel(1.25), method = "lm")

gg <- gg + theme(
  panel.grid.minor = element_blank(),
  panel.grid.major.x = element_line(colour="#FEFCFD", linetype='dashed'),
  panel.grid.major.y = element_line(colour="#FEFCFD", linetype='dashed'),
  axis.line.y = element_line(size = rel(3), linetype = "solid",
                             colour = "#000505"),
  plot.background = element_rect(fill = "#BFCDE0"),
  panel.background = element_rect(fill = "#BFCDE0"),
  text=element_text(family="Helvetica", face="bold",  colour="#000505"),
  axis.text = element_text(colour = "#000505", size=rel(1)),
  
  axis.ticks = element_line(colour = "#000505", size=rel(1)),
  legend.background = element_rect(fill="transparent"),
  legend.text = element_text(size=rel(.75)),
  legend.title=element_blank(),
  legend.justification=c(0,0), legend.position= c(.01, -.03),
  legend.key = element_blank(),
  axis.line.x = element_line(size = rel(3), linetype = "solid",
                             colour = "#000505"),
  axis.ticks.length=unit(.25, "cm")
  # #                  panel.margin = unit(c(1,1,1,1), "cm"))
)

gg <- gg + theme(legend.direction = 'horizontal')

gg <- gg +  coord_cartesian(xlim = c(-3, 5), ylim = c(60, 100)) + scale_colour_manual(values = c("#1C649C", "#F26C4F", "#7c808f", "#f1c40f",  "#32B5E3"))
gg <- gg + geom_point(data = fg2, color = "#61B329", size = rel(5)) +
  geom_text(colour='#000505', data = NULL, x = -.8, y = 97, label = "OAK", size = 4)
gg <- gg + geom_point(data = fg3, color = "#4169e1", size = rel(5))+
  geom_text(colour='#000505', data = NULL, x = 3.6, y = 95, label = "NYY", size = 4)
gg <- gg + ggtitle("Normalized Salaries vs Avg Wins 2000-2005")
gg
#ggsave(file = 'NormSal_vs_AvgW_0005.png', plot = gg, dpi = 1200, w=7, h=4.66666, unit="in" )

tempLm = lm(W ~ salary, data = fg)
sqrt(summary(tempLm)$r.squared)