#Alexander Booth
#April 25, 2018

#Predicting MLB Records from Small Sample Size

#References
#http://blog.philbirnbaum.com/2011/08/tango-method-of-regression-to-mean-kind.html
#https://fivethirtyeight.com/features/how-to-predict-mlb-records-from-early-results/
#https://www.oddsshark.com/mlb/mlb-season-win-totals

setwd("~/MLBRecordApril18")

#Load Libraries
library(ggplot2)
source("vnl_theme.R")

#Load Data
mlb.current.records <- read.csv("mlbStandings42518.csv")
mlb.2017 <- read.csv("mlbStandings2017.csv")
oddsShark.2018 <- read.csv("oddshark2018.csv")

###################################################################################

# We need to estimate the number of games to add to our W/L
# Assuming Talent and Luck are independent:

# var(actual performance e.g. WP%) = var(talent) + var(luck)

# Average win/loss% is .500
p <- .5
q <- .5

#Use 2017 data to calculate Variance of MLB Performance (WP%)
perf.sd <- sd(mlb.2017$W.L.) #.07128
#Normal Approximation of Binomial Distribution to calculate variance of luck
luck.sd <- sqrt(p*q/162) #.03928
#Solve for variance of talent
talent.var <- perf.sd^2 - luck.sd^2
talent.sd <- sqrt(talent.var) #.0595

#Normal Approximation of Binomial Distribution to calculate games
regr.games <- p*q/talent.var #70.6
sqrt(p*q/regr.games) == talent.sd

# Calculate our priors
prior.alpha = regr.games * p
prior.beta = regr.games * q

#Show Plot
set.seed(123)
n.trials = 10000
test.samples <- rbeta(n.trials, prior.alpha, prior.beta)
median(test.samples) * 162 #80.9 ~ 81

#Plot
gg<-ggplot(data.frame(test.samples), aes(test.samples)) + ylab("Density") + xlab("Test Regressed WP%") + 
  geom_histogram(aes(y = ..density..), binwidth = 0.01, boundary = 0, closed = "left")
gg <- gg + vnl_theme()
gg <- gg + ggtitle(paste("Histogram for Bayesian Estimates of Test Regressed WP%")) +
  stat_function(fun = dbeta, 
                args = list(prior.alpha, prior.beta), 
                lwd = 1.5, aes(colour = "Beta Approximation")) +
  scale_colour_manual("", values = c("blue")) + theme(legend.position="bottom")
gg

#Texas Rangers Example
tex.W <- mlb.current.records[mlb.current.records$Tm == "TEX", "W"]
tex.L <- mlb.current.records[mlb.current.records$Tm == "TEX", "L"]

set.seed(123)
n.trials = 10000
a.samples <- rbeta(n.trials, tex.W + prior.alpha, tex.L + prior.beta)
median(a.samples) * 162 #73.2
sum(a.samples >= .500) / n.trials #18.08%
sum(a.samples >= .6172) / n.trials #0%
sum(a.samples <= .3827) / n.trials #8.29

#Plot
gg<-ggplot(data.frame(a.samples), aes(a.samples)) + ylab("Density") + xlab("Sampled Regressed WP%") + 
  geom_histogram(aes(y = ..density..), binwidth = 0.01, boundary = 0, closed = "left")
gg <- gg + vnl_theme()
gg <- gg + ggtitle(paste("Histogram for Bayesian Estimates of Regressed WP% (.500)\n \n Texas Rangers 2018")) +
  stat_function(fun = dbeta, 
                args = list(tex.W + prior.alpha, tex.L + prior.beta), 
                lwd = 1.5, aes(colour = "Beta Approximation")) +
  scale_colour_manual("", values = c("red")) + theme(legend.position="bottom")
gg

