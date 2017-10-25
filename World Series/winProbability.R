# Alexander Booth
# October 24, 2017

# external libraries for visualizations and data manipulation
# ensure that these have been installed prior to calls
library(lattice) 
library(ggplot2)
library(scales)
library(grid)
library(RColorBrewer)
library(gridExtra)
library(hash)
library(reshape2)

#Set WD
setwd("C:/Users/Alexander/Documents/baseball/World Series")

#Reference:
#Woolf, Max. (2015). An Introduction on How to Make Beautiful Charts With R and ggplot2
#R code retrieved from the World Wide Web on October 5, 2017, at 
#https://github.com/minimaxir/ggplot-tutorial/blob/master/ggplot_tutorial_1.R

#FTE Theme adapted from minimaxir, aka Max Woolf of Buzzfeed
fte_theme <- function() {
  
  # Generate the colors for the chart procedurally with RColorBrewer
  palette <- brewer.pal("Greys", n=9)
  color.background = "white"
  color.grid.major = palette[3]
  color.axis.text = palette[6]
  color.axis.title = palette[7]
  color.title = palette[9]
  
  # Begin construction of chart
  theme_bw(base_size=9) +
    
    # Set the entire chart region to a light gray color
    theme(panel.background=element_rect(fill=color.background, color=color.background)) +
    theme(plot.background=element_rect(fill=color.background, color=color.background)) +
    theme(panel.border=element_rect(color=color.background)) +
    
    # Format the grid
    theme(panel.grid.major=element_line(color=color.grid.major,size=.25)) +
    theme(panel.grid.minor=element_blank()) +
    theme(axis.ticks=element_blank()) +
    
    # Format the legend, but hide by default
    theme(legend.position="right") +
    theme(legend.background = element_rect(fill=color.background)) +
    theme(legend.text = element_text(size=7,color=color.axis.title)) +
    
    # Set title and axis labels, and format these and tick marks
    theme(plot.title=element_text(color=color.title, size=10, vjust=1.25)) +
    theme(plot.title = element_text(hjust = 0.5)) +
    theme(axis.text.x=element_text(size=7,color=color.axis.text)) +
    theme(axis.text.y=element_text(size=7,color=color.axis.text)) +
    theme(axis.title.x=element_text(size=8,color=color.axis.title, vjust=0)) +
    theme(axis.title.y=element_text(size=8,color=color.axis.title, vjust=1.25)) +
    
    # Plot margins
    theme(plot.margin = unit(c(0.35, 0.2, 0.3, 0.35), "cm"))
}

#data
games <- c(0,1)
winProbs <- c(0.50407, 0.34831639768878264, 0.49593, 0.6516836023112174)
Team <- c("Astros", "Astros", "Dodgers", "Dodgers") 

df <- data.frame(winProbs = winProbs, Team = Team, game=games)

gg <- ggplot(data = df, aes(x=game, y=winProbs)) + geom_line(aes(colour=Team))
gg <- gg + ylab("Win Probability") + xlab("World Series Game") + 
      geom_point(size = 2, aes(color = Team)) +
      coord_cartesian(xlim = c(0,7), ylim = c(0, 1)) + 
      scale_colour_manual(values = c("#CF4520", "#1E90FF")) +
      scale_x_continuous(breaks = seq(0,7)) +
      ggtitle("World Series Win Probability") + 
      theme(plot.title = element_text(hjust = 0.5)) +
      fte_theme()
gg


