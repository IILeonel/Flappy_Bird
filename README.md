# Flappy Bird
Ahh! Flappy Bird... Quem não passou horas de nervoso jogando este jogo.
O jogo foi um sucesso em 2014, 2015 e deixou muita gente estressada, mas ja pensou como seria uma rede neural jogando? Bom, foi o que fizemos.



# Projeto
O projeto consiste basicamente em colocar uma rede neural para jogar Flappy Bird. 
Utilizamos algumas bibliotecas para isso:
* Pygame
* OS
* Random 
* Neat

No arquivo IA.txt temos as configurações do <a href="https://neat-python.readthedocs.io/en/latest/">Neat</a>, o nosso metodo escolhido para desenvolver a nossa rede neural.

# Algumas observações
* Geração: O aprendizado será por gerações, ou seja, cada vez que a rede neural não consegue passar pelos obstaculos e acabando morrendo, foi uma geração.
* População de passaros: Começamos com uma população de 100 passaros, porem, por ser uma rede neural pequena, a mesma estava aprendendo muito rapido,   então, optamos por utilizar uma população de apenas 5 passaros.

# Relatorio
Para sabermos como a nossa rede neural esta indo, colocamos um reporte por gerações:
![Captura de tela de 2023-01-27 16-08-16](https://user-images.githubusercontent.com/61874620/215272290-93e86959-30ac-41e4-b8f2-fead6a770ab3.png)

