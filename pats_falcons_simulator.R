setwd("C:/Users/Alexander/Documents/baseball")

pats_off = c(23, 31, 27, 0, 33, 35, 27, 41, 24, 30, 22, 26, 30, 16, 41, 35, 34, 36)
pats_def = c(21, 24, 0, 16, 13, 17, 16, 25, 31, 17, 17, 10, 23, 3, 3, 14, 16, 17)

falc_off = c(24, 35, 45, 48, 23, 24, 30, 33, 43, 15, 38, 28, 42, 41, 33, 38, 36, 44)
falc_def = c(31, 28, 32, 33, 16, 26, 33, 32, 28, 24, 19, 29, 14, 13, 16, 32, 20, 21)

simulator <- function(team1_off_mean, team1_def_mean, team2_off_mean, team2_def_mean, niterations){
  set.seed(1234)
  team1_game_score <- numeric(niterations)
  team2_game_score <- numeric(niterations)
  
  team1_wins <- numeric(niterations)
  team2_wins <- numeric(niterations)
  
  i <- 1
  
  while(i <= niterations){
    team1_off = rnbinom(1, mu=team1_off_mean, size = 4)
    team1_def = rnbinom(1, mu=team1_def_mean, size = 4)
    
    team2_off = rnbinom(1, mu=team2_off_mean, size = 4)
    team2_def = rnbinom(1, mu=team2_def_mean, size = 4)
    
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

pats_off_mean = mean(pats_off)
pats_def_mean = mean(pats_def)

falc_off_mean = mean(falc_off)
falc_def_mean = mean(falc_def)
niterations = 100000

final_scores <- simulator(pats_off_mean, pats_def_mean, falc_off_mean, falc_def_mean, niterations)