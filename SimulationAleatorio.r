rm(list = ls()); gc()

library(dplyr)

simulaciones_prueba <- 40
ciclos_prueba <- 1000
poblacion_prueba <- 101

data_prueba <- NULL
group <- sample(
  c(0, 1),
  size = simulaciones_prueba * ciclos_prueba * poblacion_prueba,
  replace = T
)

data_prueba <- as.data.frame(group)

data_prueba$simulacion <- rep(
  1:simulaciones_prueba,
  ciclos_prueba * poblacion_prueba
)

data_prueba <- data_prueba[order(data_prueba$simulacion),]

data_prueba$ciclo <- rep(
  1:ciclos_prueba,
  simulaciones_prueba * poblacion_prueba
)

data_prueba <- data_prueba[order(data_prueba$ciclo),]

data_prueba$agente <- rep(
  1:poblacion_prueba,
  simulaciones_prueba * ciclos_prueba
)

group_data_prueba <- data_prueba %>%
  group_by(simulacion, ciclo) %>%
  summarize(
    sum_ones = sum(group, na.rm = TRUE)
  )

result <- group_data_prueba %>%
  group_by(simulacion) %>%
  summarize(
    m = mean(sum_ones, na.rm = TRUE),
    sd = sd(sum_ones, na.rm = TRUE)
  )

plot(rep(1, length(result$sd)), result$sd)
