setwd("C:/Users/Alexander/Downloads/lahman-csv_2014-02-14")
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

fg = teams %>% filter(yearID == 2001) %>% select(salary, W)
fg$salary = fg$salary/1000000

fg2 = teams %>% filter(yearID == 2001, teamID == "OAK") %>% select(salary, W)
fg2$salary = fg2$salary/1000000

fg3 = teams %>% filter(yearID == 2001, teamID == "NYA") %>% select(salary, W)
fg3$salary = fg3$salary/1000000

windowsFonts(Helvetica=windowsFont("Helvetica"))

gg<-ggplot(fg, aes(y=W, x=salary)) + ylab("Wins") + xlab("Salaries (Millions of $)")
gg<- gg + geom_point(size = 5, color = "#5D5D81")

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

gg <- gg +  coord_cartesian(xlim = c(0, 120), ylim = c(40, 120)) + scale_colour_manual(values = c("#1C649C", "#F26C4F", "#7c808f", "#f1c40f",  "#32B5E3"))
gg <- gg + geom_point(data = fg2, color = "#61B329", size = rel(5)) +
      geom_text(colour='#000505', data = NULL, x = 33.5, y = 107, label = "OAK", size = 4)
gg <- gg + geom_point(data = fg3, color = "#4169e1", size = rel(5))+
  geom_text(colour='#000505', data = NULL, x = 112, y = 99, label = "NYY", size = 4)
gg <- gg + ggtitle("Salaries Vs Wins 2001")
gg
#ggsave(file = 'SalVsWins_2001.png', plot = gg, dpi = 1200, w=7, h=4.66666, unit="in" )