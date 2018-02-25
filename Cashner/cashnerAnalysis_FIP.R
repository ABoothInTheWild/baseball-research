#Alexander Booth

#Libraries
library(readr)
library(ggplot2)

#Load data
Teams <- read_csv("https://raw.githubusercontent.com/ABoothInTheWild/baseball-research/master/Teams.csv")
pitchers_full <- read.csv("G:/Other Docs/blurp/Pitching.csv", stringsAsFactors=FALSE)
fangraphs_constants <- read_csv("G:/Other Docs/blurp/FanGraphs_FIP_Constants.csv")

#Load Prewritten functions
source("G:/Other Docs/blurp/vnl_theme.R")

#subset by year and variable
teamSub <- subset(Teams, (yearID > 1996 & yearID <= 2016))
teamSub <- teamSub[, c("yearID", "franchID", "IPouts", "HA", "BBA", "SOA", "RA",
                         "ERA", "HRA")]

#sanity check
teamIds <- unique(teamSub$franchID)
length(unique(teamIds)) #30

#Create statistics
teamSub["BRA"] <- teamSub$HA + teamSub$BBA  #base runners allowed
teamSub["KINN"] <- teamSub$SOA / (teamSub$IPouts/3)  #strikeouts per inning
teamSub["KPer9"] <-(teamSub$SOA / (teamSub$IPouts/3)) * 9  #strikeouts per 9 innings
teamSub["WHIP"] <-(teamSub$BRA / (teamSub$IPouts/3))   #Walks plus Hits per Inning Pitched
teamSub["FIP"] <- apply(teamSub, 1, function(x) (((13*as.numeric(x["HRA"])+(3*(as.numeric(x["BBA"])))
                                                     - (2*as.numeric(x["SOA"])))/(as.numeric(x["IPouts"])/3)) +
                                                     fangraphs_constants[fangraphs_constants$Season == x["yearID"],]$cFIP))
#Check Correlations
cor(teamSub$FIP, teamSub$RA)
fit <- lm(RA ~ FIP, data=teamSub)
summary(fit)

#Regression Plot
gg<-ggplot(teamSub, aes(x=teamSub$FIP, y=teamSub$RA)) + geom_point(aes(color = "Team FIP"), size = 2) + 
  ylab("Runs Allowed") + xlab("FIP") + 
  geom_smooth(method='lm', lwd = 1.5, aes(color = "Regression Line")) + vnl_theme()
gg <- gg + ggtitle(paste("Team Runs Allowed vs FIP")) + 
  scale_colour_manual("", values = c("blue", "black")) + theme(legend.position="right")
gg

#LOL
gg<-ggplot(teamSub, aes(x=teamSub$ERA, y=teamSub$RA)) + geom_point(aes(color = "Team ERA"), size = 2) + 
  ylab("Runs Allowed") + xlab("ERA") + 
  geom_smooth(method='lm', lwd = 1.5, aes(color = "Regression Line")) + vnl_theme()
gg <- gg + ggtitle(paste("Team Runs Allowed vs ERA")) + 
  scale_colour_manual("", values = c("blue", "black")) + theme(legend.position="right")
gg

#Variance
var(teamSub$ERA)
var(teamSub$FIP)

#Plot Team ERA
gg<-ggplot(teamSub, aes(teamSub$ERA)) + ylab("Density") + xlab("ERA") + 
  geom_histogram(aes(y = ..density..), binwidth = 0.25, boundary = 0, closed = "left")
gg <- gg + vnl_theme() + xlim(2.5, 6) + ylim(0,1)
gg <- gg + ggtitle(paste("Histogram for Team ERA")) +
  stat_function(fun = dnorm, 
                args = list(mean(teamSub$ERA), sd(teamSub$ERA)), 
                lwd = 1.5, aes(colour = "Normal Approximation")) +
  scale_colour_manual("", values = c("red")) + theme(legend.position="bottom")
gg

#Plot Team FIP
gg<-ggplot(teamSub, aes(teamSub$FIP)) + ylab("Density") + xlab("FIP") + 
  geom_histogram(aes(y = ..density..), binwidth = 0.25, boundary = 0, closed = "left")
gg <- gg + vnl_theme() + xlim(2.5, 6) + ylim(0,1)
gg <- gg + ggtitle(paste("Histogram for Team FIP")) +
  stat_function(fun = dnorm, 
                args = list(mean(teamSub$FIP), sd(teamSub$FIP)), 
                lwd = 1.5, aes(colour = "Normal Approximation")) +
  scale_colour_manual("", values = c("red")) + theme(legend.position="bottom")
gg

##########################################################################

#Individual Pitchers
pitchers <- pitchers_full[(pitchers_full$yearID > 1996) &
                          (pitchers_full$stint == 1) &
                          (pitchers_full$IPouts >= 360),]

pitchers["IP"] <- pitchers$IPouts / 3
pitchers <- na.omit(pitchers)

