#Alexander Booth
#February 6, 2018

#Super Bowl Analysis and Prediction

#Load libraries
library(psych)
library(dplyr)
library(ggplot2)

#Load Prewritten functions
source("vnl_theme.R")
source("multiplot.R")
source("Sports_Simulator_R_2018.R")
source("BayesAnalysis_Generalized.R")

#Read and format data
nflScores <- read.csv("nfl2018.csv", header=TRUE, stringsAsFactors = FALSE)
nfl_notSB <- nflScores[ !(nflScores$Week == "SuperBowl"), ]

###########################################################################

#Part 1: Force a Negative Binomial distribution onto the points scored and
#allowed for both the Eagles and the Patriots. Perform a Monte Carlo simulation
#by sampling from each distribution thousands of times. Look at the results.

#Get Eagles points scored and allowed for the season
eagles <- nfl_notSB[(nfl_notSB$Winner == "Philadelphia Eagles" |
                       nfl_notSB$Loser == "Philadelphia Eagles"),]

eagles_pf <- eagles[(eagles$Winner == "Philadelphia Eagles"), "PtsW"]
eagles_pf<- append(eagles_pf, eagles[(eagles$Loser == "Philadelphia Eagles"), "PtsL"] )
eagles_pa <- eagles[!(eagles$Loser == "Philadelphia Eagles"), "PtsL"]
eagles_pa <- append(eagles_pa, eagles[!(eagles$Winner == "Philadelphia Eagles"), "PtsW"] )

#Get Patriots points scored and allowed for the season
patriots <- nfl_notSB[(nfl_notSB$Winner == "New England Patriots" |
                         nfl_notSB$Loser == "New England Patriots"),]

pats_pf <- patriots[(patriots$Winner == "New England Patriots"), "PtsW"]
pats_pf<- append(pats_pf, patriots[(patriots$Loser == "New England Patriots"), "PtsL"] )
pats_pa <- patriots[!(patriots$Loser == "New England Patriots"), "PtsL"]
pats_pa <- append(pats_pa, patriots[!(patriots$Winner == "New England Patriots"), "PtsW"] )

#Look at some stats
scores_df <- data.frame(pats_pf, pats_pa, eagles_pf, eagles_pa)
describe(scores_df)

make_hist <- function(df, var_name){
  gg<-ggplot(df, aes(var_name)) + ylab("Frequency") + xlab("Points") + 
    geom_histogram(aes(y = ..density..), binwidth = 5, boundary = 0, closed = "left")
  gg <- gg + vnl_theme()
  gg <- gg + ggtitle(paste("Histogram of ", deparse(substitute(var_name))))
  return (gg)
}

#Create Graphs of scores
pats_off_hist <- make_hist(scores_df, pats_pf)
pats_def_hist <- make_hist(scores_df, pats_pa)
eagles_off_hist <- make_hist(scores_df, eagles_pf)
eagles_def_hist <- make_hist(scores_df, eagles_pa)
multiplot(pats_off_hist, pats_def_hist, eagles_off_hist, eagles_def_hist, cols = 2)

#Overlay with Neg. Bin approximation
set.seed(123)
fit <- MASS::fitdistr(pats_pf[pats_pf > 0], "negative binomial")
pats_off_hist <- pats_off_hist + geom_line(aes(y=dnbinom(pats_pf, size=fit$estimate[1], mu=fit$estimate[2]), 
                                           colour = "Negative Binomial Approximation"), lwd = 2) +
                                scale_colour_manual("", values = c("red")) + theme(legend.position="bottom")
pats_off_hist
fit <- MASS::fitdistr(pats_pa[pats_pa > 0], "negative binomial")
pats_def_hist <- pats_def_hist + geom_line(aes(y=dnbinom(pats_pa, size=fit$estimate[1], mu=fit$estimate[2]), 
                                               colour = "Negative Binomial Approximation"), lwd = 2) +
                                  scale_colour_manual("", values = c("red")) + theme(legend.position="bottom")
pats_def_hist
fit <- MASS::fitdistr(eagles_pf[eagles_pf > 0], "negative binomial")
eagles_off_hist <- eagles_off_hist + geom_line(aes(y=dnbinom(eagles_pf, size=fit$estimate[1], mu=fit$estimate[2]), 
                                                   colour = "Negative Binomial Approximation"), lwd = 2) +
                                  scale_colour_manual("", values = c("red")) + theme(legend.position="bottom")