#############################################################################################
#Calculate sample of success %
#p = probability of success, q = probability of failure, perf.data = performance data
BayesRegressedMLBRecord <- function(p, q, team.W, team.L, perf.data, n.trials=10000){
  mlb.games <- 162
  
  #Calculate regressed games to add from p and q
  perf.sd <- sd(perf.data) #.07128
  luck.sd <- sqrt(p*q/mlb.games) #.03928
  talent.var <- perf.sd^2 - luck.sd^2
  talent.sd <- sqrt(talent.var) #.0595
  regr.games <- p*q/talent.var #70.6
  sqrt(p*q/regr.games) == talent.sd
  
  prior.alpha = regr.games * p
  prior.beta = regr.games * q
  
  #Get sampled success %
  set.seed(123)
  a.samples <- rbeta(n.trials, team.W + prior.alpha, team.L + prior.beta)
  
  return(a.samples)
}

#############################################################################################
#Get Every Team

team_abbrs <- unique(as.character(mlb.current.records$Tm))
regressed.team <- rep(0, 30)

for(i in 1:length(team_abbrs)){
  currTeam <- team_abbrs[i]
  team.W <- mlb.current.records[mlb.current.records$Tm == currTeam, "W"]
  team.L <- mlb.current.records[mlb.current.records$Tm == currTeam, "L"]
  regressedSample.team <- BayesRegressedMLBRecord(.5, .5, team.W, team.L, mlb.2017$W.L.)
  regressed.team[i] <- median(regressedSample.team) * 162
}

df <- data.frame(team_abbrs, mlb.current.records$W, mlb.current.records$L, mlb.current.records$W.L., round(regressed.team,0), 162 - round(regressed.team,0), round(regressed.team,0)/162)
names(df) <- c("Team", "Current_Wins", "Current_Losses", "Current_WP%", "Regressed_Wins", "Regressed_Losses", "Regressed_WP%")

#write.csv(df, "MLBRegressedRecord_500.csv")

#############################################################################################

# We can't assume that every team should go .500
# A smarter prior would be to regress towards pre-season estimates

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

#write.csv(df2, "MLBRegressedRecord_OddsShark.csv")

#############################################################################################

p_tex <- oddsShark.2018[oddsShark.2018$Team_Abbr == "TEX", "Win_Total_2018"] / 162
q_tex <- 1 - p_tex

#Use 2017 data to calculate Variance of MLB Performance (WP%)
perf.sd <- sd(mlb.2017$W.L.) #.07128
#Normal Approximation of Binomial Distribution to calculate variance of luck
luck.sd <- sqrt(p_tex*q_tex/162) #.03928
#Solve for variance of talent
talent.var <- perf.sd^2 - luck.sd^2
talent.sd <- sqrt(talent.var) #.0595

#Normal Approximation of Binomial Distribution to calculate games
regr.games_tex <- p_tex*q_tex/talent.var #70.6
sqrt(p_tex*q_tex/regr.games_tex) == talent.sd

# Calculate our priors
prior.alpha_tex = regr.games_tex * p_tex
prior.beta_tex = regr.games_tex * q_tex
set.seed(123)
a.samples2 <- rbeta(n.trials, tex.W + prior.alpha_tex, tex.L + prior.beta_tex)
median(a.samples2) * 162 #70.6
sum(a.samples2 >= .500) / n.trials #10.7%
sum(a.samples2 <= .3827) / n.trials #14.35%

quantile(a.samples2, .95)
quantile(a.samples2, .05)


#Plot
gg<-ggplot(data.frame(a.samples2), aes(a.samples2)) + ylab("Density") + xlab("Sampled Regressed WP%") + 
  geom_histogram(aes(y = ..density..), binwidth = 0.01, boundary = 0, closed = "left")
gg <- gg + vnl_theme()
gg <- gg + ggtitle(paste("Histogram for Bayesian Estimates of Regressed WP% (OddsShark)\n \n Texas Rangers 2018")) +
  stat_function(fun = dbeta, 
                args = list(tex.W + prior.alpha_tex, tex.L + prior.beta_tex), 
                lwd = 1.5, aes(colour = "Beta Approximation")) +
  scale_colour_manual("", values = c("red")) + theme(legend.position="bottom")
gg
