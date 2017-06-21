#The Death of the Batting Average
#Alexander Booth
#6/20/2017

#Imports
library(readr)
library(dplyr)
library(ggplot2)
library(stats)

#Set Working directory
setwd("C:\\Users\\Alexander\\Documents\\baseball")

#Load data
Teams <- read_csv("baseballdatabank-master\\core\\Teams.csv")
View(Teams)

#subset by year and variable
teamSub <- subset(Teams, (yearID >= 1995 & yearID <= 2014))
teamSub <- teamSub[, c("yearID", "franchID", "W", "R", "H", "2B", "3B", "HR", "BB", "AB", "IPouts", "HA", "BBA", "SOA", "ERA")]

#sanity check
teamIds <- unique(teamSub$franchID)
length(unique(teamIds)) #30

#Create statistics
teamSub["BA"] <- teamSub$H/teamSub$AB
teamSub["OBP"] <- (teamSub$H + teamSub$BB)/teamSub$AB
teamSub["SLG"] <- (teamSub$H + teamSub["2B"] + 2*teamSub["3B"] + 3*teamSub$HR)/teamSub$AB
teamSub["OPS"] <- teamSub$OBP + teamSub$SLG

#Check Correlations
cor(teamSub$BA, teamSub$R)
cor(teamSub$OBP, teamSub$R)
cor(teamSub$SLG, teamSub$R)
cor(teamSub$OPS, teamSub$R)

#Linear Model of all three statistics
#Not useful due to mulitcollinearity
fit <- lm(R ~ OBP + SLG + BA, data=teamSub)
summary(fit)
confint(fit, "BA", .95)

#Linear Models for each statistic
summary(lm(R ~ BA, data=teamSub))
summary(lm(R ~ OBP, data=teamSub))
summary(lm(R ~ SLG, data=teamSub))
summary(lm(R ~ OPS, data=teamSub))

#Graph for Runs Scored by Batting Average
windowsFonts(Helvetica=windowsFont("Helvetica"))

gg<-ggplot(teamSub, aes(y=R, x=BA)) + ylab("Runs Scored") + xlab("Batting Average")
gg<- gg + geom_point(size = 5, color = "#32B5E3") + geom_smooth(fill = NA, colour= "#1C649C", size= rel(1.5), method = "lm")

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
gg <- gg +  coord_cartesian(xlim = c(.225, .3), ylim = c(0, 1050)) + scale_colour_manual(values = c("#1C649C", "#F26C4F", "#7c808f", "#f1c40f",  "#32B5E3"))
gg <- gg + ggtitle("Runs Scored by Batting Average") + theme(plot.title = element_text(hjust = 0.5))
gg <- gg + annotate("text", label = "R^2 = .66", x=.29, y = 200, fontface = 2, colour = "#000505")
gg
#ggsave(file = 'RunsScored_BA.png', plot = gg, dpi = 1200, w=7, h=4.66666, unit="in" )


#Graph for Runs Scored by OPS
windowsFonts(Helvetica=windowsFont("Helvetica"))

gg<-ggplot(teamSub, aes(y=R, x=OPS)) + ylab("Runs Scored") + xlab("On-Base Plus Slugging (OPS)")
gg<- gg + geom_point(size = 5, color = "#32B5E3") + geom_smooth(fill = NA, colour= "#1C649C", size= rel(1.5), method = "lm")

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
gg <- gg +  coord_cartesian(xlim = c(.64, .9), ylim = c(0, 1050)) + scale_colour_manual(values = c("#1C649C", "#F26C4F", "#7c808f", "#f1c40f",  "#32B5E3"))
gg <- gg + ggtitle("Runs Scored by OPS") + theme(plot.title = element_text(hjust = 0.5))
gg <- gg + annotate("text", label = "R^2 = .89", x=.84, y = 200, fontface = 2, colour = "#000505")
gg
#ggsave(file = 'RunsScored_OPS.png', plot = gg, dpi = 1200, w=7, h=4.66666, unit="in" )

