library(ggmap)
register_google(key = "AIzaSyAl1rzC9ZUplwaDeIy-U6hF7kzci3Tosx0")
locs <- c("Addison, Illinois")
# geocode(locs)

# data = readxl::read_excel("Code/Data/output.xls", skip = 4)  
data=read.csv("Code/Data/United_States_COVID-19_Community_Levels_by_County.csv",skip=0)
colnames(data)
data 

