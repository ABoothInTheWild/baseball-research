#Alexander Booth
#July 23, 2018

#MLB Playoff Odds

#References
#http://blog.philbirnbaum.com/2011/08/tango-method-of-regression-to-mean-kind.html
#https://fivethirtyeight.com/features/how-to-predict-mlb-records-from-early-results/
#https://www.oddsshark.com/mlb/mlb-season-win-totals

#Load Libraries
library(ggplot2)
source("C:/Users/abooth/Documents/Docs/vnl_theme.R")

#Load Data
#mlb.current.records <- read.csv("C:/Users/abooth/Documents/Docs/mlbStandings71618.csv")
#mlb.current.records <- mlb.current.records[-31,]
mlb.current.records <- read.csv("C:/Users/abooth/Documents/Docs/mlbStandings42518.csv")
mlb.2017 <- read.csv("C:/Users/abooth/Documents/Docs/mlbStandings2017.csv")
oddsShark.2018 <- read.csv("C:/Users/abooth/Documents/Docs/oddshark2018.csv")

#############################################################################################
#Calculate sample of success %
#p = probability of success, q = probability of failure, perf.data = performance data
BayesParamsForTeams <- function(p, q, team.W, team.L, perf.data){
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
  
  return(c(team.W, prior.alpha, team.L, prior.beta))
}

##########################################################################

#Division Winners

team_abbrs <- unique(as.character(mlb.current.records$Tm))
n_trials = 100000

#Name Divisions
AL_East <- c("BOS", "NYY", "TOR", "BAL", "TBR")
AL_Central <- c("CLE", "DET", "CHW", "MIN", "KCR")
AL_West <- c("TEX", "HOU", "SEA", "OAK", "LAA")
NL_East <- c("PHI", "WSN", "MIA", "NYM", "ATL")
NL_Central <- c("STL", "CHC", "MIL", "PIT", "CIN")
NL_West <- c("LAD", "SFG", "SDP", "ARI", "COL")

Divisions <- list(AL_West, AL_Central, AL_East, NL_West, NL_Central, NL_East)
AL <- list(AL_West, AL_Central, AL_East)
NL <- list(NL_West, NL_Central, NL_East)

#Loop through each division
set.seed(123)
finals = data.frame()
for(z in 1:length(Divisions)){
  div <- unlist(Divisions[z])
  
  parms <- c()
  #For each team in the division, get their beta distribution parameters
  for(i in 1:length(div)){
    currTeam <- div[i]
    team.W <- mlb.current.records[mlb.current.records$Tm == currTeam, "W"]
    team.L <- mlb.current.records[mlb.current.records$Tm == currTeam, "L"]
    p_hat <- oddsShark.2018[oddsShark.2018$Team_Abbr == currTeam, "Win_Total_2018"] / 162
    q_hat <- 1 - p_hat
    team.params <- BayesParamsForTeams(p_hat, q_hat, team.W, team.L, mlb.2017$W.L.)
    parms <- append(parms, team.params)
  }
  
  #For each trial
  sim.results <- rep(0,5)
  for(i in 1:n_trials){
    results <- rep(0,5)
    x <- 1
    #sample from beta for each team
    for(j in seq(1, 20, by=4)){
      results[x] = round(rbeta(1, parms[j] + parms[j+1], parms[j+2] + parms[j+3]) * 162,0)
      x <- x + 1
    }
    #increment the winner
    sim.results[which.max(results)] = sim.results[which.max(results)] + 1
  }
  #get percentage
  sim.results = sim.results/n_trials
  #append all the divisions
  finals <- rbind(finals,cbind.data.frame(div, as.numeric(sim.results)))
}

#Loop through each league
set.seed(456)
parms <- c()
for(z in 1:length(AL)){
  div <- unlist(AL[z])
  
  #For each team in the division, get their beta distribution parameters
  for(i in 1:length(div)){
    currTeam <- div[i]
    team.W <- mlb.current.records[mlb.current.records$Tm == currTeam, "W"]
    team.L <- mlb.current.records[mlb.current.records$Tm == currTeam, "L"]
    p_hat <- oddsShark.2018[oddsShark.2018$Team_Abbr == currTeam, "Win_Total_2018"] / 162
    q_hat <- 1 - p_hat
    team.params <- BayesParamsForTeams(p_hat, q_hat, team.W, team.L, mlb.2017$W.L.)
    parms <- append(parms, team.params)
  }
}
  
