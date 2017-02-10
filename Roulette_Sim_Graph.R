#Roulette Graph
#Using Martingale betting strategy
#And Simulator

#Alexander Booth
#February 3, 2017

#Imports
library(lubridate)
library(forecast)
library(devtools)
library(ggplot2)
library(dplyr)
options(scipen=999)

#init probability variables
p_win = 18/38
p_lose = 20/38
niterations = 10000
#this is the intial bet put down
#It get's doubled after each loss
init_bet <- 1
#maximum cash willing to lose
stop_loss = 130

goal = 1
final_probabilities = c(1:100)

#Loop for all target goals
while(goal <= 100){
  
  results = simulator(p_win, p_lose, niterations, init_bet, stop_loss, goal)
  
  #determine probability of reaching our goal
  prob = sum(results[1])/length(row(results[1]))
  final_probabilities[goal] = prob
  goal = goal + 1
}

#x-value
Winnings_goal = c(1:100)

#data frame
df = data.frame(Winnings_goal, final_probabilities)

#Plot dataframe
windowsFonts(Helvetica=windowsFont("Helvetica"))

gg<-ggplot(df, aes(y=final_probabilities, x=Winnings_goal)) + ylab("Final Probabilities") + xlab("Winnings Goal")
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
  legend.justification=c(0,0), legend.position= c(25, .25),
  legend.key = element_blank(),
  axis.line.x = element_line(size = rel(3), linetype = "solid",
                             colour = "#000505"),
  axis.ticks.length=unit(.25, "cm")
  # #                  panel.margin = unit(c(1,1,1,1), "cm"))
)

gg <- gg + theme(legend.direction = 'horizontal')

gg <- gg +  coord_cartesian(xlim = c(1, 100), ylim = c(0, 1)) + scale_colour_manual(values = c("#1C649C", "#F26C4F", "#7c808f", "#f1c40f",  "#32B5E3"))
gg <- gg + ggtitle("Winnings Goal vs Probability")
gg
