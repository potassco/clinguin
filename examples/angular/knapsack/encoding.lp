{take(O)}:-object(O).
:- #sum{W,O : take(O), weight(O,W)} > MAX, weight_limit(MAX).
#maximize{V,O : take(O), value(O,V)}.