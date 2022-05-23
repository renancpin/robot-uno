from random import randint, shuffle
from time import sleep

cores = ['Vermelho','Amarelo','Verde','Azul','Coringa']
faces = [['0','1','2','3','4','5','6','7','8','9','+2','(/)','<->','#'],['+4','#']]
tamanhoTela = 50

class Carta:
    def __init__(self, cor, face):
        if cor in cores and (face in faces[1] or face in faces[0]):
            self.cor = cor
            self.face = face
            
    def seCoringa(self, cor):
        if self.cor == 'Coringa' and cor in cores:
            self.cor = cor
            print(f'A cor escolhida foi: {cor}\n')
        elif cor == 'Coringa':
            self.cor = 'Coringa'
        
    def getCor(self):
        return self.cor

    def getFace(self):
        return self.face

    def printCarta(self, fim='\n'):
        print(' '*3 + f'{self.getFace().center(5)}{self.getCor()}',end=fim)

class Baralho:
    #preenche o baralho com as cartas existentes
    def __init__(self):
        self.cartas = []
        self.cemiterio = []
        
        for i in range(4):
            for j in range(1,13):
                for z in range(2):
                    cart = Carta(cores[i],faces[0][j])
                    self.cartas.append(cart)
            cart = Carta(cores[i],'0')
            self.cartas.append(cart)

        for i in range(4):
            for j in range(2):
                cart = Carta(cores[4],faces[1][j])
                self.cartas.append(cart)
        
        shuffle(self.cartas)
    
    #retorna a carta no topo do baralho
    def puxaCarta(self):
        if len(self.cartas) > 0:
            carta = self.cartas.pop()
            return carta
        else:
            #caso o baralho fique vazio, embaralha-se o cemitério e coloca-se no lugar do baralho
            #é preciso resetar a cor escolhida para as cartas coringa (faces '+4' e '#')
            for carta in cemiterio:
                if carta.getFace() in ['+4','#']:
                    carta.seCoringa('Coringa')
                self.cartas.append(carta)
            cemiterio = []
            shuffle(self.cartas)
            return self.puxaCarta()
    
    #recebe a lista de cartas (jogada do usuário anterior) e a adiciona ao cemitério
    def descartar(self, cartas):
        for carta in cartas:
            self.cemiterio.append(carta)
            
class Jogador:
    def __init__(self):
        self.cartas = []
    
    def mostraMao(self):
        for cart in self.cartas:
            cart.printCarta()
            #print('')

    #recebe uma carta e a adiciona à mão do jogador
    def pegaCarta(self, carta):
        if not (carta is None):
            self.cartas.append(carta)
    
    #define as jogadas possíveis de acordo com a ultima carta recebida
    #gera dor e sofrimento aos desenvolvedores
    def jogada(self, ultimaCarta):
        possiveis = []
        #verificar cada carta da mão, se encaixa na jogada possível
        for i in range(len(self.cartas)):
            card = self.cartas[i]
            
            # caso seja elegível, calcular um número de jogadas possíveis a partir desta,
            # como cartas de mesma face e cores diferentes, ou sequencias numéricas de mesma cor
            # cartas +2 e +4 são especiais, em termos de jogada
            # se o jogador estiver em risco de puxar cartas, deve procurar sair desta situação com outro +2 ou +4
            # caso o risco tenha passado (o jogador anterior puxou as cartas), 
            # há mais jogadas possíveis como cartas da mesma cor e face diferente
            if card.getFace() == ultimaCarta.getFace() or \
               (card.getCor() == ultimaCarta.getCor() and card.getCor() != 'Coringa' and  (card.getFace() == '+2' or ultimaCarta.getFace() != '+4')) or \
               (card.getCor() == 'Coringa' and (card.getFace() == '+4' or not('+' in ultimaCarta.getFace()))):
                
                possiveis.append([self.cartas[i]])
                for j in range(len(self.cartas)):
                    if j != i and self.cartas[j].getFace() == card.getFace():
                        possiveis[-1].append(self.cartas[j])

                if card.getFace() in ['0','1','2','3','4','5','6','7','8','9']:
                    z = int(card.getFace())
                    a = z
                    possiveis.append([self.cartas[i]])
                    possiveis.append([self.cartas[i]])
                    for k in range(len(self.cartas)):
                        for j in range(len(self.cartas)):
                            if j != i and self.cartas[j].getCor() == card.getCor():
                                if self.cartas[j].getFace() in ['0','1','2','3','4','5','6','7','8','9']:
                                    if int(self.cartas[j].getFace()) == z + 1:
                                        z += 1
                                        possiveis[-1].append(self.cartas[j])
                                        break
                                    elif int(self.cartas[j].getFace()) == a - 1:
                                        a -= 1
                                        possiveis[-2].append(self.cartas[j])
                                        break
        
        if len(possiveis) == 0:
            return []

        jogcerta = []
        
        for jog in possiveis:
            if len(jog) > len(jogcerta):
                jogcerta = jog
        
        for i in jogcerta:
            self.cartas.remove(i)
        
        return jogcerta