#Create statistics
pitchers["BRA"] <- pitchers$H + pitchers$BB #base runners allowed
pitchers["KINN"] <- pitchers$SO / pitchers$IP  #strikeouts per inning
pitchers["KPer9"] <- pitchers$KINN * 9  #strikeouts per 9 innings
pitchers["WHIP"] <- pitchers$BRA / pitchers$IP   #Walks plus Hits per Inning Pitched
pitchers["KRate"] <- pitchers$SO / pitchers$BFP #SO percent
pitchers["BBRate"] <- pitchers$BB / pitchers$BFP #Walk percent
pitchers["HRRate"] <- pitchers$HR / pitchers$BFP #Home Run Rate
pitchers["BABIP"] <- (pitchers$H - pitchers$HR)/(pitchers$BFP - pitchers$BB - pitchers$SH - pitchers$SF - pitchers$SO - pitchers$HR)

#FIP
pitchers["FIP"] <- apply(pitchers, 1, function(x) (((13*as.numeric(x["HR"])+(3*(as.numeric(x["BB"])+as.numeric(x["HBP"])))
                                                       - (2*as.numeric(x["SO"])))/as.numeric(x["IP"])) +
                                                       fangraphs_constants[fangraphs_constants$Season == x["yearID"],]$cFIP))
#Difference
pitchers["FIP_ERA"] <- pitchers["FIP"] - pitchers["ERA"]

#Check Correlations
cor(pitchers$FIP, pitchers$R)
cor(pitchers$ERA, pitchers$R)

#Variance
var(pitchers$FIP)
var(pitchers$ERA)

fit2 <- lm(R ~ FIP, data=pitchers)
summary(fit2)

#Regression Plot
gg<-ggplot(pitchers, aes(x=FIP, y=R)) + geom_point(aes(color = "Pitcher FIP"), size = 2) + 
  ylab("Runs Allowed") + xlab("FIP") + 
  geom_smooth(method='lm', lwd = 1.5, aes(color = "Regression Line")) + vnl_theme()
gg <- gg + ggtitle(paste("Pitcher Runs Allowed vs FIP")) + 
  scale_colour_manual("", values = c("black", "blue")) + theme(legend.position="right")
gg

#Plot Pitcher ERA
gg<-ggplot(pitchers, aes(pitchers$ERA)) + ylab("Density") + xlab("ERA") + 
  geom_histogram(aes(y = ..density..), binwidth = 0.25, boundary = 0, closed = "left")
gg <- gg + vnl_theme() + xlim(1, 7) + ylim(0,.6)
gg <- gg + ggtitle(paste("Histogram for Pitcher ERA")) +
  stat_function(fun = dnorm, 
                args = list(mean(pitchers$ERA), sd(pitchers$ERA)), 
                lwd = 1.5, aes(colour = "Normal Approximation")) +
  scale_colour_manual("", values = c("blue")) + theme(legend.position="bottom")
gg

#Plot Pitcher FIP
gg<-ggplot(pitchers, aes(pitchers$FIP)) + ylab("Density") + xlab("FIP") + 
  geom_histogram(aes(y = ..density..), binwidth = 0.25, boundary = 0, closed = "left")
gg <- gg + vnl_theme() + xlim(1, 7) + ylim(0,.6)
gg <- gg + ggtitle(paste("Histogram for Pitcher FIP")) +
  stat_function(fun = dnorm, 
                args = list(mean(pitchers$FIP), sd(pitchers$FIP)), 
                lwd = 1.5, aes(colour = "Normal Approximation")) +
  scale_colour_manual("", values = c("blue")) + theme(legend.position="bottom")
gg

#Plot Pitcher Difference
gg<-ggplot(pitchers, aes(pitchers$FIP_ERA)) + ylab("Density") + xlab("FIP-ERA") + 
  geom_histogram(aes(y = ..density..), binwidth = 0.25, boundary = 0, closed = "left")
gg <- gg + vnl_theme() + xlim(-3, 3) + ylim(0,.75)
gg <- gg + ggtitle(paste("Histogram for Pitcher FIP-ERA")) +
  stat_function(fun = dnorm, 
                args = list(mean(pitchers$FIP_ERA), sd(pitchers$FIP_ERA)), 
                lwd = 1.5, aes(colour = "Normal Approximation")) +
  scale_colour_manual("", values = c("blue")) + theme(legend.position="bottom")
gg

pnorm(1.2, mean(pitchers$FIP_ERA), sd(pitchers$FIP_ERA), lower.tail = F)

sd(pitchers$BABIP)

#Plot Pitcher BABIP
gg<-ggplot(pitchers, aes(pitchers$BABIP)) + ylab("Density") + xlab("BABIP") + 
  geom_histogram(aes(y = ..density..), binwidth = 0.01, boundary = 0, closed = "left")
gg <- gg + vnl_theme() + xlim(0.2, 0.4) + ylim(0,23)
gg <- gg + ggtitle(paste("Histogram for Pitcher BABIP")) +
  stat_function(fun = dnorm, 
                args = list(mean(pitchers$BABIP), sd(pitchers$BABIP)), 
                lwd = 1.5, aes(colour = "Normal Approximation")) +
  scale_colour_manual("", values = c("darkgreen")) + theme(legend.position="bottom")
gg

df <- pitchers[pitchers$playerID == "cashnan01",]