#For each trial
sim.results <- rep(0,15)
for(i in 1:n_trials){
  results <- rep(0,15)
  x <- 1
  #sample from beta for each team
  for(j in seq(1, 60, by=4)){
    results[x] = round(rbeta(1, parms[j] + parms[j+1], parms[j+2] + parms[j+3]) * 162,0)
    x <- x + 1
  }
  results_Orig <- results
  for(k in seq(1,15,5)){
    results[(which.max(results[k:(k+4)]) + k - 1)] <- 0
  }
  #increment the winner
  sim.results[which.max(results)] = sim.results[which.max(results)] + 1
  n <- length(unique(results))
  ix <- which(results == sort(unique(results),partial=n-1)[n-1])
  #deal with ties for second wildcard
  if(length(ix) > 1){
    ix <- sample(ix, 1)
  }
  sim.results[ix] = sim.results[ix] + 1
}

#get percentage
sim.resultsAL = sim.results/n_trials

#National League
parms <- c()
for(z in 1:length(NL)){
  div <- unlist(NL[z])
  
  #For each team in the division, get their beta distribution parameters
  for(i in 1:length(div)){
    currTeam <- div[i]
    team.W <- mlb.current.records[mlb.current.records$Tm == currTeam, "W"]
    team.L <- mlb.current.records[mlb.current.records$Tm == currTeam, "L"]
    p_hat <- oddsShark.2018[oddsShark.2018$Team_Abbr == currTeam, "Win_Total_2018"] / 162
    q_hat <- 1 - p_hat
    team.params <- BayesParamsForTeams(p_hat, q_hat, team.W, team.L, mlb.2017$W.L.)
    parms <- append(parms, team.params)
  }
}

#For each trial
sim.results <- rep(0,15)
for(i in 1:n_trials){
  results <- rep(0,15)
  x <- 1
  #sample from beta for each team
  for(j in seq(1, 60, by=4)){
    results[x] = round(rbeta(1, parms[j] + parms[j+1], parms[j+2] + parms[j+3]) * 162,0)
    x <- x + 1
  }
  
  for(k in seq(1,15,5)){
    results[(which.max(results[k:(k+4)]) + k - 1)] <- 0
  }
  #increment the winner
  sim.results[which.max(results)] = sim.results[which.max(results)] + 1
  n <- length(unique(results))
  ix <- which(results == sort(unique(results),partial=n-1)[n-1])
  #deal with ties for second wildcard
  if(length(ix) > 1){
    ix <- sample(ix, 1)
  }
  sim.results[ix] = sim.results[ix] + 1
}

#get percentage
sim.resultsNL = sim.results/n_trials

wildCardProb = append(sim.resultsAL, sim.resultsNL)
finals <- cbind.data.frame(finals, wildCardProb)
names(finals) <- c("Team", "Division_Odds", "WildCard_Odds")
finals["Playoff_Odds"] <- finals[,2] + finals[,3]

write.csv(finals, "C:/Users/abooth/Documents/Docs/playoffOdds_April25.csv")

#####################################################

df <- read.csv("C:/Users/abooth/Documents/Docs/playoffOdds_AprilJuly.csv", stringsAsFactors = F)

#April vs July
gg <- ggplot(df, aes(x=Playoff_Odds_April24, y=Playoff_Odds_July16)) + 
  geom_point(colour="blue") + geom_text(aes(label=ifelse(Playoff_Odds_April24 > 0.03, Team, "")),hjust=-.1, vjust=-.1) + vnl_theme()
gg <- gg + ylab("July 16 Playoff Odds") + xlab("April 24 Playoff Odds")
gg <- gg + ggtitle(paste("April 24 vs July 16 Playoff Odds"))
gg <- gg + stat_function(fun = function(x) x, linetype = "dashed")
gg

gg <- ggplot(df, aes(x=Division_Odds_April24, y=Division_Odds_July16)) + 
  geom_point(colour="red") + geom_text(aes(label=ifelse(Division_Odds_April24 > 0.03, Team, "")),hjust=-.1, vjust=-.1) + vnl_theme()
gg <- gg + ylab("July 16 Division Odds") + xlab("April 24 Division Odds")
gg <- gg + ggtitle(paste("April 24 vs July 16 Division Odds"))
gg <- gg + stat_function(fun = function(x) x, linetype = "dashed")
gg

