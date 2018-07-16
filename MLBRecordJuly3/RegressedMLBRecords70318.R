#Alexander Booth
#July 03, 2018

#Predicting MLB Records from Midseason

#References
#http://blog.philbirnbaum.com/2011/08/tango-method-of-regression-to-mean-kind.html
#https://fivethirtyeight.com/features/how-to-predict-mlb-records-from-early-results/
#https://www.oddsshark.com/mlb/mlb-season-win-totals

setwd("C:/Users/Alexander/Documents/baseball/MLBRecordJuly3")

#Load Libraries
library(ggplot2)
source("vnl_theme.R")

#Load Data
mlb.current.records <- read.csv("mlbStandings71618.csv")
mlb.current.records <- mlb.current.records[-31,]
mlb.2017 <- read.csv("mlbStandings2017.csv")
oddsShark.2018 <- read.csv("oddshark2018.csv")

mlb.current.recordsApril <- read.csv("mlbStandings42518.csv")

#############################################################################################
#Calculate sample of success %
#p = probability of success, q = probability of failure, perf.data = performance data
BayesRegressedMLBRecord <- function(p, q, team.W, team.L, perf.data, n.trials=10000){
  mlb.games <- 162
  
  #Calculate regressed games to add from p and q
  perf.sd <- sd(perf.data)
  luck.sd <- sqrt(p*q/mlb.games)
  talent.var <- perf.sd^2 - luck.sd^2
  talent.sd <- sqrt(talent.var)
  regr.games <- p*q/talent.var
  sqrt(p*q/regr.games) == talent.sd
  
  prior.alpha = regr.games * p
  prior.beta = regr.games * q
  
  #Get sampled success %
  set.seed(123)
  a.samples <- rbeta(n.trials, team.W + prior.alpha, team.L + prior.beta)
  
  return(a.samples)
}

#############################################################################################

# We can't assume that every team should go .500
# A smarter prior would be to regress towards pre-season estimates

team_abbrs <- unique(as.character(mlb.current.records$Tm))
n.trials = 10000

regressed.team2 <- rep(0, 30)
oddsShark.team2 <- rep(0,30)
loss100.team2 <- rep(0,30)
win100.team2 <- rep(0,30)
quantile05.team2 <- rep(0,30)
quantile95.team2 <- rep(0,30)

for(i in 1:length(team_abbrs)){
  currTeam <- team_abbrs[i]
  team.W <- mlb.current.records[mlb.current.records$Tm == currTeam, "W"]
  team.L <- mlb.current.records[mlb.current.records$Tm == currTeam, "L"]
  p_hat <- oddsShark.2018[oddsShark.2018$Team_Abbr == currTeam, "Win_Total_2018"] / 162
  q_hat <- 1 - p_hat
  oddsShark.team2[i] <- oddsShark.2018[oddsShark.2018$Team_Abbr == currTeam, "Win_Total_2018"]
  
  regressedSample.team <- BayesRegressedMLBRecord(p_hat, q_hat, team.W, team.L, mlb.2017$W.L.)
  regressed.team2[i] <- median(regressedSample.team) * 162
  loss100.team2[i] <- sum(regressedSample.team <= .3827) / n.trials
  win100.team2[i] <- sum(regressedSample.team >= .6172) / n.trials
  quantile05.team2[i] <- quantile(regressedSample.team, .05)
  quantile95.team2[i] <- quantile(regressedSample.team, .95)
}

df2 <- data.frame(team_abbrs, mlb.current.records$W, mlb.current.records$L, mlb.current.records$W.L., oddsShark.team2, 162 - oddsShark.team2, oddsShark.team2/162, round(regressed.team2,0), 162 - round(regressed.team2,0), round(regressed.team2,0)/162, quantile05.team2, quantile95.team2, loss100.team2, win100.team2)
names(df2) <- c("Team", "Current_Wins", "Current_Losses", "Current_WP%", "OddsShark_Wins", "OddsShark_Losses", "OddsShark_WP%",  "Regressed_Wins", "Regressed_Losses", "Regressed_WP%", ".05 WP% CI", ".95 WP% CI", "P(Lose100)", "P(Win100)")

write.csv(df2, "MLBRegressedRecord_OddsShark_July16.csv")

#############################################################################################

