library(rjson)

setwd("~/Documents/Tesis/Code/MinorityGame")

data <- fromJSON(file = "Result.json")


data <- lapply(
  data, 
  function(x){
    x[sapply(x, is.null)] <- NA
    unlist(x)
  }
  )

do.call("rbind", data)
