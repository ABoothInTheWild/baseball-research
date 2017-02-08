setwd("C:/Users/Alexander/Documents/baseball")
library(ggplot2)

#Super Bowl Simulator
#Using Negative Binomial Disribution

#Alexander Booth
#January 31, 2017

pats_off_2016 = c(23, 31, 27, 0, 33, 35, 27, 41, 24, 30, 22, 26, 30, 16, 41, 35, 34, 36)
pats_def_2016 = c(21, 24, 0, 16, 13, 17, 16, 25, 31, 17, 17, 10, 23, 3, 3, 14, 16, 17)

falc_off_2016 = c(24, 35, 45, 48, 23, 24, 30, 33, 43, 15, 38, 28, 42, 41, 33, 38, 36, 44)
falc_def_2016 = c(31, 28, 32, 33, 16, 26, 33, 32, 28, 24, 19, 29, 14, 13, 16, 32, 20, 21)

scores_df <- data.frame(pats_off_2016, pats_def_2016, falc_off_2016, falc_def_2016)
apply(scores_df, 2, mean)
apply(scores_df, 2, sd)

#Create Graphs of scores
pats_off_hist <- make_hist(scores_df, pats_off_2016)
pats_def_hist <- make_hist(scores_df, pats_def_2016)
falc_off_hist <- make_hist(scores_df, falc_off_2016)
falc_def_hist <- make_hist(scores_df, falc_def_2016)

combined <- multiplot(pats_off_hist, pats_def_hist, falc_off_hist, falc_def_hist, cols = 2)

#Create Graphs of Neg. Binomial sizes
NBD_size4 <- rnbinom(1000, mu=mean(falc_off), size = 4)
NBD_size50 <- rnbinom(1000, mu=mean(falc_off), size = 50)
NBD_size100 <- rnbinom(1000, mu=mean(falc_off), size = 100)
sizes_df <- data.frame(NBD_size4, NBD_size50, NBD_size100)

size4_hist <- make_hist(sizes_df, NBD_size4)
size50_hist <- make_hist(sizes_df, NBD_size50)
size100_hist <- make_hist(sizes_df, NBD_size100)

combined2 <- multiplot(falc_off_hist, size4_hist, size50_hist, size100_hist, cols = 2)

#Simulator
simulator <- function(team1_off_mean, team1_def_mean, team2_off_mean, team2_def_mean, NB_size, niterations){
  set.seed(1234)
  team1_game_score <- numeric(niterations)
  team2_game_score <- numeric(niterations)
  
  team1_wins <- numeric(niterations)
  team2_wins <- numeric(niterations)
  
  i <- 1
  
  while(i <= niterations){
    team1_off = rnbinom(1, mu=team1_off_mean, size = NB_size)
    team1_def = rnbinom(1, mu=team1_def_mean, size = NB_size)
    
    team2_off = rnbinom(1, mu=team2_off_mean, size = NB_size)
    team2_def = rnbinom(1, mu=team2_def_mean, size = NB_size)
    
    team1_score = round(mean(c(team1_off, team2_def)))
    team2_score = round(mean(c(team2_off, team1_def)))
    
    if(team1_score == 1 || team2_score == 1){
      next
    }
    
    if(team1_score == team2_score){
      next
    }
    
    team1_game_score[i] <- team1_score
    team2_game_score[i] <- team2_score
    
    if(team1_score > team2_score){
      team1_wins[i] = 1
      team2_wins[i] = 0
    }
    
    if(team2_score > team1_score){
      team2_wins[i] = 1
      team1_wins[i] = 0
    }
    
    i <- i + 1
  }
  
  team1_sum <- sum(team1_wins)
  team2_sum <- sum(team2_wins)
  
  team1_win_pcnt <- team1_sum/niterations
  team2_win_pcnt <- team2_sum/niterations
  
  return(c(team1_win_pcnt, team2_win_pcnt, mean(team1_game_score), mean(team2_game_score), sd(team1_game_score), sd(team2_game_score)))
}

pats_off_mean = mean(pats_off_2016)
pats_def_mean = mean(pats_def_2016)

falc_off_mean = mean(falc_off_2016)
falc_def_mean = mean(falc_def_2016)

NB_size = 100
niterations = 100000

final_scores <- simulator(pats_off_mean, pats_def_mean, falc_off_mean, falc_def_mean, NB_size, niterations)