eagles_off_hist
fit <- MASS::fitdistr(eagles_pa[eagles_pa > 0], "negative binomial")
eagles_def_hist <- eagles_def_hist + geom_line(aes(y=dnbinom(eagles_pa, size=fit$estimate[1], mu=fit$estimate[2]), 
                                                   colour = "Negative Binomial Approximation"), lwd = 2) +
                                    scale_colour_manual("", values = c("red")) + theme(legend.position="bottom")
eagles_def_hist

#Simulate
niterations = 100000
final_scores <- simulator(team1_off_data = pats_pf, team1_def_data = pats_pa, 
                          team2_off_data = eagles_pf, team2_def_data = eagles_pa, niterations)
final_scores["Diff"] <- final_scores$Team_2_Game_Score - final_scores$Team_1_Game_Score

describe(final_scores[,c("Team_1_Game_Score", "Team_2_Game_Score", "Diff")])

#Get Win Percentages
team1_sum <- sum(final_scores$Team_1_Wins)
team2_sum <- sum(final_scores$Team_2_Wins)

team1_win_pcnt <- team1_sum/niterations
team2_win_pcnt <- team2_sum/niterations
team1_win_pcnt #45.5
team2_win_pcnt #54.5

#Probability of hitting the Over
over_prob <- nrow(final_scores[(final_scores$Team_1_Game_Score + final_scores$Team_2_Game_Score >= 48),]) / niterations
over_prob

#Probability of Game ending with at least 74 points
over_prob2 <- nrow(final_scores[(final_scores$Team_1_Game_Score + final_scores$Team_2_Game_Score >= 74),]) / niterations
over_prob2

#Probability of Game ending within 1 score (8 points)
over_prob3 <- nrow(final_scores[(abs(final_scores$Diff) <= 8),]) / niterations
over_prob3

#Probability of Game ending within 1 FG (3 points)
over_prob4 <- nrow(final_scores[(abs(final_scores$Diff) <= 3),]) / niterations
over_prob4

#Probability of Eagles winning by 1 score (8 points or less), given they won
over_prob5 <- nrow(final_scores[(0 <= final_scores$Diff & final_scores$Diff <= 8),]) / team2_sum
over_prob5

#Median score would be 24-22 to the Eagles

#Plot
gg<-ggplot(final_scores, aes(final_scores$Diff)) + ylab("Frequency") + xlab("Points") + 
             geom_histogram(aes(y = ..density..), binwidth = 5, boundary = 0, closed = "left")
gg <- gg + vnl_theme()
gg <- gg + ggtitle(paste("Histogram of Difference in Scores")) +
  stat_function(fun = dnorm, 
                args = list(mean = mean(final_scores$Diff), sd = sd(final_scores$Diff)), 
                lwd = 1.5, aes(colour = "Normal Approximation")) +
  scale_colour_manual("", values = c("red")) + theme(legend.position="bottom")
gg

#Double check with CLT normal curve
1 - pnorm(0, mean = mean(final_scores$Diff), sd = sd(final_scores$Diff))

#Plot 2
gg2 <- ggplot(data = data.frame(x = c(0, 50)), aes(x)) +
  stat_function(fun = dnorm, args = list(mean = mean(final_scores$Team_1_Game_Score), 
                                         sd = sd(final_scores$Team_1_Game_Score)), 
                                         lwd = 1.5, aes(colour = "Patriots")) +
  stat_function(fun = dnorm, args = list(mean = mean(final_scores$Team_2_Game_Score), 
                                         sd = sd(final_scores$Team_2_Game_Score)), 
                                         lwd = 1.5, aes(colour = "Eagles")) +
  vnl_theme() + ggtitle(paste("Normal Approximations of Simulation Scores")) +
  ylab("Density") + xlab("Simulated Points Scored") +
  scale_colour_manual("Team", values = c("blue", "red")) + theme(legend.position="right")
gg2

###########################################################################
#Part 2: Use Pythagorean Expectation and Bayesian analysis to determine the
#probability that one team is truly better than the other. This probability
#can then be seen as the chance that team can best the other one.
#Reference: https://en.wikipedia.org/wiki/Pythagorean_expectation#Use_in_pro_football

#Use the xWP of each team to determine a prior. Use the xWP of the Eagles and
#the Patriots in our Bayesian analysis with that prior, based on 18 games

