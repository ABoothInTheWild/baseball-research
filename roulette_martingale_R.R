#Roulette Simulator
#Using Martingale betting strategy

#Alexander Booth
#January 25, 2017

#init probability variables
p_win = 18/38
p_lose = 20/38
niterations = 10000
#this is the intial bet put down
#It get's doubled after each loss
init_bet <- 1
#maximum cash willing to lose
stop_loss = 130
#Goal to win
goal = 1

simulator <- function(p_win, p_lose, niterations, init_bet, stop_loss, goal){
  #Allow for reproduction
  set.seed(1234)
  #init variables
  results_bin <- numeric(niterations)
  results_prof <- numeric(niterations)
  total_profit <- 0
  
  #figure out max losses in a row
  #Geometric sequence: ar^n
  a <- init_bet
  sum <- a
  max_losses <- 1
  while(sum <= stop_loss){
    double <- 2 ^ max_losses
    a <- init_bet * double
    sum <- sum + a
    max_losses <- max_losses + 1
  }
  
  max_losses <- max_losses - 1
  
  i <- 1
  #Loop through iterations
  while(i <= niterations){
    #Per turn, we play until we hit our goal
    #or hit our max_losses in a row
    current_profit <- 0
    bet <- init_bet
    win <- FALSE
    j <- 0
    
    while(j < max_losses){
      
      #Random number from uniform distribution
      spin <- runif(1)
      
      #If win, add bet to the current profit
      #Check if current profit hits our goal
      #reset losses in a row
      #reset bet
      
      if(spin >= p_lose){
        current_profit <- current_profit + bet
        if(current_profit >= goal){
          win <- TRUE
          break
        }
        bet <- init_bet
        j <- 0
      }
      
      #If lose, subtract bet from current profit
      #double our bet
      #add 1 to our losses in a row
      
      if(spin <= p_lose){
        current_profit <- current_profit - bet
        bet <- bet * 2
        j <- j + 1
      }
    }
    
    #Set total profit for that game
    total_profit <- current_profit
    
    #add profit and win boolean to arrays
    results_prof[i] <- total_profit
    if(win == TRUE){
      results_bin[i] = 1
    }
    else{
      results_bin[i] = 0
    }
    i <- i + 1
  }
  
  #return dataframe
  return(data.frame(results_bin, results_prof))
}

results = simulator(p_win, p_lose, niterations, init_bet, stop_loss, goal)

#determine probability of reaching our goal
sum(results[1])/length(row(results[1]))