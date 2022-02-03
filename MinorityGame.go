package main

import (
	"fmt"
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

func update_system(choice []int, number_of_agents *int, minority *int, mean, sd, sum *float64) {
	*sum = 0
	*minority = 2
	*mean = 0
	*sd = 0

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
	// var len_memory_max, strategies_per_agent_max, number_of_agents int

	// fmt.Print("Número de agentes: ")
	// fmt.Scan(&number_of_agents)

	// fmt.Print("Longitud máxima de la memoría: ")
	// fmt.Scan(&len_memory_max)

	// fmt.Print("Estrategias máximas por agente: ")
	// fmt.Scan(&strategies_per_agent_max)

	number_Iteration := 10000

	len_memory := 3
	number_of_agents := 101
	strategies_per_agent := 2

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

	// for strategies_per_agent := 2; strategies_per_agent < strategies_per_agent_max; strategies_per_agent++ {
	// 	for len_memory := 2; len_memory < len_memory_max; len_memory++ {
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

	rute := "../Result_go/Result"
	rute += fmt.Sprint(
		"_Memory_",
		len_memory,
		"_StrategiesAgent_",
		strategies_per_agent,
		"_NumberAgent_",
		number_of_agents,
		".txt",
	)

	file, _ := os.OpenFile(rute, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)

	out := headTable()
	file.Write([]byte(out))

	/*
		Run model
	*/

	for simulation := 0; simulation < 40; simulation++ {
		// Inicial
		setup(
			&len_memory, &number_of_agents, &minority,
			history, choice,
			turtles,
			current_strategy,
			strategies_scores,
			&avg_score, &stdev_score, &sum,
		)

		out = concatOut(
			simulation,
			0,
			number_of_agents,
			len_memory,
			strategies_per_agent,
			minority,
			sum,
			stdev_score,
			score,
			avg_score,
		)

		file.Write([]byte(out))

		// Runing
		for iteration := 1; iteration < number_Iteration; iteration++ {
			goRun(
				&minority, &number_of_agents,
				&avg_score, &stdev_score, &sum,
				turtles,
				strategies_scores,
				current_strategy,
				history, score, choice,
			)

			out = concatOut(simulation,
				iteration,
				number_of_agents,
				len_memory,
				strategies_per_agent,
				minority,
				sum,
				stdev_score,
				score,
				avg_score,
			)

			file.Write([]byte(out))
		}
	}
	file.Close()
	// 	}
	// }
}

func headTable() string {
	out := "Simulation,"
	out += "Iteration,"
	out += "Population,"
	out += "LenMemory,"
	out += "NumberStrategy,"
	out += "Minoritygroup,"
	out += "n_zeros,"
	out += "Standardeviation,"
	out += "Max_score,"
	out += "Avg_score,"
	out += "Min_score,"
	out += "Max_for_time_score,"
	out += "Avg_for_time_score,"
	out += "Min_for_time_score"
	out += "Min_for_time_score\n"
	return out
}

func concatOut(
	simulation int,
	iteration int,
	number_of_agents int,
	len_memory int,
	strategies_per_agent int,
	minority int,
	sum float64,
	stdev_score float64,
	score []int,
	avg_score float64) (out string) {
	out = fmt.Sprint(
		simulation,
		", ",
		iteration,
		", ",
		number_of_agents,
		", ",
		len_memory,
		", ",
		strategies_per_agent,
		", ",
		minority,
		", ",
	)
	out += strconv.FormatFloat((float64(number_of_agents) - sum), 'g', -1, 64)
	out += ", "
	out += strconv.FormatFloat((stdev_score), 'g', -1, 64)
	out += ", "
	out += strconv.FormatFloat((MaxArray(score)), 'g', -1, 64)
	out += ", "
	out += strconv.FormatFloat((avg_score), 'g', -1, 64)
	out += ", "
	out += strconv.FormatFloat((MinArray(score)), 'g', -1, 64)
	out += ", "
	out += strconv.FormatFloat((MaxArray(score) / float64(iteration)), 'g', -1, 64)
	out += ", "
	out += strconv.FormatFloat((avg_score / float64(iteration)), 'g', -1, 64)
	out += ", "
	out += strconv.FormatFloat((MinArray(score) / float64(iteration)), 'g', -1, 64)
	out += "\n"
	return out
}