class MestreJogo:
    # iniciar o jogo, criar os jogadores e o baralho e processar as jogadas
    def __init__(self, nJogadores):
        self.jogoHorario = 1
        self.jogadores = []
        self.baralho = Baralho()
        
        for i in range(nJogadores):
            jog = Jogador()
            for j in range(7):
                jog.pegaCarta(self.baralho.puxaCarta())
            self.jogadores.append(jog)
    
    def Jogo(self):
        # função auxiliar apenas para definir o próximo jogador, 
        # baseado no sentido do jogo e no acumulo de cartas de bloqueio:
        def proxJog(atual, pular):
            i = atual + self.jogoHorario * (1+pular)
            
            while i >= len(self.jogadores):
                i -= len(self.jogadores)
            while i < 0:
                i += len(self.jogadores)

            return i
        
        ganhador = None
        i = -1
        puxar = 0
        pular = 0
        # a carta inicial é retirada pelo mestre e começa a valer para o primeiro jogador
        # considerando seus efeitos especiais, se houver
        ultima = self.baralho.puxaCarta()
        cartas = [ultima]

        print(f'Nº de Jogadores: {len(self.jogadores)}')
        print('Iniciando jogo',end='')
        sleep(1)
        print('.',end='')
        sleep(1)
        print('.',end='')
        sleep(1)
        print('.')
        sleep(1)
        print('-'*tamanhoTela)
        print('Primeira Carta ',end='')
        
        #O loop principal
        while ganhador is None:

            if cartas != []:
                self.baralho.descartar(cartas)
                
                print('Jogada:\n')
                for cart in cartas:
                    if cart is cartas[-1]:
                        cart.printCarta('')
                        print('   << Carta no topo')
                    else:
                        cart.printCarta()
                        
                    if cart.getFace() == '+2':
                        puxar += 2
                    elif cart.getFace() == '(/)':
                        pular += 1
                    elif cart.getFace() == '<->':
                        self.jogoHorario = (self.jogoHorario) * (-1)
                    elif cart.getFace() == '+4':
                        puxar += 4
                print('')
                
            if len(self.jogadores[i].cartas) == 1:
                print(f'Jogador {i+1} gritou: UNO!\n')
            elif len(self.jogadores[i].cartas) == 0:
                #de acordo com as regras definidas, sua ultima jogada não pode ser uma carta de ação
                if ultima.getFace() in ['#','+2','+4','(/)','<->']:
                    print(f'Não se pode bater com uma carta de ação.\n Jogador {i+1} puxou uma carta!')
                    self.jogadores[i].pegaCarta(self.baralho.puxaCarta())
                else:
                    print(f'O ganhador é: Jogador {i+1}!!')
                    break
                    
            # uma carta coringa precisa ter sua cor definida
            # neste caso, o proprio mestre escolhe aleatoriamente, pois não há jogadores humanos
            if ultima.getCor() == 'Coringa':
                ultima.seCoringa(cores[randint(0,3)])
                
            i = proxJog(i,pular)
            pular = 0
            
            print('-'*tamanhoTela + '\n' + f'   Próximo: Jogador {i+1}',end='')
            sleep(1)
            print('.',end='')
            sleep(1)
            print('.',end='')
            sleep(1)
            print('.')
            sleep(1)
            print('-'*tamanhoTela)
            
            print(f'Mão do Jogador {i+1}:\n')
            self.jogadores[i].mostraMao()
            print('\n' + '*'*tamanhoTela)
            
            # puxar > 0 significa que existe risco de puxar cartas para o próximo jogador
            if puxar > 0:
                if ultima.getFace() == '+4':
                    # neste caso especial, o jogador só pode escapar de puxar cartas se 
                    # jogar outro +4, ou um +2 da cor escolhida
                    # nesse caso, o jogador irá enxergar a carta +4 com a cor definida para saber o que fazer
                    cartas = self.jogadores[i].jogada(ultima)
                    if cartas == []:
                        # se não foi possivel se salvar, o jogador puxará as cartas,
                        # e o mestre mostrará uma carta "falsa", com a face '#' e a cor definida anteriormente
                        # pois o jogador seguinte poderá jogar qualquer carta daquela cor
                        print(f'O Jogador {i+1} puxou {puxar} cartas!!\n')
                        for pux in range(puxar):
                            self.jogadores[i].pegaCarta(self.baralho.puxaCarta())
                        puxar = 0
                        ultima = Carta(ultima.getCor(), '#')
                    else:
                        ultima = cartas[-1]
                else:
                    # neste caso especial, o jogador pode jogar uma carta +4 ou uma carta +2 de qualquer cor
                    # mas se enxergar um +2 de cor definida, tentará jogar qualquer carta daquela cor
                    # portanto, o mestre mostrará uma carta "falsa" de face '+2' e cor 'Coringa'
                    cartas = self.jogadores[i].jogada(Carta('Coringa','+2'))
                    if cartas == []:
                        # se o jogador puxou as cartas, agora o proximo pode enxergar o +2 com cor definida 
                        # pois não estará mais sob risco de puxar, e pode jogar qualquer carta daquela cor
                        print(f'O Jogador {i+1} puxou {puxar} cartas!!\n')
                        for pux in range(puxar):
                            self.jogadores[i].pegaCarta(self.baralho.puxaCarta())
                        puxar = 0
                    else:
                        ultima = cartas[-1]
            else:
                # caso padrão
                cartas = self.jogadores[i].jogada(ultima)
                if cartas == []:
                    # se o jogador retornou uma lista vazia, significa que não pôde jogar
                    # segundo as regras, nesse caso deve puxar uma carta e tentar jogar novamente
                    # e o mestre deve informar isso a todos
                    print(f'O Jogador {i+1} puxou uma carta',end='')
                    self.jogadores[i].pegaCarta(self.baralho.puxaCarta())
                    cartas = self.jogadores[i].jogada(ultima)
                    
                    # caso após puxar a carta, tenha conseguido jogar, o jogo segue
                    if cartas != []:
                        print('!\n')
                        ultima = cartas[-1]
                    # se não conseguiu, o mestre completa a informação
                    else:
                        print(' e não jogou!\n')
                else:
                    ultima = cartas[-1]
            
def main():
    # chamar um novo jogo com 3 jogadores
    mestre = MestreJogo(3)
    mestre.Jogo()
    
    
if __name__ == '__main__':
    main()
