not.installed = function(package_name)  !is.element(package_name, installed.packages()[,1])

if (not.installed("RCurl")) install.packages("RCurl")
if (not.installed("plyr")) install.packages("plyr")
if (not.installed("ggplot2")) install.packages("ggplot2")

library(RCurl)
library(plyr)
library(ggplot2)

#reading Baby Names
bnames <- read.csv("/Users/shivinkapur/Desktop/246Code/ProjectCode/names.csv", stringsAsFactors = FALSE)
dim(bnames)
print(summary(bnames))

#reading Twitter Names
tnames <- read.csv("/Users/shivinkapur/Desktop/246Code/ProjectCode/FirstDBoutput.csv", stringsAsFactors = FALSE)
dim(tnames)
summary(tnames)

#pruning twitter names to only required columns
tnames <- tnames[,1:2]
dim(tnames)
summary(tnames)


#separating boys and girls
names_f=subset(bnames,bnames$gender=="F")
names_m=subset(bnames, bnames$gender=="M")
bnames
names_f
names_m

names_overallProp=ddply(bnames, .(name,gender), summarize, total=sum(count))
colnames(names_overallProp)=c("names","gender","births")
head(names_overallProp)

names_overallSingle=ddply(bnames, .(name), summarize, total=sum(count))
colnames(names_overallSingle)=c("names","sumbirths")
head(names_overallSingle)

#totalBirths=sum(names_overallProp$total)
#totalBirths
#names_overallProp$overallProp=names_overallProp$total/totalBirths
#names_overallProp$overallProp

