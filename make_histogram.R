#Make Histograms Using Theme
#returns a ggplot

#Alexander Booth
#February 3, 2017

library(ggplot2)

make_hist <- function(df, var_name){
  
  windowsFonts(Helvetica=windowsFont("Helvetica"))
  
  gg<-ggplot(df, aes(var_name)) + ylab("Frequency") + xlab("Points") + geom_histogram()
  
  gg <- gg + theme(
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_line(colour="#FEFCFD", linetype='dashed'),
    panel.grid.major.y = element_line(colour="#FEFCFD", linetype='dashed'),
    axis.line.y = element_line(size = rel(2), linetype = "solid",
                               colour = "#000505"),
    plot.background = element_rect(fill = "#BFCDE0"),
    panel.background = element_rect(fill = "#BFCDE0"),
    text=element_text(family="Helvetica", face="bold",  colour="#000505"),
    axis.text = element_text(colour = "#000505", size=rel(1)),
    
    axis.ticks = element_line(colour = "#000505", size=rel(1)),
    axis.line.x = element_line(size = rel(2), linetype = "solid",
                               colour = "#000505"),
    axis.ticks.length=unit(.25, "cm")
  )
  
  gg <- gg + ggtitle(paste("Histogram of ", deparse(substitute(var_name))))
  
  return (gg)
}