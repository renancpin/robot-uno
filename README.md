# UNO!!

Este é o nosso UNO!

Para este trabalho, foi solicitado um programa que executasse o popular jogo de cartas, mas com uma diferença: \
_A execução é totalmente automática._ \
Os jogadores são parte do próprio programa, e não há interação com usuários humanos. \
As jogadas são mostradas na tela, e nós humanos somos meros expectadores.

Adicionalmente, para este programa, existem algumas regras predefinidas diferentes das oficiais e das usadas tradicionalmente.

## Regras diferenciadas
* _Não há cortes._ \
Talvez a maior diferença em relação ao jogo original, essa possibilidade foi deixada de lado por ser custosa em termos de tempo de desenvolvimento
* A carta inicial _é aplicada ao primeiro jogador_! \
A primeira carta foi um +4? Espero que o jogador tenha uma igual, ou um +2... \
Foi uma carta de bloqueio? Nos vemos na próxima rodada... \
A adrenalina está presente do começo ao fim, assim como o risco iminente de destruir amizades.
* Cartas +2 e +4 se acumulam! \
Você não esperava que fosse diferente, certo?
* As únicas cartas de ação são +2, +4, Bloqueios e Inverter Sentido. \
Nada de fazer silêncio ao jogar um 7, bater no cemitério ao jogar um 9 ou trocar baralhos ao jogar um 0. Quem inventou isso afinal?

## Os Jogadores
Como mencionado, os jogadores são parte do programa. \
Nossa equipe decidiu que os jogadores seriam implementados como classes, assim como as cartas, o baralho e o Mestre do jogo. \
Interação humana estava fora do escopo do trabalho, mas desta forma seria mais fácil de implementar, eventualmente.

As funções principais da classe Jogador são:
* Pegar uma carta \
Recebe uma carta geralmente entregue pelo mestre, e a adiciona à sua "mão"
* Mostrar a mão \
Útil para facilitar a apresentação na tela ao expectador
* Fazer uma jogada \
Talvez a parte mais complexa do trabalho. Existem alguns tipos diferentes de jogadas possíveis, \
assim como casos especiais _muito especiais_ (já tentou descrever as regras do UNO de maneira literal? É uma experiência desafiante)

Nosso Jogador experimenta, com cada carta, sequências de mesma cor (crescente e decrescente) ou várias cartas \
de mesma face, e armazena todas as possíveis jogadas encontradas em uma lista. \
Por fim, analisa qual possível jogada descartará mais cartas de sua mão (afinal o objetivo do jogo é descartar todas as suas cartas)

Não há dependências para este programa. Apenas execute-o no IDLE do python e assista com atenção. \
Divirta-se!
