def better_coeff_merger(each_method_candidates: list[list[tuple[str, float]]]) -> list[tuple[str, float]] :
    candidate_dict = {}
    for method in each_method_candidates :
        for candidate in method :
            candidate_dict[candidate[0]] = max(candidate_dict.get(candidate[0], -1), candidate[1])
    merged_candidate_list = [(candidate, candidate_dict[candidate]) for candidate in candidate_dict.keys()]

    def sorting_function(t) :
        return t[1]

    merged_candidate_list = sorted(merged_candidate_list, key = sorting_function, reverse = False)
    return merged_candidate_list


def arithmetic_mean_coeff_merger(each_method_candidates: list[list[tuple[str, float]]]) -> list[tuple[str, float]] :
    candidate_dict = {}
    for method in each_method_candidates :
        for candidate in method :
            candidate_dict[candidate[0]] = candidate_dict.get(candidate[0], (0, 0)) + (candidate[1], 1)
    merged_candidate_list = [(candidate, candidate_dict[candidate][0] / candidate_dict[candidate][1]) for candidate in
                             candidate_dict.keys()]

    def sorting_function(t) :
        return t[1]

    merged_candidate_list = sorted(merged_candidate_list, key = sorting_function, reverse = False)
    return merged_candidate_list


def geometric_mean_coeff_merger(each_method_candidates: list[list[tuple[str, float]]]) -> list[tuple[str, float]] :
    candidate_dict = {}
    for method in each_method_candidates :
        for candidate in method :
            previous = candidate_dict.get(candidate[0], (1, 0))
            next = (previous[0] * candidate[1], previous[1] + 1)
            candidate_dict[candidate[0]] = next
    merged_candidate_list = [(candidate, pow(candidate_dict[candidate][0], 1 / candidate_dict[candidate][1])) for
                             candidate in candidate_dict.keys()]

    def sorting_function(t) :
        return t[1]

    merged_candidate_list = sorted(merged_candidate_list, key = sorting_function, reverse = False)
    return merged_candidate_list


def worse_coeff_merger(each_method_candidates: list[list[tuple[str, float]]]) -> list[tuple[str, float]] :
    candidate_dict = {}
    for method in each_method_candidates :
        for candidate in method :
            candidate_dict[candidate[0]] = min(candidate_dict.get(candidate[0], float("inf")), candidate[1])
    merged_candidate_list = [(candidate, candidate_dict[candidate]) for candidate in candidate_dict.keys()]

    def sorting_function(t) :
        return t[1]

    merged_candidate_list = sorted(merged_candidate_list, key = sorting_function, reverse = False)
    return merged_candidate_list
