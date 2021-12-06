# rm(list <- ls()); gc()

library(readr)
library(dplyr)
library(ggplot2)

# setwd("~/Documents/Tesis/Code/GameMinority/Result")
# setwd("~/Documents/Tesis/Code/GameMinority/result_NuevasEstrategias")
# setwd("~/Documents/Tesis/Code/GameMinority/result_RemplazoReglaM")
# setwd("~/Downloads/Result/")
setwd("~/Documents/Tesis/Code/GameMinority/Result_CalculoEstrategia/")

files_puntuation <- list.files(pattern = "_puntuation")
files_summary <- list.files(pattern = "\\d\\.csv")

data_summmary <- NULL
for (file in files_summary) {
  tmp <- read_csv(file)
  tmp$file <- file
  data_summmary <- rbind(data_summmary, tmp)
}

tmp <- NULL
gc()

data_summmary$sum_ones <- ifelse(
  data_summmary$MinorityGroup == 1,
  data_summmary$n_wins,
  101 - data_summmary$n_wins
)

# result <- data_summmary %>%
#   select(LenMemory, Simulation, n_wins) %>%
#   group_by(LenMemory, Simulation) %>%
#   summarize(
#     m = mean(n_wins, na.rm = TRUE),
#     sd = sd(n_wins)
#   )

# plot(result$LenMemory, result$sd)

result <- data_summmary %>%
  select(LenMemory, Simulation, NumberStrategy, sum_ones) %>%
  group_by(LenMemory, Simulation, NumberStrategy) %>%
  summarize(
    m = mean(sum_ones, na.rm = TRUE),
    sd = sd(sum_ones)
  )

# result_filter <- filter(result, NumberStrategy == 1)

# plot(
#   result_filter$LenMemory, result_filter$sd,
#   xlab = "m", ylab = "Std. Dev.",
#   col = "black",
#   xlim=c(0,16),
#   ylim=c(0,15),
# )

result$Population <- 101
result$sigma2_N <- result$sd^2 / result$Population
result$z <- 2^result$LenMemory / result$Population

# plot(
#   result$z, result$sigma2_N,
#   xlab = "z", ylab = "sigma^2/N"
#   )


img <- ggplot(filter(result, NumberStrategy == 2)) +
  aes(x = LenMemory, y = sd) +
  geom_point() +
  coord_cartesian(xlim = c(0, 16), ylim = c(0, 15))

# ggplot(filter(result, NumberStrategy == 1)) +
#   aes(x = z, y = sigma2_N) +
#   geom_point() +
#   scale_x_log10() +
#   scale_y_log10() +
#   coord_cartesian(xlim = c(0.01, 10000), ylim = c(0.01, 10))

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
