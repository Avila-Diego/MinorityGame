package main

import (
	"encoding/json"
	"math"
	"math/rand"
	"os"
	"strconv"
	"strings"
)

func generete_memory(len_memory int, history []int) {
	for i := 0; i < len_memory; i++ {
		num_rand := rand.Float64()
		if num_rand < 0.5 {
			num_rand = 0.0
		} else {
			num_rand = 1.0
		}
		history[i] = int(num_rand)
	}
}

func assign_strategies(strategies_per_agent int, len_memory int) (strategies_local [][]int) {
	strategies_local = make([][]int, strategies_per_agent)
	twoTwoM := math.Exp2(float64(len_memory))

	// tmp := strconv.FormatInt(int64(twoTwoM-1), 2)
	// fmt.Println(string(tmp))
	// var digits = strings.SplitAfter(string(tmp), "")
	// fmt.Println(digits)

	var strategiesDec string

	for i := 0; i < strategies_per_agent; i++ {
		tmp_Dec := rand.Int63n((int64(math.Exp2(twoTwoM))))
		// fmt.Println("tmp_Dec: ", tmp_Dec)
		strategiesDec = strconv.FormatInt(tmp_Dec, 2)
		// fmt.Println("strategiesDec: ", strategiesDec)
		var digits = strings.SplitAfter(string(strategiesDec), "")
		strategies_local[i] = make([]int, int(twoTwoM))
		len_tmp := len(strategies_local[i]) - len(digits)

		var value_tmp int64
		for j := 0; j < len(digits); j++ {
			value_tmp, _ = strconv.ParseInt(digits[j], 10, 64)
			strategies_local[i][j+len_tmp] = int(value_tmp)
		}
	}
	return strategies_local
}

func select_strategy(
	turtles [][][]int,
	current_strategy [][]int,
	strategies_scores [][]float64,
	history []int,
	choice []int) {
	for i := 0; i < len(strategies_scores); i++ {
		current_strategy[i] = turtles[i][0]
		score_tmp := strategies_scores[i][0]
		for j := 1; j < len(strategies_scores[i]); j++ {
			if strategies_scores[i][j]+rand.Float64() > score_tmp+rand.Float64() {
				score_tmp = strategies_scores[i][j]
				current_strategy[i] = turtles[i][j]
			}
		}
	}

	choice_func(history, current_strategy, choice)
}

func choice_func(history []int, current_strategy [][]int, choice []int) {
	number_strategies := historyToDec(history)

	for i := 0; i < len(current_strategy); i++ {
		choice[i] = current_strategy[i][number_strategies]
	}
}

func historyToDec(history []int) int64 {
	var numberText string

	tmp_number := int64(history[0])
	numberText = strconv.FormatInt(tmp_number, 10)

	for i := 1; i < len(history); i++ {
		tmp_number = int64(history[i])
		numberText += strconv.FormatInt(tmp_number, 10)
	}

	number_strategies, _ := strconv.ParseInt(numberText, 2, 64)
	return number_strategies
}

func update_system(choice []int, number_of_agents *int, minority *int, mean, sd *float64, sum *float64) {
	// var minority int

	for i := 0; i < len(choice); i++ {
		*sum += float64(choice[i])
	}

	if *sum > float64(*number_of_agents/2) {
		// print("Minoritario 0")
		*minority = 0
	} else {
		// print("Minoritario 1")
		*minority = 1
	}
	*mean = *sum / float64(*number_of_agents)

	for i := 0; i < len(choice); i++ {
		*sd += math.Pow(float64(choice[i]), 2)
	}
	*sd = math.Sqrt(*sd / float64(*number_of_agents-1))
}

func increment_score(
	minority int, turtles [][][]int, strategies_scores [][]float64, history []int, score, choice []int,
) {
	number_strategies := historyToDec(history)

	for i_agente := 0; i_agente < len(turtles); i_agente++ {
		for i_strategy := 0; i_strategy < len(turtles[i_agente]); i_strategy++ {
			if minority == turtles[i_agente][i_strategy][number_strategies] {
				strategies_scores[i_agente][i_strategy] += 1
			}
		}
	}

	for i_agente := 0; i_agente < len(choice); i_agente++ {
		if choice[i_agente] == minority {
			score[i_agente] += 1
		}
	}
}

func update_history(history []int, minority int) {
	for i_history := 0; i_history < len(history)-1; i_history++ {
		history[i_history] = history[i_history+1]
	}
	history[len(history)-1] = minority
}

func update_scores_and_strategy(
	minority *int, turtles [][][]int, strategies_scores [][]float64, history []int, score, choice []int,
) {
	increment_score(*minority, turtles, strategies_scores, history, score, choice)
}

