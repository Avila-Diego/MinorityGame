setwd("~/Documents/Tesis/Code/GameMinority")

library(readr)
library(dplyr)
library(ggplot2)

data <- read_csv("results_memory_ReplicateNetLogo.csv")
data

result <- data %>%
  # filter(Population == 11, NumberStrategy == 2) %>%
  select(LenMemory, Simulation, NumberStrategy, n_zeros) %>%
  group_by(LenMemory, Simulation, NumberStrategy) %>%
  summarize(
    m = mean(n_zeros, na.rm = TRUE),
    sd = sd(n_zeros)
  )

ggplot(result) +
  aes(x = LenMemory, y = sd) +
  geom_point() +
  geom_hline(yintercept=5, linetype="dashed", color = "red") + 
  scale_y_continuous(breaks = seq(0, 16, by = 1)) + 
  scale_x_continuous(breaks = seq(2, 15, by = 1))


data_filter <- data %>% 
  filter(Simulation == 1, LenMemory == 2)

ggplot(data_filter, aes(x=Iteration)) + 
  geom_line(aes(y = max_score), color = 'red') + 
  geom_line(aes(y = avg_score), color = 'green') +
  geom_line(aes(y = min_score), color = 'blue')

ggplot(data_filter, aes(x=Iteration)) + 
  geom_line(aes(y = max_for_time_score), color = 'red') + 
  geom_line(aes(y = avg_for_time_score), color = 'green') +
  geom_line(aes(y = min_for_time_score), color = 'blue')