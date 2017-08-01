#Alexander Booth
#An Investigation of the 2014 Cardinals with openWar
#7/09/2017

# Player and Team Valuation

# to begin identify the computer environment as Windows versus Mac/Linux
# comment out the system that does not apply
#windows_system <- FALSE  # setting for Mac and Linux
windows_system <- TRUE  # setting for Windows

# specify a valid repository name for your compute
repo_name <- "http://cran.rstudio.com/"

# This jump-start code shows how to bring in the openWAR functions
# into the R workspace for subsequent use without employing
# the usual R program installation routines for openWAR. 
# We are not loading Sxslt, which is required for loading data
# directly from Major League Baseball Advanced Media (MLBAM).

# -----------------------------------
# Installing software into R
# and bringing it into the workspace
# -----------------------------------

# we begin by placing the entire openWAR-master directory within
# the working directory. Key subdirectories within openWAR-master
# include the R subdirectory which contains R functions and
# the data subdirectory which contains R binary data files.

package_needed <- (c("acepack", "car", "Formula", "ggdendro", 
                     "gridExtra", "Hmisc", "latticeExtra", "lme4", 
                     "MatrixModels", "minqa", "mosaic", "mosaicData", 
                     "nloptr", "pbkrtest", "quantreg", "RCurl", "readr", 
                     "SparseM", "XML", "plyr"))

# check on available libraries with library()
available_libraries <- library()  

for (ipack in seq(along = package_needed)) {
  if (!package_needed[ipack] %in% available_libraries)
    install.packages(package_needed[ipack], dependencies=TRUE, 
                     repos= repo_name)
}

# bring libraries into the workspace for use with openWAR functions
library("acepack") 
library("car")
library("Formula")
library("ggdendro")
library("gridExtra")
library("Hmisc")
library("latticeExtra")
library("lme4")
library("MatrixModels")
library("minqa")
library("mosaic")
library("mosaicData")
library("nloptr")
library("pbkrtest")
library("quantreg")
library("RCurl")
library("SparseM")
library("XML")
library("plyr")

# set the workspace location to be the directory where
# this program resides, with text_documents as a subdirectory/folder

# file manipulation code that follows
# is designed to work on either Mac/Linux or Windows_systems
# but we need to specify the type of computer system prior to execution
# locate yourself in working directory that has corpus directory
# and identify the directory labeled "corpus"
if (windows_system) 
  r_program_location <- paste(getwd(), "\\openWAR-master\\R\\", sep = "")

if(!windows_system)     
  r_program_location <- paste(getwd(), "/openWAR-master/R/", sep = "")

# get file names in the corpus directory_location
r_file_names <- dir(r_program_location)

for (ifile in seq(along = r_file_names)) { # begin for-loop for R programs/functions
  # define the file name within the directory text_documents
  this_file <- paste(paste(r_program_location, r_file_names[ifile], sep = ""))
  source(this_file)  # bring the R function into the workspace    
}  # end for-loop for R programs/functions

# you can check the availability of R openWAR functions by printing their names
# print(ls())

# -------------------------------------
# Gathering Play-by-Play Data  
# -------------------------------------
# An alternative for using Sxslt is to go directly to the source
# and scrape the data. For example, play-by-play data for 2015
# may be located under

# http://gd2.mlb.com/components/game/mlb/year_2015/

# pick months with data April (month_04) through September (month_09)
# pick days... then choose a game... for example

# http://gd2.mlb.com/components/game/mlb/year_2015/month_05/day_01/gid_2015_05_01_anamlb_sfnmlb_1/game_events.json

# gives the April 1, 2015 game between the Anaheim Angels of the
# American League versus the San Francisco Giants of the National League.
# These are the play-by-play data in JSON format. 
# For a complete regular season, there will be 162 games for each team.

# under the data subdirectory of openWAR-master 
# there are numerous R binary data files to consider
# feel free to use one of these files rather than loading
# play-by-play data directly from MLBAM

# here we choose openWAR2014.rda
binary_data_file <- "openWAR2014.rda"
# these are summary measures derived from play-by-play data

if (windows_system) 
  data_location <- paste(getwd(), "\\openWAR-master\\data\\", sep = "")