type SummaryRun struct {
	Simulation         int     `json:"Simulation"`
	Iteration          int     `json:"Iteration"`
	Population         int     `json:"Population"`
	LenMemory          int     `json:"LenMemory"`
	Numberstrategy     int     `json:"Numberstrategy"`
	Minoritygroup      int     `json:"Minoritygroup"`
	N_zeros            float64 `json:"N_zeros"`
	Standardeviation   float64 `json:"Standardeviation"`
	Max_score          float64 `json:"Max_score"`
	Avg_score          float64 `json:"Avg_score"`
	Min_score          float64 `json:"Min_score"`
	Max_for_time_score float64 `json:"Max_for_time_score"`
	Avg_for_time_score float64 `json:"Avg_for_time_score"`
	Min_for_time_score float64 `json:"Min_for_time_score"`
}

func MaxArray(array []int) (max float64) {
	for i := 0; i < len(array); i++ {
		if float64(array[i]) > max {
			max = float64(array[i])
		}
	}
	return max
}

func MinArray(array []int) (min float64) {
	for i := 0; i < len(array); i++ {
		if float64(array[i]) < min {
			min = float64(array[i])
		}
	}
	return min
}

func setup(
	len_memory, number_of_agents, minority *int,
	history, choice []int,
	turtles [][][]int,
	current_strategy [][]int,
	strategies_scores [][]float64,
	avg_score, stdev_score, sum *float64,
) {
	generete_memory(*len_memory, history)
	select_strategy(turtles, current_strategy, strategies_scores, history, choice)
	update_system(choice, number_of_agents, minority, avg_score, stdev_score, sum)
}

func goRun(
	minority, number_of_agents *int,
	avg_score, stdev_score, sum *float64,
	turtles [][][]int,
	strategies_scores [][]float64,
	current_strategy [][]int,
	history, score, choice []int,
) {
	update_scores_and_strategy(minority, turtles, strategies_scores, history, score, choice)
	update_history(history, *minority)
	select_strategy(turtles, current_strategy, strategies_scores, history, choice)
	update_system(choice, number_of_agents, minority, avg_score, stdev_score, sum)
}

func main() {
	/*
		Inicialización de los parametros del modelos
	*/
	len_memory := 16
	strategies_per_agent := 16
	number_of_agents := 1001
	number_Iteration := 10000
	rand.Seed(123)

	/*
		Inicialización de las variables del modelo
	*/
	var (
		avg_score, stdev_score float64
		turtles                [][][]int
		strategies_scores      [][]float64
		current_strategy       [][]int
		score, choice          []int
		minority               int
		sum                    float64
	)

	history := make([]int, len_memory)
	for i := 0; i < number_of_agents; i++ {
		strategies_tmp := assign_strategies(strategies_per_agent, len_memory)
		turtles = append(turtles, strategies_tmp)
	}
	strategies_scores = make([][]float64, number_of_agents)
	for i := 0; i < number_of_agents; i++ {
		strategies_scores[i] = make([]float64, strategies_per_agent)
	}
	score = make([]int, number_of_agents)
	current_strategy = make([][]int, number_of_agents)
	choice = make([]int, number_of_agents)

	file, _ := os.OpenFile("Result.json", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	file.Write([]byte("[\n"))

	/*
		Run model
	*/
	// Inicial
	setup(
		&len_memory, &number_of_agents, &minority,
		history, choice,
		turtles,
		current_strategy,
		strategies_scores,
		&avg_score, &stdev_score, &sum,
	)

	summarySim := SummaryRun{
		Simulation:         0,
		Iteration:          0,
		Population:         number_of_agents,
		LenMemory:          len_memory,
		Numberstrategy:     strategies_per_agent,
		Minoritygroup:      minority,
		N_zeros:            float64(number_of_agents) - sum,
		Standardeviation:   stdev_score,
		Max_score:          MaxArray(score),
		Avg_score:          avg_score,
		Min_score:          MinArray(score),
		Max_for_time_score: 0,
		Avg_for_time_score: 0,
		Min_for_time_score: 0,
	}
	datosJson, _ := json.Marshal(summarySim)

	file.Write(datosJson)
	file.Write([]byte(",\n"))

	// Runing
	for i := 1; i < number_Iteration; i++ {
		goRun(
			&minority, &number_of_agents,
			&avg_score, &stdev_score, &sum,
			turtles,
			strategies_scores,
			current_strategy,
			history, score, choice,
		)
		summarySim = SummaryRun{
			Simulation:         0,
			Iteration:          i,
			Population:         number_of_agents,
			LenMemory:          len_memory,
			Numberstrategy:     strategies_per_agent,
			Minoritygroup:      minority,
			N_zeros:            float64(number_of_agents) - sum,
			Standardeviation:   stdev_score,
			Max_score:          MaxArray(score),
			Avg_score:          avg_score,
			Min_score:          MinArray(score),
			Max_for_time_score: MaxArray(score) / float64(i),
			Avg_for_time_score: avg_score / float64(i),
			Min_for_time_score: MinArray(score) / float64(i),
		}

		datosJson, _ = json.Marshal(summarySim)
		file.Write(datosJson)
		file.Write([]byte(",\n"))
	}

	file.Write([]byte("\n]\n"))
	file.Close()
}