gg <- ggplot(df, aes(x=WildCard_Odds_April24, y=WildCard_Odds_July16)) + 
  geom_point(colour="purple") + geom_text(aes(label=ifelse(WildCard_Odds_April24 > 0.03, Team, "")),hjust=-.1, vjust=-.1) + vnl_theme()
gg <- gg + ylab("July 16 WildCard Odds") + xlab("April 24 WildCard Odds")
gg <- gg + ggtitle(paste("April 24 vs July 16 WildCard Odds"))
gg <- gg + stat_function(fun = function(x) x, linetype = "dashed")
gg

#Vs Fangraphs July
gg <- ggplot(df, aes(x=FG_Playoffs_July16, y=Playoff_Odds_July16)) + 
  geom_point(colour="blue") + geom_text(aes(label=ifelse(FG_Playoffs_July16 > 0.01, Team, "")),hjust=-.1, vjust=-.1) + vnl_theme()
gg <- gg + ylab("July 16 Playoff Odds") + xlab("FG July 16  Playoff Odds")
gg <- gg + ggtitle(paste("FanGraphs vs SaberSmart July 16 Playoff Odds"))
gg <- gg + stat_function(fun = function(x) x, linetype = "dashed")
gg

gg <- ggplot(df, aes(x=FG_Division_July16, y=Division_Odds_July16)) + 
  geom_point(colour="red") + geom_text(aes(label=ifelse(FG_Division_July16 > 0.01, Team, "")),hjust=-.1, vjust=-.1) + vnl_theme()
gg <- gg + ylab("July 16 Division Odds") + xlab("FG July 16  Division Odds")
gg <- gg + ggtitle(paste("FanGraphs vs SaberSmart July 16 Division Odds"))
gg <- gg + stat_function(fun = function(x) x, linetype = "dashed")
gg

gg <- ggplot(df, aes(x=FG_WildCard_July16, y=WildCard_Odds_July16)) + 
  geom_point(colour="purple") + geom_text(aes(label=ifelse(FG_WildCard_July16 > 0.01, Team, "")),hjust=-.1, vjust=-.1) + vnl_theme()
gg <- gg + ylab("July 16 WildCard Odds") + xlab("FG July 16 WildCard Odds")
gg <- gg + ggtitle(paste("FanGraphs vs SaberSmart July 16 WildCard Odds"))
gg <- gg + stat_function(fun = function(x) x, linetype = "dashed")
gg

#Vs Fangraphs April
gg <- ggplot(df, aes(x=FG_Playoffs_April24, y=Playoff_Odds_April24)) + 
  geom_point(colour="blue") + geom_text(aes(label=ifelse(FG_Playoffs_April24 > 0.03, Team, "")),hjust=-.1, vjust=-.1) + vnl_theme()
gg <- gg + ylab("April 24 Playoff Odds") + xlab("FG April 24  Playoff Odds")
gg <- gg + ggtitle(paste("FanGraphs vs SaberSmart April 24 Playoff Odds"))
gg <- gg + stat_function(fun = function(x) x, linetype = "dashed")
gg

gg <- ggplot(df, aes(x=FG_Division_April24, y=Division_Odds_April24)) + 
  geom_point(colour="red") + geom_text(aes(label=ifelse(FG_Division_April24 > 0.05, Team, "")),hjust=-.1, vjust=-.1) + vnl_theme()
gg <- gg + ylab("April 24 Division Odds") + xlab("FG April 24  Division Odds")
gg <- gg + ggtitle(paste("FanGraphs vs SaberSmart April 24 Division Odds"))
gg <- gg + stat_function(fun = function(x) x, linetype = "dashed")
gg

gg <- ggplot(df, aes(x=FG_WildCard_April24, y=WildCard_Odds_April24)) + 
  geom_point(colour="purple") + geom_text(aes(label=ifelse(FG_WildCard_April24 > 0.03, Team, "")),hjust=-.1, vjust=-.1) + vnl_theme()
gg <- gg + ylab("April 24 WildCard Odds") + xlab("FG April 24 WildCard Odds")
gg <- gg + ggtitle(paste("FanGraphs vs SaberSmart April 24 WildCard Odds"))
gg <- gg + stat_function(fun = function(x) x, linetype = "dashed")
gg

########################################

summary(100 * (df$FG_Playoffs_July16 - df$Playoff_Odds_July16))
summary(100 * (df$FG_Playoffs_April24 - df$Playoff_Odds_April24))
