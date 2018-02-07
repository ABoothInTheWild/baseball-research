#Alexander Booth
#January 31, 2017
#Sport Simulator with Negative Binomial Distribution

#Updated February 6, 2018

#Simulator inputs include points/runs scored and allowed by two teams
#to use as the basis of out data generation and simulation

#niterations is defaulted to 10,000
simulator <- function(team1_off_data, team1_def_data, team2_off_data, team2_def_data, niterations = 10000){
  set.seed(123)
  
  #Init Game Scores and who Won
  team1_game_score <- numeric(niterations)
  team2_game_score <- numeric(niterations)
  team1_wins <- numeric(niterations)
  team2_wins <- numeric(niterations)
  
  #Init params for approximating a negative binomial distribution
  inputs <- cbind(team1_off_data, team1_def_data, team2_off_data, team2_def_data)
  params <- matrix(NA, nrow = 4, ncol=2)
  
  #For each input, fit a negative binomial distribution and record
  #its parameters
  for(i in 1:4){
    fit <- MASS::fitdistr(inputs[,i][inputs[,i] > 0], "negative binomial")
    # get the fitted densities. mu and size from fit.
    params[i,] <- c(fit$estimate[1], fit$estimate[2])
  }
  
  j = 1
  while(j <= niterations){
    
    #Get offense and defense random samples by sampling from
    #negative distrbution approximated to inputs
    team1_off = rnbinom(1, size = params[1,1], mu=params[1,2])
    team1_def = rnbinom(1, size = params[2,1], mu=params[2,2])
    team2_off = rnbinom(1, size = params[3,1], mu=params[3,2])
    team2_def = rnbinom(1, size = params[4,1], mu=params[4,2])
    
    #determine score by averaging offensse and opposing defense
    team1_score = round(mean(c(team1_off, team2_def)))
    team2_score = round(mean(c(team2_off, team1_def)))
    
    #Throw out ties and continue while
    if(team1_score == team2_score){
      next
    }
    
    #Record Game Scores
    team1_game_score[j] <- team1_score
    team2_game_score[j] <- team2_score
    
    #Record who won
    team1_wins[j] = ifelse(team1_score > team2_score, 1, 0)
    team2_wins[j] = ifelse(team2_score > team1_score, 1, 0)
    
    #Move to next simulation
    j <- j + 1
  }
  
  #Accumulate results and Create Return DF
  results <- cbind(team1_game_score, team2_game_score, team1_wins, team2_wins)
  results_df <- as.data.frame(results, stringsAsFactors = FALSE)
  colnames(results_df) <- c("Team_1_Game_Score", "Team_2_Game_Score", 
                            "Team_1_Wins", "Team_2_Wins")
  
  return(results_df)
}