if(!windows_system)     
  data_location <- paste(getwd(), "/openWAR-master/data/", sep = "")

load(file = paste(data_location, binary_data_file, sep = ""))

# show the structure of the data we have brought into the workspace
print(str(openWAR2014))

# Consider only your selected team of starting position players.
# I have select the Stl Cardinals for example.
# It looks like the starting lineup of position players will be:
#
# Position 2 (Catcher): Yadier Molina (MLBAM ID = "425877")
# Position 3 (First Baseman): Matt Adams (MLBAM ID = "571431")
# Position 4 (Second Baseman): Kolten Wong (MLBAM ID = "543939")
# Position 5 (Third Baseman): Matt Carpenter (MLBAM ID = "572761")
# Position 6 (Shortstop): Jhonny Peralta (MLBAM ID = "425509")
# Position 7 (Left Field): Matt Holliday (MLBAM ID = "407812")
# Position 8 (Center Field): Jon Jay (MLBAM ID = "445055")
# Position 9 (Right Field): Allen Craig (MLBAM ID = "501800")
#                           Oscar Taveras(MLBAM ID = "570805")

# We can now obtain data for the players of interest by filtering
# or subsetting the data frame openWAR2014:

team <- c("425877", "571431", "543939", "572761", "425509", "407812", "445055", "501800", "570805")
cat("\n\n2014 Cardinals player IDs:")
print(team)

team_openWAR2014 <- openWAR2014[(openWAR2014$playerId %in% team),]

# show the structure of Cardinals player data
print(str(team_openWAR2014))

cat("\n\nPlayer IDs included in the selected data frame:")
print(team_openWAR2014$playerId)
cat("\nCorresponding to players:")
print(team_openWAR2014$Name)

cat("\n\nCardinals player IDs not included in the selected data frame:")
print(setdiff(team, team_openWAR2014$playerId))

#Great, we have data for all 8 players

#Get RAA and WAR
print(team_openWAR2014[, c('Name', "RAA", "WAR")])

#Get DF with replacement players as well
team_subOpenWar2014 <- subset(openWAR2014, isReplacement == T | playerId %in% team)

#Make Factor variable for legend
team_subOpenWar2014$isReplacementFactor = ""
team_subOpenWar2014$isReplacementFactor[team_subOpenWar2014$isReplacement == T] <- "Replacement Player"
team_subOpenWar2014$isReplacementFactor[team_subOpenWar2014$isReplacement == F] <- "Cardinals Roster Player"

#Graph for WAR by Plate Appearances
windowsFonts(Helvetica=windowsFont("Helvetica"))

gg<-ggplot(team_subOpenWar2014, aes(y=WAR, x=PA.bat, colour = isReplacementFactor)) + ylab("WAR") + xlab("Plate Appearances")
gg<- gg + geom_point(size = 4)

gg <- gg + theme(
  panel.grid.minor = element_blank(),
  panel.grid.major.x = element_line(colour="#FEFCFD", linetype='dashed'),
  panel.grid.major.y = element_line(colour="#FEFCFD", linetype='dashed'),
  axis.line.y = element_line(size = rel(3), linetype = "solid",
                             colour = "#000505"),
  plot.background = element_rect(fill = "#BFCDE0"),
  panel.background = element_rect(fill = "#BFCDE0"),
  text=element_text(family="Helvetica", face="bold",  colour="#000505"),
  axis.text = element_text(colour = "#000505", size=rel(1)),
  
  axis.ticks = element_line(colour = "#000505", size=rel(1)),
  legend.background = element_rect(fill="transparent"),
  legend.text = element_text(size=rel(.75)),
  legend.title=element_blank(),
  #legend.justification=c(1,0),
  legend.key = element_blank(),
  axis.line.x = element_line(size = rel(3), linetype = "solid",
                             colour = "#000505"),
  axis.ticks.length=unit(.25, "cm")
  # #                  panel.margin = unit(c(1,1,1,1), "cm"))
)

gg <- gg + ggtitle("WAR by Plate Appearances") + theme(plot.title = element_text(hjust = 0.5))
gg
#ggsave(file = 'WAR_by_PA.png', plot = gg, dpi = 1200, w=7, h=4.66666, unit="in" )
