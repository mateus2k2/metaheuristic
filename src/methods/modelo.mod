set I;               # INDICE PARA OS PERIODOS
set J;               # INDICE PARA AS TAREFAS


# ----------------------------------------------------------------------------------------------------------------


param p{J};          # TEMPO DE PROCESSAMENTO DE CADA TAREFA
param r{J};          # TEMPO DE PROCESSAMENTO DE CADA TAREFA
param T;             # DURACAO TOTAL DE CADA PERIODO
param R;             # MAXIMO DE RECURSOS DISPONIVEIS POR PERIODO
param M;             # NUMERO POSITIVO GRANDE


# ----------------------------------------------------------------------------------------------------------------


var X{I, J} binary;  # 1 SE A TAREFA J E PROCESSADA NO PERIODO I, 0 CASO CONTRAIO
var y{I}    binary;  # 1 SE O PERIODO I E USADO NA SOLUCAO, 0 CASO CONTRARIO
var w{I}    binary;  # 1 SE O PERIODO I E O MAIOR TEMPO OCIOSO , 0 CASO CONTRARIO
var z       >= 0  ;  # COMPUTA O TEMPO OCIOSO (SLACK) DO PERIODO COM MAIOR


# ----------------------------------------------------------------------------------------------------------------


minimize obj:
    T * sum{i in I} y[i] - z;


# ----------------------------------------------------------------------------------------------------------------


subject to designicaoTarefas{j in J}:
    sum{i in I} X[i, j] = 1;

subject to limiteDeTempo{i in I}:
    sum{j in J} p[j] * X[i, j] <= T;

subject to limiteDeRecurso{i in I}:
    sum{j in J} r[j] * X[i, j] <= R;

subject to limitaTarefasParaPeriodoUsados{i in I, j in J}:
    X[i, j] <= y[i];

subject to apenasUmPeriodoComMaiorTempoOcioso:
    sum{i in I} w[i] = 1;

subject to limitaPeriodoComMaiorTempoOciosoParaPeriodosUsados{i in I}:
    w[i] <= y[i];

subject to calculaMaiorTempoOcioso{i in I}:
    z <= (M * (1 - w[i])) + (T * (y[i])) - (sum{j in J} (p[j] * X[i, j]));


# ----------------------------------------------------------------------------------------------------------------

# Data exemplo do Artigo Modificado

data;

set J := 1 2 3 4 5;
set I := 1 2 3;

param p := 
    1 2
    2 1
    3 5
    4 4
    5 3;

param r := 
    1 3
    2 3
    3 4
    4 1
    5 1;

param T := 6;
param R := 4;
param M := 1000000;

end;

# ----------------------------------------------------------------------------------------------------------------

# Data sm3

# data;

# set J := 1 2 3 4 5 6 7 8 9 10;
# set I := 1 2 3 4 5 6 7 8;

# param p := 
#     1 140
#     2 45
#     3 132
#     4 145
#     5 150 
#     6 30
#     7 136
#     8 80
#     9 3
#     10 144;

# param r := 
#     1 91
#     2 95
#     3 60
#     4 60
#     5 170
#     6 102
#     7 36
#     8 33
#     9 160
#     10 165;

# param T := 188;
# param R := 170;
# param M := 1000000;

# end;

# ----------------------------------------------------------------------------------------------------------------

# sm20

# data;

# set J := 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20;
# set I := 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17;

# param p := 
#     1 33
#     2 29
#     3 100
#     4 84
#     5 136
#     6 42
#     7 57
#     8 143
#     9 101
#     10 119
#     11 5
#     12 53
#     13 121
#     14 127
#     15 132
#     16 46
#     17 53
#     18 94
#     19 148
#     20 69;

# param r := 
#     1 186
#     2 155
#     3 40
#     4 172
#     5 153
#     6 47
#     7 4
#     8 118
#     9 172
#     10 26
#     11 54
#     12 56
#     13 102
#     14 169
#     15 184
#     16 39
#     17 1
#     18 163
#     19 160
#     20 60;

# param T := 163;
# param R := 188;
# param M := 1000000;

# end;

# ----------------------------------------------------------------------------------------------------------------

# sm30

# data;

# set J := 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30;
# set I := 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27;

# param p := 
#     1 70
#     2 52
#     3 4
#     4 94
#     5 129
#     6 162
#     7 135
#     8 15
#     9 47
#     10 7
#     11 147
#     12 28
#     13 36
#     14 91
#     15 85
#     16 44
#     17 103
#     18 112
#     19 139
#     20 144
#     21 110
#     22 38
#     23 141
#     24 34
#     25 116
#     26 77
#     27 112
#     28 141
#     29 62
#     30 14;

# param r := 
#     1 37
#     2 166
#     3 48
#     4 4
#     5 53
#     6 5
#     7 125
#     8 181
#     9 154
#     10 93
#     11 107
#     12 78
#     13 156
#     14 71
#     15 19
#     16 26
#     17 158
#     18 79
#     19 114
#     20 5
#     21 180
#     22 34
#     23 83
#     24 3
#     25 80
#     26 175
#     27 41
#     28 7
#     29 167
#     30 165;

# param T := 165;
# param R := 181;
# param M := 1000000;

# end;