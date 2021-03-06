% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/makeWAR.R
\name{makeWARBaserunning}
\alias{makeWARBaserunning}
\title{Computes RAA for each baserunner.}
\usage{
makeWARBaserunning(data, ...)
}
\arguments{
\item{data}{An MLBAM data.frame}

\item{...}{currently ignored}
}
\value{
A data.frame with 4 columns: baserunner id, raa for the runner on first base, raa for the runner on second base, and raa for the runner on third base.
}
\description{
Calculates the runs above average (RAA) created by each baserunner.
}
\details{
These RAA values are calculated by first computing the expected number of bases 
advanced given a starting position (e.g. runner on second) and an event (e.g. Single).  
Runners are attributed RAA based on how much they exceeded or underperformed 
relative to the expected number of bases advanced given an event.  For example, a baserunner who 
advances exactly the expected number of bases given an event would not be attributed any 
RAA for that play.
}

