%% SWI Prolog version
%%
%% Run tests:
%%   $ swipl -q -t run_tests day01.pl
%%
%% Find solution for part 1:
%%   $ swipl -q -t part1 day01.pl

required_fuel(Mass, Fuel) :- Fuel is max(0, Mass // 3 - 2).

:- begin_tests(tests).
test(required_fuel, true(F == 2)) :- required_fuel(12, F).
test(required_fuel, true(F == 2)) :- required_fuel(14, F).
test(required_fuel, true(F == 654)) :- required_fuel(1969, F).
test(required_fuel, true(F == 33583)) :- required_fuel(100756, F).
test(required_fuel, true(F == 0)) :- required_fuel(2, F).
:- end_tests(tests).

read_input(Filename, Values) :-
    read_file_to_string(Filename, String, []),
    split_string(String, "\n", "", Lines),
    maplist(number_string, Values, Lines).

total_required_fuel(MassList, TotalFuel) :-
    maplist(required_fuel, MassList, FuelList),
    sum_list(FuelList, TotalFuel).

part1 :-
    read_input("day01.txt", MassList),
    forall(total_required_fuel(MassList, TotalFuel), writeln(TotalFuel)).
