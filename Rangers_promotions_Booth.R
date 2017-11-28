#Alexander Booth
#Assignment 3
#7/30/2017

# Predictive Model for Texas Rangers Promotion and Attendance (R)

#Imports
library(car)  # special functions for linear regression
library(lattice)  # graphics package

#Set Working directory
setwd("C:\\Users\\Alexander\\Documents\\Northwestern\\Summer 2017\\457\\Assignment 3")

# read in data and create a data frame called rangers
rangers <- read.csv("texas_rangers_attendance_2012.csv")
print(str(rangers))  # check the structure of the data frame

# define an ordered day-of-week variable 
# for plots and data summaries
rangers$ordered_day_of_week <- with(data=rangers,
  ifelse ((day_of_week == "Monday"),1,
  ifelse ((day_of_week == "Tuesday"),2,
  ifelse ((day_of_week == "Wednesday"),3,
  ifelse ((day_of_week == "Thursday"),4,
  ifelse ((day_of_week == "Friday"),5,
  ifelse ((day_of_week == "Saturday"),6,7)))))))
rangers$ordered_day_of_week <- factor(rangers$ordered_day_of_week, levels=1:7,
labels=c("Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"))

# exploratory data analysis with standard graphics: attendance by day of week
with(data=rangers,plot(ordered_day_of_week, attend/1000, 
xlab = "Day of Week", ylab = "Attendance (thousands)", 
col = "violet", las = 1))

#count promotions
library(plyr)
count(rangers, "bobblehead")
count(rangers, "cap")
count(rangers, "shirt")
count(rangers, "fireworks")

#add promotions
rangers$promotions = rangers$bobblehead == "YES" | rangers$cap == "YES" |
  rangers$shirt == "YES" | rangers$fireworks == "YES"

#add weekend
rangers$weekend = rangers$day_of_week == "Friday" | rangers$day_of_week == "Saturday" |
  rangers$day_of_week == "Sunday"

mean(rangers[rangers$weekend == T & rangers$promotions == F,]$attend)
mean(rangers[rangers$weekend == T & rangers$promotions == T,]$attend)

# when do the rangers use promotions
with(rangers, table(promotions,ordered_day_of_week)) # promotions on Weekends

# define an ordered month variable 
# for plots and data summaries
rangers$ordered_month <- with(data=rangers,
  ifelse ((month == "APR"),4,
  ifelse ((month == "MAY"),5,
  ifelse ((month == "JUN"),6,
  ifelse ((month == "JUL"),7,
  ifelse ((month == "AUG"),8,
  ifelse ((month == "SEP"),9,10)))))))
rangers$ordered_month <- factor(rangers$ordered_month, levels=4:10,
labels = c("April", "May", "June", "July", "Aug", "Sept", "Oct"))

# exploratory data analysis with standard R graphics: attendance by month 
with(data=rangers,plot(ordered_month,attend/1000, xlab = "Month", 
ylab = "Attendance (thousands)", col = "light blue", las = 1))

# exploratory data analysis displaying many variables
# looking at attendance and conditioning on day/night
# the skies and whether or not fireworks are displayed
library(lattice) # used for plotting 
# let us prepare a graphical summary of the rangers data
rangers_no_rain <- rangers[rangers$skies != "Rainy",]
group.labels <- c("No Fireworks","Fireworks")
group.symbols <- c(21,24)
group.colors <- c("black","black") 
group.fill <- c("black","red")
xyplot(attend/1000 ~ temp | skies + day_night, 
    data = rangers_no_rain, groups = fireworks, pch = group.symbols, 
    aspect = 1, cex = 1.5, col = group.colors, fill = group.fill,
    layout = c(2, 2), type = c("p","g"),
    strip=strip.custom(strip.levels=TRUE,strip.names=FALSE, style=1),
    xlab = "Temperature (Degrees Fahrenheit)", 
    ylab = "Attendance (thousands)",
    key = list(space = "top", 
        text = list(rev(group.labels),col = rev(group.colors)),
        points = list(pch = rev(group.symbols), col = rev(group.colors),
        fill = rev(group.fill))))                  
