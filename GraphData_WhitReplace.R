rm(list = ls()); gc()

setwd("~/Documents/Tesis/Code/Result_WhitReplace")

library(readr)
library(dplyr)
library(ggplot2)

# data <- readRDS("../Result_out/0_Result_NetLogo_Merge.rds")
data <- NULL
files <- list.files()

for (file in files) {
  data_tmp <- read_csv(file)
  data <- rbind(data, data_tmp)
  data_tmp <- NULL; gc()
}

result <- data %>%
  filter(Population == 101, NumberStrategy == 2) %>%
  select(LenMemory, Simulation, NumberStrategy, n_zeros) %>%
  group_by(LenMemory, Simulation, NumberStrategy) %>%
  summarize(
    m = mean(n_zeros, na.rm = TRUE),
    sd = sd(n_zeros)
  )


Fig1 <- ggplot(result) +
  aes(x = LenMemory, y = sd) +
  geom_point() +
  geom_hline(yintercept=5, linetype="dashed", color = "red") + 
  scale_y_continuous(breaks = seq(0, 16, by = 1)) + 
  scale_x_continuous(breaks = seq(2, 15, by = 1))

Fig1

result <- data %>%
  filter(NumberStrategy == 2) %>% 
  select(Population, LenMemory, Simulation, NumberStrategy, n_zeros) %>%
  group_by(Population, LenMemory, Simulation, NumberStrategy) %>%
  summarize(
    m = mean(n_zeros, na.rm = TRUE),
    sd = sd(n_zeros)
  )

result$sigma2_N <- result$sd^2 / result$Population
result$z <- 2^result$LenMemory / result$Population

result <- result %>%
  # select(sigma2_N, z, LenMemory, Population) %>%
  group_by(LenMemory, Population) %>%
  summarize(
    sigma2_N = mean(sigma2_N),
    z = mean(z)
  )

result$Population <- factor(result$Population)

Fig6 <- ggplot(result) +
  aes(x = z, y = sigma2_N, group = Population) +
  geom_point(aes(
    shape=Population, 
    color=Population
  )) + 
  scale_color_manual(values=c("#ffa600", "#7a5195", "#ef5675", "#003f5c")) +
  scale_x_log10() + 
  scale_y_log10() # +
# coord_cartesian(xlim=c(0.01, 10000), ylim=c(0.01, 10))

Fig6

tabulate_memory <- function(vector, memory) {
  tabulate <- NULL
  
  for (i_pos in 1:(length(vector) - (memory + 1))) {
    tmp_prev <- paste0(vector[i_pos:(i_pos + memory - 1)], collapse = "")
    tmp_forecast <- vector[(i_pos + memory)]
    tabulate <- rbind(tabulate, cbind(tmp_prev, tmp_forecast))
  }
  
  tabulate <- data.frame(tabulate)
  
  tabulate$tmp_forecast <- as.numeric(tabulate$tmp_forecast)
  
  resume <- tabulate %>%
    group_by(tmp_prev) %>%
    summarise(sum = sum(tmp_forecast),
              n = n())
  
  return(resume)
}

filter_data <-
  function(table,
           population,
           number_strategy,
           simulation,
           len_memory) {
    result <- table %>%
      filter(
        Population == population,
        NumberStrategy == number_strategy,
        Simulation == simulation,
        LenMemory == len_memory
      )
    
    return(result)
  }

result_append <- function(
  table,
  population,
  number_strategy,
  len_memory,
  memory) {
  result_app <- NULL
  
  for (i_simulation in 1:max(data$Simulation)) {
    data_filter <- filter_data(table, population, number_strategy, i_simulation, len_memory)
    resume <- tabulate_memory(data_filter$MinorityGroup, memory)
    result_app <- rbind(result_app, resume)
  }
  
  result_app <- result_app %>% 
    group_by(tmp_prev) %>% 
    summarise(
      suma = sum(sum),
      n_sum = sum(n)
    )
  
  result_app$prob <- result_app$suma / result_app$n_sum
  
  return(result_app)
}