RegressTeamsAndPlot <- function(teamAbbr){
  tex.W <- mlb.current.records[mlb.current.records$Tm == teamAbbr, "W"]
  tex.L <- mlb.current.records[mlb.current.records$Tm == teamAbbr, "L"]
  
  tex.W.Apr <- mlb.current.recordsApril[mlb.current.recordsApril$Tm == teamAbbr, "W"]
  tex.L.Apr <- mlb.current.recordsApril[mlb.current.recordsApril$Tm == teamAbbr, "L"]
  
  p_tex <- oddsShark.2018[oddsShark.2018$Team_Abbr == teamAbbr, "Win_Total_2018"] / 162
  q_tex <- 1 - p_tex
  
  #Use 2017 data to calculate Variance of MLB Performance (WP%)
  perf.sd <- sd(mlb.2017$W.L.) #.07128
  #Normal Approximation of Binomial Distribution to calculate variance of luck
  luck.sd <- sqrt(p_tex*q_tex/162) #.03928
  #Solve for variance of talent
  talent.var <- perf.sd^2 - luck.sd^2
  talent.sd <- sqrt(talent.var) #.0595
  
  #Normal Approximation of Binomial Distribution to calculate games
  regr.games_tex <- p_tex*q_tex/talent.var #70.5
  sqrt(p_tex*q_tex/regr.games_tex) == talent.sd
  
  # Calculate our priors
  prior.alpha_tex = regr.games_tex * p_tex
  prior.beta_tex = regr.games_tex * q_tex
  set.seed(123)
  a.samples2 <- rbeta(n.trials, tex.W + prior.alpha_tex, tex.L + prior.beta_tex)
  median(a.samples2) * 162 #74.1
  sum(a.samples2 >= .500) / n.trials #15%
  sum(a.samples2 <= .3827) / n.trials #2.93%
  
  quantile(a.samples2, .95)
  quantile(a.samples2, .05)
  
  # #Plot
  # gg<-ggplot(data.frame(a.samples2), aes(a.samples2)) + ylab("Density") + xlab("Sampled Regressed WP%") + 
  #   geom_histogram(aes(y = ..density..), binwidth = 0.01, boundary = 0, closed = "left")
  # gg <- gg + vnl_theme() + xlim(0.2, 0.8)
  # gg <- gg + ggtitle(paste("Histogram for Bayesian Estimates of Regressed WP% (OddsShark)\n \n", teamAbbr, " 2018")) +
  #   stat_function(fun = dbeta, 
  #                 args = list(tex.W + prior.alpha_tex, tex.L + prior.beta_tex), 
  #                 lwd = 1.5, aes(colour = "July16 Beta Approx.")) +
  #   scale_colour_manual("", values = c("red")) + theme(legend.position="bottom")
  # print(gg)
  
  gg<-ggplot(data.frame(a.samples2), aes(a.samples2)) + ylab("Density") + xlab("Sampled Regressed WP%") + 
    vnl_theme() + xlim(0.2, 0.8)
  gg <- gg + ggtitle(paste("April vs July Bayesian Estimates of Regressed WP% (OddsShark)\n \n", teamAbbr, " 2018")) +
    stat_function(fun = dbeta, 
                  args = list(tex.W + prior.alpha_tex, tex.L + prior.beta_tex), 
                  lwd = 1.5, aes(colour = "July16 Beta Approx.")) +
    stat_function(fun = dbeta, 
                  args = list(tex.W.Apr + prior.alpha_tex, tex.L.Apr + prior.beta_tex), 
                  lwd = 1.5, aes(colour = "April18 Beta Approx.")) +
    scale_colour_manual("", values = c("red", "blue")) + theme(legend.position="bottom")
  print(gg)
}

#############################################################################################

#Texas Rangers Example
RegressTeamsAndPlot("TEX")

#Mets Example
RegressTeamsAndPlot("NYM")

#Reds Example
RegressTeamsAndPlot("CIN")

RegressTeamsAndPlot("BAL")
RegressTeamsAndPlot("KCR")
RegressTeamsAndPlot("OAK")
RegressTeamsAndPlot("BOS")
RegressTeamsAndPlot("SEA")
RegressTeamsAndPlot("TOR")
RegressTeamsAndPlot("LAA")


#####################################################

df <- read.csv("MLBRegressedRecord_OddsShark_July16.csv")

gg <- ggplot(df, aes(x=OddsShark_Wins, y=Regressed_Wins)) + 
  geom_point(colour="blue") + geom_text(aes(label=Team),hjust=-.1, vjust=-.1) + vnl_theme()
gg <- gg + ylab("July 16 Regressed Wins") + xlab("OddsShark Pre-Season Wins")
gg <- gg + ggtitle(paste("OddsShark Pre-Season Wins vs July 16 Regressed Wins"))
gg <- gg + stat_function(fun = function(x) x, linetype = "dashed")
gg

gg <- ggplot(df, aes(x=Regressed_Wins_Apr18, y=Regressed_Wins)) + 
  geom_point(colour="Red") + geom_text(aes(label=Team),hjust=-.1, vjust=-.1) + vnl_theme()
gg <- gg + ylab("July 16 Regressed Wins") + xlab("April 18 Regressed Wins")
gg <- gg + ggtitle(paste("April 18 Regressed Wins vs July 16 Regressed Wins"))
gg <- gg + stat_function(fun = function(x) x, linetype = "dashed")
gg