#Get the total points for and against for each team across the season
df <- data.frame(stringsAsFactors = FALSE)
teams <- unique(nfl_notSB$Loser)

#Loop through and get the points for and against each team per game
for(i in 1:length(teams)){
  temp <- nfl_notSB[(nfl_notSB$Winner == teams[i] |
                         nfl_notSB$Loser == teams[i]),]
  
  temp_pf <- temp[(temp$Winner == teams[i]), "PtsW"]
  temp_pf<- append(temp_pf, temp[(temp$Loser == teams[i]), "PtsL"] )
  temp_pa <- temp[!(temp$Loser == teams[i]), "PtsL"]
  temp_pa <- append(temp_pa, temp[!(temp$Winner == teams[i]), "PtsW"] )
  
  df <- rbind(df, cbind(rep(teams[i],length(temp_pa)), temp_pf, temp_pa))
}
colnames(df)[1] <- "Team"
df$temp_pf <- as.numeric(as.character(df$temp_pf))
df$temp_pa <- as.numeric(as.character(df$temp_pa))

#Add them up per group
df_pointsFandA <- as.data.frame(df %>%
                  group_by(Team) %>%
                  summarise(sumPF = sum(temp_pf), sumPA = sum(temp_pa)))

# Calculate xWP per team based off of the official formula
df_pointsFandA["Expected_WinPerc"] <- ((df_pointsFandA$sumPF^2.37)/(df_pointsFandA$sumPF^2.37 + 
                                                                      df_pointsFandA$sumPA^2.37))
describe(df_pointsFandA)
#Force into a beta distribution and determine parameters to act as a prior
set.seed(123)
m <- MASS::fitdistr(df_pointsFandA$Expected_WinPerc, dbeta,
                    start = list(shape1 = 0.5, shape2 = 0.5))
#Get priors
prior.alpha <- m$estimate[1]
prior.beta <- m$estimate[2]

#Plot to see how good they look on every team
gg<-ggplot(df_pointsFandA, aes(df_pointsFandA$Expected_WinPerc)) + ylab("Density") + xlab("xWP") + 
  geom_histogram(aes(y = ..density..), binwidth = 0.1, boundary = 0, closed = "left")
gg <- gg + vnl_theme()
gg <- gg + ggtitle(paste("Histogram for Expected Win Percentage")) +
  stat_function(fun = dbeta, 
                args = list(prior.alpha, prior.beta), 
                lwd = 1.5, aes(colour = "Beta Approximation")) +
  scale_colour_manual("", values = c("red")) + theme(legend.position="bottom")
gg

#Get Bayes results. Successes and Failures are determined by xWP * 18 (games pre-Super Bowl)
bayesResults <- bayesAnalysis(df_pointsFandA[df_pointsFandA$Team == "New England Patriots", "Expected_WinPerc"] * 18, 
                       (1-df_pointsFandA[df_pointsFandA$Team == "New England Patriots", "Expected_WinPerc"]) * 18,
                       df_pointsFandA[df_pointsFandA$Team == "Philadelphia Eagles", "Expected_WinPerc"] * 18, 
                       (1-df_pointsFandA[df_pointsFandA$Team == "Philadelphia Eagles", "Expected_WinPerc"]) * 18,
                       prior_alpha = prior.alpha, prior_beta = prior.beta)

bayesResults$`Probability Group 2 is Superior` #Probability that the Eagles truly are the better team is .547

#make columns numeric
bayesResults[1:15] <- lapply(bayesResults[1:15], as.numeric) 

a.group.success = bayesResults[, "Group 1 Successes"]
a.group.failure = bayesResults[, "Group 1 Failures"]
b.group.success = bayesResults[, "Group 2 Successes"]
b.group.failure = bayesResults[, "Group 2 Failures"]

#Plot
gg2 <- ggplot(data = data.frame(x = c(0, 1)), aes(x)) +
  stat_function(fun = dbeta, args = list(a.group.success+1, a.group.failure+1), 
                lwd = 1.5, aes(colour = "Patriots")) +
  stat_function(fun = dbeta, args = list(b.group.success+1, b.group.failure+1), 
                lwd = 1.5, aes(colour = "Eagles")) +
  vnl_theme() + ggtitle(paste("Bayesian Estimates of True xWP")) +
  ylab("Density") + xlab("Expected Win Percentage (xWP)") +
  scale_colour_manual("Team", values = c("blue", "red")) + theme(legend.position="right")
gg2

#Fin
