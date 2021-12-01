rm(list <- ls()); gc()

library(readr)
library(dplyr)

setwd("~/Documents/Tesis/Code/GameMinority/Result")

files_puntuation <- list.files(pattern = "_puntuation")
files_summary <- list.files(pattern = "\\d\\.csv")

data_summmary <- NULL
for (file in files_summary) {
  tmp <- read_csv(file)
  data_summmary <- rbind(data_summmary, tmp)
}

tmp <- NULL
gc()

result <- data_summmary %>%
  select(LenMemory, Simulation, n_wins) %>%
  group_by(LenMemory, Simulation) %>%
  summarize(
    m = mean(n_wins, na.rm = TRUE),
    sd = sd(n_wins)
  )

plot(result$LenMemory, result$sd)

# data_pupulation <- NULL
# for (file in files_puntuation) {
#   tmp <- read_csv(file)
#   tmp$file <- file
#   data_pupulation <- rbind(data_pupulation, tmp)
# }
# tmp <- NULL
# gc()

# result_pupulation <- data_pupulation %>%
#   group_by(file) %>%
#   summarize(
#     m = mean(`0`, na.rm = TRUE),
#     sd = sd(`0`)
#   )

# result_pupulation