resumen <- result_append(
  table = data,
  population = 101,
  number_strategy = 2,
  len_memory = 4,
  memory = 4)

barplot(resumen$prob, ylim = c(0, 1))

resumen_2 <- result_append(
  table = data,
  population = 101,
  number_strategy = 2,
  len_memory = 4,
  memory = 5)

barplot(resumen_2$prob, ylim = c(0, 1))

resumen_3 <- result_append(
  table = data,
  population = 101,
  number_strategy = 2,
  len_memory = 6,
  memory = 6)

barplot(resumen_3$prob, ylim = c(0, 1))

resumen_4 <- result_append(
  table = data,
  population = 101,
  number_strategy = 2,
  len_memory = 6,
  memory = 7)

barplot(resumen_4$prob, ylim = c(0, 1))

### FIG 6a
result <- data %>%
  filter((LenMemory == 3| LenMemory == 16) & NumberStrategy == 2) %>%
  select(Population, LenMemory, Simulation, NumberStrategy, n_zeros) %>%
  group_by(LenMemory, Simulation, NumberStrategy, Population) %>%
  summarize(
    m = mean(n_zeros, na.rm = TRUE),
    sd = sd(n_zeros)
  )

result <- result %>%
  # select(sigma2_N, z, LenMemory, Population) %>%
  group_by(LenMemory, NumberStrategy, Population) %>%
  summarize(
    sd_mean = mean(sd),
    m_mean = mean(m)
  )

result$LenMemory <- factor(result$LenMemory)

Fig6a <- ggplot(result) +
  aes(x = Population, y = sd_mean, group = Population) +
  geom_point(aes(
    shape=LenMemory, 
    color=LenMemory
  )) + 
  scale_color_manual(values=c("#ffa600", "#7a5195")) +
  scale_x_log10() + 
  scale_y_log10() # +
# coord_cartesian(xlim=c(0.01, 10000), ylim=c(0.01, 10))

Fig6a


# Fig 8
result <- data %>%
  filter(Population == 101, NumberStrategy == 6) %>%
  select(LenMemory, Simulation, NumberStrategy, n_zeros) %>%
  group_by(LenMemory, Simulation, NumberStrategy) %>%
  summarize(
    m = mean(n_zeros, na.rm = TRUE),
    sd = sd(n_zeros)
  )


Fig8 <- ggplot(result) +
  aes(x = LenMemory, y = sd) +
  geom_point() +
  geom_hline(yintercept=5, linetype="dashed", color = "red") + 
  # scale_y_continuous(breaks = seq(0, 16, by = 1)) + 
  scale_x_continuous(breaks = seq(2, 15, by = 1))

Fig8

result <- data %>%
  filter(NumberStrategy == 6) %>% 
  select(Population, LenMemory, Simulation, NumberStrategy, n_zeros) %>%
  group_by(Population, LenMemory, Simulation, NumberStrategy) %>%
  summarize(
    m = mean(n_zeros, na.rm = TRUE),
    sd = sd(n_zeros)
  )

result$sigma2_N <- result$sd^2 / result$Population
result$z <- 2^result$LenMemory / result$Population

result <- result %>%
  # select(sigma2_N, z, LenMemory, Population) %>%
  group_by(LenMemory, Population) %>%
  summarize(
    sigma2_N = mean(sigma2_N),
    z = mean(z)
  )

result$Population <- factor(result$Population)

Fig10 <- ggplot(result) +
  aes(x = z, y = sigma2_N, group = Population) +
  geom_point(aes(
    shape=Population, 
    color=Population
  )) + 
  scale_color_manual(values=c("#ffa600", "#7a5195", "#ef5675", "#003f5c")) +
  scale_x_log10() + 
  scale_y_log10() +
  # coord_cartesian(xlim=c(0.01, 10000), ylim=c(0.01, 10))
  # geom_smooth(method='lm', formula= y ~ x)
  geom_smooth(method='lm')

Fig10