# attendance by opponent and day/night game
group.labels <- c("Day","Night")
group.symbols <- c(1,20)
group.symbols.size <- c(2,2.75)
bwplot(opponent ~ attend/1000, data = rangers, groups = day_night, 
    xlab = "Attendance (thousands)",
    panel = function(x, y, groups, subscripts, ...) 
       {panel.grid(h = (length(levels(rangers$opponent)) - 1), v = -1)
        panel.stripplot(x, y, groups = groups, subscripts = subscripts, 
        cex = group.symbols.size, pch = group.symbols, col = "darkblue")
       },
    key = list(space = "top", 
    text = list(group.labels,col = "black"),
    points = list(pch = group.symbols, cex = group.symbols.size, 
    col = "darkblue")))
     
# employ training-and-test regimen for model validation
set.seed(1234) # set seed for repeatability of training-and-test split
training_test <- c(rep(1,length=trunc((2/3)*nrow(rangers))),
rep(2,length=(nrow(rangers) - trunc((2/3)*nrow(rangers)))))
rangers$training_test <- sample(training_test) # random permutation 
rangers$training_test <- factor(rangers$training_test, 
  levels=c(1,2), labels=c("TRAIN","TEST"))
rangers.train <- subset(rangers, training_test == "TRAIN")
print(str(rangers.train)) # check training data frame
rangers.test <- subset(rangers, training_test == "TEST")
print(str(rangers.test)) # check test data frame

# specify a simple model with promotions entered last
my.model <- {attend ~ ordered_month + ordered_day_of_week + promotions}
# fit the model to the training set
train.model.fit <- lm(my.model, data = rangers.train)
# summary of model fit to the training set
print(summary(train.model.fit))
# training set predictions from the model fit to the training set
rangers.train$predict_attend <- predict(train.model.fit) 
# test set predictions from the model fit to the training set
rangers.test$predict_attend <- predict(train.model.fit, 
  newdata = rangers.test)

# compute the proportion of response variance
# accounted for when predicting out-of-sample
cat("\n","Proportion of Test Set Variance Accounted for: ",
round((with(rangers.test,cor(attend,predict_attend)^2)),
  digits=3),"\n",sep="")
# merge the training and test sets for plotting
rangers.plotting.frame <- rbind(rangers.train,rangers.test)

# generate predictive modeling visual for management
group.labels <- c("No Promotions","Promotions")
group.symbols <- c(21,24)
group.colors <- c("black","black") 
group.fill <- c("black","red")  
xyplot(predict_attend/1000 ~ attend/1000 | training_test, 
       data = rangers.plotting.frame, groups = promotions, cex = 2,
       pch = group.symbols, col = group.colors, fill = group.fill, 
       layout = c(2, 1), xlim = c(20,65), ylim = c(20,65), 
       aspect=1, type = c("p","g"),
       panel=function(x,y, ...)
            {panel.xyplot(x,y,...)
             panel.segments(25,25,60,60,col="black",cex=2)
            },
       strip=function(...) strip.default(..., style=1),
       xlab = "Actual Attendance (thousands)", 
       ylab = "Predicted Attendance (thousands)",
       key = list(space = "top", 
              text = list(rev(group.labels),col = rev(group.colors)),
              points = list(pch = rev(group.symbols), 
              col = rev(group.colors),
              fill = rev(group.fill))))                   
# use the full data set to obtain an estimate of the increase in
# attendance due to promotions, controlling for other factors 
my.model.fit <- lm(my.model, data = rangers)  # use all available data
print(summary(my.model.fit))
# tests statistical significance of promotions
# type I anova computes sums of squares for sequential tests
print(anova(my.model.fit))  
cat("\n","Estimated Effect of Promotions on Attendance: ",
round(my.model.fit$coefficients[length(my.model.fit$coefficients)],
digits = 0),"\n",sep="")
# standard graphics provide diagnostic plots
plot(my.model.fit)
# additional model diagnostics drawn from the car package
library(car)
residualPlots(my.model.fit)
marginalModelPlots(my.model.fit)
print(outlierTest(my.model.fit))

