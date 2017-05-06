#Baseball Strikeouts Vs Moose Population
#Author: Alexander Booth

#Imports
library(readr)
library(dplyr)
library(ggplot2)
library(stats)

#Read Data
Teams <- read_csv("C:\\Users\\Alexander\\Documents\\Northwestern\\Spring 2017\\401\\Week 4\\Teams.csv")
View(Teams)

isleRoyale <- read_csv("C:\\Users\\Alexander\\Documents\\Northwestern\\Spring 2017\\401\\Week 4\\isleroyale_graph_data_28Dec2011.csv", 
                       skip = 1)
View(isleRoyale)

#Subset moose population
isleSub <- isleRoyale[isleRoyale$Year >= 2002, ]
moosePop <- isleSub$`moose abundance`
moosePop <- moosePop[!is.na(moosePop)]

years <- isleSub$Year
years <- years[!is.na(years)]

#Subset team data
teamSub <- subset(Teams, (yearID >= 2002 & yearID <= 2011))
teamSub <- teamSub[, c("yearID", "franchID", "SOA")]

#sanity check
teamIds <- unique(teamSub$franchID)
length(unique(teamIds)) #30

#Get the correlation for each team
corrs = {}
for(teamId in teamIds){
  teamData <- teamSub[teamSub$franchID == teamId,]
  strikeOuts <- teamData$SOA
  corr = cor(strikeOuts, moosePop)
  corrs[teamId] = corr
  #this prints each correlation test
  print(cor.test(strikeOuts, moosePop))
}

print(corrs)
maxCorr <- max(corrs) #ARIZONA

#Max team data
maxTeamId <- "ARI"
maxTeamData <- teamSub[teamSub$franchID == maxTeamId,]
maxTeamStrikeOuts <- maxTeamData$SOA
maxTest <- cor.test(moosePop, maxTeamStrikeOuts)

#data to graph
fg <- data.frame(moosePop, maxTeamStrikeOuts)

#linear model
reg <- lm(maxTeamStrikeOuts~moosePop, data=fg)
coeff = coefficients(reg)
intcpt <- coeff[2]
slp <- coeff[1]

windowsFonts(Helvetica=windowsFont("Helvetica"))

#Make graph
gg<-ggplot(fg, aes(y=maxTeamStrikeOuts, x=moosePop)) + ylab("Arizona SOs") + xlab("Moose Population")
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
gg <- gg +  coord_cartesian(xlim = c(250, 1200), ylim = c(1000, 1400)) + scale_colour_manual(values = c("#1C649C", "#F26C4F", "#7c808f", "#f1c40f",  "#32B5E3"))
gg <- gg + ggtitle("Arizona SOs vs Moose Population, 2002-2011") + theme(plot.title = element_text(hjust = 0.5))
gg <- gg + annotate("text", label = "R^2 = .72", x=1100, y = 1050, fontface = 2, colour = "#000505")
gg
#ggsave(file = 'Arizona SOs vs Moose Population.png', plot = gg, dpi = 1200, w=7, h=4.66666, unit="in" )